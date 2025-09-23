"""
📚 Dataset Management System
Dataset validation, loading ve preprocessing
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datasets import Dataset

from ..utils.logger import setup_logger

logger = setup_logger("DatasetManager")


class DatasetManager:
    """Dataset yönetimi sınıfı"""

    def __init__(self, dataset_dir: str = "datasets"):
        self.dataset_dir = Path(dataset_dir)
        self.dataset_dir.mkdir(exist_ok=True)

    def validate_conversation_dataset(self, dataset_path: str) -> Dict[str, Any]:
        """Conversation dataset formatını doğrula"""
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Format kontrolü
            if isinstance(data, list):
                examples = data
            elif isinstance(data, dict):
                examples = data.get('examples', [])
            else:
                raise ValueError("Geçersiz dataset formatı")

            # Validation metrikleri
            conversation_count = sum(1 for ex in examples if ex.get('conversation_mode', False))
            valid_count = sum(1 for ex in examples if ex.get('instruction') and ex.get('output'))

            return {
                "valid": True,
                "total_examples": len(examples),
                "conversation_examples": conversation_count,
                "regular_examples": len(examples) - conversation_count,
                "valid_examples": valid_count,
                "quality_score": valid_count / len(examples) if examples else 0
            }

        except Exception as e:
            logger.error(f"Dataset validation hatası: {e}")
            return {"valid": False, "error": str(e)}

    def save_dataset(self, examples: List[Dict], filename: str) -> str:
        """Dataset'i dosyaya kaydet"""
        timestamp = int(time.time())
        full_path = self.dataset_dir / f"{filename}_{timestamp}.json"

        dataset_content = {
            "metadata": {
                "created_at": timestamp,
                "total_examples": len(examples),
                "format_version": "1.0"
            },
            "examples": examples
        }

        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(dataset_content, f, ensure_ascii=False, indent=2)

        logger.info(f"Dataset kaydedildi: {full_path}")
        return str(full_path)
