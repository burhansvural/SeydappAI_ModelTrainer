# src/research/real_web_search.py
"""
🌐 Real Web Search System - Gerçek İnternet Araması
Bu sistem DuckDuckGo kullanarak gerçek web araması yapar
"""

import logging
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    logger.warning("⚠️ DuckDuckGo search not available. Install with: pip install ddgs")


class RealWebSearchSystem:
    """
    🌐 Gerçek Web Araması Sistemi
    
    Özellikler:
    - DuckDuckGo ile gerçek web araması
    - Programlama sorularına özel optimizasyon
    - Güvenilir kaynaklardan sonuç filtreleme
    - Kalite skorlaması
    """
    
    def __init__(self):
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
            'geeksforgeeks.org',
            'medium.com',
            'dev.to',
            'tutorialspoint.com'
        ]
        
        logger.info("🌐 Real Web Search System initialized")
    
    async def search_programming_question(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Programlama sorusu için gerçek web araması yap
        
        Args:
            query: Arama sorgusu
            max_results: Maksimum sonuç sayısı
            
        Returns:
            List[Dict]: Arama sonuçları
        """
        try:
            if not DDGS_AVAILABLE:
                logger.error("❌ DuckDuckGo search not available")
                return []
            
            logger.info(f"🔍 Real web search for: {query}")
            
            # Android kart oluşturma sorusu için özel arama
            if self._is_android_card_question(query):
                return await self._search_android_card_creation(query, max_results)
            
            # Genel programlama araması
            return await self._search_general_programming(query, max_results)
            
        except Exception as e:
            logger.error(f"❌ Real web search error: {e}")
            return []
    
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
                "Android CardView Java profile card example",
                "Android custom card layout with image Java",
                "Android RecyclerView card design tutorial"
            ]
            
            all_results = []
            
            for search_term in search_terms:
                results = await self._perform_ddg_search(search_term, 2)
                all_results.extend(results)
            
            # Sonuçları kalite skoruna göre sırala
            all_results.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
            
            # En iyi sonuçları seç
            best_results = all_results[:max_results]
            
            return best_results
            
        except Exception as e:
            logger.error(f"❌ Android card search error: {e}")
            return []
    
    async def _search_general_programming(self, query: str, max_results: int = 5) -> List[Dict]:
        """Genel programlama araması"""
        try:
            # Programlama odaklı arama terimi oluştur
            enhanced_query = self._enhance_programming_query(query)
            
            results = await self._perform_ddg_search(enhanced_query, max_results * 2)
            
            # Güvenilir kaynaklardan sonuçları filtrele
            filtered_results = self._filter_trusted_sources(results)
            
            # Sonuçları kalite skoruna göre sırala
            filtered_results.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
            
            return filtered_results[:max_results]
            
        except Exception as e:
            logger.error(f"❌ General programming search error: {e}")
            return []
    
    async def _perform_ddg_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """DuckDuckGo ile arama yap"""
        try:
            results = []
            
            # DuckDuckGo araması yap
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=max_results))
                
                for result in search_results:
                    try:
                        title = result.get('title', '')
                        body = result.get('body', '')
                        url = result.get('href', '')
                        
                        if not title or not url:
                            continue
                        
                        # Kalite skorunu hesapla
                        quality_score = self._calculate_quality_score(title, body, url)
                        
                        result_dict = {
                            'title': title,
                            'content': body,
                            'url': url,
                            'source': self._extract_domain(url),
                            'quality_score': quality_score
                        }
                        
                        results.append(result_dict)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Error processing search result: {e}")
                        continue
            
            logger.info(f"✅ Found {len(results)} DuckDuckGo results")
            return results
            
        except Exception as e:
            logger.error(f"❌ DuckDuckGo search error: {e}")
            return []
    
    def _enhance_programming_query(self, query: str) -> str:
        """Programlama araması için sorguyu geliştir"""
        # Türkçe sorguları İngilizce'ye çevir
        turkish_to_english = {
            'android için java programlama dili ile bir kart oluştur': 'Android Java CardView profile card example tutorial',
            'android': 'Android',
            'java': 'Java',
            'kart': 'card',
            'profil': 'profile',
            'oluştur': 'create',
            'programlama': 'programming',
            'dili': 'language'
        }
        
        query_lower = query.lower()
        
        # Tam eşleşme kontrolü
        if query_lower in turkish_to_english:
            return turkish_to_english[query_lower]
        
        # Kısmi çeviri
        enhanced_query = query
        for turkish, english in turkish_to_english.items():
            if turkish in query_lower:
                enhanced_query = enhanced_query.replace(turkish, english)
        
        # Programlama anahtar kelimeleri ekle
        programming_terms = ['tutorial', 'example', 'code', 'how to']
        
        # Eğer sorgu zaten programlama terimleri içeriyorsa, olduğu gibi bırak
        if any(term in enhanced_query.lower() for term in programming_terms):
            return enhanced_query
        
        # Aksi halde 'example' ekle
        return f"{enhanced_query} example"
    
    def _filter_trusted_sources(self, results: List[Dict]) -> List[Dict]:
        """Güvenilir kaynaklardan sonuçları filtrele"""
        filtered = []
        
        for result in results:
            url = result.get('url', '')
            domain = self._extract_domain(url)
            
            # Güvenilir domain'lerden olanları öncelikle al
            if any(trusted in domain for trusted in self.trusted_domains):
                result['quality_score'] = result.get('quality_score', 0) + 2.0  # Bonus puan
                filtered.append(result)
            elif len(filtered) < 3:  # En az 3 sonuç olsun
                filtered.append(result)
        
        return filtered
    
    def _extract_domain(self, url: str) -> str:
        """URL'den domain adını çıkar"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except:
            return url
    
    def _calculate_quality_score(self, title: str, content: str, url: str) -> float:
        """Sonuç kalitesini hesapla (0-10 arası)"""
        try:
            score = 0.0
            
            # Başlık kalitesi
            if title:
                title_lower = title.lower()
                # Programlama anahtar kelimeleri
                prog_keywords = ['java', 'android', 'python', 'javascript', 'tutorial', 'example', 'how to']
                keyword_count = sum(1 for keyword in prog_keywords if keyword in title_lower)
                score += min(keyword_count * 0.5, 2.0)
                
                # Başlık uzunluğu
                if 20 <= len(title) <= 100:
                    score += 1.0
            
            # İçerik kalitesi
            if content:
                content_length = len(content)
                if content_length > 100:
                    score += 1.0
                if content_length > 300:
                    score += 1.0
                
                # Kod blokları veya teknik terimler
                content_lower = content.lower()
                if any(term in content_lower for term in ['code', 'function', 'class', 'method']):
                    score += 1.0
            
            # URL kalitesi
            domain = self._extract_domain(url)
            if any(trusted in domain for trusted in self.trusted_domains):
                score += 2.0
            
            return min(score, 10.0)
            
        except Exception as e:
            logger.error(f"❌ Quality score calculation error: {e}")
            return 5.0
    
    def format_search_results(self, results: List[Dict], query: str) -> str:
        """Arama sonuçlarını formatla"""
        try:
            if not results:
                return f"🔍 '{query}' için güncel bilgi bulunamadı."
            
            formatted_response = f"🔍 **'{query}' için gerçek zamanlı web araması sonuçları:**\n\n"
            
            for i, result in enumerate(results, 1):
                source = result.get('source', 'Web')
                title = result.get('title', 'Başlıksız')
                content = result.get('content', '')[:800]  # İlk 800 karakter
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
            formatted_response += "💡 **Not:** Bu bilgiler DuckDuckGo ile gerçek zamanlı web araması ile elde edilmiştir."
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"❌ Result formatting error: {e}")
            return f"Arama sonuçları formatlanırken hata oluştu: {str(e)}"


# Test fonksiyonu
async def test_real_search():
    """Test real web search functionality"""
    test_queries = [
        "Android için java programlama dili ile bir kart oluştur",
        "Python Flask blog uygulaması nasıl yapılır",
        "React hooks useState örneği"
    ]
    
    search_system = RealWebSearchSystem()
    
    for query in test_queries:
        print(f"\n🔍 Testing real search: {query}")
        results = await search_system.search_programming_question(query)
        
        if results:
            formatted = search_system.format_search_results(results, query)
            print(formatted[:800] + "..." if len(formatted) > 800 else formatted)
        else:
            print("❌ No results found")


if __name__ == "__main__":
    asyncio.run(test_real_search())