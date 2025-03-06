import logging
import time
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.api.tomtom_client import TomTomClient
from src.database.models import SessionLocal
from src.database.operations import save_route_info
from src.config import ROUTES, SCHEDULE_INTERVAL_MINUTES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global flag to control countdown
running = True

def collect_route_data():
    """Collect route data for all configured routes"""
    client = TomTomClient()
    db = SessionLocal()
    success_count = 0
    total_routes = len(ROUTES)
    
    try:
        logger.info(f"Starting data collection for {total_routes} routes")
        
        for route in ROUTES:
            logger.info(f"Collecting data for route: {route['name']}")
            
            route_info = client.get_route_info(
                from_coords=route["from_coords"],
                to_coords=route["to_coords"]
            )
            
            if route_info:
                try:
                    save_route_info(
                        db=db,
                        route_data=route_info,
                        from_coords=route["from_coords"],
                        to_coords=route["to_coords"]
                    )
                    db.commit()
                    success_count += 1
                    logger.info(f"Successfully saved route data for {route['name']}")
                except Exception as e:
                    logger.error(f"Failed to save route data for {route['name']}: {str(e)}")
                    db.rollback()
            else:
                logger.error(f"Failed to collect data for route {route['name']}")
        
        logger.info(f"Data collection completed. Success: {success_count}/{total_routes} routes")
    
    except Exception as e:
        logger.error(f"Error collecting route data: {str(e)}")
    finally:
        db.commit()
        db.close()

def get_next_run_time():
    """Calculate the next run time (next multiple of 5 minutes)"""
    now = datetime.now()
    current_minute = now.minute
    next_multiple = ((current_minute // 5) + 1) * 5
    if next_multiple == 60:
        next_time = (now + timedelta(hours=1)).replace(minute=0)
    else:
        next_time = now.replace(minute=next_multiple, second=0, microsecond=0)
    return next_time

def show_countdown():
    """Show countdown to next execution"""
    global running
    while running:
        try:
            now = datetime.now()
            next_run = get_next_run_time()
            time_left = next_run - now
            minutes_left = time_left.seconds // 60
            seconds_left = time_left.seconds % 60
            print(f"\rNext run at {next_run.strftime('%H:%M:%S')} (in {minutes_left:02d}:{seconds_left:02d})", end='', flush=True)
            time.sleep(1)
        except KeyboardInterrupt:
            running = False
            break

def run_scheduler():
    """Run the scheduler with configured interval"""
    global running
    scheduler = BlockingScheduler()
    
    # Add job to run every 5 minutes at :00, :05, :10, etc.
    scheduler.add_job(
        collect_route_data,
        trigger=CronTrigger(minute='*/5'),  # Run at minutes 0,5,10,15,20,25,30,35,40,45,50,55
        next_run_time=None
    )
    
    logger.info("Starting scheduler, collecting data every 5 minutes (aligned to :00, :05, :10, etc.)")
    
    # Start countdown in a separate thread
    countdown_thread = threading.Thread(target=show_countdown)
    countdown_thread.daemon = True  # Thread will exit when main thread exits
    countdown_thread.start()
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        running = False
        raise 