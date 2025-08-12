from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import logging
import os
from pathlib import Path
import shutil
import uuid
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create data directory structure
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Concept Atlas API", version="0.1.0")

@app.post("/upload")
async def upload_file(file: UploadFile = File(description="File to upload")):
    """
    Upload a file to the concept atlas system.
    
    Args:
        file: File to upload
        
    Returns:
        JSON response with upload status and file info
    """
    try:
        # Log the upload
        logger.info(f"Processing file: {file.filename}, size: {file.size} bytes")
        
        # Create safe filename with random UUID and preserve extension
        original_filename = Path(file.filename).name
        file_extension = Path(file.filename).suffix
        random_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = DATA_DIR / random_filename
        
        # Save file to local storage
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved to: {file_path}")
        
        # Get file size after saving
        file_size = os.path.getsize(file_path)
        
        file_info = {
            "filename": file.filename,
            "original_filename": original_filename,
            "saved_filename": random_filename,
            "content_type": file.content_type,
            "size": file_size,
            "local_path": str(file_path),
            "status": "uploaded"
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully",
                "file_info": file_info
            }
        )
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to upload file", "details": str(e)}
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "concept-atlas"}
