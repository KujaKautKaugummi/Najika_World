# NAJIKA JETSON MIGRATION PLAN

**Target:** NVIDIA Jetson AGX Orin 64GB
**Timeline:** Q1-Q2 2026
**Goal:** Standalone Portable Najika System

---

## HARDWARE REQUIREMENTS

### Jetson AGX Orin 64GB Specs
- 275 TFLOPS (INT8)
- 64GB LPDDR5 RAM
- 64GB eMMC + NVMe SSD Slot
- 2x HDMI (dual display support!)
- 4x USB 3.2
- 2x USB 2.0
- Gigabit Ethernet
- M.2 Key M (NVMe SSD)
- 40-pin GPIO header
- **Power:** 15-60W (adjustable)

### Additional Hardware
- [x] 7" HDMI Touchscreen (1024x600) - ~60€
- [x] NVMe SSD 512GB (M.2 2280) - ~50€
- [x] Powerbank 30000mAh (100W PD) - ~50€
- [x] USB-C Hub (HDMI, USB-A x3, Ethernet) - ~30€
- [x] Wireless Keyboard + Mouse - ~30€
- [x] USB Webcam (1080p) OR use built-in if available
- [x] USB Microphone OR use webcam mic
- [x] Custom Case (3D print or buy)

**Total:** ~940€ (Jetson gebraucht) to ~1140€ (neu)

---

## SOFTWARE STACK (ARM64 COMPATIBLE)

### Base System ✅
- **OS:** JetPack 6.0 (Ubuntu 22.04 LTS ARM64)
- **Python:** 3.10+ (pre-installed)
- **Docker:** ARM64 support ✅
- **Git:** Native ARM ✅

### AI/ML Stack ✅
- **Ollama:** ARM64 builds available! ✅
  - Llama 3.1 8B
  - Llama 3.1 70B (4-bit quantized)
  - Qwen 2.5 7B/72B
- **PyTorch:** NVIDIA optimized for Jetson ✅
- **Unsloth:** ARM64 compatible ✅
- **Transformers:** Hugging Face ARM support ✅

### Vision Stack ✅
- **YOLO v8:** Ultralytics Jetson-optimized ✅
- **MediaPipe:** Google ARM64 builds ✅
- **OpenCV:** CUDA-enabled for Jetson ✅

### Audio Stack ✅
- **Whisper:** OpenAI (runs on ARM via PyTorch) ✅
- **Faster-Whisper:** CTranslate2 ARM support ✅
- **Coqui TTS:** ARM64 compatible ✅
- **PortAudio:** Native ARM ✅

### Database ✅
- **ChromaDB:** Pure Python, ARM compatible ✅
- **SQLite:** Built-in ✅

### Web Stack ✅
- **Flask:** Pure Python ✅
- **Node.js:** ARM64 official builds ✅

---

## MIGRATION CHECKLIST

### Pre-Migration (NOW - DEC 2025)

**Training:**
- [ ] Maximize training on PC (8-10h nightly)
- [ ] Collect all LoRA checkpoints
- [ ] Document best-performing configs
- [ ] Create training baseline metrics

**Code Preparation:**
- [x] All Python scripts (platform-independent) ✅
- [ ] Test Docker containers (build ARM64 images)
- [ ] Document all dependencies
- [ ] Create requirements.txt (verified ARM64)
- [ ] Port-forward test (Jetson IP setup)

**Data Backup:**
- [ ] Backup ChromaDB (C:\NajikaFinal\memory_db)
- [ ] Backup all LoRA checkpoints (C:\Najika-World\lora_checkpoints)
- [ ] Backup najika_state.json
- [ ] Export training logs
- [ ] Backup voice models (Coqui TTS)

---

### Jetson Purchase (JAN-MAR 2026)

**Shopping List:**
```
[ ] Jetson AGX Orin 64GB Dev Kit
    - Check: eBay, Amazon Warehouse, NVIDIA Shop
    - Target: ~700€ (gebraucht) or ~900€ (neu)
    - Verify: Includes heatsink/fan, power supply

[ ] 7" HDMI Touchscreen
    - Model: Waveshare 7" HDMI LCD (C) or similar
    - Resolution: 1024x600 minimum
    - Touch: Capacitive (better than resistive)

[ ] NVMe SSD 512GB
    - Form: M.2 2280
    - Type: NVMe (not SATA!)
    - Brand: Samsung, WD, Crucial

[ ] Powerbank 30000mAh
    - Output: 100W PD (USB-C)
    - Example: Anker PowerCore III Elite

[ ] USB-C Hub
    - Ports: 3x USB-A, 1x HDMI, 1x Ethernet
    - Power: PD Pass-through

[ ] Wireless Keyboard/Mouse
    - Combo: Logitech K400+ or similar
    - Compact for portable use
```

