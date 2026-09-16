from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from app.schemas.vigil import HashResponse
from app.services.vigil_service import (
    REPORT_FILENAME,
    get_forensic_report_path,
    hash_uploaded_file,
)

router = APIRouter(prefix="/vigil", tags=["Vigil AI"])


@router.post("/hash", response_model=HashResponse)
async def create_file_hash(
    file: UploadFile = File(..., description="Document, invoice, or media payload"),
) -> HashResponse:
    """
    Process an uploaded payload with local SHA-256 hashing.

    Returns the live 64-character hexadecimal signature for the Vigil AI console.
    """
    result = await hash_uploaded_file(file)
    return HashResponse(**result)


@router.get("/report")
def download_forensic_report() -> FileResponse:
    """
    Download the pre-formatted court-admissible forensic validation report.

    This is a static mock PDF stored on the server for MVP sales demonstrations.
    """
    report_path = get_forensic_report_path()
    return FileResponse(
        path=report_path,
        media_type="application/pdf",
        filename=REPORT_FILENAME,
    )
