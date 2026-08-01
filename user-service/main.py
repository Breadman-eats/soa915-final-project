from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import itertools

app = FastAPI(title="User Service")

# --- In-memory "database" (just a Python dict for now) ---
users_db = {}
id_counter = itertools.count(1)


# --- What a User looks like ---
class UserCreate(BaseModel):
    name: str
    email: str


class User(BaseModel):
    id: int
    name: str
    email: str


# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "User Service is running"}


@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    new_id = next(id_counter)
    new_user = {"id": new_id, "name": user.name, "email": user.email}
    users_db[new_id] = new_user
    return new_user


@app.get("/users", response_model=list[User])
def list_users():
    return list(users_db.values())


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": f"User {user_id} deleted", "deleted_user": user}