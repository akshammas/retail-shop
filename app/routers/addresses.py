# app/routers/addresses.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.dependencies import get_current_user
from app.db.database import get_db
from app.db.crud.address import (
    get_addresses_by_user,
    get_address_by_id,
    get_default_address,
    create_address,
    update_address,
    delete_address,
    set_default_address
)
from typing import List

router = APIRouter()


# get all my addresses
@router.get("/", response_model=List[AddressResponse])
async def list_my_addresses(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_addresses_by_user(db, current_user.id)


# get default address
@router.get("/default", response_model=AddressResponse)
async def get_my_default_address(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    address = get_default_address(db, current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="No default address set")
    return address


# get single address
@router.get("/{address_id}", response_model=AddressResponse)
async def get_my_address(
    address_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    address = get_address_by_id(db, address_id)
    if not address or address.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


# add new address
@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def add_address(
    address: AddressCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    address_data = address.model_dump()
    return create_address(db, current_user.id, address_data)


# update address
@router.put("/{address_id}", response_model=AddressResponse)
async def update_my_address(
    address_id: int,
    updates: AddressUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_data = updates.model_dump(exclude_unset=True)
    updated = update_address(db, address_id, current_user.id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated


# set default address
@router.patch("/{address_id}/set-default", response_model=AddressResponse)
async def set_my_default_address(
    address_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    address = set_default_address(db, address_id, current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


# delete address
@router.delete("/{address_id}")
async def delete_my_address(
    address_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = delete_address(db, address_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted"}