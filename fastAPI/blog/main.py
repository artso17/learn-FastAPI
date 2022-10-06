from typing import List
from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models, crud
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create-blog')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = crud.create_blog(db, request)
    return new_blog


""" Blogs """


@app.get('/blog/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def query(id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog(id, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Current blog not found')
    return blog


@app.get('/blogs')
def query(skip: int, limit: int, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Blogs not found')
    return blogs


@app.delete('/delete/blog', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    db_blogs = crud.get_blog(id, db)
    if not db_blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Current blog not found')
    return crud.delete_blog(id, db)


@app.put('/update/blog', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    db_blogs = crud.get_blog(id, db)
    if not db_blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Current blog not found')
    return crud.update_blog(id, db, request)


"""Users"""


@app.post('/create/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, request)
    return new_user


@app.get('/user', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int = None, username: str = None, db: Session = Depends(get_db)):
    if id and username:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = crud.get_user(db, user_id=id, user_username=username)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='Current user not founds')
    return user


@app.get('/users/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)
