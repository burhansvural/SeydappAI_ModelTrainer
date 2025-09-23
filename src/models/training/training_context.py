# src/models/training/training_context.py
"""
Training Context Manager
Following PyTorch training loop patterns[1][2]
"""
import torch
import logging
import threading
from contextlib import contextmanager
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TrainingContext:
    """Thread-safe training context management"""

    def __init__(self, rtx3060_detected: bool):
        self.rtx3060_detected = rtx3060_detected
        self._training_lock = threading.Lock()
        self._training_active = False

    @contextmanager
    def training_session(self):
        """
        Training context following PyTorch patterns[1]
        Manages training state and cleanup
        """
        with self._training_lock:
            self._training_active = True
            model_refs = {}

            try:
                logger.debug("🎯 Training session started")
                yield model_refs

            finally:
                self._training_active = False

                # Cleanup training artifacts[1]
                self._cleanup_training_refs(model_refs)

                # GPU memory cleanup
                if torch.cuda.is_available():
                    self._gpu_cleanup()

                logger.debug("🧹 Training session cleanup completed")

    def _cleanup_training_refs(self, model_refs: Dict[str, Any]):
        """Clean up training references"""
        cleanup_items = ['trainer', 'model', 'optimizer', 'scheduler']

        for item_name in cleanup_items:
            if item_name in model_refs:
                try:
                    item = model_refs[item_name]

                    # Special handling for different types
                    if item_name == 'trainer' and hasattr(item, 'model'):
                        if hasattr(item.model, 'cpu'):
                            item.model = item.model.cpu()
                    elif item_name == 'model' and hasattr(item, 'cpu'):
                        item = item.cpu()

                    del item
                    logger.debug(f"✅ {item_name} cleaned up")

                except Exception as e:
                    logger.warning(f"⚠️ {item_name} cleanup failed: {e}")

        model_refs.clear()

    def _gpu_cleanup(self):
        """GPU-specific cleanup following PyTorch patterns[1]"""
        try:
            # Multi-pass cleanup for RTX 3060
            cleanup_passes = 3 if self.rtx3060_detected else 1

            for i in range(cleanup_passes):
                torch.cuda.empty_cache()
                if i == 0:  # First pass
                    torch.cuda.synchronize()

            # IPC cleanup if available
            if hasattr(torch.cuda, 'ipc_collect'):
                torch.cuda.ipc_collect()

            logger.debug("🧹 GPU cleanup completed")

        except Exception as e:
            logger.warning(f"⚠️ GPU cleanup failed: {e}")

    def is_training_active(self) -> bool:
        """Check if training is currently active"""
        return self._training_active