---

### Initial Setup (WEEK 1)

**Day 1: OS Installation**
```bash
# Flash JetPack 6.0 via NVIDIA SDK Manager
# OR use pre-flashed SD card

# First boot:
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl wget vim
```

**Day 2: Development Tools**
```bash
# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Python packages
pip3 install --upgrade pip
pip3 install virtualenv

# VS Code (ARM64)
wget https://code.visualstudio.com/sha/download?build=stable&os=linux-arm64
sudo dpkg -i code_*.deb
```

**Day 3: Ollama Setup**
```bash
# Install Ollama (ARM64 version)
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.1:8b
ollama pull llama3.1:70b-instruct-q4_0  # 4-bit quantized for 64GB!
ollama pull qwen2.5:7b
```

**Day 4: NVIDIA Tools**
```bash
# CUDA Toolkit (included in JetPack)
# TensorRT (included)
# cuDNN (included)

# Verify:
python3 -c "import torch; print(torch.cuda.is_available())"  # Should be True
jtop  # Jetson monitoring tool
```

---

### Najika Migration (WEEK 2)

**Step 1: Transfer Files**
```bash
# On PC: Create backup archive
cd C:\Najika_World
tar -czf najika_backup.tar.gz backend/ digivice/ saves/

# Transfer to Jetson
scp najika_backup.tar.gz jetson@<JETSON_IP>:~/
```

**Step 2: Setup Environment**
```bash
# On Jetson
mkdir -p ~/Najika_World
cd ~/Najika_World
tar -xzf ~/najika_backup.tar.gz

# Install Python dependencies
cd backend
pip3 install -r requirements.txt
```

**Step 3: ChromaDB Migration**
```bash
# Transfer ChromaDB
scp -r C:\NajikaFinal\memory_db jetson@<IP>:~/NajikaFinal/

# Test
python3 -c "from najika_memory_enhanced import NajikaMemoryEnhanced; mem = NajikaMemoryEnhanced(); print('OK!')"
```

**Step 4: LoRA Checkpoints**
```bash
# Transfer all LoRA checkpoints
scp -r C:\Najika-World\lora_checkpoints jetson@<IP>:~/Najika-World/

# Verify
ls -lh ~/Najika-World/lora_checkpoints/
```

**Step 5: Test Server**
```bash
cd ~/Najika_World/backend
python3 najika_server.py

# Test from PC browser:
# http://<JETSON_IP>:8000/digivice/
```

---

### Hardware Integration (WEEK 3)

**Touchscreen Setup**
```bash
# Connect 7" HDMI Display
# Auto-detected by JetPack

# Configure touch input
sudo apt install -y xinput-calibrator
xinput_calibrator  # Follow on-screen instructions

# Set resolution
xrandr --output HDMI-1 --mode 1024x600
```

**Webcam Setup**
```bash
# Test webcam
sudo apt install -y v4l-utils
v4l2-ctl --list-devices

# Test in Python
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK!' if cap.isOpened() else 'FAIL')"
```

**Microphone Setup**
```bash
# Test microphone
arecord -l  # List devices
arecord -d 5 test.wav  # Record 5 seconds
aplay test.wav  # Playback
```

**Powerbank Test**
```bash
# Install battery monitoring
sudo apt install -y powertop

# Test runtime
# Full charge → Run Najika → Measure hours
# Target: 4-8 hours on 30000mAh
```

---

### Performance Optimization (WEEK 4)

**Power Modes**
```bash
# Max performance (60W)
sudo nvpmodel -m 0

# Balanced (30W)
sudo nvpmodel -m 2

# Power save (15W)
sudo nvpmodel -m 8

# Check current mode
sudo nvpmodel -q
```

**CUDA Optimization**
```bash
# Enable max GPU clocks
sudo jetson_clocks

# Monitor performance
jtop  # Real-time monitoring
```

**Ollama Optimization**
```bash
# Set environment variables
export OLLAMA_NUM_PARALLEL=2  # Run 2 models parallel (64GB allows this!)
export OLLAMA_MAX_LOADED_MODELS=2

# Test Llama 70B
ollama run llama3.1:70b-instruct-q4_0 "Test prompt"
```

---

## NEW FEATURES (MAY-JUNE 2026)

### Computer Vision

**YOLO v8 Integration**
```python
# backend/najika_vision.py
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # Nano for speed
results = model(frame)

# Object Detection → Scanner function!
```

**Face Recognition**
```python
import mediapipe as mp

face_mesh = mp.solutions.face_mesh.FaceMesh()
# Detect faces, expressions, emotions
```

