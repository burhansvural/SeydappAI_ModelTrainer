# src/models/core/device_manager.py
"""Device management following PyTorch patterns[1]"""
import torch
import os
import logging

logger = logging.getLogger(__name__)


class DeviceManager:
    """Centralized device and memory management"""

    def __init__(self, rtx3060_detected: bool):
        self.rtx3060_detected = rtx3060_detected
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._apply_device_optimizations()

    def _apply_device_optimizations(self):
        """Apply device-specific optimizations"""
        if not self.rtx3060_detected or self.device.type != 'cuda':
            return

        try:
            # RTX 3060 memory optimizations
            torch.cuda.set_per_process_memory_fraction(0.75)
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:32'

            # Enable memory recording for debugging[1]
            if hasattr(torch.cuda.memory, '_record_memory_history'):
                torch.cuda.memory._record_memory_history()

            logger.info("🔧 RTX 3060 device optimizations applied")

        except Exception as e:
            logger.warning(f"⚠️ Device optimization failed: {e}")

    def get_device(self) -> torch.device:
        """Get optimal device for operations"""
        return self.device

    def is_rtx3060(self) -> bool:
        """Check if RTX 3060 is detected"""
        return self.rtx3060_detected
