"""
Main application entry point for the Hippo Family Club language learning app.
"""
import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import APP_CONFIG, GCS_CONFIG, PLAYBACK_CONFIG, AGENTSPACE_CONFIG
from app.utils import setup_gcp_services, get_audio_file, process_audio_playback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=APP_CONFIG["name"],
    description=APP_CONFIG["description"],
    version=APP_CONFIG["version"]
)

# Set up templates and static files
templates_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"

templates = Jinja2Templates(directory=str(templates_dir))
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Create cache directory if it doesn't exist
os.makedirs(PLAYBACK_CONFIG["cache_directory"], exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    try:
        # Set up GCP services
        setup_gcp_services()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

@app.get("/")
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/audio/{file_id}")
async def get_audio(file_id: str):
    """
    Get audio file metadata.
    
    Args:
        file_id: ID of the audio file
        
    Returns:
        JSON response with audio metadata
    """
    try:
        audio_info = get_audio_file(file_id)
        return JSONResponse(content=audio_info)
    except Exception as e:
        logger.error(f"Error getting audio file {file_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Audio file not found: {str(e)}")

@app.get("/api/audio/{file_id}/play")
async def play_audio(
    file_id: str, 
    start_time: float = 0, 
    end_time: Optional[float] = None, 
    speed: float = 1.0,
    repeat: bool = False
):
    """
    Stream audio file for playback.
    
    Args:
        file_id: ID of the audio file
        start_time: Start time in seconds
        end_time: End time in seconds
        speed: Playback speed
        repeat: Whether to repeat the audio
        
    Returns:
        Streaming response with audio data
    """
    try:
        return process_audio_playback(file_id, int(start_time), int(end_time) if end_time is not None else None, speed, repeat)
    except Exception as e:
        logger.error(f"Error playing audio file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error playing audio: {str(e)}")

@app.post("/api/agent/query")
async def agent_query(request: Request):
    """
    Send a query to the Agentspace learning agent.
    
    Args:
        request: Request object containing query parameters
        
    Returns:
        JSON response with agent response
    """
    try:
        data = await request.json()
        # TODO: Implement Agentspace API integration
        return JSONResponse(content={"message": "Agent integration not yet implemented"})
    except Exception as e:
        logger.error(f"Error querying agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying agent: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host=APP_CONFIG["host"], 
        port=APP_CONFIG["port"],
        reload=True
    )
