import os
import secrets
from fastapi import Header, HTTPException, status

API_KEY = os.getenv("TIMELINE_API_KEY", "")


def require_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfigured: TIMELINE_API_KEY not set",
        )
    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
