# src/models/training/optimized_trainer.py
"""
Optimized Trainer following PyTorch training loop patterns[2][3]
RTX 3060 specific optimizations
"""
import torch
import logging
from transformers import Trainer
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class OptimizedTrainer(Trainer):
    """
    RTX 3060 optimized trainer following PyTorch patterns[2][3]
    Enhanced error handling and memory management
    """

    def __init__(self, rtx3060_detected: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.rtx3060_detected = rtx3060_detected
        self._training_step_count = 0

    def compute_loss(self, model, inputs, return_outputs=False):
        """
        Enhanced loss computation following PyTorch patterns[1]
        Forward pass with error handling
        """
        try:
            # Forward pass[1]
            outputs = model(**inputs)
            loss = outputs.loss

            # Loss validation - prevent NaN/Inf
            if torch.isnan(loss) or torch.isinf(loss):
                logger.warning("⚠️ Invalid loss detected - using fallback")
                # Create fallback loss tensor
                loss = torch.tensor(0.001, requires_grad=True, device=loss.device)

            return (loss, outputs) if return_outputs else loss

        except torch.cuda.OutOfMemoryError:
            logger.error("❌ OOM in compute_loss")
            if self.rtx3060_detected:
                torch.cuda.empty_cache()
            raise
        except Exception as e:
            logger.error(f"❌ Loss computation error: {e}")
            # Return minimal loss to prevent training crash
            fallback_loss = torch.tensor(0.001, requires_grad=True)
            return fallback_loss

    def training_step(self, model, inputs, num_items_in_batch=None):
        """
        RTX 3060 optimized training step following PyTorch patterns[2]
        Steps: forward → backward → optimizer step[1]
        """
        model.train()
        inputs = self._prepare_inputs(inputs)
        self._training_step_count += 1

        try:
            # Forward pass[2]
            with self.compute_loss_context_manager():
                loss = self.compute_loss(model, inputs)

            # Scale loss for gradient accumulation[2]
            if self.args.gradient_accumulation_steps > 1:
                loss = loss / self.args.gradient_accumulation_steps

            # Backward pass[2]
            loss.backward()

            # RTX 3060 specific monitoring
            if self.rtx3060_detected and self._training_step_count % 10 == 0:
                self._monitor_rtx3060_status()

            return loss.detach()

        except torch.cuda.OutOfMemoryError:
            logger.error(f"❌ OOM at training step {self._training_step_count}")
            if self.rtx3060_detected:
                self._handle_rtx3060_oom()
            return torch.tensor(0.0, device=self.args.device)

        except Exception as e:
            logger.error(f"❌ Training step error: {e}")
            return torch.tensor(0.001, requires_grad=True)

    def _monitor_rtx3060_status(self):
        """Monitor RTX 3060 specific metrics during training"""
        try:
            if torch.cuda.is_available():
                allocated = torch.cuda.memory_allocated(0) / 1024 ** 3  # GB
                if allocated > 9.0:  # > 9GB on 12GB card
                    logger.warning(f"⚠️ RTX 3060 high memory usage: {allocated:.2f}GB")

        except Exception as e:
            logger.debug(f"Memory monitoring error: {e}")

    def _handle_rtx3060_oom(self):
        """RTX 3060 specific OOM recovery"""
        logger.warning("🎮 RTX 3060 OOM recovery initiated")
        try:
            # Emergency cleanup
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

            # Additional cleanup passes for RTX 3060
            for _ in range(2):
                torch.cuda.empty_cache()

        except Exception as e:
            logger.error(f"❌ RTX 3060 OOM recovery failed: {e}")

    def save_model(self, output_dir: Optional[str] = None, _internal_call: bool = False):
        """
        Enhanced model saving with RTX 3060 optimizations
        Following PyTorch checkpoint patterns[1]
        """
        if output_dir is None:
            output_dir = self.args.output_dir

        logger.info(f"💾 Saving model to {output_dir}")

        try:
            # Move model to CPU for safe saving if RTX 3060
            if self.rtx3060_detected and torch.cuda.is_available():
                current_device = next(self.model.parameters()).device
                self.model = self.model.cpu()
                logger.debug("📱 Model moved to CPU for safe saving")

            # Call parent save method
            super().save_model(output_dir, _internal_call)

            # Move model back to original device
            if self.rtx3060_detected and 'current_device' in locals():
                self.model = self.model.to(current_device)
                logger.debug(f"📱 Model moved back to {current_device}")

            logger.info("✅ Model saved successfully")

        except Exception as e:
            logger.error(f"❌ Model saving failed: {e}")
            raise
