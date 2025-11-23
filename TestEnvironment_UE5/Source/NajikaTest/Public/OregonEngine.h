// OregonEngine.h
// Procedural Event System - >1 Million scene variations
// Section 2.3 from PDF: Grammar-based dimensional events

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "OregonEngine.generated.h"

// Event Dimensions (Grammar)
UENUM(BlueprintType)
enum class EBiome : uint8
{
    B_Forest UMETA(DisplayName = "Wald"),
    B_Mountain UMETA(DisplayName = "Berg"),
    B_Desert UMETA(DisplayName = "Wüste"),
    B_Snow UMETA(DisplayName = "Schnee"),
    B_Swamp UMETA(DisplayName = "Sumpf"),
    B_Volcano UMETA(DisplayName = "Vulkan"),
    B_Ocean UMETA(DisplayName = "Ozean")
};

UENUM(BlueprintType)
enum class EWeather : uint8
{
    W_Clear UMETA(DisplayName = "Klar"),
    W_Rain UMETA(DisplayName = "Regen"),
    W_Storm UMETA(DisplayName = "Sturm"),
    W_Snow UMETA(DisplayName = "Schnee"),
    W_Fog UMETA(DisplayName = "Nebel"),
    W_Sandstorm UMETA(DisplayName = "Sandsturm"),
    W_Heatwave UMETA(DisplayName = "Hitze")
};

UENUM(BlueprintType)
enum class ETimeOfDay : uint8
{
    T_Morning UMETA(DisplayName = "Morgen"),
    T_Noon UMETA(DisplayName = "Mittag"),
    T_Evening UMETA(DisplayName = "Abend"),
    T_Night UMETA(DisplayName = "Nacht"),
    T_Midnight UMETA(DisplayName = "Mitternacht")
};

UENUM(BlueprintType)
enum class EHazard : uint8
{
    H_None UMETA(DisplayName = "Keine"),
    H_Bandits UMETA(DisplayName = "Banditen"),
    H_Monsters UMETA(DisplayName = "Monster"),
    H_Ambush UMETA(DisplayName = "Hinterhalt"),
    H_Trap UMETA(DisplayName = "Falle"),
    H_Poison UMETA(DisplayName = "Gift"),
    H_Fire UMETA(DisplayName = "Feuer"),
    H_Avalanche UMETA(DisplayName = "Lawine")
};

UENUM(BlueprintType)
enum class EActor : uint8
{
    A_Merchant UMETA(DisplayName = "Händler"),
    A_Traveler UMETA(DisplayName = "Reisender"),
    A_Guard UMETA(DisplayName = "Wache"),
    A_Hermit UMETA(DisplayName = "Einsiedler"),
    A_Child UMETA(DisplayName = "Kind"),
    A_Elder UMETA(DisplayName = "Ältester"),
    A_Knight UMETA(DisplayName = "Ritter"),
    A_Mage UMETA(DisplayName = "Magier")
};

UENUM(BlueprintType)
enum class ECause : uint8
{
    C_Lost UMETA(DisplayName = "Verirrt"),
    C_Injured UMETA(DisplayName = "Verletzt"),
    C_Attacked UMETA(DisplayName = "Angegriffen"),
    C_Robbed UMETA(DisplayName = "Ausgeraubt"),
    C_Cursed UMETA(DisplayName = "Verflucht"),
    C_Seeking UMETA(DisplayName = "Sucht etwas"),
    C_Fleeing UMETA(DisplayName = "Auf der Flucht")
};

UENUM(BlueprintType)
enum class EConsequence : uint8
{
    C_Help UMETA(DisplayName = "Hilfe anbieten"),
    C_Ignore UMETA(DisplayName = "Ignorieren"),
    C_Attack UMETA(DisplayName = "Angreifen"),
    C_Trade UMETA(DisplayName = "Handeln"),
    C_Escort UMETA(DisplayName = "Begleiten"),
    C_Heal UMETA(DisplayName = "Heilen")
};

