from fastapi import FastAPI
import shop
from database import engine
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware 
import cart
from cart import main

secret_key = 'cart'

middleware = [
    Middleware(SessionMiddleware, secret_key=secret_key)
]

app=FastAPI(middleware=middleware)

app.mount('/static', StaticFiles(directory='static'), name='static')

shop.models.Base.metadata.create_all(bind=engine)

app.include_router(shop.main.router)
app.include_router(cart.main.router)