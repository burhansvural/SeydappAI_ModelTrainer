# src/ui/builder/control_panel/progress_monitor.py
"""
📊 Progress Monitor - RTX 3060 için İlerleme Takip Sistemi
Bu dosya sistem kaynaklarını izler ve UI progress güncellemelerini yapar
Memory-aware monitoring ile RTX 3060 optimizasyonları sağlar
"""

import logging
import threading
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ProgressMonitor:
    """
    RTX 3060 için memory-aware progress monitoring sınıfı[1]

    Python sınıf özellikleri[1][2]:
    - __init__ constructor ile initialization
    - Instance nitelikleri ile state management[2]
    - Method'lar ile monitoring behavior[1]
    - Thread-safe operations ile concurrent monitoring
    """

    def __init__(self, control_panel_instance):
        """
        Progress Monitor constructor'ı[1]

        Args:
            control_panel_instance: Ana control panel referansı
        """
        logger.info("📊 Initializing ProgressMonitor")

        # Ana control panel referansı
        self.control_panel = control_panel_instance

        # Instance nitelikleri[2] - monitoring state
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()

        # Memory monitoring settings - RTX 3060 specific
        self.memory_warning_threshold = 85  # %85 RAM usage
        self.memory_critical_threshold = 95  # %95 RAM usage
        self.monitoring_interval = 2.0  # 2 saniye interval

        # Statistics
        self.monitoring_cycles = 0
        self.memory_warnings_count = 0
        self.cleanup_triggers_count = 0

        self._stop_requested = False

        logger.info("✅ ProgressMonitor initialized")

    def stop_monitoring(self):
        """Progress monitoring'i durduran method"""
        logger.info("⏹️ Stopping progress monitoring")

        if not self.is_monitoring:
            logger.debug("Progress monitoring not active")
            return

        # ✅ Stop flag set et
        self._stop_requested = True
        self._shutdown_event.set()
        self.is_monitoring = False

        # Monitor thread'in bitmesini bekle
        if self.monitor_thread and self.monitor_thread.is_alive():
            logger.info("Waiting for monitor thread to finish...")
            self.monitor_thread.join(timeout=5.0)

            # Force stop if still alive
            if self.monitor_thread.is_alive():
                logger.warning("Monitor thread didn't stop gracefully")

        logger.info("✅ Progress monitoring stopped")

    def _start_monitor_thread(self):
        """Monitor thread'ini başlatan private method"""

        def monitor_worker():
            """Ana monitoring loop'u"""
            logger.info("🔍 Memory-aware progress monitoring started")

            try:
                while not self._stop_requested and not self._shutdown_event.is_set():  # ✅ Stop flag kontrol et

                    # Early exit check
                    if self._stop_requested:
                        break

                    self.monitoring_cycles += 1

                    try:
                        # Monitoring cycles...
                        self._monitor_memory_usage()

                        # Stop check between operations
                        if self._stop_requested:
                            break

                        self._monitor_thread_health()

                        if self._stop_requested:
                            break

                        self._monitor_training_progress()
                        self._update_ui_indicators()
                        self._update_dashboard_stats()

                    except Exception as cycle_error:
                        logger.debug(f"Monitor cycle error: {cycle_error}")

                    # Interruptible sleep
                    if not self._stop_requested:
                        sleep_time = self._calculate_adaptive_sleep()
                        if self._shutdown_event.wait(timeout=sleep_time):
                            break  # Event was set, exit loop

                logger.info(f"🏁 Monitor stopped after {self.monitoring_cycles} cycles")

            except Exception as e:
                logger.error(f"❌ Monitor worker crashed: {e}")
            finally:
                self._cleanup_monitor_thread()

        # ✅ Daemon=False kullanın, manuel control için
        self.monitor_thread = threading.Thread(
            target=monitor_worker,
            name="ProgressMonitor",
            daemon=False  # ✅ False yapın
        )

        self.control_panel.active_threads.append(self.monitor_thread)
        self.monitor_thread.start()

    def emergency_stop(self):
        """Emergency stop - immediate shutdown"""
        logger.warning("🚨 Emergency stop progress monitoring")

        self._shutdown_event.set()
        self.is_monitoring = False

        # Immediate cleanup without waiting
        logger.info("✅ Emergency stop completed")

    def _start_monitor_thread(self):
        """Monitor thread'ini başlatan private method[1]"""

        def monitor_worker():
            """Ana monitoring loop'u"""
            logger.info("🔍 Memory-aware progress monitoring started")

            try:
                while not self._shutdown_event.is_set():
                    self.monitoring_cycles += 1

                    try:
                        # Memory monitoring cycle
                        self._monitor_memory_usage()

                        # Thread cleanup cycle
                        self._monitor_thread_health()

                        # Training progress cycle
                        self._monitor_training_progress()

                        # UI update cycle
                        self._update_ui_indicators()

                        # Dashboard update cycle
                        self._update_dashboard_stats()

                    except Exception as cycle_error:
                        logger.debug(f"Monitor cycle error: {cycle_error}")

                    # Adaptive sleep based on system load
                    sleep_time = self._calculate_adaptive_sleep()
                    self._shutdown_event.wait(timeout=sleep_time)

                logger.info(f"🏁 Monitor stopped after {self.monitoring_cycles} cycles")

            except Exception as e:
                logger.error(f"❌ Monitor worker crashed: {e}")
            finally:
                self._cleanup_monitor_thread()

        # Thread oluştur ve başlat
        self.monitor_thread = threading.Thread(
            target=monitor_worker,
            name="ProgressMonitor",
            daemon=True
        )

        self.control_panel.active_threads.append(self.monitor_thread)
        self.monitor_thread.start()

        logger.info("✅ Monitor thread started")

    def _monitor_memory_usage(self):
        """Memory usage'ı monitor eden method - RTX 3060 için kritik"""
        try:
            import psutil

            # System memory stats
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            memory_percent = memory.percent
            swap_percent = swap.percent

            # ✅ SWAP memory management
            if swap_percent > 50:  # Swap %50'den fazla kullanılıyorsa
                logger.warning(f"🔄 HIGH SWAP USAGE: {swap_percent}%")
                self._trigger_swap_cleanup()

            # Critical memory management
            if memory_percent > self.memory_critical_threshold or swap_percent > 80:
                self.memory_warnings_count += 1
                logger.warning(f"🚨 CRITICAL MEMORY: RAM {memory_percent}%, SWAP {swap_percent}%")
                self._trigger_emergency_cleanup()

            elif memory_percent > self.memory_warning_threshold or swap_percent > 30:
                self.memory_warnings_count += 1
                logger.warning(f"⚠️ HIGH MEMORY: RAM {memory_percent}%, SWAP {swap_percent}%")
                self._trigger_memory_cleanup()

            # Update status text
            self._update_memory_status(memory_percent, swap_percent)

        except ImportError:
            self._update_basic_status()
        except Exception as e:
            logger.debug(f"Memory monitoring error: {e}")

    def _trigger_swap_cleanup(self):
        """Swap memory cleanup için agresif temizlik"""
        try:
            import gc
            import os

            logger.info("🔄 Starting aggressive swap cleanup")

            # 1. Python garbage collection
            for i in range(3):
                collected = gc.collect()
                logger.debug(f"GC cycle {i + 1}: collected {collected} objects")

            # 2. GPU memory cleanup
            try:
                from src.models.model_loader import force_gpu_cleanup
                force_gpu_cleanup()
            except:
                pass

            # 3. Force process memory trim (Linux)
            try:
                if hasattr(os, 'sched_yield'):
                    os.sched_yield()
            except:
                pass

            self.cleanup_triggers_count += 1
            logger.info("✅ Swap cleanup completed")

        except Exception as e:
            logger.error(f"❌ Swap cleanup failed: {e}")

    def _monitor_thread_health(self):
        """Active thread'lerin sağlığını monitor eden method"""
        try:
            if hasattr(self.control_panel, 'cleanup_threads'):
                self.control_panel.cleanup_threads()
        except Exception as e:
            logger.debug(f"Thread health monitoring error: {e}")

    def _monitor_training_progress(self):
        """Training progress'ini monitor eden method"""
        try:
            # Training coordinator'dan status al
            if hasattr(self.control_panel, 'training_coordinator'):
                training_status = self.control_panel.training_coordinator.get_queue_status()
                self._update_training_indicators(training_status)
        except Exception as e:
            logger.debug(f"Training progress monitoring error: {e}")

    def _update_ui_indicators(self):
        """UI indicator'larını güncelleyen method"""
        try:
            # Progress bar update
            if hasattr(self.control_panel, 'progress_bar') and self.control_panel.progress_bar:
                # Calculate progress based on autonomous manager
                if hasattr(self.control_panel, 'autonomous_manager'):
                    progress_info = self.control_panel.autonomous_manager.get_progress_info()
                    if progress_info['total_topics'] > 0:
                        progress_value = progress_info['progress_percentage'] / 100.0
                        self.control_panel.progress_bar.value = progress_value

            # Safe page update
            self.control_panel.safe_page_update()

        except Exception as e:
            logger.debug(f"UI indicator update error: {e}")

    def _update_dashboard_stats(self):
        """Dashboard statistics'i güncelleyen method"""
        try:
            if (hasattr(self.control_panel, 'dashboard_cards') and
                    self.control_panel.dashboard_cards and
                    hasattr(self.control_panel.dashboard_cards, 'update_research_stats')):
                # Create comprehensive stats
                stats = {
                    'monitoring_cycles': self.monitoring_cycles,
                    'memory_warnings': self.memory_warnings_count,
                    'cleanup_triggers': self.cleanup_triggers_count,
                    'active_threads': len(self.control_panel.active_threads)
                }

                self.control_panel.dashboard_cards.update_research_stats(stats)

        except Exception as e:
            logger.debug(f"Dashboard update error: {e}")

    def _trigger_emergency_cleanup(self):
        """Emergency memory cleanup tetikleyen method"""
        try:
            from src.models.model_loader import force_gpu_cleanup

            self.cleanup_triggers_count += 1

            logger.warning("🚨 Triggering emergency memory cleanup")
            cleanup_success = force_gpu_cleanup()

            if cleanup_success:
                logger.info("✅ Emergency cleanup successful")
            else:
                logger.warning("⚠️ Emergency cleanup had issues")

        except Exception as e:
            logger.error(f"❌ Emergency cleanup failed: {e}")

    def _trigger_memory_cleanup(self):
        """Regular memory cleanup tetikleyen method"""
        try:
            # Regular cleanup - less aggressive than emergency
            import gc
            gc.collect()

            # GPU cleanup if available
            try:
                from src.models.model_loader import force_gpu_cleanup
                force_gpu_cleanup()
            except:
                pass  # Silent fail for GPU cleanup

        except Exception as e:
            logger.debug(f"Regular cleanup error: {e}")

    def _update_memory_status(self, memory_percent: float, swap_percent: float):
        """Memory status'unu UI'da güncelleyen method"""
        try:
            if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:

                # Global training state check
                from src.ui.builder.control_panel.training_coordinator import _active_model

                if _active_model:
                    status = f"🔄 Training: {_active_model}"
                    color = "blue"
                elif memory_percent > self.memory_critical_threshold:
                    status = f"🚨 CRITICAL: {memory_percent:.1f}% RAM"
                    color = "red"
                elif memory_percent > self.memory_warning_threshold:
                    status = f"⚠️ HIGH: {memory_percent:.1f}% RAM, {swap_percent:.1f}% SWAP"
                    color = "orange"
                else:
                    active_count = len([t for t in self.control_panel.active_threads if t.is_alive()])
                    status = f"📊 Memory: {memory_percent:.1f}% - {active_count} threads"
                    color = "green"

                self.control_panel.status_text.value = status
                # Color update logic here if needed

        except Exception as e:
            logger.debug(f"Memory status update error: {e}")

    def _update_basic_status(self):
        """Basic status update - psutil olmadığında"""
        try:
            if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:
                active_count = len([t for t in self.control_panel.active_threads if t.is_alive()])
                status = f"📡 Monitor cycle #{self.monitoring_cycles} - {active_count} threads"
                self.control_panel.status_text.value = status
        except Exception as e:
            logger.debug(f"Basic status update error: {e}")

    def _update_training_indicators(self, training_status: Dict[str, Any]):
        """Training indicator'larını güncelleyen method"""
        try:
            if training_status.get('queue_size', 0) > 0:
                queue_size = training_status['queue_size']
                if hasattr(self.control_panel, 'status_text') and self.control_panel.status_text:
                    self.control_panel.status_text.value = f"⏳ Queue: {queue_size} pending"
        except Exception as e:
            logger.debug(f"Training indicator update error: {e}")

    def _calculate_adaptive_sleep(self) -> float:
        """Sistem yüküne göre adaptive sleep süresi hesaplayan method"""
        try:
            # Memory pressure'a göre sleep time ayarla
            if self.memory_warnings_count > 0:
                return 1.0  # Fast monitoring during memory pressure
            else:
                return self.monitoring_interval  # Normal interval
        except:
            return 2.0  # Fallback interval

    def _cleanup_monitor_thread(self):
        """Monitor thread cleanup"""
        logger.debug("🧹 Progress monitor cleanup completed")
