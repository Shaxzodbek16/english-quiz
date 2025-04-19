from fastapi import Depends, APIRouter, HTTPException, status

router = APIRouter(
    prefix="/users",
    tags=["users"],
    redirect_slashes=False,
)
