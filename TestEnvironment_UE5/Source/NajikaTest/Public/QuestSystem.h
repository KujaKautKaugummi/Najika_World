// QuestSystem.h
// Complete Quest System: Missions, Objectives, Rewards, Tracking

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "QuestSystem.generated.h"

// Quest Type
UENUM(BlueprintType)
enum class EQuestType : uint8
{
    QT_Main UMETA(DisplayName = "Main Quest"),
    QT_Side UMETA(DisplayName = "Side Quest"),
    QT_Daily UMETA(DisplayName = "Daily Quest"),
    QT_Repeatable UMETA(DisplayName = "Repeatable"),
    QT_Hidden UMETA(DisplayName = "Hidden/Secret")
};

// Quest Status
UENUM(BlueprintType)
enum class EQuestStatus : uint8
{
    QS_NotStarted UMETA(DisplayName = "Not Started"),
    QS_Active UMETA(DisplayName = "Active"),
    QS_Completed UMETA(DisplayName = "Completed"),
    QS_Failed UMETA(DisplayName = "Failed"),
    QS_TurnedIn UMETA(DisplayName = "Turned In")
};

// Objective Type
UENUM(BlueprintType)
enum class EObjectiveType : uint8
{
    OT_Kill UMETA(DisplayName = "Kill Enemies"),
    OT_Collect UMETA(DisplayName = "Collect Items"),
    OT_Reach UMETA(DisplayName = "Reach Location"),
    OT_Talk UMETA(DisplayName = "Talk to NPC"),
    OT_Escort UMETA(DisplayName = "Escort NPC"),
    OT_Defend UMETA(DisplayName = "Defend Location"),
    OT_Craft UMETA(DisplayName = "Craft Item"),
    OT_Use UMETA(DisplayName = "Use Item/Skill"),
    OT_Discover UMETA(DisplayName = "Discover Location")
};

// Quest Objective
USTRUCT(BlueprintType)
struct FQuestObjective
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ObjectiveID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EObjectiveType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TargetID;  // Enemy ID, Item ID, Location ID, etc.

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredCount = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentCount = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsOptional = false;

    UPROPERTY(BlueprintReadWrite)
    bool bIsCompleted = false;

    float GetProgress() const { return (float)CurrentCount / (float)RequiredCount; }
    bool IsComplete() const { return CurrentCount >= RequiredCount; }
};

// Quest Reward
USTRUCT(BlueprintType)
struct FQuestReward
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Experience = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Gold = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> ItemRewards;  // Item IDs

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<int32> ItemQuantities;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString UnlockTalent;  // Talent ID to unlock

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 SkillExperience = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString UnlockRecipe;  // Crafting recipe ID
};

