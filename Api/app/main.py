from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
from typing import List
# import psycopg
# from psycopg.rows import dict_row
# import time

#ORM
from .database import engine
from sqlmodel import Session, select
from . import models, schemas


app = FastAPI()


# my_posts = [
#     {
#         "title": "title post 1",
#         "content": "content 1",
#         "id": "1"
#     },
#     {
#         "title": "title post 2",
#         "content": "content 2",
#         "id": "2"
#     }
# ]

# def find_post(id, idx = True):
#     for i in range(len(my_posts)):
#         if int(my_posts[i]["id"])== id:
#             if idx:
#                 return i
#             else:
#                 return my_posts[i]


# try:
#     conn = psycopg.connect(
#         host="localhost",
#         port=5432,
#         dbname="test",
#         user="postgres",
#         password="admin",
#         row_factory=dict_row
#     )
#     cursor = conn.cursor()
#     print("Database connection was successful")
# except Exception as error:
#     print(f"postgres not found : {error}")
 

@app.get("/")
def main():
    return {"message": "Hello World"}


@app.get("/posts",response_model=List[schemas.Post])
def get_posts():
    # cursor.execute("""SELECT * from posts""")
    # posts = cursor.fetchall()
    with Session(engine) as session:
        statement = select(models.Posts)
        result = session.exec(statement)
        posts = result.all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    with Session(engine) as session:
        entry = models.Posts(title=post.title, content=post.content,rating=post.rating)
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int, respose: Response):

    # cursor.execute("""SELECT * from posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    with Session(engine) as session:
        statement = select(models.Posts).where(models.Posts.id == id)
        result = session.exec(statement)
        post = result.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} not found")
        # respose.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post {id} not found"}
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, respose: Response):
    # cursor.execute("""DELETE from posts WHERE id = %s returning *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    with Session(engine) as session:
        statement = select(models.Posts).where(models.Posts.id == id)
        result = session.exec(statement)
        post = result.one()
        session.delete(post)
        session.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#title str, content str

@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def put_post(id: int, post: schemas.PostBase, respose: Response):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    with Session(engine) as session:
        statement = select(models.Posts).where(models.Posts.id == id)
        entry = session.exec(statement).first()
        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post {id} not found"
            )

        entry.title = post.title
        entry.content = post.content
        entry.published = post.published
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry

    return entry
