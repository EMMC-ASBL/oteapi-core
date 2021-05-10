from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_mapping():
    return ' '

@router.get("/")
async def show_mapping():
    return ' '

@router.get("/{resource_id}")
async def info_mapping():
    return ' '

@router.delete("/{resource_id}")
async def delete_mapping():
    return ' '

@router.get("/{resource_id}/read")
async def read_mapping():
    return ' '