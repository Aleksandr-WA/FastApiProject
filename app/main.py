from fastapi import FastAPI
from app.models.models import User

app = FastAPI()


@app.get("/")
def get_main_page():
    return 'welcome to my main page 11111111'


@app.post("/user")
def create_user(user: User):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18
    }

# uvicorn app.main:app --reload
