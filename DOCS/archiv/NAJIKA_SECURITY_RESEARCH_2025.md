# NAJIKA SECURITY & OPTIMIZATION RESEARCH 2025
**Research Date:** 2025-11-11
**Sources:** Google, Reddit, XDA Forums, Apple Security Docs, Unity/Unreal Docs

---

## 🔐 ANDROID SECURITY FINDINGS (2025)

### **1. Biometric Authentication (BIOMETRIC_STRONG)**
```
✅ IMPLEMENTATION: BiometricPrompt API
✅ FALLBACK: Device Credentials (PIN/Pattern) required
✅ CRYPTO: CryptoObject integration for biometric-protected keys
✅ RE-AUTH: Primary authentication every 72 hours mandatory
✅ ANDROID 14: Improved fallback behavior
```

**Najika Use:**
- Voice Call activation (biometric unlock)
- Alcatraz Mode unlock
- Private Mode toggle

---

### **2. Android Keystore + TEE (Trusted Execution Environment)**
```
✅ HARDWARE: Keys NEVER leave secure hardware
✅ LEVELS:
   - TRUSTED_ENVIRONMENT (TrustZone/TEE)
   - STRONGBOX (Secure Element - höchste Sicherheit!)
✅ API: AndroidKeyStore Provider
✅ PROCESS: KeyMint TA runs in TrustZone
✅ ISOLATION: Key material NEVER enters app process
```

**Najika Use:**
- Verschlüsselung von Najika State (najika_state.json)
- Voice Call Audio verschlüsselt
- ChromaDB Encryption Keys
- Private Mode Content

**Implementation:**
```kotlin
val keyGenerator = KeyGenerator.getInstance(
    KeyProperties.KEY_ALGORITHM_AES,
    "AndroidKeyStore"
)
val keyGenParameterSpec = KeyGenParameterSpec.Builder(
    "najika_master_key",
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .setUserAuthenticationValidityDurationSeconds(300) // 5 min
    .build()
keyGenerator.init(keyGenParameterSpec)
val secretKey = keyGenerator.generateKey()
```

---

### **3. Encrypted SharedPreferences (Jetpack Security)**
```
✅ ENCRYPTION: AES-256 for keys AND values
✅ LIBRARY: androidx.security.crypto
✅ AUTO: Device-specific key from Keystore
```

**Najika Use:**
- User Settings
- API Keys
- Session Tokens

**Implementation:**
```kotlin
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val sharedPreferences = EncryptedSharedPreferences.create(
    context,
    "najika_secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```

---

### **4. Play Integrity API (SafetyNet Replacement)**
```
✅ USE: App integrity verification
✅ DETECT: Rooted devices, tampered apps
✅ 2025: Standard for security checks
```

**Najika Use:**
- Prüft ob System kompromittiert
- Warnung bei Root/Tampering
- Alcatraz Mode Auto-Trigger

---

## 🍎 APPLE SECURITY FEATURES (Inspiration for Android)

### **1. Secure Enclave (Apple)**
```
✅ ISOLATION: Separate processor for sensitive data
✅ DATA: Face ID, Touch ID, Encryption Keys
✅ BACKUP: NEVER backed up to iCloud
✅ ACCESS: Even Apple can't access it
```

**Android Equivalent:** TEE/StrongBox Keystore

---

### **2. Lockdown Mode (iOS 16+, Kernel-Level since iOS 17!)**
```
✅ LEVEL: Kernel-level protection (can't be undone without reboot!)
✅ DAEMON: /System/Library/PrivateFrameworks/LockdownMode.framework/lockdownmoded
✅ KEXT: com.apple.driver.AppleLockdownMode
✅ RESTRICTIONS:
   - FaceTime: Only contacts from last 30 days
   - Messages: No links, no attachments (except images)
   - Web: No JIT compilation
   - Location: Removed from shared photos
   - USB: Restricted when locked
```

**Najika "Alcatraz Mode" (inspired by Lockdown):**
```
✅ TRIGGER: Duress PIN, Remote SMS, 3x Shake
✅ ACTIONS:
   - Lock device immediately
   - Hide Najika data (encrypted)
   - Show FAKE decoy screen
   - Disable all network (except emergency)
   - Kill all background processes
   - Log all access attempts
   - Optional: Remote wipe after X failed attempts
```

**Implementation Plan:**
```kotlin
class AlcatrazMode {
    fun activate(trigger: TriggerType) {
        // 1. Immediate lock
        devicePolicyManager.lockNow()

        // 2. Network kill
        afwallKillAllConnections()

        // 3. Encrypt sensitive data
        najikaStateManager.emergencyEncrypt()

        // 4. Show decoy
        startActivity(Intent(context, DecoyLockscreenActivity::class.java))

        // 5. Alert backup device
        sendEmergencySMS("Alcatraz activated at ${System.currentTimeMillis()}")

        // 6. Enable paranoid logging
        enableKernelAudit()
    }
}
```

