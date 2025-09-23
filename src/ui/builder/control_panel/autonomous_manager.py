# src/ui/builder/control_panel/autonomous_manager.py
"""
🤖 Autonomous Learning Manager - Otonom Öğrenme Sistemi Yöneticisi
Bu dosya RTX 3060 için optimize edilmiş otonom öğrenme sistemini yönetir
Python class inheritance ve composition pattern'lerini kullanır[1][4]
"""

import logging
import asyncio
import threading
import time
from typing import List, Dict, Any, Optional
from src.utils.async_logger import async_logger

logger = logging.getLogger(__name__)

# Safe import with fallback
try:
    from src.research.intelligent_web_scraper import create_autonomous_learning_system
except ImportError as import_error:
    logger.error(f"❌ Autonomous scraper import failed: {import_error}")
    create_autonomous_learning_system = None


class AutonomousLearningManager:
    """
    Otonom öğrenme sistemini yöneten ana sınıf

    Bu sınıf Python'ın OOP özelliklerini kullanır[1][4]:
    - Constructor (__init__) ile initialization
    - Instance method'ları (self parametreli)
    - Private method'lar (_underscore ile)
    - Property-like behavior için getter/setter'lar
    """

    def __init__(self, control_panel_instance):
        """
        Autonomous Learning Manager constructor'ı[1]

        Args:
            control_panel_instance: Ana control panel referansı

        Python sınıf özelliklerini kullanır:
        - self ile instance niteliklerini tanımlar[1]
        - Composition pattern ile diğer sınıfları referans eder
        - Thread-safe initialization sağlar
        """
        logger.info("🤖 Initializing AutonomousLearningManager")

        # Ana control panel referansı - composition pattern
        self.control_panel = control_panel_instance

        # Instance nitelikleri[1] - state management için
        self.is_running = False  # Manager aktif mi?
        self.current_topics = []  # Şu anda işlenen topic'ler
        self.processed_count = 0  # İşlenen topic sayısı
        self.total_topics = 0  # Toplam topic sayısı

        # Thread management - RTX 3060 için kritik
        self._worker_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()  # Graceful shutdown için
        self._manager_lock = threading.Lock()  # Thread-safe operations

        # Scraper management - lazy loading
        self._scraper_instance = None
        self._scraper_initialized = False

        # Performance tracking
        self._start_time = 0.0
        self._last_topic_time = 0.0

        logger.info("✅ AutonomousLearningManager initialized")

    def start_learning(self, topics: List[str]) -> bool:
        """
        Otonom öğrenme sürecini başlatan public method[1]

        Args:
            topics: Öğrenilecek konuların listesi

        Returns:
            bool: Başlatma başarılı ise True

        Method özellikleri:
        - Public interface (client code'dan çağrılır)
        - Bool return type ile success/failure indication
        - Thread-safe implementation
        """
        logger.info(f"🚀 Starting autonomous learning with {len(topics)} topics")

        # Input validation
        if not topics:
            logger.warning("⚠️ No topics provided for learning")
            return False

        # Thread-safe state check
        with self._manager_lock:
            if self.is_running:
                logger.warning("⚠️ Autonomous learning already running")
                return False

            # State initialization
            self.is_running = True
            self.current_topics = topics.copy()  # Defensive copy
            self.total_topics = len(topics)
            self.processed_count = 0
            self.control_panel.autonomous_running = True

            # Reset shutdown event
            self._shutdown_event.clear()

            # Performance tracking
            self._start_time = time.time()

        try:
            # Scraper initialization
            if not self._initialize_scraper():
                self._cleanup_failed_start()
                return False

            # Worker thread başlat
            self._start_worker_thread()

            logger.info("✅ Autonomous learning started successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start autonomous learning: {e}")
            self._cleanup_failed_start()
            return False

    def stop_learning(self):
        """
        Otonom öğrenme sürecini durdurma method'u

        Graceful shutdown pattern:
        1. Shutdown event set et
        2. Worker thread'in bitmesini bekle
        3. State'i temizle
        4. Resources'ları release et
        """
        logger.info("⏹️ Stopping autonomous learning")

        with self._manager_lock:
            if not self.is_running:
                logger.debug("Autonomous learning not running, nothing to stop")
                return

            # Shutdown signal gönder
            self._shutdown_event.set()
            self.is_running = False
            self.control_panel.autonomous_running = False

        # Worker thread'in bitmesini bekle (timeout ile)
        if self._worker_thread and self._worker_thread.is_alive():
            logger.info("⏳ Waiting for worker thread to finish...")
            self._worker_thread.join(timeout=10.0)  # 10 saniye timeout

            if self._worker_thread.is_alive():
                logger.warning("⚠️ Worker thread did not finish gracefully")

        # Final cleanup
        self._cleanup_after_stop()

        logger.info("✅ Autonomous learning stopped")

    def emergency_stop(self):
        """
        Emergency stop - immediate shutdown
        Normal stop'tan daha agresif, timeout yok
        """
        logger.warning("🚨 Emergency stop requested")

        with self._manager_lock:
            self._shutdown_event.set()
            self.is_running = False
            self.control_panel.autonomous_running = False

        # Immediate cleanup, thread join'siz
        self._cleanup_after_stop()

        logger.info("✅ Emergency stop completed")

    def get_progress_info(self) -> Dict[str, Any]:
        """
        Current progress information'ı döndüren getter method

        Returns:
            Dict: Progress bilgileri

        Property-like behavior sağlar:
        - Read-only access to internal state
        - Formatted progress data
        - Thread-safe read operations
        """
        with self._manager_lock:
            elapsed_time = time.time() - self._start_time if self._start_time > 0 else 0

            progress_info = {
                'is_running': self.is_running,
                'total_topics': self.total_topics,
                'processed_count': self.processed_count,
                'remaining_topics': self.total_topics - self.processed_count,
                'progress_percentage': (self.processed_count / self.total_topics * 100) if self.total_topics > 0 else 0,
                'elapsed_time': elapsed_time,
                'current_topic': self.current_topics[self.processed_count] if self.processed_count < len(
                    self.current_topics) else None
            }

            return progress_info

    def _initialize_scraper(self) -> bool:
        """
        Web scraper'ı initialize eden private method[1]

        Returns:
            bool: Initialization başarılı ise True

        Private method özellikleri:
        - Underscore ile başlar (_) - internal use[1]
        - Implementation detail'i gizler
        - Sadece sınıf içinden çağrılır
        """
        if self._scraper_initialized and self._scraper_instance:
            logger.debug("Scraper already initialized")
            return True

        try:
            if create_autonomous_learning_system is None:
                logger.error("❌ Scraper factory function not available")
                return False

            # Scraper instance oluştur
            self._scraper_instance = create_autonomous_learning_system()

            if self._scraper_instance:
                self._scraper_initialized = True
                logger.info("✅ Autonomous scraper initialized")
                return True
            else:
                logger.error("❌ Scraper factory returned None")
                return False

        except Exception as e:
            logger.error(f"❌ Scraper initialization failed: {e}")
            return False

    def _start_worker_thread(self):
        """
        Background worker thread'ini başlatan private method

        Thread management pattern:
        - Daemon thread kullanır (main program exit'te otomatik temizlik)
        - Descriptive thread name verir
        - Thread'i active list'e ekler
        """

        def worker_target():
            """Worker thread'in target fonksiyonu"""
            try:
                # Async worker'ı sync context'te çalıştır
                asyncio.run(self._async_learning_worker())
            except Exception as e:
                logger.error(f"❌ Worker thread failed: {e}")
            finally:
                logger.info("🏁 Worker thread finished")

        # Worker thread oluştur
        self._worker_thread = threading.Thread(
            target=worker_target,
            name=f"AutonomousLearning-{int(time.time())}",
            daemon=True
        )

        # Thread'i active list'e ekle
        self.control_panel.active_threads.append(self._worker_thread)

        # Thread'i başlat
        self._worker_thread.start()

        logger.info("✅ Autonomous learning worker thread started")

    async def _async_learning_worker(self):
        """
        Ana öğrenme loop'unu çalıştıran async method

        Async pattern özellikleri:
        - await keyword'leri ile non-blocking operations
        - asyncio.sleep ile cooperative multitasking
        - Exception handling ile error tolerance
        - Graceful shutdown support
        """
        logger.info("🤖 Async learning worker started")

        try:
            for topic_index, topic in enumerate(self.current_topics):
                # Shutdown check - graceful exit
                if self._shutdown_event.is_set():
                    logger.info("🛑 Learning stopped by user request")
                    break

                # Progress update
                self.processed_count = topic_index
                self._last_topic_time = time.time()

                logger.info(f"🔍 Processing topic {topic_index + 1}/{self.total_topics}: {topic}")

                try:
                    # Research ve training sürecini başlat
                    await self._process_single_topic(topic)

                    # Success feedback
                    logger.info(f"✅ Completed topic: {topic}")

                    # Inter-topic delay - RTX 3060 için cooling time
                    if not self._shutdown_event.is_set():
                        await asyncio.sleep(3.0)  # 3 saniye ara

                except Exception as topic_error:
                    logger.error(f"❌ Topic processing failed: {topic} - {topic_error}")

                    # Continue with next topic despite error
                    continue

            # Final progress update
            self.processed_count = len(self.current_topics)

            logger.info(f"🎯 Learning completed: {self.processed_count}/{self.total_topics} topics")

        except asyncio.CancelledError:
            logger.info("🛑 Async learning worker cancelled")
        except Exception as e:
            logger.error(f"❌ Async learning worker failed: {e}")
        finally:
            # Final cleanup
            await self._async_cleanup()

    async def _process_single_topic(self, topic: str):
        """
        Tek bir topic'i işleyen async method

        Args:
            topic: İşlenecek topic string'i

        Processing pipeline:
        1. Research examples generation
        2. Training data preparation
        3. Model training trigger
        4. Result validation
        """
        logger.info(f"🔬 Starting research for topic: {topic}")

        try:
            # 1. Research phase - examples generation
            examples = await self._scraper_instance.research_and_generate_examples(topic)

            if not examples:
                logger.warning(f"⚠️ No examples generated for topic: {topic}")
                return

            logger.info(f"✅ Generated {len(examples)} examples for: {topic}")

            # 2. Training phase - trigger model training
            self._trigger_training_for_topic(examples, topic)

            # 3. Success logging
            async_logger.info(f"🎯 Successfully processed topic: {topic} with {len(examples)} examples")

        except Exception as e:
            logger.error(f"❌ Single topic processing failed: {topic} - {e}")
            raise  # Re-raise to handle at caller level

    def _trigger_training_for_topic(self, examples: List[Dict], topic: str):
        """
        Topic için training'i tetikleyen method

        Args:
            examples: Training examples listesi
            topic: Topic adı

        Training coordination:
        - Training coordinator'ı kullanır
        - Thread-safe training queue
        - RTX 3060 memory management
        """
        try:
            # Training coordinator üzerinden training tetikle
            if hasattr(self.control_panel, 'training_coordinator'):
                self.control_panel.training_coordinator.queue_training(examples, topic)
            else:
                logger.warning("⚠️ Training coordinator not available")

        except Exception as e:
            logger.error(f"❌ Training trigger failed for {topic}: {e}")

    def _cleanup_failed_start(self):
        """Başlatma başarısızlığında cleanup yapan method"""
        with self._manager_lock:
            self.is_running = False
            self.control_panel.autonomous_running = False
            self.current_topics = []
            self.processed_count = 0
            self.total_topics = 0

    def _cleanup_after_stop(self):
        """Stop sonrası cleanup yapan method"""
        with self._manager_lock:
            self.current_topics = []
            self.processed_count = 0
            self.total_topics = 0
            self._start_time = 0.0
            self._last_topic_time = 0.0

    async def _async_cleanup(self):
        """Async cleanup operations"""
        try:
            # Scraper cleanup if needed
            if hasattr(self._scraper_instance, 'cleanup'):
                await self._scraper_instance.cleanup()

            logger.info("✅ Async cleanup completed")

        except Exception as e:
            logger.debug(f"Async cleanup error: {e}")
