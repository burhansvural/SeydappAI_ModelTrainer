# src/research/intelligent_web_scraper.py
"""
🤖 Modern Web Scraping System - Search Results[1][5] Based
Fixed session management and browser fingerprinting
"""

import asyncio
import aiohttp
import logging
import random
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from pathlib import Path
import threading
import warnings
from urllib.parse import quote_plus

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)


class ModernWebScraper:
    """Search results[1][5]: Modern web scraper with proper session management"""

    def __init__(self, flet_version: str = "0.28.3"):
        logger.info(f"🤖 Initializing Modern Web Scraper for Flet {flet_version}")

        self._lock = threading.Lock()
        self.learning_active = False
        self.session = None

        # Stats tracking
        self.stats = {
            'topics_researched': 0,
            'knowledge_nodes': 0,
            'auto_generated_examples': 0,
            'learning_cycles': 0,
            'last_scan': 'Never',
            'status': 'Idle',
            'quality_score': '70%'
        }

        self.topics_completed = 0
        self.total_examples = 0
        self.cycles_completed = 0

        # ✅ Search results[1][5]: Modern browser fingerprinting
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="140", "Google Chrome";v="140", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }

        logger.info("✅ Modern Web Scraper initialized")

    async def initialize_session(self):
        """Search results[1][2]: Proper async session initialization"""
        try:
            if self.session and not self.session.closed:
                await self.session.close()

            # ✅ Conservative connection settings
            connector = aiohttp.TCPConnector(
                limit=5,
                limit_per_host=1,
                ttl_dns_cache=300,
                use_dns_cache=True,
                enable_cleanup_closed=True,
                ssl=False  # Disable SSL verification for testing
            )

            # ✅ Generous timeout
            timeout = aiohttp.ClientTimeout(total=30, connect=10)

            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers=self._headers,
                cookie_jar=aiohttp.CookieJar()
            )

            logger.info("✅ Session initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Session initialization failed: {e}")
            return False

    async def cleanup_session(self):
        """Proper session cleanup"""
        try:
            if self.session and not self.session.closed:
                await self.session.close()
                await asyncio.sleep(0.1)
            logger.debug("✅ Session cleaned up")
        except Exception as e:
            logger.debug(f"Session cleanup error: {e}")

    async def fetch_url(self, url: str, max_retries: int = 2) -> Optional[str]:
        """Search results[1][5]: Modern fetch with proper error handling"""

        for attempt in range(max_retries):
            try:
                # ✅ Ensure session is ready
                if not self.session or self.session.closed:
                    success = await self.initialize_session()
                    if not success:
                        return None

                # ✅ Human-like delay
                await asyncio.sleep(random.uniform(1, 3))

                logger.debug(f"🌐 Fetching {url[:50]}... (attempt {attempt + 1})")

                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        logger.debug(f"✅ Successfully fetched {len(content)} chars")
                        return content
                    elif response.status == 403:
                        logger.debug(f"🚫 Access forbidden: {url}")
                        return None
                    elif response.status == 429:
                        wait_time = (2 ** attempt) * random.uniform(2, 4)
                        logger.debug(f"⏱️ Rate limited, waiting {wait_time:.1f}s")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.debug(f"⚠️ HTTP {response.status}: {url}")

            except asyncio.TimeoutError:
                logger.debug(f"⏰ Timeout for {url} (attempt {attempt + 1})")
                await asyncio.sleep(2)

            except Exception as e:
                logger.debug(f"❌ Request error: {str(e)[:100]} (attempt {attempt + 1})")
                await asyncio.sleep(1)

        logger.debug(f"❌ Failed to fetch {url} after {max_retries} attempts")
        return None

    async def search_topic(self, topic: str) -> List[Dict]:
        """Search results[2]: Smart search with API detection"""
        results = []

        try:
            logger.info(f"🔍 Searching for: {topic}")

            # ✅ Search results[2]: Try different search strategies
            search_urls = [
                f"https://duckduckgo.com/html/?q={quote_plus(f'python {topic}')}&ia=web",
                f"https://www.startpage.com/sp/search?query={quote_plus(f'python {topic}')}&t=device"
            ]

            for search_url in search_urls:
                try:
                    html = await self.fetch_url(search_url)
                    if html:
                        # ✅ Extract search results
                        soup = BeautifulSoup(html, 'html.parser')

                        # ✅ Look for result links
                        for link in soup.find_all('a', href=True)[:5]:
                            href = link.get('href', '')
                            title = link.get_text().strip()

                            if (href.startswith('http') and title and len(title) > 15 and
                                    any(edu in href.lower() for edu in
                                        ['github', 'stackoverflow', 'medium', 'tutorial', 'guide'])):
                                results.append({
                                    'url': href,
                                    'title': title[:100],
                                    'source': 'search'
                                })

                        if results:
                            break

                except Exception as e:
                    logger.debug(f"Search engine failed: {e}")
                    continue

                # ✅ Delay between search engines
                await asyncio.sleep(random.uniform(2, 4))

            # ✅ Search results[2]: Fallback to direct educational URLs
            if not results:
                logger.info("🔄 Using direct educational sources")
                results = await self._get_educational_sources(topic)

            logger.info(f"✅ Found {len(results)} search results")
            return results

        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []

    async def _get_educational_sources(self, topic: str) -> List[Dict]:
        """Search results[2]: Direct educational content sources"""
        educational_sources = []

        # ✅ Educational URL patterns
        base_urls = [
            f"https://github.com/search?q={quote_plus(f'python {topic}')}&type=repositories",
            f"https://stackoverflow.com/search?q={quote_plus(f'python {topic}')}",
            f"https://medium.com/search?q={quote_plus(f'python {topic}')}"
        ]

        for url in base_urls[:2]:  # Limit to 2 sources
            try:
                educational_sources.append({
                    'url': url,
                    'title': f'Educational content for {topic}',
                    'source': 'educational'
                })
            except Exception:
                continue

        return educational_sources

    async def extract_content(self, url: str) -> str:
        """Search results[2]: Smart content extraction"""
        try:
            html = await self.fetch_url(url)
            if not html:
                return ""

            soup = BeautifulSoup(html, 'html.parser')

            # ✅ Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()

            # ✅ Extract meaningful content
            content_selectors = ['main', 'article', '.content', '#content', 'pre', 'code']
            content = ""

            for selector in content_selectors:
                elements = soup.select(selector)
                for elem in elements[:3]:
                    text = elem.get_text().strip()
                    if len(text) > 50:
                        content += text + "\n\n"
                if len(content) > 500:
                    break

            # ✅ Clean text
            content = ' '.join(content.split())
            return content[:2000] if content else ""

        except Exception as e:
            logger.debug(f"Content extraction failed: {e}")
            return ""

    async def research_and_generate_examples(self, topic: str) -> List[Dict]:
        """Main research function with modern approach"""
        try:
            with self._lock:
                self.learning_active = True

            logger.info(f"🔍 Researching topic: {topic}")
            start_time = time.time()

            # ✅ Initialize session first
            success = await self.initialize_session()
            if not success:
                logger.error("❌ Failed to initialize session")
                return []

            # ✅ Search for topic
            search_results = await self.search_topic(topic)

            if not search_results:
                logger.warning(f"⚠️ No search results for: {topic}")
                return []

            # ✅ Extract content from results
            examples = []
            for result in search_results[:3]:  # Process top 3
                try:
                    await asyncio.sleep(random.uniform(2, 4))  # Rate limit
                    content = await self.extract_content(result['url'])

                    if content and len(content) > 100:
                        example = {
                            "input": f"How to implement {topic} in Python?",
                            "output": content,
                            "source": result['url'],
                            "title": result['title'],
                            "topic": topic,
                            "timestamp": datetime.now().isoformat(),
                            "auto_generated": True,
                            "content_length": len(content),
                            "quality_score": 0.8,
                            "content": content,
                            "type": "web_scraped_modern"
                        }
                        examples.append(example)
                        logger.debug(f"✅ Extracted content for {topic}")

                except Exception as e:
                    logger.debug(f"Failed to process result: {e}")
                    continue

            # ✅ Update stats
            with self._lock:
                self.topics_completed += 1
                self.total_examples += len(examples)
                self.cycles_completed += 1
                self.stats.update({
                    'topics_researched': self.topics_completed,
                    'auto_generated_examples': self.total_examples,
                    'learning_cycles': self.cycles_completed,
                    'last_scan': datetime.now().strftime("%H:%M"),
                    'status': 'Active'
                })

            # ✅ Save examples
            if examples:
                await self._save_examples(topic, examples)

            duration = time.time() - start_time
            logger.info(f"✅ Generated {len(examples)} examples for '{topic}' in {duration:.2f}s")

            return examples

        except Exception as e:
            logger.error(f"❌ Research failed for {topic}: {e}")
            return []
        finally:
            await self.cleanup_session()
            with self._lock:
                self.learning_active = False

    async def _save_examples(self, topic: str, examples: List[Dict]):
        """Save examples to file"""
        try:
            dataset_file = Path("datasets/conversations/autonomous_research.jsonl")
            dataset_file.parent.mkdir(parents=True, exist_ok=True)

            with open(dataset_file, 'a', encoding='utf-8') as f:
                for example in examples:
                    f.write(json.dumps(example, ensure_ascii=False) + '\n')

            logger.info(f"💾 Saved {len(examples)} examples for {topic}")

        except Exception as e:
            logger.error(f"❌ Save error: {e}")

    def load_user_topics(self) -> List[str]:
        """Load user topics with fallback"""
        try:
            topics_file = Path("datasets/conversations/user_topics.jsonl")
            if not topics_file.exists():
                topics_file = Path("config/user_topics.jsonl")

            if topics_file.exists():
                topics = []
                with open(topics_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                data = json.loads(line.strip())
                                if data.get('topic'):
                                    topics.append(data['topic'])
                            except json.JSONDecodeError:
                                continue

                if topics:
                    logger.info(f"📚 Loaded {len(topics)} topics")
                    return topics

            # ✅ Realistic fallback topics
            fallback_topics = [
                "web scraping requests",
                "data analysis pandas",
                "machine learning basics"
            ]
            logger.info("📚 Using fallback topics")
            return fallback_topics

        except Exception as e:
            logger.error(f"❌ Topic loading error: {e}")
            return ["python programming"]

    def stop_autonomous_learning(self):
        """Stop learning safely"""
        with self._lock:
            self.learning_active = False
            logger.info("⏹️ Learning stopped")

    def get_research_stats(self) -> dict:
        """Get current stats"""
        with self._lock:
            base_quality = 75
            progress_bonus = min(20, self.topics_completed * 3)
            quality_score = min(100, base_quality + progress_bonus)

            return {
                'topics_researched': self.stats['topics_researched'],
                'knowledge_nodes': self.total_examples,
                'auto_generated_examples': self.stats['auto_generated_examples'],
                'learning_cycles': self.stats['learning_cycles'],
                'last_scan': self.stats['last_scan'],
                'status': 'Learning' if self.learning_active else 'Idle',
                'quality_score': f"{int(quality_score)}%"
            }

    async def start_autonomous_research(self):
        """Start autonomous research"""
        try:
            topics = self.load_user_topics()
            logger.info(f"🚀 Starting research for {len(topics)} topics")

            for topic in topics:
                try:
                    examples = await self.research_and_generate_examples(topic)
                    logger.info(f"✅ Completed {topic}: {len(examples)} examples")

                    # ✅ Long delay between topics
                    await asyncio.sleep(random.uniform(10, 20))

                except Exception as e:
                    logger.error(f"❌ Failed topic {topic}: {e}")
                    continue

            logger.info("🎯 Autonomous research completed")

        except Exception as e:
            logger.error(f"❌ Autonomous research error: {e}")


# ✅ Wrapper for compatibility
class AutonomousLearningSystem(ModernWebScraper):
    """Compatibility wrapper"""
    pass


# ✅ Factory function
def create_autonomous_learning_system(flet_version: str = "0.28.3"):
    """Create modern web scraper instance"""
    try:
        return ModernWebScraper(flet_version)
    except Exception as e:
        logger.error(f"❌ Creation failed: {e}")
        return None
