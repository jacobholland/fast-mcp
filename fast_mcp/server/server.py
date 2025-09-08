from fastmcp import FastMCP
from fast_mcp.server.database import DataManager
from fast_mcp.server.pipelines.weather_pipeline import load_weather_simple
import logging
import json
from datetime import datetime

# Initialize logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize data manager and MCP server
data_manager = DataManager()
mcp = FastMCP("DataEngineering-DuckDB-Server")


@mcp.tool
async def fetch_weather_data(city: str = "London") -> str:
    """Trigger DLT pipeline to fetch and store weather data"""
    try:
        # Trigger the DLT weather pipeline
        load_weather_simple(data_manager)
        
        return json.dumps(
            {
                "status": "success",
                "message": f"Weather data pipeline completed for {city}",
                "pipeline": "weather",
                "triggered_at": datetime.now().isoformat(),
            },
            indent=2,
        )

    except Exception as e:
        logger.error(f"Weather pipeline failed: {e}")
        return f"Error running weather pipeline: {str(e)}"

@mcp.tool
def query_weather_data(limit: int = 10) -> str:
    """Query the stored weather data - simple analytics"""
    try:
        query = """
            SELECT 
              latitude
            , longitude
            , current_units__time
            , current_units__temperature_2m

            FROM weather_data.london_weather
            LIMIT ?
        """

        results = data_manager.execute_query(query, (limit,))

        if not results:
            return json.dumps({"message": "No weather data found"})

        return json.dumps({
            "status": "success",
            "record_count": len(results),
            "data": results
        }, indent=2)

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return f"Error querying weather data: {str(e)}"

@mcp.tool
def weather_analytics(analysis_type: str = "summary") -> str:
    """Perform weather data analytics for business insights"""
    try:
        if analysis_type == "summary":
            query = """
            SELECT 
                COUNT(*) as total_records,
                MIN(current__time) as earliest_record,
                MAX(current__time) as latest_record,
                AVG(CAST(current__temperature_2m AS FLOAT)) as avg_temperature,
                MIN(CAST(current__temperature_2m AS FLOAT)) as min_temperature,
                MAX(CAST(current__temperature_2m AS FLOAT)) as max_temperature
            FROM weather_data.london_weather
            WHERE current__temperature_2m IS NOT NULL
            """
        elif analysis_type == "trends":
            query = """
            SELECT 
                DATE(current__time) as date,
                AVG(CAST(current__temperature_2m AS FLOAT)) as avg_temp,
                MIN(CAST(current__temperature_2m AS FLOAT)) as min_temp,
                MAX(CAST(current__temperature_2m AS FLOAT)) as max_temp
            FROM weather_data.london_weather
            WHERE current__temperature_2m IS NOT NULL
            GROUP BY DATE(current__time)
            ORDER BY date DESC
            LIMIT 7
            """
        elif analysis_type == "conditions":
            query = """
            SELECT 
                CASE 
                    WHEN CAST(current__temperature_2m AS FLOAT) < 10 THEN 'Cold'
                    WHEN CAST(current__temperature_2m AS FLOAT) < 20 THEN 'Mild' 
                    ELSE 'Warm'
                END as condition_category,
                COUNT(*) as frequency,
                AVG(CAST(current__temperature_2m AS FLOAT)) as avg_temp_in_category
            FROM weather_data.london_weather
            WHERE current__temperature_2m IS NOT NULL
            GROUP BY condition_category
            ORDER BY frequency DESC
            """
        else:
            return json.dumps({"error": f"Unknown analysis type: {analysis_type}. Use 'summary', 'trends', or 'conditions'"})

        results = data_manager.execute_query(query)

        if not results:
            return json.dumps({"message": "No weather data available for analysis"})

        return json.dumps({
            "analysis_type": analysis_type,
            "status": "success",
            "insights": results,
            "generated_at": datetime.now().isoformat()
        }, indent=2)

    except Exception as e:
        logger.error(f"Analytics failed: {e}")
        return f"Error performing weather analytics: {str(e)}"

