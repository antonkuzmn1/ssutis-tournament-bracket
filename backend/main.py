from uvicorn import main as uvicorn
from fastapi import FastAPI

from config import BACKEND_URL, BACKEND_PORT
from .api.users import router as users_router

app = FastAPI()

app.include_router(users_router)


def main() -> None:
    uvicorn(['backend.main:app',
             '--host', BACKEND_URL,
             '--port', BACKEND_PORT])
