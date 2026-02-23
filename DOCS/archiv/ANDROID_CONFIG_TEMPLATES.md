# ANDROID CONFIGURATION TEMPLATES
**Model 1 - Digivice APK**
**Created:** 2025-11-11

---

## 📱 ANDROID CONFIG FILES ÜBERSICHT

Diese Datei enthält alle Android-spezifischen Konfigurationsdateien die du für das Najika Digivice APK brauchst!

**Files enthalten:**
```
✅ AndroidManifest.xml (Permissions, Activities)
✅ build.gradle (Build configuration)
✅ proguard-rules.pro (Code obfuscation)
✅ strings.xml (String resources)
✅ network_security_config.xml (Network rules)
✅ DefaultEngine.ini (UE5 Android settings)
```

---

## 📄 FILE 1: AndroidManifest.xml

**Location in UE5:** `Build/Android/AndroidManifest.xml`
**Purpose:** Android app configuration, permissions, activities

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.najika.digivice"
    android:versionCode="1"
    android:versionName="1.0.0"
    android:installLocation="auto">

    <!-- Target Android 10 (API 29) minimum, Android 14 (API 34) target -->
    <uses-sdk
        android:minSdkVersion="29"
        android:targetSdkVersion="34" />

    <!-- PERMISSIONS -->

    <!-- Essential Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.VIBRATE" />

    <!-- Microphone for Voice Calls -->
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />

    <!-- Storage for Save Files -->
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="28" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32" />

    <!-- Biometric Authentication -->
    <uses-permission android:name="android.permission.USE_BIOMETRIC" />
    <uses-permission android:name="android.permission.USE_FINGERPRINT" />

    <!-- Optional: Camera for Scanner feature (Phase 8) -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />

    <!-- Optional: Notifications -->
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <!-- Feature declarations -->
    <uses-feature android:glEsVersion="0x00030001" android:required="true" />
    <uses-feature android:name="android.hardware.touchscreen" android:required="true" />
    <uses-feature android:name="android.hardware.microphone" android:required="false" />

    <!-- Application Configuration -->
    <application
        android:name="com.epicgames.unreal.GameApplication"
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:theme="@style/NajikaTheme"
        android:hardwareAccelerated="true"
        android:allowBackup="true"
        android:requestLegacyExternalStorage="true"
        android:usesCleartextTraffic="true"
        android:networkSecurityConfig="@xml/network_security_config"
        android:supportsRtl="true">

        <!-- Main Game Activity -->
        <activity
            android:name="com.epicgames.unreal.GameActivity"
            android:label="@string/app_name"
            android:theme="@style/NajikaTheme"
            android:launchMode="singleTask"
            android:screenOrientation="sensorLandscape"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|screenLayout|uiMode"
            android:exported="true">

            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>

            <!-- Deep linking (optional) -->
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="najika" android:host="digivice" />
            </intent-filter>
        </activity>

        <!-- Splash Screen Activity -->
        <activity
            android:name="com.epicgames.unreal.SplashActivity"
            android:label="@string/app_name"
            android:theme="@style/NajikaSplashTheme"
            android:launchMode="singleTask"
            android:screenOrientation="sensorLandscape"
            android:configChanges="orientation|keyboardHidden|keyboard">
        </activity>

        <!-- Services -->
        <!-- Background service for auto-save -->
        <service
            android:name=".NajikaBackgroundService"
            android:enabled="true"
            android:exported="false" />

    </application>

</manifest>
```

---

## 📄 FILE 2: build.gradle

**Location in UE5:** `Build/Android/gradle/app/build.gradle`
**Purpose:** Android build configuration

```gradle
apply plugin: 'com.android.application'

android {
    compileSdkVersion 34
    buildToolsVersion '34.0.0'

    defaultConfig {
        applicationId "com.najika.digivice"
        minSdkVersion 29
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"

        // Multilib support (ARM64 only)
        ndk {
            abiFilters 'arm64-v8a'
        }

        // Enable ProGuard (optional)
        minifyEnabled false
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }

    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'

            // Signing config
            signingConfig signingConfigs.release
        }

        debug {
            applicationIdSuffix ".debug"
            debuggable true
            jniDebuggable true
        }
    }

    signingConfigs {
        release {
            storeFile file("../najika-release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD") ?: "your_keystore_password"
            keyAlias "najika"
            keyPassword System.getenv("KEY_PASSWORD") ?: "your_key_password"
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    packagingOptions {
        exclude 'META-INF/DEPENDENCIES'
        exclude 'META-INF/LICENSE'
        exclude 'META-INF/LICENSE.txt'
        exclude 'META-INF/NOTICE'
        exclude 'META-INF/NOTICE.txt'
    }

    // Disable automatic BuildConfig generation
    buildFeatures {
        buildConfig false
    }
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])

    // AndroidX libraries
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'

    // Google Play Services (optional, for achievements later)
    // implementation 'com.google.android.gms:play-services-games:23.1.0'

    // Biometric Authentication
    implementation 'androidx.biometric:biometric:1.1.0'

    // Security Crypto for encrypted storage
    implementation 'androidx.security:security-crypto:1.1.0-alpha06'

    // Material Design
    implementation 'com.google.android.material:material:1.11.0'
}
```

---

## 📄 FILE 3: proguard-rules.pro

**Location:** `Build/Android/gradle/app/proguard-rules.pro`
**Purpose:** Code obfuscation rules (security!)

```proguard
# Najika Digivice ProGuard Rules

