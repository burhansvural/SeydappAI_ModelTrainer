# src/models/memory/oom_handler.py
"""Out of Memory Error Handler"""
import torch
import logging
import gc
from typing import Dict, Any

logger = logging.getLogger(__name__)


class OOMHandler:
    """RTX 3060 OOM error recovery system"""

    def __init__(self, rtx3060_detected: bool):
        self.rtx3060_detected = rtx3060_detected
        self._oom_recovery_active = False

    def handle_oom_error(self, memory_info: Dict[str, Any] = None):
        """Handle CUDA OOM error with recovery strategies"""
        if self._oom_recovery_active:
            logger.warning("⚠️ OOM recovery already in progress")
            return

        logger.error("❌ CUDA Out of Memory error detected")

        try:
            self._oom_recovery_active = True

            # Stage 1: Basic cleanup
            torch.cuda.empty_cache()
            gc.collect()

            # Stage 2: Get memory status
            if memory_info is None:
                try:
                    allocated = torch.cuda.memory_allocated(0) / 1024 ** 3
                    reserved = torch.cuda.memory_reserved(0) / 1024 ** 3
                    memory_info = {'allocated': allocated, 'reserved': reserved}
                except:
                    memory_info = {'allocated': 0, 'reserved': 0}

            logger.warning(f"💾 Memory status: {memory_info}")

            # Stage 3: RTX 3060 specific recovery
            if self.rtx3060_detected:
                self._rtx3060_recovery_strategy(memory_info)

            # Stage 4: Final cleanup
            if torch.cuda.is_available():
                torch.cuda.synchronize()
                torch.cuda.empty_cache()

            logger.info("✅ OOM recovery completed")

        except Exception as e:
            logger.error(f"❌ OOM recovery failed: {e}")
        finally:
            self._oom_recovery_active = False

    def _rtx3060_recovery_strategy(self, memory_info: Dict[str, Any]):
        """RTX 3060 specific recovery strategies"""
        allocated = memory_info.get('allocated', 0)

        if allocated > 8.0:  # > 8GB on 12GB card
            logger.warning("🎮 RTX 3060 critical memory level - applying aggressive recovery")

            # Multiple cache clearing passes
            for i in range(3):
                torch.cuda.empty_cache()
                gc.collect()
                logger.debug(f"🧹 Recovery pass #{i + 1}")

            # IPC memory cleanup if available
            if hasattr(torch.cuda, 'ipc_collect'):
                torch.cuda.ipc_collect()
                logger.debug("🧹 IPC memory cleanup completed")

    def is_recovery_active(self) -> bool:
        """Check if OOM recovery is currently active"""
        return self._oom_recovery_active

    def get_recovery_suggestions(self) -> list:
        """Get suggestions for preventing future OOM errors"""
        suggestions = [
            "Reduce batch size to 1",
            "Enable gradient checkpointing",
            "Use 4-bit quantization",
            "Reduce model size or use smaller variant"
        ]

        if self.rtx3060_detected:
            suggestions.extend([
                "Use max_split_size_mb=32 for RTX 3060",
                "Set memory fraction to 0.75",
                "Consider using gradient accumulation"
            ])

        return suggestions
