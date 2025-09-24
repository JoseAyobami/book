from decimal import Decimal
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, ConfigDict
from app.models.base import generate_ulid

#Service: 
#id, title, description, price, 
#duration_minutes, is_active, 
#created_at

class ServiceBase(BaseModel):
    title: str
    description: str
    price: Decimal = Field(..., gt=0)
    duration_minutes: timedelta

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration_minutes: Optional[timedelta] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class ServiceResponse(ServiceBase):
    id: str = Field(default_factory=generate_ulid)
    is_active: bool
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)





















# from decimal import Decimal
# from typing import Optional
# from pydantic import BaseModel, Field
# from datetime import datetime

# from sqlalchemy import Numeric
# from app.models.base import generate_ulid





# class ServiceBase(BaseModel):
#     title: str
#     description: str
#     price: Numeric = Field(..., gt=0)
#     duration_minutes: int

# class ServiceCreate(ServiceBase):
#     pass


# class ServiceUpdate(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[Decimal] = None
#     duration_minutes: Optional[int] = None
#     is_active: Optional[bool] = None


# class ServiceResponse(ServiceBase):
#     id: str = Field(default_factory=generate_ulid)
#     is_active: bool
#     created_at: datetime

#     class Config:
#         from_attributes = True





