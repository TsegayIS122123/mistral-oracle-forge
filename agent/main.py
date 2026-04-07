#!/usr/bin/env python3
"""Mistral Oracle Forge - Main Agent Entry Point"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Fix imports for both direct and module execution
try:
    from agent.query_router import QueryRouter
    from agent.db_connector import DBConnector
    from agent.join_resolver import JoinResolver
except ImportError:
    from query_router import QueryRouter
    from db_connector import DBConnector
    from join_resolver import JoinResolver


class OracleForgeAgent:
    """Main agent class for multi-database analytics"""
    
    def __init__(self, kb_path: str = "kb"):
        self.kb_path = Path(kb_path)
        self.router = QueryRouter()
        self.connector = DBConnector()
        self.join_resolver = JoinResolver()
        self.context = self._load_context()
    
    def _load_context(self) -> Dict[str, str]:
        """Load all three context layers from KB"""
        context = {}
        
        # Layer 1: Schema & metadata
        schema_file = self.kb_path / "domain" / "schema.md"
        if schema_file.exists():
            context["schema"] = schema_file.read_text()
        
        # Layer 2: Institutional knowledge
        join_file = self.kb_path / "domain" / "join-glossary.md"
        if join_file.exists():
            context["join_knowledge"] = join_file.read_text()
        
        # Layer 3: Corrections log (most important)
        corrections_file = self.kb_path / "corrections" / "corrections-log.md"
        if corrections_file.exists():
            context["corrections"] = corrections_file.read_text()
        
        return context
    
    def answer(self, question: str) -> Dict[str, Any]:
        """Answer a natural language question"""
        
        # Step 1: Identify required databases
        databases = self.router.identify_databases(question)
        
        # Step 2: Load relevant schema
        schema = self._get_relevant_schema(databases)
        
        # Step 3: Generate and execute queries
        results = []
        for db in databases:
            query = self.router.generate_query(question, db, schema)
            result = self.connector.execute(db, query)
            results.append(result)
        
        # Step 4: Resolve joins if multiple databases
        if len(results) > 1:
            final_result = self.join_resolver.merge(results)
        else:
            final_result = results[0] if results else None
        
        # Step 5: Format answer with trace
        return {
            "answer": self._format_answer(final_result),
            "query_trace": self.router.get_trace(),
            "confidence": self._calculate_confidence(final_result),
            "databases_used": databases,
            "corrections_applied": []
        }
    
    def _get_relevant_schema(self, databases: list) -> Dict:
        """Extract schema relevant to the databases needed"""
        return {}
    
    def _format_answer(self, result) -> str:
        """Format result for user"""
        if result is None:
            return "Could not answer the question."
        if isinstance(result, dict) and "error" in result:
            return f"Error: {result['error']}"
        return str(result)
    
    def _calculate_confidence(self, result) -> int:
        """Calculate confidence score 1-3"""
        if result is None:
            return 1
        if isinstance(result, dict) and "error" in result:
            return 1
        return 3


def main():
    parser = argparse.ArgumentParser(description="Mistral Oracle Forge Agent")
    parser.add_argument("--question", "-q", type=str, help="Question to answer")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    agent = OracleForgeAgent()
    
    if args.interactive:
        print("🔮 Mistral Oracle Forge Agent")
        print("Type 'exit' to quit\n")
        while True:
            question = input("> ")
            if question.lower() == "exit":
                break
            result = agent.answer(question)
            print(f"\nAnswer: {result['answer']}")
            print(f"Confidence: {result['confidence']}/3")
            print(f"Databases: {result['databases_used']}\n")
    
    elif args.question:
        result = agent.answer(args.question)
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()