---

## 🎮 GAME DEV OPTIMIZATION (Unity/Unreal - 2025)

### **Unity Android Optimization**

#### **1. Adaptive Performance**
```
✅ REAL-TIME: Adapts to thermal/performance
✅ SCALERS: Framerate, Resolution, LOD, Quality
✅ BATTERY: Avoids unnecessary GPU work
✅ API: Android Performance Tuner
```

**Implementation:**
```csharp
// Unity Adaptive Performance
using UnityEngine.AdaptivePerformance;

var perf = Holder.Instance;
perf.Active = true;

// Auto-adjust quality based on thermals
var thermalManager = perf.ThermalStatus;
if (thermalManager.WarningLevel >= WarningLevel.Throttling) {
    QualitySettings.SetQualityLevel(0); // Low quality
}
```

#### **2. Frame Pacing (Optimized Frame Pacing)**
```
✅ ENABLE: Project Settings > Player > Android > Optimized Frame Pacing
✅ BENEFIT: Smooth gameplay, less battery drain
✅ AVOID: Unnecessary display updates (60 FPS on 120 Hz screen)
✅ RESULT: Mir 2 dropped "Slow Sessions" from 40% to 10%!
```

**Najika Use:**
- 3D World rendering (60 FPS target)
- Battery-aware FPS scaling
- Thermal throttling prevention

#### **3. Battery Optimization**
```
✅ VSYNC: Use for precise frame timing
✅ ADAPTIVE: Scale down quality when battery low
✅ IDLE: Reduce FPS when idle (e.g. 10 FPS on lock screen)
```

---

### **Unreal Engine Mobile**
```
✅ POWER: High-quality visuals
✅ DOWNSIDE: Battery drain if not optimized
✅ 2025: Built-in mobile optimization tools
```

**Najika:** Stick with Unity or native Kotlin (besser für Battery!)

---

## 🔥 LINEAGEOS CUSTOM ROM (Xiaomi 11T Pro - vili)

### **Device Info**
```
CODENAME: vili (NOT alioth!)
DEVICE: Xiaomi 11T Pro
SOC: Snapdragon 888
RAM: 8GB/12GB
STORAGE: 128GB/256GB
DISPLAY: 6.67" AMOLED 120Hz
```

### **Current Status (Nov 2025)**
```
✅ LineageOS 23.0 (Android 16) - UNOFFICIAL
✅ LineageOS 22.2 (Android 15) - UNOFFICIAL
✅ Last Build: October 27, 2025
✅ STATUS: All hardware working (VoIP, Wi-Fi calling, Dolby Atmos, etc.)
✅ ALTERNATIVE: crDroid v12.2 (OFFICIAL!)
```

### **Build Requirements (Android 14+)**
```
RAM: 64GB (or 32GB + 16GB ZRAM)
OS: Ubuntu 22.04
DISK: 200GB+ free space
CCACHE: 25-100GB (reduces build time from 1h to 20min!)
```

### **Build Commands**
```bash
# 1. Setup
repo init -u https://github.com/LineageOS/android.git -b lineage-23.0
repo sync -j$(nproc)

# 2. Build
source build/envsetup.sh
breakfast vili
export USE_CCACHE=1
ccache -M 50G
brunch vili

# 3. Flash
adb reboot bootloader
fastboot flash boot boot.img
fastboot flash vendor_boot vendor_boot.img
fastboot flash system system.img
fastboot reboot
```

---

## 🛡️ XDA SECURITY HARDENING (2025 Golden Standard)

### **Ultimate Privacy Setup (Root Required)**

#### **1. AFWall+ (iptables Firewall)**
```
✅ ROOT: Required for kernel-level control
✅ TECH: Linux iptables framework
✅ UPDATED: Oct 2025 (v4.0.0)
✅ FEATURES:
   - Per-app network control
   - Multiple profiles
   - VPN/LAN/Tether control
   - Tasker integration
   - Material Design UI
✅ BINARIES: busybox v1.36.1, iptables v1.8.10
```

**vs NetGuard (No Root):**
```
❌ NetGuard: Uses VPN slot (can't use real VPN!)
✅ AFWall+: iptables (VPN slot free!)
```

#### **2. Net Switch Magisk Module**
```
✅ FUNCTION: Completely rejects network for all apps
✅ INTEGRATION: AFWall+ via iptables
✅ USE: Maximum network isolation
```

#### **3. Kernel Hardening**
```
✅ SELinux: Enforcing mode
✅ AppArmor: Profile-based security
✅ Verity: Verified boot (dm-verity)
✅ Audit: Kernel audit logging
```

---

## 📦 NAJIKA FEATURE-MODULE MATRIX

