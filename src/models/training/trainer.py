# src/models/training/trainer.py
"""
Main Training Module following PyTorch patterns[1][2][3]
RTX 3060 optimized training implementation
"""
import torch
import logging
from pathlib import Path
from datasets import Dataset
from transformers import TrainingArguments, DataCollatorForLanguageModeling
from peft import LoraConfig
from typing import List, Dict, Optional, Any

from ..memory.memory_manager import MemoryManager
from peft import get_peft_model
from .training_context import TrainingContext
from .optimized_trainer import OptimizedTrainer

logger = logging.getLogger(__name__)


class RTX3060Trainer:
    """
    RTX 3060 optimized trainer following PyTorch training patterns[1][2]
    Implements complete training workflow
    """

    def __init__(self, rtx3060_detected: bool, device: torch.device, memory_manager: MemoryManager):
        self.rtx3060_detected = rtx3060_detected
        self.device = device
        self.training_context = TrainingContext(rtx3060_detected)
        self.memory_manager = memory_manager

        # Training configuration
        self.default_model_name = "bigcode/starcoder2-3b"

        logger.info(f"🎯 RTX3060Trainer initialized - Device: {device}")

    def run_training_session(
            self,
            model: torch.nn.Module,  # Dışarıdan gelen saf, quantize model
            tokenizer: Any,
            examples: List[Dict],
            topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main training function that now correctly applies LoRA adapters.
        """
        logger.info(f"🚀 Starting training session for: {topic}")
        if not examples:
            return {"status": "error", "message": "No training examples provided"}

        with self.training_context.training_session() as session_refs:
            try:
                # ### ANA DÜZELTME: LoRA ADAPTÖRÜNÜ BURADA EKLE ###
                # Dışarıdan gelen saf, quantize edilmiş modele, eğitilebilir
                # LoRA katmanlarını ekliyoruz. `model` değişkeni artık
                # bir `PeftModel` nesnesine dönüşüyor.
                lora_config = self._get_lora_config()
                model = get_peft_model(model, lora_config)
                logger.info("✅ LoRA adapters attached to the quantized model.")
                model.print_trainable_parameters()  # Eğitilebilir parametreleri logla

                # Referansları temizlik için sakla
                session_refs['model'] = model

                dataset = self._prepare_training_dataset(examples, tokenizer)
                training_args = self._get_training_arguments(topic)

                # Artık `model`, üzerinde eğitilebilir katmanlar olan bir PEFT modelidir.
                trainer = self._create_trainer(model, dataset, tokenizer, training_args, session_refs)

                logger.info("🔍 Starting training loop...")
                train_result = trainer.train()

                save_success, save_path = self._save_trained_model(trainer.model, tokenizer, topic)
                result = self._compile_training_results(train_result, save_success, save_path, topic, len(examples))

                logger.info(f"✅ Training completed successfully: {topic}")
                return result

            except torch.cuda.OutOfMemoryError:
                logger.error("❌ CUDA OOM during training")
                return {"status": "error", "message": "CUDA Out of Memory"}
            except Exception as e:
                logger.error(f"❌ Training failed: {e}", exc_info=True)
                return {"status": "error", "message": str(e)}

    def run_optimized_training(
            self,
            model: torch.nn.Module,  # Dışarıdan gelen saf, quantize model
            tokenizer: Any,
            examples: List[Dict],
            topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main training function that correctly applies LoRA adapters to the provided model.
        """
        logger.info(f"🚀 Starting optimized training for: {topic}")
        if not examples:
            return {"status": "error", "message": "No training examples provided"}

        with self.training_context.training_session() as session_refs:
            try:
                # Adım 1: Dışarıdan gelen modele LoRA adaptörlerini uygula
                lora_config = self._get_lora_config()
                model = get_peft_model(model, lora_config)
                logger.info("✅ LoRA adapters attached to the quantized model.")
                model.print_trainable_parameters()
                session_refs['model'] = model

                # Adım 2: Veri setini hazırla
                dataset = self._prepare_training_dataset(examples, tokenizer)

                # Adım 3: Eğitim argümanlarını yapılandır
                training_args = self._get_training_arguments(topic)

                # Adım 4: `Trainer`'ı oluştur
                trainer = self._create_trainer(model, dataset, tokenizer, training_args, session_refs)

                # Adım 5: Eğitimi başlat
                logger.info("🔍 Training loop starting...")
                train_result = trainer.train()

                # Adım 6: Eğitilmiş modeli kaydet
                save_success, save_path = self._save_trained_model(trainer.model, tokenizer, topic)

                # Adım 7: Sonuçları derle
                result = self._compile_training_results(train_result, save_success, save_path, topic, len(examples))

                logger.info(f"✅ Training completed successfully: {topic}")
                return result

            except torch.cuda.OutOfMemoryError:
                logger.error("❌ CUDA OOM during training", exc_info=True)
                return {"status": "error", "message": "CUDA Out of Memory"}
            except Exception as e:
                logger.error(f"❌ Training failed: {e}", exc_info=True)
                return {"status": "error", "message": str(e)}


    def _load_and_prepare_model_for_training(self, session_refs: Dict[str, Any]) -> tuple:
        """Loads the base model, quantizes it, and applies LoRA adapters."""
        # Bu metot, eski `_load_training_model`'ın işini yapar.
        base_loader = BaseModelLoader(self.rtx3060_detected, self.device)

        # Temel modeli yükle (bu adımda quantization zaten yapılıyor)
        model, tokenizer = base_loader.load_base_model(
            self.default_model_name,
            use_quantization=True,
            use_auto_device_map=True
        )

        # LoRA adaptörlerini quantize edilmiş modelin üzerine ekle
        lora_config = self._get_lora_config()
        model = get_peft_model(model, lora_config)
        logger.info("✅ LoRA adapters attached to the quantized model.")
        model.print_trainable_parameters()

        # Referansı temizlik için sakla
        session_refs['model'] = model

        return model, tokenizer


    def _setup_training_environment(self):
        """Setup RTX 3060 optimized training environment"""
        if not torch.cuda.is_available():
            return

        try:
            # Memory optimizations
            if self.rtx3060_detected:
                torch.cuda.set_per_process_memory_fraction(0.75)
                import os
                os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'

                # Enable memory history for debugging
                if hasattr(torch.cuda.memory, '_record_memory_history'):
                    torch.cuda.memory._record_memory_history()

                logger.info("🔧 RTX 3060 training environment configured")

        except Exception as e:
            logger.warning(f"⚠️ Training environment setup failed: {e}")


    def _get_lora_config(self) -> LoraConfig:
        """Get RTX 3060 optimized LoRA configuration"""
        return LoraConfig(
            r=8 if self.rtx3060_detected else 16,  # Lower rank for RTX 3060
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],  # Minimal modules for memory
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )

    def _prepare_training_dataset(self, examples: List[Dict], tokenizer) -> Dataset:
        """Prepares and tokenizes the dataset from raw examples."""
        training_data = []
        for example in examples:
            text = example.get('text') or f"{example.get('input', '')}\n\n{example.get('output', '')}"
            if text.strip():
                training_data.append({"text": text})

        if not training_data:
            logger.warning("⚠️ No valid training data, using a default example.")
            training_data = [{"text": "def hello_world():\n    print('Hello World')"}]

        dataset = Dataset.from_list(training_data)
        return self._tokenize_dataset(dataset, tokenizer)

    def _tokenize_dataset(self, dataset: Dataset, tokenizer) -> Dataset:
        """Tokenizes the dataset."""
        def tokenize_function(examples):
            texts = examples['text']
            max_length = 512
            # ### DÜZELTME: Eksik `return_tensors` parametresi eklendi ###
            model_inputs = tokenizer(texts, truncation=True, padding="max_length", max_length=max_length, return_tensors="pt")
            model_inputs["labels"] = model_inputs["input_ids"].clone()
            return model_inputs

        return dataset.map(tokenize_function, batched=True, batch_size=100, remove_columns=dataset.column_names)

    def _get_training_arguments(self, topic: Optional[str]) -> TrainingArguments:
        """Returns optimized TrainingArguments for RTX 3060."""
        output_dir = f'./model_output/{topic.replace(" ", "_")}' if topic else './model_output/default'
        return TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=8,
            learning_rate=2e-4,
            logging_steps=5,
            bf16=True,
            max_steps=20,
            report_to="none",
            gradient_checkpointing=True,
            save_strategy="no"
        )

    def _create_trainer(self, model, dataset, tokenizer, training_args: TrainingArguments,
                        session_refs: Dict[str, Any]) -> OptimizedTrainer:
        """Creates an instance of the OptimizedTrainer."""
        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
        trainer = OptimizedTrainer(
            rtx3060_detected=self.rtx3060_detected,
            model=model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator
        )
        session_refs['trainer'] = trainer
        return trainer

    def _save_trained_model(self, model, tokenizer, topic: Optional[str]) -> tuple:
        """Saves the trained model adapters safely."""
        save_dir = f"trained_models/{topic.replace(' ', '_')}" if topic else "trained_models/default"
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        try:
            model.save_pretrained(save_dir)
            tokenizer.save_pretrained(save_dir)
            logger.info(f"✅ Model saved to: {save_dir}")
            return True, save_dir
        except Exception as e:
            logger.error(f"❌ Model saving failed: {e}", exc_info=True)
            return False, None

    def _compile_training_results(self, train_result, save_success: bool, save_path: str, topic: str, example_count: int) -> Dict[str, Any]:
        """Compiles the final results dictionary."""
        return {
            "status": "success", "topic": topic, "examples": example_count,
            "training_time": train_result.metrics.get('train_runtime', 0),
            "final_loss": train_result.metrics.get('train_loss', 0),
            "metrics": train_result.metrics,
            "model_saved": save_path if save_success else None,
            "rtx3060_optimized": self.rtx3060_detected
        }
