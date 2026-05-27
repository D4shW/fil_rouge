from dataclasses import dataclass


@dataclass
class Contact:
    id: int
    name: str
    email: str
    phone: str
    subject: str
    message: str
    date: str
    status: str = 'nouveau'

    @classmethod
    def from_row(cls, row) -> 'Contact':
        return cls(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            phone=row['phone'],
            subject=row['subject'],
            message=row['message'],
            date=row['date'],
            status=row['status'],
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'date': self.date,
            'status': self.status,
        }
