from sqlalchemy.orm import Session
from . import models, schemas, utils


def get_blog(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    return blog


def get_blogs(db: Session, skip=0, limit=5):
    blogs = db.query(models.Blog).offset(skip).limit(limit).all()
    return blogs


def create_blog(db: Session, request):
    new_blog = models.Blog(title=request.title,
                           body=request.body, published=request.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def update_blog(id: int, db: Session, request):
    db.query(models.Blog).filter(models.Blog.id == id).update(
        request.dict(), synchronize_session=False)
    db.commit()


def delete_blog(id: int, db: Session):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()


def create_user(db: Session, request):
    new_user = models.User(username=request.username,
                           email=request.email, password=utils.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id=None, user_username=None):
    if user_id:
        user = db.query(models.User).filter(models.User.id == user_id).first()
    elif user_username:
        user = db.query(models.User).filter(
            models.User.username == user_username).first()
    return user


def get_all_users(db: Session):
    return db.query(models.User).all()
