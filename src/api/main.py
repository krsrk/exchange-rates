import json

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from exceptions.auth import AuthTokenNotFoundException, InvalidAuthBearerTokenException, InvalidSignedTokenException, \
    InvalidUserException
from jwt_gen.jwtcreator import JwtCreator
from orm.peewee import OrmEngine
from models import User, ExchangeRate
from repositories import UserRepository, ExchangeRateRepository
from services.service_provider import ServiceRatesProvider

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


@app.post("/auth/register")
async def register(request: Request):
    body = await request.json()
    user_name = body['username']
    password = body['password']

    created_user = UserRepository().create(user_name, password)

    if not created_user:
        raise HTTPException(status_code=500, detail="Created user failed!")

    return {"message": "User created satisfactory!"}


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
        'password': user_payload['password']
    }).createToken()

    return {"token": token}


@app.put("/exchange/rates")
async def get_exchange_rates(request: Request):
    # Validations
    AuthTokenNotFoundException(request.headers)
    InvalidAuthBearerTokenException(request.headers['authorization'])
    token = request.headers['authorization'].split()
    decode_token = JwtCreator().decodeToken(token[1])
    InvalidSignedTokenException(decode_token)
    auth_user = UserRepository().auth(decode_token['user_name'], decode_token['password'])
    InvalidUserException(auth_user)

    fixer_data = [
        ServiceRatesProvider('fixer').dispatch().get_exchange_rates(),
        ServiceRatesProvider('banxico').dispatch().get_exchange_rates(),
        ServiceRatesProvider('dof').dispatch().get_exchange_rates()
    ]
    response_data = ExchangeRateRepository().upsert(user_id=str(auth_user['id']), fix_data=fixer_data)

    return response_data
