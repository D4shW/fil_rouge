from typing import List
from database import Database
from models import Agence
from .base_repository import BaseRepository


class AgenceRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    def get_all(self) -> List[Agence]:
        return self._get_all('agences', Agence)
