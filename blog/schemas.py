from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body: str
    published = True
    user_id:int

class Blogs(BaseModel):
    title:str
    body:str 
    published:bool

    class Config:
        orm_mode=True



class User(BaseModel):
    username: str
    email: str
    password: str


class ShowUser(BaseModel):
    id: int
    username: str
    email: str
    blogs:List[Blogs]

    class Config:
        orm_mode = True

class Creator(BaseModel):
    id:int
    username:str

    class Config:
        orm_mode=True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: Creator
    class Config:
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str