import pytest

from repositories import UserRepository


def test_if_user_repository_exists():
    assert UserRepository()


def test_user_repository_has_model_attr():
    assert UserRepository().model


def test_user_repository_has_method_auth_with_args():
    assert UserRepository().auth('admin', 'P@ssW0rd')
