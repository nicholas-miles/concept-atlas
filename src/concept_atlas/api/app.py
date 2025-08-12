from fastapi import FastAPI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app
app = FastAPI(title="Concept Atlas API", version="0.1.0")

# Import and include routers
from .routes import router
app.include_router(router)
