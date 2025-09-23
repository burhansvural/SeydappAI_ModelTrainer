# src/utils/async_logger.py
"""
🚀 AsyncLogger - Search results [1][2] best practices
Non-blocking logging for asyncio applications
"""

import logging
import asyncio
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import flet as ft


class AsyncLogger:
    """
    Search results [2] - QueueHandler/QueueListener approach
    Search results [1] - Non-blocking asyncio logging
    """

    def __init__(self, name: str = "AsyncLogger"):
        self.logger = logging.getLogger(name)

        # Search results [2] - QueueHandler for non-blocking logging
        self.log_queue = queue.Queue()
        self.queue_handler = logging.handlers.QueueHandler(self.log_queue)

        # Search results [1] - Separate thread for logs
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="AsyncLogger")
        self.queue_listener = None
        self._setup_logging()

    def _setup_logging(self):
        """Search results [2] - QueueListener setup"""
        # Console handler for queue listener
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
        )

        # Search results [2] - QueueListener in separate thread
        self.queue_listener = logging.handlers.QueueListener(
            self.log_queue, console_handler, respect_handler_level=True
        )
        self.queue_listener.start()

        # Add queue handler to logger
        self.logger.addHandler(self.queue_handler)
        self.logger.setLevel(logging.INFO)

    def log_async(self, level: int, message: str):
        """Search results [1] - Log without blocking"""
        self.logger.log(level, message)

    def info(self, message: str):
        self.log_async(logging.INFO, message)

    def error(self, message: str):
        self.log_async(logging.ERROR, message)

    def warning(self, message: str):
        self.log_async(logging.WARNING, message)

    def debug(self, message: str):
        self.log_async(logging.DEBUG, message)

    def cleanup(self):
        """Cleanup resources"""
        if self.queue_listener:
            self.queue_listener.stop()
        self.executor.shutdown(wait=True)


# Global async logger instance
async_logger = AsyncLogger("ControlPanel")
