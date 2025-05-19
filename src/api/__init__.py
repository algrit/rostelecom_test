from fastapi import APIRouter
from .v1 import router as equip_router

router = APIRouter()
router.include_router(equip_router, prefix="/v1")
