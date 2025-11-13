// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "NajikaBackendTypes.generated.h"

/**
 * Equipment Item Structure
 */
USTRUCT(BlueprintType)
struct FNajikaEquipment
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Equipment")
	FString Weapon;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Equipment")
	FString Armor;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Equipment")
	FString Accessory;

	FNajikaEquipment()
		: Weapon(TEXT(""))
		, Armor(TEXT(""))
		, Accessory(TEXT(""))
	{
	}
};

/**
 * Najika State Structure (matches Python backend najika_server.py STATE["najika"])
 */
USTRUCT(BlueprintType)
struct FNajikaState
{
	GENERATED_BODY()

	// NEEDS (0-100, decay over time)
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Needs")
	float Hunger = 100.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Needs")
	float Thirst = 100.0f;

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

	// EQUIPMENT
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Equipment")
	FNajikaEquipment Equipment;

	// TIMESTAMPS
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Time")
	double LastFed = 0.0;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Time")
	double LastTrained = 0.0;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Time")
	double LastSleep = 0.0;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Time")
	double LastUpdate = 0.0;
};

/**
 * Living System State (matches najika_living_system.py LIVING_STATE)
 */
USTRUCT(BlueprintType)
struct FNajikaLivingState
{
	GENERATED_BODY()

	// Emotional States
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	FString CurrentMood = TEXT("neutral");

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	int32 MoodIntensity = 50;

	// Game Stats
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	float LivingHunger = 100.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	float LivingEnergy = 100.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	float MoodGame = 100.0f;

	// Self-Care
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	float AngerLevel = 0.0f;

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	bool bAutoCareEnabled = true;

	// Control Mode
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	FString ControlMode = TEXT("ai");

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	bool bPlayerOnline = false;

	// Autonomy
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	int32 AutonomyLevel = 50;

	// Growth
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	FString GrowthStage = TEXT("developing");

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	FString RelationshipStage = TEXT("getting_to_know");

	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	int32 EmotionalBond = 0;

	// Activity
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Living")
	FString CurrentActivity;
};

/**
 * Battle State Structure
 */
USTRUCT(BlueprintType)
struct FNajikaBattleState
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	bool bActive = false;

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	int32 HP = 100;

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	int32 MaxHP = 100;

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	int32 Wave = 0;

	UPROPERTY(BlueprintReadWrite, Category = "Battle")
	int32 EnemyCount = 0;
};

/**
 * Enemy Data Structure
 */
USTRUCT(BlueprintType)
struct FNajikaEnemy
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Enemy")
	FString EnemyID;

	UPROPERTY(BlueprintReadWrite, Category = "Enemy")
	FString Name;

	UPROPERTY(BlueprintReadWrite, Category = "Enemy")
	int32 HP = 20;

	UPROPERTY(BlueprintReadWrite, Category = "Enemy")
	int32 MaxHP = 20;

	UPROPERTY(BlueprintReadWrite, Category = "Enemy")
	int32 Attack = 3;

	UPROPERTY(BlueprintReadWrite, Category = "Enemy")
	int32 Defense = 1;

	UPROPERTY(BlueprintReadWrite, Category = "Enemy")
	bool bIsBoss = false;
};

/**
 * Item Data Structure
 */
USTRUCT(BlueprintType)
struct FNajikaItem
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Item")
	FString ItemID;

	UPROPERTY(BlueprintReadWrite, Category = "Item")
	FString Name;

	UPROPERTY(BlueprintReadWrite, Category = "Item")
	FString Type;

	UPROPERTY(BlueprintReadWrite, Category = "Item")
	FString Effect;

	UPROPERTY(BlueprintReadWrite, Category = "Item")
	int32 Value = 0;

	UPROPERTY(BlueprintReadWrite, Category = "Item")
	int32 Duration = 0;

	UPROPERTY(BlueprintReadWrite, Category = "Item")
	FString Description;
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
	int32 Importance = 50;

	UPROPERTY(BlueprintReadWrite, Category = "Chat")
	double Timestamp = 0.0;
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

	UPROPERTY(BlueprintReadWrite, Category = "API")
	FString ErrorMessage;
};

/**
 * Voice Call Stats Structure
 */
USTRUCT(BlueprintType)
struct FNajikaVoiceCallStats
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "VoiceCall")
	int32 TotalCalls = 0;

	UPROPERTY(BlueprintReadWrite, Category = "VoiceCall")
	float TotalDurationSeconds = 0.0f;

	UPROPERTY(BlueprintReadWrite, Category = "VoiceCall")
	float AvgSTTLatencyMS = 0.0f;

	UPROPERTY(BlueprintReadWrite, Category = "VoiceCall")
	float AvgTTSLatencyMS = 0.0f;
};

/**
 * Proactive Message Structure
 */
USTRUCT(BlueprintType)
struct FNajikaProactiveMessage
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Living")
	bool bShouldSend = false;

	UPROPERTY(BlueprintReadWrite, Category = "Living")
	FString Message;

	UPROPERTY(BlueprintReadWrite, Category = "Living")
	FString Mood;

	UPROPERTY(BlueprintReadWrite, Category = "Living")
	FString Reason;
};

// Delegate Declarations

/**
 * Delegate for HTTP Response
 */
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnNajikaHTTPResponse, FNajikaAPIResponse, Response);

/**
 * Delegate for Chat Response (with Najika state)
 */
DECLARE_DYNAMIC_DELEGATE_ThreeParams(FOnNajikaChatResponse, FString, Response, FNajikaState, NajikaState, FNajikaLivingState, LivingState);

/**
 * Delegate for Najika Status
 */
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnNajikaStatusResponse, FNajikaState, NajikaState, FNajikaLivingState, LivingState);

/**
 * Delegate for Battle Start
 */
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnBattleStartResponse, FNajikaBattleState, BattleState, const TArray<FNajikaEnemy>&, Enemies);

/**
 * Delegate for Battle Action
 */
DECLARE_DYNAMIC_DELEGATE_ThreeParams(FOnBattleActionResponse, FNajikaBattleState, BattleState, int32, DamageDealt, bool, bEnemyDefeated);

/**
 * Delegate for Voice Call Audio Response
 */
DECLARE_DYNAMIC_DELEGATE_ThreeParams(FOnVoiceCallAudioResponse, FString, TranscribedText, FString, NajikaResponse, FString, ResponseAudioBase64);

/**
 * Delegate for Generic Success/Fail
 */
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnNajikaActionResponse, bool, bSuccess, FString, Message);

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
