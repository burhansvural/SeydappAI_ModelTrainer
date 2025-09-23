# src/ui/builder/control_panel/training_coordinator.py
"""
🎯 Training Coordinator - RTX 3060 için Eğitim Koordinasyon Sistemi (Nihai Sürüm)

Bu dosya, model eğitimi süreçlerini koordine eder. Bu sürüm, `model_loader`'ın
doğru ve güvenli fonksiyonlarını çağırarak loglarda görülen kritik hataları giderir
ve refactoring uygulanarak daha basit ve kararlı bir yapıya kavuşturulmuştur.
"""
import logging
import threading
import time
import queue
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

# ### AÇIKLAMA: Doğru ve Güvenli Fonksiyonların Import Edilmesi ###
# Artık sadece `model_loader`'dan tek bir ana eğitim fonksiyonu ve güvenli
# temizlik fonksiyonunu import ediyoruz.
from src.models.model_loader import run_optimized_training, safe_gpu_cleanup

logger = logging.getLogger(__name__)

# Global eğitim durumu, tek seferde bir eğitim için.
_training_lock = threading.Lock()
_active_model_topic: Optional[str] = None


@dataclass(order=True)
class TrainingJob:
    """Eğitim işini temsil eden veri sınıfı."""
    priority: int
    # Syntax hatası düzeltildi (`==` yerine `=`)
    created_time: float = field(init=False, default_factory=time.time)
    topic: str = field(compare=False)
    examples: List[Dict[str, Any]] = field(compare=False)


