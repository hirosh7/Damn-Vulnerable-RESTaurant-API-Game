import os
import platform

import psutil
from apis.auth.utils import get_current_user
from config import ENVIRONMENT, ENV
from db.models import User, UserRole
from fastapi import APIRouter, Depends, HTTPException, status
from typing_extensions import Annotated

router = APIRouter()


@router.get("/debug", status_code=status.HTTP_200_OK)
def get_debug_info_service(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Debug endpoint - ONLY enabled in development mode and ONLY for CHEF role.
    Exposes minimal system information for troubleshooting.
    """
    # Only allow CHEF role to access debug information
    if current_user.role != UserRole.CHEF:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Chef can access debug information"
        )
    
    # Only enable debug endpoint in development environment
    if ENVIRONMENT != ENV.DEVELOPMENT:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debug endpoint is disabled in production"
        )

    # Return ONLY non-sensitive system information
    # DO NOT expose environment variables, paths, or detailed system info
    os_info = {
        "system": platform.system(),
        "python_version": platform.python_version(),
    }

    disk_usage = psutil.disk_usage('/')
    disk_info = {
        "total_gb": round(disk_usage.total / (1024**3), 2),
        "used_gb": round(disk_usage.used / (1024**3), 2),
        "free_gb": round(disk_usage.free / (1024**3), 2),
        "percent": disk_usage.percent,
    }

    mem = psutil.virtual_memory()
    memory_info = {
        "total_gb": round(mem.total / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "percent": mem.percent,
    }

    debug_info = {
        "os_info": os_info,
        "disk_usage": disk_info,
        "memory_usage": memory_info,
        "warning": "This endpoint should be disabled in production"
    }

    return debug_info
