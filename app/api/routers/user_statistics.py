from fastapi import Depends, APIRouter, HTTPException, status

router = APIRouter(
    prefix="/user-statistics",
    tags=["User Statistics"],
    redirect_slashes=False,
)
