// FactionSystem.h
// Complete Faction/Reputation System with standings, rewards, conflicts

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "FactionSystem.generated.h"

// Reputation Level
UENUM(BlueprintType)
enum class EReputationLevel : uint8
{
    RL_Hated UMETA(DisplayName = "Hated"),
    RL_Hostile UMETA(DisplayName = "Hostile"),
    RL_Unfriendly UMETA(DisplayName = "Unfriendly"),
    RL_Neutral UMETA(DisplayName = "Neutral"),
    RL_Friendly UMETA(DisplayName = "Friendly"),
    RL_Honored UMETA(DisplayName = "Honored"),
    RL_Revered UMETA(DisplayName = "Revered"),
    RL_Exalted UMETA(DisplayName = "Exalted")
};

// Faction Relationship
UENUM(BlueprintType)
enum class EFactionRelationship : uint8
{
    FR_Allied UMETA(DisplayName = "Allied"),
    FR_Friendly UMETA(DisplayName = "Friendly"),
    FR_Neutral UMETA(DisplayName = "Neutral"),
    FR_Hostile UMETA(DisplayName = "Hostile"),
    FR_AtWar UMETA(DisplayName = "At War")
};

// Reputation Reward
USTRUCT(BlueprintType)
struct FReputationReward
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EReputationLevel RequiredLevel;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RewardID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RewardName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 GoldReward = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 XPReward = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> ItemRewards;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString UnlockedShopID;  // Unlock special shop

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString UnlockedQuestID;  // Unlock special quest

    UPROPERTY(BlueprintReadWrite)
    bool bClaimed = false;
};

// Player Reputation with a Faction
USTRUCT(BlueprintType)
struct FPlayerReputation
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString FactionID;

    UPROPERTY(BlueprintReadWrite)
    int32 ReputationPoints = 0;

    UPROPERTY(BlueprintReadWrite)
    EReputationLevel Level = EReputationLevel::RL_Neutral;

    UPROPERTY(BlueprintReadWrite)
    TArray<FReputationReward> AvailableRewards;

    UPROPERTY(BlueprintReadWrite)
    bool bDiscovered = false;  // Has player discovered this faction?

    int32 GetPointsToNextLevel() const;
    int32 GetPointsInCurrentLevel() const;
    float GetProgressToNextLevel() const;
};

// Faction Definition
USTRUCT(BlueprintType)
struct FFaction
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString FactionID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString FactionName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FLinearColor FactionColor = FLinearColor::White;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FReputationReward> Rewards;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, EFactionRelationship> Relationships;  // Other FactionID -> Relationship

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsHidden = false;  // Hidden until discovered

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 StartingReputation = 0;  // Default 0 (Neutral)
};

// Reputation Change Event
USTRUCT(BlueprintType)
struct FReputationChangeEvent
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString FactionID;

    UPROPERTY(BlueprintReadWrite)
    int32 PointsGained;

    UPROPERTY(BlueprintReadWrite)
    EReputationLevel OldLevel;

    UPROPERTY(BlueprintReadWrite)
    EReputationLevel NewLevel;

    UPROPERTY(BlueprintReadWrite)
    FString Reason;  // Quest, Kill, etc.

    UPROPERTY(BlueprintReadWrite)
    FDateTime Timestamp;
};

UCLASS()
class NAJIKATEST_API AFactionSystem : public AActor
{
    GENERATED_BODY()

public:
    AFactionSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== REPUTATION MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Faction|Reputation")
    void AddReputation(const FString& PlayerID, const FString& FactionID, int32 Points, const FString& Reason);

    UFUNCTION(BlueprintCallable, Category = "Faction|Reputation")
    void SetReputation(const FString& PlayerID, const FString& FactionID, int32 Points);

    UFUNCTION(BlueprintPure, Category = "Faction|Reputation")
    int32 GetReputation(const FString& PlayerID, const FString& FactionID) const;

    UFUNCTION(BlueprintPure, Category = "Faction|Reputation")
    EReputationLevel GetReputationLevel(const FString& PlayerID, const FString& FactionID) const;

    UFUNCTION(BlueprintPure, Category = "Faction|Reputation")
    FPlayerReputation GetPlayerReputation(const FString& PlayerID, const FString& FactionID) const;

    // ========== LEVEL CALCULATIONS ==========

    UFUNCTION(BlueprintPure, Category = "Faction|Reputation")
    EReputationLevel CalculateLevel(int32 ReputationPoints) const;

    UFUNCTION(BlueprintPure, Category = "Faction|Reputation")
    int32 GetPointsRequiredForLevel(EReputationLevel Level) const;

    UFUNCTION(BlueprintPure, Category = "Faction|Reputation")
    FString GetReputationLevelName(EReputationLevel Level) const;

    // ========== FACTION QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "Faction|Query")
    FFaction GetFaction(const FString& FactionID) const;

    UFUNCTION(BlueprintPure, Category = "Faction|Query")
    TArray<FFaction> GetAllFactions() const;

