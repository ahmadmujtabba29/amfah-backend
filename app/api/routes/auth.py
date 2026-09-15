from fastapi import APIRouter

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    """
    Admin login.

    - Validates email format and non-empty password via Pydantic
    - Verifies credentials against the stored password hash
    - Returns a JWT access token on success
    """
    access_token = login_user(body.email, body.password)
    return TokenResponse(access_token=access_token)
