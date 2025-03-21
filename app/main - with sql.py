from typing import Optional
from fastapi import FastAPI,status,Response,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='seydou',
                          cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database was connected succesfully!")
        break

    except Exception as error:
        print("Database connection failed")
        print(f"The error was {error}")
        time.sleep(2)

my_posts=[
    {"title":"title of post 1","content":"content of post 1","id":1},
    {"title":"favorite foods","content":"I like pizzas","id":2}
]

# Define find post function

def find_post(id):
    for p in my_posts:
        print(p)
        if p['id']==id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if int(p['id'])==id:
            return i     
    

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published))
    
    new_post=cursor.fetchone()
    conn.commit()
    return{"data":new_post}

@app.get("/posts/{id}")
def get_posts(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s""",(str(id)))
    postfound=cursor.fetchone()
    if not postfound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
        
    return {"data":postfound}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id)))
    deleted_post=cursor.fetchone()
    conn.commit()
    index=find_post_index(id)
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
                   (post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
   
    return {"data":updated_post}
    