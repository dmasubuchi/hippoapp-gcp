"""
Utility functions specific to App Engine deployment.
"""
import os
import logging
from google.cloud import storage
from google.auth import default

logger = logging.getLogger(__name__)

def init_app_engine_services():
    """
    Initialize GCP services for App Engine environment.
    Uses App Engine's default service account credentials.
    """
    try:
        # Get project ID from environment variable
        project_id = os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            logger.warning("GCP_PROJECT_ID not set in environment variables")
            return None
            
        # Use default credentials provided by App Engine
        credentials, project = default()
        storage_client = storage.Client(
            project=project_id,
            credentials=credentials
        )
        
        logger.info(f"Successfully initialized App Engine services for project: {project_id}")
        return storage_client
    except Exception as e:
        logger.error(f"Error initializing App Engine services: {str(e)}")
        return None
