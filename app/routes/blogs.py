from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Blog
from app.schemas import BlogCreate, BlogResponse

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.get("/", response_model=list[BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    new_blog = Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(blog_id: int, blog_data: BlogCreate, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.title = blog_data.title
    blog.content = blog_data.content
    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}