# Keep Unreal Engine classes
-keep class com.epicgames.unreal.** { *; }
-dontwarn com.epicgames.unreal.**

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep enums
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Keep Parcelables
-keep class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator *;
}

# Keep Serializables
-keepnames class * implements java.io.Serializable
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    !static !transient <fields>;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

# Keep AndroidX classes
-keep class androidx.** { *; }
-dontwarn androidx.**

# Keep Google Play Services (if used)
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.android.gms.**

# Keep biometric classes
-keep class androidx.biometric.** { *; }

# Security Crypto
-keep class androidx.security.crypto.** { *; }

# Remove logging in release (security!)
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# Optimize
-optimizationpasses 5
-dontusemixedcaseclassnames
-dontskipnonpubliclibraryclasses
-dontpreverify
-verbose

# Keep custom classes (add yours here!)
-keep class com.najika.digivice.** { *; }
```

---

## 📄 FILE 4: strings.xml

**Location:** `Build/Android/gradle/app/src/main/res/values/strings.xml`
**Purpose:** String resources (translations!)

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- App Name -->
    <string name="app_name">Najika Digivice</string>

    <!-- Permissions -->
    <string name="permission_microphone_title">Microphone Permission</string>
    <string name="permission_microphone_message">Najika needs microphone access for voice calls. Allow?</string>
    <string name="permission_camera_title">Camera Permission</string>
    <string name="permission_camera_message">Najika needs camera access for the scanner feature. Allow?</string>
    <string name="permission_storage_title">Storage Permission</string>
    <string name="permission_storage_message">Najika needs storage access to save your progress. Allow?</string>
    <string name="permission_biometric_title">Biometric Authentication</string>
    <string name="permission_biometric_message">Use your fingerprint to unlock Najika Digivice securely.</string>

    <!-- Buttons -->
    <string name="button_allow">Allow</string>
    <string name="button_deny">Deny</string>
    <string name="button_ok">OK</string>
    <string name="button_cancel">Cancel</string>
    <string name="button_retry">Retry</string>

    <!-- Notifications -->
    <string name="notification_channel_name">Najika Notifications</string>
    <string name="notification_channel_description">Notifications from Najika</string>
    <string name="notification_najika_hungry">Najika is hungry! 🍖</string>
    <string name="notification_najika_tired">Najika is tired! 😴</string>
    <string name="notification_najika_sad">Najika is sad! 😢</string>
    <string name="notification_najika_misses_you">Najika misses you! Come back soon! 💜</string>

    <!-- Errors -->
    <string name="error_network">Network error. Please check your connection.</string>
    <string name="error_server">Server error. Please try again later.</string>
    <string name="error_unknown">An unknown error occurred.</string>
    <string name="error_microphone">Cannot access microphone.</string>
    <string name="error_camera">Cannot access camera.</string>
    <string name="error_storage">Cannot access storage.</string>
    <string name="error_biometric_not_available">Biometric authentication not available on this device.</string>
    <string name="error_biometric_no_hardware">No biometric hardware detected.</string>
    <string name="error_biometric_not_enrolled">No biometric credentials enrolled. Please set up fingerprint in device settings.</string>

    <!-- Dialogs -->
    <string name="dialog_exit_title">Exit Najika Digivice?</string>
    <string name="dialog_exit_message">Are you sure you want to exit? Don\'t leave Najika alone! 🥺</string>
    <string name="dialog_update_title">Update Available</string>
    <string name="dialog_update_message">A new version of Najika Digivice is available! Update now?</string>

    <!-- Loading -->
    <string name="loading">Loading...</string>
    <string name="loading_najika">Loading Najika...</string>
    <string name="loading_world">Loading World...</string>

    <!-- Gameplay -->
    <string name="hunger">Hunger</string>
    <string name="energy">Energy</string>
    <string name="happiness">Happiness</string>
    <string name="hygiene">Hygiene</string>
    <string name="level">Level</string>

    <!-- Actions -->
    <string name="action_feed">Feed</string>
    <string name="action_drink">Drink</string>
    <string name="action_wash">Wash</string>
    <string name="action_sleep">Sleep</string>
    <string name="action_train">Train</string>
    <string name="action_praise">Praise</string>
    <string name="action_scold">Scold</string>

    <!-- About -->
    <string name="about_version">Version %1$s</string>
    <string name="about_developer">Developed with 💜 by Najika Team</string>
</resources>
```

