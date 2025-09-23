"""
🔧 SeydappAI ModelTrainer - Central Configuration Management
Merkezi konfigürasyon yönetimi - environment variables ve YAML destekli
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

# Proje kök dizini
PROJECT_ROOT = Path(__file__).parent.parent.parent


@dataclass
class AppConfig:
    """Uygulama konfigürasyon sınıfı"""
    title: str = "SeydappAI Model Trainer"
    version: str = "1.0.0"
    window_width: int = 1200
    window_height: int = 1000
    theme: str = "dark"


@dataclass
class TrainingConfig:
    """Eğitim konfigürasyon sınıfı"""
    default_epochs: int = 6
    default_batch_size: int = 1
    default_learning_rate: float = 1e-4
    max_sequence_length: int = 2048
    output_dir: str = "./trained_models"


class ConfigManager:
    """Konfigürasyon yöneticisi sınıfı"""

    def __init__(self):
        self.config_path = PROJECT_ROOT / "configs" / "app_config.yaml"
        self.app_config = AppConfig()
        self.training_config = TrainingConfig()
        self.load_config()

    def load_config(self):
        """YAML konfigürasyonunu yükle"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)

                # App config güncelle
                if 'app' in config_data:
                    app_data = config_data['app']
                    self.app_config.title = app_data.get('title', self.app_config.title)
                    self.app_config.version = app_data.get('version', self.app_config.version)
                    if 'window' in app_data:
                        self.app_config.window_width = app_data['window'].get('width', 1200)
                        self.app_config.window_height = app_data['window'].get('height', 1000)

                # Training config güncelle
                if 'training' in config_data:
                    training_data = config_data['training']
                    self.training_config.default_epochs = training_data.get('default_epochs', 6)
                    self.training_config.default_batch_size = training_data.get('default_batch_size', 1)

        except Exception as e:
            print(f"Config yükleme hatası: {e}")

    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Model-specific konfigürasyon al"""
        # Environment variables'dan öncelik ver
        env_lr = os.getenv('TRAINING_LEARNING_RATE')
        if env_lr:
            self.training_config.default_learning_rate = float(env_lr)

        return {
            "learning_rate": self.training_config.default_learning_rate,
            "epochs": self.training_config.default_epochs,
            "batch_size": self.training_config.default_batch_size
        }


# Global config instance
config_manager = ConfigManager()

# Model configurations - orijinal AVAILABLE_MODELS'dan adapt edildi
AVAILABLE_MODELS = {
    "./starcoder2_finetuned_20250828_130807": {
        "name": "StarCoder2 3B (Özel Eğitilmiş) 🎯",
        "size": "~6GB + LoRA adapters",
        "category": "code",
        "description": "Kişisel dataset ile fine-tuned StarCoder2 modeli",
        "custom_trained": True,
        "base_model": "bigcode/starcoder2-3b",
        "adapter_path": "./starcoder2_finetuned_20250828_130807",
        "load_method": "lora_adapter"
    },
    "bigcode/starcoder2-3b": {
        "name": "StarCoder2 3B ⚡",
        "size": "~6GB (optimized)",
        "category": "code",
        "description": "17 dil destekli, yeni nesil kod üretim modeli"
    },
    "bigcode/starcoder2-7b": {
        "name": "StarCoder2 7B 🔥",
        "size": "~14GB (VRAM yetersiz olabilir)",
        "category": "code",
        "description": "Gelişmiş kod üretimi, büyük VRAM gerektirir",
        "warning": "RTX 3060 için memory yetersiz olabilir"
    }
}
