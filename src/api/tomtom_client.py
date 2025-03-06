import requests
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from zoneinfo import ZoneInfo

from src.config import (
    TOMTOM_API_KEY,
    TOMTOM_API_BASE_URL,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS
)

class TomTomClient:
    def __init__(self):
        self.api_key = TOMTOM_API_KEY
        self.base_url = TOMTOM_API_BASE_URL
        self.logger = logging.getLogger(__name__)
        
        if not self.api_key:
            raise ValueError("TomTom API key not found in environment variables")

    def get_route_info(self, from_coords: str, to_coords: str) -> Optional[Dict[str, Any]]:
        """
        Get route information from TomTom API
        
        Args:
            from_coords (str): Starting coordinates (format: "latitude,longitude")
            to_coords (str): Destination coordinates (format: "latitude,longitude")
            
        Returns:
            dict: Processed route information or None if request fails
        """
        url = f"{self.base_url}/{from_coords}:{to_coords}/json"
        params = {
            "key": self.api_key,
            "routeRepresentation": "summaryOnly",
        }

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                return self._process_response(data)
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"API request failed (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY_SECONDS)
                continue
                
            except Exception as e:
                self.logger.error(f"Unexpected error processing route data: {str(e)}")
                return None
        
        return None

    def _process_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the API response and extract relevant information"""
        route_summary = data["routes"][0]["summary"]
        
        # Convert departure time to Dubai time
        departure_str = route_summary["departureTime"]
        utc_time = datetime.fromisoformat(departure_str.replace("Z", "+00:00"))
        dubai_time = utc_time.astimezone(ZoneInfo("Asia/Dubai"))
        
        return {
            "timestamp": int(dubai_time.timestamp()),  # Convert to Unix timestamp (integer)
            "date": dubai_time.strftime("%Y-%m-%d"),
            "day_of_week": dubai_time.strftime("%A"),
            "distance_km": route_summary["lengthInMeters"] / 1000.0,
            "travel_time_seconds": route_summary["travelTimeInSeconds"],
            "travel_time_minutes": round(route_summary["travelTimeInSeconds"] / 60)
        } 