from datetime import datetime
from pydantic import BaseModel, Field
from app.models.base import generate_ulid
from app.models.booking import BookingStatus
from datetime import datetime
from pydantic import BaseModel
from app.models.booking import BookingStatus


# Booking: id, user_id, service_id, start_time, 
# end_time, status (pending | confirmed | cancelled | completed), 
# created_at



class BookingBase(BaseModel):
    user_id: str
    service_id: str
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingRecord(BookingBase):
    id: str = Field(default_factory=generate_ulid)
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True



