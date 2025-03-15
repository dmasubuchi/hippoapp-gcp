"""
Authentication utilities for Google Cloud Platform services.
"""
import os
from google.cloud import storage, speech, translate_v2, firestore
from google.oauth2 import service_account
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_credentials(credentials_path=None):
    """
    Set up Google Cloud credentials from a service account key file.
    
    Args:
        credentials_path (str, optional): Path to the service account key file.
            If not provided, will use GOOGLE_APPLICATION_CREDENTIALS environment variable.
            
    Returns:
        dict: Information about the authenticated service account
    """
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        logger.info(f"Set GOOGLE_APPLICATION_CREDENTIALS to {credentials_path}")
    
    # Check if credentials are properly set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        logger.warning("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        logger.info("You can set it manually with: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json")
        return None
    
    try:
        # Test authentication by creating a simple storage client
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        
        # Get service account details
        project_id = credentials.project_id
        client_email = credentials.service_account_email
        
        logger.info(f"Successfully authenticated as {client_email} for project {project_id}")
        return {
            "project_id": project_id,
            "client_email": client_email,
            "credentials_path": credentials_path
        }
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        return None

def test_gcp_services():
    """
    Test connection to required GCP services.
    
    Returns:
        dict: Status of each service connection
    """
    services_status = {}
    
    # Test Storage
    try:
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets(max_results=1))
        services_status["storage"] = "Connected"
    except Exception as e:
        services_status["storage"] = f"Failed: {str(e)}"
    
    # Test Speech-to-Text
    try:
        speech_client = speech.SpeechClient()
        services_status["speech"] = "Connected"
    except Exception as e:
        services_status["speech"] = f"Failed: {str(e)}"
    
    # Test Translation
    try:
        translate_client = translate_v2.Client()
        services_status["translate"] = "Connected"
    except Exception as e:
        services_status["translate"] = f"Failed: {str(e)}"
    
    # Test Firestore
    try:
        firestore_client = firestore.Client()
        services_status["firestore"] = "Connected"
    except Exception as e:
        services_status["firestore"] = f"Failed: {str(e)}"
    
    return services_status

def get_auth_instructions():
    """
    Return instructions for setting up GCP authentication.
    
    Returns:
        str: Formatted instructions
    """
    instructions = """
# Google Cloud Authentication Setup

To use this application, you need to set up Google Cloud authentication:

1. Create a service account in the Google Cloud Console:
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
   - Create a new service account with the following roles:
      - Storage Admin
      - Speech-to-Text Admin
      - Cloud Translation API User
      - Firestore User

2. Create and download a JSON key file for the service account

3. Set the environment variable to point to your key file:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-key-file.json"
   ```

4. Run the authentication test script:
   ```
   python -m data-ingestion.scripts.auth
   ```
"""
    return instructions

if __name__ == "__main__":
    # Print authentication instructions
    print(get_auth_instructions())
    
    # Try to set up credentials
    auth_info = setup_credentials()
    
    if auth_info:
        # Test GCP services
        print("\nTesting GCP services:")
        services_status = test_gcp_services()
        
        for service, status in services_status.items():
            print(f"- {service}: {status}")
