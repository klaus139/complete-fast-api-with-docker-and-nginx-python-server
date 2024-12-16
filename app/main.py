from fastapi import  FastAPI
from . import models
from .database import engine
from .routers import post, user,auth,voting
from .config import settings

print(settings.database_password)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(voting.router)

@app.get("/")
async def read_root():
    return {"Hello": "Welcome to my apiddddww"}

