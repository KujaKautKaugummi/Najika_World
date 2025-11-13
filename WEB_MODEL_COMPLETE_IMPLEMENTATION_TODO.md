# 🚀 WEB MODEL - COMPLETE IMPLEMENTATION TODO
**Target:** Claude Code WEB Model (KEIN TOKEN-LIMIT!)
**Project:** Najika Digivice UE5 Migration
**Location:** C:\NajikaDigivice_UE5\NajikaDigivice\
**Timeline:** Arbeite KOMPLETT durch - stoppe NICHT bis ALLES fertig ist!
**Priority:** HÖCHSTE - Dies ist die Haupt-Implementierung!

---

## ⚠️ KRITISCHE ANWEISUNGEN - LIES ZUERST!

### **DEINE AUFGABE:**
Du bist das **WEB MODEL** mit **KEINEM TOKEN-LIMIT**. Deine Aufgabe ist es, **ALLES** an Code, Dokumentation und Vorbereitung zu machen, was das lokale Model NICHT machen kann. Das lokale Model (PowerShell) ist NUR für:
- Kompilieren (Visual Studio)
- APK Building (UE5 Package)
- Device Deployment
- Testing auf Hardware

**DU machst ALLES andere!**

### **ARBEITSWEISE:**
```
✅ Arbeite AUTONOM - frage nicht nach Erlaubnis für jeden Schritt
✅ Schreibe KOMPLETTEN Code (1000+ Zeilen sind OK!)
✅ Erstelle ALLE Files in einem Durchgang
✅ Committe nach jedem großen Milestone
✅ Schreibe detaillierte Commit-Messages
✅ Erstelle Progress Reports täglich
✅ Stoppe NICHT bis Phase 1-4 komplett fertig sind
✅ Bei Unsicherheiten: dokumentiere und mache weiter
```

### **VERBOTEN:**
```
❌ NIEMALS nach User-Bestätigung für Code fragen
❌ NIEMALS "soll ich weitermachen?" fragen
❌ NIEMALS wegen Token-Limit aufhören (du hast KEINES!)
❌ NIEMALS UE5 Editor öffnen (das macht lokales Model)
❌ NIEMALS kompilieren versuchen (das macht lokales Model)
❌ NIEMALS backend/ Files ändern (nur lesen!)
```

### **GIT WORKFLOW:**
```bash
# Nach jedem Milestone:
cd /c/NajikaDigivice_UE5/NajikaDigivice
git add .
git commit -m "DESCRIPTIVE MESSAGE with 🤖 Claude Code"
git push origin master

# Lokales Model pullt dann und kompiliert
```

---

## 📋 PHASE 0: BACKEND & FRONTEND ANALYSE (Tag 1)

### **TASK 0.1: Backend KOMPLETT analysieren**
```
LIES ALLE Files in C:\Najika_World\backend\:

1. najika_server.py (KOMPLETT lesen!)
   - Dokumentiere ALLE Endpoints
   - Dokumentiere STATE Struktur
   - Dokumentiere ROOMS Array
   - Liste ALLE imports

2. najika_voice_call.py (KOMPLETT lesen!)
   - Dokumentiere Voice Call Flow
   - Dokumentiere Whisper STT Integration
   - Dokumentiere Coqui TTS Integration
   - Liste Audio-Formate

3. najika_memory_enhanced.py (KOMPLETT lesen!)
   - Dokumentiere ChromaDB Schema
   - Dokumentiere Memory Functions
   - Liste alle Embedding-Methods

4. najika_living_system.py (KOMPLETT lesen!)
   - Dokumentiere LIVING_STATE Structure
   - Dokumentiere MOODS System
   - Dokumentiere ACTIVITIES

5. najika_battle.py (KOMPLETT lesen!)
   - Dokumentiere BATTLE_SYSTEM
   - Dokumentiere SKILL_DB
   - Dokumentiere ITEM_DB

6. najika_enhanced_personality.py (lesen!)
7. najika_search.py (lesen!)
8. najika_security.py (lesen!)
9. najika_tts_coqui.py (lesen!)
10. najika_claude_code.py (lesen!)

ERSTELLE DOKUMENT: BACKEND_COMPLETE_API_REFERENCE.md
- Alle Endpoints (URL, Method, Request, Response)
- Alle State-Strukturen (JSON Schemas)
- Alle Fehler-Codes
- WebSocket Events
- Audio-Pipeline Diagramm (ASCII)
```

