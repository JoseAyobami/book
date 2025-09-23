from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.login import router as login_route
from .database import engine, Base
from app import models
from app.models import user, booking, service, review
from app.routes.services import router as services_route

app = FastAPI(
    title="BookIt API",
    description="API for managing users, services, bookings, and reviews.",
    version="1.0.0",
)


Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(login_route)
app.include_router(services_route)


@app.get("/")
def read_root():
    return {"message": "Welcome to the BookIt API"}





