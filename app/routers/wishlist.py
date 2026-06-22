# app/routers/wishlist.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.wishlist import WishlistAdd, WishlistItemResponse
from app.dependencies import get_current_user
from app.db.database import get_db
import app.services.wishlist_service as wishlist_service

router = APIRouter()


@router.get("/", response_model=List[WishlistItemResponse])
async def view_wishlist(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return wishlist_service.get_my_wishlist(db, current_user.id)


@router.get("/ids", response_model=List[int])
async def view_wishlist_ids(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return wishlist_service.get_my_wishlist_ids(db, current_user.id)


@router.post("/", response_model=WishlistItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist_route(
    body: WishlistAdd,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return wishlist_service.add(db, current_user.id, body.product_id)


@router.delete("/{product_id}")
async def remove_from_wishlist_route(
    product_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    wishlist_service.remove(db, current_user.id, product_id)
    return {"message": "Removed from wishlist"}