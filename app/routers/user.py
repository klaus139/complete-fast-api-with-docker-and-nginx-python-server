from fastapi import Body, Response, status, HTTPException, Depends, APIRouter, FastAPI
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session=Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    #hash the password - user.password
    hash_passwword = utils.hash(user.password)
    user.password = hash_passwword

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user     


@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exists")
    
    return user
