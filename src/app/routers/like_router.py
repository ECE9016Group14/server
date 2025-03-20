import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Query

from app.schema.comment import LikeSchema
from app.services.like_service import LikeService
from src.app.schema.base import CommRes, ListArgsSchema, ListFilterSchema


like_router = APIRouter(prefix="/like", tags=["Like module"], responses={
    404: {"description": "Notfound"}
})

@like_router.post("/add", response_model=CommRes, status_code=status.HTTP_201_CREATED)
async def create(line: LikeSchema, service: LikeService = Depends()):
     line.id=None
     result=service.create(line)
     return CommRes.success(result)


@like_router.get("/get-all", response_model=CommRes)
async def get_all(service: LikeService = Depends()):
    return CommRes.success(service.get_list(None))

@like_router.get("/get_by_post_and_user", response_model=CommRes)
async def get(post_id: str = Query(None), user_id: str = Query(None), service: LikeService = Depends()):
    filters=[]
    if post_id:
        filters.append(ListFilterSchema(
            key="post_id",
            condition="=",
            value=post_id
        ))
    if user_id:
        filters.append(ListFilterSchema(
            key="user_id",
            condition="=",
            value=user_id
        ))
    result=[]
    if len(filters) > 0:

        result = service.get_list(ListArgsSchema(
            filters=filters
        ))
    if result is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return CommRes.success(result)

@like_router.put("/update", response_model=CommRes)
async def update(line: LikeSchema, service: LikeService = Depends()):
    return CommRes.success( service.update(line))

@like_router.delete("/delete_by_id/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(id: str, service: LikeService = Depends()):
    return CommRes.success(service.delete(id))

@like_router.delete("/delete/{user_id}/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: str, post_id: str, service: LikeService = Depends()):
    return CommRes.success(service.delete_like(user_id, post_id))
