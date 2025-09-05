from fastmcp import FastMCP
from DataManager import DataManager
import httpx 
import logging 
import json 
from datetime import datetime 

# Initialize logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize data manager and MCP server
data_manager = DataManager("./analytics.duckdb")
mcp = FastMCP("DataEngineering-DuckDB-Server")

@mcp.tool
async def fetch_weather_data(city: str = "London") -> str:
    """Fetch weather data from OpenWeatherMap API and store in DuckDB"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://wttr.in/{city}?format=j1"
            response = await client.get(url, timeout=10.0)
            
            if response.status_code != 200:
                return f"Failed to fetch weather data: {response.status_code}"
            
            weather_data = response.json()
            current = weather_data.get('current_condition', [{}])[0]
            
            processed_data = {
                'location': city,
                'temperature': float(current.get('temp_C', 0)),
                'humidity': float(current.get('humidity', 0)),
                'pressure': float(current.get('pressure', 0)),
                'description': current.get('weatherDesc', [{}])[0].get('value', 'Unknown'),
                'raw_api_response': weather_data
            }
            
            rows_inserted = data_manager.insert_weather_data(processed_data)
            
            return json.dumps({
                'status': 'success',
                'city': city,
                'data': processed_data,
                'rows_inserted': rows_inserted,
                'fetched_at': datetime.now().isoformat()
            }, indent=2)
            
    except Exception as e:
        logger.error(f"Weather fetch failed for {city}: {e}")
        return f"Error fetching weather data: {str(e)}"

@mcp.tool
def query_weather_data(limit: int = 10) -> str:
    """Query the stored weather data - simple analytics"""
    try:
        query = """
            SELECT 
                location,
                temperature,
                humidity,
                pressure,
                timestamp,
                ingested_at
            FROM raw_weather 
            ORDER BY ingested_at DESC 
            LIMIT ?
        """
        
        results = data_manager.execute_query(query, (limit,))
        
        if not results:
            return json.dumps({"message": "No weather data found"})
        
        return json.dumps({
            "row_count": len(results),
            "data": results
        }, indent=2, default=str)
        
    except Exception as e:
        logger.error(f"Query failed: {e}")
        return f"Error querying weather data: {str(e)}"

@mcp.tool 
def get_table_info() -> str:
    """Get basic info about what's in our database"""
    try:
        # Get row count
        count_query = "SELECT COUNT(*) as total_records FROM raw_weather"
        count_result = data_manager.execute_query(count_query)
        total_records = count_result[0]['total_records'] if count_result else 0
        
        # Get distinct cities
        cities_query = "SELECT DISTINCT location FROM raw_weather ORDER BY location"
        cities_result = data_manager.execute_query(cities_query)
        cities = [row['location'] for row in cities_result]
        
        return json.dumps({
            "database_path": data_manager.db_path,
            "total_weather_records": total_records,
            "cities_with_data": cities,
            "available_tables": ["raw_weather", "metrics_agg", "events"]
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Table info query failed: {e}")
        return f"Error getting table info: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting simplified DuckDB MCP Server...")
    logger.info(f"Database: {data_manager.db_path}")
    mcp.run()