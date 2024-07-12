from fastapi import FastAPI
from app.models.models import User, Feedback

app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

fake_lst_db = []


@app.get("/")
async def get_main_page():
    return "Welcome my main page"


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.get("/users/")
async def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


@app.post("/user")
async def create_user(user: User):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18
    }


@app.post("/feedback")
async def leave_a_review(feedback: Feedback):
    fake_lst_db.append({"name": feedback.name, "message": feedback.message})
    return {"message": f"Feedback received. Thank you, {feedback.name}!"}


# uvicorn app.main:app
