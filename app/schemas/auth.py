from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Incoming login body — email format and non-empty password validated here."""

    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """Successful login response with a JWT access token."""

    access_token: str
    token_type: str = "bearer"
