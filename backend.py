# backend.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import uvicorn

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./prompts.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contents = Column(Text)

Base.metadata.create_all(bind=engine)

# Pydantic models
class PromptCreate(BaseModel):
    name: str
    contents: str

class PromptUpdate(BaseModel):
    name: str = None
    contents: str = None

class PromptOut(BaseModel):
    id: int
    name: str
    contents: str

    class Config:
        orm_mode = True

# API Endpoints
@app.get("/api/prompts", response_model=List[PromptOut])
def get_prompts():
    db = SessionLocal()
    prompts = db.query(Prompt).all()
    db.close()
    return prompts

@app.post("/api/prompts", response_model=PromptOut)
def create_prompt(prompt: PromptCreate):
    db = SessionLocal()
    db_prompt = Prompt(name=prompt.name, contents=prompt.contents)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    db.close()
    return db_prompt

@app.put("/api/prompts/{prompt_id}", response_model=PromptOut)
def update_prompt(prompt_id: int, prompt: PromptUpdate):
    db = SessionLocal()
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        db.close()
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt.name is not None:
        db_prompt.name = prompt.name
    if prompt.contents is not None:
        db_prompt.contents = prompt.contents
    db.commit()
    db.refresh(db_prompt)
    db.close()
    return db_prompt

@app.delete("/api/prompts/{prompt_id}")
def delete_prompt(prompt_id: int):
    db = SessionLocal()
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        db.close()
        raise HTTPException(status_code=404, detail="Prompt not found")
    db.delete(db_prompt)
    db.commit()
    db.close()
    return {"detail": "Prompt deleted"}

# Serve static files and index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    return FileResponse("index.html")

# Uncomment the following lines to run the app directly
# if __name__ == "__main__":
#     uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