// Complete Event Definition
USTRUCT(BlueprintType)
struct FOregonEvent
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EventID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EBiome Biome;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EWeather Weather;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ETimeOfDay TimeOfDay;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EHazard Hazard;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EActor Actor;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ECause Cause;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<EConsequence> AvailableChoices;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EventText;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<EConsequence, FString> ChoiceOutcomes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<EConsequence, int32> RewardGold;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<EConsequence, int32> RewardXP;

    // In-World experience (no UI popups)
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsInWorld = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector SpawnLocation = FVector::ZeroVector;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    AActor* EventActor = nullptr;
};

// Event Statistics for Meta-Learning
USTRUCT(BlueprintType)
struct FOregonEventStats
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    int32 TimesTriggered = 0;

    UPROPERTY(BlueprintReadOnly)
    TMap<EConsequence, int32> ChoiceFrequency;

    UPROPERTY(BlueprintReadOnly)
    float AveragePlayerLevel = 0.0f;

    UPROPERTY(BlueprintReadOnly)
    float SuccessRate = 0.0f;
};

UCLASS()
class NAJIKATEST_API AOregonEngine : public AActor
{
    GENERATED_BODY()

public:
    AOregonEngine();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== EVENT GENERATION ==========

    UFUNCTION(BlueprintCallable, Category = "Oregon|Generation")
    FOregonEvent GenerateRandomEvent();

    UFUNCTION(BlueprintCallable, Category = "Oregon|Generation")
    FOregonEvent GenerateContextualEvent(EBiome CurrentBiome, EWeather CurrentWeather, ETimeOfDay CurrentTime);

    UFUNCTION(BlueprintCallable, Category = "Oregon|Generation")
    void TriggerEvent(const FOregonEvent& Event);

    // ========== EVENT RESOLUTION ==========

    UFUNCTION(BlueprintCallable, Category = "Oregon|Resolution")
    void ResolveEvent(const FOregonEvent& Event, EConsequence PlayerChoice);

    UFUNCTION(BlueprintPure, Category = "Oregon|Resolution")
    FString GetOutcomeText(const FOregonEvent& Event, EConsequence Choice) const;

    // ========== EVENT STATISTICS ==========

    UFUNCTION(BlueprintCallable, Category = "Oregon|Statistics")
    void RecordEventChoice(const FString& EventID, EConsequence Choice);

    UFUNCTION(BlueprintPure, Category = "Oregon|Statistics")
    FOregonEventStats GetEventStats(const FString& EventID) const;

    UFUNCTION(BlueprintPure, Category = "Oregon|Statistics")
    int32 GetTotalEventVariations() const;

    // ========== IN-WORLD SPAWNING ==========

    UFUNCTION(BlueprintCallable, Category = "Oregon|World")
    void SpawnEventInWorld(const FOregonEvent& Event, FVector Location);

    UFUNCTION(BlueprintCallable, Category = "Oregon|World")
    void DespawnEvent(const FOregonEvent& Event);

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Oregon|Config")
    float EventSpawnInterval = 300.0f;  // Every 5 minutes

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Oregon|Config")
    float EventSpawnRadius = 5000.0f;  // 50 meters from player

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Oregon|Config")
    int32 MaxActiveEvents = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Oregon|Config")
    bool bEnableInWorldEvents = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Oregon|State")
    TArray<FOregonEvent> ActiveEvents;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Oregon|State")
    TMap<FString, FOregonEventStats> EventStatistics;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Oregon|State")
    EBiome CurrentBiome = EBiome::B_Forest;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Oregon|State")
    EWeather CurrentWeather = EWeather::W_Clear;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Oregon|State")
    ETimeOfDay CurrentTimeOfDay = ETimeOfDay::T_Morning;

private:
    // ========== EVENT TIMER ==========

    float TimeSinceLastEvent = 0.0f;

    // ========== HELPER FUNCTIONS ==========

    FString GenerateEventText(const FOregonEvent& Event) const;
    TArray<EConsequence> GetAvailableChoices(const FOregonEvent& Event) const;
    void ApplyEventOutcome(const FOregonEvent& Event, EConsequence Choice);

    // ========== RANDOM GENERATION ==========

    template<typename TEnum>
    TEnum GetRandomEnumValue() const;
};
