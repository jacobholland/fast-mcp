# FastMCP Playground

A development playground for experimenting with FastMCP servers and clients. This project demonstrates:

- FastMCP server with weather data collection via DLT pipelines
- DuckDB integration for data storage and querying
- Clean separation of data ingestion (DLT) and querying (DataManager)
- Client examples for interacting with MCP tools

## Project Structure

```
fast-mcp/
├── fast_mcp/                    # Main package
│   ├── server/                  # Server components
│   │   ├── server.py           # Main MCP server with tools
│   │   ├── database.py         # DuckDB query interface
│   │   ├── data/               # Data persistence directory
│   │   └── pipelines/          # DLT data processing pipelines
│   │       └── weather_pipeline.py
│   └── client/                 # Client components
│       └── client.py
├── examples/                   # Usage examples
│   └── basic_usage.py
└── pyproject.toml             # Project configuration
```

## Getting Started

### 1. Install Dependencies
```bash
uv sync
```

### 2. Start the Server
```bash
cd fast_mcp/server
uv run server.py
```

The server will:
- Start on the default FastMCP port
- Create a DuckDB database in `fast_mcp/server/data/analytics.duckdb`
- Initialize tables for weather data, metrics, and events
- Log the database path for verification

### 3. Use the Tools

Once the server is running, you can interact with it via:

#### A. Run the Client Example
In a new terminal:
```bash
uv run examples/basic_usage.py
```

This will demonstrate:
- Triggering weather data collection
- Querying stored data
- Getting database information

#### B. Use with Claude Desktop or Other MCP Clients
Configure your MCP client to connect to the server and use the available tools.

## Available MCP Tools

| Tool | Purpose | Usage |
|------|---------|--------|
| `fetch_weather_data(city="London")` | Trigger DLT pipeline to collect weather data | Runs the weather pipeline to fetch and store data |
| `query_weather_data(limit=10)` | Query stored weather records | Returns recent weather data from DuckDB |
| `get_table_info()` | Get database schema and stats | Shows row counts, available cities, table info |
| `trigger_dlt_pipeline(pipeline_name="weather")` | Run specific DLT pipeline | Manually trigger data collection pipelines |

## Data Flow

1. **Data Collection**: `fetch_weather_data()` or `trigger_dlt_pipeline()` → DLT pipeline fetches from APIs
2. **Data Storage**: DLT writes data to DuckDB tables in `fast_mcp/server/data/`
3. **Data Querying**: `query_weather_data()` and `get_table_info()` → DataManager reads from DuckDB

## Development Notes

- **Data Persistence**: All data is stored in `fast_mcp/server/data/analytics.duckdb`
- **Clean Separation**: DLT handles writes, DataManager handles reads
- **Extensible**: Add new pipelines in `pipelines/` and new tools in `server.py`
