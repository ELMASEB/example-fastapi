from typing import List, Optional
from fastapi import Depends, FastAPI,status,Response,HTTPException,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import oauth2
from .. import models,schemas,utils
from ..database import get_db

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
              limit:int=10,skip: int=0 ,search:Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()

    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                        models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()

    
    
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session=Depends(get_db),
                 current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #               (post.title,post.content,post.published))
    
    #new_post=cursor.fetchone()
    #conn.commit()
    #new_post=models.Post(title=post.title,content=post.content,published=post.published)
    
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_posts(id:int,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id=%s""",(str(id)))
    #postfound=cursor.fetchone()
    #postfound=db.query(models.Post).filter(models.Post.id==id).first()

    postfound=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                        models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    if not postfound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    
    #if postfound.owner_id!=current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to perform this action")
    
        
    return postfound


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id)))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    deleted_posts=db.query(models.Post).filter(models.Post.id==id)
    if deleted_posts.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    
    if deleted_posts.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    deleted_posts.delete(synchronize_session=False)
    db.commit()
    
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_posts(id:int,post:schemas.PostCreate,db: Session=Depends(get_db),
                 current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
    #               (post.title,post.content,post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    
    if updated_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(),synchronize_session=False)

    db.commit()
   
    return post_query.first()
    
