from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import database,schemas,utils,crud

get_db=database.get_db

router = APIRouter(
    tags=['authentication']
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user= crud.get_user(db,user_username=request.username)
    if not user: raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not utils.verify_password(user.password, request.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    
    access_token = utils.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
