import sqlite3
from datetime import datetime
import pandas as pd
from zoneinfo import ZoneInfo

def verify_data():
    # Connect to the database
    conn = sqlite3.connect('database/routes.db')
    
    # Read all data into a pandas DataFrame
    query = "SELECT * FROM route_info ORDER BY timestamp DESC LIMIT 5"
    df = pd.read_sql_query(query, conn)
    
    if len(df) == 0:
        print("No data found in the database!")
        return
    
    print("\nLast 5 route measurements:")
    print("-" * 80)
    
    for _, row in df.iterrows():
        # Parse the timestamp (already in Dubai time)
        timestamp = pd.to_datetime(row['timestamp'])
        
        print(f"Time (Dubai): {timestamp}")
        print(f"Route: {row['from_coords']} → {row['to_coords']}")
        print(f"Travel Time: {row['travel_time_minutes']} minutes")
        print(f"Distance: {row['distance_km']:.2f} km")
        print("-" * 80)
    
    # Print some statistics
    print("\nSummary Statistics:")
    print(f"Total records: {len(pd.read_sql_query('SELECT * FROM route_info', conn))}")
    print(f"Date range: {pd.to_datetime(df['timestamp'].min())} to {pd.to_datetime(df['timestamp'].max())}")
    print(f"Average travel time: {df['travel_time_minutes'].mean():.1f} minutes")
    
    conn.close()

if __name__ == "__main__":
    verify_data() 