class TrainingCoordinator:
    """RTX 3060 için optimize edilmiş, thread-safe eğitim koordinatörü."""

    def __init__(self, control_panel_instance):
        """Training Coordinator'ı başlatır."""
        logger.info("🎯 TrainingCoordinator (Nihai Sürüm) başlatılıyor...")
        self.control_panel = control_panel_instance
        self.page = control_panel_instance.page
        self.is_active = False
        self.training_queue = queue.PriorityQueue()
        self._coordinator_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        self._max_queue_size = 10
        self.completed_trainings = []
        self.failed_trainings = []
        self._total_jobs_processed = 0
        logger.info("✅ TrainingCoordinator başlatıldı.")

    def start_coordinator(self) -> bool:
        """Eğitim koordinatörünü ve arkaplan işleyici thread'ini başlatır."""
        if self.is_active:
            logger.warning("⚠️ Training coordinator zaten aktif.")
            return False

        logger.info("🚀 Training coordinator başlatılıyor...")
        self.is_active = True
        self._shutdown_event.clear()

        self._coordinator_thread = threading.Thread(
            target=self._worker_loop, daemon=True, name="TrainingCoordinator"
        )
        self._coordinator_thread.start()

        if hasattr(self.control_panel, 'active_threads'):
            self.control_panel.active_threads.append(self._coordinator_thread)

        logger.info("✅ Training coordinator başarıyla başlatıldı.")
        return True

    def stop_coordinator(self):
        """Koordinatörü güvenli bir şekilde durdurur."""
        if not self.is_active: return
        logger.info("⏹️ Training coordinator durduruluyor...")
        self._shutdown_event.set()
        if self._coordinator_thread and self._coordinator_thread.is_alive():
            self._coordinator_thread.join(timeout=5.0)
        self.is_active = False
        self._clear_pending_jobs()
        logger.info("✅ Training coordinator durduruldu.")

    def queue_training(self, examples: List[Dict], topic: str, priority: int = 1) -> bool:
        """Yeni bir eğitim görevini öncelikli sıraya ekler."""
        if not self.is_active:
            logger.error("❌ Coordinator aktif değil. Eğitim sıraya alınamadı.")
            return False

        if self.training_queue.qsize() >= self._max_queue_size:
            logger.warning(f"⚠️ Eğitim sırası dolu. Görev eklenemedi: {topic}")
            return False

        job = TrainingJob(priority=priority, topic=topic, examples=examples)
        self.training_queue.put(job)
        logger.info(f"📝 Eğitim görevi sıraya eklendi: {topic} (Öncelik: {priority})")
        return True

    def _worker_loop(self):
        """Arka planda çalışarak sıradaki eğitim görevlerini işleyen ana döngü."""
        logger.info("🔄 Eğitim işleyici döngüsü başladı.")
        while not self._shutdown_event.is_set():
            try:
                job = self.training_queue.get(timeout=1.0)
                self._process_training_job(job)
                self.training_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ İşleyici döngüsünde beklenmedik hata: {e}", exc_info=True)
                time.sleep(5)
        logger.info("🏁 Eğitim işleyici döngüsü sonlandı.")

    def _process_training_job(self, job: TrainingJob):
        """
        ### AÇIKLAMA: Yeniden Yapılandırılmış Ana İşlem Metodu ###
        Bu metot artık tek bir eğitim görevini baştan sona yönetir. Karmaşık
        çağrı zinciri yerine, tüm adımlar burada net bir şekilde sıralanmıştır.
        """
        global _training_lock, _active_model_topic

        logger.info(f"🎯 Eğitim görevi işleniyor: {job.topic}")

        with _training_lock:
            _active_model_topic = job.topic
            job_start_time = time.time()
            result = None
            try:
                self._update_ui_status(f"🔄 Eğitim başlıyor: {job.topic}")

                # --- ANA DÜZELTME ---
                # Artık doğrudan `model_loader`'dan doğru ve güvenli fonksiyonu çağırıyoruz.
                # Bu tek fonksiyon, kendi içinde temizlik, model yükleme, eğitim ve
                # tekrar temizlik işlemlerini yönetir.
                result = run_optimized_training(job.examples, job.topic)

            except Exception as e:
                logger.error(f"💥 Eğitim görevi '{job.topic}' kritik bir hatayla çöktü: {e}", exc_info=True)
                result = {"status": "error", "message": str(e)}
            finally:
                # Eğitim bittiğinde veya hata verdiğinde sonuçları işle.
                job_duration = time.time() - job_start_time
                if result and result.get("status") == "success":
                    logger.info(f"✅ Eğitim görevi '{job.topic}' {job_duration:.2f} saniyede başarıyla tamamlandı.")
                    self._update_ui_status(f"✅ Başarılı: {job.topic}")
                    self.completed_trainings.append({'topic': job.topic, 'duration': job_duration, 'result': result})
                else:
                    error_msg = result.get("message", "Bilinmeyen hata") if result else "Çökme"
                    logger.error(f"❌ Eğitim görevi '{job.topic}' başarısız oldu. Hata: {error_msg}")
                    self._update_ui_status(f"❌ Hata: {job.topic}")
                    self.failed_trainings.append({'topic': job.topic, 'duration': job_duration, 'error': error_msg})

                self._total_jobs_processed += 1
                _active_model_topic = None
                # Son bir güvenlik temizliği. `run_optimized_training` zaten kendi
                # temizliğini yapsa da, bu ek çağrı zararsızdır.
                safe_gpu_cleanup()

    def _update_ui_status(self, text: str):
        """UI'daki durum metnini thread-safe bir şekilde günceller."""
        if self.control_panel and hasattr(self.control_panel, 'status_text'):
            try:
                self.control_panel.status_text.value = text
                if self.page and self.page.session_id:
                    self.page.update()
            except Exception as e:
                logger.debug(f"UI güncelleme hatası (sayfa kapalı olabilir): {e}")

    def _clear_pending_jobs(self):
        """Kuyruktaki tüm bekleyen işleri temizler."""
        with self.training_queue.mutex:
            cleared_count = self.training_queue.qsize()
            self.training_queue.queue.clear()
        if cleared_count > 0:
            logger.info(f"🗑️ Bekleyen {cleared_count} eğitim görevi temizlendi.")

    def get_queue_status(self) -> Dict[str, Any]:
        """Kuyruk durumu hakkında anlık bilgi döndürür."""
        # Lock kullanmak yerine, thread-safe olan `qsize`'ı doğrudan kullanabiliriz.
        # Bu, daha performanslı bir okuma sağlar.
        return {
            'is_active': self.is_active,
            'queue_size': self.training_queue.qsize(),
            'max_queue_size': self._max_queue_size,
            'total_processed': self._total_jobs_processed,
            'completed_count': len(self.completed_trainings),
            'failed_count': len(self.failed_trainings),
            'active_model': _active_model_topic
        }