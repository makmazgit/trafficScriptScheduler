import sqlite3
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
from pathlib import Path

def analyze_data():
    # Connect to the database
    conn = sqlite3.connect('database/routes.db')
    
    # Read all data into a DataFrame
    df = pd.read_sql_query('SELECT * FROM route_info ORDER BY timestamp ASC', conn)
    
    if len(df) == 0:
        print("No data found in the database!")
        return
    
    print("\nRaw Data Sample:")
    print("-" * 80)
    print(df.head())
        
    # Convert timestamps to datetime with flexible parsing
    df['datetime'] = pd.to_datetime(df['timestamp'], format='mixed')
    df['datetime'] = df['datetime'].dt.tz_localize('Asia/Dubai')
    
    print("\nData Collection Summary:")
    print("-" * 80)
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"Expected records (every 5 mins): {int((df['datetime'].max() - df['datetime'].min()).total_seconds() / 300)}")
    print(f"Average travel time: {df['travel_time_minutes'].mean():.1f} minutes")
    print(f"Min travel time: {df['travel_time_minutes'].min()} minutes")
    print(f"Max travel time: {df['travel_time_minutes'].max()} minutes")
    
    # Check for gaps
    time_diffs = df['datetime'].diff()
    gaps = time_diffs[time_diffs > pd.Timedelta(minutes=6)]  # Gaps longer than 6 minutes
    
    if not gaps.empty:
        print("\nFound gaps in data collection:")
        for idx in gaps.index:
            gap_start = df['datetime'][idx-1]
            gap_end = df['datetime'][idx]
            gap_duration = time_diffs[idx]
            print(f"Gap of {gap_duration}: {gap_start} to {gap_end}")
    
    # Create plots directory if it doesn't exist
    Path('plots').mkdir(exist_ok=True)
    
    # Plot travel times
    plt.figure(figsize=(15, 6))
    plt.plot(df['datetime'], df['travel_time_minutes'])
    plt.title('Travel Time Over Time')
    plt.xlabel('Time')
    plt.ylabel('Travel Time (minutes)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/travel_times.png')
    plt.close()
    
    # Daily statistics
    daily_stats = df.groupby(df['datetime'].dt.date).agg({
        'travel_time_minutes': ['count', 'mean', 'min', 'max']
    }).round(1)
    
    print("\nDaily Statistics:")
    print("-" * 80)
    print(daily_stats)
    
    # Print raw data for debugging
    print("\nFirst few records (raw data):")
    print("-" * 80)
    print(df[['timestamp', 'datetime', 'travel_time_minutes']].head())
    
    conn.close()

if __name__ == "__main__":
    analyze_data() 