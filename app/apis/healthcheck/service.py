from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/healthcheck")
def healthcheck():
    """
    Health check endpoint for monitoring application status.
    Does not expose any technology stack information for security reasons.
    """
    return {"ok": True}
