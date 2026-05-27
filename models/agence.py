from dataclasses import dataclass


@dataclass
class Agence:
    id: int
    name: str
    address: str
    phone: str
    is_siege: bool

    @classmethod
    def from_row(cls, row) -> 'Agence':
        return cls(
            id=row['id'],
            name=row['name'],
            address=row['address'],
            phone=row['phone'],
            is_siege=bool(row['is_siege']),
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'is_siege': self.is_siege,
        }
