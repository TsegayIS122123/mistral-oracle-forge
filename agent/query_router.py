"""Query routing logic for multi-database queries"""

from typing import List, Dict, Any


class QueryRouter:
    """Routes natural language questions to appropriate databases"""
    
    # Database keywords mapping
    DB_KEYWORDS = {
        "postgresql": ["transaction", "customer", "sales", "order", "payment"],
        "mongodb": ["review", "comment", "log", "event", "activity"],
        "sqlite": ["local", "cache", "temp", "config"],
        "duckdb": ["analytics", "aggregate", "timeseries", "report"]
    }
    
    def __init__(self):
        self.trace = []
    
    def identify_databases(self, question: str) -> List[str]:
        """Identify which databases are needed to answer the question"""
        question_lower = question.lower()
        databases = []
        
        for db, keywords in self.DB_KEYWORDS.items():
            for keyword in keywords:
                if keyword in question_lower:
                    databases.append(db)
                    break
        
        # Default to PostgreSQL if none identified
        if not databases:
            databases = ["postgresql"]
        
        self.trace.append({
            "step": "identify_databases",
            "question": question,
            "databases": databases
        })
        
        return databases
    
    def generate_query(self, question: str, database: str, schema: Dict) -> str:
        """Generate appropriate query for the database type"""
        # This will be enhanced with LLM integration
        # For now, return placeholder
        
        query_templates = {
            "postgresql": f"SELECT * FROM table LIMIT 10;",
            "mongodb": f'{{"$match": {{}}}}',
            "sqlite": f"SELECT * FROM table LIMIT 10;",
            "duckdb": f"SELECT * FROM table LIMIT 10;"
        }
        
        query = query_templates.get(database, "SELECT 1;")
        
        self.trace.append({
            "step": "generate_query",
            "database": database,
            "query": query
        })
        
        return query
    
    def get_trace(self) -> List[Dict]:
        """Return the full query trace"""
        return self.trace