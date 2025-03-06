from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.database.models import RouteInfo

def save_route_info(db: Session, route_data: Dict[str, Any], from_coords: str, to_coords: str) -> RouteInfo:
    """Save route information to database"""
    db_route = RouteInfo(
        timestamp=datetime.fromtimestamp(route_data["timestamp"]),
        date=route_data["date"],
        day_of_week=route_data["day_of_week"],
        from_coords=from_coords,
        to_coords=to_coords,
        distance_km=route_data["distance_km"],
        travel_time_seconds=route_data["travel_time_seconds"],
        travel_time_minutes=route_data["travel_time_minutes"]
    )
    
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route 