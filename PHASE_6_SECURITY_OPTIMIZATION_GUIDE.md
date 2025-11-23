# PHASE 6: SECURITY & OPTIMIZATION - COMPLETE GUIDE
**Model 1 - Digivice APK**
**Datum:** 2025-11-11
**Phase:** 6 - Security & Optimization (Woche 9)
**Dauer:** 1 Woche

---

## 🎯 PHASE 6 ÜBERSICHT

### **Was wird gebaut:**
```
✅ Biometric Authentication (Android Keystore + BiometricPrompt)
✅ Encrypted Storage (EncryptedSharedPreferences)
✅ Network Security (HTTPS, Certificate Pinning)
✅ Performance Optimization (LOD, Culling, Texture Streaming)
✅ Battery Optimization (Adaptive Performance)
✅ Memory Management
✅ Security Best Practices (Alcatraz Integration)
```

---

## 🔐 TODO 6.1: BIOMETRIC AUTHENTICATION

### **Android Integration (Java/Kotlin + JNI):**

#### **1. Create Android Plugin:**

```
Location: C:\NajikaDigivice_UE5\Plugins\NajikaBiometric\

Files:
- NajikaBiometric.uplugin
- Source/NajikaBiometric/
  - NajikaBiometric.Build.cs
  - Public/BiometricAuth.h
  - Private/BiometricAuth.cpp
  - Java/BiometricHelper.java (Android)
```

#### **2. BiometricHelper.java (Android Native):**

```java
// Location: Plugins/NajikaBiometric/Source/NajikaBiometric/Java/BiometricHelper.java

package com.najika.biometric;

import android.app.Activity;
import android.content.Context;
import android.os.Build;
import androidx.biometric.BiometricPrompt;
import androidx.biometric.BiometricManager;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.FragmentActivity;
import java.util.concurrent.Executor;

public class BiometricHelper {

    private static BiometricHelper instance;
    private Context context;
    private BiometricPrompt biometricPrompt;

    public static BiometricHelper getInstance(Context ctx) {
        if (instance == null) {
            instance = new BiometricHelper(ctx);
        }
        return instance;
    }

    private BiometricHelper(Context ctx) {
        this.context = ctx;
    }

    /**
     * Check if biometric authentication is available
     */
    public boolean isBiometricAvailable() {
        BiometricManager biometricManager = BiometricManager.from(context);
        int canAuthenticate = biometricManager.canAuthenticate(
            BiometricManager.Authenticators.BIOMETRIC_STRONG
        );
        return canAuthenticate == BiometricManager.BIOMETRIC_SUCCESS;
    }

    /**
     * Authenticate user with biometrics
     * Calls native callback on success/failure
     */
    public void authenticate(final Activity activity) {
        if (!(activity instanceof FragmentActivity)) {
            nativeOnBiometricResult(false, "Activity is not FragmentActivity");
            return;
        }

        FragmentActivity fragmentActivity = (FragmentActivity) activity;
        Executor executor = ContextCompat.getMainExecutor(context);

        biometricPrompt = new BiometricPrompt(fragmentActivity, executor,
            new BiometricPrompt.AuthenticationCallback() {
                @Override
                public void onAuthenticationSucceeded(
                    BiometricPrompt.AuthenticationResult result) {
                    super.onAuthenticationSucceeded(result);
                    nativeOnBiometricResult(true, "Authentication successful");
                }

                @Override
                public void onAuthenticationFailed() {
                    super.onAuthenticationFailed();
                    nativeOnBiometricResult(false, "Authentication failed");
                }

                @Override
                public void onAuthenticationError(int errorCode, CharSequence errString) {
                    super.onAuthenticationError(errorCode, errString);
                    nativeOnBiometricResult(false, errString.toString());
                }
            }
        );

        BiometricPrompt.PromptInfo promptInfo = new BiometricPrompt.PromptInfo.Builder()
            .setTitle("Najika Digivice")
            .setSubtitle("Authenticate to access Najika")
            .setDescription("Use your fingerprint or face to unlock")
            .setNegativeButtonText("Cancel")
            .build();

        biometricPrompt.authenticate(promptInfo);
    }

    /**
     * Native callback (implemented in C++)
     */
    private native void nativeOnBiometricResult(boolean success, String message);
}
```

