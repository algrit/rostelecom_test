from fastapi import APIRouter
from .cpe import router as cpe_router


router = APIRouter()
router.include_router(cpe_router, prefix="/equipment")
