# AI Assistant Integration Guide

This guide shows you **exactly** how to connect AI assistants to interrogate your weather dataset dynamically.

## Method 1: Claude Desktop (Recommended)

### Step 1: Install Claude Desktop
Download from: https://claude.ai/download

### Step 2: Configure MCP Server
Add this to your Claude Desktop MCP configuration file:

**Location:** 
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Config:**
```json
{
  "mcpServers": {
    "weather-data": {
      "command": "uv",
      "args": ["run", "fast_mcp/server/server.py"],
      "cwd": "/Users/jacob.holland/github/fast-mcp"
    }
  }
}
```

### Step 3: Start Claude Desktop
Claude will automatically connect to your MCP server.

### Step 4: Test the Integration
Ask Claude questions like:

```
"What data do we have available? Can you explore the weather dataset?"

"Show me temperature patterns in the data"

"Find any anomalies or interesting trends in the weather data"

"Write a SQL query to analyze humidity patterns"
```

Claude will use your MCP tools to dynamically explore and analyze the data!

---

## Method 2: Run the Demo (See AI in Action)

### Quick Test
```bash
cd /Users/jacob.holland/github/fast-mcp
uv run examples/ai_interrogation_demo.py
```

This simulates exactly how Claude would interrogate your data:
1. Discovers available tables and columns
2. Asks analytical questions 
3. Writes custom SQL queries
4. Generates insights in natural language

---

## Method 3: Custom Integration (Any AI Assistant)

### Using OpenAI GPT with MCP
```python
import openai
from your_mcp_client import MCPClient

# Connect to your MCP server
mcp_client = MCPClient("fast_mcp/server/server.py")

# Let GPT use your MCP tools
def ask_gpt_with_data(question):
    # Get available tools from MCP
    tools = mcp_client.list_tools()
    
    # Ask GPT to use the tools
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}],
        tools=tools,  # Give GPT access to your MCP tools
        tool_choice="auto"
    )
    
    return response
```

### Using Anthropic Claude API
```python
import anthropic
from your_mcp_client import MCPClient

client = anthropic.Anthropic(api_key="your-key")
mcp_client = MCPClient("fast_mcp/server/server.py")

# Let Claude API use your MCP tools for data analysis
```

---

## Method 4: Jupyter Integration

Create a notebook that lets AI explore your data:

```python
# notebook.py
import asyncio
from mcp_client import MCPSession

async def ai_data_analysis():
    async with MCPSession("fast_mcp/server/server.py") as session:
        # AI discovers schema
        schema = await session.call_tool("discover_database_schema")
        
        # AI writes custom queries
        insights = await session.call_tool("execute_sql_query", {
            "sql_query": "SELECT * FROM weather_data.london_weather WHERE temperature > 25"
        })
        
        return insights
```

---

## What Makes This Powerful

### Traditional Approach:
```
You → Write specific SQL → Get fixed results
```

### MCP + AI Approach:
```
You → Ask natural language question → AI explores dynamically → AI writes SQL → AI interprets results → AI gives insights
```

### Example Conversation with AI:

**You:** "What patterns do you see in the weather data?"

**AI Response:**
1. *Uses `discover_database_schema()` to understand data structure*
2. *Uses `execute_sql_query()` to explore temperature trends*  
3. *Uses `analyze_data_quality()` to check data completeness*
4. *Writes custom SQL to find correlations*
5. *Provides natural language insights*

"I found that temperatures peak around 2 PM and drop overnight. There are 1,247 readings with 98% completeness. Humidity inversely correlates with temperature (R² = 0.73). I detected 3 anomalous readings that may be sensor errors."

---

## Next Steps

1. **Try Claude Desktop** - Easiest way to see AI data exploration
2. **Run the demo** - See exactly how AI interrogates data  
3. **Build custom integration** - Connect your preferred AI assistant
4. **Add more data sources** - Expand beyond weather data

The key insight: **AI assistants become data analysts** that can discover, explore, and synthesize insights from your data without pre-programming every possible question.