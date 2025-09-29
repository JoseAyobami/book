from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.routes.login import router as login_route
from app.routes.services import router as services_route
from app.routes.booking import router as booking_route
from app.routes.review import router as review_route
from app.database import engine, Base
from app import models  


app = FastAPI(
    title="BookIt API",
    description="API for managing users, services, bookings, and reviews.",
    version="1.0.0",
)


Base.metadata.create_all(bind=engine)


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


app.add_middleware(SlowAPIMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],        
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Try again later."},
    )


app.include_router(login_route)
app.include_router(services_route)
app.include_router(booking_route)
app.include_router(review_route)


@app.get("/")
@limiter.limit("10/minute")  
async def read_root(request: Request):
    return {"message": "Welcome to the BookIt API"}





