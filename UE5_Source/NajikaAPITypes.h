// NajikaAPITypes.h
// Datenstrukturen für Najika World API
// Kopiere diese Datei nach: Source/NajikaWorld/

#pragma once

#include "CoreMinimal.h"
#include "NajikaAPITypes.generated.h"

// ============================================================================
// CHAT API
// ============================================================================

USTRUCT(BlueprintType)
struct FNajikaChatResponse
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Chat")
    FString Response;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Chat")
    FString Mode;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Chat")
    FString Emotion; // excited, sad, angry, tired, happy, explosive

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Chat")
    FString ModelUsed;
};

// ============================================================================
// CHARACTER API
// ============================================================================

USTRUCT(BlueprintType)
struct FNajikaCharacterStats
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Attack = 10.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Defense = 5.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Speed = 8.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Magic = 15.0f;

    // S.P.E.C.I.A.L. Stats (Learning by Doing!)
    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Strength = 5.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Perception = 5.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Endurance = 5.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Charisma = 5.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Intelligence = 5.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Agility = 5.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Stats")
    float Luck = 5.0f;
};

USTRUCT(BlueprintType)
struct FNajikaCharacterStatus
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Status")
    float Health = 100.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Status")
    float MaxHealth = 100.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Status")
    float Stamina = 100.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Status")
    float MaxStamina = 100.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Status")
    float Hunger = 50.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Status")
    float Happiness = 75.0f;
};

// ============================================================================
// COMBAT API (Two-Hand System)
// ============================================================================

UENUM(BlueprintType)
enum class ECombatHand : uint8
{
    Left    UMETA(DisplayName = "Left Hand"),
    Right   UMETA(DisplayName = "Right Hand"),
    Both    UMETA(DisplayName = "Both Hands (Dual)")
};

UENUM(BlueprintType)
enum class EAttackType : uint8
{
    Light   UMETA(DisplayName = "Light Attack"),
    Heavy   UMETA(DisplayName = "Heavy Attack")
};

USTRUCT(BlueprintType)
struct FNajikaCombatResult
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Combat")
    bool bSuccess = false;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Combat")
    float Damage = 0.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Combat")
    bool bCritical = false;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Combat")
    int32 ComboCount = 0;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Combat")
    FString Animation;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Combat")
    FString Message;
};

// ============================================================================
// COMPANION API (Najika's 4 Personalities)
// ============================================================================

UENUM(BlueprintType)
enum class ENajikaPersonality : uint8
{
    Megumin     UMETA(DisplayName = "Megumin (35%) - EXPLOSION!"),
    Harley      UMETA(DisplayName = "Harley Quinn (25%) - Mr. K!"),
    Shiro       UMETA(DisplayName = "Shiro (20%) - Analytical"),
    Melissa     UMETA(DisplayName = "Melissa (20%) - Dominant")
};

USTRUCT(BlueprintType)
struct FNajikaCompanionStatus
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Companion")
    ENajikaPersonality ActivePersonality = ENajikaPersonality::Megumin;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Companion")
    FString Mood;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Companion")
    int32 RelationshipLevel = 1;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Companion")
    FString RelationshipName; // Stranger, Friend, Partner, Soulmate...

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Companion")
    FString CombatStyleName;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Companion")
    float DamageBonus = 1.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Companion")
    float DodgeBonus = 0.0f;
};

// ============================================================================
// MIMIK API (Kuja's Exclusive Character)
// ============================================================================

UENUM(BlueprintType)
enum class EMimikForm : uint8
{
    Chest   UMETA(DisplayName = "Chest Form (Hidden)"),
    Human   UMETA(DisplayName = "Human Form")
};

USTRUCT(BlueprintType)
struct FMimikStatus
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Mimik")
    EMimikForm CurrentForm = EMimikForm::Chest;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Mimik")
    bool bIsHidden = false;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Mimik")
    TArray<FString> StomachContents;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Mimik")
    TArray<FString> UnlockedAbilities;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Mimik")
    int32 NajikaBond = 0;
};

// ============================================================================
// STAT TRAINING API (Learning by Doing!)
// ============================================================================

UENUM(BlueprintType)
enum class ETrainableStat : uint8
{
    Strength    UMETA(DisplayName = "Strength - Heavy lifting, smithing"),
    Endurance   UMETA(DisplayName = "Endurance - Running, swimming"),
    Intelligence UMETA(DisplayName = "Intelligence - Reading, puzzles"),
    Agility     UMETA(DisplayName = "Agility - Archery, lockpicking"),
    Perception  UMETA(DisplayName = "Perception - Hunting, herbalism"),
    Charisma    UMETA(DisplayName = "Charisma - Trading, performing"),
    Luck        UMETA(DisplayName = "Luck - Special events only!")
};

USTRUCT(BlueprintType)
struct FStatTrainingResult
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    bool bSuccess = false;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    FString StatName;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    float OldValue = 0.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    float NewValue = 0.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    float XPGained = 0.0f;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    FString Message;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    int32 TrainingsToday = 0;

    UPROPERTY(BlueprintReadOnly, Category = "Najika|Training")
    int32 MaxTrainingsPerDay = 5;
};

// ============================================================================
// INVENTORY
// ============================================================================

USTRUCT(BlueprintType)
struct FInventoryItem
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Inventory")
    FString ItemId;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Inventory")
    FString Name;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Inventory")
    FString ItemType; // weapon, armor, consumable, material

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Inventory")
    int32 Quantity = 1;

    UPROPERTY(BlueprintReadWrite, Category = "Najika|Inventory")
    bool bIsStackable = true;
};

// ============================================================================
// DELEGATES (für Async Callbacks)
// ============================================================================

DECLARE_DYNAMIC_DELEGATE_OneParam(FOnChatResponse, FNajikaChatResponse, Response);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnCombatResult, FNajikaCombatResult, Result);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnCompanionStatus, FNajikaCompanionStatus, Status);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnMimikStatus, FMimikStatus, Status);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnTrainingResult, FStatTrainingResult, Result);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnAPIError, FString, ErrorMessage);
