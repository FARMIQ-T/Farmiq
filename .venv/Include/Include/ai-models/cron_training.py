#!/usr/bin/env python3
import os
import sys
import logging
import json
import traceback
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from train_credit_model import DynamicCreditScorer

# Get the absolute path of the script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Set up logging directory
LOG_DIR = PROJECT_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
LOG_FILE = LOG_DIR / 'model_training.log'

# Set up logging with rotation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=1024*1024,  # 1MB
            backupCount=5
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def send_notification(subject: str, message: str) -> None:
    """Send notification about training status (implement as needed)"""
    # TODO: Implement notification system (email, Slack, etc.)
    logger.info(f"Notification - {subject}: {message}")

def create_lock_file() -> bool:
    """Create a lock file to prevent concurrent runs"""
    lock_file = SCRIPT_DIR / '.training.lock'
    if lock_file.exists():
        # Check if the process is still running
        try:
            with open(lock_file, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)  # Check if process exists
            return False
        except (OSError, ValueError):
            # Process not running, remove stale lock
            lock_file.unlink()
    
    # Create new lock file
    with open(lock_file, 'w') as f:
        f.write(str(os.getpid()))
    return True

def remove_lock_file() -> None:
    """Remove the lock file"""
    lock_file = SCRIPT_DIR / '.training.lock'
    if lock_file.exists():
        lock_file.unlink()

def train_model():
    """Function to be called by cron"""
    if not create_lock_file():
        logger.warning("Another training process is running. Exiting.")
        return
    
    try:
        # Load environment variables
        env_file = PROJECT_ROOT / '.env'
        load_dotenv(env_file)
        
        # Validate environment
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing environment variables: {missing_vars}")
        
        logger.info("Starting model training")
        start_time = datetime.now()
        
        # Initialize scorer
        scorer = DynamicCreditScorer(
            supabase_url=os.getenv('SUPABASE_URL'),
            supabase_key=os.getenv('SUPABASE_KEY')
        )
        
        # Train model
        scorer.train_model(force_retrain=False)
        
        # Log completion
        duration = datetime.now() - start_time
        logger.info(f"Model training completed in {duration}")
        
        # Check and log metrics
        model_metadata = SCRIPT_DIR / 'models/model_metadata.json'
        if model_metadata.exists():
            with open(model_metadata, 'r') as f:
                metadata = json.load(f)
                metrics = metadata.get('metrics', {})
                logger.info(f"Model metrics: {metrics}")
                
                # Check model performance
                if metrics.get('accuracy', 0) < 0.7:  # Example threshold
                    send_notification(
                        "Model Performance Warning",
                        f"Model accuracy ({metrics['accuracy']:.2f}) below threshold"
                    )
        
        send_notification(
            "Model Training Success",
            f"Training completed in {duration}"
        )
        
    except Exception as e:
        error_msg = f"Error in model training: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        send_notification("Model Training Error", error_msg)
        sys.exit(1)
        
    finally:
        remove_lock_file()

if __name__ == "__main__":
    train_model()