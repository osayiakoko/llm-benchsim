from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """
    Handles HTTP GET requests to the root endpoint ("/").

    Returns a JSON response with a success message.
    """
    return {"message": "Ok"}
