from fastapi import APIRouter
from . import filesystem

router = APIRouter(prefix='/api')
router.include_router(filesystem.router)
