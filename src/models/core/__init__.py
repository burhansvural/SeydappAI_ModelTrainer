# src/models/core/__init__.py
"""Core GPU detection and device management"""
from .gpu_detector import GPUDetector
from .device_manager import DeviceManager

__all__ = ['GPUDetector', 'DeviceManager']
