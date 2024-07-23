from fastapi import FastAPI
from routes import inbound_routes, outbound_routes, appointment_routes, crm_routes

app = FastAPI()

app.include_router(inbound_routes.router, prefix="/inbound", tags=["inbound"])
app.include_router(outbound_routes.router, prefix="/outbound", tags=["outbound"])
app.include_router(appointment_routes.router, prefix="/appointments", tags=["appointments"])
app.include_router(crm_routes.router, prefix="/crm", tags=["crm"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Changed port to 8000 to avoid potential conflicts with common services on port 6969