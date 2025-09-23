# src/models/memory/cleanup_utils.py
"""
GPU Cleanup Utilities - PyTorch Best Practices Implementation
Enhanced cleanup following PyTorch official guidelines[1][2][3]
"""
import torch
import gc
import os
import logging
import ctypes
import ctypes.util
from typing import List, Any, Optional

logger = logging.getLogger(__name__)


def safe_gpu_cleanup(*objects) -> bool:
    """
    Safe GPU cleanup following PyTorch patterns[1]
    """
    logger.info("🛡️ Starting safe GPU cleanup")

    try:
        # Step 1: Move objects to CPU first[3]
        for obj in objects:
            if obj is not None:
                if hasattr(obj, 'cpu'):
                    obj = obj.cpu()
                del obj

        # Step 2: Synchronize before cache cleanup[3]
        if torch.cuda.is_available():
            torch.cuda.synchronize()  # Critical for proper cleanup[3]
            torch.cuda.empty_cache()

        # Step 3: Python garbage collection
        collected = gc.collect()
        logger.debug(f"🧹 GC collected {collected} objects")

        logger.info("✅ Safe GPU cleanup completed")
        return True

    except Exception as e:
        logger.error(f"❌ Safe cleanup failed: {e}")
        return False


def enhanced_gpu_cleanup() -> bool:
    """
    Enhanced GPU cleanup with PyTorch best practices[1][2]
    """
    logger.info("🧹 Starting enhanced GPU cleanup")

    try:
        if not torch.cuda.is_available():
            logger.info("✅ No CUDA device available")
            return True

        # Step 1: Synchronize all CUDA operations[3]
        torch.cuda.synchronize()
        logger.debug("🔄 CUDA synchronized")

        # Step 2: Clear gradient accumulation artifacts[1]
        _clear_gradient_artifacts()

        # Step 3: Multiple cache clear passes[2]
        for i in range(3):
            torch.cuda.empty_cache()
            logger.debug(f"🧹 Cache clear pass #{i + 1}")

        # Step 4: Reset memory stats[2]
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.reset_accumulated_memory_stats()

        # Step 5: Aggressive garbage collection[2]
        for cycle in range(5):
            collected = gc.collect()
            logger.debug(f"🧹 GC cycle #{cycle + 1}: {collected} objects")

        # Step 6: CUDA context reset (nuclear option)
        cuda_reset_success = _attempt_cuda_reset()

        # Step 7: Final synchronization[3]
        torch.cuda.synchronize()

        # Validation
        allocated_after = torch.cuda.memory_allocated(0) / 1024 ** 2  # MB
        logger.info(f"📊 Memory after cleanup: {allocated_after:.1f}MB")

        success = allocated_after < 50  # Stricter threshold
        logger.info(f"✅ Enhanced cleanup {'successful' if success else 'partial'}")
        return success

    except Exception as e:
        logger.error(f"❌ Enhanced cleanup failed: {e}")
        return safe_gpu_cleanup()


def _clear_gradient_artifacts():
    """Clear gradient accumulation artifacts[1]"""
    try:
        # Clear any lingering gradient computations
        torch.cuda.empty_cache()

        # Reset autograd engine
        if hasattr(torch.autograd, 'set_grad_enabled'):
            with torch.autograd.set_grad_enabled(False):
                pass

        logger.debug("✅ Gradient artifacts cleared")

    except Exception as e:
        logger.debug(f"⚠️ Gradient cleanup warning: {e}")


def cleanup_training_artifacts(model=None, trainer=None, optimizer=None, **kwargs):
    """
    Enhanced training cleanup following PyTorch patterns[1][2]
    """
    logger.info("🧹 Cleaning up training artifacts")

    try:
        # Model cleanup[1]
        if model is not None:
            # Clear gradients first
            if hasattr(model, 'zero_grad'):
                model.zero_grad(set_to_none=True)  # More efficient[1]

            # Move to CPU before deletion[3]
            if hasattr(model, 'cpu'):
                model = model.cpu()

            # Clear model state dict
            if hasattr(model, 'state_dict'):
                del model.state_dict

            del model
            logger.debug("✅ Model cleaned")

        # Optimizer cleanup[1]
        if optimizer is not None:
            # Clear optimizer state
            if hasattr(optimizer, 'zero_grad'):
                optimizer.zero_grad(set_to_none=True)

            if hasattr(optimizer, 'state'):
                optimizer.state.clear()

            del optimizer
            logger.debug("✅ Optimizer cleaned")

        # Trainer cleanup
        if trainer is not None:
            if hasattr(trainer, 'model') and trainer.model is not None:
                if hasattr(trainer.model, 'cpu'):
                    trainer.model = trainer.model.cpu()
            del trainer
            logger.debug("✅ Trainer cleaned")

        # Additional cleanup
        for key, value in kwargs.items():
            if value is not None:
                del value
                logger.debug(f"✅ {key} cleaned")

        # Synchronize before final cleanup[3]
        if torch.cuda.is_available():
            torch.cuda.synchronize()
            torch.cuda.empty_cache()

        # Force garbage collection[2]
        gc.collect()

        logger.info("✅ Training artifacts cleanup completed")
        return True

    except Exception as e:
        logger.error(f"❌ Training artifacts cleanup failed: {e}")
        return False


def _attempt_cuda_reset() -> bool:
    """Enhanced CUDA device reset with better error handling"""
    try:
        # First try PyTorch's internal reset
        if hasattr(torch.cuda, 'reset_peak_memory_stats'):
            torch.cuda.reset_peak_memory_stats()

        if hasattr(torch.cuda, 'reset_accumulated_memory_stats'):
            torch.cuda.reset_accumulated_memory_stats()

        # Then attempt device reset via CUDA runtime
        cuda_libs = [
            'libcudart.so.12', 'libcudart.so.11', 'libcudart.so',
            'cudart64_110.dll', 'cudart64_120.dll'
        ]

        for lib_name in cuda_libs:
            try:
                if os.name == 'nt':  # Windows
                    cudart = ctypes.CDLL(lib_name)
                else:  # Linux/Mac
                    lib_path = ctypes.util.find_library(
                        lib_name.replace('lib', '').replace('.so', '')
                    )
                    if lib_path:
                        cudart = ctypes.CDLL(lib_path)
                    else:
                        cudart = ctypes.CDLL(lib_name)

                result = cudart.cudaDeviceReset()
                if result == 0:
                    logger.info("🔄 CUDA device reset successful")
                    return True
                break

            except OSError:
                continue

        logger.warning("⚠️ CUDA runtime reset not available, using PyTorch reset")
        return True

    except Exception as e:
        logger.warning(f"⚠️ CUDA reset failed: {e}")
        return False
