from pydantic import BaseModel, Field
from datetime import datetime

from app.models.base import generate_ulid



#Review: id, booking_id, rating (1–5), comment, created_at

class ReviewBase(BaseModel):
    booking_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str


class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: str = Field(default_factory=generate_ulid)
    created_at: datetime

    class Config:
        from_attributes = True


