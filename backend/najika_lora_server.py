#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 NAJIKA LORA INFERENCE SERVER 🚀

Lädt das LoRA-Modell und bietet API an (parallel zu Ollama)
najika_server.py kann dann wählen: Ollama ODER LoRA-Server
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# ===== CONFIG =====

LORA_ADAPTER = "C:/Najika_World/lora_checkpoints/najika_lora_latest"
BASE_MODEL = "unsloth/Meta-Llama-3.1-8B-Instruct"
PORT = 11435  # Port 11435 (Ollama ist 11434)

print("=" * 60)
print("🚀 NAJIKA LORA INFERENCE SERVER")
print("=" * 60)
print(f"LoRA: {LORA_ADAPTER}")
print(f"Base: {BASE_MODEL}")
print(f"Port: {PORT}")
print()

# ===== LOAD MODEL =====

print("⚙️  Lade Model (4-bit)...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

try:
    # Lade Base Model
    print("  → Base Model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        offload_folder="C:/Najika_World/offload_temp"  # Nutze Disk für Offload
    )

    # Lade Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    # Lade LoRA Adapter
    print("  → LoRA Adapter...")
    model = PeftModel.from_pretrained(
        base_model,
        LORA_ADAPTER,
        offload_folder="C:/Najika_World/offload_temp"
    )

    print("✅ Model geladen!")
    print()

except Exception as e:
    print(f"❌ Model-Fehler: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ===== API SERVER =====

class NajikaHandler(BaseHTTPRequestHandler):
    """API Handler (Ollama-kompatibel)"""

    def do_POST(self):
        if self.path == "/api/generate":
            self.handle_generate()
        else:
            self.send_error(404)

    def handle_generate(self):
        """Generiere Antwort (wie Ollama)"""
        try:
            # Lese Request
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            prompt = data.get('prompt', '')

            # Generiere
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.8,
                    top_p=0.9,
                    do_sample=True
                )

            response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extrahiere nur den generierten Teil (nach dem Prompt)
            generated = response_text[len(prompt):].strip()

            # Sende Response (Ollama-Format)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            response_data = {
                "model": "najika-lora",
                "created_at": "",
                "response": generated,
                "done": True
            }

            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except Exception as e:
            print(f"❌ Generation Error: {e}")
            import traceback
            traceback.print_exc()

            self.send_error(500)

    def log_message(self, format, *args):
        """Unterdrücke HTTP-Logs"""
        pass

# ===== START SERVER =====

print("🚀 Starte Server...")
print(f"API: http://localhost:{PORT}/api/generate")
print()
print("Test mit:")
print(f'  curl -X POST http://localhost:{PORT}/api/generate -d \'{{"prompt":"Hallo Najika!"}}\'')
print()
print("Press Ctrl+C to stop")
print("=" * 60)
print()

server = HTTPServer(('0.0.0.0', PORT), NajikaHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n\n✅ Server gestoppt")
    server.shutdown()
