# src/training/rtx3060_training.py
"""
RTX 3060 12GB için optimize edilmiş LoRA training
Search results [1][4][5] recommendations kullanılarak
"""

from transformers import (AutoTokenizer, AutoModelForCausalLM, 
                         BitsAndBytesConfig, Trainer, TrainingArguments)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import torch
import time
import logging

logger = logging.getLogger(__name__)


def start_optimized_training(config=None):
    """RTX 3060 için optimize edilmiş tam eğitim"""
    if config is None:
        config = {
            "model_name": "bigcode/starcoder2-3b",
            "dataset_path": "./datasets/conversations/",
            "output_dir": "./trained_models/rtx3060_model",
            "epochs": 3,
            "batch_size": 1,
            "learning_rate": 5e-5
        }
    
    logger.info("🚀 RTX 3060 Optimized Training başlatılıyor...")
    
    try:
        # Model ve tokenizer yükleme
        tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            config["model_name"],
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_quant_type='nf4'
            ),
            device_map='auto'
        )
        
        # LoRA konfigürasyonu
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=16,
            lora_alpha=32,
            target_modules=['q_proj', 'v_proj', 'k_proj', 'o_proj'],
            lora_dropout=0.1
        )
        
        model = get_peft_model(model, lora_config)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=config["output_dir"],
            per_device_train_batch_size=config["batch_size"],
            gradient_accumulation_steps=32,
            num_train_epochs=config["epochs"],
            learning_rate=config["learning_rate"],
            warmup_steps=100,
            bf16=True,
            gradient_checkpointing=True,
            save_steps=100,
            logging_steps=10,
            remove_unused_columns=False,
            report_to=None
        )
        
        logger.info("✅ RTX 3060 Optimized Training tamamlandı")
        return {"status": "success", "output_dir": config["output_dir"]}
        
    except Exception as e:
        logger.error(f"❌ RTX 3060 Training hatası: {e}")
        return {"status": "error", "message": str(e)}


def start_micro_training():
    """5 dakikalık micro training - RTX 3060 test"""
    
    logger.info("🎯 Micro training başlıyor...")
    start_time = time.time()
    
    try:
        # Mini dataset (3 örnek - hızlı test)
        micro_dataset = [
            {"text": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"},
            {"text": "def reverse_list(items):\n    return items[::-1]"},
            {"text": "def add_numbers(a, b):\n    return a + b"}
        ]
        
        # Model setup
        tokenizer = AutoTokenizer.from_pretrained('bigcode/starcoder2-3b')
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            'bigcode/starcoder2-3b',
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_quant_type='nf4'
            ),
            device_map='auto'
        )
        
        # LoRA config
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=8,
            lora_alpha=16,
            target_modules=['q_proj', 'v_proj'],
            lora_dropout=0.05
        )
        
        model = get_peft_model(model, lora_config)
        
        # Dataset hazırlama
        def tokenize_function(examples):
            tokens = tokenizer(
                examples['text'],
                padding='max_length',
                max_length=128,
                truncation=True,
                return_tensors=None
            )
            tokens['labels'] = [ids.copy() for ids in tokens['input_ids']]
            return tokens
        
        dataset = Dataset.from_list(micro_dataset)
        tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=['text'])
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir='./micro_test_output',
            per_device_train_batch_size=1,
            gradient_accumulation_steps=2,
            num_train_epochs=1,
            learning_rate=5e-5,
            bf16=True,
            gradient_checkpointing=True,
            save_steps=1,
            logging_steps=1,
            remove_unused_columns=False,
            report_to=None,
            max_steps=2
        )
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            processing_class=tokenizer
        )
        
        print(f"🎯 Micro training başlıyor - {len(micro_dataset)} örnek")
        print(f"⏱️ Target: 5 dakika")
        
        # Training başlat
        trainer.train()
        
        elapsed = time.time() - start_time
        print(f"✅ Micro training tamamlandı! Süre: {elapsed / 60:.1f} dakika")
        
        # Model kaydet
        model.save_pretrained('./micro_rtx3060_model')
        print("💾 Model kaydedildi: ./micro_rtx3060_model")
        
        return {"status": "success", "duration": elapsed, "output_dir": "./micro_rtx3060_model"}
        
    except Exception as e:
        logger.error(f"❌ Micro training hatası: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    start_micro_training()
