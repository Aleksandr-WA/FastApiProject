from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from fastapi import Request, Response
import secrets
from app.models.models import User, Feedback, UserCreate

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

fake_lst_db = []

fake_users_db = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"},
}


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


@app.post("/create_user")
async def user_create(user: UserCreate):
    return user


@app.get("/products/search")
async def search_product(keyword: str, category: str | None = None, limit: int = 10):
    return list(filter(lambda x: keyword.lower() in x['name'] and x['category'] == category, sample_products))[:limit]


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    return list(filter(lambda x: x['product_id'] == product_id, sample_products))


# Маршрут для входа в систему
@app.post("/login")
async def login(user: User, response: Response):
    if user.username in fake_users_db and fake_users_db[user.username]["password"] == user.password:
        session_token = secrets.token_hex(16)
        response.set_cookie(key="session_token", value=session_token, httponly=True)
        return {"message": "Login successful"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# Функция для проверки аутентификации
def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    # Здесь вы можете добавить дополнительную проверку токена
    return {"username": "user1"}  # Возвращаем фиктивного пользователя для примера


# Защищенный маршрут
@app.get("/user")
async def read_user(current_user: dict = Depends(get_current_user)):
    return current_user


# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn app.main:app
