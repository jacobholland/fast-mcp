from typing import Any

import dlt
from dlt.sources.rest_api import rest_api_source


def load_weather_simple() -> None:
    """Simple weather data from a free API - no auth required"""
    pipeline = dlt.pipeline(
        pipeline_name="weather_api",
        destination="duckdb",
        dataset_name="weather_data",
    )

    # Super simple config - just hits one endpoint
    weather_source = rest_api_source(
        {
            "client": {
                "base_url": "https://api.open-meteo.com/v1/",
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
                            "forecast_days": 3,
                        },
                    },
                },
            ],
        }
    )

    load_info = pipeline.run(weather_source)
    print(f"✅ Weather data loaded: {load_info}")


if __name__ == "__main__":

    print("🚀 Loading weather data...")
    load_weather_simple()
