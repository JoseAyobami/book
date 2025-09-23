from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.deps import get_current_user, get_current_admin
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.crud.service import ServiceCrud

router = APIRouter(prefix="/service", tags=["Service"])


# --- Public endpoint ---
@router.get("/", response_model=list[ServiceResponse])
def get_services(
    q: Optional[str] = Query(None),
    price_min: float = 0,
    price_max: float = float("inf"),
    active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return ServiceCrud.list_services(db, q, price_min, price_max, active, skip, limit)

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: str, db: Session = Depends(get_db)):
    service = ServiceCrud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


# --- Admin endpoints ---
@router.post("/", response_model=ServiceResponse)
def create_service(service_data: ServiceCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return ServiceCrud.create_service(db, service_data)

@router.patch("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: str, update_data: ServiceUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    service = ServiceCrud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return ServiceCrud.update_service(db, service, update_data)

@router.delete("/{service_id}")
def delete_service(service_id: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    service = ServiceCrud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return ServiceCrud.delete_service(db, service)