// FishingSystem.h
// Complete Fishing Mini-Game System with rarity, timing, bait, weather effects

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "FishingSystem.generated.h"

// Fishing State
UENUM(BlueprintType)
enum class EFishingState : uint8
{
    FS_Idle UMETA(DisplayName = "Idle"),
    FS_Casting UMETA(DisplayName = "Casting"),
    FS_Waiting UMETA(DisplayName = "Waiting for Bite"),
    FS_Hooked UMETA(DisplayName = "Fish Hooked!"),
    FS_Reeling UMETA(DisplayName = "Reeling In"),
    FS_Success UMETA(DisplayName = "Caught!"),
    FS_Failed UMETA(DisplayName = "Got Away")
};

// Fish Rarity
UENUM(BlueprintType)
enum class EFishRarity : uint8
{
    FR_Common UMETA(DisplayName = "Common"),
    FR_Uncommon UMETA(DisplayName = "Uncommon"),
    FR_Rare UMETA(DisplayName = "Rare"),
    FR_Epic UMETA(DisplayName = "Epic"),
    FR_Legendary UMETA(DisplayName = "Legendary")
};

// Water Type
UENUM(BlueprintType)
enum class EWaterType : uint8
{
    WT_Freshwater UMETA(DisplayName = "Freshwater"),
    WT_Saltwater UMETA(DisplayName = "Saltwater"),
    WT_Lake UMETA(DisplayName = "Lake"),
    WT_River UMETA(DisplayName = "River"),
    WT_Ocean UMETA(DisplayName = "Ocean"),
    WT_Swamp UMETA(DisplayName = "Swamp")
};

// Fish Data
USTRUCT(BlueprintType)
struct FFishData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString FishID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString FishName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EFishRarity Rarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MinSize = 10.0f;  // cm

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MaxSize = 50.0f;  // cm

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 BaseValue = 10;  // Gold

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 XPReward = 5;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<EWaterType> PreferredWaterTypes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Difficulty = 0.5f;  // 0-1, affects mini-game

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bNightOnly = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bRainBonus = false;  // More likely in rain

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString PreferredBaitID;

    int32 GetSellValue(float Size) const
    {
        float SizeMultiplier = (Size - MinSize) / (MaxSize - MinSize);
        return BaseValue * (1.0f + SizeMultiplier);
    }
};

// Bait Item
USTRUCT(BlueprintType)
struct FBaitData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BaitID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BaitName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float RarityBonus = 0.0f;  // Increase rare fish chance

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float BiteSpeedMultiplier = 1.0f;  // Faster bites

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> AttractedFishIDs;  // Specific fish attracted
};

// Fishing Spot
USTRUCT(BlueprintType)
struct FFishingSpot
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString SpotID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector Location;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EWaterType WaterType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Radius = 500.0f;  // 5 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> FishPool;  // Fish IDs that can spawn here

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float RarityBonus = 0.0f;  // Legendary spots

    UPROPERTY(BlueprintReadWrite)
    bool bDepleted = false;

    UPROPERTY(BlueprintReadWrite)
    FDateTime LastFished;
};

// Catch Record
USTRUCT(BlueprintType)
struct FCatchRecord
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString FishID;

    UPROPERTY(BlueprintReadWrite)
    float Size;

    UPROPERTY(BlueprintReadWrite)
    FDateTime CaughtTime;

    UPROPERTY(BlueprintReadWrite)
    FString SpotID;

    UPROPERTY(BlueprintReadWrite)
    bool bIsRecord = false;  // Personal best
};

UCLASS()
class NAJIKATEST_API AFishingSystem : public AActor
{
    GENERATED_BODY()

public:
    AFishingSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== FISHING ACTIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Fishing|Actions")
    void StartFishing(const FVector& CastLocation, const FString& BaitID = "");

    UFUNCTION(BlueprintCallable, Category = "Fishing|Actions")
    void CastLine();

    UFUNCTION(BlueprintCallable, Category = "Fishing|Actions")
    void ReelIn();

    UFUNCTION(BlueprintCallable, Category = "Fishing|Actions")
    void CancelFishing();

    UFUNCTION(BlueprintPure, Category = "Fishing|Actions")
    bool IsFishing() const { return CurrentState != EFishingState::FS_Idle; }

    UFUNCTION(BlueprintPure, Category = "Fishing|Actions")
    EFishingState GetFishingState() const { return CurrentState; }

    // ========== MINI-GAME ==========

    UFUNCTION(BlueprintCallable, Category = "Fishing|MiniGame")
    void OnPlayerInput(float InputValue);  // -1 to 1 for reeling direction

    UFUNCTION(BlueprintPure, Category = "Fishing|MiniGame")
    float GetTension() const { return LineTension; }

    UFUNCTION(BlueprintPure, Category = "Fishing|MiniGame")
    float GetProgress() const { return ReelingProgress; }

