from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

# Product Model
class Product(BaseModel):
    product_id: UUID
    name: str
    description: str
    picture: str
    price: float
    quantity: int
    available: bool

# User Model
class User(BaseModel):
    user_id: UUID
    name: str
    username: str
    email: str
    password: str
    orders: List[UUID]  # List of order IDs

# Order Model
class Order(BaseModel):
    order_id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int
    price: float
    timestamp: Optional[str]
