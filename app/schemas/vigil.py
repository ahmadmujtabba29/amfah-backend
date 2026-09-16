from pydantic import BaseModel, Field


class HashResponse(BaseModel):
    """SHA-256 audit result for an uploaded payload."""

    filename: str
    content_type: str | None = None
    size_bytes: int = Field(ge=0)
    sha256: str = Field(
        min_length=64,
        max_length=64,
        description="64-character hexadecimal SHA-256 digest",
    )
