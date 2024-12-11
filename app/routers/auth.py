from fastapi import Body, Response, status, HTTPException, Depends, APIRouter, FastAPI
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)): this is theoriginal model the
# next line is the dependacy modelthis  is because of fastapi
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first() initial model aswell
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #oauth2passwordrequestformstores email as username
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #create a token
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    #return the token
    return{"access_token": access_token, "token_type":"bearer"}

    