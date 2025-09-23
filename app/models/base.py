from enum import Enum
import ulid

def generate_ulid():
    return str(ulid.new())

class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"