#### **3. BiometricAuth.h (UE5 C++):**

```cpp
// BiometricAuth.h

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "BiometricAuth.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnBiometricResult, bool, Success, const FString&, Message);

UCLASS(Blueprintable)
class NAJIKABIOMETRIC_API UBiometricAuth : public UObject
{
    GENERATED_BODY()

public:
    /**
     * Check if biometric authentication is available on this device
     */
    UFUNCTION(BlueprintCallable, Category = "Najika|Biometric")
    static bool IsBiometricAvailable();

    /**
     * Request biometric authentication
     * Fires OnBiometricResult when complete
     */
    UFUNCTION(BlueprintCallable, Category = "Najika|Biometric")
    void RequestBiometricAuth();

    /**
     * Event fired when biometric authentication completes
     */
    UPROPERTY(BlueprintAssignable, Category = "Najika|Biometric")
    FOnBiometricResult OnBiometricResult;

private:
    /**
     * JNI callback from Android
     */
    void OnBiometricResultNative(bool Success, FString Message);
};
```

#### **4. Usage in Blueprint:**

```
Event BeginPlay:
→ If Platform == Android:
   * Check UBiometricAuth::IsBiometricAvailable()
   * If available:
     - Show "Use Fingerprint?" dialog
     - If yes: RequestBiometricAuth()

OnBiometricResult(Success, Message):
→ If Success:
   * Unlock app
   * Load game
→ Else:
   * Show error message
   * Allow retry or PIN fallback
```

---

## 🔒 TODO 6.2: ENCRYPTED STORAGE

### **Android EncryptedSharedPreferences:**

#### **SecureStorage.java:**

```java
package com.najika.security;

import android.content.Context;
import android.content.SharedPreferences;
import androidx.security.crypto.EncryptedSharedPreferences;
import androidx.security.crypto.MasterKey;

public class SecureStorage {

    private SharedPreferences encryptedPrefs;
    private static SecureStorage instance;

    public static SecureStorage getInstance(Context context) {
        if (instance == null) {
            instance = new SecureStorage(context);
        }
        return instance;
    }

    private SecureStorage(Context context) {
        try {
            MasterKey masterKey = new MasterKey.Builder(context)
                .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
                .build();

            encryptedPrefs = EncryptedSharedPreferences.create(
                context,
                "najika_secure_prefs",
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            );
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void saveString(String key, String value) {
        encryptedPrefs.edit().putString(key, value).apply();
    }

    public String getString(String key, String defaultValue) {
        return encryptedPrefs.getString(key, defaultValue);
    }

    public void saveInt(String key, int value) {
        encryptedPrefs.edit().putInt(key, value).apply();
    }

    public int getInt(String key, int defaultValue) {
        return encryptedPrefs.getInt(key, defaultValue);
    }

    public void clear() {
        encryptedPrefs.edit().clear().apply();
    }
}
```

#### **What to encrypt:**

```
Sensitive Data:
✅ API Keys (if any)
✅ Authentication Tokens
✅ User Credentials (if stored)
✅ Save Game Data (optional, for protection)

Non-Sensitive (can be plain):
- UI Settings (volume, graphics)
- Last played timestamp
- Tutorial completion flags
```

---

## 🌐 TODO 6.3: NETWORK SECURITY

### **HTTPS Configuration:**

#### **1. Update DefaultEngine.ini:**

```ini
[/Script/Engine.NetworkSettings]
bUseHttps=True
n.AllowDownloads=True

[/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]
bAllowCleartextTraffic=False
```

#### **2. Network Security Config (Android):**

```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Production: Only HTTPS -->
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <!-- Development: Allow localhost -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">127.0.0.1</domain>
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
    </domain-config>

    <!-- Certificate Pinning (Optional but recommended) -->
    <domain-config>
        <domain includeSubdomains="true">api.najika.com</domain>
        <pin-set expiration="2026-01-01">
            <!-- Replace with your certificate SHA-256 -->
            <pin digest="SHA-256">YOUR_CERTIFICATE_PIN_HERE</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

#### **3. Add to AndroidManifest.xml:**

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ... >
```

---

## ⚡ TODO 6.4: PERFORMANCE OPTIMIZATION

### **1. LOD (Level of Detail):**

