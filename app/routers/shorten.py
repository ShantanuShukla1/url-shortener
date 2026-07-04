from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
import string
import random

from app.database import get_db
from app.models import URL
from app.cache import get_cached_url, set_cached_url

router = APIRouter()

class URLCreate(BaseModel):
    original_url: str

class URLResponse(BaseModel):
    short_code: str
    original_url: str

    class Config:
        from_attributes = True

def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

@router.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    # Try a few times in case of short code collisions
    for _ in range(5):
        short_code = generate_short_code()
        db_url = URL(short_code=short_code, original_url=payload.original_url)
        db.add(db_url)
        try:
            db.commit()
            db.refresh(db_url)
            return db_url
        except IntegrityError:
            db.rollback()
            continue
    raise HTTPException(status_code=500, detail="Could not generate a unique short code")

from fastapi.responses import RedirectResponse

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    # Check Redis cache first
    cached = get_cached_url(short_code)
    if cached:
        return RedirectResponse(url=cached)

    # Fall back to Postgres
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    db_url.click_count += 1
    db.commit()

    set_cached_url(short_code, db_url.original_url)

    return RedirectResponse(url=db_url.original_url)