from fastapi import Body, Response, status, HTTPException, Depends, APIRouter, FastAPI
from .. import models,schemas,oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# #@router.get("/", response_model=List[schemas.Post])
# @router.get("/")
# def get_posts(db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search: Optional[str] = ""):
#     #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id) #this to get current user all posts
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #to get all posts in the database regardless of user

#     #results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

#     results = db.query(models.Post, func.count(models.Votes.post_id).label("votes"))\
#     .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
#     .group_by(models.Post.id).all()

#     return results

    
#     # cursor.execute(""" SELECT * FROM posts """)
#     # posts = cursor.fetchall()
#     # print(posts)
    
@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes"))\
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).limit(limit).offset(skip).all()

    # Prepare the results in the format that matches the PostWithVotes model
    return [
        {"title": post.title, "content": post.content, "created_at": post.created_at, 
          "votes": vote_count} 
        for post, vote_count in results
    ]



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() #to push the changes out and commit it to the database
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (int(id),))  # Pass as a tuple
    # post = cursor.fetchone()
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
   
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)



    new_post = post_query.first()

    if new_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
    
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()
    
    return post_query.first()
    