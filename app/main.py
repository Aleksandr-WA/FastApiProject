from fastapi import FastAPI
from app.models.models import User

app = FastAPI()


@app.get("/")
async def get_main_page():
    return 'welcome to my main page'


@app.post("/user")
async def create_user(user: User):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18
    }

# uvicorn app.main:app --reload
