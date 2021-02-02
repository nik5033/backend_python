import pytest

from helpers.auth.exceptions import ReadTokenException
from helpers.auth.token import create_token, read_token


@pytest.fixture()
def token_data() -> dict:
    return {'id': 10}


def test_read_valid_token(token_data):
    req_token = create_token(token_data)
    res_token = read_token(req_token)

    res_token.pop('exp')

    assert res_token == token_data


def test_read_invalid_token():
    invalid_token = 'wrong token'

    with pytest.raises(ReadTokenException):
        read_token(invalid_token)


def test_read_expired_token(token_data):

    req_token = create_token(token_data, lifetime=-10)

    with pytest.raises(ReadTokenException):
        read_token(req_token)