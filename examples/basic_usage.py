import asyncio
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

async def main():
    """Example usage connecting to FastMCP server via stdio."""
    
    # Define how to start your server
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "fast_mcp/server/server.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the MCP connection
                await session.initialize()
                
                print("🔗 Connected to MCP server!")
                
                # List available tools first
                tools_result = await session.list_tools()
                print(f"\n📋 Available tools:")
                for tool in tools_result.tools:
                    print(f"  • {tool.name}: {tool.description}")
                
                # Fetch weather data for a city
                print("\n🌤️  Fetching weather data for London...")
                try:
                    result = await session.call_tool("fetch_weather_data", {"city": "London"})
                    print("Weather fetch result:", result.content[0].text if result.content else "No content")
                except Exception as e:
                    print(f"Error calling fetch_weather_data: {e}")
                
                # Query the stored weather data
                print("\n📊 Querying stored weather data...")
                try:
                    result = await session.call_tool("query_weather_data", {"limit": 5})
                    print("Query result:", result.content[0].text if result.content else "No content")
                except Exception as e:
                    print(f"Error calling query_weather_data: {e}")
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Make sure your server is working by running:")
        print("   uv run fast_mcp/server/server.py")

if __name__ == "__main__":
    asyncio.run(main())