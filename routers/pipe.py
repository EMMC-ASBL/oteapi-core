from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_pipe():
    return ' '


# return data
@router.get("/{pipe_id}")
async def data_pipe():
    return ' '

# Add a mapper or datasource
@router.post("/{pipe_id}/add")
async def addInput_pipe():
    # map mapper or datasource id
    return ' '

#get data - no need /data
# @router.get("/{pipe_id}/data")
# async def info_mapping():
#     return ' '

@router.get("/")
async def show_pipe():
    return ' '

@router.put("/{pipe_id}/flush")
async def read_pipe():
    return ' '

@router.delete("/{pipe_id}") 
async def delete_pipe():
    return ' '
