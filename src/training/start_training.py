# src/training/start_training.py - EXECUTABLE VERSION
"""
RTX 3060 Real LoRA Training Test
Search results [1][4] Trainer pattern kullanılarak
"""


def run_micro_training_test():
    """3 örneklik micro training test - RTX 3060 safe"""

    print("🎯 RTX 3060 Micro LoRA Training Test")
    print("=" * 45)

    import torch
    from transformers import (AutoTokenizer, AutoModelForCausalLM,
                              BitsAndBytesConfig, Trainer, TrainingArguments,
                              DataCollatorForLanguageModeling)
    from peft import (LoraConfig, get_peft_model, TaskType,
                      prepare_model_for_kbit_training)
    from datasets import Dataset

    # Test dataset
    micro_data = [
        {"text": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"},
        {"text": "def reverse_list(items):\n    return items[::-1]"},
        {"text": "def add_numbers(a, b):\n    return a + b"}
    ]
    dataset = Dataset.from_list(micro_data)
    print(f"✅ Dataset: {len(micro_data)} örnek hazırlandı")

    # Model ve tokenizer
    model_name = 'bigcode/starcoder2-3b'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Quantization config
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type='nf4'
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        device_map="auto",
        use_cache=False  # <-- DÜZELTME 1: `use_cache` uyarısını engellemek için
    )

    # Modeli k-bit eğitimi için hazırla
    model = prepare_model_for_kbit_training(model)

    # LoRA config
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj'],
        lora_dropout=0.05
    )
    model = get_peft_model(model, lora_config)
    print(f"💾 Memory: {model.get_memory_footprint() / 1e6:.2f} MB")
    model.print_trainable_parameters()

    # Tokenization
    def tokenize_function(examples):
        return tokenizer(examples['text'], truncation=True, max_length=256)

    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=['text'])

    # Language model'ler için 'labels' sütununu eklemek iyi bir pratiktir
    tokenized_dataset = tokenized_dataset.add_column("labels", tokenized_dataset["input_ids"])

    # Training arguments
    training_args = TrainingArguments(
        output_dir='./micro_test_results',
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=1,
        learning_rate=5e-5,
        bf16=True,
        save_steps=10,
        logging_steps=1,
        report_to=None,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={'use_reentrant': False}
    )

    # Data Collator
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator
        # <-- DÜZELTME 2: `tokenizer` parametresi kaldırıldı, uyarıyı giderir.
    )

    print('🚀 Micro training başlatılıyor...')
    print('⏱️ Tahmini süre: 3-5 dakika')

    trainer.train()

    print('✅ Micro training tamamlandı!')
    return True

def main():
    # Ana test execution
    try:
        print("🤖 SeydappAI ModelTrainer - Training Test")
        print("🎯 RTX 3060 + StarCoder2-3B + LoRA Pipeline")
        print("=" * 50)

        # ✅ METODU ÇAĞIR
        success = run_micro_training_test()

        if success:
            print("🎉 Training test BAŞARILI!")
            print("💡 Şimdi full training'e geçebilirsiniz")
        else:
            print("❌ Training test başarısız")

    except Exception as e:
        print(f"❌ Training test hatası: {e}")
        import traceback
        traceback.print_exc()


# ✅ PYTHON EXECUTION PATTERN
if __name__ == "__main__":
    main()  # Metod çağrısı burada!
