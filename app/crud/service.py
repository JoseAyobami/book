from decimal import Decimal
from sqlalchemy.orm import Session
from app.logger import get_logger
from app.models.base import UserRole
from app.schemas.service import ServiceCreate, ServiceUpdate
from app.models.service import Service as ServiceModel



logger = get_logger(__name__)

class ServiceCrud:
    @staticmethod
    def create_service(db: Session, service_data: ServiceCreate):
        new_service = ServiceModel(
            title=service_data.title,
            description=service_data.description,
            price=service_data.price,
            duration_minutes=service_data.duration_minutes,
            role = UserRole.admin.value,
            is_active=True
        )
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
        return new_service
    

    @staticmethod
    def get_service(db: Session, service_id: str):
        return db.query(ServiceModel).filter(ServiceModel.id == service_id).first()

    @staticmethod
    def list_services(
        db: Session,
        q: str = "",
        price_min: Decimal = Decimal("0.00"),
        price_max: Decimal = Decimal("9999999999.99"),
        active: bool | None = None,
        skip: int = 0,
        limit: int = 100
    ):
        query = db.query(ServiceModel)
        if q:
            query = query.filter(ServiceModel.title.ilike(f"%{q}%"))
        query = query.filter(ServiceModel.price >= price_min, ServiceModel.price <= price_max)
        if active is not None:
            query = query.filter(ServiceModel.is_active == active)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_service(db: Session, service: ServiceModel, update_data: ServiceUpdate):
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(service, field, value)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def delete_service(db: Session, service: ServiceModel):
        db.delete(service)
        db.commit()
        return {"detail": "Service deleted"}
    


service_crud = ServiceCrud()

    