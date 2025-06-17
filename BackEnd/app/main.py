from fastapi import FastAPI
from app.routers import (
    administrator_router,
    auth_router,
    technician_router,
    user_router,
    sensor_routes,
    ticket_router
)

app = FastAPI(title="Sensor Monitoring API")

app.include_router(administrator_router.router, prefix="/administrators", tags=["Administrators"])
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(technician_router.router, prefix="/technicians", tags=["Technicians"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(sensor_routes.router)
app.include_router(ticket_router.router, prefix="/tickets", tags=["Tickets"])
