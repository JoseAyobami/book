from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum
from app.database import Base
from app.models.base import generate_ulid
from sqlalchemy.orm import relationship
from app.models.base import UserRole

#User: id, name, email, password_hash, 
#role (user | admin), created_at

    


class User(Base):
    __tablename__ = "user"

    id = Column(String(26), primary_key=True, index=True, default=generate_ulid)
    name = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    


    bookings = relationship("Booking", back_populates="user")