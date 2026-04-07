"""Resolves join key format mismatches across databases"""

import re
from typing import Dict, Any, List


class JoinResolver:
    """Detects and fixes inconsistent join key formats"""
    
    # Known format patterns from DAB datasets
    FORMAT_PATTERNS = {
        "int_to_cust_prefix": {
            "source_pattern": r"^\d+$",
            "target_pattern": r"^CUST-\d+$",
            "transform": lambda x: f"CUST-{x}" if x.isdigit() else x
        },
        "cust_prefix_to_int": {
            "source_pattern": r"^CUST-(\d+)$",
            "target_pattern": r"^\d+$",
            "transform": lambda x: re.sub(r"^CUST-", "", x) if x.startswith("CUST-") else x
        },
        "string_to_int": {
            "source_pattern": r"^\d+$",
            "target_pattern": r"^\d+$",
            "transform": lambda x: int(x) if x.isdigit() else x
        }
    }
    
    def __init__(self):
        self.resolutions_applied = []
    
    def detect_mismatch(self, value_from_db1: Any, value_from_db2: Any) -> bool:
        """Detect if two values represent the same entity but different format"""
        str1 = str(value_from_db1)
        str2 = str(value_from_db2)
        
        # Check if they might match after transformation
        for pattern_name, pattern in self.FORMAT_PATTERNS.items():
            if re.match(pattern["source_pattern"], str1) and re.match(pattern["target_pattern"], str2):
                transformed = pattern["transform"](str1)
                if str(transformed) == str2:
                    self.resolutions_applied.append({
                        "pattern": pattern_name,
                        "original": str1,
                        "transformed": str(transformed),
                        "target": str2
                    })
                    return True
        
        return False
    
    def resolve(self, value: Any, target_format: str) -> Any:
        """Transform value to target format"""
        str_value = str(value)
        
        for pattern_name, pattern in self.FORMAT_PATTERNS.items():
            if re.match(pattern["source_pattern"], str_value):
                if target_format in pattern_name:
                    return pattern["transform"](str_value)
        
        return value
    
    def merge(self, results: List[Dict]) -> Dict:
        """Merge results from multiple databases after resolving join keys"""
        if not results:
            return {}
        
        # Simple merge for now - will be enhanced
        merged = {"data": [], "joins_applied": self.resolutions_applied}
        
        for result in results:
            if "data" in result:
                merged["data"].extend(result["data"])
            else:
                merged["data"].append(result)
        
        return merged