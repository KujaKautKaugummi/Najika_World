// ProgressionComponent.h
// Complete Progression System: XP, Levels, Skills, Talents, Attributes

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ProgressionComponent.generated.h"

// Attribute Type
UENUM(BlueprintType)
enum class EAttributeType : uint8
{
    AT_Strength UMETA(DisplayName = "Strength"),
    AT_Dexterity UMETA(DisplayName = "Dexterity"),
    AT_Intelligence UMETA(DisplayName = "Intelligence"),
    AT_Vitality UMETA(DisplayName = "Vitality"),
    AT_Luck UMETA(DisplayName = "Luck")
};

// Skill Type (Use-based progression - Hard Rule #5!)
UENUM(BlueprintType)
enum class ESkillType : uint8
{
    SK_OneHanded UMETA(DisplayName = "One-Handed"),
    SK_TwoHanded UMETA(DisplayName = "Two-Handed"),
    SK_Archery UMETA(DisplayName = "Archery"),
    SK_Magic UMETA(DisplayName = "Magic"),
    SK_Explosion UMETA(DisplayName = "Explosion"),
    SK_Defense UMETA(DisplayName = "Defense"),
    SK_Crafting UMETA(DisplayName = "Crafting"),
    SK_Alchemy UMETA(DisplayName = "Alchemy"),
    SK_Stealth UMETA(DisplayName = "Stealth"),
    SK_Survival UMETA(DisplayName = "Survival")
};

// Skill Data
USTRUCT(BlueprintType)
struct FSkillData
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    ESkillType SkillType;

    UPROPERTY(BlueprintReadWrite)
    int32 Level = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 Experience = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 ExperienceToNextLevel = 100;

    UPROPERTY(BlueprintReadWrite)
    int32 TotalUses = 0;  // Use-based tracking
};

// Talent Node
USTRUCT(BlueprintType)
struct FTalentNode
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TalentID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TalentName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredPoints = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> Prerequisites;  // Other talent IDs required

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> StatBonuses;  // "Damage": 1.05 (5% increase)

    UPROPERTY(BlueprintReadWrite)
    bool bIsUnlocked = false;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentRank = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxRank = 5;
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class NAJIKATEST_API UProgressionComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UProgressionComponent();

protected:
    virtual void BeginPlay() override;

public:
    // ========== EXPERIENCE & LEVEL ==========

    UFUNCTION(BlueprintCallable, Category = "Progression|Level")
    void AddExperience(int32 Amount);

    UFUNCTION(BlueprintPure, Category = "Progression|Level")
    int32 GetLevel() const { return Level; }

    UFUNCTION(BlueprintPure, Category = "Progression|Level")
    int32 GetExperience() const { return Experience; }

    UFUNCTION(BlueprintPure, Category = "Progression|Level")
    int32 GetExperienceToNextLevel() const { return ExperienceToNextLevel; }

    UFUNCTION(BlueprintPure, Category = "Progression|Level")
    float GetExperiencePercent() const;

    // ========== SKILLS (Use-based - Hard Rule #5!) ==========

    UFUNCTION(BlueprintCallable, Category = "Progression|Skills")
    void AddSkillExperience(ESkillType SkillType, int32 Amount);

    UFUNCTION(BlueprintCallable, Category = "Progression|Skills")
    void UseSkill(ESkillType SkillType);  // Call this when player uses skill

    UFUNCTION(BlueprintPure, Category = "Progression|Skills")
    FSkillData GetSkillData(ESkillType SkillType) const;

    UFUNCTION(BlueprintPure, Category = "Progression|Skills")
    int32 GetSkillLevel(ESkillType SkillType) const;

    UFUNCTION(BlueprintPure, Category = "Progression|Skills")
    TArray<FSkillData> GetAllSkills() const;

    // ========== ATTRIBUTES ==========

    UFUNCTION(BlueprintCallable, Category = "Progression|Attributes")
    void AddAttributePoint(EAttributeType Attribute);

    UFUNCTION(BlueprintPure, Category = "Progression|Attributes")
    int32 GetAttributeValue(EAttributeType Attribute) const;

    UFUNCTION(BlueprintPure, Category = "Progression|Attributes")
    int32 GetAvailableAttributePoints() const { return AttributePoints; }

    // ========== TALENTS ==========

    UFUNCTION(BlueprintCallable, Category = "Progression|Talents")
    bool UnlockTalent(const FString& TalentID);

    UFUNCTION(BlueprintCallable, Category = "Progression|Talents")
    bool UpgradeTalent(const FString& TalentID);

    UFUNCTION(BlueprintPure, Category = "Progression|Talents")
    bool IsTalentUnlocked(const FString& TalentID) const;

    UFUNCTION(BlueprintPure, Category = "Progression|Talents")
    int32 GetTalentRank(const FString& TalentID) const;

    UFUNCTION(BlueprintPure, Category = "Progression|Talents")
    int32 GetAvailableTalentPoints() const { return TalentPoints; }

    UFUNCTION(BlueprintPure, Category = "Progression|Talents")
    TArray<FTalentNode> GetUnlockedTalents() const;

    // ========== STAT BONUSES ==========

    UFUNCTION(BlueprintPure, Category = "Progression|Stats")
    float GetTotalStatBonus(const FString& StatName) const;

    UFUNCTION(BlueprintPure, Category = "Progression|Stats")
    TMap<FString, float> GetAllStatBonuses() const;

    // ========== PRESTIGE/RESET ==========

    UFUNCTION(BlueprintCallable, Category = "Progression|Prestige")
    void PrestigeReset();

    UFUNCTION(BlueprintPure, Category = "Progression|Prestige")
    int32 GetPrestigeLevel() const { return PrestigeLevel; }

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLevelUp, int32, NewLevel);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnSkillLevelUp, ESkillType, SkillType, int32, NewLevel);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTalentUnlocked, FString, TalentID);

    UPROPERTY(BlueprintAssignable, Category = "Progression|Events")
    FOnLevelUp OnLevelUp;

    UPROPERTY(BlueprintAssignable, Category = "Progression|Events")
    FOnSkillLevelUp OnSkillLevelUp;

    UPROPERTY(BlueprintAssignable, Category = "Progression|Events")
    FOnTalentUnlocked OnTalentUnlocked;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Progression|Config")
    int32 MaxLevel = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Progression|Config")
    float ExperienceCurveMultiplier = 1.2f;  // Each level needs 20% more XP

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Progression|Config")
    int32 AttributePointsPerLevel = 5;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Progression|Config")
    int32 TalentPointsPerLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Progression|Config")
    TMap<FString, FTalentNode> TalentTree;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|State")
    int32 Level = 1;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|State")
    int32 Experience = 0;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|State")
    int32 ExperienceToNextLevel = 100;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|State")
    int32 AttributePoints = 0;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|State")
    int32 TalentPoints = 0;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|State")
    int32 PrestigeLevel = 0;

    // Attributes
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|Attributes")
    TMap<EAttributeType, int32> Attributes;

    // Skills (Use-based progression!)
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|Skills")
    TMap<ESkillType, FSkillData> Skills;

    // Unlocked Talents
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Progression|Talents")
    TArray<FString> UnlockedTalents;

private:
    // ========== HELPER FUNCTIONS ==========

    void LevelUp();
    void SkillLevelUp(ESkillType SkillType);
    void CalculateExperienceToNextLevel();
    void CalculateSkillExperienceToNextLevel(FSkillData& Skill);
    void InitializeSkills();
    void InitializeAttributes();
    bool CanUnlockTalent(const FString& TalentID) const;
};
