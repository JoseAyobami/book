from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import generate_ulid
from app.models.base import BookingStatus





#Booking: id, user_id, service_id, start_time, end_time, status (pending | confirmed | cancelled | completed), created_at


class Booking(Base):
    __tablename__ = "booking"

    id = Column(String(26), primary_key=True, default=generate_ulid)
    user_id = Column(String(26), ForeignKey("user.id"), nullable=False)
    service_id = Column(String(26), ForeignKey("service.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


    user = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False)

    
    

