# src/models/core/gpu_detector.py
"""
RTX 3060 GPU Detection Module
PyTorch model organization following CS230 patterns[2]
"""
import torch
import logging

logger = logging.getLogger(__name__)


class GPUDetector:
    """GPU detection and hardware analysis"""

    @staticmethod
    def detect_rtx3060() -> bool:
        """Detect RTX 3060 GPU with comprehensive checking"""
        try:
            if not torch.cuda.is_available():
                logger.info("🖥️ CUDA not available - using CPU")
                return False

            device_name = torch.cuda.get_device_name(0).lower()
            rtx3060_variants = [
                'rtx 3060', 'geforce rtx 3060', 'rtx3060',
                'rtx 3060 ti', 'rtx 3060 laptop', 'rtx 3060 mobile'
            ]

            is_rtx3060 = any(variant in device_name for variant in rtx3060_variants)

            if is_rtx3060:
                logger.info(f"🎮 RTX 3060 family detected: {device_name}")
                logger.info(f"📊 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024 ** 3:.1f}GB")
            else:
                logger.info(f"🖥️ GPU detected: {device_name}")

            return is_rtx3060

        except Exception as e:
            logger.warning(f"⚠️ GPU detection failed: {e}")
            return False

    @staticmethod
    def get_gpu_info() -> dict:
        """Get comprehensive GPU information"""
        if not torch.cuda.is_available():
            return {'available': False, 'message': 'CUDA not available'}

        try:
            props = torch.cuda.get_device_properties(0)
            return {
                'available': True,
                'name': props.name,
                'total_memory': props.total_memory / 1024 ** 3,  # GB
                'major': props.major,
                'minor': props.minor,
                'multi_processor_count': props.multi_processor_count
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}
