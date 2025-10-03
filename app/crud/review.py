from sqlalchemy.orm import Session
from app.models.review import Review as ReviewModel
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.logger import get_logger
from app.models.booking import Booking as BookingModel, BookingStatus
from datetime import datetime, timezone

logger = get_logger(__name__)

class ReviewCrud:

    @staticmethod
    def create_review(db: Session, user_id: str, review_data: ReviewCreate):
        # Check if booking exists and belongs to the user
        booking = db.query(BookingModel).filter(
            BookingModel.id == review_data.booking_id,
            BookingModel.user_id == user_id
        ).first()

        if not booking:
            return None, "Booking not found or does not belong to the user"

        # Ensure booking is completed
        #if booking.status != BookingStatus.completed:
            #return None, "Cannot review a booking that is not completed"

        # Ensure one review per booking
        existing = db.query(ReviewModel).filter(
            ReviewModel.booking_id == review_data.booking_id,
            ReviewModel.user_id == user_id
        ).first()
        if existing:
            return None, "Review already exists for this booking"

        review = ReviewModel(
            user_id=user_id,
            booking_id=review_data.booking_id,
            service_id=review_data.service_id,
            rating=review_data.rating,
            comment=review_data.comment,
            created_at=datetime.now(timezone.utc)
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return review, None

    @staticmethod
    def get_reviews_by_service(db: Session, service_id: str):
        return db.query(ReviewModel).filter(ReviewModel.service_id == service_id).all()

    @staticmethod
    def update_review(db: Session, review_id: str, review_data: ReviewUpdate):
        review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
        if not review:
            return None
        if review_data.rating is not None:
            review.rating = review_data.rating
        if review_data.comment is not None:
            review.comment = review_data.comment
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def delete_review(db: Session, review_id: str):
        review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
        if not review:
            return None
        db.delete(review)
        db.commit()
        return review


review_crud = ReviewCrud()

