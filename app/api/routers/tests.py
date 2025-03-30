from fastapi import Depends, APIRouter, HTTPException, status

router = APIRouter(
    prefix="/tests",
    tags=["Tests"],
    redirect_slashes=False,
)
