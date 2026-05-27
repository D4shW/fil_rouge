from dataclasses import dataclass


@dataclass
class Service:
    id: int
    name: str
    category: str
    price: float
    unit: str
    description: str
    icon: str
    popular: bool

    @classmethod
    def from_row(cls, row) -> 'Service':
        return cls(
            id=row['id'],
            name=row['name'],
            category=row['category'],
            price=row['price'],
            unit=row['unit'],
            description=row['description'],
            icon=row['icon'],
            popular=bool(row['popular']),
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'unit': self.unit,
            'description': self.description,
            'icon': self.icon,
            'popular': self.popular,
        }
