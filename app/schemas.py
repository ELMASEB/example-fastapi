from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    model_config = {"from_attributes": True}

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at: datetime
    owner_id:int
    owner:UserOut

    model_config = {"from_attributes": True}
    # pydantic V1
    #class Config():
    #    orm_mode=True

class PostOut(BaseModel):
    Post:Post
    votes:int
    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
    post_id:int
    dir:Annotated[int, conint(ge=0,le=1)]
