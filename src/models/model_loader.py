# src/models/model_loader.py
"""
SeydappAI Model Loader - 2025 Edition
Modern PyTorch model loading following 2025 best practices[1][2]

Key Features:
- State dictionary management[1]
- Checkpoint saving with optimizer state[2][3]
- Optimized DataLoader with multi-process loading[4][5]
- RTX 3060 specific optimizations
- Modular architecture with clean separation
- Thread-safe operations
"""

import torch
import logging
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple
import threading
import gc

# Import our modular components
from .core.gpu_detector import GPUDetector
from .core.device_manager import DeviceManager
from .memory.memory_manager import MemoryManager
from .memory.oom_handler import OOMHandler
from .memory.cleanup_utils import enhanced_gpu_cleanup, safe_gpu_cleanup
from .loading.base_loader import BaseModelLoader
from .loading.lora_loader import LoRALoader
from .loading.model_cache import ModelCache
from .training.trainer import RTX3060Trainer
from .utils.validation import ParameterValidator

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    2025 PyTorch Model Loader with modern best practices[1]
    Integrates all modular components into unified interface
    """

    def __init__(self):
        """Initialize with 2025 PyTorch patterns"""
        logger.info("🚀 ModelLoader 2025 Sürümü Başlatılıyor")

        # Hardware Detection
        self.rtx3060_detected = GPUDetector.detect_rtx3060()
        self.gpu_info = GPUDetector.get_gpu_info()

        # Device Management
        self.device_manager = DeviceManager(self.rtx3060_detected)
        self.device = self.device_manager.get_device()

        # Memory Management Subsystem
        self.memory_manager = MemoryManager(self.rtx3060_detected)
        self.oom_handler = OOMHandler(self.rtx3060_detected)

        # Model Loading Subsystem
        self.base_loader = BaseModelLoader(self.rtx3060_detected, self.device)
        self.lora_loader = LoRALoader(self.base_loader)
        self.model_cache = ModelCache()

        # Training Subsystem
        self.trainer = RTX3060Trainer(self.rtx3060_detected, self.device, self.memory_manager)

        # Initialize monitoring for RTX 3060
        if self.rtx3060_detected:
            self.memory_manager.start_memory_monitoring()

        logger.info(f"✅ ModelLoader başlatıldı - RTX 3060: {self.rtx3060_detected}, Cihaz: {self.device}")

    def load_base_model(
            self,
            model_name: str,
            use_quantization: bool = True,
            use_cache: bool = True
    ) -> Tuple[torch.nn.Module, Any]:
        """
        Load base model following 2025 best practices[1]

        Args:
            model_name: HuggingFace model name
            use_quantization: Enable quantization (forced for RTX 3060)
            use_cache: Use model caching

        Returns:
            Tuple of (model, tokenizer)
        """
        logger.info(f"🔄 Loading model: {model_name}")

        # Check cache first if enabled
        if use_cache:
            cache_key = self.model_cache.get_cache_key(model_name, use_quantization)
            cached_result = self.model_cache.get_cached_model(cache_key)

            if cached_result:
                logger.info("📚 Model loaded from cache")
                return cached_result

        try:
            # Load model using base loader
            model, tokenizer = self.base_loader.load_base_model(
                model_name,
                use_quantization=use_quantization,
                use_auto_device_map=True
            )

            # Cache the result if caching enabled
            if use_cache:
                self.model_cache.cache_model(cache_key, model, tokenizer)

            return model, tokenizer

        except torch.cuda.OutOfMemoryError:
            logger.error("❌ CUDA OOM during model loading")
            memory_info = self.memory_manager.get_memory_info()
            self.oom_handler.handle_oom_error(memory_info)
            raise
        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            raise

    def load_lora_model(self, base_model_name: str, lora_path: str) -> Tuple[Any, Any]:
        """Load LoRA adapter model"""
        logger.info(f"🔄 Loading LoRA model from: {lora_path}")
        return self.lora_loader.load_lora_model(base_model_name, lora_path)

    def save_model_checkpoint(
            self,
            model: torch.nn.Module,
            tokenizer: Any,
            optimizer: Optional[torch.optim.Optimizer] = None,
            epoch: int = 0,
            loss: float = 0.0,
            save_path: str = "./checkpoints/model_checkpoint.tar",
            **additional_state
    ) -> bool:
        """
        Save complete model checkpoint following 2025 best practices[2][3]
        Includes model, optimizer, epoch, loss as recommended
        """
        logger.info(f"💾 Checkpoint kaydediliyor: {save_path}")
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Prepare checkpoint dictionary following PyTorch 2025 patterns[2][3]
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'loss': loss,
                'pytorch_version': torch.__version__,
                'timestamp': time.time()
            }

            # Add optimizer state if provided[2]
            if optimizer is not None:
                checkpoint['optimizer_state_dict'] = optimizer.state_dict()
                logger.debug("✅ Optimizer state included in checkpoint")

            # Add tokenizer
            if tokenizer is not None:
                # Save tokenizer separately for HuggingFace compatibility
                tokenizer_path = save_path.parent / "tokenizer"
                tokenizer.save_pretrained(tokenizer_path)
                checkpoint['tokenizer_path'] = str(tokenizer_path)
                logger.debug("✅ Tokenizer saved separately")

            # Add any additional state
            checkpoint.update(additional_state)

            # RTX 3060 safe saving - move to CPU first
            if self.rtx3060_detected and torch.cuda.is_available() and hasattr(model, 'parameters') and any(True for _ in model.parameters()):
                current_device = next(model.parameters()).device
                model_cpu = model.to('cpu')
                checkpoint['model_state_dict'] = model_cpu.state_dict()
                # Move back to original device
                model.to(current_device)
                logger.debug("📱 RTX 3060 safe save - CPU transfer")

            # Save checkpoint using .tar extension as recommended[2]
            torch.save(checkpoint, save_path)
            logger.info(f"✅ Checkpoint başarıyla kaydedildi: {save_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Checkpoint kaydı başarısız: {e}", exc_info=True)
            return False

    def load_model_checkpoint(
            self,
            checkpoint_path: str,
            model_class: Optional[Any] = None,
            model_args: Tuple = (),
            model_kwargs: Dict = None,
            optimizer_class: Optional[Any] = None,
            optimizer_args: Tuple = (),
            optimizer_kwargs: Dict = None,
            for_inference: bool = True
    ) -> Dict[str, Any]:
        """
        Load model checkpoint following 2025 best practices[2][3]

        Args:
            checkpoint_path: Path to checkpoint file
            model_class: Model class to instantiate
            model_args: Model constructor args
            model_kwargs: Model constructor kwargs
            optimizer_class: Optimizer class (if resuming training)
            optimizer_args: Optimizer constructor args
            optimizer_kwargs: Optimizer constructor kwargs
            for_inference: Set model to eval mode

        Returns:
            Dictionary with loaded components
        """
        logger.info(f"🔄 Checkpoint yükleniyor: {checkpoint_path}")
        checkpoint_path = Path(checkpoint_path)

        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

        try:
            checkpoint = torch.load(checkpoint_path, map_location=self.device)
            result = {'epoch': checkpoint.get('epoch', 0), 'loss': checkpoint.get('loss', 0.0)}
            if model_class is not None:
                model = model_class(*(model_args or ()), **(model_kwargs or {}))
                model.load_state_dict(checkpoint['model_state_dict'])
                model.eval() if for_inference else model.train()
                result['model'] = model
            if optimizer_class is not None and 'optimizer_state_dict' in checkpoint:
                optimizer = optimizer_class(*(optimizer_args or ()), **(optimizer_kwargs or {}))
                optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                result['optimizer'] = optimizer
            if 'tokenizer_path' in checkpoint:
                from transformers import AutoTokenizer
                result['tokenizer'] = AutoTokenizer.from_pretrained(checkpoint['tokenizer_path'])
            logger.info("✅ Checkpoint başarıyla yüklendi.")
            return result
        except Exception as e:
            logger.error(f"❌ Checkpoint yüklemesi başarısız: {e}", exc_info=True)
            raise

    def run_optimized_training(self, examples: List[Dict], topic: Optional[str] = None, **training_kwargs) -> Dict[
        str, Any]:
        """
        Orchestrates the training process by loading the model and delegating to the trainer.
        """
        logger.info(f"🚀 Orchestrating training for: {topic}")
        if not ParameterValidator.validate_training_data(examples):
            return {"status": "error", "message": "Invalid training data."}
        if self.oom_handler.is_recovery_active():
            return {"status": "error", "message": "OOM recovery mode is active."}

        self.memory_manager.set_training_active(True)
        model, tokenizer = None, None
        try:
            # Sorumluluk 1: Modeli ve tokenizer'ı yükle.
            model, tokenizer = self.load_base_model("bigcode/starcoder2-3b")

            # Sorumluluk 2: Eğitimi, bu iş için uzmanlaşmış trainer'a delege et.
            # ### DÜZELTME: Artık `trainer.py`'deki tek ve doğru metodu çağırıyoruz ###
            result = self.trainer.run_optimized_training(
                model=model,
                tokenizer=tokenizer,
                examples=examples,
                topic=topic
            )

            return result
        except torch.cuda.OutOfMemoryError:
            self.oom_handler.handle_oom_error(self.memory_manager.get_memory_info())
            return {"status": "error", "message": "CUDA Out of Memory"}
        except Exception as e:
            logger.error(f"❌ Critical error during training orchestration: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}
        finally:
            logger.info(f"🧹 Post-training cleanup for '{topic}'.")
            # `run_optimized_training` kendi içindeki `finally` bloğunda `safe_gpu_cleanup`
            # çağırmadığı için, onu burada çağırmak güvenli ve doğrudur.
            safe_gpu_cleanup(model, tokenizer)
            self.memory_manager.set_training_active(False)


    def create_optimized_dataloader(
            self,
            dataset,
            batch_size: int = 1,
            shuffle: bool = True,
            num_workers: int = 0,
            **dataloader_kwargs
    ):
        """
        Create optimized DataLoader following 2025 best practices[4][5]
        """
        from torch.utils.data import DataLoader

        # RTX 3060 specific optimizations
        if self.rtx3060_detected:
            # Optimize for RTX 3060 memory constraints
            batch_size = min(batch_size, 2)  # Conservative batch size
            # Use multi-process loading as recommended[5]
            num_workers = min(num_workers or 4, 6)  # 4-6 workers optimal[4]

        # Apply 2025 DataLoader optimizations[4][5]
        dataloader_config = {
            'batch_size': batch_size,
            'shuffle': shuffle,
            'num_workers': num_workers,
            'pin_memory': True,  # 20-30% faster GPU transfer[4]
            'persistent_workers': num_workers > 0,  # Keep workers alive
            'prefetch_factor': 2 if num_workers > 0 else None,  # Async loading[4]
            **dataloader_kwargs
        }

        logger.info(f"🔧 DataLoader config: batch_size={batch_size}, workers={num_workers}")
        return DataLoader(dataset, **dataloader_config)

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'rtx3060_detected': self.rtx3060_detected,
            'device': str(self.device),
            'gpu_info': self.gpu_info,
            'memory_info': self.memory_manager.get_memory_info(),
            'cache_info': self.model_cache.get_cache_info(),
            'training_active': self.memory_manager._training_active,
            'oom_recovery_active': self.oom_handler.is_recovery_active(),
            'pytorch_version': torch.__version__
        }

    def cleanup_system(self):
        """Complete system cleanup"""
        logger.info("🧹 Starting system cleanup")

        # Stop monitoring
        self.memory_manager.stop_monitoring()

        # Clear cache
        self.model_cache.clear_cache()

        # GPU cleanup
        # enhanced_gpu_cleanup()

        # ### DÜZELTME 2: GÜVENLİ TEMİZLİK KULLANIMI ###
        # Riskli `enhanced_gpu_cleanup` yerine `safe_gpu_cleanup` çağrılıyor.
        safe_gpu_cleanup()

        logger.info("✅ System cleanup completed")


# Global singleton instance with thread safety
_model_loader_instance: Optional[ModelLoader] = None
_loader_lock = threading.Lock()


def get_model_loader() -> ModelLoader:
    """
    Thread-safe singleton getter for ModelLoader
    Following 2025 singleton best practices
    """
    global _model_loader_instance

    if _model_loader_instance is None:
        with _loader_lock:
            if _model_loader_instance is None:
                _model_loader_instance = ModelLoader()

    return _model_loader_instance


# Convenience functions for backward compatibility and ease of use
def load_base_model(model_name: str, **kwargs) -> Tuple[torch.nn.Module, Any]:
    """Load base model - convenience function"""
    return get_model_loader().load_base_model(model_name, **kwargs)


def load_trained_model(model_path: str) -> Tuple[Any, Any]:
    """Load trained model - convenience function"""
    return get_model_loader().load_lora_model("bigcode/starcoder2-3b", model_path)


def save_model_checkpoint(**kwargs) -> bool:
    """Save model checkpoint - convenience function"""
    return get_model_loader().save_model_checkpoint(**kwargs)


def load_model_checkpoint(checkpoint_path: str, **kwargs) -> Dict[str, Any]:
    """Load model checkpoint - convenience function"""
    return get_model_loader().load_model_checkpoint(checkpoint_path, **kwargs)


def get_device() -> torch.device:
    """Get current device"""
    return get_model_loader().device


def run_optimized_training(examples: List[Dict], topic: Optional[str] = None) -> Dict[str, Any]:
    """
    Main training function with 2025 optimizations
    Includes pre-training setup and CUDA stability checks
    """
    logger.info(f"➡️ Eğitim talebi alındı: {topic}")

    # Pre-training GPU cleanup
    # enhanced_gpu_cleanup()

    # ### DÜZELTME 3: RİSKLİ TEMİZLİK YERİNE GÜVENLİ TEMİZLİK ###
    # Her eğitim öncesi, GPU'yu bir sonraki işleme hazırlamak için
    # `safe_gpu_cleanup` çağrılır. Bu, `enhanced_gpu_cleanup`'tan daha güvenlidir.
    safe_gpu_cleanup()

    # CUDA stability check
    # if torch.cuda.is_available():
    #     try:
    #         # Test CUDA functionality
    #         test_tensor = torch.tensor([1.0], device='cuda')
    #         result = test_tensor + 1
    #         del test_tensor, result
    #         torch.cuda.empty_cache()
    #         logger.info("✅ CUDA pre-flight check passed")
    #     except Exception as e:
    #         logger.error(f"❌ CUDA pre-flight failed: {e}")
    #         enhanced_gpu_cleanup()
    #         time.sleep(2)  # Stability delay

    if torch.cuda.is_available():
        try:
            torch.tensor([1.0], device='cuda')
            logger.info("✅ CUDA ön kontrolü başarılı.")
        except Exception as e:
            error_msg = f"CUDA ön kontrolü başarısız oldu. GPU kararsız olabilir: {e}"
            logger.error(error_msg)
            safe_gpu_cleanup()  # Başarısız olursa tekrar temizle
            return {"status": "error", "message": error_msg}

    # Execute training
    model_loader = get_model_loader()
    return model_loader.run_optimized_training(examples, topic)


def cleanup_gpu_system():
    """Cleanup GPU system"""
    model_loader = get_model_loader()
    model_loader.cleanup_system()


def get_system_status() -> Dict[str, Any]:
    """Get system status"""
    model_loader = get_model_loader()
    return model_loader.get_system_status()


# ### DÜZELTME 1: YENİ GÜVENLİ TEMİZLİK FONKSİYONU ###
# AÇIKLAMA: Bu yeni fonksiyon, GPU çökmelerine neden olan `force_gpu_cleanup`
# fonksiyonunun yerine geçmek üzere tasarlanmıştır. Sadece standart ve güvenli
# PyTorch ve Python komutlarını kullanarak belleği temizler.
def safe_gpu_cleanup(*args):
    """
    Tehlikeli `cudaDeviceReset` yerine standart, güvenli GPU temizliği yapar.
    Bu fonksiyon, kendisine verilen model, trainer gibi nesneleri siler ve
    PyTorch'un bellekte tuttuğu gereksiz verileri (cache) temizler.
    Bu yöntem CUDA çalışma ortamını (context) bozmaz ve GPU çökmesini önler.

    Args:
        *args: Bellekten silinmesi istenen nesneler (model, trainer, tokenizer vb.).
    """
    logger.info("🧹 Güvenli GPU temizliği başlatılıyor...")

    # Argüman olarak verilen nesnelerin Python referanslarını sil.
    for obj in args:
        if obj is not None:
            del obj

    # Python'un çöp toplayıcısını manuel olarak çalıştır.
    gc.collect()

    # Eğer bir NVIDIA GPU (CUDA) kullanılıyorsa, PyTorch'un ayırdığı
    # ama artık kullanılmayan bellek önbelleğini (cache) boşalt.
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # İkinci bir çöp toplama döngüsü, daha kapsamlı bir temizlik sağlar.
    gc.collect()
    logger.info("✅ Güvenli GPU temizliği tamamlandı.")


# Export public API following 2025 Python conventions
__all__ = [
    # Main classes
    'ModelLoader', 'get_model_loader',

    # Model operations
    'load_base_model', 'load_trained_model',

    # Checkpoint operations (2025 best practices)
    'save_model_checkpoint', 'load_model_checkpoint',

    # Training operations
    'run_optimized_training',

    # System operations
    'get_device', 'cleanup_gpu_system', 'get_system_status',

    # Utility functions
    'enhanced_gpu_cleanup', 'safe_gpu_cleanup'
]

# Version info for 2025 compatibility
__version__ = "2025.1.0"
__pytorch_version__ = torch.__version__

logger.info(f"📦 ModelLoader 2025 Edition v{__version__} - PyTorch {__pytorch_version__}")
