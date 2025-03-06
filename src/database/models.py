from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.config import DATABASE_URL

Base = declarative_base()

class RouteInfo(Base):
    __tablename__ = 'route_info'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    date = Column(String, nullable=False)
    day_of_week = Column(String, nullable=False)
    from_coords = Column(String, nullable=False)
    to_coords = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
    travel_time_seconds = Column(Integer, nullable=False)
    travel_time_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create database engine
engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 