from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from app.schema.comment import CommentSchema
from app.services.comment_service import CommentService
from src.app.schema.base import CommRes, ListArgsSchema, ListFilterSchema


comment_router = APIRouter(prefix="/comment", tags=["Comment module"], responses={
    404: {"description": "Notfound"}
})

@comment_router.post("/add", response_model=CommRes, status_code=status.HTTP_201_CREATED)
async def create(line: CommentSchema, service: CommentService = Depends()):
     result=service.create(line)
     return CommRes.success(result)


@comment_router.get("/get-all", response_model=CommRes)
async def get_all(service: CommentService = Depends()):
    return CommRes.success(service.get_list(None))

@comment_router.get("/get/{id}", response_model=CommRes)
async def get_by_id(id: str, service: CommentService = Depends()):
    line = service.get(id)
    if line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return CommRes.success(line)

@comment_router.put("/update", response_model=CommRes)
async def update(line: CommentSchema, service: CommentService = Depends()):
    return CommRes.success( service.update(line))

@comment_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: CommentService = Depends()):
    return CommRes.success(service.delete(id))
