from apis.router import api_router
from config import settings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rate_limiting import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Remove server identification header
        response.headers.pop("Server", None)
        
        return response


def init_app():
    app = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        servers=settings.SERVERS,
        root_path=settings.ROOT_PATH,
        docs_url=None,
        redoc_url=None,
    )
    
    # Add security headers middleware FIRST
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Configure CORS with stricter settings
    app.add_middleware(
        CORSMiddleware,
        # Use explicit domain list instead of regex for better security
        allow_origins=[
            "https://restaurant.com",
            "https://www.restaurant.com",
            "https://api.restaurant.com",
            "https://deliveryservice.com",
            "https://www.deliveryservice.com",
        ],
        allow_credentials=True,
        # Restrict methods to only what's needed
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        # Restrict headers
        allow_headers=["Authorization", "Content-Type"],
        # Set max age for preflight requests
        max_age=600,
    )
    
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.include_router(api_router)

    return app