**Optional: Create `strings.xml` for German (values-de):**

```xml
<!-- values-de/strings.xml -->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Najika Digivice</string>
    <string name="permission_microphone_title">Mikrofon-Berechtigung</string>
    <string name="permission_microphone_message">Najika braucht Mikrofon-Zugriff für Sprachanrufe. Erlauben?</string>
    <string name="error_network">Netzwerkfehler. Bitte überprüfe deine Verbindung.</string>
    <!-- ... mehr Übersetzungen ... -->
</resources>
```

---

## 📄 FILE 5: network_security_config.xml

**Location:** `Build/Android/gradle/app/src/main/res/xml/network_security_config.xml`
**Purpose:** Network security rules (allow localhost!)

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Allow cleartext (HTTP) traffic to localhost for development -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">127.0.0.1</domain>
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain> <!-- Android emulator host -->
    </domain-config>

    <!-- Production: Use HTTPS for all external connections -->
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <!-- Allow HTTP for specific development server (optional) -->
    <!-- Uncomment if you want to allow your dev server IP -->
    <!--
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">192.168.1.100</domain>
    </domain-config>
    -->

    <!-- Pin certificates for production server (optional, advanced!) -->
    <!--
    <domain-config>
        <domain includeSubdomains="true">api.najika.com</domain>
        <pin-set>
            <pin digest="SHA-256">YOUR_CERTIFICATE_SHA256_HASH</pin>
        </pin-set>
    </domain-config>
    -->
</network-security-config>
```

**WICHTIG:** Für Production-Release:
- Ändere `cleartextTrafficPermitted="false"` im base-config
- Nutze HTTPS für alle API calls!
- Entferne localhost aus domain-config

---

## 📄 FILE 6: DefaultEngine.ini (UE5 Android Settings)

**Location in UE5:** `Config/DefaultEngine.ini`
**Purpose:** Unreal Engine Android configuration

```ini
[/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]

; Basic Settings
PackageName=com.najika.digivice
StoreVersion=1
StoreVersionOffsetArm64=0
ApplicationDisplayName=Najika Digivice
VersionDisplayName=1.0.0

; SDK Versions
MinSDKVersion=29
TargetSDKVersion=34

; Architecture (ARM64 only for modern devices)
bBuildForArm64=True
bBuildForX8664=False

; Orientation
Orientation=SensorLandscape
bAllowLandscapeLeftAndRight=True

; Graphics
bSupportsVulkan=True
bBuildForES31=True
bSupportsOpenGLES3=True

; Permissions
bEnableMicrophonePermissionByDefault=True
bPackageDataInsideApk=True

; Performance
bEnableGrayscaleAlpha=False
bSupportAdrenoTextureFormats=True
bSupportsASTCTextureFormats=True
bMultiTargetFormat_ETC2=True
bMultiTargetFormat_DXT=False
bMultiTargetFormat_ASTC=True

; Memory
MaxShaderSize=2048
TargetMemoryForTextureStreaming=512

; Packaging
bAllowLargeOBBFiles=True
bPackageForOculusMobile=False

; Install Location
InstallLocation=Auto

; Splash Screen
bShowLaunchImage=True

; Biometric
bEnableFingerprint=True

; Optional: Google Play Services (if using achievements later)
bEnableGooglePlaySupport=False
GamesAppID=

; Optional: Firebase
bEnableFirebase=False

