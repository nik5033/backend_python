import bcrypt

from helpers.password.exceptions import GenPassHashException, CheckPassHashException


def generate_hash(password: str) -> str:
    try:
        return bcrypt.hashpw(
            password=password.encode(),
            salt=bcrypt.gensalt(),
        ).decode()
    except (TypeError, ValueError):
        raise GenPassHashException


def check_pass(cand_pass: str, real_pass: str) -> bool:
    try:
        return bcrypt.checkpw(
            password=cand_pass.encode(),
            hashed_password=real_pass.encode(),
        )
    except (TypeError, ValueError):
        raise CheckPassHashException
