# src/models/__init__.py
"""
Complete Model Loader System - Final Integration
Following PyTorch best practices and CS230 patterns[2]
"""
from .core.gpu_detector import GPUDetector
from .core.device_manager import DeviceManager
from .memory.memory_manager import MemoryManager
from .memory.oom_handler import OOMHandler
from .memory.cleanup_utils import enhanced_gpu_cleanup, safe_gpu_cleanup
from .loading.base_loader import BaseModelLoader
from .loading.lora_loader import LoRALoader
from .loading.model_cache import ModelCache
from .training.trainer import RTX3060Trainer
from .training.training_context import TrainingContext
from .utils.validation import ParameterValidator

import threading
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class GPUModelLoader:
    """
    Complete GPU Model Loader System
    Modular architecture following PyTorch best practices[1][2]
    """

    def __init__(self):
        # Hardware detection
        self.rtx3060_detected = GPUDetector.detect_rtx3060()
        gpu_info = GPUDetector.get_gpu_info()

        # Device management
        self.device_manager = DeviceManager(self.rtx3060_detected)
        self.device = self.device_manager.get_device()

        # Memory management
        self.memory_manager = MemoryManager(self.rtx3060_detected)
        self.oom_handler = OOMHandler(self.rtx3060_detected)

        # Model loading subsystem
        self.base_loader = BaseModelLoader(self.rtx3060_detected, self.device)
        self.lora_loader = LoRALoader(self.base_loader)
        self.model_cache = ModelCache()

        # Training subsystem
        self.trainer = RTX3060Trainer(self.rtx3060_detected, self.device)

        # Apply initial optimizations
        if self.rtx3060_detected:
            self.memory_manager.start_memory_monitoring()

        logger.info(f"✅ Complete GPUModelLoader initialized")
        logger.info(f"🎮 RTX 3060 Detected: {self.rtx3060_detected}")
        logger.info(f"🖥️ Device: {self.device}")
        logger.info(f"📊 GPU Info: {gpu_info}")

    def load_base_model(self, model_name: str, **kwargs):
        """Load base model with caching"""
        # Check cache first
        cache_key = self.model_cache.get_cache_key(
            model_name, kwargs.get('use_quantization', True)
        )
        cached_result = self.model_cache.get_cached_model(cache_key)

        if cached_result:
            return cached_result

        # Load model
        model, tokenizer = self.base_loader.load_base_model(model_name, **kwargs)

        # Cache the result
        self.model_cache.cache_model(cache_key, model, tokenizer)

        return model, tokenizer

    def load_lora_model(self, base_model_name: str, lora_path: str):
        """Load LoRA model"""
        return self.lora_loader.load_lora_model(base_model_name, lora_path)

    def run_optimized_training(self, examples: List[Dict], topic: Optional[str] = None):
        """Run complete optimized training"""
        # Validate training data
        if not ParameterValidator.validate_training_data(examples):
            return {"status": "error", "message": "Invalid training data"}

        # Check OOM recovery status
        if self.oom_handler.is_recovery_active():
            return {"status": "error", "message": "OOM recovery in progress"}

        # Set memory manager training status
        self.memory_manager.set_training_active(True)

        try:
            # Run training
            result = self.trainer.run_optimized_training(examples, topic)
            return result

        except torch.cuda.OutOfMemoryError:
            # Handle OOM with specialized handler
            memory_info = self.memory_manager.get_memory_info()
            self.oom_handler.handle_oom_error(memory_info)

            suggestions = self.oom_handler.get_recovery_suggestions()
            return {
                "status": "error",
                "message": "CUDA Out of Memory",
                "suggestions": suggestions
            }
        finally:
            # Always cleanup training status
            self.memory_manager.set_training_active(False)

    def get_gpu_memory_info(self):
        """Get comprehensive GPU memory information"""
        base_info = self.memory_manager.get_memory_info()
        cache_info = self.model_cache.get_cache_info()

        return {
            **base_info,
            "cache_info": cache_info,
            "rtx3060_detected": self.rtx3060_detected
        }

    def cleanup_all(self):
        """Complete system cleanup"""
        logger.info("🧹 Starting complete system cleanup")

        # Stop memory monitoring
        self.memory_manager.stop_monitoring()

        # Clear model cache
        self.model_cache.clear_cache()

        # GPU cleanup
        enhanced_gpu_cleanup()

        logger.info("✅ Complete system cleanup finished")

    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            "rtx3060_detected": self.rtx3060_detected,
            "device": str(self.device),
            "memory_info": self.get_gpu_memory_info(),
            "training_active": self.memory_manager._training_active,
            "oom_recovery_active": self.oom_handler.is_recovery_active(),
            "cache_status": self.model_cache.get_cache_info()
        }


# Global singleton pattern with thread safety
_model_loader_instance: Optional[GPUModelLoader] = None
_loader_lock = threading.Lock()


def get_model_loader() -> GPUModelLoader:
    """Thread-safe singleton getter"""
    global _model_loader_instance

    if _model_loader_instance is None:
        with _loader_lock:
            if _model_loader_instance is None:
                _model_loader_instance = GPUModelLoader()

    return _model_loader_instance


# Convenience functions for backward compatibility
def load_base_model(model_name: str, **kwargs):
    """Load base model - convenience function"""
    return get_model_loader().load_base_model(model_name, **kwargs)


def load_trained_model(model_path: str):
    """Load trained model - convenience function"""
    return get_model_loader().load_lora_model("bigcode/starcoder2-3b", model_path)


def get_device():
    """Get current device - convenience function"""
    return get_model_loader().device


def run_optimized_training(examples: List[Dict], topic: Optional[str] = None):
    """
    Main training function with pre-training setup
    Following PyTorch training loop patterns[1][2][3]
    """
    logger.info(f"🚀 Pre-training setup for: {topic}")

    # Pre-training cleanup
    enhanced_gpu_cleanup()

    # CUDA stability check
    if torch.cuda.is_available():
        try:
            test_tensor = torch.tensor([1.0], device='cuda')
            _ = test_tensor + 1
            del test_tensor
            torch.cuda.empty_cache()
            logger.info("✅ CUDA pre-flight check passed")
        except Exception as e:
            logger.error(f"❌ CUDA pre-flight failed: {e}")
            enhanced_gpu_cleanup()

    # Run training
    model_loader = get_model_loader()
    return model_loader.run_optimized_training(examples, topic)


# System management functions
def cleanup_gpu_system():
    """Cleanup entire GPU system"""
    model_loader = get_model_loader()
    model_loader.cleanup_all()


def get_system_status():
    """Get complete system status"""
    model_loader = get_model_loader()
    return model_loader.get_system_status()


# Export all public interfaces
__all__ = [
    'GPUModelLoader', 'get_model_loader',
    'load_base_model', 'load_trained_model', 'get_device',
    'run_optimized_training', 'cleanup_gpu_system', 'get_system_status',
    'enhanced_gpu_cleanup', 'safe_gpu_cleanup'
]