    UFUNCTION(BlueprintPure, Category = "Faction|Query")
    TArray<FFaction> GetDiscoveredFactions(const FString& PlayerID) const;

    UFUNCTION(BlueprintCallable, Category = "Faction|Query")
    void DiscoverFaction(const FString& PlayerID, const FString& FactionID);

    // ========== FACTION RELATIONSHIPS ==========

    UFUNCTION(BlueprintPure, Category = "Faction|Relationships")
    EFactionRelationship GetFactionRelationship(const FString& FactionID1, const FString& FactionID2) const;

    UFUNCTION(BlueprintPure, Category = "Faction|Relationships")
    bool AreFactionsFriendly(const FString& FactionID1, const FString& FactionID2) const;

    UFUNCTION(BlueprintPure, Category = "Faction|Relationships")
    bool AreFactionsHostile(const FString& FactionID1, const FString& FactionID2) const;

    UFUNCTION(BlueprintCallable, Category = "Faction|Relationships")
    void SetFactionRelationship(const FString& FactionID1, const FString& FactionID2, EFactionRelationship Relationship);

    // ========== REPUTATION EFFECTS ==========

    UFUNCTION(BlueprintCallable, Category = "Faction|Effects")
    void ApplyReputationDecay(const FString& PlayerID, float DecayPercent);

    UFUNCTION(BlueprintCallable, Category = "Faction|Effects")
    void ApplyConflictingFactionPenalty(const FString& PlayerID, const FString& GainedFactionID, int32 PointsGained);

    // ========== REWARDS ==========

    UFUNCTION(BlueprintPure, Category = "Faction|Rewards")
    TArray<FReputationReward> GetAvailableRewards(const FString& PlayerID, const FString& FactionID) const;

    UFUNCTION(BlueprintCallable, Category = "Faction|Rewards")
    bool ClaimReward(const FString& PlayerID, const FString& FactionID, const FString& RewardID);

    UFUNCTION(BlueprintPure, Category = "Faction|Rewards")
    bool CanClaimReward(const FString& PlayerID, const FString& FactionID, const FString& RewardID) const;

    // ========== REPUTATION HISTORY ==========

    UFUNCTION(BlueprintPure, Category = "Faction|History")
    TArray<FReputationChangeEvent> GetReputationHistory(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Faction|History")
    TArray<FReputationChangeEvent> GetFactionHistory(const FString& PlayerID, const FString& FactionID) const;

    // ========== FACTION MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Faction|Management")
    void RegisterFaction(const FFaction& Faction);

    UFUNCTION(BlueprintCallable, Category = "Faction|Management")
    void UnregisterFaction(const FString& FactionID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnReputationChanged, FString, FactionID, int32, NewReputation, FString, Reason);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnReputationLevelChanged, FString, FactionID, EReputationLevel, OldLevel, EReputationLevel, NewLevel);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnFactionDiscovered, FString, FactionID, FString, FactionName);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnRewardUnlocked, FString, FactionID, FString, RewardID);

    UPROPERTY(BlueprintAssignable, Category = "Faction|Events")
    FOnReputationChanged OnReputationChanged;

    UPROPERTY(BlueprintAssignable, Category = "Faction|Events")
    FOnReputationLevelChanged OnReputationLevelChanged;

    UPROPERTY(BlueprintAssignable, Category = "Faction|Events")
    FOnFactionDiscovered OnFactionDiscovered;

    UPROPERTY(BlueprintAssignable, Category = "Faction|Events")
    FOnRewardUnlocked OnRewardUnlocked;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    TMap<FString, FFaction> Factions;

    // Reputation thresholds for each level
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 HatedThreshold = -36000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 HostileThreshold = -3000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 UnfriendlyThreshold = -300;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 NeutralThreshold = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 FriendlyThreshold = 3000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 HonoredThreshold = 9000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 ReveredThreshold = 21000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    int32 ExaltedThreshold = 42000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    float ConflictingFactionPenalty = 0.1f;  // Lose 10% in opposing factions

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    bool bEnableReputationDecay = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Faction|Config")
    float WeeklyDecayPercent = 0.01f;  // 1% per week

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Faction|State")
    TMap<FString, TMap<FString, FPlayerReputation>> PlayerReputations;  // PlayerID -> (FactionID -> Reputation)

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Faction|State")
    TMap<FString, TArray<FReputationChangeEvent>> ReputationHistory;  // PlayerID -> History

private:
    // ========== HELPER FUNCTIONS ==========

    void InitializePlayerReputation(const FString& PlayerID, const FString& FactionID);
    void UpdateReputationLevel(const FString& PlayerID, const FString& FactionID);
    void CheckAndUnlockRewards(const FString& PlayerID, const FString& FactionID, EReputationLevel NewLevel);
    void AddReputationHistoryEntry(const FString& PlayerID, const FReputationChangeEvent& Event);
    TArray<FString> GetConflictingFactions(const FString& FactionID) const;
};
