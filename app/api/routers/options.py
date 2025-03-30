from fastapi import Depends, APIRouter, HTTPException, status

router = APIRouter(
    prefix="/options",
    tags=["Options"],
    redirect_slashes=False,
)
