# src/knowledge/self_learning_system.py
"""
🧠 Self-Learning System - AI Chat için Otomatik Öğrenme Sistemi
Bu sistem AI Chat'in verdiği cevapları analiz eder ve yeni bilgileri öğrenir
"""

import logging
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

logger = logging.getLogger(__name__)

class SelfLearningSystem:
    """
    🧠 Self-Learning System - AI Chat'in kendini geliştirmesi için
    
    Özellikler:
    - Yeni soruları ve cevapları analiz eder
    - Bilgi kalitesini değerlendirir
    - Öğrenilen bilgileri kategorize eder
    - Gelecekteki sorular için hızlı erişim sağlar
    """
    
    def __init__(self):
        self.learning_data_file = Path("storage/data/learned_knowledge.json")
        self.learning_data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Öğrenilen bilgileri yükle
        self.learned_knowledge = self.load_learned_knowledge()
        
        # Öğrenme istatistikleri
        self.learning_stats = {
            'total_learned': len(self.learned_knowledge),
            'categories': {},
            'last_update': datetime.now().isoformat()
        }
        
        logger.info(f"🧠 Self-Learning System initialized - {len(self.learned_knowledge)} knowledge entries loaded")
    
    def load_learned_knowledge(self) -> Dict:
        """Öğrenilen bilgileri dosyadan yükle"""
        try:
            if self.learning_data_file.exists():
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"📚 Loaded {len(data)} learned knowledge entries")
                    return data
            else:
                logger.info("📚 Creating new learned knowledge database")
                return {}
        except Exception as e:
            logger.warning(f"⚠️ Learned knowledge load error: {e}")
            return {}
    
    def save_learned_knowledge(self):
        """Öğrenilen bilgileri dosyaya kaydet"""
        try:
            # İstatistikleri güncelle
            self.learning_stats['total_learned'] = len(self.learned_knowledge)
            self.learning_stats['last_update'] = datetime.now().isoformat()
            
            # Kategorileri say
            categories = {}
            for entry in self.learned_knowledge.values():
                category = entry.get('category', 'unknown')
                categories[category] = categories.get(category, 0) + 1
            self.learning_stats['categories'] = categories
            
            # Dosyaya kaydet
            save_data = {
                'knowledge': self.learned_knowledge,
                'stats': self.learning_stats
            }
            
            with open(self.learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Learned knowledge saved: {len(self.learned_knowledge)} entries")
            
        except Exception as e:
            logger.error(f"❌ Learned knowledge save error: {e}")
    
    def analyze_and_learn(self, user_query: str, ai_response: str, web_content: str = "") -> bool:
        """
        Yeni soru-cevap çiftini analiz et ve öğren
        
        Args:
            user_query: Kullanıcının sorusu
            ai_response: AI'ın verdiği cevap
            web_content: Web'den alınan ek bilgi
            
        Returns:
            bool: Öğrenme başarılı mı
        """
        try:
            # Soru hash'i oluştur (benzersiz kimlik için)
            query_hash = hashlib.md5(user_query.lower().encode()).hexdigest()
            
            # Eğer bu soru daha önce öğrenildiyse, güncelle
            if query_hash in self.learned_knowledge:
                logger.info(f"🔄 Updating existing knowledge for query: {user_query[:50]}...")
                return self._update_existing_knowledge(query_hash, user_query, ai_response, web_content)
            
            # Yeni bilgi öğren
            return self._learn_new_knowledge(query_hash, user_query, ai_response, web_content)
            
        except Exception as e:
            logger.error(f"❌ Learning analysis failed: {e}")
            return False
    
    def _learn_new_knowledge(self, query_hash: str, user_query: str, ai_response: str, web_content: str) -> bool:
        """Yeni bilgi öğren"""
        try:
            # Kategori tespit et
            category = self._detect_category(user_query)
            
            # Anahtar kelimeler çıkar
            keywords = self._extract_keywords(user_query)
            
            # Bilgi kalitesini değerlendir
            quality_score = self._evaluate_response_quality(ai_response)
            
            # Yeni bilgi girişi oluştur
            knowledge_entry = {
                'query': user_query,
                'response': ai_response,
                'web_content': web_content[:1000] if web_content else "",  # İlk 1000 karakter
                'category': category,
                'keywords': keywords,
                'quality_score': quality_score,
                'learned_at': datetime.now().isoformat(),
                'usage_count': 0,
                'last_used': None
            }
            
            # Bilgiyi kaydet
            self.learned_knowledge[query_hash] = knowledge_entry
            
            # Dosyaya kaydet
            self.save_learned_knowledge()
            
            logger.info(f"🎓 New knowledge learned - Category: {category}, Quality: {quality_score}")
            return True
            
        except Exception as e:
            logger.error(f"❌ New knowledge learning failed: {e}")
            return False
    
    def _update_existing_knowledge(self, query_hash: str, user_query: str, ai_response: str, web_content: str) -> bool:
        """Mevcut bilgiyi güncelle"""
        try:
            existing = self.learned_knowledge[query_hash]
            
            # Yeni cevabın kalitesini değerlendir
            new_quality = self._evaluate_response_quality(ai_response)
            old_quality = existing.get('quality_score', 0)
            
            # Eğer yeni cevap daha kaliteliyse güncelle
            if new_quality > old_quality:
                existing['response'] = ai_response
                existing['quality_score'] = new_quality
                existing['updated_at'] = datetime.now().isoformat()
                
                if web_content:
                    existing['web_content'] = web_content[:1000]
                
                self.save_learned_knowledge()
                logger.info(f"📈 Knowledge updated with better quality: {new_quality} > {old_quality}")
                return True
            else:
                logger.info(f"📊 Existing knowledge quality is better: {old_quality} >= {new_quality}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Knowledge update failed: {e}")
            return False
    
    def search_learned_knowledge(self, query: str) -> Optional[Dict]:
        """
        Öğrenilen bilgiler arasında arama yap
        
        Args:
            query: Arama sorgusu
            
        Returns:
            Dict: Bulunan bilgi girişi veya None
        """
        try:
            query_lower = query.lower()
            best_match = None
            best_score = 0
            
            for entry in self.learned_knowledge.values():
                # Anahtar kelime eşleşmesi
                entry_keywords = entry.get('keywords', [])
                if isinstance(entry_keywords, str):
                    entry_keywords = entry_keywords.split()
                keyword_matches = sum(1 for keyword in entry_keywords if keyword in query_lower)
                
                # Soru benzerliği
                entry_query = entry.get('query', '')
                query_similarity = self._calculate_similarity(query_lower, entry_query.lower()) if entry_query else 0
                
                # Toplam skor
                quality_score = entry.get('quality_score', 0)
                total_score = (keyword_matches * 2) + (query_similarity * 3) + quality_score
                
                if total_score > best_score and total_score > 3:  # Minimum eşik
                    best_score = total_score
                    best_match = entry
            
            if best_match:
                # Kullanım sayısını artır
                best_match_query = best_match.get('query', '')
                if best_match_query:
                    query_hash = hashlib.md5(best_match_query.lower().encode()).hexdigest()
                if query_hash in self.learned_knowledge:
                    self.learned_knowledge[query_hash]['usage_count'] += 1
                    self.learned_knowledge[query_hash]['last_used'] = datetime.now().isoformat()
                
                logger.info(f"🎯 Found learned knowledge match - Score: {best_score}")
                return best_match
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Learned knowledge search failed: {e}")
            return None
    
    def _detect_category(self, query: str) -> str:
        """Soru kategorisini tespit et"""
        query_lower = query.lower()
        
        categories = {
            'android': ['android', 'java', 'kotlin', 'recyclerview', 'listview', 'activity'],
            'web_frontend': ['react', 'vue', 'angular', 'javascript', 'html', 'css', 'frontend'],
            'web_backend': ['flask', 'django', 'express', 'api', 'backend', 'server'],
            'python': ['python', 'tkinter', 'pyqt', 'pandas', 'numpy'],
            'mobile': ['flutter', 'dart', 'ios', 'swift', 'mobile'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'database'],
            'general': []
        }
        
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Sorudan anahtar kelimeleri çıkar"""
        # Türkçe ve İngilizce stop words
        stop_words = {
            'bir', 'bu', 'şu', 'o', 've', 'ile', 'için', 'nasıl', 'ne', 'nedir', 'olan',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'by', 'how', 'what', 'where', 'when', 'why', 'which', 'that', 'this'
        }
        
        # Kelimeleri ayır ve temizle
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        return keywords[:10]  # En fazla 10 anahtar kelime
    
    def _evaluate_response_quality(self, response: str) -> float:
        """Cevap kalitesini değerlendir (0-10 arası)"""
        try:
            score = 0.0
            
            # Uzunluk skoru (çok kısa veya çok uzun cevaplar düşük puan)
            length = len(response)
            if 100 <= length <= 5000:
                score += 2.0
            elif 50 <= length < 100 or 5000 < length <= 10000:
                score += 1.0
            
            # Kod bloğu varlığı
            if '```' in response:
                score += 2.0
            
            # Yapılandırılmış içerik (başlıklar, listeler)
            if any(marker in response for marker in ['##', '**', '- ', '1.', '2.']):
                score += 1.5
            
            # Emoji kullanımı (kullanıcı dostu)
            emoji_count = len(re.findall(r'[🎯🚀✅❌🔧🎨📱💡🌐🔍📊🎮]', response))
            if emoji_count > 0:
                score += min(emoji_count * 0.3, 1.0)
            
            # Teknik terimler
            technical_terms = ['class', 'function', 'method', 'variable', 'import', 'export', 'component']
            term_count = sum(1 for term in technical_terms if term in response.lower())
            score += min(term_count * 0.2, 1.5)
            
            return min(score, 10.0)  # Maksimum 10 puan
            
        except Exception as e:
            logger.error(f"❌ Quality evaluation failed: {e}")
            return 5.0  # Varsayılan orta kalite
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """İki metin arasındaki benzerliği hesapla (0-1 arası)"""
        try:
            words1 = set(text1.split())
            words2 = set(text2.split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
            
        except Exception:
            return 0.0
    
    def get_learning_stats(self) -> Dict:
        """Öğrenme istatistiklerini getir"""
        return {
            'total_learned': len(self.learned_knowledge),
            'categories': self.learning_stats.get('categories', {}),
            'last_update': self.learning_stats.get('last_update'),
            'top_used': self._get_most_used_knowledge(5)
        }
    
    def _get_most_used_knowledge(self, limit: int = 5) -> List[Dict]:
        """En çok kullanılan bilgileri getir"""
        try:
            sorted_knowledge = sorted(
                self.learned_knowledge.values(),
                key=lambda x: x.get('usage_count', 0),
                reverse=True
            )
            
            return [
                {
                    'query': entry.get('query', 'Unknown')[:100] + '...' if len(entry.get('query', '')) > 100 else entry.get('query', 'Unknown'),
                    'category': entry.get('category', 'unknown'),
                    'usage_count': entry.get('usage_count', 0),
                    'quality_score': entry.get('quality_score', 0)
                }
                for entry in sorted_knowledge[:limit]
            ]
            
        except Exception as e:
            logger.error(f"❌ Most used knowledge retrieval failed: {e}")
            return []
    
    def cleanup_old_knowledge(self, days_threshold: int = 30, min_usage: int = 1):
        """Eski ve az kullanılan bilgileri temizle"""
        try:
            current_time = datetime.now()
            removed_count = 0
            
            to_remove = []
            for query_hash, entry in self.learned_knowledge.items():
                learned_at = datetime.fromisoformat(entry['learned_at'])
                days_old = (current_time - learned_at).days
                usage_count = entry.get('usage_count', 0)
                
                # Eski ve az kullanılan bilgileri işaretle
                if days_old > days_threshold and usage_count < min_usage:
                    to_remove.append(query_hash)
            
            # İşaretlenen bilgileri kaldır
            for query_hash in to_remove:
                del self.learned_knowledge[query_hash]
                removed_count += 1
            
            if removed_count > 0:
                self.save_learned_knowledge()
                logger.info(f"🧹 Cleaned up {removed_count} old knowledge entries")
            
            return removed_count
            
        except Exception as e:
            logger.error(f"❌ Knowledge cleanup failed: {e}")
            return 0