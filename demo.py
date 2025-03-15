#!/usr/bin/env python3
"""
Demo script for testing Google Cloud authentication and running the web application.
"""
import os
import sys
import argparse
import logging
import subprocess
from pathlib import Path
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_auth():
    """Test Google Cloud authentication."""
    logger.info("Testing Google Cloud authentication...")
    
    # Import auth module
    sys.path.append(str(Path(__file__).parent / "data-ingestion" / "scripts"))
    import auth
    
    # Test authentication
    auth_info = auth.setup_credentials()
    if auth_info:
        logger.info(f"Authentication successful: {auth_info}")
        
        # Test GCP services
        services_status = auth.test_gcp_services()
        for service, status in services_status.items():
            logger.info(f"Service {service}: {status}")
        
        # ADCを使用して認証
        client = storage.Client()
        
        # バケットにアクセス
        bucket = client.bucket('language-learning-audio')
        
        return True
    else:
        logger.error("Authentication failed")
        print(auth.get_auth_instructions())
        return False

def run_web_app():
    """Run the web application."""
    logger.info("Starting web application...")
    
    # Change to agentspace-app directory
    os.chdir(Path(__file__).parent / "agentspace-app")
    
    # Run the application
    try:
        subprocess.run(["python", "-m", "app.main"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running web application: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("Web application stopped")
    
    return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Demo script for Hippo Family Club GCP application")
    parser.add_argument("--auth", action="store_true", help="Test Google Cloud authentication")
    parser.add_argument("--web", action="store_true", help="Run web application")
    
    args = parser.parse_args()
    
    if args.auth:
        test_auth()
    elif args.web:
        run_web_app()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
