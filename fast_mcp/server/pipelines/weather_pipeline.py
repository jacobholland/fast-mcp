import dlt
from dlt.sources.rest_api import rest_api_source
from fast_mcp.server.database import DataManager

def load_weather_simple(data_manager: DataManager = None) -> str:
    """DLT pipeline for weather data ingestion - creates its own schema"""
    
    if data_manager is None:
        data_manager = DataManager()
    
    try:
        # DLT pipeline - focused only on ingestion
        pipeline = dlt.pipeline(
            pipeline_name="weather_api",
            destination=dlt.destinations.duckdb(data_manager.db_path),
            dataset_name="weather_data"
        )
        
        # Weather API configuration
        weather_source = rest_api_source({
            "client": {
                "base_url": "https://api.open-meteo.com/v1/",
                "paginator": {
                    "type": "json_link",
                    "next_url_path": "paging.next",
                },
            },
            "resources": [
                {
                    "name": "london_weather",
                    "endpoint": {
                        "path": "forecast",
                        "params": {
                            "latitude": 51.5074,
                            "longitude": -0.1278,
                            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                            "hourly": "temperature_2m,relative_humidity_2m",
                            "forecast_days": 1,
                        },
                        "data_selector": "$"
                    },
                },
            ],
        })

        # Run pipeline - DLT decides the schema
        load_info = pipeline.run(weather_source)
        
        return f"Weather data loaded successfully. Tables created: {load_info.loads_ids}"
        
    except Exception as e:
        return f"Pipeline failed: {str(e)}"


if __name__ == "__main__":
    result = load_weather_simple()