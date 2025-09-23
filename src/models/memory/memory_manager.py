# src/models/memory/memory_manager.py
"""
Memory Management Module
Following PyTorch checkpoint patterns[1]
"""
import torch
import threading
import time
import logging
import gc
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class MemoryManager:
    """RTX 3060 optimized memory management"""

    def __init__(self, rtx3060_detected: bool):
        self.rtx3060_detected = rtx3060_detected
        self._memory_monitor_active = False
        self._training_active = False
        self._last_oom_time = 0
        self._training_lock = threading.Lock()
        self._power_management_active = False
        self._min_power_limit = 100

        if rtx3060_detected:
            self._setup_rtx3060_monitoring()

    def _setup_rtx3060_monitoring(self):
        """Setup RTX 3060 specific monitoring"""
        logger.info("🔍 Setting up RTX 3060 memory monitoring")
        # Memory monitoring will be activated during training

    def start_memory_monitoring(self):
        """Start background memory monitoring"""
        if not self.rtx3060_detected or self._memory_monitor_active:
            return

        self._memory_monitor_active = True
        logger.info("🔍 RTX 3060 memory monitoring started")

        def monitor():
            try:
                while self._memory_monitor_active:
                    if not self._training_active:
                        time.sleep(5)
                        continue

                    memory_info = self.get_memory_info()

                    # Critical memory level check
                    if memory_info.get('utilization', 0) > 85:
                        logger.warning(f"⚠️ High memory usage: {memory_info['utilization']:.1f}%")

                        with self._training_lock:
                            if time.time() - self._last_oom_time > 300:  # 5 min cooldown
                                self._emergency_cleanup()
                                self._last_oom_time = time.time()

                    time.sleep(2)

            except Exception as e:
                logger.error(f"❌ Memory monitoring error: {e}")
            finally:
                self._memory_monitor_active = False

        threading.Thread(target=monitor, daemon=True).start()

    def _emergency_cleanup(self):
        """Emergency memory cleanup for RTX 3060"""
        logger.warning("🚨 Emergency memory cleanup triggered")

        try:
            torch.cuda.empty_cache()
            gc.collect()

            # Power management if enabled
            if self._power_management_active:
                import os
                os.system(f"nvidia-smi -i 0 -pl {self._min_power_limit}")
                logger.info(f"🔋 Power limit reduced to {self._min_power_limit}W")

        except Exception as e:
            logger.error(f"❌ Emergency cleanup failed: {e}")

    def get_memory_info(self) -> Dict[str, float]:
        """Get detailed memory information"""
        if not torch.cuda.is_available():
            return {'message': 'CUDA not available'}

        try:
            allocated = torch.cuda.memory_allocated(0) / 1024 ** 3  # GB
            reserved = torch.cuda.memory_reserved(0) / 1024 ** 3  # GB
            total = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3  # GB

            return {
                'allocated': round(allocated, 2),
                'reserved': round(reserved, 2),
                'total': round(total, 2),
                'free': round(total - reserved, 2),
                'utilization': round((allocated / total) * 100, 1)
            }
        except Exception as e:
            return {'error': str(e)}

    def set_training_active(self, active: bool):
        """Set training status for monitoring"""
        self._training_active = active

    def stop_monitoring(self):
        """Stop memory monitoring"""
        self._memory_monitor_active = False
        logger.info("⏹️ Memory monitoring stopped")
