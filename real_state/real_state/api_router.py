from estates.endpoints import router as estate_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(estate_router, prefix="/estate", tags=["Blog"])
