import hashlib
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

REPORT_FILENAME = "forensic_validation_report.pdf"
REPORT_PATH = Path(__file__).resolve().parents[1] / "data" / REPORT_FILENAME

# 25 MB soft for MVP demo uploads
MAX_UPLOAD_BYTES = 25 * 1024 * 1024


async def hash_uploaded_file(file: UploadFile) -> dict[str, str | int | None]:
    """
    Read an uploaded file stream and compute a SHA-256 hex digest.

    Returns metadata used by the Vigil AI dashboard console.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A file payload is required",
        )

    digest = hashlib.sha256()
    total_bytes = 0

    while True:
        chunk = await file.read(1024 * 1024)
        if not chunk:
            break

        total_bytes += len(chunk)
        if total_bytes > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds the 25MB upload limit",
            )

        digest.update(chunk)

    if total_bytes == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": total_bytes,
        "sha256": digest.hexdigest(),
    }


def get_forensic_report_path() -> Path:
    """Return the path to the pre-configured mock forensic PDF."""
    if not REPORT_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forensic validation report is not available",
        )

    return REPORT_PATH
