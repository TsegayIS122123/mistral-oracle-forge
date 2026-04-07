"""Database connector using MCP Toolbox"""

from typing import Dict, Any, Optional
import requests
import os


class DBConnector:
    """Handles all database connections via MCP Toolbox"""
    
    def __init__(self, toolbox_url: str = None):
        self.toolbox_url = toolbox_url or os.getenv("MCP_TOOLBOX_URL", "http://localhost:5000")
    
    def execute(self, database: str, query: str) -> Optional[Dict[str, Any]]:
        """Execute query on specified database"""
        
        # Map database to tool name
        tool_map = {
            "postgresql": "query_postgres",
            "mongodb": "query_mongodb",
            "sqlite": "query_sqlite",
            "duckdb": "query_duckdb"
        }
        
        tool = tool_map.get(database)
        if not tool:
            return {"error": f"Unknown database: {database}"}
        
        # Call MCP Toolbox
        try:
            response = requests.post(
                f"{self.toolbox_url}/v1/tools/{tool}",
                json={"query": query},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "database": database, "query": query}