from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read():
    return 'hello from test'
