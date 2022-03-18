import pytest

from .jwtcreator import JwtCreator
from .exceptionshandler import UnsupportedAlgoException


def test_if_jwt_creator_exists():
    assert JwtCreator()


def test_if_jwt_creator_has_payload_attr():
    assert JwtCreator.payload


def test_if_jwt_creator_has_secret_attr():
    assert JwtCreator.secret


def test_if_jwt_creator_has_payload_arg():
    assert JwtCreator(payload={})


def test_if_jwt_creator_has_secret_arg():
    assert JwtCreator(secret='')


def test_if_jwt_creator_has_algo_arg():
    assert JwtCreator(algo='HS256')


def test_raised_exception_if_algo_is_unsupported():
    with pytest.raises(UnsupportedAlgoException):
        JwtCreator(algo='HS2565')


def test_create_token_with_HS256_algo_with_default_args():
    assert JwtCreator().createToken()
