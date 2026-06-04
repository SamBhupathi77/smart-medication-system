# backend/security.py

def hash_password(password: str):
    return password


def verify_password(
    plain_password: str,
    stored_password: str
):
    return plain_password == stored_password