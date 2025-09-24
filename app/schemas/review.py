from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.base import generate_ulid
from app.models.booking import BookingStatus


# Review: id, booking_id, user_id, service_id, rating (1-5), comment, created_at
class ReviewBase(BaseModel):
    booking_id: str
    service_id: str
    rating: int = Field(..., ge=1, le=5)  # rating between 1 and 5
    comment: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewResponse(ReviewBase):
    id: str = Field(default_factory=generate_ulid)
    user_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