| Feature | Digivice App | LineageOS ROM | Jetson | Priority |
|---------|--------------|---------------|--------|----------|
| **CORE FEATURES** |
| Voice Calls (Whisper STT + Coqui TTS) | ✅ WebView | ✅ Native Service | ✅ Native | P0 |
| Chat (Text AI) | ✅ WebView | ✅ Native | ✅ Native | P0 |
| 3D World | ✅ WebView/Unity | ✅ Unity APK | ✅ Qt3D | P1 |
| Tamagotchi System | ✅ WebView | ✅ Native | ✅ Native | P0 |
| Memory (ChromaDB) | 🔄 Server | 🔄 Server | ✅ Local | P0 |
| **SECURITY** |
| Biometric Auth | ✅ BiometricPrompt | ✅ System-Level | ❌ N/A | P0 |
| Encrypted Storage | ✅ Keystore | ✅ Keystore | ✅ LUKS2 | P0 |
| Alcatraz Mode | ✅ App-Level | ✅ System-Level | ✅ Kernel | P1 |
| Firewall (AFWall+) | ⚠️ Root Only | ✅ Pre-installed | ✅ iptables | P1 |
| VPN (WireGuard) | ✅ System VPN | ✅ Built-in | ✅ NetworkManager | P1 |
| **SENSORS** |
| Camera (Scanner) | ✅ CameraX API | ✅ Native | ✅ V4L2 | P0 |
| Microphone (Voice) | ✅ MediaRecorder | ✅ Native | ✅ ALSA/Pulse | P0 |
| Face Recognition | ✅ ML Kit | ✅ ML Kit | ✅ OpenCV | P2 |
| YOLO Object Detection | 🔄 Server | 🔄 Server | ✅ TensorRT | P2 |
| **PERFORMANCE** |
| Adaptive Performance | ✅ Android API | ✅ System | ❌ Desktop | P1 |
| Battery Optimization | ✅ Doze/JobScheduler | ✅ Enhanced | ❌ AC Power | P0 |
| Frame Pacing | ✅ Unity/Native | ✅ System | ❌ N/A | P1 |
| **CONNECTIVITY** |
| Bluetooth | ✅ System BT | ✅ System | ✅ BlueZ | P2 |
| NFC | ✅ System NFC | ✅ System | ❌ N/A | P2 |
| GPS | ✅ Location API | ✅ System | ✅ gpsd | P2 |

**Legend:**
- ✅ = Fully Supported
- 🔄 = Backend Server (HTTP API)
- ⚠️ = Limited/Conditional
- ❌ = Not Applicable
- P0 = Critical, P1 = High, P2 = Nice-to-Have

---

## 🚀 DEVELOPMENT PRIORITY

### **Phase 1: Digivice APK (NOW - DEC 2025)**
```
1. WebView Wrapper (Quick Test - 1 Day)
2. Native Voice Calls (CameraX + MediaRecorder - 1 Week)
3. Biometric Auth (BiometricPrompt - 2 Days)
4. Encrypted Storage (Keystore - 3 Days)
5. Battery Optimization (Adaptive Performance - 3 Days)
6. Testing auf Xiaomi 11T Pro
```

### **Phase 2: LineageOS Custom ROM (JAN-FEB 2026)**
```
1. Build Environment Setup
2. Add Najika System Apps (/system/priv-app)
3. AFWall+ Pre-installation
4. Security Hardening (SELinux, Verity)
5. Alcatraz Mode (System-Level)
6. Flash & Test
```

### **Phase 3: Jetson Port (MÄR 2026)**
```
1. Backend Migration (Python - direkt kopieren!)
2. Qt/QML UI Development
3. TensorRT Optimization (YOLO, etc.)
4. Dual-Display Setup
5. Final Polish
```

---

## 💡 KEY TAKEAWAYS

### **Android Security (2025):**
- BiometricPrompt + TEE Keystore = Beste Security
- Play Integrity API statt SafetyNet
- Encrypted SharedPreferences für alle Daten

### **Apple Inspiration:**
- Lockdown Mode → Najika "Alcatraz Mode"
- Kernel-level protection (seit iOS 17)
- Secure Enclave = Android TEE/StrongBox

### **Game Dev:**
- Unity Adaptive Performance = Battery Hero
- Frame Pacing = 40% weniger Lag (Mir 2 Proof!)
- VSync + Doze = Maximum Battery Life

### **LineageOS:**
- Xiaomi 11T Pro (vili) = LineageOS 23.0 verfügbar!
- Unofficial aber STABIL (Oct 2025)
- crDroid = Official Alternative

### **XDA Security:**
- AFWall+ > NetGuard (VPN frei!)
- Root = Maximum Control
- 2025 Golden Standard Setup verfügbar

---

**NEXT:** Implement in Digivice APK! 🔥