@mcp.tool
def execute_sql_query(sql_query: str, limit: int = 100) -> str:
    """Execute custom SQL queries on the weather database - AI can explore data dynamically"""
    try:
        # Basic SQL injection protection
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'TRUNCATE']
        sql_upper = sql_query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return json.dumps({
                    "error": f"Query contains dangerous keyword: {keyword}",
                    "message": "Only SELECT queries are allowed for data exploration"
                })
        
        # Add LIMIT if not present to prevent runaway queries
        if 'LIMIT' not in sql_upper and limit:
            sql_query = f"{sql_query.rstrip(';')} LIMIT {limit}"
        
        results = data_manager.execute_query(sql_query)
        
        return json.dumps({
            "status": "success",
            "query": sql_query,
            "record_count": len(results),
            "data": results,
            "executed_at": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        logger.error(f"SQL query failed: {e}")
        return json.dumps({
            "error": str(e),
            "query": sql_query,
            "message": "Query execution failed - check syntax and table names"
        })

@mcp.tool
def discover_database_schema() -> str:
    """Discover available tables, columns, and data types - AI can understand the data structure"""
    try:
        # Get all tables
        tables_query = """
        SELECT table_schema, table_name, table_type 
        FROM information_schema.tables 
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name
        """
        
        tables = data_manager.execute_query(tables_query)
        
        schema_info = {"tables": []}
        
        for table in tables:
            table_name = f"{table['table_schema']}.{table['table_name']}"
            
            # Get column information for each table
            columns_query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = ? AND table_name = ?
            ORDER BY ordinal_position
            """
            
            columns = data_manager.execute_query(
                columns_query, 
                (table['table_schema'], table['table_name'])
            )
            
            # Get sample data
            sample_query = f"SELECT * FROM {table_name} LIMIT 3"
            try:
                sample_data = data_manager.execute_query(sample_query)
            except:
                sample_data = []
            
            schema_info["tables"].append({
                "name": table_name,
                "type": table['table_type'],
                "columns": columns,
                "sample_rows": len(sample_data),
                "sample_data": sample_data[:2] if sample_data else []
            })
        
        return json.dumps({
            "status": "success",
            "database_schema": schema_info,
            "discovered_at": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Schema discovery failed: {e}")
        return f"Error discovering database schema: {str(e)}"

@mcp.tool
def analyze_data_quality(table_name: str = "weather_data.london_weather") -> str:
    """Analyze data quality metrics - AI can understand data completeness and issues"""
    try:
        # Get table row count
        count_query = f"SELECT COUNT(*) as total_rows FROM {table_name}"
        count_result = data_manager.execute_query(count_query)
        total_rows = count_result[0]['total_rows'] if count_result else 0
        
        # Get column information
        columns_query = f"DESCRIBE {table_name}"
        try:
            columns = data_manager.execute_query(columns_query)
        except:
            # Fallback method for getting columns
            sample_query = f"SELECT * FROM {table_name} LIMIT 1"
            sample = data_manager.execute_query(sample_query)
            columns = [{"column_name": col, "column_type": "unknown"} for col in sample[0].keys()] if sample else []
        
        quality_metrics = {
            "table": table_name,
            "total_rows": total_rows,
            "columns": []
        }
        
        # Analyze each column
        for col in columns:
            col_name = col.get('column_name') or col.get('Field', '')
            if not col_name:
                continue
                
            # Check for nulls and get basic stats
            analysis_query = f"""
            SELECT 
                COUNT(*) as non_null_count,
                COUNT(*) - COUNT({col_name}) as null_count,
                COUNT(DISTINCT {col_name}) as distinct_values
            FROM {table_name}
            """
            
            try:
                stats = data_manager.execute_query(analysis_query)
                if stats:
                    stat = stats[0]
                    quality_metrics["columns"].append({
                        "name": col_name,
                        "type": col.get('column_type', col.get('Type', 'unknown')),
                        "non_null_count": stat['non_null_count'],
                        "null_count": stat['null_count'],
                        "null_percentage": round((stat['null_count'] / total_rows * 100), 2) if total_rows > 0 else 0,
                        "distinct_values": stat['distinct_values']
                    })
            except Exception as col_error:
                quality_metrics["columns"].append({
                    "name": col_name,
                    "type": col.get('column_type', col.get('Type', 'unknown')),
                    "error": str(col_error)
                })
        
        return json.dumps({
            "status": "success",
            "data_quality": quality_metrics,
            "analyzed_at": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Data quality analysis failed: {e}")
        return f"Error analyzing data quality: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting simplified DuckDB MCP Server...")
    logger.info(f"Database: {data_manager.db_path}")
    mcp.run()
