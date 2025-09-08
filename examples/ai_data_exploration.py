"""
Example demonstrating how an AI assistant would dynamically explore weather data
This shows the real value of MCP - AI can discover, explore, and analyze data 
without pre-programmed queries.
"""
import asyncio
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

async def ai_exploration_workflow():
    """Simulate how an AI assistant would explore weather data dynamically"""
    
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "fast_mcp/server/server.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("🤖 AI Assistant: Starting data exploration...")
                print("="*60)
                
                # Step 1: AI discovers what data is available
                print("🔍 AI: Let me see what data we have...")
                schema_result = await session.call_tool("discover_database_schema", {})
                print("✅ Found database schema!")
                
                # Step 2: AI checks data quality
                print("\n📊 AI: Analyzing data quality...")
                quality_result = await session.call_tool("analyze_data_quality", {
                    "table_name": "weather_data.london_weather"
                })
                print("✅ Data quality analysis complete!")
                
                # Step 3: AI asks dynamic questions about the data
                print("\n🤔 AI: What's the temperature range in our dataset?")
                temp_analysis = await session.call_tool("execute_sql_query", {
                    "sql_query": """
                        SELECT 
                            MIN(CAST(current__temperature_2m AS FLOAT)) as min_temp,
                            MAX(CAST(current__temperature_2m AS FLOAT)) as max_temp,
                            AVG(CAST(current__temperature_2m AS FLOAT)) as avg_temp,
                            COUNT(*) as total_readings
                        FROM weather_data.london_weather 
                        WHERE current__temperature_2m IS NOT NULL
                    """
                })
                print("✅ Temperature analysis:", temp_analysis.content[0].text)
                
                # Step 4: AI explores patterns
                print("\n📈 AI: Are there any interesting hourly patterns?")
                hourly_pattern = await session.call_tool("execute_sql_query", {
                    "sql_query": """
                        SELECT 
                            EXTRACT(hour FROM current__time) as hour_of_day,
                            AVG(CAST(current__temperature_2m AS FLOAT)) as avg_temp,
                            COUNT(*) as readings_count
                        FROM weather_data.london_weather 
                        WHERE current__temperature_2m IS NOT NULL
                        GROUP BY EXTRACT(hour FROM current__time)
                        ORDER BY hour_of_day
                    """
                })
                print("✅ Hourly patterns discovered!")
                
                # Step 5: AI finds anomalies
                print("\n🚨 AI: Looking for temperature anomalies...")
                anomaly_query = await session.call_tool("execute_sql_query", {
                    "sql_query": """
                        WITH temp_stats AS (
                            SELECT 
                                AVG(CAST(current__temperature_2m AS FLOAT)) as mean_temp,
                                STDDEV(CAST(current__temperature_2m AS FLOAT)) as stddev_temp
                            FROM weather_data.london_weather 
                            WHERE current__temperature_2m IS NOT NULL
                        )
                        SELECT 
                            current__time,
                            current__temperature_2m,
                            ABS(CAST(current__temperature_2m AS FLOAT) - mean_temp) / stddev_temp as z_score
                        FROM weather_data.london_weather, temp_stats
                        WHERE current__temperature_2m IS NOT NULL
                        AND ABS(CAST(current__temperature_2m AS FLOAT) - mean_temp) / stddev_temp > 2
                        ORDER BY z_score DESC
                    """
                })
                print("✅ Anomaly detection complete!")
                
                # Step 6: AI correlates multiple variables
                print("\n🔗 AI: How does temperature correlate with humidity?")
                correlation = await session.call_tool("execute_sql_query", {
                    "sql_query": """
                        SELECT 
                            CASE 
                                WHEN CAST(current__temperature_2m AS FLOAT) < 15 THEN 'Cold'
                                WHEN CAST(current__temperature_2m AS FLOAT) < 25 THEN 'Moderate'
                                ELSE 'Hot'
                            END as temp_category,
                            AVG(CAST(current__relative_humidity_2m AS FLOAT)) as avg_humidity,
                            COUNT(*) as sample_size
                        FROM weather_data.london_weather 
                        WHERE current__temperature_2m IS NOT NULL 
                        AND current__relative_humidity_2m IS NOT NULL
                        GROUP BY temp_category
                        ORDER BY avg_humidity DESC
                    """
                })
                print("✅ Temperature-humidity correlation analyzed!")
                
                print("\n" + "="*60)
                print("🎯 AI Assistant: Data exploration complete!")
                print("💡 Key insight: The AI dynamically discovered data structure,")
                print("   identified patterns, found anomalies, and explored correlations")
                print("   without any pre-programmed knowledge of the dataset!")
                
    except Exception as e:
        print(f"❌ Exploration failed: {e}")

if __name__ == "__main__":
    asyncio.run(ai_exploration_workflow())