### Audio Processing

**Whisper Large**
```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="int8")
# Best STT quality!
```

**Audio Anomaly Detection**
```python
# Classify sounds: gunshot, glass break, scream, etc.
# Pre-trained models on Hugging Face
```

---

## DIGIVICE BUILD (JULY 2026+)

### Case Design
- 3D printable STL (custom design)
- OR buy: Pelican case + foam cutout
- OR professional: CNC aluminum (expensive!)

### Features
- Cutout for 7" screen
- Ventilation holes (Jetson gets warm!)
- USB-C charging port access
- Volume buttons (GPIO-controlled)
- Power button
- Status LED (RGB, GPIO-controlled)

### Software Polish
- Boot animation (Najika logo)
- Startup sound (Megumin: "EXPLOSION!")
- Sleep mode (motion sensor wake)
- Auto-brightness (ambient light sensor)

---

## DUAL-DISPLAY MODE

**Portable Mode:**
- 7" Touchscreen only
- Battery-powered
- Najika Digivice!

**Desktop Mode:**
- HDMI to large monitor (1080p/4K)
- Keyboard + Mouse
- AC-powered (max performance)
- Like a PC!

**Setup:**
```bash
# Detect displays
xrandr

# Dual display (extend)
xrandr --output HDMI-0 --primary --mode 1920x1080 --output HDMI-1 --mode 1024x600 --right-of HDMI-0

# Mirror displays
xrandr --output HDMI-1 --same-as HDMI-0
```

---

## BENCHMARKS (TARGET)

### Inference Speed
- Llama 3.1 8B: 25-30 tokens/sec ✅
- Llama 3.1 70B (4-bit): 8-10 tokens/sec ✅
- YOLO v8 (640x640): 30-40 FPS ✅
- Whisper Large: Real-time (<1sec latency) ✅

### Training Speed
- LoRA (8B, 4-bit): ~2-3h per epoch
- LoRA (70B, 4-bit): ~8-12h per epoch
- **OK for overnight training!**

### Battery Life
- Idle (screen on): 8-10h
- Chatting (Llama 8B): 6-8h
- Intensive (Llama 70B + Vision): 4-6h
- **Target: Full day usage!**

---

## BACKUP STRATEGY

**Daily:**
- ChromaDB auto-backup to NVMe SSD
- State JSON backup

**Weekly:**
- Full system backup to external HDD
- Sync to PC (if still available)

**Monthly:**
- Cloud backup (optional, encrypted!)
- LoRA checkpoint archive

---

## TROUBLESHOOTING

### Common Issues

**Ollama slow:**
- Check: `sudo jetson_clocks` enabled?
- Check: Power mode (nvpmodel -m 0)
- Check: Thermal throttling (jtop)

**Out of memory:**
- 64GB should be enough for Llama 70B 4-bit
- If not: Try 3-bit quantization
- Close other apps

**Touchscreen not working:**
- Re-calibrate: `xinput_calibrator`
- Check drivers: `dmesg | grep input`

**Low FPS (Vision):**
- Use smaller YOLO model (yolov8n)
- Lower resolution (640x480)
- Enable CUDA optimizations

---

## COST BREAKDOWN

```
HARDWARE:
- Jetson AGX Orin 64GB:  700€ (gebraucht) / 900€ (neu)
- 7" Touchscreen:         60€
- NVMe SSD 512GB:         50€
- Powerbank 30000mAh:     50€
- USB-C Hub:              30€
- Keyboard/Mouse:         30€
- Custom Case:            20€ (3D print) / 100€ (professional)

TOTAL (gebraucht): ~940€
TOTAL (neu):      ~1140€
```

---

## TIMELINE SUMMARY

**Now - Dec 2025:** Training on PC, Code prep
**Jan-Mar 2026:** Purchase Jetson + Hardware
**April 2026:** Setup & Migration (4 weeks)
**May-June 2026:** New Features (Vision, Audio)
**July 2026+:** Polish, Digivice case, final touches

**GOAL:** Portable standalone Najika by Summer 2026! 🔥

---

## FALLBACK PLAN

**If Jetson too expensive / not available:**
- **Alternative 1:** Jetson AGX Xavier (32GB) - cheaper, still good!
- **Alternative 2:** Raspberry Pi 5 (8GB) - very cheap, slower but works!
- **Alternative 3:** Mini PC (x86) - more power, less portable

**Priority:** Portable > Performance
**Najika's goal:** ALWAYS be with you! 💜

---

**Last updated:** 2025-11-11
**Status:** PLANNING PHASE
**Next milestone:** JETSON PURCHASE Q1 2026
