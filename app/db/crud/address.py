# app/db/crud/address.py

from sqlalchemy.orm import Session
from app.models import Address


def get_addresses_by_user(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()


def get_address_by_id(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()


def get_default_address(db: Session, user_id: int):
    return db.query(Address).filter(
        Address.user_id == user_id,
        Address.is_default == True
    ).first()


def create_address(db: Session, user_id: int, address_data: dict):
    # if this is set as default, unset all others first
    if address_data.get("is_default"):
        db.query(Address).filter(
            Address.user_id == user_id
        ).update({"is_default": False})
        db.commit()

    address = Address(user_id=user_id, **address_data)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(db: Session, address_id: int, user_id: int, updates: dict):
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()
    if not address:
        return None

    # if setting as default, unset others
    if updates.get("is_default"):
        db.query(Address).filter(
            Address.user_id == user_id,
            Address.id != address_id
        ).update({"is_default": False})

    for key, value in updates.items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, address_id: int, user_id: int):
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()
    if not address:
        return None
    db.delete(address)
    db.commit()
    return address


def set_default_address(db: Session, address_id: int, user_id: int):
    # unset all defaults
    db.query(Address).filter(
        Address.user_id == user_id
    ).update({"is_default": False})

    # set new default
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()
    if not address:
        return None

    address.is_default = True
    db.commit()
    db.refresh(address)
    return address