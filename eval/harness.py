#!/usr/bin/env python3
"""Minimal Evaluation Harness for Oracle Forge"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.main import OracleForgeAgent


class EvaluationHarness:
    """Minimal harness for testing agent performance"""
    
    def __init__(self):
        self.agent = OracleForgeAgent()
        self.results = []
    
    def run_query(self, query: str, expected_answer: str = None) -> Dict[str, Any]:
        """Run a single query and record result"""
        try:
            result = self.agent.answer(query)
            is_correct = None
            if expected_answer:
                is_correct = expected_answer.lower() in str(result.get("answer", "")).lower()
            
            return {
                "query": query,
                "answer": result.get("answer"),
                "confidence": result.get("confidence"),
                "trace": result.get("query_trace"),
                "expected": expected_answer,
                "passed": is_correct if expected_answer else None
            }
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "passed": False
            }
    
    def run_held_out_set(self, queries_file: str) -> List[Dict]:
        """Run all held-out queries"""
        with open(queries_file, 'r') as f:
            queries = json.load(f)
        
        results = []
        for item in queries:
            print(f"Running: {item['query'][:50]}...")
            result = self.run_query(item['query'], item.get('expected'))
            results.append(result)
            
            # Print progress
            status = "✓" if result.get("passed") else "✗" if result.get("passed") is False else "?"
            print(f"  {status} {result.get('answer', 'error')[:50]}")
        
        # Calculate score
        passed = [r for r in results if r.get("passed") is True]
        score = len(passed) / len([r for r in results if r.get("passed") is not None]) if results else 0
        
        # Save results
        self.results = results
        self.score = score
        
        return results
    
    def save_score_log(self, log_file: str = "eval/score_log.md"):
        """Save score log with improvement tracking"""
        with open(log_file, 'w') as f:
            f.write(f"# Score Log\n\n")
            f.write(f"## Run {len(self.results)} queries\n\n")
            f.write(f"**Pass@1 Score:** {self.score:.1%}\n\n")
            f.write(f"## Results Summary\n\n")
            f.write(f"| Query | Passed | Answer |\n")
            f.write(f"|-------|--------|--------|\n")
            for r in self.results:
                query_short = r['query'][:40] + "..."
                passed = "✅" if r.get("passed") else "❌" if r.get("passed") is False else "⏳"
                answer = str(r.get("answer", r.get("error", "")))[:40]
                f.write(f"| {query_short} | {passed} | {answer} |\n")


def main():
    parser = argparse.ArgumentParser(description="Evaluation Harness")
    parser.add_argument("--held-out", help="JSON file with held-out queries")
    parser.add_argument("--query", "-q", help="Single query to run")
    
    args = parser.parse_args()
    
    harness = EvaluationHarness()
    
    if args.held_out:
        print(f"Running held-out set from {args.held_out}")
        results = harness.run_held_out_set(args.held_out)
        harness.save_score_log()
        print(f"\n📊 Score: {harness.score:.1%}")
        
    elif args.query:
        result = harness.run_query(args.query)
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result.get('confidence')}")
        
    else:
        print("Usage: python eval/harness.py --held-out eval/held_out_queries.json")
        print("   or: python eval/harness.py --query 'your question'")


if __name__ == "__main__":
    main()