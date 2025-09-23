from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from .base import generate_ulid

#Review: id, booking_id, rating (1–5), comment, created_at


class Review(Base):
    __tablename__ = "review"

    id = Column(String(26), primary_key=True, default=generate_ulid)
    booking_id =Column (String, ForeignKey("booking.id"), nullable=False, unique=True)
    rating = Column(Integer, nullable=True)
    comment=  Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    booking = relationship("Booking", back_populates="review")

        


    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_check'),
    ) 
