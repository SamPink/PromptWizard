# backend.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Optional
import uvicorn
import logging
import sys
import os

from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.exc import SQLAlchemyError

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Starting PromptWizard application")

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
logger.info(f"Database URL: {DATABASE_URL}")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)  # Needed for SQLite

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# SQLAlchemy ORM Models
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    prompts = relationship("Prompt", back_populates="category", cascade="all, delete-orphan")

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contents = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="prompts")

# Pydantic Models
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PromptCreate(BaseModel):
    name: str
    contents: str
    category_id: Optional[int] = None

class PromptUpdate(BaseModel):
    name: Optional[str] = None
    contents: Optional[str] = None
    category_id: Optional[int] = None

class PromptResponse(BaseModel):
    id: int
    name: str
    contents: str
    category_id: Optional[int] = None

    class Config:
        from_attributes = True

# Create the database tables
def create_db_and_tables():
    logger.info("Creating database and tables")
    Base.metadata.create_all(bind=engine)
    logger.info("Database and tables created")

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
    logger.info("Running startup event")
    create_db_and_tables()
    logger.info("Startup complete")

# API Endpoints

@app.get("/api/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Category).all()
        return [CategoryResponse(id=category.id, name=category.name) for category in categories]
    except SQLAlchemyError as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/categories", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        db_category = Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return CategoryResponse(id=db_category.id, name=db_category.name)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/api/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Attempting to delete category with id: {category_id}")
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            logger.warning(f"Category with id {category_id} not found")
            raise HTTPException(status_code=404, detail="Category not found")
        
        logger.info(f"Deleting category: {db_category.name}")
        db.delete(db_category)
        db.commit()
        logger.info(f"Category {category_id} deleted successfully")
        return
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/prompts", response_model=List[PromptResponse])
def get_prompts(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        if category_id:
            prompts = db.query(Prompt).filter(Prompt.category_id == category_id).all()
        else:
            prompts = db.query(Prompt).all()
        return [PromptResponse(id=prompt.id, name=prompt.name, contents=prompt.contents, category_id=prompt.category_id) for prompt in prompts]
    except SQLAlchemyError as e:
        logger.error(f"Error fetching prompts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/prompts", response_model=PromptResponse, status_code=201)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received prompt data: {prompt}")
        db_prompt = Prompt(name=prompt.name, contents=prompt.contents, category_id=prompt.category_id)
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        logger.info(f"Created prompt: {db_prompt}")
        return PromptResponse(id=db_prompt.id, name=db_prompt.name, contents=db_prompt.contents, category_id=db_prompt.category_id)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

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
        if prompt_update.category_id is not None:
            db_prompt.category_id = prompt_update.category_id
        
        db.commit()
        db.refresh(db_prompt)
        return PromptResponse(id=db_prompt.id, name=db_prompt.name, contents=db_prompt.contents, category_id=db_prompt.category_id)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

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
        logger.error(f"Error deleting prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_index():
    logger.info("Serving index.html")
    return FileResponse("index.html")

# Run the app with: uvicorn backend:app --host 0.0.0.0 --port 8300 --reload
if __name__ == "__main__":
    logger.info("Starting uvicorn server")
    uvicorn.run("backend:app", host="0.0.0.0", port=8300, reload=True)

logger.info("Application shutdown")
