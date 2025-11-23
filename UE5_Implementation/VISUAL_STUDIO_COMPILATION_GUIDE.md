# Visual Studio Compilation Guide - Najika UE5 Project

**Version:** 1.0
**Last Updated:** 2025-01-13
**Target:** Unreal Engine 5.3+ with C++ Plugins
**IDE:** Visual Studio 2022 (recommended) or Visual Studio 2019

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Visual Studio Installation](#visual-studio-installation)
3. [Project Setup](#project-setup)
4. [Build Configurations](#build-configurations)
5. [Compilation Steps](#compilation-steps)
6. [Hot Reload](#hot-reload)
7. [Debugging](#debugging)
8. [Common Errors & Solutions](#common-errors--solutions)
9. [Performance Optimization](#performance-optimization)
10. [Advanced Topics](#advanced-topics)

---

## Prerequisites

### Required Software

| Software | Version | Download Link |
|----------|---------|---------------|
| **Unreal Engine** | 5.3 or higher | Epic Games Launcher |
| **Visual Studio** | 2022 (preferred) or 2019 | https://visualstudio.microsoft.com/ |
| **.NET Framework** | 4.6.2 or higher | Included with VS |
| **Windows SDK** | 10.0.18362.0 or higher | Included with VS |

### Visual Studio Workloads Required

During Visual Studio installation, ensure these workloads are selected:

- ✅ **Game development with C++**
  - Includes Unreal Engine installer
  - C++ profiling tools
  - Windows 10/11 SDK

- ✅ **Desktop development with C++**
  - MSVC v143 compiler (VS 2022) or v142 (VS 2019)
  - C++ ATL for latest build tools
  - C++ MFC for latest build tools

### Individual Components (Optional but Recommended)

In the Visual Studio Installer, go to **Individual Components** and select:

- ✅ C++ AddressSanitizer
- ✅ C++ profiling tools
- ✅ IntelliCode
- ✅ Live Share

### System Requirements

- **OS:** Windows 10 (64-bit) version 1909 or higher
- **CPU:** Quad-core Intel or AMD, 2.5 GHz or faster
- **RAM:** 16 GB minimum, 32 GB recommended
- **Disk Space:** 50 GB free (for engine, project, and intermediate files)
- **GPU:** DirectX 11/12 compatible graphics card

---

## Visual Studio Installation

### Step 1: Download Visual Studio

1. Go to https://visualstudio.microsoft.com/downloads/
2. Download **Visual Studio 2022 Community** (free for individual developers)
3. Run the installer

### Step 2: Select Workloads

In the Visual Studio Installer:

1. Check **Game development with C++**
2. Check **Desktop development with C++**
3. On the right panel (Installation details), ensure these are selected:
   - MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)
   - Windows 10/11 SDK (latest version)
   - C++ profiling tools
   - C++ ATL for latest build tools
   - Unreal Engine installer

### Step 3: Install

Click **Install** and wait for completion (may take 30-60 minutes depending on connection).

### Step 4: Verify Installation

After installation:

1. Launch Visual Studio 2022
2. Go to **Help > About Microsoft Visual Studio**
3. Verify version is **17.0 or higher**
4. Close Visual Studio

---

## Project Setup

### Step 1: Copy Plugin Files

Use the PowerShell script to copy plugin files to your UE5 project:

```powershell
.\COPY_TO_UE5_PROJECT.ps1 -ProjectPath "C:\Users\YourName\Documents\Unreal Projects\NajikaDigivice"
```

This will:
- Copy NajikaBackendClient plugin
- Copy NajikaVoiceSystem plugin
- Copy all documentation
- Create backup of existing files

### Step 2: Generate Visual Studio Project Files

**Method 1: Right-Click (Recommended)**

1. Navigate to your UE5 project folder
2. Find the `.uproject` file (e.g., `NajikaDigivice.uproject`)
3. Right-click on it
4. Select **Generate Visual Studio project files**
5. Wait for the process to complete (15-30 seconds)

**Method 2: Manual (If Right-Click Doesn't Work)**

1. Open Command Prompt as Administrator
2. Navigate to your UE5 installation:
   ```batch
   cd "C:\Program Files\Epic Games\UE_5.3\Engine\Binaries\DotNET"
   ```
3. Run UnrealBuildTool:
   ```batch
   UnrealBuildTool.exe -projectfiles -project="C:\Path\To\Your\NajikaDigivice.uproject" -game -rocket -progress
   ```

### Step 3: Open Solution in Visual Studio

1. After generation completes, you'll see a new `.sln` file in your project folder
2. Double-click `NajikaDigivice.sln` to open in Visual Studio
3. Visual Studio will load the solution (may take 1-2 minutes)

### Step 4: Solution Explorer Overview

In Visual Studio, you should see:

```
Solution 'NajikaDigivice' (2 projects)
├── Engine
│   └── UE5 (thousands of files - don't modify)
├── Games
│   └── NajikaDigivice
│       ├── Source
│       │   └── NajikaDigivice
│       │       ├── NajikaDigivice.Build.cs
│       │       └── ... (game C++ files)
│       ├── Plugins
│       │   ├── NajikaBackendClient
│       │   │   ├── Source
│       │   │   │   ├── NajikaBackendClient.Build.cs
│       │   │   │   ├── Public
│       │   │   │   │   ├── NajikaBackendClient.h
│       │   │   │   │   ├── NajikaHttpClient.h
│       │   │   │   │   └── ... (8 header files)
│       │   │   │   └── Private
│       │   │   │       ├── NajikaHttpClient.cpp
│       │   │   │       └── ... (8 cpp files)
│       │   └── NajikaVoiceSystem
│       │       ├── Source
│       │       │   ├── NajikaVoiceSystem.Build.cs
│       │       │   ├── Public
│       │       │   │   └── ... (10 header files)
│       │       │   └── Private
│       │       │       └── ... (10 cpp files)
```

---

## Build Configurations

### Available Configurations

Visual Studio toolbar (top) shows two dropdowns:

1. **Configuration** (left dropdown)
2. **Platform** (right dropdown)

### Configuration Types

| Configuration | Purpose | Optimization | Debug Symbols | Use Case |
|--------------|---------|--------------|---------------|----------|
| **DebugGame** | Development | Minimal | Full | Active development, debugging |
| **DebugGame Editor** | Editor development | Minimal | Full | Default for UE5 Editor testing |
| **Development** | Testing | Medium | Partial | Performance testing |
| **Development Editor** | Editor testing | Medium | Partial | Editor with better performance |
| **Shipping** | Final build | Maximum | None | Production APK/release |

### Platform Types

| Platform | Target | Use Case |
|----------|--------|----------|
| **Win64** | Windows 64-bit | Development machine |
| **Android** | Android ARM64 | Mobile device (Xiaomi 11T Pro) |
| **Android_ASTC** | Android with ASTC textures | High-quality mobile textures |

### Recommended Configuration

For daily development:
- **Configuration:** `DebugGame Editor`
- **Platform:** `Win64`

This allows:
- Fast iteration with Hot Reload
- Full debugging capabilities
- Running within UE5 Editor

---

## Compilation Steps

### First-Time Full Build

**IMPORTANT:** The first build will take 30-60 minutes. Subsequent builds are much faster (1-5 minutes).

#### Step 1: Set Configuration

1. In Visual Studio toolbar, select:
   - **Configuration:** `DebugGame Editor`
   - **Platform:** `Win64`

#### Step 2: Build Solution

**Option A: Menu Bar**
1. Go to **Build > Build Solution** (or press `Ctrl+Shift+B`)

**Option B: Solution Explorer**
1. Right-click on `NajikaDigivice` project (NOT the solution)
2. Select **Build**

#### Step 3: Monitor Output

Watch the **Output** window (bottom panel):
- **View > Output** if not visible
- You'll see compilation progress:
  ```
  1>------ Build started: Project: UE5, Configuration: DebugGame_Editor x64 ------
  1>Building NajikaBackendClient...
  1>  NajikaHttpClient.cpp
  1>  NajikaWebSocketClient.cpp
  1>  ... (compiling files)
  1>  Creating library...
  1>Build succeeded.
  ```

#### Step 4: Verify Success

After build completes, check **Output** window for:
```
========== Build: 1 succeeded, 0 failed, 0 up-to-date, 0 skipped ==========
```

**Success Indicators:**
- ✅ Green checkmark in status bar
- ✅ "Build succeeded" message
- ✅ No red error messages in Error List

**Build Time Expectations:**
- **First build:** 30-60 minutes (compiles entire engine + project)
- **Incremental builds:** 1-5 minutes (only changed files)
- **Hot reload:** 10-30 seconds (minimal recompilation)

### Incremental Builds

After the first build, subsequent builds are much faster because only changed files are recompiled.

**When to rebuild:**
- You modified C++ code
- You added new classes
- You changed plugin code
- You modified `.Build.cs` files

**Incremental Build Steps:**
1. Make code changes
2. Save files (`Ctrl+S`)
3. Press `Ctrl+Shift+B` to build
4. Wait for compilation (usually 1-3 minutes)
5. Launch/restart UE5 Editor

### Building Specific Plugins

To build only a specific plugin (faster):

1. In **Solution Explorer**, expand:
   - `Games > NajikaDigivice > Plugins > NajikaBackendClient`
2. Right-click on the plugin project
3. Select **Build**

This only recompiles the selected plugin.

---

## Hot Reload

**Hot Reload** allows you to recompile C++ code while the UE5 Editor is running, without restarting.

### Using Hot Reload

#### Method 1: From UE5 Editor (Recommended)

1. Keep UE5 Editor open
2. Switch to Visual Studio
3. Make code changes in C++ files
4. Save files (`Ctrl+S`)
5. Press **Ctrl+Alt+F11** (or click **Compile** button in UE5 Editor toolbar)
6. Wait for compilation (10-30 seconds)
7. UE5 Editor automatically reloads the module

#### Method 2: From Visual Studio

1. Keep UE5 Editor open
2. In Visual Studio, make code changes
3. Press `Ctrl+Shift+B` to build
4. Switch back to UE5 Editor
5. Click the **Compile** button (circular arrows icon) in the toolbar

### Hot Reload Limitations

**Hot Reload CANNOT handle:**
- ❌ Adding new UCLASS/USTRUCT/UENUM
- ❌ Changing class inheritance
- ❌ Adding new UPROPERTY to Blueprint-exposed classes
- ❌ Changing function signatures of UFUNCTION
- ❌ Modifying .Build.cs files

**For these changes, you MUST:**
1. Close UE5 Editor
2. Build in Visual Studio
3. Reopen UE5 Editor

**Hot Reload CAN handle:**
- ✅ Changing function implementations
- ✅ Adding new non-Blueprint functions
- ✅ Modifying logic in existing functions
- ✅ Changing variable values
- ✅ Adding new private members

### Hot Reload Best Practices

1. **Save often:** Press `Ctrl+S` before compiling
2. **Close Blueprints:** Close Blueprint editors that use the modified C++ class
3. **Watch Output:** Check **Output Log** in UE5 for compilation messages
4. **Restart if needed:** If Hot Reload fails, restart UE5 Editor

---

## Debugging

### Setting Up Debugging

#### Step 1: Set Startup Project

1. In **Solution Explorer**, right-click on `NajikaDigivice` (under Games)
2. Select **Set as Startup Project**
3. The project name will appear bold

#### Step 2: Set Breakpoints

1. Open a C++ file (e.g., `NajikaHttpClient.cpp`)
2. Click in the left margin (gray area) next to a line of code
3. A red circle appears = breakpoint set

Example:
```cpp
void UNajikaHttpClient::SendRequest(const FString& Endpoint, const FString& JsonData)
{
    // Set breakpoint here ← Click in left margin
    FString URL = BaseURL + Endpoint;

    // Or here
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
}
```

#### Step 3: Start Debugging

**Option A: Launch UE5 Editor with Debugger**

1. Press `F5` (or click **Debug > Start Debugging**)
2. UE5 Editor launches (may take 1-2 minutes)
3. Editor runs with debugger attached
4. Breakpoints will trigger when code executes

**Option B: Attach to Running Editor**

1. Launch UE5 Editor normally (from Epic Games Launcher)
2. In Visual Studio, go to **Debug > Attach to Process** (`Ctrl+Alt+P`)
3. Find `UnrealEditor.exe` in the process list
4. Click **Attach**
5. Debugger is now attached

#### Step 4: Trigger Breakpoint

1. In UE5 Editor, perform action that calls your C++ code
   - Example: Press Play to call BeginPlay()
   - Example: Click a button that calls your UFUNCTION
2. When code hits breakpoint, UE5 Editor freezes
3. Visual Studio comes to foreground
4. Yellow arrow shows current execution line

#### Step 5: Debug Controls

| Key | Action | Description |
|-----|--------|-------------|
| `F5` | Continue | Resume execution until next breakpoint |
| `F10` | Step Over | Execute current line, don't enter functions |
| `F11` | Step Into | Enter function calls |
| `Shift+F11` | Step Out | Exit current function |
| `Shift+F5` | Stop Debugging | Detach debugger |

#### Step 6: Inspect Variables

While paused at breakpoint:

1. **Locals Window** (`Debug > Windows > Locals`):
   - Shows all local variables in current scope
   - Expand objects to see members

2. **Autos Window** (`Debug > Windows > Autos`):
   - Shows variables used near current line

3. **Watch Window** (`Debug > Windows > Watch > Watch 1`):
   - Add custom expressions to monitor
   - Example: Type `BaseURL` to watch its value

4. **Immediate Window** (`Debug > Windows > Immediate`):
   - Execute code while paused
   - Example: Type `? BaseURL` to print value

### Debugging Blueprints + C++

When Blueprint calls C++ UFUNCTION:

1. Set breakpoint in C++ implementation
2. Run Editor with debugger (`F5`)
3. In Editor, run Blueprint (e.g., Press Play)
4. When Blueprint calls UFUNCTION, C++ breakpoint triggers
5. You can see call stack: Blueprint → C++ function

**Call Stack Window** (`Debug > Windows > Call Stack`):
```
NajikaHttpClient.cpp:45 - UNajikaHttpClient::SendLoginRequest()
[External Code] ← Unreal Engine internals
BlueprintVM ← Blueprint execution
```

### Common Debugging Scenarios

#### Scenario 1: Login Request Fails

**Breakpoint location:**
```cpp
void UNajikaHttpClient::SendLoginRequest(const FString& Username, const FString& Password)
{
    // Breakpoint here ← Check if Username/Password are correct
    FString JsonData = FString::Printf(TEXT("{\"username\":\"%s\",\"password\":\"%s\"}"), *Username, *Password);

    // Breakpoint here ← Check if JSON is formatted correctly
    SendRequest(TEXT("/api/auth/login"), JsonData, OnLoginResponse);
}
```

**Check:**
- `Username` value in Locals window
- `Password` value (ensure it's not empty)
- `JsonData` format

#### Scenario 2: Voice Capture Not Starting

**Breakpoint location:**
```cpp
bool UNajikaVoiceCapture::StartCapture()
{
    // Breakpoint here ← Verify Initialize() was called first
    if (!bIsInitialized) {
        UE_LOG(LogNajikaVoice, Error, TEXT("Voice capture not initialized"));
        return false;
    }

    // Breakpoint here ← Check if AudioCapture is valid
    if (!AudioCapture) {
        return false;
    }

    // Continue stepping to see where it fails
}
```

---

## Common Errors & Solutions

### Error 1: "Cannot open include file: 'CoreMinimal.h'"

**Error Message:**
```
error C1083: Cannot open include file: 'CoreMinimal.h': No such file or directory
```

**Cause:** Visual Studio can't find Unreal Engine headers.

**Solution:**
1. Close Visual Studio
2. Right-click `.uproject` file
3. Select **Generate Visual Studio project files**
4. Reopen solution in Visual Studio
5. Rebuild

### Error 2: "LNK2019: unresolved external symbol"

**Error Message:**
```
error LNK2019: unresolved external symbol "public: void __cdecl UNajikaHttpClient::SendRequest(...)"
```

**Cause:** Function declared but not implemented, or missing module dependency.

**Solution:**

**Check 1:** Verify function is implemented in `.cpp` file
```cpp
// NajikaHttpClient.h
void SendRequest(const FString& Endpoint);

// NajikaHttpClient.cpp - MUST EXIST
void UNajikaHttpClient::SendRequest(const FString& Endpoint)
{
    // Implementation
}
```

**Check 2:** Verify module dependency in `.Build.cs`
```csharp
PublicDependencyModuleNames.AddRange(new string[] {
    "Core",
    "HTTP",  // ← Ensure required modules are listed
    "Json"
});
```

### Error 3: "Plugin 'NajikaBackendClient' failed to load"

**Error Message in UE5 Editor:**
```
Plugin 'NajikaBackendClient' failed to load because module 'NajikaBackendClient' could not be loaded.
```

**Cause:** Plugin DLL compilation failed or is out of date.

**Solution:**
1. Close UE5 Editor
2. Delete these folders from project:
   - `Binaries/`
   - `Intermediate/`
   - `Saved/`
3. In Visual Studio, **Build > Rebuild Solution**
4. Wait for full rebuild (30+ minutes)
5. Launch UE5 Editor

### Error 4: "Incompatible or missing module"

**Error Message:**
```
The following modules are missing or built with a different engine version:
- NajikaBackendClient
- NajikaVoiceSystem
```

**Cause:** Plugin built with different UE5 version, or binaries missing.

**Solution:**
1. Right-click `.uproject` file
2. Select **Switch Unreal Engine version**
3. Select your installed UE5 version
4. Regenerate Visual Studio files
5. Rebuild solution in Visual Studio

### Error 5: "MSB3073: exited with code 6"

**Error Message:**
```
error MSB3073: The command "...\UnrealBuildTool.exe" exited with code 6.
```

**Cause:** UnrealBuildTool failed, often due to syntax errors in C++ code.

**Solution:**
1. Check **Error List** window for C++ syntax errors
2. Fix all C++ compilation errors first
3. Common causes:
   - Missing semicolons
   - Mismatched braces
   - Incorrect function signatures
4. Rebuild after fixing errors

### Error 6: "Android NDK not found"

**Error Message:**
```
ERROR: Android NDK not found. Please install Android NDK r21 or higher.
```

**Cause:** Attempting to build for Android without NDK installed.

**Solution:**
See **ANDROID_BUILD_GUIDE.md** for complete Android setup instructions. Quick fix:
1. Open UE5 Editor
2. **Edit > Project Settings**
3. **Platforms > Android**
4. Click **Configure Now**
5. Install Android Studio and NDK
6. Restart Visual Studio

### Error 7: "Hot Reload Failed"

**Error Message in UE5:**
```
Hot Reload Failed
The following modules could not be reloaded:
- NajikaBackendClient
```

**Cause:** Hot Reload limitations exceeded (see Hot Reload Limitations above).

**Solution:**
1. Close UE5 Editor
2. Build in Visual Studio
3. Reopen UE5 Editor
4. Verify changes

### Error 8: "Access Denied" during build

**Error Message:**
```
error : Access to the path '...\Binaries\Win64\UnrealEditor-NajikaBackendClient.dll' is denied.
```

**Cause:** UE5 Editor is running and locking the DLL file.

**Solution:**
1. Close UE5 Editor completely
2. In Visual Studio, **Build > Clean Solution**
3. **Build > Rebuild Solution**
4. Reopen UE5 Editor

---

## Performance Optimization

### Build Performance

#### Enable Multi-Processor Compilation

In Visual Studio:
1. **Tools > Options**
2. **Projects and Solutions > Build and Run**
3. Set **Maximum number of parallel project builds** to your CPU core count (e.g., 8)

#### Disable Unnecessary Features

For faster builds, disable features you don't need:

Edit `NajikaDigivice.Build.cs`:
```csharp
public NajikaDigivice(ReadOnlyTargetRules Target) : base(Target)
{
    // Faster builds
    bUseUnity = true;  // Unity builds (faster)
    bUsePCHFiles = true;  // Precompiled headers
    MinFilesUsingPrecompiledHeaderOverride = 1;
    bFasterWithoutUnity = false;
}
```

#### Use Incredibuild (Optional)

For teams with multiple machines:
- Install Incredibuild to distribute compilation across network
- Can reduce build times by 5-10x
- Commercial license required

### Runtime Performance

#### Profiling C++ Code

1. In UE5 Editor, press `~` (tilde) to open console
2. Type: `stat startfile` to begin profiling
3. Run your gameplay
4. Type: `stat stopfile` to end profiling
5. Find profile data in `Saved/Profiling/`

#### Optimize Hot Paths

Identify slow functions:
```cpp
// Add scoped timers
void UNajikaHttpClient::ProcessResponse(const FString& Response)
{
    SCOPE_CYCLE_COUNTER(STAT_ProcessResponse);  // UE5 profiler marker

    // Your code here
}
```

View in UE5:
- Press `~` → Type `stat game` to see timing stats

---

## Advanced Topics

### Custom Build Configurations

Create a custom configuration for profiling:

1. Edit `NajikaDigivice.Target.cs`:
```csharp
public class NajikaDigiviceTarget : TargetRules
{
    public NajikaDigiviceTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V2;

        // Custom profiling configuration
        if (Configuration == UnrealTargetConfiguration.Development)
        {
            bUseLoggingInShipping = true;
            bUseChecksInShipping = false;
        }
    }
}
```

### Static Code Analysis

Enable Visual Studio Code Analysis:

1. Right-click project in Solution Explorer
2. **Properties**
3. **Code Analysis**
4. Check **Enable Code Analysis on Build**
5. Select **Microsoft All Rules**

Finds potential bugs:
- Memory leaks
- Null pointer dereferences
- Uninitialized variables

### Unit Testing C++

Create unit tests for plugin functions:

1. Create `Tests/` folder in plugin
2. Add test files:

```cpp
// NajikaBackendClientTests.cpp
#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "NajikaHttpClient.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaHttpClientTest, "Najika.HttpClient.Construction",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaHttpClientTest::RunTest(const FString& Parameters)
{
    UNajikaHttpClient* Client = NewObject<UNajikaHttpClient>();
    TestNotNull(TEXT("HttpClient created"), Client);

    return true;
}
```

Run tests:
- In UE5 Editor: **Window > Test Automation**
- Select tests and click **Start Tests**

### Continuous Integration

For automated builds:

**Using GitHub Actions:**

```yaml
# .github/workflows/build-ue5.yml
name: Build UE5 Project

on: [push]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Project
        run: |
          & "C:\Program Files\Epic Games\UE_5.3\Engine\Build\BatchFiles\Build.bat" `
            NajikaDigivice Win64 Development `
            -project="$PWD\NajikaDigivice.uproject"
```

---

## Quick Reference

### Most Used Commands

| Action | Shortcut | Menu |
|--------|----------|------|
| Build Solution | `Ctrl+Shift+B` | Build > Build Solution |
| Start Debugging | `F5` | Debug > Start Debugging |
| Start Without Debugging | `Ctrl+F5` | Debug > Start Without Debugging |
| Attach to Process | `Ctrl+Alt+P` | Debug > Attach to Process |
| Go to Definition | `F12` | Right-click > Go to Definition |
| Find in Files | `Ctrl+Shift+F` | Edit > Find and Replace > Find in Files |
| Toggle Breakpoint | `F9` | Debug > Toggle Breakpoint |
| Clean Solution | - | Build > Clean Solution |
| Rebuild Solution | - | Build > Rebuild Solution |

### Build Order

1. **Clean** (removes all compiled files)
2. **Build** (compiles changed files only)
3. **Rebuild** (clean + build everything)

**When to use:**
- **Build:** Normal development (fastest)
- **Rebuild:** After major changes or errors
- **Clean:** Before creating release build

---

## Next Steps

After successful compilation:

1. ✅ **Launch UE5 Editor** - Verify plugins load correctly
2. ✅ **Enable Plugins** - Edit > Plugins > Enable NajikaBackendClient & NajikaVoiceSystem
3. ✅ **Create Blueprints** - Follow `BLUEPRINT_CREATION_GUIDE.md`
4. ✅ **Build for Android** - Follow `ANDROID_BUILD_GUIDE.md`
5. ✅ **Run Tests** - Follow `TESTING_CHECKLIST.md`

---

## Support

### Documentation Files

- `BLUEPRINT_CREATION_GUIDE.md` - Create Blueprints
- `ANDROID_BUILD_GUIDE.md` - Build APK for Android
- `TESTING_CHECKLIST.md` - Test procedures
- `ASSET_REQUIREMENTS.md` - Asset specifications

### Online Resources

- **Unreal Engine Documentation:** https://docs.unrealengine.com/5.3/
- **UE5 C++ API Reference:** https://docs.unrealengine.com/5.3/en-US/API/
- **Visual Studio Docs:** https://docs.microsoft.com/en-us/visualstudio/

---

**End of Visual Studio Compilation Guide**

*This guide is part of the Najika UE5 Implementation documentation suite.*
