from fastapi import APIRouter,status,Depends
from typing import List
from sqlalchemy.orm import Session
from .. import database,models,schemas,crud

router=APIRouter(
    prefix='/blog',
    tags=['blogs']
)
get_db=database.get_db

@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = crud.create_blog(db, request)
    return new_blog


@router.get('/', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def query(id: int, db: Session = Depends(get_db)):
    blog = crud.get_blog(id, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Current blog not found')
    return blog


@router.get('/')
def query(skip: int, limit: int, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Blogs not found')
    return blogs


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    db_blogs = crud.get_blog(id, db)
    if not db_blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Current blog not found')
    return crud.delete_blog(id, db)


@router.put('/', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    db_blogs = crud.get_blog(id, db)
    if not db_blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Current blog not found')
    return crud.update_blog(id, db, request)