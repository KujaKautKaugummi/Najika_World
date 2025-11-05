#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 NAJIKA LORA TRAINING - QWEN2.5 7B (DEPLOYMENT-READY) 🚀

Qwen2.5 7B für besseres Deutsch und Character-Roleplay!

EIGENSCHAFTEN:
- Qwen2.5 7B Base-Model (besser für Deutsch!)
- Passt in 8GB VRAM (4-bit quantized + LoRA)
- LoRA zu GGUF Export möglich
- Deployment zu Ollama via ADAPTER directive

VERWENDUNG:
  python najika_lora_training_3b.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
import torch
from datetime import datetime
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training
)
from datasets import Dataset

# ChromaDB Import
from najika_memory import NajikaMemory

class NajikaLoRATrainer3B:
    """LoRA Fine-Tuning für Qwen2.5 7B (passt in 8GB!)"""

    def __init__(
        self,
        base_model="Qwen/Qwen2.5-7B-Instruct",  # Qwen2.5 7B für besseres Deutsch!
        output_dir="C:/Najika-World/lora_checkpoints",
        logs_dir="C:/Najika-World/training_logs"
    ):
        self.base_model = base_model
        self.output_dir = output_dir
        self.logs_dir = logs_dir

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)

        self.memory = NajikaMemory()

        self.training_log = {
            "start_time": datetime.now().isoformat(),
            "base_model": base_model,
            "model_size": "7B",
            "deployment_ready": True,
            "training_samples": 0,
            "status": "initializing"
        }

        print("=" * 60)
        print("NAJIKA LoRA TRAINING - QWEN2.5 7B")
        print("=" * 60)
        print(f"Basis-Modell: {base_model}")
        print(f"Größe: 7B (Qwen2.5 für besseres Deutsch!)")
        print(f"Output: {output_dir}")
        print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
        print()

    def prepare_training_data(self, min_samples=10):
        """Lädt Training-Daten aus ChromaDB"""
        print("📚 Lade Training-Daten...")

        try:
            all_convs = self.memory.conversations.get()

            if not all_convs['documents'] or len(all_convs['documents']) < min_samples:
                print(f"❌ Zu wenig Daten! Brauche {min_samples}, habe {len(all_convs['documents'])}")
                return None

            conversations = []

            for i in range(0, len(all_convs['documents']) - 1, 2):
                user_msg = all_convs['documents'][i]
                najika_msg = all_convs['documents'][i + 1]

                formatted = self._format_qwen_chat(user_msg, najika_msg)
                conversations.append({"text": formatted})

            print(f"✅ {len(conversations)} Konversationen geladen")

            dataset = Dataset.from_list(conversations)
            self.training_log['training_samples'] = len(conversations)

            return dataset

        except Exception as e:
            print(f"❌ Fehler beim Laden: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _format_qwen_chat(self, user_msg, assistant_msg):
        """Formatiert als Qwen2.5 Chat Template"""
        return f"""<|im_start|>user
{user_msg}<|im_end|>
<|im_start|>assistant
{assistant_msg}<|im_end|>"""

    def train(self, epochs=10, batch_size=1, learning_rate=2e-4):
        """Training mit Qwen2.5 7B-Modell"""
        print("\n🚀 Starte LoRA Training (Qwen2.5 7B)...")
        print(f"Epochs: {epochs}")
        print(f"Batch Size: {batch_size}")
        print()

        # 1. Training-Daten
        dataset = self.prepare_training_data()
        if dataset is None:
            return False

        # 2. 4-bit Config
        print("⚙️  Lade Modell (4-bit)...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )

        # 3. Base Model laden
        try:
            model = AutoModelForCausalLM.from_pretrained(
                self.base_model,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )

            tokenizer = AutoTokenizer.from_pretrained(
                self.base_model,
                trust_remote_code=True
            )
            tokenizer.pad_token = tokenizer.eos_token

            print("✅ Modell geladen!")

        except Exception as e:
            print(f"❌ Fehler: {e}")
            return False

        # 4. LoRA Config
        print("⚙️  LoRA Config...")
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )

        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, lora_config)

        print("✅ LoRA aktiviert!")
        model.print_trainable_parameters()

        # 5. Training Args
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_dir = os.path.join(self.output_dir, f"najika_lora_qwen_{timestamp}")

        training_args = TrainingArguments(
            output_dir=checkpoint_dir,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,  # Qwen2.5 7B größer als 3B
            num_train_epochs=epochs,
            learning_rate=learning_rate,
            fp16=True,
            logging_steps=10,
            save_steps=50,
            save_total_limit=2,
            report_to="none",
            optim="paged_adamw_8bit",
            warmup_steps=10,
            lr_scheduler_type="cosine"
        )

        # 6. Tokenize
        print("\n⚙️  Tokenize...")

        def tokenize_function(examples):
            return tokenizer(
                examples["text"],
                truncation=True,
                max_length=512,
                padding="max_length"
            )

        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )

        print(f"✅ {len(tokenized_dataset)} Samples tokenized")

        # 7. Data Collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )

        # 8. Trainer
        print("\n🎓 Starte Training...")
        print(f"Checkpoint: {checkpoint_dir}")
        print()

        trainer = Trainer(
            model=model,
            train_dataset=tokenized_dataset,
            args=training_args,
            data_collator=data_collator
        )

        # 9. TRAIN!
        self.training_log['status'] = "training"

        try:
            trainer.train()

            # 10. Speichern
            print("\n💾 Speichere LoRA Adapter...")
            final_adapter = os.path.join(self.output_dir, "najika_lora_latest")
            trainer.model.save_pretrained(final_adapter)
            tokenizer.save_pretrained(final_adapter)

            print(f"✅ Adapter gespeichert: {final_adapter}")

            self.training_log['status'] = "completed"
            self.training_log['end_time'] = datetime.now().isoformat()
            self.training_log['adapter_path'] = final_adapter

            # Log speichern
            log_file = os.path.join(self.logs_dir, f"training_qwen_{timestamp}.json")
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_log, f, indent=2, ensure_ascii=False)

            print(f"📊 Training-Log: {log_file}")
            print()
            print("=" * 60)
            print("✅ TRAINING ABGESCHLOSSEN (QWEN2.5)!")
            print("=" * 60)
            print()
            print("Next Step: LoRA zu GGUF konvertieren")
            print("  Dann in Ollama Modelfile mit ADAPTER directive einbinden")
            print()

            return True

        except Exception as e:
            print(f"❌ Training-Fehler: {e}")
            import traceback
            traceback.print_exc()
            self.training_log['status'] = "failed"
            self.training_log['error'] = str(e)
            return False

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("NAJIKA LoRA FINE-TUNING (QWEN2.5 7B)")
    print("Deployment-Ready für RTX 3060 Ti (8GB)")
    print("=" * 60)
    print()

    # Prüfe CUDA
    if not torch.cuda.is_available():
        print("⚠️  CUDA nicht verfügbar!")
        response = input("Trotzdem fortfahren? (j/n): ")
        if response.lower() != 'j':
            sys.exit(0)
    else:
        print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        print(f"✅ VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        print()

    # Training
    trainer = NajikaLoRATrainer3B()

    success = trainer.train(
        epochs=10,
        batch_size=1,  # Qwen2.5 7B braucht mehr VRAM
        learning_rate=2e-4
    )

    if success:
        print("🎉 Training erfolgreich!")
        print("Qwen2.5 7B LoRA kann jetzt zu GGUF konvertiert werden!")
    else:
        print("❌ Training fehlgeschlagen")