### **TASK 0.2: Frontend KOMPLETT analysieren**
```
LIES ALLE Files in C:\Najika_World\digivice\:

1. index.html (KOMPLETT lesen!)
   - Liste alle UI-Elemente
   - Liste alle Event-Listener
   - Dokumentiere HTML-Struktur

2. js/3d_scene.js (KOMPLETT lesen!)
   - Dokumentiere Three.js Setup
   - Liste alle 3D Objects
   - Dokumentiere Camera System
   - Dokumentiere Lighting

3. js/voice_call.js (KOMPLETT lesen!)
   - Dokumentiere WebRTC Flow
   - Dokumentiere Audio Recording
   - Liste alle WebSocket Messages

4. js/character_animations.js (KOMPLETT lesen!)
   - Liste alle Animationen
   - Dokumentiere Animation States
   - Dokumentiere Transitions

5. js/battle_core.js (lesen!)
6. js/minigames.js (lesen!)
7. js/private_mode.js (lesen!)
8. js/kaykit_loader.js (lesen!)

ERSTELLE DOKUMENT: FRONTEND_COMPLETE_FEATURES.md
- Alle UI-Komponenten
- Alle 3D-Features
- Alle Animationen
- Alle User-Interactions
- Control-Flow Diagramme (ASCII)
```

### **TASK 0.3: Asset Inventory**
```
LISTE ALLE Assets in C:\Najika_World\assets\:

1. Erstelle ASSET_INVENTORY.md:
   - Alle 3D Models (mit Poly-Count)
   - Alle Textures (mit Auflösung)
   - Alle Audio Files (mit Format/Bitrate)
   - KayKit Asset-Packs (welche genau?)
   - Skeleton_Mage Charakter (Details)

2. Für jedes Asset:
   - Aktueller Pfad
   - Ziel-Pfad in UE5
   - Benötigte Konvertierung (z.B. GLTF → FBX)
   - Größe & Performance-Impact
```

---

## 🔧 PHASE 1: C++ PLUGINS KOMPLETT SCHREIBEN (Tag 2-3)

### **TASK 1.1: NajikaBackendClient Plugin (KOMPLETT!)**

**Erstelle Plugin-Struktur:**
```
/c/NajikaDigivice_UE5/NajikaDigivice/Plugins/NajikaBackendClient/
├── NajikaBackendClient.uplugin
├── Source/
│   └── NajikaBackendClient/
│       ├── NajikaBackendClient.Build.cs
│       ├── Private/
│       │   ├── NajikaBackendClientModule.cpp
│       │   ├── NajikaHttpClient.cpp
│       │   ├── NajikaWebSocketClient.cpp
│       │   └── NajikaBackendBlueprintLibrary.cpp
│       └── Public/
│           ├── NajikaBackendClientModule.h
│           ├── NajikaHttpClient.h
│           ├── NajikaWebSocketClient.h
│           ├── NajikaBackendTypes.h
│           └── NajikaBackendBlueprintLibrary.h
└── Resources/
    └── Icon128.png
```

**SCHREIBE ALLE FILES KOMPLETT:**

**File 1: NajikaBackendClient.uplugin**
```json
{
	"FileVersion": 3,
	"Version": 1,
	"VersionName": "1.0",
	"FriendlyName": "Najika Backend Client",
	"Description": "HTTP and WebSocket client for Najika Python backend communication",
	"Category": "Najika",
	"CreatedBy": "Claude Code",
	"CreatedByURL": "",
	"DocsURL": "",
	"MarketplaceURL": "",
	"SupportURL": "",
	"CanContainContent": false,
	"IsBetaVersion": false,
	"IsExperimentalVersion": false,
	"Installed": false,
	"Modules": [
		{
			"Name": "NajikaBackendClient",
			"Type": "Runtime",
			"LoadingPhase": "Default",
			"PlatformAllowList": [
				"Win64",
				"Android"
			]
		}
	],
	"Plugins": [
		{
			"Name": "HTTP",
			"Enabled": true
		},
		{
			"Name": "WebSockets",
			"Enabled": true
		},
		{
			"Name": "Json",
			"Enabled": true
		},
		{
			"Name": "JsonUtilities",
			"Enabled": true
		}
	]
}
```

