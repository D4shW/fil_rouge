from dataclasses import dataclass, field
from typing import List


@dataclass
class InterventionItem:
    service_id: int
    qty: int
    service_name: str = ''
    service_icon: str = ''
    service_price: float = 0.0
    service_unit: str = ''

    @property
    def subtotal(self) -> float:
        return self.service_price * self.qty


@dataclass
class Intervention:
    id: int
    user_id: int
    date: str
    status: str
    notes: str
    items: List[InterventionItem] = field(default_factory=list)

    @classmethod
    def from_row(cls, row) -> 'Intervention':
        return cls(
            id=row['id'],
            user_id=row['user_id'],
            date=row['date'],
            status=row['status'],
            notes=row['notes'],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'status': self.status,
            'notes': self.notes,
            'items': [
                {'service_id': it.service_id, 'qty': it.qty}
                for it in self.items
            ],
        }