// Complete Quest Definition
USTRUCT(BlueprintType)
struct FQuest
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString QuestID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString QuestName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EQuestType Type;

    UPROPERTY(BlueprintReadWrite)
    EQuestStatus Status = EQuestStatus::QS_NotStarted;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> PrerequisiteQuests;  // Quest IDs required

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FQuestObjective> Objectives;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FQuestReward Reward;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString QuestGiverID;  // NPC ID

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCanAbandon = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsRepeatable = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float TimeLimit = 0.0f;  // 0 = no limit

    UPROPERTY(BlueprintReadWrite)
    float TimeRemaining = 0.0f;

    bool AreAllObjectivesComplete() const
    {
        for (const FQuestObjective& Obj : Objectives)
        {
            if (!Obj.bIsOptional && !Obj.bIsCompleted)
            {
                return false;
            }
        }
        return true;
    }
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class NAJIKATEST_API UQuestSystem : public UActorComponent
{
    GENERATED_BODY()

public:
    UQuestSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    // ========== QUEST MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Quest")
    bool AcceptQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest")
    bool CompleteQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest")
    bool AbandonQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest")
    bool TurnInQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest")
    bool FailQuest(const FString& QuestID);

    // ========== OBJECTIVE PROGRESS ==========

    UFUNCTION(BlueprintCallable, Category = "Quest|Objective")
    void UpdateObjectiveProgress(const FString& QuestID, const FString& ObjectiveID, int32 Amount = 1);

    UFUNCTION(BlueprintCallable, Category = "Quest|Objective")
    void SetObjectiveComplete(const FString& QuestID, const FString& ObjectiveID);

    UFUNCTION(BlueprintCallable, Category = "Quest|Objective")
    bool IsObjectiveComplete(const FString& QuestID, const FString& ObjectiveID) const;

    // ========== QUEST QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "Quest")
    TArray<FQuest> GetActiveQuests() const;

    UFUNCTION(BlueprintPure, Category = "Quest")
    TArray<FQuest> GetCompletedQuests() const;

    UFUNCTION(BlueprintPure, Category = "Quest")
    TArray<FQuest> GetAvailableQuests() const;

    UFUNCTION(BlueprintPure, Category = "Quest")
    FQuest GetQuest(const FString& QuestID) const;

    UFUNCTION(BlueprintPure, Category = "Quest")
    bool HasQuest(const FString& QuestID) const;

    UFUNCTION(BlueprintPure, Category = "Quest")
    bool IsQuestActive(const FString& QuestID) const;

    UFUNCTION(BlueprintPure, Category = "Quest")
    bool IsQuestCompleted(const FString& QuestID) const;

    // ========== QUEST TRACKING ==========

    UFUNCTION(BlueprintCallable, Category = "Quest|Tracking")
    void TrackQuest(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Quest|Tracking")
    void UntrackQuest();

    UFUNCTION(BlueprintPure, Category = "Quest|Tracking")
    FQuest GetTrackedQuest() const;

    UFUNCTION(BlueprintPure, Category = "Quest|Tracking")
    bool HasTrackedQuest() const { return !TrackedQuestID.IsEmpty(); }

    // ========== QUEST CONDITIONS ==========

    UFUNCTION(BlueprintPure, Category = "Quest")
    bool CanAcceptQuest(const FString& QuestID) const;

    UFUNCTION(BlueprintPure, Category = "Quest")
    bool CanTurnInQuest(const FString& QuestID) const;

    // ========== AUTO-TRACKING ==========

    UFUNCTION(BlueprintCallable, Category = "Quest|Auto")
    void OnEnemyKilled(const FString& EnemyID);

    UFUNCTION(BlueprintCallable, Category = "Quest|Auto")
    void OnItemCollected(const FString& ItemID, int32 Amount = 1);

    UFUNCTION(BlueprintCallable, Category = "Quest|Auto")
    void OnLocationReached(const FString& LocationID);

    UFUNCTION(BlueprintCallable, Category = "Quest|Auto")
    void OnNPCTalked(const FString& NPCID);

    UFUNCTION(BlueprintCallable, Category = "Quest|Auto")
    void OnItemCrafted(const FString& ItemID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestAccepted, FQuest, Quest);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestCompleted, FQuest, Quest);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnObjectiveUpdated, FString, QuestID, FQuestObjective, Objective);

    UPROPERTY(BlueprintAssignable, Category = "Quest|Events")
    FOnQuestAccepted OnQuestAccepted;

    UPROPERTY(BlueprintAssignable, Category = "Quest|Events")
    FOnQuestCompleted OnQuestCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Quest|Events")
    FOnObjectiveUpdated OnObjectiveUpdated;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest|Config")
    TMap<FString, FQuest> AllQuests;  // Quest database

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest|Config")
    int32 MaxActiveQuests = 10;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Quest|State")
    TArray<FQuest> ActiveQuests;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Quest|State")
    TArray<FString> CompletedQuestIDs;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Quest|State")
    FString TrackedQuestID;

private:
    // ========== HELPER FUNCTIONS ==========

    void GiveQuestRewards(const FQuest& Quest);
    void UpdateQuestTimers(float DeltaTime);
    void CheckQuestCompletion(FQuest& Quest);
    FQuest* FindActiveQuest(const FString& QuestID);
};
