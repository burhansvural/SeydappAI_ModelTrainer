# src/models/loading/model_cache.py
"""Model Cache Management System"""
import torch
import logging
from typing import Dict, Any, Optional, Tuple
from threading import Lock

logger = logging.getLogger(__name__)


class ModelCache:
    """Thread-safe model cache for performance optimization"""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._max_cache_size = 3  # Maximum models to cache

    def get_cache_key(self, model_name: str, quantization: bool = True) -> str:
        """Generate cache key for model"""
        return f"{model_name}_quant_{quantization}"

    def get_cached_model(self, cache_key: str) -> Optional[Tuple[Any, Any]]:
        """Get model from cache if available"""
        with self._lock:
            if cache_key in self._cache:
                cached_item = self._cache[cache_key]

                # PEFT cleanup check
                model = cached_item['model']
                if hasattr(model, 'peft_config'):
                    if hasattr(model, 'unload'):
                        try:
                            model.unload()
                            logger.info("🔄 PEFT adapter unloaded")
                        except Exception as e:
                            logger.warning(f"⚠️ PEFT unload failed: {e}")
                            # Remove problematic cache entry
                            del self._cache[cache_key]
                            return None
                    else:
                        # No unload method, remove from cache
                        del self._cache[cache_key]
                        return None

                logger.info("📚 Model loaded from cache")
                return model, cached_item['tokenizer']

        return None

    def cache_model(self, cache_key: str, model: Any, tokenizer: Any):
        """Cache model with size management"""
        with self._lock:
            # Check cache size and evict if necessary
            if len(self._cache) >= self._max_cache_size:
                self._evict_oldest()

            # Cache the model
            device = next(model.parameters()).device if hasattr(model, 'parameters') else 'unknown'

            self._cache[cache_key] = {
                'model': model,
                'tokenizer': tokenizer,
                'device': device
            }

            logger.debug(f"📚 Model cached: {cache_key}")

    def _evict_oldest(self):
        """Evict oldest cache entry (simple FIFO)"""
        if self._cache:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.debug(f"🗑️ Evicted from cache: {oldest_key}")

    def clear_cache(self):
        """Clear all cached models"""
        with self._lock:
            # Cleanup models before clearing
            for cache_key, cached_item in self._cache.items():
                try:
                    model = cached_item['model']
                    if hasattr(model, 'cpu'):
                        model.cpu()
                    del model
                except Exception as e:
                    logger.warning(f"⚠️ Cache cleanup error for {cache_key}: {e}")

            self._cache.clear()

            # Force garbage collection
            import gc
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            logger.info("🗑️ Model cache cleared")

    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            return {
                'cached_models': list(self._cache.keys()),
                'cache_size': len(self._cache),
                'max_size': self._max_cache_size
            }
