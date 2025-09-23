# src/knowledge/__init__.py
"""
🧠 Knowledge Module - Singleton Pattern for Persistence
Search results [3] pattern: Global state management[3]
"""
from datetime import datetime
from typing import List, Dict, Optional
from .knowledge_processor import KnowledgeProcessor

# ✅ Global singleton instance
_global_knowledge_processor = None


def get_knowledge_processor() -> KnowledgeProcessor:
    """✅ SEARCH RESULTS [3] PATTERN: Singleton for persistent state[3]"""
    global _global_knowledge_processor

    if _global_knowledge_processor is None:
        _global_knowledge_processor = KnowledgeProcessor()

    return _global_knowledge_processor


def get_knowledge_stats() -> Dict:
    """Quick stats access"""
    processor = get_knowledge_processor()
    return {
        "total_entities": len(processor.knowledge_graph),
        "graph_file_exists": processor.knowledge_graph_file.exists(),
        "last_updated": datetime.now().strftime("%H:%M")
    }
