"""
main page
"""
from fastapi import FastAPI,Request, HTTPException
from uuid import UUID, uuid4
from typing import List
from database import get_session
from models import Product, User, Order
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import astrapy

app = FastAPI()

# Initialize the AstraDB session
client = get_session()

# Database configurations
keyspace = "default_keyspace" 
products_table = "products"  
users_table = "users"
orders_table = "orders" 

#Api endpoint
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT") 

# Homepage view
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Products 
# Get all products

#client = DataAPIClient()

@app.get("/products")
async def get_products():
    database = client.get_database(api_endpoint=api_endpoint)
    if database:
        # Add further logic if necessary for fetching data, etc.
        return {"message": "Successfully connected to the database."}
    else:
        # If database connection fails for any reason not covered above
        raise HTTPException(status_code=400, detail="Failed to connect to the database.")

# Create a new product
@app.post("/products", response_model=Product)
async def create_product(product: Product):
    product.product_id = uuid4()  # Generate new UUID
    client.insert_row(keyspace, products_table, product.dict())
    return product

# Get a single product by ID
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: UUID):
    product = client.get_by_id(keyspace, products_table, str(product_id))
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Update a product
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: UUID, product: Product):
    product.product_id = product_id
    client.update_row(keyspace, products_table, str(product_id), product.dict())
    return product

# Delete a product
@app.delete("/products/{product_id}")
async def delete_product(product_id: UUID):
    client.delete_row(keyspace, products_table, str(product_id))
    return {"detail": "Product deleted"}


# Users 
# Get all users
@app.get("/users", response_model=List[User])
async def get_users():
    response = client.get_all(keyspace, users_table)
    return response

# Create a new user
@app.post("/users", response_model=User)
async def create_user(user: User):
    user.user_id = uuid4()  #new UUID
    client.insert_row(keyspace, users_table, user.dict())
    return user

# Get a single user by ID
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    user = client.get_by_id(keyspace, users_table, str(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: User):
    user.user_id = user_id
    client.update_row(keyspace, users_table, str(user_id), user.dict())
    return user

# Delete a user
@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID):
    client.delete_row(keyspace, users_table, str(user_id))
    return {"detail": "User deleted"}


# Orders 
# Get all orders
@app.get("/orders", response_model=List[Order])
async def get_orders():
    response = client.get_all(keyspace, orders_table)
    return response

# Create a new order
@app.post("/orders", response_model=Order)
async def create_order(order: Order):
    order.order_id = uuid4()  # for new UUID
    client.insert_row(keyspace, orders_table, order.dict())
    return order

# Get a single order by ID
@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: UUID):
    order = client.get_by_id(keyspace, orders_table, str(order_id))
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Update an order
@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: UUID, order: Order):
    order.order_id = order_id 
    client.update_row(keyspace, orders_table, str(order_id), order.dict())
    return order

# Delete an order
@app.delete("/orders/{order_id}")
async def delete_order(order_id: UUID):
    client.delete_row(keyspace, orders_table, str(order_id))
    return {"detail": "Order deleted"}
