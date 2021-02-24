from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_pipe():
    return ' '

@router.get("/")
async def show_pipe():
    return ' '

@router.delete("/{pipe_id}") 
async def delete_pipe():
    return ' '

@router.get("/{pipe_id}")
async def info_pipe():
    return ' '

#get data - no need /data
# @router.get("/{pipe_id}/data")
# async def info_mapping():
#     return ' '

@router.put("/{pipe_id}/flush")
async def read_pipe():
    return ' '