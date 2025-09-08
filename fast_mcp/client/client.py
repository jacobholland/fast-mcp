import asyncio
from fastmcp import Client

async def main():
    """Example usage of the FastMCP client with weather tools."""
    client = Client("/Users/jacob.holland/github/fast-mcp/fast_mcp/server/server.py")
    
    async with client:
        # Fetch weather data for a city
        print("Fetching weather data for London...")
        result = await client.call_tool("fetch_weather_data", {"city": "London"})
        print("Weather fetch result:", result)
        
        # Query the stored weather data
        print("\nQuerying stored weather data...")
        result = await client.call_tool("query_weather_data", {"limit": 5})
        print("Query result:", result)

if __name__ == "__main__":
    asyncio.run(main())