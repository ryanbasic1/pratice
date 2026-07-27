from fastapi import FastAPI

from app.routers import routes

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-one-theta-tznvtxa4h7.vercel.app",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5500",

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

