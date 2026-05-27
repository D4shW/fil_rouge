from typing import List, Optional
from database import Database
from models import Contact
from .base_repository import BaseRepository

VALID_STATUSES = ('nouveau', 'en cours', 'traité', 'fermé')


class ContactRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_all(self) -> List[Contact]:
        with self._db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM contacts ORDER BY date DESC").fetchall()
        return [Contact.from_row(r) for r in rows]

    def create(self, name: str, email: str, phone: str,
               subject: str, message: str) -> Contact:
        with self._db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO contacts (name, email, phone, subject, message) VALUES (?,?,?,?,?)",
                (name, email, phone, subject, message),
            )
            row = conn.execute(
                "SELECT * FROM contacts WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return Contact.from_row(row)

    def update_status(self, contact_id: int, status: str) -> Optional[Contact]:
        if status not in VALID_STATUSES:
            return None
        with self._db.get_connection() as conn:
            conn.execute(
                "UPDATE contacts SET status = ? WHERE id = ?", (status, contact_id)
            )
            row = conn.execute(
                "SELECT * FROM contacts WHERE id = ?", (contact_id,)
            ).fetchone()
        return Contact.from_row(row) if row else None
