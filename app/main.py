from fastapi import FastAPI

from .routers import product_routers, order_routers


app = FastAPI()

app.include_router(product_routers.router)
app.include_router(order_routers.router)
