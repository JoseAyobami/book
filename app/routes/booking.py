from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import date, datetime, timezone
from app.models.base import BookingStatus
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.crud.booking import BookingCrud
from app.database import get_db
from app.models.user import User as UserModel, UserRole
from app.deps import get_current_user  
from app.limiter import limiter

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
@limiter.limit("10/minute")
def list_bookings(
    request: Request,
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
    # Step 1: Get booking
    booking = BookingCrud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Step 2: Check ownership or admin
    if booking.user_id != current_user.id and current_user.role != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="Not authorized to view this booking")

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

    
    if current_user.role == UserRole.admin.value:
        updated_booking = BookingCrud.update_booking(db, booking, data, is_admin=True)
        return updated_booking

    
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this booking")

    
    if booking.status not in [BookingStatus.pending, BookingStatus.confirmed]:
        raise HTTPException(status_code=400, detail="Cannot update booking in this status")

    updated_booking = BookingCrud.update_booking(db, booking, data)
    return updated_booking


@router.delete("/{booking_id}")
def delete_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    booking = BookingCrud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    
    if current_user.role == UserRole.admin.value:
        BookingCrud.delete_booking(db, booking)
        return {"detail": "Booking deleted by admin"}

    
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this booking")

    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    if now_utc >= booking.start_time:
        raise HTTPException(status_code=400, detail="Cannot delete booking after start time")

    
    BookingCrud.delete_booking(db, booking)
    return {"detail": "Booking deleted successfully"}


