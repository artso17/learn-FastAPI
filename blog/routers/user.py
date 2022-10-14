from fastapi import APIRouter,Depends,status,HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import database,models,schemas,crud

router=APIRouter(
    prefix='/user',
    tags=['users']
)
get_db=database.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return crud.create_user(db, request)


@router.get('/', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int = None, username: str = None, db: Session = Depends(get_db)):
    if id and username:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = crud.get_user(db, user_id=id, user_username=username)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='Current user not founds')
    return user


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)
