from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from src.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Retrieves the API key from the request header and validates it against the stored API key.

    Args:
        api_key (str): The API key extracted from the request header.

    Returns:
        str: The validated API key if it matches the stored key.

    Raises:
        HTTPException: If the provided API key does not match the stored key.
    """
    if api_key == settings.API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate API key")
