# src/utils/gpu_monitor.py

import psutil
import logging

logger = logging.getLogger(__name__)


class SystemMonitor:
    """✅ Search results [2] GPU monitoring pattern[2]"""

    @staticmethod
    def get_real_training_status():
        """✅ Search results [2] GPUtil proper usage[2]"""
        gpu_usage = 0
        vram_used = 0
        vram_total = 12288  # RTX 3060 default

        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                # ✅ CRITICAL FIX: List index access - Search results [2] ordered list[2]
                gpu = gpus[0]  # ✅ İlk GPU'yu al
                gpu_usage = gpu.load * 100
                vram_used = gpu.memoryUsed
                vram_total = gpu.memoryTotal
                logger.debug(f"✅ GPU {gpu.name}: {gpu_usage:.1f}% load, {vram_used:.1f}GB VRAM")
        except Exception as e:
            logger.warning(f"GPU info unavailable: {e}")

        cpu_usage = psutil.cpu_percent(interval=0.1)  # ✅ Non-blocking CPU check
        ram_usage = psutil.virtual_memory().percent

        return {
            "gpu_usage": gpu_usage,
            "vram_used": vram_used,
            "vram_total": vram_total,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage
        }

    @staticmethod
    def get_gpu_temperature():
        """✅ Search results [2] GPU temperature from list[2]"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].temperature  # ✅ First GPU temperature
        except:
            return 0
        return 0
    
    @staticmethod
    def get_detailed_system_stats():
        """✅ Detaylı sistem istatistikleri"""
        try:
            import GPUtil
            import shutil
            from datetime import datetime
            
            # GPU bilgileri
            gpu_info = {"name": "Unknown", "driver": "Unknown", "memory_total": 0}
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_info = {
                        "name": gpu.name,
                        "driver": getattr(gpu, 'driver', 'Unknown'),
                        "memory_total": gpu.memoryTotal,
                        "temperature": gpu.temperature,
                        "power_draw": getattr(gpu, 'powerDraw', 0),
                        "power_limit": getattr(gpu, 'powerLimit', 0)
                    }
            except Exception as e:
                logger.debug(f"GPU info error: {e}")
            
            # Disk bilgileri
            disk_usage = shutil.disk_usage("/")
            disk_free_gb = disk_usage.free / (1024**3)
            disk_total_gb = disk_usage.total / (1024**3)
            disk_used_percent = ((disk_usage.total - disk_usage.free) / disk_usage.total) * 100
            
            # Network bilgileri (basit)
            network_stats = psutil.net_io_counters()
            
            # Sistem bilgileri
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            return {
                "gpu_info": gpu_info,
                "disk": {
                    "free_gb": disk_free_gb,
                    "total_gb": disk_total_gb,
                    "used_percent": disk_used_percent
                },
                "network": {
                    "bytes_sent": network_stats.bytes_sent,
                    "bytes_recv": network_stats.bytes_recv
                },
                "system": {
                    "boot_time": boot_time,
                    "uptime": str(uptime).split('.')[0],
                    "cpu_count": psutil.cpu_count(),
                    "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Detailed stats error: {e}")
            return {}
    
    @staticmethod
    def get_training_metrics():
        """✅ Eğitim metrikleri - Gerçek training state'den alır"""
        try:
            from src.utils.training_state import training_state
            return training_state.get_state()
        except ImportError:
            # Fallback - training_state yoksa statik değerler
            from datetime import datetime
            return {
                "current_epoch": 0,
                "total_epochs": 3,
                "current_step": 0,
                "total_steps": 100,
                "learning_rate": 5e-5,
                "train_loss": 0.0,
                "eval_loss": 0.0,
                "accuracy": 0.0,
                "perplexity": 0.0,
                "tokens_per_second": 0.0,
                "eta_minutes": 0,
                "last_updated": datetime.now(),
                "is_training": False
            }
    
    @staticmethod
    def is_training_active():
        """✅ Training aktif mi kontrol et"""
        try:
            # Önce training state'i kontrol et
            from src.utils.training_state import training_state
            if training_state.is_training():
                return True
        except ImportError:
            pass
        
        # Fallback: GPU kullanımı %50'den fazlaysa training aktif kabul et
        try:
            status = SystemMonitor.get_real_training_status()
            return status['gpu_usage'] > 50.0
        except:
            return False
