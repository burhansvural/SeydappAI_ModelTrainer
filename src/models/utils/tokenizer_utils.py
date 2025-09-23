# src/models/utils/tokenizer_utils.py
"""Tokenizer utilities and helpers"""
import torch
import logging
from transformers import AutoTokenizer
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class TokenizerUtils:
    """Tokenizer utilities and optimizations"""

    @staticmethod
    def configure_tokenizer(tokenizer: AutoTokenizer) -> AutoTokenizer:
        """Configure tokenizer with optimal settings"""
        # Set pad token if not present
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            logger.debug("🔧 Pad token configured as EOS token")

        # Additional tokenizer optimizations
        if hasattr(tokenizer, 'model_max_length') and tokenizer.model_max_length > 2048:
            tokenizer.model_max_length = 2048  # Reasonable limit
            logger.debug("🔧 Tokenizer max length limited to 2048")

        return tokenizer

    @staticmethod
    def batch_tokenize(
            texts: List[str],
            tokenizer: AutoTokenizer,
            max_length: int = 512,
            rtx3060_optimized: bool = False
    ) -> Dict[str, torch.Tensor]:
        """Optimized batch tokenization"""

        # RTX 3060 specific optimizations
        if rtx3060_optimized:
            max_length = min(max_length, 512)  # Limit for memory
            batch_size = min(len(texts), 32)  # Smaller batches
        else:
            batch_size = len(texts)

        try:
            tokenized = tokenizer(
                texts,
                truncation=True,
                padding="max_length",
                max_length=max_length,
                return_attention_mask=True,
                return_tensors="pt"
            )

            logger.debug(f"🔤 Tokenized {len(texts)} texts (max_len: {max_length})")
            return tokenized

        except Exception as e:
            logger.error(f"❌ Batch tokenization failed: {e}")
            raise

    @staticmethod
    def estimate_token_count(text: str, tokenizer: AutoTokenizer) -> int:
        """Estimate token count for a text"""
        try:
            tokens = tokenizer.encode(text, add_special_tokens=True)
            return len(tokens)
        except Exception as e:
            logger.warning(f"⚠️ Token estimation failed: {e}")
            # Rough estimation: ~4 characters per token
            return len(text) // 4