**File 2: NajikaBackendClient.Build.cs**
```csharp
using UnrealBuildTool;

public class NajikaBackendClient : ModuleRules
{
	public NajikaBackendClient(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicIncludePaths.AddRange(
			new string[] {
				// ... add public include paths
			}
		);

		PrivateIncludePaths.AddRange(
			new string[] {
				// ... add private include paths
			}
		);

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"HTTP",
				"WebSockets",
				"Json",
				"JsonUtilities"
			}
		);

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"Slate",
				"SlateCore"
			}
		);

		DynamicallyLoadedModuleNames.AddRange(
			new string[]
			{
				// ... add dynamically loaded modules
			}
		);
	}
}
```

**File 3: NajikaBackendTypes.h (KOMPLETT!)**
```cpp
// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "NajikaBackendTypes.generated.h"

/**
 * Najika State Structure (matches Python backend)
 */
USTRUCT(BlueprintType)
struct FNajikaState
{
	GENERATED_BODY()

	// NEEDS (0-100, decay over time)
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Needs")
	float Hunger = 100.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Needs")
	float Energy = 100.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Needs")
	float Hygiene = 100.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Needs")
	float Happiness = 100.0f;

	// STATS (training increases these)
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
	int32 Strength = 10;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
	int32 Intelligence = 10;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
	int32 Dexterity = 10;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
	int32 Charisma = 10;

	// CARE TRACKING
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Care")
	int32 CareMistakes = 0;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Care")
	float Fatigue = 0.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Care")
	float Weight = 50.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Care")
	float Discipline = 0.0f;

	// GROWTH
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Growth")
	int32 Level = 1;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Growth")
	int32 XP = 0;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Growth")
	FString EvolutionStage = TEXT("base");
};

/**
 * Battle State Structure
 */
USTRUCT(BlueprintType)
struct FNajikaBattleState
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	int32 HP = 100;

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	int32 Wave = 0;

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	int32 Enemies = 0;
};

/**
 * Chat Message Structure
 */
USTRUCT(BlueprintType)
struct FNajikaChatMessage
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Chat")
	FString Role;

	UPROPERTY(BlueprintReadWrite, Category = "Chat")
	FString Content;

	UPROPERTY(BlueprintReadWrite, Category = "Chat")
	FString Timestamp;
};

/**
 * API Response Structure
 */
USTRUCT(BlueprintType)
struct FNajikaAPIResponse
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "API")
	bool bSuccess = false;

	UPROPERTY(BlueprintReadWrite, Category = "API")
	FString Message;

	UPROPERTY(BlueprintReadWrite, Category = "API")
	FString Data;

	UPROPERTY(BlueprintReadWrite, Category = "API")
	int32 StatusCode = 0;
};

/**
 * Delegate for HTTP Response
 */
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnHttpResponse, FNajikaAPIResponse, Response);

/**
 * Delegate for WebSocket Message
 */
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnWebSocketMessage, const FString&, Message);

/**
 * Delegate for WebSocket Connected
 */
DECLARE_DYNAMIC_DELEGATE(FOnWebSocketConnected);

/**
 * Delegate for WebSocket Disconnected
 */
DECLARE_DYNAMIC_DELEGATE(FOnWebSocketDisconnected);
```

