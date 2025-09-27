from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import and_
from datetime import datetime, timezone
from app.logger import get_logger
from app.models.base import UserRole
from app.models.booking import Booking as BookingModel, BookingStatus
from app.schemas.booking import BookingCreate, BookingUpdate
from app.models.user import User as UserModel

logger = get_logger(__name__)

class BookingCrud:

    @staticmethod
    def create_booking(db: Session, user_id: str, booking_data: BookingCreate):
        # Check overlap
        conflict = db.query(BookingModel).filter(
            BookingModel.service_id == booking_data.service_id,
            BookingModel.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
            and_(
                BookingModel.start_time < booking_data.end_time,
                BookingModel.end_time > booking_data.start_time
            )
        ).first()
        if conflict:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking time conflicts with an existing booking.")

        new_booking = BookingModel(
            user_id=user_id,
            service_id=booking_data.service_id,
            start_time=booking_data.start_time,
            end_time=booking_data.end_time,
            status=BookingStatus.pending
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking

    @staticmethod
    def get_booking(db: Session, booking_id: str):
        return db.query(BookingModel).filter(BookingModel.id == booking_id).first()

    @staticmethod
    def list_bookings(db: Session, user_id: str, is_admin=False, status=None, from_dt=None, to_dt=None):
        query = db.query(BookingModel)
        if not is_admin:
            query = query.filter(BookingModel.user_id == user_id)
        else:
            if status:
                query = query.filter(BookingModel.status == status)
            if from_dt:
                query = query.filter(BookingModel.start_time >= from_dt)
            if to_dt:
                query = query.filter(BookingModel.end_time <= to_dt)
        return query.all()

    @staticmethod
    def update_booking(db: Session, booking: BookingModel, data: BookingUpdate, is_admin=False):
        if data.start_time:
            booking.start_time = data.start_time
        if data.end_time:
            booking.end_time = data.end_time
        if is_admin and data.status:
            booking.status = data.status
        db.commit()
        db.refresh(booking)
        return booking
    
    @staticmethod
    def delete_booking(db: Session, booking: BookingModel):
        db.delete(booking)
        db.commit()

        

booking_crud = BookingCrud()    
