import asyncio
from fastmcp import Client

async def main():
    """Example usage of the FastMCP client with weather tools."""
    client = Client("http://localhost:8000")
    
    async with client:
        # Fetch weather data for a city
        print("Fetching weather data for London...")
        result = await client.call_tool("fetch_weather_data", {"city": "London"})
        print("Weather fetch result:", result)
        
        # Query the stored weather data
        print("\nQuerying stored weather data...")
        result = await client.call_tool("query_weather_data", {"limit": 5})
        print("Query result:", result)
        
        # Get table info
        print("\nGetting table info...")
        result = await client.call_tool("get_table_info", {})
        print("Table info:", result)

if __name__ == "__main__":
    asyncio.run(main())