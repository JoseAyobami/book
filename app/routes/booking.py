from time import timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.models.base import BookingStatus
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.crud.booking import BookingCrud
from app.database import get_db
from app.models.user import User as UserModel, UserRole
from app.deps import get_current_user  

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    new_booking = BookingCrud.create_booking(db, current_user.id, booking)
    if not new_booking:
        raise HTTPException(status_code=400, detail="Booking conflict")
    return new_booking

@router.get("/", response_model=list[BookingResponse])
def list_bookings(
    status: str = None,
    from_dt: date = None,
    to_dt: date = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    is_admin = current_user.role == UserRole.admin.value
    return BookingCrud.list_bookings(db, current_user.id, is_admin, status, from_dt, to_dt)

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    booking = BookingCrud.get_booking(db, booking_id)
    if not booking or (booking.user_id != current_user.id and current_user.role != UserRole.admin.value):
        raise HTTPException(status_code=403, detail="Not authorized")
    return booking

@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: str,
    data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    booking = BookingCrud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Owner can update only pending/confirmed
    if current_user.role != UserRole.admin.value:
        if booking.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        if booking.status not in [BookingStatus.pending, BookingStatus.confirmed]:
            raise HTTPException(status_code=400, detail="Cannot update booking in this status")

    return BookingCrud.update_booking(db, booking, data, is_admin=(current_user.role == UserRole.admin.value))

@router.delete("/{booking_id}")
def delete_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    booking = BookingCrud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Owner can delete only before start_time
    if current_user.role != UserRole.admin.value:
        if booking.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        if datetime.now(timezone.utc) >= booking.start_time:
            raise HTTPException(status_code=400, detail="Cannot delete booking after start time")

    BookingCrud.delete_booking(db, booking)
    return {"detail": "Booking deleted"}
