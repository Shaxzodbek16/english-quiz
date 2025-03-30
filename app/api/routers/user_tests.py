from fastapi import Depends, APIRouter, HTTPException, status

router = APIRouter(
    prefix="/user-tests",
    tags=["user-tests"],
    redirect_slashes=False,
)
