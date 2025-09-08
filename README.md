# FastMCP Data Engineering Platform

A production-ready MCP server demonstrating real-world data engineering workflows. This project showcases:

- **MCP Protocol Implementation**: Standards-compliant server using FastMCP framework
- **Data Pipeline Orchestration**: DLT-powered API ingestion with weather data collection
- **Analytical Database**: DuckDB backend with optimized connection management  
- **Concurrent Data Access**: Read/write locking strategy for multi-client scenarios
- **Client Integration**: Both FastMCP and pure MCP client examples

## Project Structure

```
fast-mcp/
├── fast_mcp/                    # Main package
│   ├── server/                  # MCP server components
│   │   ├── server.py           # MCP server with weather analysis tools
│   │   ├── database.py         # DuckDB connection manager (read/write locks)
│   │   ├── data/               # Persistent data storage
│   │   └── pipelines/          # DLT data ingestion pipelines
│   │       └── weather_pipeline.py  # Weather API → DuckDB pipeline
│   └── client/                 # Client implementations
│       └── client.py           # FastMCP HTTP client
├── examples/                   # Usage demonstrations
│   └── basic_usage.py          # Full MCP stdio client
└── pyproject.toml             # Dependencies & tooling config
```

## Getting Started

### 1. Install Dependencies
```bash
uv sync
```

### 2. Start the Server
```bash
uv run fast_mcp/server/server.py
```

The server will:
- Start via stdio transport (MCP standard)
- Create DuckDB database at `fast_mcp/server/data/analytics.duckdb`
- Initialize connection pooling with read/write lock management
- Expose weather data collection and analysis tools

### 3. Connect an AI Assistant (The Real Value!)

#### 🎯 **Quick Demo - See AI Data Exploration in Action:**
```bash
uv run examples/ai_interrogation_demo.py
```

Watch an AI assistant:
- **Discover** your data structure dynamically
- **Ask questions** like "What's the temperature range?"
- **Write custom SQL** queries on the fly
- **Generate insights** in natural language

#### 🤖 **Claude Desktop Integration:**
```bash
# 1. Copy the MCP config
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Start Claude Desktop and ask:
# "What weather data do we have? Can you explore patterns and anomalies?"
```

#### 🔗 **Manual Claude Desktop Setup:**
Add to your Claude Desktop configuration file:
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

#### 📚 **Full Integration Guide:**
See `AI_INTEGRATION_GUIDE.md` for complete setup instructions including custom AI integrations.

## Available MCP Tools

| Tool | Purpose | AI Assistant Value |
|------|---------|-------------------|
| `fetch_weather_data(city="London")` | Collect current weather data via DLT pipeline | Real-time data ingestion for analysis |
| `query_weather_data(limit=10)` | Query historical weather records | Basic data retrieval |
| `execute_sql_query(sql_query, limit)` | **Execute custom SQL queries dynamically** | **🎯 AI writes custom analysis queries on-demand** |
| `discover_database_schema()` | **Discover tables, columns, data types** | **🔍 AI learns data structure without prior knowledge** |
| `analyze_data_quality(table_name)` | **Analyze data completeness and quality** | **📊 AI assesses data reliability** |

## Architecture & Data Flow

### Data Pipeline
```
Weather API → DLT Pipeline → DuckDB → MCP Tools → AI Assistant
```

1. **Ingestion**: MCP tools trigger DLT pipelines with write-lock protection
2. **Storage**: DLT writes to DuckDB with automatic schema evolution  
3. **Access**: Concurrent read-only queries via optimized connection pooling
4. **Integration**: AI assistants access data through standardized MCP protocol

### Connection Management
- **Read Operations**: Concurrent access with `read_only=True` connections
- **Write Operations**: Exclusive locking via `threading.RLock()` 
- **DLT Integration**: Pipeline execution coordinated with connection locks
- **No Persistent Connections**: Per-operation connections prevent lock conflicts

## 🚀 AI Assistant Data Exploration Examples

### **The Key Difference:**

**Traditional Approach:**
```
You → Write specific SQL → Get fixed results
```

**MCP + AI Approach:**
```
You → Ask natural language question → AI explores dynamically → AI writes SQL → AI interprets results → AI gives insights
```

### **Real AI Conversation Examples:**

#### 🔍 **Data Discovery**
```
You: "What data do we have available?"
AI: → discover_database_schema()
AI: "I found a weather_data.london_weather table with temperature, humidity, wind speed, and time columns. Let me explore it..."
```

#### 📊 **Dynamic Analysis**
```
You: "Show me temperature patterns"
AI: → execute_sql_query("SELECT AVG(temperature) FROM ... GROUP BY EXTRACT(hour FROM time)")
AI: "Temperatures peak at 2 PM (18.5°C) and drop overnight to 12°C. Here's the hourly breakdown..."
```

#### 🚨 **Anomaly Detection**  
```
You: "Find any unusual weather readings"
AI: → execute_sql_query("WITH stats AS ... SELECT * WHERE z_score > 2")  
AI: "I detected 3 anomalous readings: 35°C at midnight (likely sensor error) and two readings with impossible humidity values."
```

#### 🧠 **Pattern Recognition**
```
You: "How does temperature relate to humidity?"
AI: → Multiple custom SQL queries analyzing correlations
AI: "There's a strong inverse correlation (R² = 0.73). When temperatures exceed 25°C, humidity drops below 45% on average."
```

### **Why This Matters:**

- **🎯 Dynamic Discovery**: AI learns your data structure without pre-programming
- **📝 Custom Queries**: AI writes SQL based on natural language questions
- **🔍 Pattern Recognition**: AI finds relationships you might miss  
- **💬 Natural Insights**: AI explains findings in business terms
- **⚡ Real-Time**: AI adapts queries based on what it discovers

## 🎯 Quick Start - Try It Now!

```bash
# 1. Fetch some weather data
uv run fast_mcp/server/server.py &
uv run examples/basic_usage.py

# 2. Watch AI explore the data dynamically  
uv run examples/ai_interrogation_demo.py

# 3. Connect Claude Desktop and ask:
# "What weather patterns do you see in the data? Any anomalies?"
```

## Development Notes

- **Database**: `fast_mcp/server/data/analytics.duckdb` (auto-created)
- **Connection Strategy**: Read/write locks prevent conflicts during DLT operations
- **Extensibility**: Add pipelines in `pipelines/`, tools in `server.py`
- **AI Integration**: See `AI_INTEGRATION_GUIDE.md` for complete setup instructions
- **Client Support**: Works with Claude Desktop, custom MCP clients, FastMCP

---

**🚀 The real magic happens when you connect an AI assistant and watch it dynamically explore your data like a human data analyst would!**