; Audio
bDisableAudioMixer=False
bUseAndroidAudioCallbacks=True
```

---

## 📄 FILE 7: colors.xml (Material Theme)

**Location:** `Build/Android/gradle/app/src/main/res/values/colors.xml`
**Purpose:** Color definitions for Android UI

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Najika Brand Colors -->
    <color name="najika_purple">#9966FF</color>
    <color name="najika_pink">#FF66CC</color>
    <color name="najika_blue">#6699FF</color>

    <!-- Material Design Colors -->
    <color name="colorPrimary">#9966FF</color>
    <color name="colorPrimaryDark">#7744DD</color>
    <color name="colorAccent">#FF66CC</color>

    <!-- Status Bar -->
    <color name="statusBarColor">#7744DD</color>

    <!-- Background -->
    <color name="backgroundColor">#FFFFFF</color>
    <color name="backgroundDark">#121212</color>

    <!-- Text -->
    <color name="textPrimary">#000000</color>
    <color name="textSecondary">#757575</color>
    <color name="textWhite">#FFFFFF</color>

    <!-- UI Elements -->
    <color name="buttonBackground">#9966FF</color>
    <color name="buttonText">#FFFFFF</color>
    <color name="errorRed">#FF0000</color>
    <color name="successGreen">#00FF00</color>
    <color name="warningYellow">#FFAA00</color>
</resources>
```

---

## 📄 FILE 8: styles.xml (Theme Definition)

**Location:** `Build/Android/gradle/app/src/main/res/values/styles.xml`
**Purpose:** Android app theme

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Najika Main Theme -->
    <style name="NajikaTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <!-- Primary Colors -->
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>

        <!-- Status Bar -->
        <item name="android:statusBarColor">@color/statusBarColor</item>

        <!-- Navigation Bar -->
        <item name="android:navigationBarColor">@color/colorPrimaryDark</item>

        <!-- Window Background -->
        <item name="android:windowBackground">@color/backgroundColor</item>

        <!-- Fullscreen -->
        <item name="android:windowFullscreen">true</item>
        <item name="android:windowContentOverlay">@null</item>

        <!-- Keep screen on during gameplay -->
        <item name="android:keepScreenOn">true</item>
    </style>

    <!-- Splash Screen Theme -->
    <style name="NajikaSplashTheme" parent="NajikaTheme">
        <item name="android:windowBackground">@drawable/splash_screen</item>
        <item name="android:windowNoTitle">true</item>
        <item name="android:windowFullscreen">true</item>
    </style>
</resources>
```

---

## 🎨 SPLASH SCREEN IMAGE

**Location:** `Build/Android/gradle/app/src/main/res/drawable/splash_screen.xml`
**Purpose:** Splash screen background

```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android"
    android:opacity="opaque">

    <!-- Background Color -->
    <item android:drawable="@color/najika_purple" />

    <!-- Logo (center) -->
    <item>
        <bitmap
            android:gravity="center"
            android:src="@mipmap/splash_logo" />
    </item>

</layer-list>
```

**Note:** Du musst `splash_logo.png` erstellen und in `res/mipmap-xxxhdpi/` platzieren!

---

## 📊 CONFIG FILES SUMMARY

```
✅ AndroidManifest.xml       → Permissions, Activities
✅ build.gradle              → Build configuration
✅ proguard-rules.pro        → Code obfuscation
✅ strings.xml               → String resources (DE/EN)
✅ network_security_config   → Network rules
✅ DefaultEngine.ini         → UE5 Android settings
✅ colors.xml                → Color definitions
✅ styles.xml                → App theme
✅ splash_screen.xml         → Splash screen

OPTIONAL:
- firebase.json (if using Firebase)
- google-services.json (if using Google Play Services)
```

---

## 🔧 USAGE INSTRUCTIONS

### **Step 1: Copy Templates**

```bash
# Im UE5 Projekt:
cd C:\NajikaDigivice_UE5

# Erstelle Ordner
mkdir -p Build\Android\gradle\app\src\main\res\values
mkdir -p Build\Android\gradle\app\src\main\res\values-de
mkdir -p Build\Android\gradle\app\src\main\res\xml

# Kopiere Templates aus dieser Datei in die entsprechenden Ordner
```

### **Step 2: Edit Project Settings in UE5**

```
1. Edit → Project Settings → Android
2. Folge PHASE_7 Guide für vollständige Konfiguration
3. Import diese Config-Files
4. Build APK
```

### **Step 3: Test**

```
1. Build APK
2. Install on device: adb install NajikaDigivice.apk
3. Test all permissions
4. Test biometric auth
5. Test network connectivity
```

---

## 🎉 ANDROID CONFIGS COMPLETE!

Alle Android-Konfigurationsdateien sind jetzt vorbereitet!

**Next:** Erstelle Material Templates & Animation Blueprints!

---

**Model 1 - Digivice APK Development**
**Status:** Android Configs Ready ✅
**Files:** 8 Config Templates Created

**READY FOR ANDROID DEPLOYMENT! 📱🚀**
