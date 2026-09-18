from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.repositories.users_repository import get_user_by_email


def login_user(email: str, password: str) -> str:
    """
    Authenticate a user and return a JWT access token.

    MVP: looks up the user in app/data/users.json.
    Later: replace the repository with a database-backed implementation.
    """
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = get_user_by_email(email)
    if user is None:
        raise invalid_credentials

    password_hash = user.get("password_hash")
    if not isinstance(password_hash, str):
        raise invalid_credentials

    if not verify_password(password, password_hash):
        raise invalid_credentials

    return create_access_token(subject=email.lower())
