from typing import List, Optional, Type, TypeVar
from database import Database

T = TypeVar('T')


class BaseRepository:
    def __init__(self, db: Database):
        self._db = db

    def _get_all(self, table: str, model_cls: Type[T]) -> List[T]:
        with self._db.get_connection() as conn:
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
        return [model_cls.from_row(r) for r in rows]

    def _get_by_id(self, table: str, model_cls: Type[T], entity_id: int) -> Optional[T]:
        with self._db.get_connection() as conn:
            row = conn.execute(
                f"SELECT * FROM {table} WHERE id = ?", (entity_id,)
            ).fetchone()
        return model_cls.from_row(row) if row else None

    def _delete(self, table: str, entity_id: int) -> None:
        with self._db.get_connection() as conn:
            conn.execute(f"DELETE FROM {table} WHERE id = ?", (entity_id,))
