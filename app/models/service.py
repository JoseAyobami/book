from datetime import datetime, timezone
from app.models.base import generate_ulid
from ..database import Base
from sqlalchemy import Column, DateTime, Interval, String, Boolean, Text, Numeric, Enum
from sqlalchemy.orm import relationship
from app.models.base import UserRole
    

# Service: id, title, description, price, duration_minutes, is_active, created_at                                



class Service(Base):
    __tablename__ = "service"

    id = Column(String(26), primary_key=True, index=True, default=generate_ulid)
    title= Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price =Column(Numeric(10, 2), nullable=False)
    duration_minutes = Column(Interval, nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.admin, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False,default=lambda: datetime.now(timezone.utc))


    bookings = relationship("Booking", back_populates="service", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="service", cascade="all, delete-orphan")




    





