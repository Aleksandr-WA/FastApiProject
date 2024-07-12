from fastapi import FastAPI
from app.models.models import User

app = FastAPI()

user = User(name="John Doe", id=1)

@app.get("/")
def read_root():
    return user


# uvicorn app.main:app --reload