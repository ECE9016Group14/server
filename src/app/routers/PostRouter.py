from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from app.schema.post import PostSchema
from app.services.post_service import PostService
from src.app.schema.base import CommRes, ListArgsSchema, ListFilterSchema


post_router = APIRouter(prefix="/post", tags=["Post module"], responses={
    404: {"description": "Notfound"}
})

@post_router.post("/add", response_model=CommRes, status_code=status.HTTP_201_CREATED)
async def create(line: PostSchema, service: PostService = Depends()):
     result=service.create(line)
     return CommRes.success(result)


@post_router.get("/get-all", response_model=CommRes)
async def get_all(service: PostService = Depends()):
    return CommRes.success(service.get_list(None))

@post_router.get("/get/{id}", response_model=CommRes)
async def get_by_id(id: str, service: PostService = Depends()):
    line = service.get(id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return CommRes.success(line)

@post_router.put("/update", response_model=CommRes)
async def update(line: PostSchema, service: PostService = Depends()):
    return CommRes.success( service.update(line))

@post_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: PostService = Depends()):
    return CommRes.success(service.delete(id))
