from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import itertools

app = FastAPI(title="Order Service")

# --- In-memory "database" ---
orders_db = {}
id_counter = itertools.count(1)


# --- What an Order looks like ---
class OrderCreate(BaseModel):
    user_id: int
    item: str
    quantity: int


class Order(BaseModel):
    id: int
    user_id: int
    item: str
    quantity: int
    status: str


# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "Order Service is running"}


@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    new_id = next(id_counter)
    new_order = {
        "id": new_id,
        "user_id": order.user_id,
        "item": order.item,
        "quantity": order.quantity,
        "status": "pending",
    }
    orders_db[new_id] = new_order
    return new_order


@app.get("/orders", response_model=list[Order])
def list_orders():
    return list(orders_db.values())


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    del orders_db[order_id]
    return {"message": f"Order {order_id} deleted", "deleted_order": order}
