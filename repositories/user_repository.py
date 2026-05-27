from typing import Optional
from database import Database
from models import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._get_by_id('users', User, user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        with self._db.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()
        return User.from_row(row) if row else None

    def create(self, name: str, email: str, password: str,
               phone: str = '', company: str = '') -> User:
        with self._db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, email, password, phone, company) VALUES (?,?,?,?,?)",
                (name, email, password, phone, company),
            )
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return User.from_row(row)
