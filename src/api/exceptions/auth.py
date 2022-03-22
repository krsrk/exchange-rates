from fastapi import HTTPException
from jwt_gen.jwtcreator import JwtCreator
from repositories import UserRepository


class AuthTokenNotFoundException:
    auth_token_key = 'authorization'

    def __init__(self, value, http_exception=True):
        if not self.auth_token_key in value:
            if http_exception:
                raise HTTPException(status_code=401, detail="Invalid Authentification Request!")
            else:
                raise Exception("Invalid Authentification Request!")


class InvalidAuthBearerTokenException:

    def __init__(self, value, http_exception=True):
        auth_header_data = value.split()
        if not auth_header_data[0] == 'Bearer':
            if http_exception:
                raise HTTPException(status_code=406, detail="Invalid Header Auth Token!")
            else:
                raise Exception("Invalid Auth Token!")


class InvalidSignedTokenException:

    def __init__(self, value, http_exception=True):
        # token = value
        # decode_token = JwtCreator().decodeToken(token)
        if not value:
            if http_exception:
                raise HTTPException(status_code=406, detail="Invalid Token!")
            else:
                raise Exception("Invalid Token!")


class InvalidUserException:

    def __init__(self, value, http_exception=True):
        if not value:
            if http_exception:
                raise HTTPException(status_code=401, detail="Invalid User!")
            else:
                raise Exception("Invalid User!")