```
For all Static Meshes:

Location: Content/Environment/

LOD Settings:
- LOD 0 (High):   100% triangles, Distance 0-1000
- LOD 1 (Medium): 50% triangles, Distance 1000-2000
- LOD 2 (Low):    25% triangles, Distance 2000-3000
- LOD 3 (Lowest): 10% triangles, Distance 3000+

Auto-Generate LODs:
1. Select mesh in Content Browser
2. Right-click → LOD → Generate LODs
3. Settings:
   - LOD Group: SmallProp / LargeProp
   - Number of LODs: 3-4
   - Percent Triangles: 50%, 25%, 10%
   - Screen Size: Auto

For Najika Character:
- LOD 0: Full detail (always, camera focus)
- LOD 1: Simplified hair (if far away)
- LOD 2: Very simple (if in distance)
```

### **2. Texture Optimization:**

```
Texture Settings:

High Priority (Najika, UI):
- Compression: ASTC (Android)
- Max Size: 2048x2048
- Mip Maps: Yes
- Streaming: Enabled

Medium Priority (Environment):
- Compression: ASTC
- Max Size: 1024x1024
- Mip Maps: Yes
- Streaming: Enabled

Low Priority (Background):
- Compression: ASTC
- Max Size: 512x512
- Mip Maps: Yes
- Streaming: Enabled

Texture Streaming Pool:
Project Settings → Rendering → Textures:
- Pool Size: 1000 MB (Xiaomi 11T Pro has 8GB RAM)
- Enable Streaming: Yes
```

### **3. Lighting Optimization:**

```
Static Lights:
- Bake lightmaps for static geometry
- Lightmap Resolution: 64-256 (based on object size)

Dynamic Lights:
- Limit to 3-4 per scene
- Use Lumen Mobile (efficient)
- Avoid overlapping light areas

Shadows:
- Static Shadows: Baked
- Dynamic Shadows: Only for character + important objects
- Shadow Distance: 2000 units
- Cascaded Shadow Maps: 3 cascades
```

### **4. Culling:**

```
Frustum Culling: (Automatic, enabled by default)

Occlusion Culling:
→ Place "PrecomputedVisibilityVolume" in level
→ Build → Build Lighting
→ Generates occlusion data

Distance Culling:
Per mesh:
- Cull Distance: Based on importance
- Character: Never cull
- Buildings: 3000
- Small props: 1500
- Grass/Details: 500

Tick Optimization:
→ Disable tick for objects not in view
→ Reduce tick rate for distant objects
```

---

## 🔋 TODO 6.5: BATTERY OPTIMIZATION

### **Adaptive Performance:**

#### **1. Enable in Project Settings:**

```
Project Settings → Plugins → Android:
✅ Enable Adaptive Performance
✅ Enable Thermal API
```

#### **2. Adaptive Quality System:**

```
Blueprint: BP_AdaptiveQuality

Variables:
- CurrentQuality (Int): 0-3 (Low, Med, High, Epic)
- ThermalState (Enum): None, Light, Moderate, Severe, Critical
- BatteryLevel (Float): 0-100

Event Tick (Every 5 seconds):
→ Get ThermalState from Android API
→ Get BatteryLevel from Battery API
→ Adjust quality:

If ThermalState >= Moderate OR BatteryLevel < 20:
   → Reduce quality by 1 level
   → Lower frame rate to 30
   → Reduce shadow quality
   → Disable particles

Else If ThermalState == Light AND BatteryLevel > 50:
   → Increase quality by 1 level (max 3)
   → Restore to 60 FPS
   → Enable full shadows

Apply Quality:
→ Execute console commands:
   * sg.ViewDistanceQuality {quality}
   * sg.ShadowQuality {quality}
   * sg.EffectsQuality {quality}
   * r.SetRes {resolution}
   * t.MaxFPS {fps}
```

### **Idle Optimization:**

```
Blueprint: BP_IdleOptimization

Event: OnPlayerIdle (No input for 30 seconds)
→ Reduce frame rate to 30 FPS
→ Stop animations (far objects)
→ Reduce particle spawn rates
→ Lower audio update rate

Event: OnPlayerActive (Input detected)
→ Restore frame rate to 60 FPS
→ Resume all systems
```

---

## 💾 TODO 6.6: MEMORY MANAGEMENT

### **Asset Streaming:**

