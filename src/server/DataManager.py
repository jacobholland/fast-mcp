import duckdb
import json
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataManager:
    """Centralized data management with DuckDB"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._setup_tables()
    
    def _setup_tables(self):
        """Initialize our analytical tables"""
        try:
            # Raw API data storage
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS raw_weather (
                    id INTEGER PRIMARY KEY,
                    location VARCHAR,
                    temperature DOUBLE,
                    humidity DOUBLE,
                    pressure DOUBLE,
                    timestamp TIMESTAMP,
                    raw_response JSON,
                    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Aggregated metrics table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics_agg (
                    metric_name VARCHAR,
                    metric_value DOUBLE,
                    dimensions JSON,
                    recorded_at TIMESTAMP,
                    PRIMARY KEY (metric_name, recorded_at)
                )
            """)
            
            # Generic events table for any structured data
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id UUID DEFAULT gen_random_uuid(),
                    event_type VARCHAR,
                    event_data JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("Database tables initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup tables: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute query and return results as dict list"""
        try:
            result = self.conn.execute(query, params).fetchall()
            columns = [desc[0] for desc in self.conn.description]
            return [dict(zip(columns, row)) for row in result]
        except Exception as e:
            logger.error(f"Query failed: {query}, Error: {e}")
            raise
    
    def insert_weather_data(self, data: Dict[str, Any]) -> int:
        """Insert weather data and return row count"""
        try:
            query = """
                INSERT INTO raw_weather (location, temperature, humidity, pressure, timestamp, raw_response)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.conn.execute(query, (
                data.get('location', 'Unknown'),
                data.get('temperature'),
                data.get('humidity'), 
                data.get('pressure'),
                datetime.now(),
                json.dumps(data)
            ))
            
            # Get the number of affected rows
            changes = self.conn.execute("SELECT changes()").fetchone()[0]
            logger.info(f"Inserted weather data for {data.get('location')}")
            return changes
            
        except Exception as e:
            logger.error(f"Failed to insert weather data: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.close()