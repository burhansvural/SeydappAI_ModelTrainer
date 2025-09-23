# src/core/app_manager.py
"""
🎛️ SeydappAI ModelTrainer - Application Manager
Ana uygulama yöneticisi - dependency checking ve initialization
"""
import logging
import os
import sys
from pathlib import Path

from ..utils.environment import check_python_version, check_dependencies
from .config import config_manager

logger = logging.getLogger(__name__)


class AppManager:
    """Ana uygulama yöneticisi"""

    def __init__(self):
        self.initialized = False
        self.project_root = Path(__file__).parent.parent.parent

    def initialize(self) -> bool:
        """Uygulama başlatma kontrolü"""
        try:
            # Python versiyon kontrolü
            if not check_python_version():
                return False

            # Dependency kontrolü
            deps = check_dependencies()
            missing_deps = [pkg for pkg, status in deps.items() if not status]

            if missing_deps:
                logger.error(f"❌ Eksik bağımlılıklar: {missing_deps}")
                logger.info("💡 'pip install -r requirements.txt' çalıştırın")
                return False

            # Dizin yapısını kontrol et ve oluştur
            self._ensure_directories()

            # Environment variables
            self._setup_environment()

            self.initialized = True
            logger.info("✅ SeydappAI ModelTrainer başarıyla başlatıldı")
            return True

        except Exception as e:
            logger.error(f"❌ Başlatma hatası: {e}")
            return False

    def _ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        required_dirs = [
            "logs", "datasets", "trained_models",
            "storage/temp", "storage/data"
        ]

        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)

    def _setup_environment(self):
        """Environment variables ayarla"""
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'

        # Project root'u Python path'e ekle
        if str(self.project_root) not in sys.path:
            sys.path.insert(0, str(self.project_root))


# Global app manager instance
app_manager = AppManager()
