import jwt
from .exceptionshandler import UnsupportedAlgoException


class JwtCreator:
    payload = {
        "sub": "619",
        "name": "Krs Lo",
        "nickname": "krsrk",
        "description": "Python Jwt Creator by krsrk"
    }
    secret = '$2a$12$.41LPyWgKri1tIRNX4hUDeDj1BP3lB5tOG1RPN2R77lJ0htiEOk5.'
    algo = ''
    supported_algos = ['HS256']

    def __init__(self, payload=None, secret='', algo='HS256'):
        self.algo = algo
        if not self.isAlgoSupported():
            raise UnsupportedAlgoException

        if payload:
            self.payload = payload

        if secret != '':
            self.secret = secret

    def createToken(self):
        return jwt.encode(
            payload=self.payload,
            key=self.secret,
            algorithm=self.algo
        )

    def decodeToken(self, token):
        try:
            return jwt.decode(token, key=self.secret, algorithms=[self.algo, ])
        except Exception as e:
            print(str(e))
            return None

    def isAlgoSupported(self):
        return self.algo in self.supported_algos