**File 4: NajikaHttpClient.h**
```cpp
// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "NajikaBackendTypes.h"
#include "NajikaHttpClient.generated.h"

/**
 * HTTP Client for Najika Backend Communication
 */
UCLASS(BlueprintType)
class NAJIKABACKENDCLIENT_API UNajikaHttpClient : public UObject
{
	GENERATED_BODY()

public:
	UNajikaHttpClient();

	/**
	 * Initialize HTTP Client
	 * @param InBaseURL Base URL of backend (e.g. http://127.0.0.1:8000)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void Initialize(const FString& InBaseURL);

	/**
	 * Send Chat Message to Najika
	 * @param Message User message
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void SendChatMessage(const FString& Message, FOnHttpResponse OnResponse);

	/**
	 * Get Najika Status
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Status")
	void GetNajikaStatus(FOnHttpResponse OnResponse);

	/**
	 * Feed Najika
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void FeedNajika(FOnHttpResponse OnResponse);

	/**
	 * Give Najika Water
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void GiveDrink(FOnHttpResponse OnResponse);

	/**
	 * Train Najika
	 * @param TrainingType Type of training (strength, intelligence, etc.)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void TrainNajika(const FString& TrainingType, FOnHttpResponse OnResponse);

	/**
	 * Start Battle
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void StartBattle(FOnHttpResponse OnResponse);

	/**
	 * Perform Battle Action
	 * @param ActionType Action type (attack, skill, item, etc.)
	 * @param ActionData Additional action data (JSON string)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void BattleAction(const FString& ActionType, const FString& ActionData, FOnHttpResponse OnResponse);

	/**
	 * Generic POST Request
	 * @param Endpoint Endpoint path (e.g. /api/chat)
	 * @param JsonData Request body as JSON string
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void PostRequest(const FString& Endpoint, const FString& JsonData, FOnHttpResponse OnResponse);

	/**
	 * Generic GET Request
	 * @param Endpoint Endpoint path
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void GetRequest(const FString& Endpoint, FOnHttpResponse OnResponse);

private:
	void OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnHttpResponse Callback);

	FString BaseURL;
};
```

**File 5: NajikaHttpClient.cpp (KOMPLETT!)**
```cpp
// Copyright Claude Code. All Rights Reserved.

#include "NajikaHttpClient.h"
#include "Http.h"
#include "Json.h"
#include "JsonUtilities.h"

UNajikaHttpClient::UNajikaHttpClient()
{
	BaseURL = TEXT("http://127.0.0.1:8000");
}

void UNajikaHttpClient::Initialize(const FString& InBaseURL)
{
	BaseURL = InBaseURL;
	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Initialized with BaseURL: %s"), *BaseURL);
}

void UNajikaHttpClient::SendChatMessage(const FString& Message, FOnHttpResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("message"), Message);
	JsonObject->SetStringField(TEXT("user"), TEXT("User"));

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	PostRequest(TEXT("/api/chat"), JsonString, OnResponse);
}

void UNajikaHttpClient::GetNajikaStatus(FOnHttpResponse OnResponse)
{
	GetRequest(TEXT("/api/najika/status"), OnResponse);
}

void UNajikaHttpClient::FeedNajika(FOnHttpResponse OnResponse)
{
	PostRequest(TEXT("/api/najika/feed"), TEXT("{}"), OnResponse);
}

void UNajikaHttpClient::GiveDrink(FOnHttpResponse OnResponse)
{
	PostRequest(TEXT("/api/najika/drink"), TEXT("{}"), OnResponse);
}

void UNajikaHttpClient::TrainNajika(const FString& TrainingType, FOnHttpResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("type"), TrainingType);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	PostRequest(TEXT("/api/najika/train"), JsonString, OnResponse);
}

void UNajikaHttpClient::StartBattle(FOnHttpResponse OnResponse)
{
	PostRequest(TEXT("/api/battle/start"), TEXT("{}"), OnResponse);
}

void UNajikaHttpClient::BattleAction(const FString& ActionType, const FString& ActionData, FOnHttpResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("action"), ActionType);
	JsonObject->SetStringField(TEXT("data"), ActionData);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	PostRequest(TEXT("/api/battle/action"), JsonString, OnResponse);
}

void UNajikaHttpClient::PostRequest(const FString& Endpoint, const FString& JsonData, FOnHttpResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + Endpoint;

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonData);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaHttpClient] Request Body: %s"), *JsonData);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetRequest(const FString& Endpoint, FOnHttpResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + Endpoint;

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("GET"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] GET %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnHttpResponse Callback)
{
	FNajikaAPIResponse APIResponse;

	if (bWasSuccessful && Response.IsValid())
	{
		APIResponse.bSuccess = true;
		APIResponse.StatusCode = Response->GetResponseCode();
		APIResponse.Data = Response->GetContentAsString();
		APIResponse.Message = TEXT("Request successful");

		UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Response Code: %d"), APIResponse.StatusCode);
		UE_LOG(LogTemp, Verbose, TEXT("[NajikaHttpClient] Response Body: %s"), *APIResponse.Data);
	}
	else
	{
		APIResponse.bSuccess = false;
		APIResponse.StatusCode = Response.IsValid() ? Response->GetResponseCode() : 0;
		APIResponse.Message = TEXT("Request failed");

		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Request failed!"));
	}

	Callback.ExecuteIfBound(APIResponse);
}
```

