from fastapi import FastAPI

from app.api import appeal, auth

app = FastAPI()
app.include_router(appeal)
app.include_router(auth)
