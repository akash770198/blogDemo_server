from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import Base, engine
from app.routes.blogs import router as blogs_router

app = FastAPI(
    title="Edumentry Blog API",
    description="A simple CRUD API for managing blog posts using FastAPI and PostgreSQL.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://blog-demo-frontend-fawn.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(blogs_router)


@app.get("/")
def read_root():
    return {"message": "Edumentry Blog API is running"}