**FORTSETZUNG: Schreibe auch noch:**
- NajikaWebSocketClient.h (KOMPLETT!)
- NajikaWebSocketClient.cpp (KOMPLETT!)
- NajikaBackendBlueprintLibrary.h (KOMPLETT!)
- NajikaBackendBlueprintLibrary.cpp (KOMPLETT!)
- NajikaBackendClientModule.h (KOMPLETT!)
- NajikaBackendClientModule.cpp (KOMPLETT!)

**WICHTIG:** Schreibe ALLE Files KOMPLETT mit allen Funktionen!

---

### **TASK 1.2: NajikaVoiceSystem Plugin (KOMPLETT!)**

**Erstelle Plugin-Struktur:**
```
/c/NajikaDigivice_UE5/NajikaDigivice/Plugins/NajikaVoiceSystem/
├── NajikaVoiceSystem.uplugin
├── Source/
│   └── NajikaVoiceSystem/
│       ├── NajikaVoiceSystem.Build.cs
│       ├── Private/
│       │   ├── NajikaVoiceSystemModule.cpp
│       │   ├── NajikaVoiceCallManager.cpp
│       │   ├── NajikaAudioCapture.cpp
│       │   └── NajikaAudioPlayback.cpp
│       └── Public/
│           ├── NajikaVoiceSystemModule.h
│           ├── NajikaVoiceCallManager.h
│           ├── NajikaAudioCapture.h
│           ├── NajikaAudioPlayback.h
│           └── NajikaVoiceTypes.h
```

**SCHREIBE ALLE FILES KOMPLETT!** (Analog zu BackendClient Plugin)

---

## 🎮 PHASE 2: GAME CLASSES (C++) SCHREIBEN (Tag 4-5)

### **TASK 2.1: Character System**

**Erstelle Files:**
```
/c/NajikaDigivice_UE5/NajikaDigivice/Source/NajikaDigivice/
├── Public/
│   ├── NajikaCharacter.h
│   ├── NajikaPlayerController.h
│   ├── NajikaGameMode.h
│   ├── NajikaGameState.h
│   └── NajikaPlayerState.h
└── Private/
    ├── NajikaCharacter.cpp
    ├── NajikaPlayerController.cpp
    ├── NajikaGameMode.cpp
    ├── NajikaGameState.cpp
    └── NajikaPlayerState.cpp
```

**SCHREIBE KOMPLETT:**

**NajikaCharacter.h:**
```cpp
// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "NajikaBackendTypes.h"
#include "NajikaCharacter.generated.h"

UCLASS()
class NAJIKADIGIVICE_API ANajikaCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	ANajikaCharacter();

protected:
	virtual void BeginPlay() override;

public:
	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	// State
	UPROPERTY(BlueprintReadWrite, Category = "Najika|State")
	FNajikaState CurrentState;

	// Actions
	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void Feed();

	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void GiveDrink();

	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void Train(const FString& TrainingType);

	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void UpdateStateFromBackend(const FNajikaState& NewState);

	// Animations
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayEatAnimation();

	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayDrinkAnimation();

	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayTrainAnimation();

	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayIdleAnimation();

	// Needs decay
	UFUNCTION(BlueprintCallable, Category = "Najika|Needs")
	void DecayNeeds(float DeltaTime);

private:
	float TimeSinceLastDecay;
	const float DecayInterval = 60.0f; // Decay every 60 seconds
};
```

