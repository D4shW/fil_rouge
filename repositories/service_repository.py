from typing import List, Optional
from database import Database
from models import Service
from .base_repository import BaseRepository


class ServiceRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_all(self) -> List[Service]:
        return self._get_all('services', Service)

    def get_by_id(self, service_id: int) -> Optional[Service]:
        return self._get_by_id('services', Service, service_id)

    def get_popular(self) -> List[Service]:
        with self._db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM services WHERE popular = 1"
            ).fetchall()
        return [Service.from_row(r) for r in rows]

    def get_by_category(self, category: str) -> List[Service]:
        with self._db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM services WHERE category = ?", (category,)
            ).fetchall()
        return [Service.from_row(r) for r in rows]

    def get_categories(self) -> List[str]:
        with self._db.get_connection() as conn:
            rows = conn.execute(
                "SELECT DISTINCT category FROM services ORDER BY category"
            ).fetchall()
        return [r['category'] for r in rows]

    def create(self, name: str, category: str, price: float, unit: str,
               description: str, icon: str, popular: bool) -> Service:
        with self._db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO services (name,category,price,unit,description,icon,popular) VALUES (?,?,?,?,?,?,?)",
                (name, category, price, unit, description, icon, int(popular)),
            )
            row = conn.execute(
                "SELECT * FROM services WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return Service.from_row(row)

    def update(self, service_id: int, **fields) -> Optional[Service]:
        allowed = {'name', 'category', 'price', 'unit', 'description', 'icon', 'popular'}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return self.get_by_id(service_id)
        set_clause = ', '.join(f"{k} = ?" for k in updates)
        with self._db.get_connection() as conn:
            conn.execute(
                f"UPDATE services SET {set_clause} WHERE id = ?",
                (*updates.values(), service_id),
            )
        return self.get_by_id(service_id)

    def delete(self, service_id: int) -> None:
        self._delete('services', service_id)
