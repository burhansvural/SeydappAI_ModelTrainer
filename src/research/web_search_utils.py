# src/research/web_search_utils.py
"""
🔍 Web Search Utilities for AI Chat
Enhanced search functionality for programming questions - NOW USING REAL WEB SEARCH
"""

import logging
import asyncio
from typing import List, Dict, Optional
import re

logger = logging.getLogger(__name__)


async def search_programming_question(query: str) -> List[Dict]:
    """
    Search for programming-related questions using REAL web search
    
    Args:
        query: The search query
        
    Returns:
        List of search results with title, content, and url
    """
    try:
        logger.info(f"🌐 REAL web search for programming question: {query}")
        
        # Use real web search system for real results
        from .real_web_search import RealWebSearchSystem
        
        search_system = RealWebSearchSystem()
        results = await search_system.search_programming_question(query, max_results=3)
        
        if results:
            logger.info(f"✅ Found {len(results)} real web results")
            return results
        else:
            logger.warning(f"⚠️ No real web results found for: {query}")
            return []
        
    except Exception as e:
        logger.error(f"❌ Real web search error: {e}")
        # Return empty list instead of mock data
        return []


class WebSearchUtils:
    """Legacy web search utils class - kept for compatibility"""
    
    def __init__(self):
        logger.info("🔄 WebSearchUtils initialized - using real web search")
        
    async def search(self, query: str) -> List[Dict]:
        """Search using real web search system"""
        return await search_programming_question(query)