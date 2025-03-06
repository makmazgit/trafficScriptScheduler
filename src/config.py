import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
TOMTOM_API_KEY = os.getenv('TOMTOM_API_KEY')
TOMTOM_API_BASE_URL = "https://api.tomtom.com/routing/1/calculateRoute"

# Route Configuration
ROUTES = [
    {
        "name": "Dubai Route 1",
        "from_coords": "24.996083,55.375999",
        "to_coords": "25.250287,55.337958"
    }
    # Add more routes as needed
]

# Database Configuration
DATABASE_URL = "sqlite:///database/routes.db"

# Scheduler Configuration
SCHEDULE_INTERVAL_MINUTES = 15  # How often to collect data
MAX_RETRIES = 3  # Number of retries for failed API calls
RETRY_DELAY_SECONDS = 5  # Delay between retries

# Logging Configuration
LOG_FILE = "logs/traffic_monitor.log"
LOG_LEVEL = "INFO"

# API Rate Limiting
MAX_REQUESTS_PER_SECOND = 5  # TomTom free tier limit 