```
Level Streaming:
- Split world into sublevels
- Load/Unload based on player position

Example:
L_MainWorld_Persistent (Always loaded)
├── Sky, Lighting, Game Mode
└── Streaming Levels:
    - L_Forest (Load Distance: 500)
    - L_Village (Load Distance: 500)
    - L_SchwarzenMuehle (Load Distance: 300)
    - L_River (Load Distance: 500)

Blueprint: BP_LevelStreamingManager
→ Track player position
→ Stream in levels when near
→ Stream out when far
```

### **Object Pooling:**

```
For frequently spawned objects:
- Particles
- Projectiles
- Damage numbers
- UI notifications

Example: Particle Pool
Blueprint: BP_ParticlePool

Variables:
- Pool (Array of Particle Components)
- PoolSize: 20

Function GetParticle:
→ Find inactive particle in pool
→ If found: Activate & return
→ Else: Create new (if pool not full)

Function ReturnParticle:
→ Deactivate particle
→ Reset to default state
→ Keep in pool for reuse
```

### **Garbage Collection:**

```
Blueprint: BP_MemoryManager

Event Tick (Every 60 seconds):
→ Execute console command:
   gc.CollectGarbageEveryFrame 0
   obj gc

→ Force garbage collection
→ Log memory usage:
   stat memory
```

---

## 🛡️ TODO 6.7: ALCATRAZ INTEGRATION

### **Security Best Practices (from NAJIKA_SECURITY_RESEARCH_2025.md):**

#### **Die 8 Gebote:**

```
1. Zero-Trust Architecture:
   ✅ Only connect to 127.0.0.1:8000 (localhost)
   ✅ No external connections without VPN
   ✅ Verify all network traffic

2. Owner-Token Authentication:
   ✅ Generate unique token on first run
   ✅ Store in encrypted storage
   ✅ Include in all API requests

3. VPN Check:
   ✅ Check VPN status before connecting
   ✅ Warn user if VPN disconnected
   ✅ Optional: Block operations if no VPN

4. Privacy-First:
   ✅ No telemetry without consent
   ✅ No analytics
   ✅ All data stays local

5. Offline-Capable:
   ✅ App works without internet
   ✅ Backend runs locally
   ✅ No cloud dependencies

6. NSFW Local Only:
   ✅ Private mode (Kätzchen) stays on device
   ✅ Never sync to cloud
   ✅ Encrypted storage

7. Encrypted Everything:
   ✅ Save files encrypted
   ✅ Secure storage for credentials
   ✅ No plain-text secrets

8. Auditable:
   ✅ Log all security events
   ✅ Track access attempts
   ✅ Transparent behavior
```

#### **Implementation:**

```
Blueprint: BP_SecurityManager

Function CheckSecurity:
→ VerifyVPNStatus()
→ VerifyBackendConnection()
→ CheckEncryptionStatus()
→ ValidateOwnerToken()
→ Return SecurityReport

Function ShowSecurityWarning(Issue):
→ Create WBP_SecurityWarning
→ Show issue + recommendations
→ Option to continue or fix
```

---

## 📊 SUCCESS CRITERIA

**Phase 6 ist komplett wenn:**

```
✅ Biometric Authentication funktioniert (Android)
   - Fingerprint/Face unlock
   - Fallback to PIN

✅ Encrypted Storage funktioniert
   - Sensitive data encrypted
   - Keys stored in Keystore

✅ Network Security funktioniert
   - HTTPS enforced (production)
   - Localhost allowed (development)
   - Certificate pinning (optional)

✅ Performance optimiert
   - 60 FPS stable (on Snapdragon 888)
   - LOD working
   - Culling working
   - Memory < 2GB

✅ Battery optimiert
   - Adaptive performance working
   - 4+ hours battery life
   - Thermal throttling handled

✅ Memory Management funktioniert
   - No memory leaks
   - Asset streaming working
   - GC working

✅ Security Best Practices implementiert
   - All 8 Gebote followed
   - Security checks in place
   - Audit logging
```

---

## 🎉 PHASE 6 COMPLETE!

**Nächster Schritt:** Phase 7 - Packaging & Deployment

**Geschätzte Dauer Phase 6:** 1 Woche

---

**Model 1 - Digivice APK Development**
**Phase:** 6/9 - Security & Optimization
**Status:** Ready to Execute
