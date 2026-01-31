import secrets
import string

from apis.auth.utils import update_user_password
from config import settings
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

router = APIRouter()


# this is a highly sensitive endpoint used only for admin purposes
# it's excluded from the docs to make it more secure
@router.get(
    "/admin/reset-chef-password",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
def get_reset_chef_password(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Highly sensitive endpoint for resetting Chef password.
    Only accessible from localhost and requires additional security.
    
    In production, this should:
    - Require authentication with a special admin token
    - Be completely disabled or moved to a CLI tool
    - Log all access attempts
    """
    client_host = request.client.host

    # Check both client IP and X-Forwarded-For to prevent proxy bypass
    forwarded_for = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP", "")
    
    # Only allow from localhost (127.0.0.1 or ::1)
    allowed_hosts = ["127.0.0.1", "::1", "localhost"]
    
    if (client_host not in allowed_hosts and 
        forwarded_for not in allowed_hosts and 
        real_ip not in allowed_hosts):
        # Log the unauthorized attempt
        # log_security_event("CHEF_PASSWORD_RESET", "UNKNOWN", f"Unauthorized attempt from {client_host}", False)
        raise HTTPException(
            status_code=403,
            detail="This endpoint is only accessible from localhost!",
        )

    # In production, add additional authentication requirement here
    # For example, require a special admin token or API key
    
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_-+=;:[]"

    # Generate a cryptographically secure random password
    new_password = "".join(secrets.choice(characters) for i in range(32))
    update_user_password(db, settings.CHEF_USERNAME, new_password)
    
    # Log the password reset
    # log_security_event("CHEF_PASSWORD_RESET", settings.CHEF_USERNAME, "Password reset from localhost", True)

    return {"password": new_password}
