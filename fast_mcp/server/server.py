from fastmcp import FastMCP
from fast_mcp.server.database import DataManager
from fast_mcp.server.pipelines.weather_pipeline import load_weather_simple
import logging
import json
from datetime import datetime

# Initialize logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize data manager and MCP server
data_manager = DataManager()
mcp = FastMCP("DataEngineering-DuckDB-Server")


@mcp.tool
async def fetch_weather_data(city: str = "London") -> str:
    """Trigger DLT pipeline to fetch and store weather data"""
    try:
        # Trigger the DLT weather pipeline
        load_weather_simple(data_manager)
        
        return json.dumps(
            {
                "status": "success",
                "message": f"Weather data pipeline completed for {city}",
                "pipeline": "weather",
                "triggered_at": datetime.now().isoformat(),
            },
            indent=2,
        )

    except Exception as e:
        logger.error(f"Weather pipeline failed: {e}")
        return f"Error running weather pipeline: {str(e)}"

@mcp.tool
def query_weather_data(limit: int = 10) -> str:
    """Query the stored weather data - simple analytics"""
    try:
        query = """
            SELECT 
              latitude
            , longitude
            , current_units__time
            , current_units__temperature_2m

            FROM weather_data.london_weather
        """

        results = data_manager.execute_query(query)

        if not results:
            return json.dumps({"message": "No weather data found"})

        return json.dumps(
            {"result": "success"}
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return f"Error querying weather data: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting simplified DuckDB MCP Server...")
    logger.info(f"Database: {data_manager.db_path}")
    mcp.run()