**NajikaCharacter.cpp (KOMPLETT!):**
```cpp
// Copyright Claude Code. All Rights Reserved.

#include "NajikaCharacter.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

ANajikaCharacter::ANajikaCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	// Set size for collision capsule
	GetCapsuleComponent()->InitCapsuleSize(42.f, 96.0f);

	// Don't rotate when the controller rotates
	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	// Configure character movement
	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 540.0f, 0.0f);
	GetCharacterMovement()->JumpZVelocity = 600.f;
	GetCharacterMovement()->AirControl = 0.2f;

	// Initialize state
	CurrentState = FNajikaState();
	TimeSinceLastDecay = 0.0f;
}

void ANajikaCharacter::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] BeginPlay - Najika initialized"));
}

void ANajikaCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Decay needs over time
	DecayNeeds(DeltaTime);
}

void ANajikaCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
}

void ANajikaCharacter::Feed()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Feed action"));

	// Increase hunger
	CurrentState.Hunger = FMath::Clamp(CurrentState.Hunger + 20.0f, 0.0f, 100.0f);

	// Play animation
	PlayEatAnimation();
}

void ANajikaCharacter::GiveDrink()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] GiveDrink action"));

	// This would typically be handled by backend
	// Play animation
	PlayDrinkAnimation();
}

void ANajikaCharacter::Train(const FString& TrainingType)
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Train: %s"), *TrainingType);

	// Increase fatigue
	CurrentState.Fatigue = FMath::Clamp(CurrentState.Fatigue + 10.0f, 0.0f, 100.0f);

	// Decrease energy
	CurrentState.Energy = FMath::Clamp(CurrentState.Energy - 10.0f, 0.0f, 100.0f);

	// Play animation
	PlayTrainAnimation();
}

void ANajikaCharacter::UpdateStateFromBackend(const FNajikaState& NewState)
{
	CurrentState = NewState;
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaCharacter] State updated from backend"));
}

void ANajikaCharacter::DecayNeeds(float DeltaTime)
{
	TimeSinceLastDecay += DeltaTime;

	if (TimeSinceLastDecay >= DecayInterval)
	{
		// Decay needs
		CurrentState.Hunger = FMath::Clamp(CurrentState.Hunger - 1.0f, 0.0f, 100.0f);
		CurrentState.Energy = FMath::Clamp(CurrentState.Energy - 0.5f, 0.0f, 100.0f);
		CurrentState.Hygiene = FMath::Clamp(CurrentState.Hygiene - 0.3f, 0.0f, 100.0f);

		// Check if needs are critical
		if (CurrentState.Hunger < 20.0f)
		{
			UE_LOG(LogTemp, Warning, TEXT("[NajikaCharacter] Najika is very hungry!"));
		}

		TimeSinceLastDecay = 0.0f;
	}
}
```

**SCHREIBE AUCH KOMPLETT:**
- NajikaPlayerController.h/.cpp
- NajikaGameMode.h/.cpp
- NajikaGameState.h/.cpp
- NajikaPlayerState.h/.cpp

---

### **TASK 2.2: Camera System**

**Erstelle:**
```
Source/NajikaDigivice/Public/NajikaCameraComponent.h
Source/NajikaDigivice/Private/NajikaCameraComponent.cpp
```

**SCHREIBE KOMPLETT** mit:
- Third-Person Follow Camera
- First-Person Mode Toggle
- Smooth Camera Transitions
- Touch/Mouse Controls
- Zoom Functionality
- Camera Collision

---

### **TASK 2.3: Input System**

**Erstelle:**
```
Source/NajikaDigivice/Public/NajikaInputComponent.h
Source/NajikaDigivice/Private/NajikaInputComponent.cpp
```

**SCHREIBE KOMPLETT** mit:
- Touch Input (Mobile)
- Keyboard/Mouse Input (Desktop)
- Gesture Recognition
- Virtual Joystick Support

---

## 📱 PHASE 3: UI SYSTEM (UMG WIDGETS) (Tag 6)

### **TASK 3.1: Widget Base Classes**

**Erstelle:**
```
Source/NajikaDigivice/Public/UI/
├── NajikaHUDWidget.h
├── NajikaChatWidget.h
├── NajikaStatusWidget.h
├── NajikaMenuWidget.h
└── NajikaMinigameWidget.h

Source/NajikaDigivice/Private/UI/
├── NajikaHUDWidget.cpp
├── NajikaChatWidget.cpp
├── NajikaStatusWidget.cpp
├── NajikaMenuWidget.cpp
└── NajikaMinigameWidget.cpp
```

