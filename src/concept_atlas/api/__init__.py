from fastapi import FastAPI
from .routes import router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app
app = FastAPI(title="Concept Atlas API", version="0.1.0")

# Add root endpoint
@app.get("/")
async def root():
    return {"message": "Concept Atlas API", "version": "0.1.0", "docs": "/docs"}

# Include router
app.include_router(router, prefix="/api/v1")
