from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Annotated, Optional
import models
from database import sesion_local, engine
from sqlalchemy.orm import Session

app = FastAPI()
models.base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username : str
    email : EmailStr

class CreateUser(UserBase):
    password : str

class UpdateUser(BaseModel):
    body_weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None

# class Postbase(BaseModel):
#     title: str
#     content : str
#     user_id : int


def get_db():
    db = sesion_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/{email}/post", status_code=status.HTTP_201_CREATED)
async def update_user(user: UpdateUser, email: str, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.email == email).first()
        
    # Check if the user exists
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Update user fields if they are provided
    if user.body_weight is not None:
        db_user.body_weight = user.body_weight
    if user.height is not None:
        db_user.height = user.height
    if user.age is not None:
        db_user.age = user.age
    if user.gender is not None:
        db_user.gender = user.gender
    db.commit()
    return {
        "success": True,
        "message": "user's data updated"
    }

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return {
            "success": True,
            "message": "User created successfully",
            "data": {
                "username": db_user.username,
                "email": db_user.email
            }
        }


@app.post("/users/details/{email}/", status_code=status.HTTP_200_OK)
async def get_user(email: str, db: db_dependency):
    user = db.query(models.User).filter(models.User.email == email).first() 
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
    return {
        "success" : True,
        "message" : "user's data retrived successfully",
        "data": {
            "username": user.username,
            "email": user.email,    
            "body_weight": user.body_weight,
            "age": user.age,
            "height": user.height,
            "gender": user.gender
        }
    }

@app.post("/users/auth/{email}/", status_code=status.HTTP_200_OK)
async def validate_user(email: str, db: db_dependency):

    db_user = db.query(models.User).filter(models.User.email == email).first()
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="email not found")
    if db_user:
        return {
            "success": True,
            "message": "User exists",
            "data": {
                "email": db_user.email,
                "password": db_user.password
            }
        }

# @app.post("/posts/", status_code=status.HTTP_201_CREATED)
# async def create_post(post: Postbase, db: db_dependency):
#     db_post = models.Post(**post.dict())
#     db.add(db_post)
#     db.commit()



# @app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
# async def get_user(user_id: int, db: db_dependency):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
#     return user



# @app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
# async def get_post(post_id: int, db: db_dependency):
#     post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if not post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post not found")
#     return post
