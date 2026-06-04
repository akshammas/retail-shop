# app/core/security.py

from passlib.context import CryptContext

# bcrypt is the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Convert plain password to hashed version"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain password matches the hash"""
    return pwd_context.verify(plain_password, hashed_password)