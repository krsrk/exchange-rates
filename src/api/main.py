import json

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from jwt_gen.jwtcreator import JwtCreator
from orm.peewee import OrmEngine
from models import User, ExchangeRate
from repositories import UserRepository

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Server Events
@app.on_event('startup')
def startup():
    if OrmEngine().is_connection_closed():
        OrmEngine().connect()

    OrmEngine().migrate([User, ExchangeRate])


@app.on_event('shutdown')
def shutdown():
    if not OrmEngine().is_connection_closed():
        OrmEngine().close_connection()


# Server Routes
@app.get("/")
async def read_root():
    return {"message": "Hello World"}


# Auth Routes
@app.get("/auth")
async def auth():
    return {"message": "Auth Service"}


@app.post("/auth/login")
async def auth_login(request: Request):
    body = await request.json()
    user_name = body['username']
    password = body['password']
    user_payload = UserRepository().auth(user_name, password)

    if not user_payload:
        raise HTTPException(status_code=404, detail="User not found!")

    token = JwtCreator(payload={
        'id': str(user_payload['id']),
        'user_name': user_payload['username'],
        'password': user_payload['password'],
        'request_limit': user_payload['request_limit']
    }).createToken()

    return {"token": token}

