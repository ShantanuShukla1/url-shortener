from fastapi import FastAPI
from app.database import Base, engine
from app.routers import shorten

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Distributed URL Shortener")

app.include_router(shorten.router)

@app.get("/")
def root():
    return {"message": "URL Shortener API is running"}