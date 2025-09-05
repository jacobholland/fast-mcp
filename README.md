# FastMCP Playground

A development playground for experimenting with FastMCP servers and clients. This project demonstrates:

- FastMCP server with weather data collection
- DuckDB integration for data storage
- DLT pipelines for data processing
- Simple client examples

## Project Structure

```
fast-mcp/
├── fast_mcp/           # Main package
│   ├── server/         # Server components
│   │   ├── server.py   # Main MCP server with tools
│   │   ├── data_manager.py  # DuckDB data management
│   │   └── pipelines/  # Data processing pipelines
│   └── client/         # Client components
├── examples/           # Usage examples
└── pyproject.toml      # Project configuration
```

## Quick Start

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the server:
   ```bash
   cd fast_mcp/server
   uv run server.py
   ```

3. Run the client example:
   ```bash
   uv run examples/basic_usage.py
   ```

## Available Tools

- `fetch_weather_data(city)` - Fetch and store weather data
- `query_weather_data(limit)` - Query stored weather records
- `get_table_info()` - Get database information
- `trigger_dlt_pipeline(pipeline_name)` - Run data pipelines
