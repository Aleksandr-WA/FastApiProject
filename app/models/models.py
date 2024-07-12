from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    is_subscribed: bool


class Users(BaseModel):
    username: str
    password: str
