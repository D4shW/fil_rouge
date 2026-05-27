from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    phone: str = ''
    company: str = ''
    created: str = ''

    @classmethod
    def from_row(cls, row) -> 'User':
        return cls(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            password=row['password'],
            phone=row['phone'],
            company=row['company'],
            created=row['created'],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'created': self.created,
        }
