from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

# 7:28:50 time video
# postgres docker container
# docker run --name postgres-container -e POSTGRES_USER=leo -e POSTGRES_PASSWORD=psw -p 5432:5432 -v /data:/var/lib/postgresql/data -d postgres

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http:localhost:3000",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.posts_router)
app.include_router(users.users_router)
app.include_router(auth.auth_router)