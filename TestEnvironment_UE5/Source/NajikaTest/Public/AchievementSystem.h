// AchievementSystem.h
// Complete Achievement/Trophy System with unlocks, rewards, tracking

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AchievementSystem.generated.h"

// Achievement Category
UENUM(BlueprintType)
enum class EAchievementCategory : uint8
{
    AC_Combat UMETA(DisplayName = "Combat"),
    AC_Exploration UMETA(DisplayName = "Exploration"),
    AC_Crafting UMETA(DisplayName = "Crafting"),
    AC_Quest UMETA(DisplayName = "Quest"),
    AC_Collection UMETA(DisplayName = "Collection"),
    AC_Social UMETA(DisplayName = "Social/Multiplayer"),
    AC_Secret UMETA(DisplayName = "Secret")
};

// Achievement Rarity
UENUM(BlueprintType)
enum class EAchievementRarity : uint8
{
    AR_Common UMETA(DisplayName = "Common"),
    AR_Uncommon UMETA(DisplayName = "Uncommon"),
    AR_Rare UMETA(DisplayName = "Rare"),
    AR_Epic UMETA(DisplayName = "Epic"),
    AR_Legendary UMETA(DisplayName = "Legendary")
};

// Achievement Definition
USTRUCT(BlueprintType)
struct FAchievement
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AchievementID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Title;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString UnlockedDescription;  // Revealed after unlock

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EAchievementCategory Category;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EAchievementRarity Rarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredProgress = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentProgress = 0;

    UPROPERTY(BlueprintReadWrite)
    bool bIsUnlocked = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsSecret = false;  // Hidden until unlocked

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RewardGold = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RewardExperience = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> RewardItems;  // Item IDs

    UPROPERTY(BlueprintReadWrite)
    FDateTime UnlockTime;

    float GetProgress() const { return (float)CurrentProgress / (float)RequiredProgress; }
    bool IsComplete() const { return CurrentProgress >= RequiredProgress; }
};

UCLASS()
class NAJIKATEST_API AAchievementSystem : public AActor
{
    GENERATED_BODY()

public:
    AAchievementSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== ACHIEVEMENT MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Achievement")
    void UnlockAchievement(const FString& AchievementID);

    UFUNCTION(BlueprintCallable, Category = "Achievement")
    void AddAchievementProgress(const FString& AchievementID, int32 Amount = 1);

    UFUNCTION(BlueprintCallable, Category = "Achievement")
    void SetAchievementProgress(const FString& AchievementID, int32 Progress);

    // ========== QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "Achievement")
    bool IsAchievementUnlocked(const FString& AchievementID) const;

    UFUNCTION(BlueprintPure, Category = "Achievement")
    FAchievement GetAchievement(const FString& AchievementID) const;

    UFUNCTION(BlueprintPure, Category = "Achievement")
    TArray<FAchievement> GetAllAchievements() const;

    UFUNCTION(BlueprintPure, Category = "Achievement")
    TArray<FAchievement> GetUnlockedAchievements() const;

    UFUNCTION(BlueprintPure, Category = "Achievement")
    TArray<FAchievement> GetLockedAchievements() const;

    UFUNCTION(BlueprintPure, Category = "Achievement")
    TArray<FAchievement> GetAchievementsByCategory(EAchievementCategory Category) const;

    UFUNCTION(BlueprintPure, Category = "Achievement")
    int32 GetAchievementProgress(const FString& AchievementID) const;

    // ========== STATISTICS ==========

    UFUNCTION(BlueprintPure, Category = "Achievement|Stats")
    int32 GetTotalAchievements() const { return Achievements.Num(); }

    UFUNCTION(BlueprintPure, Category = "Achievement|Stats")
    int32 GetUnlockedCount() const;

    UFUNCTION(BlueprintPure, Category = "Achievement|Stats")
    float GetCompletionPercent() const;

    UFUNCTION(BlueprintPure, Category = "Achievement|Stats")
    int32 GetAchievementPoints() const;  // Based on rarity

    // ========== AUTO-TRACKING ==========

    UFUNCTION(BlueprintCallable, Category = "Achievement|AutoTrack")
    void OnEnemyKilled(const FString& EnemyID);

    UFUNCTION(BlueprintCallable, Category = "Achievement|AutoTrack")
    void OnQuestCompleted(const FString& QuestID);

    UFUNCTION(BlueprintCallable, Category = "Achievement|AutoTrack")
    void OnLocationDiscovered(const FString& LocationID);

    UFUNCTION(BlueprintCallable, Category = "Achievement|AutoTrack")
    void OnItemCrafted(const FString& ItemID);

    UFUNCTION(BlueprintCallable, Category = "Achievement|AutoTrack")
    void OnDeath();

    UFUNCTION(BlueprintCallable, Category = "Achievement|AutoTrack")
    void OnDistanceTraveled(float Distance);

    UFUNCTION(BlueprintCallable, Category = "Achievement|AutoTrack")
    void OnPlayerLevel(int32 Level);

    // ========== REWARDS ==========

    UFUNCTION(BlueprintCallable, Category = "Achievement|Rewards")
    void ClaimAchievementReward(const FString& AchievementID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAchievementUnlocked, FAchievement, Achievement);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAchievementProgress, FString, AchievementID, int32, Progress);

    UPROPERTY(BlueprintAssignable, Category = "Achievement|Events")
    FOnAchievementUnlocked OnAchievementUnlocked;

    UPROPERTY(BlueprintAssignable, Category = "Achievement|Events")
    FOnAchievementProgress OnAchievementProgress;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    TMap<FString, FAchievement> Achievements;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    bool bShowNotificationOnUnlock = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    bool bAutoClaimRewards = true;

    // Points per rarity
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    int32 CommonPoints = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    int32 UncommonPoints = 25;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    int32 RarePoints = 50;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    int32 EpicPoints = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Achievement|Config")
    int32 LegendaryPoints = 250;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Achievement|State")
    TArray<FString> UnlockedAchievementIDs;

private:
    // ========== HELPER FUNCTIONS ==========

    void InitializeAchievements();
    void GiveAchievementRewards(const FAchievement& Achievement);
    int32 GetRarityPoints(EAchievementRarity Rarity) const;
    void CheckAchievementCompletion(const FString& AchievementID);
};
