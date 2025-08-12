from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
import logging
import os
from pathlib import Path
import shutil
import uuid
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db.models import Document

# Configure logging
logger = logging.getLogger(__name__)

# Create data directory structure
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Create router
router = APIRouter()

@router.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Concept Atlas API", "version": "0.1.0", "docs": "/docs"}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(description="File to upload"),
    db: Session = Depends(get_db)
):
    """
    Upload a file to the concept atlas system and store metadata in database.
    
    Args:
        file: File to upload
        db: Database session
        
    Returns:
        JSON response with upload status and file info
    """
    try:
        # Debug logging
        logger.info(f"Database session type: {type(db)}")
        logger.info(f"Database session info: {db}")
        
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
        
        # Create database record
        logger.info("Creating database record...")
        document = Document(
            name=original_filename,
            uri=str(file_path)
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        logger.info(f"Document record created in database with ID: {document.id}")
        
        file_info = {
            "filename": file.filename,
            "original_filename": original_filename,
            "saved_filename": random_filename,
            "content_type": file.content_type,
            "size": file_size,
            "local_path": str(file_path),
            "database_id": str(document.id),
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
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Rollback database transaction on error
        if 'db' in locals():
            db.rollback()
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to upload file", "details": str(e)}
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "concept-atlas"}

@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    """List all documents in the database"""
    try:
        documents = db.query(Document).all()
        return {
            "documents": [
                {
                    "id": str(doc.id),
                    "name": doc.name,
                    "uri": doc.uri,
                    "created_at": doc.created_at.isoformat() if doc.created_at else None
                }
                for doc in documents
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to fetch documents", "details": str(e)}
        )