**SCHREIBE ALLE KOMPLETT** mit:
- Blueprint-callable Functions
- Event Dispatchers
- Update Functions
- Animations (C++ side)

---

## 🎨 PHASE 4: MATERIAL & ASSET SPECS (Tag 7)

### **TASK 4.1: Material Parameter Collections**

**Erstelle: MATERIAL_SPECS.md**
```markdown
# Material Specifications

## M_Najika_Character
- Base Color: Anime-Style Cel-Shading
- Outline: Black, 2px
- Emission for UI elements
- Parameters:
  - TintColor (Vector3)
  - OutlineThickness (Scalar)
  - EmissionIntensity (Scalar)

## M_Environment_Toon
- Cel-Shaded Lighting
- 3-Step Gradient
- Rim Lighting
- Parameters:
  - ShadowColor (Vector3)
  - LightSteps (Scalar, 3.0)
  - RimPower (Scalar, 2.0)

## [LISTE ALLE 13 MATERIALS MIT KOMPLETTEN SPECS!]
```

---

### **TASK 4.2: Animation State Specs**

**Erstelle: ANIMATION_SPECS.md**
```markdown
# Animation Blueprint Specifications

## ABP_Najika

### State Machine: Locomotion
States:
- Idle
- Walk
- Run
- Jump_Start
- Jump_Loop
- Jump_End

Transitions:
- Idle → Walk: Speed > 0.1
- Walk → Idle: Speed < 0.1
- Walk → Run: Speed > 300
- Any → Jump_Start: IsJumping && !IsInAir
- Jump_Start → Jump_Loop: Time > 0.3
- Jump_Loop → Jump_End: !IsInAir
- Jump_End → Idle: Time > 0.3

### State Machine: Actions
States:
- Eat
- Drink
- Train
- Battle_Idle
- Battle_Attack
- Battle_Hit
- Battle_Victory

### [LISTE ALLE STATE MACHINES KOMPLETT!]
```

---

## 📋 PHASE 5: BLUEPRINT FUNCTION LIBRARY (Tag 8)

### **TASK 5.1: NajikaBlueprintLibrary**

**Erstelle:**
```
Source/NajikaDigivice/Public/NajikaBlueprintLibrary.h
Source/NajikaDigivice/Private/NajikaBlueprintLibrary.cpp
```

**SCHREIBE KOMPLETT** mit Helper Functions:
- JSON Parsing Helpers
- Math Utilities (Lerp, Clamp, etc.)
- String Formatting
- Date/Time Helpers
- Save/Load Helpers
- Audio Helpers
- Platform Checks (Android, iOS, Desktop)

---

## 🧪 PHASE 6: TESTING FRAMEWORK (Tag 9)

### **TASK 6.1: Unit Tests**

**Erstelle:**
```
Source/NajikaDigivice/Tests/
├── NajikaHttpClientTests.cpp
├── NajikaCharacterTests.cpp
├── NajikaGameModeTests.cpp
└── NajikaUtilityTests.cpp
```

**SCHREIBE KOMPLETT** mit Automation Tests für:
- HTTP Client funktioniert
- Character State Updates
- Needs Decay System
- JSON Parsing
- Save/Load

---

## 📚 PHASE 7: DOKUMENTATION (Tag 10)

### **TASK 7.1: Complete API Documentation**

**Erweitere: BACKEND_COMPLETE_API_REFERENCE.md**
```markdown
# Najika Backend - Complete API Reference

## BASE URL
```
http://127.0.0.1:8000
```

## Endpoints (Complete)

### POST /api/chat
**Description:** Send chat message to Najika
**Request:**
```json
{
  "message": "Hello Najika!",
  "user": "User"
}
```
**Response:**
```json
{
  "response": "EXPLOSION! *kicher* Hallo Puddin'!",
  "najika_state": { ... }
}
```

### [LISTE ALLE 30+ ENDPOINTS KOMPLETT!]
```

