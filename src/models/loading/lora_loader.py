# src/models/loading/lora_loader.py
"""LoRA Model Loading Module"""
import torch
import logging
from pathlib import Path
from peft import PeftModel, LoraConfig, get_peft_model
from typing import Tuple, Any

logger = logging.getLogger(__name__)


class LoRALoader:
    """LoRA adapter loading and management"""

    def __init__(self, base_loader):
        self.base_loader = base_loader

    def load_lora_model(self, base_model_name: str, lora_path: str) -> Tuple[Any, Any]:
        """Load model with LoRA adapter"""
        logger.info(f"🔄 Loading LoRA model: {lora_path}")

        try:
            # Load base model first
            base_model, tokenizer = self.base_loader.load_base_model(
                base_model_name, use_quantization=True
            )

            # Load LoRA adapter if path exists
            lora_path = Path(lora_path)
            if lora_path.exists() and (lora_path / 'adapter_config.json').exists():
                model = PeftModel.from_pretrained(base_model, lora_path)
                logger.info(f"✅ LoRA adapter loaded: {lora_path}")
            else:
                logger.warning(f"⚠️ LoRA path not found: {lora_path}")
                model = base_model

            return model, tokenizer

        except Exception as e:
            logger.error(f"❌ LoRA model loading failed: {e}")
            raise

    def create_lora_model(self, base_model, lora_config: LoraConfig = None):
        """Create LoRA model from base model"""
        if lora_config is None:
            # Default RTX 3060 optimized LoRA config
            lora_config = LoraConfig(
                r=8,  # Low rank for memory efficiency
                lora_alpha=32,
                target_modules=["q_proj", "v_proj"],
                lora_dropout=0.05,
                bias="none",
                task_type="CAUSAL_LM"
            )

        model = get_peft_model(base_model, lora_config)
        model.print_trainable_parameters()

        logger.info("✅ LoRA model created")
        return model
