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
data_manager = DataManager()  # Will use default data directory
mcp = FastMCP("DataEngineering-DuckDB-Server")


@mcp.tool
async def fetch_weather_data(city: str = "London") -> str:
    """Trigger DLT pipeline to fetch and store weather data"""
    try:
        # Trigger the DLT weather pipeline
        load_weather_simple()
        
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

        return json.dumps(
            {"row_count": len(results), "data": results}, indent=2, default=str
        )

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
        total_records = count_result[0]["total_records"] if count_result else 0

        # Get distinct cities
        cities_query = "SELECT DISTINCT location FROM raw_weather ORDER BY location"
        cities_result = data_manager.execute_query(cities_query)
        cities = [row["location"] for row in cities_result]

        return json.dumps(
            {
                "database_path": data_manager.db_path,
                "total_weather_records": total_records,
                "cities_with_data": cities,
                "available_tables": ["raw_weather", "metrics_agg", "events"],
            },
            indent=2,
        )

    except Exception as e:
        logger.error(f"Table info query failed: {e}")
        return f"Error getting table info: {str(e)}"

@mcp.tool
def trigger_dlt_pipeline(pipeline_name: str = "weather") -> str:
    """Trigger a DLT pipeline run"""
    if pipeline_name == "weather":
        load_weather_simple()
        return "Weather pipeline completed"


if __name__ == "__main__":
    logger.info("Starting simplified DuckDB MCP Server...")
    logger.info(f"Database: {data_manager.db_path}")
    mcp.run()
