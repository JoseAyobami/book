from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.base import generate_ulid
from app.models.booking import BookingStatus
from datetime import datetime
from pydantic import BaseModel
from app.models.booking import BookingStatus


# Booking: id, user_id, service_id, start_time, 
# end_time, status (pending | confirmed | cancelled | completed), 
# created_at



class BookingBase(BaseModel):
    service_id: str
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: BookingStatus | None = None # Admin only

    model_config = ConfigDict(from_attributes=True)

class BookingResponse(BookingBase):
    id: str = Field(default_factory=generate_ulid)
    user_id: str
    status: BookingStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    



