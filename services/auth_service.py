import hashlib
from typing import Optional
from models import User
from repositories import UserRepository


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return hashlib.sha256(plain.encode()).hexdigest() == hashed

    @staticmethod
    def login(email: str, password: str, user_repo: UserRepository) -> Optional[User]:
        user = user_repo.find_by_email(email.strip().lower())
        if user and AuthService.verify_password(password, user.password):
            return user
        return None