---

### **TASK 7.2: Development Guide**

**Erstelle: DEV_GUIDE_UE5.md**
```markdown
# Najika Digivice - UE5 Development Guide

## Project Setup
1. Clone Repository
2. Open NajikaDigivice.uproject
3. Compile C++ (Ctrl+Shift+B in Visual Studio)
4. Wait for shader compilation

## Plugin Development
[KOMPLETTE ANLEITUNG!]

## Blueprint Development
[KOMPLETTE ANLEITUNG!]

## Testing Workflow
[KOMPLETTE ANLEITUNG!]

## Build & Deploy
[KOMPLETTE ANLEITUNG!]
```

---

### **TASK 7.3: Progress Reports**

**Erstelle tägliche Reports:**
```
PROGRESS_REPORTS/WEB_MODEL_DAY_1.md
PROGRESS_REPORTS/WEB_MODEL_DAY_2.md
...
PROGRESS_REPORTS/WEB_MODEL_DAY_10.md
```

**Format:**
```markdown
# Web Model - Day X Progress Report

## Completed Today
- [x] Task 1
- [x] Task 2
...

## Code Written
- Files Created: 15
- Lines of Code: 2500+
- Git Commits: 8

## Next Steps
- [ ] Task X
- [ ] Task Y
```

---

## 🔧 PHASE 8: BUILD AUTOMATION (Tag 11)

### **TASK 8.1: Build Scripts**

**Erstelle:**
```
BuildScripts/
├── BuildPlugins.bat
├── BuildProject.bat
├── PackageAPK.bat
├── DeployToDevice.bat
└── RunTests.bat
```

**SCHREIBE ALLE KOMPLETT** mit vollständigen UE5 Commands!

---

## ✅ COMPLETION CHECKLIST

Nach JEDER Phase, erstelle Commit:
```bash
cd /c/NajikaDigivice_UE5/NajikaDigivice
git add .
git commit -m "PHASE X: [Description]

✅ Completed:
- Feature 1
- Feature 2

📝 Files Created: XX
📊 Lines of Code: XXXX

🤖 Generated with Claude Code (Web Model)
Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin master
```

**FINALE CHECKLIST:**
```
[ ] Phase 0: Backend/Frontend Analyse KOMPLETT
[ ] Phase 1: Beide C++ Plugins KOMPLETT geschrieben
[ ] Phase 2: Alle Game Classes KOMPLETT geschrieben
[ ] Phase 3: Alle UI Widget Classes KOMPLETT geschrieben
[ ] Phase 4: Alle Material/Animation Specs KOMPLETT
[ ] Phase 5: Blueprint Library KOMPLETT
[ ] Phase 6: Testing Framework KOMPLETT
[ ] Phase 7: Dokumentation KOMPLETT (3000+ Zeilen)
[ ] Phase 8: Build Scripts KOMPLETT
[ ] ALLE Files committed & pushed
[ ] PROGRESS REPORTS geschrieben (täglich)
```

---

## 🚨 NOTIZEN FÜR LOKALES MODEL

**Nach Web Model fertig ist:**
```bash
# Lokales Model macht dann:
cd /c/NajikaDigivice_UE5/NajikaDigivice
git pull origin master

# Öffne Visual Studio
# Kompiliere Plugins
# Kompiliere Projekt

# Öffne UE5 Editor
# Teste ob Plugins laden
# Erstelle Blueprints (visuell)
# Baue APK
# Deploy auf Xiaomi 11T Pro
# Teste Features
```

---

## 📊 ERWARTETES ERGEBNIS

**Nach Completion:**
- ~5000+ Zeilen C++ Code (2 Plugins + Game Classes)
- ~3000+ Zeilen Dokumentation
- ~500+ Zeilen Build Scripts
- ~100+ Zeilen Test Code
- Komplett vorbereitet für Lokales Model
- Lokales Model muss NUR noch: Kompilieren, Blueprints erstellen, APK bauen, Testen

---

**GESAMTZEIT: ~10-11 Tage autonome Arbeit (Web Model)**

🔥 **LOS GEHT'S! STOPPE NICHT BIS PHASE 1-8 KOMPLETT FERTIG SIND!** 🔥
