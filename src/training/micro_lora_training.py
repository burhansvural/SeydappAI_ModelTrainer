# src/training/micro_lora_training.py
"""
Minimal LoRA Training Test
Search results [2]: systematic experimentation approach
"""


def start_micro_training():
    """
    5 dakikalık LoRA training test
    Search results [2]: start conservative, observe results
    """
    return run_5_minute_test()


def run_5_minute_test():
    """
    5 dakikalık LoRA training test
    Search results [2]: start conservative, observe results
    """
    print("🚀 5-Minute LoRA Test - Search Results [2] Approach")
    print("=" * 50)

    # Previous successful setup (tokenization fix ile)
    from transformers import (AutoTokenizer, AutoModelForCausalLM,
                              BitsAndBytesConfig, Trainer, TrainingArguments)
    from peft import LoraConfig, get_peft_model, TaskType
    from datasets import Dataset
    import torch
    import time

    start_time = time.time()

    # Micro dataset (hızlı test için 2 örnek)
    micro_data = [
        {"text": "def add(a, b): return a + b"},
        {"text": "def multiply(a, b): return a * b"}
    ]

    # Model setup (başarılı test config)
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

    # Search results [1] optimized LoRA config
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,  # Daha küçük rank (hızlı test için)
        lora_alpha=16,  # r * 2
        target_modules=['q_proj', 'v_proj'],  # Minimal modules (hızlı test)
        lora_dropout=0.05
    )

    model = get_peft_model(model, lora_config)

    # Search results [1] tokenization fix
    def tokenize_function(examples):
        tokens = tokenizer(
            examples['text'],
            padding='max_length',
            max_length=128,  # Küçük (hızlı test)
            truncation=True,
            return_tensors=None
        )
        tokens['labels'] = [ids.copy() for ids in tokens['input_ids']]
        return tokens

    # Dataset prepare
    dataset = Dataset.from_list(micro_data)
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=['text'])

    # Ultra-minimal training args (5 dakika target)
    training_args = TrainingArguments(
        output_dir='./micro_5min_test',
        per_device_train_batch_size=1,
        gradient_accumulation_steps=2,
        num_train_epochs=1,  # Tek epoch
        learning_rate=1e-4,
        bf16=True,
        save_steps=1,
        logging_steps=1,
        remove_unused_columns=False,
        report_to=None,
        max_steps=2  # Sadece 2 step (ultra-fast test)
    )

    # ✅ Fixed: processing_class kullan
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        processing_class=tokenizer  # Search results fix
    )

    print(f"🎯 {len(micro_data)} örnek, {training_args.max_steps} steps")
    print("⏱️ Target: 5 dakika")

    # Training başlat
    trainer.train()

    elapsed = time.time() - start_time
    print(f"✅ Training tamamlandı! Süre: {elapsed / 60:.1f} dakika")

    # Model kaydet
    model.save_pretrained('./micro_trained_model')
    print("💾 Model kaydedildi: ./micro_trained_model")

    return True


if __name__ == "__main__":
    start_micro_training()
