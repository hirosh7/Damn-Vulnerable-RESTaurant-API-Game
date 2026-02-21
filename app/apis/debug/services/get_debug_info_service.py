import os
import platform

import psutil
from apis.auth.utils import get_current_user
from db.models import User, UserRole
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing_extensions import Annotated

router = APIRouter()

# Environment variable keys that must never be returned to clients.
# Secrets, credentials, and keys are filtered from the debug payload so that
# even Chef-authenticated requests cannot inadvertently expose them.
_SENSITIVE_ENV_KEYS = {
    "jwt_secret_key",
    "postgres_password",
    "postgres_user",
    "secret",
    "password",
    "token",
    "key",
    "api_key",
    "auth",
    "credential",
}


def _is_sensitive(key: str) -> bool:
    k = key.lower()
    return any(s in k for s in _SENSITIVE_ENV_KEYS)


def _safe_env() -> dict:
    return {k: "***REDACTED***" if _is_sensitive(k) else v for k, v in os.environ.items()}


@router.get("/debug", status_code=status.HTTP_200_OK)
def get_debug_info_service(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.CHEF.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Chef is authorized to access debug information.",
        )

    os_info = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
    }

    disk_usage = psutil.disk_usage(os.getcwd())
    disk_info = {
        "total": disk_usage.total,
        "used": disk_usage.used,
        "free": disk_usage.free,
        "percent": disk_usage.percent,
    }

    mem = psutil.virtual_memory()
    memory_info = {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "free": mem.free,
        "percent": mem.percent,
    }

    return {
        "os_info": os_info,
        "env_vars": _safe_env(),
        "disk_usage": disk_info,
        "memory_usage": memory_info,
    }