    UFUNCTION(BlueprintPure, Category = "Fishing|MiniGame")
    float GetTargetZone() const { return TargetZone; }

    UFUNCTION(BlueprintPure, Category = "Fishing|MiniGame")
    float GetPlayerZone() const { return PlayerZone; }

    // ========== CATCHES ==========

    UFUNCTION(BlueprintPure, Category = "Fishing|Catches")
    TArray<FCatchRecord> GetCatchHistory() const { return CatchHistory; }

    UFUNCTION(BlueprintPure, Category = "Fishing|Catches")
    FCatchRecord GetBiggestCatch(const FString& FishID) const;

    UFUNCTION(BlueprintPure, Category = "Fishing|Catches")
    int32 GetTotalCatches() const { return CatchHistory.Num(); }

    UFUNCTION(BlueprintPure, Category = "Fishing|Catches")
    int32 GetUniqueFishCaught() const;

    // ========== FISHING SPOTS ==========

    UFUNCTION(BlueprintCallable, Category = "Fishing|Spots")
    void RegisterFishingSpot(const FFishingSpot& Spot);

    UFUNCTION(BlueprintPure, Category = "Fishing|Spots")
    FFishingSpot GetNearestFishingSpot(const FVector& Location) const;

    UFUNCTION(BlueprintPure, Category = "Fishing|Spots")
    bool IsInFishingSpot(const FVector& Location) const;

    // ========== BAIT MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Fishing|Bait")
    void EquipBait(const FString& BaitID);

    UFUNCTION(BlueprintCallable, Category = "Fishing|Bait")
    void UnequipBait();

    UFUNCTION(BlueprintPure, Category = "Fishing|Bait")
    FString GetEquippedBait() const { return CurrentBaitID; }

    UFUNCTION(BlueprintPure, Category = "Fishing|Bait")
    bool HasBait() const { return !CurrentBaitID.IsEmpty(); }

    // ========== FISHING STATS ==========

    UFUNCTION(BlueprintPure, Category = "Fishing|Stats")
    int32 GetFishingLevel() const { return FishingLevel; }

    UFUNCTION(BlueprintPure, Category = "Fishing|Stats")
    int32 GetFishingXP() const { return FishingXP; }

    UFUNCTION(BlueprintCallable, Category = "Fishing|Stats")
    void AddFishingXP(int32 XP);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnFishingStarted);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnFishBite);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnFishCaught, FFishData, Fish, float, Size);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnFishEscaped);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLineBroke, float, Tension);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLevelUp, int32, NewLevel);

    UPROPERTY(BlueprintAssignable, Category = "Fishing|Events")
    FOnFishingStarted OnFishingStarted;

    UPROPERTY(BlueprintAssignable, Category = "Fishing|Events")
    FOnFishBite OnFishBite;

    UPROPERTY(BlueprintAssignable, Category = "Fishing|Events")
    FOnFishCaught OnFishCaught;

    UPROPERTY(BlueprintAssignable, Category = "Fishing|Events")
    FOnFishEscaped OnFishEscaped;

    UPROPERTY(BlueprintAssignable, Category = "Fishing|Events")
    FOnLineBroke OnLineBroke;

    UPROPERTY(BlueprintAssignable, Category = "Fishing|Events")
    FOnLevelUp OnLevelUp;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    TMap<FString, FFishData> FishDatabase;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    TMap<FString, FBaitData> BaitDatabase;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    TArray<FFishingSpot> FishingSpots;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float MinWaitTime = 3.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float MaxWaitTime = 15.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float BiteWindow = 2.0f;  // Time to react to bite

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float MaxLineTension = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float TensionBreakThreshold = 90.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float ReelingSpeed = 10.0f;  // Units per second

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float XPPerCatch = 10;

    // Rarity chances (without modifiers)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float CommonChance = 0.60f;  // 60%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float UncommonChance = 0.25f;  // 25%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float RareChance = 0.10f;  // 10%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float EpicChance = 0.04f;  // 4%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Fishing|Config")
    float LegendaryChance = 0.01f;  // 1%

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    EFishingState CurrentState = EFishingState::FS_Idle;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    FString CurrentBaitID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    FFishData CurrentFish;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    float CurrentFishSize = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    float LineTension = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    float ReelingProgress = 0.0f;  // 0-100

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    float TargetZone = 0.5f;  // 0-1, where fish wants to be

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    float PlayerZone = 0.5f;  // 0-1, where player is reeling

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    TArray<FCatchRecord> CatchHistory;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    int32 FishingLevel = 1;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    int32 FishingXP = 0;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fishing|State")
    float TimeSinceCast = 0.0f;

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateWaitingState(float DeltaTime);
    void UpdateReelingState(float DeltaTime);
    FFishData RollForFish();
    EFishRarity RollRarity() const;
    float RollFishSize(const FFishData& Fish) const;
    void CompleteCatch();
    void FishEscaped();
    void CheckLevelUp();
};
