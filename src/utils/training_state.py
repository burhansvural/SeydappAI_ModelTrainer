# src/utils/training_state.py

from datetime import datetime
from typing import Dict, Any, Optional
import threading
import logging

logger = logging.getLogger(__name__)


class TrainingState:
    """✅ Global training state manager - Gerçek training verilerini tutar"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.reset_state()
    
    def reset_state(self):
        """✅ Training state'i sıfırla"""
        self._state = {
            "is_training": False,
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
            "training_start_time": None,
            "model_name": "",
            "dataset_size": 0
        }
        logger.info("🔄 Training state reset")
    
    def start_training(self, config: Dict[str, Any]):
        """✅ Training başlatıldığında çağrılır"""
        with self._lock:
            self._state.update({
                "is_training": True,
                "training_start_time": datetime.now(),
                "total_epochs": config.get("epochs", 3),
                "total_steps": config.get("max_steps", 100),
                "learning_rate": config.get("learning_rate", 5e-5),
                "model_name": config.get("model_name", ""),
                "dataset_size": config.get("dataset_size", 0),
                "last_updated": datetime.now()
            })
        logger.info(f"🚀 Training started: {config.get('model_name', 'Unknown model')}")
    
    def stop_training(self):
        """✅ Training durdurulduğunda çağrılır"""
        with self._lock:
            self._state["is_training"] = False
            self._state["last_updated"] = datetime.now()
        logger.info("⏹️ Training stopped")
    
    def update_progress(self, 
                       current_epoch: Optional[int] = None,
                       current_step: Optional[int] = None,
                       train_loss: Optional[float] = None,
                       eval_loss: Optional[float] = None,
                       learning_rate: Optional[float] = None,
                       **kwargs):
        """✅ Training progress güncelle"""
        with self._lock:
            if current_epoch is not None:
                self._state["current_epoch"] = current_epoch
            if current_step is not None:
                self._state["current_step"] = current_step
            if train_loss is not None:
                self._state["train_loss"] = train_loss
            if eval_loss is not None:
                self._state["eval_loss"] = eval_loss
            if learning_rate is not None:
                self._state["learning_rate"] = learning_rate
            
            # Ek parametreler
            for key, value in kwargs.items():
                if key in self._state:
                    self._state[key] = value
            
            # ETA hesapla
            if self._state["current_step"] > 0 and self._state["training_start_time"]:
                elapsed = datetime.now() - self._state["training_start_time"]
                steps_per_second = self._state["current_step"] / elapsed.total_seconds()
                remaining_steps = self._state["total_steps"] - self._state["current_step"]
                if steps_per_second > 0:
                    eta_seconds = remaining_steps / steps_per_second
                    self._state["eta_minutes"] = int(eta_seconds / 60)
                    self._state["tokens_per_second"] = steps_per_second * 100  # Rough estimate
            
            self._state["last_updated"] = datetime.now()
    
    def get_state(self) -> Dict[str, Any]:
        """✅ Mevcut training state'i döndür"""
        with self._lock:
            return self._state.copy()
    
    def is_training(self) -> bool:
        """✅ Training aktif mi?"""
        return self._state.get("is_training", False)
    
    def get_progress_percentage(self) -> float:
        """✅ Progress yüzdesi"""
        if self._state["total_steps"] > 0:
            return (self._state["current_step"] / self._state["total_steps"]) * 100
        return 0.0


# Global instance
training_state = TrainingState()