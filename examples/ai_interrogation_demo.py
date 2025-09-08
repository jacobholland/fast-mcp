"""
Simulate how Claude or another AI assistant would interrogate the weather dataset
This shows the actual conversation flow between AI and your MCP server
"""
import asyncio
import json
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

class AIAssistant:
    """Simulated AI assistant that can explore data dynamically"""
    
    def __init__(self, session):
        self.session = session
        self.context = {"discovered_tables": [], "data_insights": []}
    
    async def think_and_query(self, thought: str, tool_name: str, params: dict = None):
        """AI thinks about what to do, then executes a tool"""
        print(f"🤖 AI Thinking: {thought}")
        
        if params is None:
            params = {}
            
        try:
            result = await self.session.call_tool(tool_name, params)
            response = result.content[0].text if result.content else "No response"
            
            # Parse JSON response if possible
            try:
                parsed = json.loads(response)
                return parsed
            except:
                return response
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    async def explore_dataset(self):
        """AI explores the dataset step by step"""
        
        print("🎯 AI Assistant: I need to understand what data is available...")
        
        # Step 1: Discover schema
        schema_data = await self.think_and_query(
            "Let me see what tables and columns are available",
            "discover_database_schema"
        )
        
        if schema_data and "database_schema" in schema_data:
            tables = schema_data["database_schema"]["tables"]
            self.context["discovered_tables"] = tables
            
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   • {table['name']} ({len(table['columns'])} columns)")
        
        # Step 2: Get some sample data
        print("\n🔍 AI Assistant: Let me examine the main weather table...")
        
        sample_data = await self.think_and_query(
            "I'll get a few sample records to understand the data structure",
            "execute_sql_query",
            {"sql_query": "SELECT * FROM weather_data.london_weather LIMIT 3"}
        )
        
        if sample_data and "data" in sample_data:
            print(f"✅ Sample data shows {sample_data['record_count']} records")
            if sample_data["data"]:
                print("   Sample columns:", list(sample_data["data"][0].keys()))
        
        # Step 3: Ask analytical questions
        await self.ask_analytical_questions()
    
    async def ask_analytical_questions(self):
        """AI asks interesting questions about the data"""
        
        questions = [
            {
                "question": "What's the temperature distribution in this dataset?",
                "sql": """
                    SELECT 
                        MIN(CAST(current__temperature_2m AS FLOAT)) as min_temp,
                        MAX(CAST(current__temperature_2m AS FLOAT)) as max_temp,
                        AVG(CAST(current__temperature_2m AS FLOAT)) as avg_temp,
                        COUNT(*) as total_readings
                    FROM weather_data.london_weather 
                    WHERE current__temperature_2m IS NOT NULL
                """
            },
            {
                "question": "Are there any patterns by time of day?",
                "sql": """
                    SELECT 
                        EXTRACT(hour FROM current__time) as hour,
                        AVG(CAST(current__temperature_2m AS FLOAT)) as avg_temp,
                        COUNT(*) as readings
                    FROM weather_data.london_weather 
                    WHERE current__temperature_2m IS NOT NULL
                    GROUP BY EXTRACT(hour FROM current__time)
                    ORDER BY hour
                    LIMIT 10
                """
            },
            {
                "question": "What about humidity patterns?",
                "sql": """
                    SELECT 
                        AVG(CAST(current__relative_humidity_2m AS FLOAT)) as avg_humidity,
                        MIN(CAST(current__relative_humidity_2m AS FLOAT)) as min_humidity,
                        MAX(CAST(current__relative_humidity_2m AS FLOAT)) as max_humidity
                    FROM weather_data.london_weather 
                    WHERE current__relative_humidity_2m IS NOT NULL
                """
            },
            {
                "question": "How recent is this data?",
                "sql": """
                    SELECT 
                        MIN(current__time) as earliest,
                        MAX(current__time) as latest,
                        COUNT(*) as total_records
                    FROM weather_data.london_weather
                """
            }
        ]
        
        print("\n📊 AI Assistant: Now let me ask some analytical questions...")
        
        for i, q in enumerate(questions, 1):
            print(f"\n❓ Question {i}: {q['question']}")
            
            result = await self.think_and_query(
                f"I'll write a SQL query to answer: {q['question']}",
                "execute_sql_query",
                {"sql_query": q["sql"]}
            )
            
            if result and "data" in result and result["data"]:
                data = result["data"][0]
                print("📈 Results:")
                for key, value in data.items():
                    print(f"   {key}: {value}")
                
                self.context["data_insights"].append({
                    "question": q["question"],
                    "results": data
                })
    
    async def generate_insights(self):
        """AI summarizes what it learned"""
        
        print("\n" + "="*60)
        print("🧠 AI Assistant: Here's what I discovered about your weather data:")
        
        insights = self.context.get("data_insights", [])
        
        if insights:
            for insight in insights:
                print(f"\n💡 {insight['question']}")
                results = insight['results']
                
                # Generate natural language insights
                if 'avg_temp' in results:
                    temp = results['avg_temp']
                    print(f"   → Average temperature is {temp:.1f}°C")
                    
                    if temp < 10:
                        print("   → This is quite cold weather")
                    elif temp > 25:
                        print("   → This is warm weather") 
                    else:
                        print("   → This is moderate weather")
                
                if 'total_readings' in results:
                    count = results['total_readings']
                    print(f"   → Dataset has {count:,} weather readings")
                
                if 'earliest' in results and 'latest' in results:
                    print(f"   → Data spans from {results['earliest']} to {results['latest']}")
        
        print(f"\n🎯 Summary: I dynamically explored your weather dataset and")
        print(f"   discovered patterns without any pre-programmed knowledge!")

async def main():
    """Run the AI interrogation demo"""
    
    server_params = StdioServerParameters(
        command="uv", 
        args=["run", "fast_mcp/server/server.py"]
    )
    
    print("🚀 Starting AI Data Interrogation Demo")
    print("="*60)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Create AI assistant
                ai = AIAssistant(session)
                
                # First, make sure we have data
                print("📥 AI Assistant: Let me ensure we have weather data...")
                await ai.think_and_query(
                    "I should fetch some fresh weather data first",
                    "fetch_weather_data", 
                    {"city": "London"}
                )
                
                # Explore the dataset
                await ai.explore_dataset()
                
                # Generate insights
                await ai.generate_insights()
                
                print("\n✅ AI interrogation complete!")
                print("\n💭 This demonstrates how an AI assistant can:")
                print("   • Discover data structure without prior knowledge")
                print("   • Ask analytical questions and write SQL dynamically")
                print("   • Generate insights in natural language")
                print("   • Adapt queries based on what it finds")
                
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\nMake sure your MCP server is working:")
        print("uv run fast_mcp/server/server.py")

if __name__ == "__main__":
    asyncio.run(main())