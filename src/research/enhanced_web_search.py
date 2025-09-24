# src/research/enhanced_web_search.py
"""
🌐 Enhanced Web Search System - Gelişmiş İnternet Araması
Bu sistem gerçek web scraping yapar ve güncel bilgileri getirir
"""

import logging
import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Optional, Tuple
from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class EnhancedWebSearchSystem:
    """
    🌐 Gelişmiş Web Araması Sistemi
    
    Özellikler:
    - Stack Overflow scraping
    - GitHub repository search
    - MDN documentation search
    - Multiple search engines
    """
    
    def __init__(self):
        self.session = None
        
        # Search URLs
        self.search_urls = {
            'stackoverflow': 'https://stackoverflow.com/search?q={}',
            'github': 'https://github.com/search?q={}&type=repositories',
            'mdn': 'https://developer.mozilla.org/en-US/search?q={}',
            'w3schools': 'https://www.w3schools.com/search/search_asp.asp?search={}',
            'geeksforgeeks': 'https://www.geeksforgeeks.org/search/{}/',
            'duckduckgo': 'https://duckduckgo.com/html/?q={}'
        }
        
        # Güvenilir kaynaklar
        self.trusted_domains = [
            'stackoverflow.com',
            'github.com',
            'developer.mozilla.org',
            'docs.python.org',
            'developer.android.com',
            'reactjs.org',
            'vuejs.org',
            'angular.io',
            'flask.palletsprojects.com',
            'django.readthedocs.io',
            'pytorch.org',
            'tensorflow.org',
            'w3schools.com',
            'geeksforgeeks.org'
        ]
        
        logger.info("🌐 Enhanced Web Search System initialized")
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def search_programming_question(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Programlama sorusu için çoklu kaynak web araması yap
        
        Args:
            query: Arama sorgusu
            max_results: Maksimum sonuç sayısı
            
        Returns:
            List[Dict]: Kalite skoruna göre sıralanmış arama sonuçları
        """
        try:
            logger.info(f"🔍 Multi-source web search for: {query}")
            
            # Session'ı başlat
            async with self:
                all_results = []
                search_tasks = []
                
                # Paralel arama görevleri oluştur - çoklu kaynak stratejisi
                search_tasks.append(self._search_stackoverflow(query, 2))
                search_tasks.append(self._search_github(query, 2))
                search_tasks.append(self._search_geeksforgeeks_real(query, 2))
                search_tasks.append(self._search_w3schools_real(query, 1))
                search_tasks.append(self._search_mdn_real(query, 1))
                search_tasks.append(self._search_bing(query, 3))
                search_tasks.append(self._search_duckduckgo(query, 2))
                search_tasks.append(self._search_google_scholar(query, 1))
                search_tasks.append(self._search_alternative_sources(query, 2))
                
                # Tüm aramaları paralel olarak çalıştır
                logger.info("🚀 Starting parallel searches across multiple sources...")
                search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
                
                # Sonuçları birleştir
                for i, results in enumerate(search_results):
                    if isinstance(results, Exception):
                        logger.warning(f"⚠️ Search task {i} failed: {results}")
                        continue
                    
                    if isinstance(results, list):
                        all_results.extend(results)
                        logger.info(f"✅ Source {i} returned {len(results)} results")
                
                # Duplicate removal (URL bazında)
                seen_urls = set()
                unique_results = []
                for result in all_results:
                    url = result.get('url', '')
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        unique_results.append(result)
                
                # Gelişmiş kalite skorlaması
                for result in unique_results:
                    result['quality_score'] = self._calculate_advanced_quality_score(result)
                
                # Sonuçları kalite skoruna göre sırala
                unique_results.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
                
                logger.info(f"🎯 Found {len(unique_results)} unique results from multiple sources")
                logger.info(f"📊 Top 3 quality scores: {[r.get('quality_score', 0) for r in unique_results[:3]]}")
                
                return unique_results[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Multi-source web search error: {e}")
            return []
    
    def _is_code_search(self, query: str) -> bool:
        """Kod araması mı kontrol et"""
        code_keywords = ['example', 'code', 'implementation', 'tutorial', 'how to']
        return any(keyword in query.lower() for keyword in code_keywords)
    
    def _is_web_tech_search(self, query: str) -> bool:
        """Web teknolojisi araması mı kontrol et"""
        web_keywords = ['html', 'css', 'javascript', 'react', 'vue', 'angular']
        return any(keyword in query.lower() for keyword in web_keywords)
    
    def _is_android_card_question(self, query: str) -> bool:
        """Android kart oluşturma sorusu mu kontrol et"""
        query_lower = query.lower()
        android_keywords = ['android', 'java']
        card_keywords = ['kart', 'card', 'profil', 'profile']
        
        has_android = any(keyword in query_lower for keyword in android_keywords)
        has_card = any(keyword in query_lower for keyword in card_keywords)
        
        return has_android and has_card
    
    async def _search_android_card_creation(self, query: str, max_results: int = 3) -> List[Dict]:
        """Android kart oluşturma için özel arama"""
        try:
            logger.info(f"🎯 Specialized Android card search for: {query}")
            
            # Özel arama terimleri
            search_terms = [
                "Android CardView Java profile card",
                "Android custom card layout with image",
                "Android RecyclerView card design Java"
            ]
            
            all_results = []
            
            for search_term in search_terms:
                # Stack Overflow'da ara
                stackoverflow_results = await self._search_stackoverflow(search_term, 1)
                all_results.extend(stackoverflow_results)
                
                # GitHub'da ara
                github_results = await self._search_github(search_term, 1)
                all_results.extend(github_results)
                
                # Çok fazla istek yapmamak için kısa bekleme
                await asyncio.sleep(0.5)
            
            # Sonuçları kalite skoruna göre sırala
            all_results.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
            
            # En iyi sonuçları seç
            best_results = all_results[:max_results]
            
            # Eğer yeterli sonuç yoksa, genel arama yap
            if len(best_results) < max_results:
                general_results = await self._search_stackoverflow(query, max_results - len(best_results))
                best_results.extend(general_results)
            
            return best_results[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Android card search error: {e}")
            return []
    
    async def _search_stackoverflow(self, query: str, max_results: int = 2) -> List[Dict]:
        """Stack Overflow'da arama yap - Gelişmiş HTML parsing"""
        try:
            if not self.session:
                return []
            
            search_url = self.search_urls['stackoverflow'].format(quote_plus(query))
            logger.info(f"🔍 Searching Stack Overflow: {search_url}")
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    
                    # Farklı HTML yapılarını dene
                    search_results = (
                        soup.find_all('div', class_='s-post-summary') or
                        soup.find_all('div', class_='question-summary') or
                        soup.find_all('div', class_='search-result')
                    )[:max_results]
                    
                    if not search_results:
                        logger.warning("⚠️ No Stack Overflow search results found in HTML")
                        return []
                    
                    for result in search_results:
                        try:
                            # Başlık ve link - farklı yapıları dene
                            title_elem = (
                                result.find('h3', class_='s-post-summary--content-title') or
                                result.find('h3', class_='question-hyperlink') or
                                result.find('a', class_='question-hyperlink') or
                                result.find('h3').find('a') if result.find('h3') else None
                            )
                            
                            if not title_elem:
                                continue
                            
                            # Link elementi bul
                            if title_elem.name == 'a':
                                link_elem = title_elem
                                title = link_elem.get_text(strip=True)
                            else:
                                link_elem = title_elem.find('a')
                                if not link_elem:
                                    continue
                                title = link_elem.get_text(strip=True)
                            
                            relative_url = link_elem.get('href', '')
                            if not relative_url:
                                continue
                                
                            full_url = urljoin('https://stackoverflow.com', relative_url)
                            
                            # Özet - farklı yapıları dene
                            excerpt_elem = (
                                result.find('div', class_='s-post-summary--content-excerpt') or
                                result.find('div', class_='excerpt') or
                                result.find('div', class_='summary')
                            )
                            excerpt = excerpt_elem.get_text(strip=True) if excerpt_elem else title
                            
                            # Skor ve cevap sayısı
                            score = 0
                            answer_count = 0
                            
                            # Stats bul
                            stats = (
                                result.find('div', class_='s-post-summary--stats') or
                                result.find('div', class_='statscontainer') or
                                result.find('div', class_='stats')
                            )
                            
                            if stats:
                                # Score bul
                                score_elems = stats.find_all('span', class_='s-post-summary--stats-item-number')
                                if not score_elems:
                                    score_elems = stats.find_all('span', class_='vote-count-post')
                                
                                if score_elems:
                                    try:
                                        score = int(score_elems[0].get_text(strip=True))
                                    except:
                                        pass
                                
                                # Answer count bul
                                if len(score_elems) > 1:
                                    try:
                                        answer_count = int(score_elems[1].get_text(strip=True))
                                    except:
                                        pass
                            
                            # Basit içerik oluştur (detaylı içerik almaya çalışma)
                            content = f"{title}\n\n{excerpt}"
                            
                            result_dict = {
                                'title': title,
                                'content': content,
                                'url': full_url,
                                'source': 'Stack Overflow',
                                'score': score,
                                'answer_count': answer_count,
                                'quality_score': self._calculate_stackoverflow_quality(score, answer_count, len(content))
                            }
                            
                            results.append(result_dict)
                            logger.info(f"✅ Stack Overflow result: {title[:50]}...")
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing Stack Overflow result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} Stack Overflow results")
                    return results
                else:
                    logger.warning(f"⚠️ Stack Overflow search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ Stack Overflow search error: {e}")
            return []
    
    async def _get_stackoverflow_content(self, url: str) -> Optional[str]:
        """Stack Overflow sayfasının detaylı içeriğini al"""
        try:
            if not self.session:
                return None
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Soru içeriği
                    question_body = soup.find('div', class_='s-prose')
                    if question_body:
                        # Code blokları için özel işlem
                        code_blocks = question_body.find_all(['code', 'pre'])
                        for block in code_blocks:
                            block.string = f"\n```\n{block.get_text()}\n```\n"
                        
                        content = question_body.get_text(strip=True)
                        return content[:1500]  # İlk 1500 karakter
                    
                    return None
                else:
                    return None
                    
        except Exception as e:
            logger.warning(f"⚠️ Error fetching Stack Overflow content: {e}")
            return None
    
    async def _search_github(self, query: str, max_results: int = 2) -> List[Dict]:
        """GitHub'da repository araması yap - Gelişmiş HTML parsing"""
        try:
            if not self.session:
                return []
            
            search_url = self.search_urls['github'].format(quote_plus(query))
            logger.info(f"🔍 Searching GitHub: {search_url}")
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    
                    # Farklı GitHub HTML yapılarını dene
                    repo_items = (
                        soup.find_all('div', class_='Box-sc-g0xbh4-0') or
                        soup.find_all('div', class_='repo-list-item') or
                        soup.find_all('li', class_='repo-list-item') or
                        soup.find_all('div', {'data-testid': 'results-list'}) or
                        soup.find_all('div', class_='f4')
                    )[:max_results]
                    
                    if not repo_items:
                        logger.warning("⚠️ No GitHub search results found in HTML")
                        return []
                    
                    for item in repo_items:
                        try:
                            # Repository adı ve linki - farklı yapıları dene
                            title_elem = (
                                item.find('a', {'data-testid': 'results-list'}) or
                                item.find('a', class_='v-align-middle') or
                                item.find('h3').find('a') if item.find('h3') else None or
                                item.find('a', href=lambda x: x and '/search' not in x)
                            )
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            href = title_elem.get('href', '')
                            
                            if not href:
                                continue
                                
                            repo_url = urljoin('https://github.com', href)
                            
                            # Açıklama - farklı yapıları dene
                            desc_elem = (
                                item.find('p', class_='color-fg-muted') or
                                item.find('p', class_='repo-list-description') or
                                item.find('p', class_='mb-1') or
                                item.find('p')
                            )
                            description = desc_elem.get_text(strip=True) if desc_elem else title
                            
                            # Yıldız sayısı - farklı yapıları dene
                            star_elem = (
                                item.find('span', {'aria-label': lambda x: x and 'stars' in x}) or
                                item.find('a', href=lambda x: x and 'stargazers' in x) or
                                item.find('span', class_='text-bold')
                            )
                            
                            stars = 0
                            if star_elem:
                                try:
                                    star_text = star_elem.get_text(strip=True).replace(',', '').replace('k', '000')
                                    stars = int(''.join(filter(str.isdigit, star_text)))
                                except:
                                    pass
                            
                            # İçerik oluştur
                            content = f"{title}\n\n{description}"
                            
                            result_dict = {
                                'title': f"GitHub: {title}",
                                'content': content,
                                'url': repo_url,
                                'source': 'GitHub',
                                'stars': stars,
                                'quality_score': min(6.0 + (stars * 0.001), 9.0)  # Yıldız sayısına göre kalite
                            }
                            
                            results.append(result_dict)
                            logger.info(f"✅ GitHub result: {title[:50]}...")
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing GitHub result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} GitHub results")
                    return results
                else:
                    logger.warning(f"⚠️ GitHub search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ GitHub search error: {e}")
            return []
    
    async def _search_duckduckgo(self, query: str, max_results: int = 2) -> List[Dict]:
        """DuckDuckGo'da arama yap - Güvenilir alternatif"""
        try:
            if not self.session:
                return []
            
            search_url = self.search_urls['duckduckgo'].format(quote_plus(query))
            logger.info(f"🔍 Searching DuckDuckGo: {search_url}")
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    
                    # DuckDuckGo HTML yapısını dene
                    search_results = (
                        soup.find_all('div', class_='result') or
                        soup.find_all('div', class_='web-result') or
                        soup.find_all('div', {'data-testid': 'result'}) or
                        soup.find_all('article')
                    )[:max_results]
                    
                    if not search_results:
                        logger.warning("⚠️ No DuckDuckGo search results found in HTML")
                        return []
                    
                    for result in search_results:
                        try:
                            # Başlık ve link
                            title_elem = (
                                result.find('h2').find('a') if result.find('h2') else None or
                                result.find('h3').find('a') if result.find('h3') else None or
                                result.find('a', class_='result__a') or
                                result.find('a')
                            )
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            href = title_elem.get('href', '')
                            
                            if not href or href.startswith('/'):
                                continue
                            
                            # Açıklama
                            desc_elem = (
                                result.find('div', class_='result__snippet') or
                                result.find('span', class_='result__snippet') or
                                result.find('p') or
                                result.find('div', class_='snippet')
                            )
                            description = desc_elem.get_text(strip=True) if desc_elem else title
                            
                            # İçerik oluştur
                            content = f"{title}\n\n{description}"
                            
                            result_dict = {
                                'title': title,
                                'content': content,
                                'url': href,
                                'source': 'DuckDuckGo',
                                'quality_score': 7.0  # DuckDuckGo için sabit kalite skoru
                            }
                            
                            results.append(result_dict)
                            logger.info(f"✅ DuckDuckGo result: {title[:50]}...")
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing DuckDuckGo result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} DuckDuckGo results")
                    return results
                else:
                    logger.warning(f"⚠️ DuckDuckGo search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ DuckDuckGo search error: {e}")
            return []

    def _calculate_stackoverflow_quality(self, score: int, answer_count: int, content_length: int) -> float:
        """Stack Overflow kalite skorunu hesapla"""
        quality = 5.0  # Başlangıç
        
        # Skor bonusu
        quality += min(score * 0.1, 2.0)
        
        # Cevap sayısı bonusu
        quality += min(answer_count * 0.3, 1.5)
        
        # İçerik uzunluğu bonusu
        if content_length > 200:
            quality += 0.5
        if content_length > 500:
            quality += 0.5
        
        return min(quality, 10.0)
    
    def format_search_results(self, results: List[Dict], query: str) -> str:
        """Arama sonuçlarını formatla"""
        try:
            if not results:
                return f"🔍 '{query}' için güncel bilgi bulunamadı."
            
            formatted_response = f"🔍 **'{query}' için güncel web araması sonuçları:**\n\n"
            
            for i, result in enumerate(results, 1):
                source = result.get('source', 'Web')
                title = result.get('title', 'Başlıksız')
                content = result.get('content', '')[:1000]  # İlk 1000 karakter
                url = result.get('url', '')
                quality = result.get('quality_score', 0)
                
                formatted_response += f"**{i}. {title}**\n"
                formatted_response += f"📍 **Kaynak:** {source} (Kalite: {quality:.1f}/10)\n"
                
                if content:
                    formatted_response += f"📝 **İçerik:**\n{content}\n"
                
                if url:
                    formatted_response += f"🔗 **Link:** {url}\n"
                
                formatted_response += "\n---\n\n"
            
            formatted_response += f"⏰ **Arama Zamanı:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            formatted_response += "💡 **Not:** Bu bilgiler gerçek zamanlı web araması ile elde edilmiştir."
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"❌ Result formatting error: {e}")
            return f"Arama sonuçları formatlanırken hata oluştu: {str(e)}"
    
    def _calculate_advanced_quality_score(self, result: Dict) -> float:
        """Gelişmiş kalite skorlama sistemi"""
        try:
            base_score = 5.0
            source = result.get('source', '').lower()
            content = result.get('content', '')
            title = result.get('title', '')
            url = result.get('url', '')
            
            # Kaynak güvenilirliği bonusu
            source_scores = {
                'stack overflow': 3.0,
                'github': 2.5,
                'mdn': 2.8,
                'google scholar': 3.5,
                'geeksforgeeks': 2.2,
                'w3schools': 2.0,
                'bing': 1.8
            }
            base_score += source_scores.get(source, 1.0)
            
            # İçerik kalitesi analizi
            if content:
                content_length = len(content)
                
                # İçerik uzunluğu bonusu
                if content_length > 1000:
                    base_score += 2.0
                elif content_length > 500:
                    base_score += 1.5
                elif content_length > 200:
                    base_score += 1.0
                elif content_length > 100:
                    base_score += 0.5
                
                # Kod bloğu varlığı
                if '```' in content or '<code>' in content or 'public class' in content:
                    base_score += 1.5
                
                # Programlama anahtar kelimeleri
                programming_keywords = ['function', 'class', 'method', 'variable', 'array', 'object', 'import', 'return']
                keyword_count = sum(1 for keyword in programming_keywords if keyword in content.lower())
                base_score += min(keyword_count * 0.2, 1.0)
            
            # Başlık kalitesi
            if title:
                if any(word in title.lower() for word in ['how to', 'tutorial', 'example', 'guide']):
                    base_score += 1.0
                if any(word in title.lower() for word in ['android', 'java', 'python', 'javascript']):
                    base_score += 0.5
            
            # URL kalitesi
            if url:
                if any(domain in url for domain in self.trusted_domains):
                    base_score += 1.0
                if '/questions/' in url or '/tutorial/' in url or '/docs/' in url:
                    base_score += 0.5
            
            # Stack Overflow özel skorlama
            if source == 'stack overflow':
                score = result.get('score', 0)
                answer_count = result.get('answer_count', 0)
                
                if score > 20:
                    base_score += 2.0
                elif score > 10:
                    base_score += 1.5
                elif score > 5:
                    base_score += 1.0
                elif score > 0:
                    base_score += 0.5
                
                if answer_count > 5:
                    base_score += 1.5
                elif answer_count > 2:
                    base_score += 1.0
                elif answer_count > 0:
                    base_score += 0.5
            
            # GitHub özel skorlama
            elif source == 'github':
                stars = result.get('stars', 0)
                if stars > 1000:
                    base_score += 2.0
                elif stars > 100:
                    base_score += 1.5
                elif stars > 10:
                    base_score += 1.0
                elif stars > 0:
                    base_score += 0.5
            
            return min(base_score, 10.0)  # Max 10 puan
            
        except Exception as e:
            logger.warning(f"⚠️ Quality score calculation error: {e}")
            return 5.0  # Default score
    
    async def _search_bing(self, query: str, max_results: int = 2) -> List[Dict]:
        """Bing ile web araması yap"""
        try:
            if not self.session:
                return []
            
            # Bing search URL
            search_url = f"https://www.bing.com/search?q={quote_plus(query + ' programming tutorial')}"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    search_results = soup.find_all('li', class_='b_algo')[:max_results]
                    
                    for result in search_results:
                        try:
                            # Başlık ve link
                            title_elem = result.find('h2')
                            if not title_elem:
                                continue
                            
                            link_elem = title_elem.find('a')
                            if not link_elem:
                                continue
                            
                            title = link_elem.get_text(strip=True)
                            url = link_elem.get('href', '')
                            
                            # Özet
                            desc_elem = result.find('p')
                            description = desc_elem.get_text(strip=True) if desc_elem else ''
                            
                            # Güvenilir kaynak kontrolü
                            is_trusted = any(domain in url for domain in self.trusted_domains)
                            base_score = 7.0 if is_trusted else 5.5
                            
                            result_dict = {
                                'title': title,
                                'content': description or title,
                                'url': url,
                                'source': 'Bing',
                                'quality_score': base_score
                            }
                            
                            results.append(result_dict)
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing Bing result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} Bing results")
                    return results
                else:
                    logger.warning(f"⚠️ Bing search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ Bing search error: {e}")
            return []
    
    async def _search_google_scholar(self, query: str, max_results: int = 1) -> List[Dict]:
        """Google Scholar'da akademik kaynak ara"""
        try:
            if not self.session:
                return []
            
            # Google Scholar search URL
            search_url = f"https://scholar.google.com/scholar?q={quote_plus(query + ' programming')}"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    articles = soup.find_all('div', class_='gs_r')[:max_results]
                    
                    for article in articles:
                        try:
                            title_elem = article.find('h3', class_='gs_rt')
                            if not title_elem:
                                continue
                            
                            link_elem = title_elem.find('a')
                            if link_elem:
                                title = link_elem.get_text(strip=True)
                                url = link_elem.get('href', '')
                            else:
                                title = title_elem.get_text(strip=True)
                                url = ''
                            
                            # Özet
                            desc_elem = article.find('div', class_='gs_rs')
                            description = desc_elem.get_text(strip=True) if desc_elem else ''
                            
                            result = {
                                'title': title,
                                'content': description or title,
                                'url': url,
                                'source': 'Google Scholar',
                                'quality_score': 8.5  # Akademik kaynak olduğu için yüksek skor
                            }
                            
                            results.append(result)
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing Google Scholar result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} Google Scholar results")
                    return results
                else:
                    logger.warning(f"⚠️ Google Scholar search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ Google Scholar search error: {e}")
            return []
    
    async def _search_alternative_sources(self, query: str, max_results: int = 2) -> List[Dict]:
        """Alternatif kaynaklarda arama yap"""
        try:
            if not self.session:
                return []
            
            results = []
            
            # CodeProject arama
            try:
                codeproject_url = f"https://www.codeproject.com/search.aspx?q={quote_plus(query)}"
                async with self.session.get(codeproject_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        articles = soup.find_all('div', class_='result-item')[:1]
                        for article in articles:
                            title_elem = article.find('h3')
                            if title_elem and title_elem.find('a'):
                                title = title_elem.find('a').get_text(strip=True)
                                url = title_elem.find('a').get('href', '')
                                if not url.startswith('http'):
                                    url = f"https://www.codeproject.com{url}"
                                
                                desc_elem = article.find('p')
                                description = desc_elem.get_text(strip=True) if desc_elem else ''
                                
                                results.append({
                                    'title': title,
                                    'content': description or title,
                                    'url': url,
                                    'source': 'CodeProject',
                                    'quality_score': 7.5
                                })
            except Exception as e:
                logger.warning(f"⚠️ CodeProject search failed: {e}")
            
            # Tutorialspoint arama
            try:
                tutorialspoint_url = f"https://www.tutorialspoint.com/search/search.php?query={quote_plus(query)}"
                async with self.session.get(tutorialspoint_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        search_results = soup.find_all('div', class_='result')[:1]
                        for result in search_results:
                            title_elem = result.find('h3')
                            if title_elem and title_elem.find('a'):
                                title = title_elem.find('a').get_text(strip=True)
                                url = title_elem.find('a').get('href', '')
                                if not url.startswith('http'):
                                    url = f"https://www.tutorialspoint.com{url}"
                                
                                desc_elem = result.find('p')
                                description = desc_elem.get_text(strip=True) if desc_elem else ''
                                
                                results.append({
                                    'title': title,
                                    'content': description or title,
                                    'url': url,
                                    'source': 'TutorialsPoint',
                                    'quality_score': 7.0
                                })
            except Exception as e:
                logger.warning(f"⚠️ TutorialsPoint search failed: {e}")
            
            logger.info(f"✅ Found {len(results)} alternative source results")
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"❌ Alternative sources search error: {e}")
            return []
    
    async def _search_geeksforgeeks_real(self, query: str, max_results: int = 2) -> List[Dict]:
        """GeeksforGeeks'te gerçek arama yap"""
        try:
            if not self.session:
                return []
            
            search_url = f"https://www.geeksforgeeks.org/search/{quote_plus(query)}/"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    articles = soup.find_all('div', class_='head')[:max_results]
                    
                    for article in articles:
                        try:
                            link_elem = article.find('a')
                            if not link_elem:
                                continue
                            
                            title = link_elem.get_text(strip=True)
                            relative_url = link_elem.get('href', '')
                            full_url = urljoin('https://www.geeksforgeeks.org', relative_url)
                            
                            # İçerik al
                            content = await self._get_geeksforgeeks_content(full_url)
                            
                            result = {
                                'title': title,
                                'content': content or title,
                                'url': full_url,
                                'source': 'GeeksforGeeks',
                                'quality_score': 7.0
                            }
                            
                            results.append(result)
                            
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
        """GeeksforGeeks makalesinin içeriğini al"""
        try:
            if not self.session:
                return None
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Makale içeriği
                    content_div = soup.find('div', class_='text')
                    if content_div:
                        # Code blokları için özel işlem
                        code_blocks = content_div.find_all(['pre', 'code'])
                        for block in code_blocks:
                            block.string = f"\n```\n{block.get_text()}\n```\n"
                        
                        content = content_div.get_text(strip=True)
                        return content[:1200]  # İlk 1200 karakter
                    
                    return None
                else:
                    return None
                    
        except Exception as e:
            logger.warning(f"⚠️ Error fetching GeeksforGeeks content: {e}")
            return None
    
    async def _search_w3schools_real(self, query: str, max_results: int = 2) -> List[Dict]:
        """W3Schools'da gerçek arama yap"""
        try:
            if not self.session:
                return []
            
            search_url = f"https://www.w3schools.com/search/search_asp.asp?search={quote_plus(query)}"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    search_results = soup.find_all('div', class_='w3-container')[:max_results]
                    
                    for result_div in search_results:
                        try:
                            link_elem = result_div.find('a')
                            if not link_elem:
                                continue
                            
                            title = link_elem.get_text(strip=True)
                            relative_url = link_elem.get('href', '')
                            full_url = urljoin('https://www.w3schools.com', relative_url)
                            
                            # Özet al
                            desc_elem = result_div.find('p')
                            description = desc_elem.get_text(strip=True) if desc_elem else ''
                            
                            result = {
                                'title': title,
                                'content': description or title,
                                'url': full_url,
                                'source': 'W3Schools',
                                'quality_score': 6.5
                            }
                            
                            results.append(result)
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing W3Schools result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} W3Schools results")
                    return results
                else:
                    logger.warning(f"⚠️ W3Schools search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ W3Schools search error: {e}")
            return []
    
    async def _search_mdn_real(self, query: str, max_results: int = 1) -> List[Dict]:
        """MDN'de gerçek arama yap"""
        try:
            if not self.session:
                return []
            
            search_url = f"https://developer.mozilla.org/en-US/search?q={quote_plus(query)}"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    search_results = soup.find_all('article', class_='result-item')[:max_results]
                    
                    for article in search_results:
                        try:
                            title_elem = article.find('h2')
                            if not title_elem:
                                continue
                            
                            link_elem = title_elem.find('a')
                            if not link_elem:
                                continue
                            
                            title = link_elem.get_text(strip=True)
                            relative_url = link_elem.get('href', '')
                            full_url = urljoin('https://developer.mozilla.org', relative_url)
                            
                            # Özet al
                            summary_elem = article.find('p')
                            summary = summary_elem.get_text(strip=True) if summary_elem else ''
                            
                            result = {
                                'title': title,
                                'content': summary or title,
                                'url': full_url,
                                'source': 'MDN',
                                'quality_score': 8.0
                            }
                            
                            results.append(result)
                            
                        except Exception as e:
                            logger.warning(f"⚠️ Error parsing MDN result: {e}")
                            continue
                    
                    logger.info(f"✅ Found {len(results)} MDN results")
                    return results
                else:
                    logger.warning(f"⚠️ MDN search failed: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"❌ MDN search error: {e}")
            return []


# Test fonksiyonu
async def test_enhanced_search():
    """Test enhanced web search functionality"""
    test_queries = [
        "Android için java programlama dili ile bir kart oluştur",
        "Python Flask blog uygulaması nasıl yapılır",
        "React hooks useState örneği"
    ]
    
    async with EnhancedWebSearchSystem() as search_system:
        for query in test_queries:
            print(f"\n🔍 Testing enhanced search: {query}")
            results = await search_system.search_programming_question(query)
            
            if results:
                formatted = search_system.format_search_results(results, query)
                print(formatted[:800] + "..." if len(formatted) > 800 else formatted)
            else:
                print("❌ No results found")


if __name__ == "__main__":
    asyncio.run(test_enhanced_search())