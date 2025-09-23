# src/models/loading/base_loader.py
"""
Base Model Loading following PyTorch best practices[5]
HuggingFace Transformers integration
"""
import torch
import logging
import os
from pathlib import Path
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
)
from peft import prepare_model_for_kbit_training
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)


class BaseModelLoader:
    """Base model loading with RTX 3060 optimizations"""

    def __init__(self, rtx3060_detected: bool, device: torch.device):
        self.rtx3060_detected = rtx3060_detected
        self.device = device
        self._setup_optimizations()

    def _setup_optimizations(self):
        """Setup device-specific optimizations"""
        if self.rtx3060_detected:
            # RTX 3060 memory optimizations
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:32'
            logger.debug("🔧 RTX 3060 loading optimizations applied")

    def load_base_model(
            self,
            model_name: str,
            use_quantization: bool = True,
            use_auto_device_map: bool = True
    ) -> Tuple[torch.nn.Module, AutoTokenizer]:
        """
        Load base model following HuggingFace patterns[5]
        """
        logger.info(f"🔄 Loading model: {model_name}")

        # Force quantization for RTX 3060
        if self.rtx3060_detected:
            use_quantization = True
            logger.info("🔧 RTX 3060 detected - quantization enforced")

        try:
            # Load tokenizer first
            tokenizer = self._load_tokenizer(model_name)

            # Configure model loading
            model_kwargs = self._get_model_kwargs(use_quantization, use_auto_device_map)

            # Load model with error handling
            model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)

            # Post-loading optimizations
            model = self._post_loading_optimizations(model, use_quantization)

            logger.info(f"✅ Model loaded successfully on {next(model.parameters()).device}")
            return model, tokenizer

        except torch.cuda.OutOfMemoryError:
            logger.error("❌ CUDA OOM during model loading")
            raise
        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            raise

    def _load_tokenizer(self, model_name: str) -> AutoTokenizer:
        """Load and configure tokenizer"""
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Configure pad token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            logger.debug("🔧 Pad token configured")

        return tokenizer

    def _get_model_kwargs(self, use_quantization: bool, use_auto_device_map: bool) -> Dict[str, Any]:
        """Get model loading configuration"""
        model_kwargs = {
            'use_cache': False,
            'dtype': torch.bfloat16,
        }

        if self.device.type == 'cuda':
            if use_quantization:
                # 4-bit quantization configuration
                model_kwargs['quantization_config'] = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    bnb_4bit_quant_type='nf4',
                    bnb_4bit_use_double_quant=True
                )
                logger.info("🔧 4-bit quantization configured")
            else:
                model_kwargs['low_cpu_mem_usage'] = True

            if use_auto_device_map:
                model_kwargs['device_map'] = 'auto'
                logger.debug("🔧 Auto device mapping enabled")

        return model_kwargs

    def _post_loading_optimizations(self, model, use_quantization: bool):
        """Apply post-loading optimizations"""
        # Meta tensor fix
        if hasattr(model, 'parameters'):
            for param in model.parameters():
                if param.device == torch.device('meta'):
                    logger.warning("⚠️ Meta tensor detected - moving to device")
                    model = model.to_empty(device=self.device)
                    break

        # K-bit training preparation
        if use_quantization:
            model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
            logger.debug("🔧 Model prepared for k-bit training")

        return model
