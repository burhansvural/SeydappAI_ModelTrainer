# src/training/optimized_rtx3060_training.py
"""
2025 LoRA Best Practices - Search Results [1][2][3] optimizations
RTX 3060 + transformers 4.56.0 future-proof approach
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.models.model_loader import model_loader





def create_optimized_lora_config():
    """Search results [2][3] based optimal LoRA config"""
    from peft import LoraConfig, TaskType

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=8,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_dropout=0.05,
        bias="none"
    )
    return lora_config


def optimized_tokenization(tokenizer):
    """Causal LM için optimize edilmiş tokenization"""

    def tokenize_function(examples):
        texts = examples['text'] if isinstance(examples['text'], list) else [examples['text']]
        model_inputs = tokenizer(
            texts,
            truncation=True,
            padding='max_length',
            max_length=512,
            return_attention_mask=True,
            return_tensors=None
        )
        model_inputs['labels'] = [ids.copy() for ids in model_inputs['input_ids']]
        return model_inputs

    return tokenize_function


def monitor_gpu_during_training():
    """Training sırasında GPU monitörü"""
    import torch
    if torch.cuda.is_available():
        print("📊 GPU Monitoring Aktif")
        allocated_start = torch.cuda.memory_allocated(0) / 1024 ** 3
        print(f"Başlangıç GPU bellek: {allocated_start:.2f} GB")
        return allocated_start
    return 0


def test_tensor_transfer():
    """Tensor GPU transfer testi - Search results [1][2] optimized"""
    import torch
    print("🧪 Tensor Transfer Testi...")

    # CPU'da tensor oluştur[1]
    test_tensor = torch.randn(3, 3)
    print(f"Tensor başlangıç device: {test_tensor.device}")

    if torch.cuda.is_available():
        # Method 1: .cuda() kullanarak[1]
        test_tensor_cuda = test_tensor.cuda()
        print(f"✅ Method 1 (.cuda()): {test_tensor_cuda.device}")

        # Method 2: .to('cuda') kullanarak[1][2]
        test_tensor_to = test_tensor.to('cuda')
        print(f"✅ Method 2 (.to('cuda')): {test_tensor_to.device}")

        # Non-blocking transfer test[3]
        test_tensor_nonblock = test_tensor.to('cuda', non_blocking=True)
        torch.cuda.synchronize()  # Synchronize for accuracy[3]
        print(f"✅ Method 3 (non_blocking): {test_tensor_nonblock.device}")

        print(f"✅ Tensor CUDA'da: {test_tensor_cuda.is_cuda}")
    else:
        print("⚠️ CUDA kullanılamıyor")

    return test_tensor.device if not torch.cuda.is_available() else test_tensor_cuda.device


def test_gpu_usage():
    """GPU kullanımını test eder - tek fonksiyon"""
    import torch
    print("🔍 GPU Test Başlatılıyor...")
    print("=" * 40)

    # Temel CUDA kontrolleri
    print(f"CUDA kullanılabilir: {torch.cuda.is_available()}")
    print(f"GPU sayısı: {torch.cuda.device_count()}")

    if torch.cuda.is_available():
        print(f"Aktif GPU: {torch.cuda.current_device()}")
        print(f"GPU adı: {torch.cuda.get_device_name(0)}")

        # Model yükle ve test et
        try:
            model, tokenizer = model_loader.load_base_model(
                'bigcode/starcoder2-3b',
                use_quantization=True,
                use_auto_device_map=True
            )

            # Model GPU'da mı kontrol et
            model_device = next(model.parameters()).device
            is_cuda = next(model.parameters()).is_cuda

            print(f"Model device: {model_device}")
            print(f"Model CUDA'da: {is_cuda}")

            # GPU bellek durumu
            memory_info = model_loader.get_gpu_memory_info()
            print(f"GPU bellek: {memory_info}")

            return model, tokenizer

        except Exception as e:
            print(f"⚠️ Model yükleme test hatası: {e}")
            return None, None
    else:
        print("⚠️ CUDA kullanılamıyor")
        return None, None


def optimize_tensor_transfers(batch):
    """Batch tensor'larını optimize edilmiş şekilde GPU'ya taşır"""
    import torch

    if torch.cuda.is_available() and isinstance(batch, dict):
        # Non-blocking transfer ile hız optimizasyonu[3]
        optimized_batch = {}
        for key, value in batch.items():
            if isinstance(value, torch.Tensor):
                optimized_batch[key] = value.to('cuda', non_blocking=True)
            else:
                optimized_batch[key] = value

        # Synchronize to ensure completion[3]
        torch.cuda.synchronize()
        return optimized_batch
    return batch


def monitor_memory_usage():
    """RTX 3060 bellek durumunu izler"""
    import torch

    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated(0) / 1024 ** 3
        reserved = torch.cuda.memory_reserved(0) / 1024 ** 3
        total = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3

        print(f"📊 GPU Bellek: {allocated:.2f}GB / {total:.2f}GB ({allocated / total * 100:.1f}%)")

        # RTX 3060 için kritik eşik (85% üzeri tehlikeli)[1]
        if allocated / total > 0.85:
            print("⚠️ UYARI: GPU bellek kullanımı %85'i aştı!")
            torch.cuda.empty_cache()
            print("🧹 Otomatik cache temizliği yapıldı")


def rtx3060_memory_optimization():
    """RTX 3060 için özel bellek optimizasyonu - Search results [2][5]"""
    import torch
    import os

    # CUDA bellek fragmentasyon kontrolü[5]
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:32'

    # RTX 3060 specific settings[2]
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = True

    print("🔧 RTX 3060 bellek optimizasyonu aktif")


def prevent_oom_rtx3060():
    """RTX 3060 OOM prevention - Search results [2][5]"""
    import torch
    import gc

    # Aggressive memory management[5]
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

        # Check available memory[2]
        allocated = torch.cuda.memory_allocated(0) / 1024 ** 3
        total = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
        free = total - allocated

        print(f"🔍 RTX 3060 Bellek Durumu: {free:.2f}GB boş / {total:.2f}GB total")

        # Early warning system[2]
        if free < 2.0:  # RTX 3060 için kritik eşik
            print("⚠️ RTX 3060 UYARI: Düşük bellek! OOM riski yüksek")
            torch.cuda.empty_cache()
            gc.collect()

def run_optimized_training():
    """Search results [1][2][3] optimization ile final training"""
    import os
    from transformers import (AutoTokenizer, AutoModelForCausalLM,
                              BitsAndBytesConfig, Trainer, TrainingArguments,
                              DataCollatorForLanguageModeling)
    from peft import get_peft_model, prepare_model_for_kbit_training
    from datasets import Dataset
    import torch

    rtx3060_memory_optimization()

    print("🚀 Optimized LoRA Training - Search Results Based")
    print("=" * 55)

    # GPU testleri
    model_test, tokenizer_test = test_gpu_usage()
    device_test = test_tensor_transfer()
    monitor_gpu_during_training()

    # Dataset
    training_data = [
        {"text": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"},
        {
            "text": "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr)//2]\n    return quick_sort([x for x in arr if x < pivot]) + [x for x in arr if x == pivot] + quick_sort([x for x in arr if x > pivot])"},
        {
            "text": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1"}
    ]
    dataset = Dataset.from_list(training_data)

    # Model setup (test'te başarılıysa aynı modeli kullan)
    if model_test is not None and tokenizer_test is not None:
        print("📦 Test modelini kullanıyor...")
        model, tokenizer = model_test, tokenizer_test
    else:
        print("📦 Model yeniden yükleniyor...")
        model, tokenizer = model_loader.load_base_model(
            'bigcode/starcoder2-3b',
            use_quantization=True,
            use_auto_device_map=True
        )

    # Training için hazırla
    model = model_loader.prepare_model_for_training(model)
    model = get_peft_model(model, create_optimized_lora_config())
    model.print_trainable_parameters()

    # Tokenization
    tokenize_fn = optimized_tokenization(tokenizer)
    tokenized_dataset = dataset.map(tokenize_fn, batched=True, remove_columns=['text'])

    # Training arguments
    training_args = TrainingArguments(
        output_dir='./optimized_lora_output',
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        dataloader_pin_memory=False,
        num_train_epochs=2,
        learning_rate=1e-4,
        bf16=True,
        save_steps=1,
        save_total_limit=5,
        logging_steps=1,
        report_to=None,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={'use_reentrant': False}
    )

    # Training döngüsü her epoch sonrası cache temizliği[2][5]
    class CustomTrainer(Trainer):
        def on_epoch_end(self, args, state, control, **kwargs):
            torch.cuda.empty_cache()  # Her epoch sonrası temizlik[2]
            super().on_epoch_end(args, state, control, **kwargs)


    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = CustomTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator
    )

    print("🎯 Optimized training başlatılıyor...")

    prevent_oom_rtx3060()

    monitor_memory_usage()  # Training öncesi kontrol
    trainer.train()
    monitor_memory_usage()  # Training sonrası kontrol

    # Training sonrası GPU durumu
    # ✅ 1. ÖNCE MODEL KAYDET
    print("💾 Model kaydediliyor...")

    model.save_pretrained('./optimized_starcoder2_lora')
    tokenizer.save_pretrained('./optimized_starcoder2_lora')

    print("✅ Model başarıyla kaydedildi!")

    # ✅ 2. SONRA BELLEK TEMİZLİĞİ
    if torch.cuda.is_available():
        allocated_end = torch.cuda.memory_allocated(0) / 1024 ** 3
        print(f"Training sonrası GPU bellek: {allocated_end:.2f} GB")

        print("🧹 GPU bellek temizliği yapılıyor...")

        # Cache temizliği - Search results [5] approach
        torch.cuda.empty_cache()

        # Variables temizliği - MODEL KAYDETME SONRASI
        del trainer
        del model  # Artık güvenli
        del tokenizer

        # Garbage collection - Search results [5] solution
        import gc
        gc.collect()

        # Final durum
        final_allocated = torch.cuda.memory_allocated(0) / 1024 ** 3
        print(f"Temizlik sonrası GPU bellek: {final_allocated:.2f} GB")

        # Model loader cache temizliği
        model_loader.clear_gpu_cache()




def main():
    try:
        print("🤖 SeydappAI - Optimized LoRA Training")
        print("🔬 GPU Test + Training")
        print("=" * 50)

        success = run_optimized_training()

        if success:
            print("🎉 Training BAŞARILI!")

    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
