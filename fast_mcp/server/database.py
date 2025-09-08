import duckdb
from pathlib import Path
from typing import List, Dict
import logging
import threading
from contextlib import contextmanager
from enum import Enum

logger = logging.getLogger(__name__)


class ConnectionMode(Enum):
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"


class DataManager:
    """Centralized data management with DuckDB"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to data directory within server module
            server_dir = Path(__file__).parent
            data_dir = server_dir / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "analytics.duckdb")
        
        self.db_path = db_path
        self._write_lock = threading.RLock()
        
    @contextmanager
    def get_connection(self, mode: ConnectionMode = ConnectionMode.READ_ONLY):
        """Get database connection with appropriate locking"""
        if mode == ConnectionMode.READ_WRITE:
            with self._write_lock:
                conn = duckdb.connect(self.db_path)
                try:
                    yield conn
                finally:
                    conn.close()
        else:
            # Read-only connection - no lock needed for concurrent reads
            conn = duckdb.connect(self.db_path, read_only=True)
            try:
                yield conn
            finally:
                conn.close()

    def execute_query(self, query: str, params: tuple = (), mode: ConnectionMode = ConnectionMode.READ_ONLY) -> List[Dict]:
        """Execute query and return results as dict list"""
        try:
            with self.get_connection(mode) as conn:
                result = conn.execute(query, params).fetchall()
                columns = [desc[0] for desc in conn.description]
                return [dict(zip(columns, row)) for row in result]
        except Exception as e:
            logger.error(f"Query failed: {query}, Error: {e}")
            raise

    def execute_write(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute write query with write lock"""
        return self.execute_query(query, params, ConnectionMode.READ_WRITE)
        
    def close(self):
        """No-op - connections are managed per operation"""
        logger.info("DataManager cleanup - connections managed per operation")

    def __del__(self):
        """Cleanup on object destruction"""
        self.close()
