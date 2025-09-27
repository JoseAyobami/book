from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.review import Review as ReviewModel
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.crud.review import ReviewCrud
from app.models.user import User as UserModel
from app.deps import get_db, get_current_user
from app.logger import get_logger

logger = get_logger(__name__) 

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("", response_model=ReviewResponse)
def create_review( 
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    review = ReviewCrud.create_review(db, current_user.id, review_data)
    if not review:
        raise HTTPException(status_code=400, detail="Review already exists for this booking")
    return review

@router.get("/services/{service_id}", response_model=list[ReviewResponse])
def get_service_reviews(service_id: str, db: Session = Depends(get_db)):
    return ReviewCrud.get_reviews_by_service(db, service_id)

@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: str,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    review = ReviewCrud.update_review(db, review_id, review_data)
    if not review or review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return review

@router.delete("/{review_id}")
def delete_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted"}

        