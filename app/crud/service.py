from datetime import timedelta
from sqlalchemy.orm import Session
from app.logger import get_logger
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
            duration_minutes=timedelta(minutes=service_data.duration_minutes),
            is_active=True
        )
        db.add(new_service)
        db.flush()
        db.refresh(new_service)
        return new_service
    

    @staticmethod
    def get_service(db: Session, service_id: str):
        return db.query(ServiceModel).filter(ServiceModel.id == service_id).first()

    @staticmethod
    def list_services(
        db: Session,
        q: str = "",
        price_min: float = 0,
        price_max: float = float("inf"),
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

    # @staticmethod
    # def get_service(db: Session, service_id: str):
    #     return db.query(ServiceModel).filter(ServiceModel.id == service_id).first()

    # @staticmethod
    # def list_services(db: Session, skip: int = 0, limit: int = 10):
    #     return db.query(ServiceModel).offset(skip).limit(limit).all()

    # @staticmethod
    # def update_service(db: Session, service_id: str, update_data: ServiceUpdate):
    #     service = db.query(ServiceModel).filter(ServiceModel.id == service_id).first()
    #     if not service:
    #         return None

    #     # Update fields if provided
    #     if update_data.title is not None:
    #         service.title = update_data.title
    #     if update_data.description is not None:
    #         service.description = update_data.description
    #     if update_data.price is not None:
    #         service.price = update_data.price
    #     if update_data.duration_minutes is not None:
    #         service.duration_minutes = update_data.duration_minutes
    #     if update_data.is_active is not None:
    #         service.is_active = update_data.is_active

    #     db.commit()
    #     db.refresh(service)
    #     return service

    # @staticmethod
    # def delete_service(db: Session, service: ServiceModel):
    #     db.delete(service)
    #     db.commit()