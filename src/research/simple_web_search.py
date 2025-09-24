# src/research/simple_web_search.py
"""
🌐 Simple Web Search System - Basit ve Etkili Web Araması
Bu sistem gerçek web araması yapar ve AI'ın öğrenmesini sağlar
"""

import logging
import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Optional
from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class SimpleWebSearchSystem:
    """
    🌐 Basit Web Araması Sistemi
    
    Özellikler:
    - DuckDuckGo instant answers
    - GeeksforGeeks scraping
    - W3Schools scraping
    - Fallback to general search
    """
    
    def __init__(self):
        self.session = None
        
        # Search URLs - Bot-friendly sites
        self.search_urls = {
            'duckduckgo': 'https://api.duckduckgo.com/?q={}&format=json&no_html=1&skip_disambig=1',
            'geeksforgeeks': 'https://www.geeksforgeeks.org/search/{}/',
            'w3schools': 'https://www.w3schools.com/search/search_asp.asp?search={}',
        }
        
        logger.info("🌐 Simple Web Search System initialized")
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=15),
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; Educational-Bot/1.0)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def search_programming_question(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Programlama sorusu için web araması yap
        
        Args:
            query: Arama sorgusu
            max_results: Maksimum sonuç sayısı
            
        Returns:
            List[Dict]: Arama sonuçları
        """
        try:
            logger.info(f"🔍 Simple web search for: {query}")
            
            async with self:
                all_results = []
                
                # 1. DuckDuckGo instant answers
                ddg_results = await self._search_duckduckgo(query)
                all_results.extend(ddg_results)
                
                # 2. GeeksforGeeks search
                if self._is_programming_query(query):
                    geeks_results = await self._search_geeksforgeeks(query, 2)
                    all_results.extend(geeks_results)
                
                # 3. W3Schools search (for web technologies)
                if self._is_web_tech_query(query):
                    w3_results = await self._search_w3schools(query, 1)
                    all_results.extend(w3_results)
                
                # Sonuçları kalite skoruna göre sırala
                all_results.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
                
                return all_results[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Simple web search error: {e}")
            return []
    
    def _is_programming_query(self, query: str) -> bool:
        """Programlama sorgusu mu kontrol et"""
        programming_keywords = [
            'java', 'android', 'python', 'javascript', 'html', 'css',
            'code', 'programming', 'tutorial', 'example', 'how to'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in programming_keywords)
    
    def _is_web_tech_query(self, query: str) -> bool:
        """Web teknolojisi sorgusu mu kontrol et"""
        web_keywords = ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'bootstrap']
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in web_keywords)
    
    async def _search_duckduckgo(self, query: str) -> List[Dict]:
        """DuckDuckGo instant answers API kullan"""
        try:
            if not self.session:
                return []
            
            search_url = self.search_urls['duckduckgo'].format(quote_plus(query))
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    results = []
                    
                    # Abstract (instant answer)
                    if data.get('Abstract'):
                        results.append({
                            'title': data.get('AbstractText', 'DuckDuckGo Answer'),
                            'content': data.get('Abstract', ''),
                            'url': data.get('AbstractURL', 'https://duckduckgo.com'),
                            'source': 'DuckDuckGo',
                            'quality_score': 8.0
                        })
                    
                    # Definition
                    if data.get('Definition'):
                        results.append({
                            'title': 'Definition',
                            'content': data.get('Definition', ''),
                            'url': data.get('DefinitionURL', 'https://duckduckgo.com'),
                            'source': 'DuckDuckGo',
                            'quality_score': 7.0
                        })
                    
                    logger.info(f"✅ Found {len(results)} DuckDuckGo results")
                    return results
                else:
                    logger.warning(f"⚠️ DuckDuckGo search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ DuckDuckGo search error: {e}")
            return []
    
    async def _search_geeksforgeeks(self, query: str, max_results: int = 2) -> List[Dict]:
        """GeeksforGeeks'te arama yap"""
        try:
            if not self.session:
                return []
            
            search_url = self.search_urls['geeksforgeeks'].format(quote_plus(query))
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    
                    # GeeksforGeeks search results
                    search_results = soup.find_all('div', class_='head')[:max_results]
                    
                    for result in search_results:
                        try:
                            link_elem = result.find('a')
                            if not link_elem:
                                continue
                            
                            title = link_elem.get_text(strip=True)
                            relative_url = link_elem.get('href', '')
                            full_url = urljoin('https://www.geeksforgeeks.org', relative_url)
                            
                            # İçerik al
                            content = await self._get_geeksforgeeks_content(full_url)
                            
                            if content:
                                result_dict = {
                                    'title': title,
                                    'content': content,
                                    'url': full_url,
                                    'source': 'GeeksforGeeks',
                                    'quality_score': 7.5
                                }
                                results.append(result_dict)
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing GeeksforGeeks result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} GeeksforGeeks results")
                    return results
                else:
                    logger.warning(f"⚠️ GeeksforGeeks search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ GeeksforGeeks search error: {e}")
            return []
    
    async def _get_geeksforgeeks_content(self, url: str) -> Optional[str]:
        """GeeksforGeeks sayfasının içeriğini al"""
        try:
            if not self.session:
                return None
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Ana içerik
                    content_div = soup.find('div', class_='text')
                    if content_div:
                        # Code blokları için özel işlem
                        code_blocks = content_div.find_all(['pre', 'code'])
                        for block in code_blocks:
                            block.string = f"\n```\n{block.get_text()}\n```\n"
                        
                        content = content_div.get_text(strip=True)
                        return content[:2000]  # İlk 2000 karakter
                    
                    return None
                else:
                    return None
                    
        except Exception as e:
            logger.warning(f"⚠️ Error fetching GeeksforGeeks content: {e}")
            return None
    
    async def _search_w3schools(self, query: str, max_results: int = 1) -> List[Dict]:
        """W3Schools'da arama yap"""
        try:
            if not self.session:
                return []
            
            # W3Schools için basit bir yaklaşım - direkt tutorial sayfalarına git
            w3_topics = {
                'html': 'https://www.w3schools.com/html/',
                'css': 'https://www.w3schools.com/css/',
                'javascript': 'https://www.w3schools.com/js/',
                'react': 'https://www.w3schools.com/react/',
                'bootstrap': 'https://www.w3schools.com/bootstrap/'
            }
            
            query_lower = query.lower()
            results = []
            
            for topic, url in w3_topics.items():
                if topic in query_lower:
                    content = await self._get_w3schools_content(url)
                    if content:
                        results.append({
                            'title': f'W3Schools {topic.upper()} Tutorial',
                            'content': content,
                            'url': url,
                            'source': 'W3Schools',
                            'quality_score': 6.5
                        })
                        break
            
            logger.info(f"✅ Found {len(results)} W3Schools results")
            return results[:max_results]
                    
        except Exception as e:
            logger.error(f"❌ W3Schools search error: {e}")
            return []
    
    async def _get_w3schools_content(self, url: str) -> Optional[str]:
        """W3Schools sayfasının içeriğini al"""
        try:
            if not self.session:
                return None
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Ana içerik
                    main_content = soup.find('div', id='main')
                    if main_content:
                        # İlk birkaç paragrafı al
                        paragraphs = main_content.find_all('p')[:5]
                        content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
                        
                        # Code örnekleri varsa ekle
                        code_examples = main_content.find_all('div', class_='w3-code')[:2]
                        for code in code_examples:
                            content += f"\n\n```\n{code.get_text()}\n```"
                        
                        return content[:1500]  # İlk 1500 karakter
                    
                    return None
                else:
                    return None
                    
        except Exception as e:
            logger.warning(f"⚠️ Error fetching W3Schools content: {e}")
            return None


# Convenience function for easy import
async def search_programming_question(query: str, max_results: int = 3) -> List[Dict]:
    """
    Programlama sorusu için basit web araması yap
    
    Args:
        query: Arama sorgusu
        max_results: Maksimum sonuç sayısı
        
    Returns:
        List[Dict]: Arama sonuçları
    """
    search_system = SimpleWebSearchSystem()
    return await search_system.search_programming_question(query, max_results)