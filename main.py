from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import sesion_local, engine
from sqlalchemy.orm import Session

app = FastAPI()
models.base.metadata.create_all(bind=engine)

class Postbase(BaseModel):
    title: str
    content : str
    user_id : int

class UserBase(BaseModel):
    username : str


def get_db():
    db = sesion_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Postbase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()



@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")
    return user



@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post not found")
    return post
