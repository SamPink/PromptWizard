# backend.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Optional
import uvicorn

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to `origins` in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "sqlite:///./prompts.db"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)  # Needed for SQLite

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# SQLAlchemy ORM Model
class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contents = Column(Text, nullable=False)

# Pydantic Models
class PromptCreate(BaseModel):
    name: str
    contents: str

class PromptUpdate(BaseModel):
    name: Optional[str] = None
    contents: Optional[str] = None

class PromptResponse(BaseModel):
    id: int
    name: str
    contents: str

    class Config:
        orm_mode = True

# Create the database tables
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database tables at startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# API Endpoints

@app.get("/api/prompts", response_model=List[PromptResponse])
def get_prompts(db: Session = Depends(get_db)):
    try:
        prompts = db.query(Prompt).all()
        return prompts
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/prompts", response_model=PromptResponse, status_code=201)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    try:
        db_prompt = Prompt(name=prompt.name, contents=prompt.contents)
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        return db_prompt
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/prompts/{prompt_id}", response_model=PromptResponse)
def update_prompt(prompt_id: int, prompt_update: PromptUpdate, db: Session = Depends(get_db)):
    try:
        db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not db_prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        if prompt_update.name is not None:
            db_prompt.name = prompt_update.name
        if prompt_update.contents is not None:
            db_prompt.contents = prompt_update.contents
        
        db.commit()
        db.refresh(db_prompt)
        return db_prompt
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    try:
        db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not db_prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        db.delete(db_prompt)
        db.commit()
        return
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_index():
    return FileResponse("index.html")

# Run the app with: uvicorn backend:app --host 0.0.0.0 --port 8300 --reload
if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8300, reload=True)
