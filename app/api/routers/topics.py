from fastapi import Depends, APIRouter, HTTPException, status

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
    redirect_slashes=False,
)
