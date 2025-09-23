# src/ui/builder/control_panel/control_panel_base.py
"""
🎮 Control Panel - Temel Sınıf ve Konfigürasyon
Bu dosya control panel'in temel yapısını ve konfigürasyonunu içerir
"""

import flet as ft
import logging
import threading
import atexit  # ✅ Shutdown hook için ekleyin
import signal  # ✅ Signal handling için ekleyin
import sys     # ✅ System operations için ekleyin
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ControlPanelConfig:
    """
    Control Panel konfigürasyon sınıfı
    RTX 3060 için optimize edilmiş varsayılan değerler
    """
    max_learning_cycles: int = 10  # Maksimum öğrenme döngüsü
    cycle_duration_seconds: int = 60  # Her döngü süresi (saniye)
    research_depth: str = 'detailed'  # Araştırma derinliği
    max_concurrent_threads: int = 3  # RTX 3060 için güvenli thread sayısı
    memory_cleanup_interval: int = 30  # Bellek temizlik aralığı (saniye)


class ControlPanelBase:
    """
    Control Panel'in temel sınıfı
    Tüm diğer bileşenler bu sınıfı inherit eder
    """

    def __init__(self, log_system, dashboard_cards, config: Optional[Dict] = None):
        """
        Temel sınıfın constructor'ı

        Args:
            log_system: Event loglama sistemi
            dashboard_cards: Dashboard widget'ları
            config: Konfigürasyon dictionary'si
        """
        logger.info("🔧 Initializing ControlPanelBase")

        # Sistem referansları
        self.log_system = log_system
        self.dashboard_cards = dashboard_cards
        self.page: ft.Page = None

        # Konfigürasyon yükleme
        self.config = self._load_configuration(config)

        # State management
        self.autonomous_running = False
        self.research_running = False
        self._shutdown_requested = False  # ✅ Shutdown flag ekleyin

        # Thread management - RTX 3060 için sınırlı
        self.active_threads: List[threading.Thread] = []
        self._thread_lock = threading.Lock()

        # UI referansları - None safety
        self.status_text = None
        self.progress_bar = None
        self.controls_container = None

        # ✅ Shutdown hooks registration[1]
        self._register_shutdown_hooks()

        logger.info("✅ ControlPanelBase initialized")

    def _register_shutdown_hooks(self):
        """Shutdown hook'larını register eden method[1]"""
        try:
            # atexit ile normal shutdown hook[1]
            atexit.register(self._cleanup_on_exit)
            logger.debug("✅ atexit shutdown hook registered")

            # Signal handlers for graceful shutdown[4]
            if hasattr(signal, 'SIGINT'):
                signal.signal(signal.SIGINT, self._signal_handler)
                logger.debug("✅ SIGINT handler registered")

            if hasattr(signal, 'SIGTERM'):
                signal.signal(signal.SIGTERM, self._signal_handler)
                logger.debug("✅ SIGTERM handler registered")

        except Exception as e:
            logger.warning(f"⚠️ Shutdown hook registration failed: {e}")

    def _signal_handler(self, signum, frame):
        """Signal handler for graceful shutdown[4]"""
        logger.info(f"📡 Received signal {signum}, initiating graceful shutdown...")

        # Shutdown flag set et
        self._shutdown_requested = True

        # Cleanup çağır
        self._cleanup_all_resources()

        # Graceful exit
        logger.info("👋 Graceful shutdown completed")
        sys.exit(0)

    def _cleanup_on_exit(self):
        """atexit tarafından çağrılan cleanup function[1]"""
        if self._shutdown_requested:
            logger.debug("Cleanup already performed via signal handler")
            return

        logger.info("🧹 Application normal exit - starting cleanup...")
        self._cleanup_all_resources()
        logger.info("✅ Normal exit cleanup completed")

    def _cleanup_all_resources(self):
        """Comprehensive resource cleanup[4]"""
        logger.info("🧹 Starting comprehensive resource cleanup")

        try:
            # 1. Set shutdown flags
            self._shutdown_requested = True
            self.autonomous_running = False
            self.research_running = False

            # 2. Stop progress monitor
            if hasattr(self, 'progress_monitor') and self.progress_monitor:
                logger.info("🛑 Stopping progress monitor...")
                self.progress_monitor.stop_monitoring()

            # 3. Stop autonomous manager
            if hasattr(self, 'autonomous_manager') and self.autonomous_manager:
                logger.info("🛑 Stopping autonomous manager...")
                if hasattr(self.autonomous_manager, 'stop'):
                    self.autonomous_manager.stop()

            # 4. Stop training coordinator
            if hasattr(self, 'training_coordinator') and self.training_coordinator:
                logger.info("🛑 Stopping training coordinator...")
                if hasattr(self.training_coordinator, 'stop'):
                    self.training_coordinator.stop()

            # 5. Clean all threads
            logger.info("🧹 Cleaning up threads...")
            self._cleanup_all_threads()

            # 6. GPU memory cleanup
            logger.info("🎮 GPU memory cleanup...")
            self._force_gpu_cleanup()

            # 7. UI cleanup
            if self.page:
                logger.info("🖥️ UI cleanup...")
                try:
                    self.page.close()
                except:
                    pass  # Silent fail for UI cleanup

            logger.info("✅ Resource cleanup completed successfully")

        except Exception as e:
            logger.error(f"❌ Resource cleanup error: {e}")

    def _cleanup_all_threads(self):
        """Enhanced thread cleanup[4]"""
        logger.info(f"🧹 Cleaning up {len(self.active_threads)} threads...")

        with self._thread_lock:
            # Give threads a chance to finish gracefully
            for thread in self.active_threads[:]:
                if thread.is_alive():
                    logger.debug(f"⏳ Waiting for thread: {thread.name}")
                    thread.join(timeout=2.0)  # 2 second timeout

                    if thread.is_alive():
                        logger.warning(f"⚠️ Thread {thread.name} didn't stop gracefully")

            # Clear the list
            cleaned_count = len(self.active_threads)
            self.active_threads.clear()

            logger.info(f"✅ {cleaned_count} threads cleaned up")

        # Force garbage collection
        import gc
        gc.collect()

    def _force_gpu_cleanup(self):
        """GPU memory cleanup - RTX 3060 specific"""
        try:
            # Import here to avoid dependency issues
            from src.models.model_loader import force_gpu_cleanup
            cleanup_success = force_gpu_cleanup()

            if cleanup_success:
                logger.info("✅ GPU cleanup successful")
            else:
                logger.warning("⚠️ GPU cleanup had issues")

        except ImportError:
            logger.debug("GPU cleanup module not available")
        except Exception as e:
            logger.warning(f"⚠️ GPU cleanup error: {e}")

    def emergency_stop_all(self):
        """Emergency stop - immediate shutdown[4]"""
        logger.warning("🚨 EMERGENCY STOP - Immediate shutdown initiated")

        try:
            # Set emergency flags
            self._shutdown_requested = True

            # Quick cleanup
            self._cleanup_all_resources()

            # Force exit after timeout
            import os
            logger.warning("🚨 Force exit in 3 seconds...")
            threading.Timer(3.0, lambda: os._exit(0)).start()

        except Exception as e:
            logger.error(f"❌ Emergency stop error: {e}")
            import os
            os._exit(1)  # Force exit with error code

    # ✅ Shutdown durumu kontrol metodu ekleyin
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested"""
        return self._shutdown_requested

    def _load_configuration(self, config: Optional[Dict]) -> ControlPanelConfig:
        """
        Konfigürasyon yükleme ve doğrulama[2]

        Args:
            config: Kullanıcı konfigürasyon dictionary'si

        Returns:
            ControlPanelConfig: Doğrulanmış konfigürasyon objesi
        """
        if config:
            return ControlPanelConfig(
                max_learning_cycles=config.get('max_cycles', 10),
                cycle_duration_seconds=config.get('cycle_duration_seconds', 60),
                research_depth=config.get('research_depth', 'detailed'),
                max_concurrent_threads=config.get('max_threads', 3),
                memory_cleanup_interval=config.get('cleanup_interval', 30)
            )
        else:
            # RTX 3060 için güvenli varsayılan değerler
            return ControlPanelConfig()

    def cleanup_threads(self):
        """
        Bitmiş thread'leri temizleme[3]
        RTX 3060 bellek optimizasyonu için önemli
        """
        # Shutdown check
        if self._shutdown_requested:
            logger.debug("Shutdown requested, skipping thread cleanup")
            return

        with self._thread_lock:
            # Canlı thread'leri filtrele
            alive_threads = [t for t in self.active_threads if t.is_alive()]

            # Bitmiş thread sayısını logla
            cleaned_count = len(self.active_threads) - len(alive_threads)
            if cleaned_count > 0:
                logger.info(f"🧹 {cleaned_count} finished thread cleaned")

            # Liste'yi güncelle
            self.active_threads = alive_threads

            # Garbage collection tetikle
            import gc
            gc.collect()

    def safe_page_update(self):
        """Thread-safe page update[1][4]"""
        try:
            if self.page and not getattr(self.page, '_closed', False):
                # ✅ Search results[1]: Essential for UI sync
                self.page.update()
                logger.debug("✅ Page updated successfully")
            else:
                logger.debug("⚠️ Page not available for update")
        except Exception as e:
            logger.debug(f"❌ Page update failed: {e}")
