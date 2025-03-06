import os
import logging
from src.scheduler.scheduler import run_scheduler
from src.config import LOG_FILE

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),
        logging.StreamHandler()
    ]
)

# Add a startup marker to easily identify new runs
logging.info("=" * 80)
logging.info("Starting new data collection run")

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logging.info("Application stopped by user")
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        raise 