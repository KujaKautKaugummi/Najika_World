// ProgressionComponent.cpp
// Complete Progression System Implementation - Use-based Skills (Hard Rule #5!)

#include "ProgressionComponent.h"

UProgressionComponent::UProgressionComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UProgressionComponent::BeginPlay()
{
    Super::BeginPlay();

    InitializeAttributes();
    InitializeSkills();
}

// ========== EXPERIENCE & LEVEL ==========

void UProgressionComponent::AddExperience(int32 Amount)
{
    if (Amount <= 0 || Level >= MaxLevel) return;

    Experience += Amount;

    // Check for level up
    while (Experience >= ExperienceToNextLevel && Level < MaxLevel)
    {
        Experience -= ExperienceToNextLevel;
        LevelUp();
    }
}

float UProgressionComponent::GetExperiencePercent() const
{
    if (ExperienceToNextLevel == 0) return 1.0f;
    return (float)Experience / (float)ExperienceToNextLevel;
}

// ========== SKILLS (Use-based - Hard Rule #5!) ==========

void UProgressionComponent::AddSkillExperience(ESkillType SkillType, int32 Amount)
{
    if (!Skills.Contains(SkillType)) return;

    FSkillData& Skill = Skills[SkillType];
    Skill.Experience += Amount;

    // Check for skill level up
    while (Skill.Experience >= Skill.ExperienceToNextLevel)
    {
        Skill.Experience -= Skill.ExperienceToNextLevel;
        SkillLevelUp(SkillType);
    }
}

void UProgressionComponent::UseSkill(ESkillType SkillType)
{
    // Use-based progression (Hard Rule #5!)
    if (!Skills.Contains(SkillType)) return;

    FSkillData& Skill = Skills[SkillType];
    Skill.TotalUses++;

    // Award XP based on skill usage
    int32 SkillXP = 10 + (Skill.Level * 2); // Scales with skill level
    AddSkillExperience(SkillType, SkillXP);
}

FSkillData UProgressionComponent::GetSkillData(ESkillType SkillType) const
{
    if (Skills.Contains(SkillType))
    {
        return Skills[SkillType];
    }
    return FSkillData();
}

int32 UProgressionComponent::GetSkillLevel(ESkillType SkillType) const
{
    if (Skills.Contains(SkillType))
    {
        return Skills[SkillType].Level;
    }
    return 0;
}

TArray<FSkillData> UProgressionComponent::GetAllSkills() const
{
    TArray<FSkillData> AllSkills;
    for (const auto& Pair : Skills)
    {
        AllSkills.Add(Pair.Value);
    }
    return AllSkills;
}

// ========== ATTRIBUTES ==========

void UProgressionComponent::AddAttributePoint(EAttributeType Attribute)
{
    if (AttributePoints <= 0) return;
    if (!Attributes.Contains(Attribute)) return;

    Attributes[Attribute]++;
    AttributePoints--;
}

int32 UProgressionComponent::GetAttributeValue(EAttributeType Attribute) const
{
    if (Attributes.Contains(Attribute))
    {
        return Attributes[Attribute];
    }
    return 0;
}

// ========== TALENTS ==========

bool UProgressionComponent::UnlockTalent(const FString& TalentID)
{
    if (!CanUnlockTalent(TalentID)) return false;
    if (!TalentTree.Contains(TalentID)) return false;

    FTalentNode& Talent = TalentTree[TalentID];

    // Consume talent points
    if (TalentPoints < Talent.RequiredPoints) return false;
    TalentPoints -= Talent.RequiredPoints;

    // Unlock talent
    Talent.bIsUnlocked = true;
    Talent.CurrentRank = 1;
    UnlockedTalents.Add(TalentID);

    OnTalentUnlocked.Broadcast(TalentID);
    return true;
}

bool UProgressionComponent::UpgradeTalent(const FString& TalentID)
{
    if (!TalentTree.Contains(TalentID)) return false;
    if (!IsTalentUnlocked(TalentID)) return false;

    FTalentNode& Talent = TalentTree[TalentID];

    // Check if talent can be upgraded
    if (Talent.CurrentRank >= Talent.MaxRank) return false;
    if (TalentPoints < Talent.RequiredPoints) return false;

    // Upgrade talent
    TalentPoints -= Talent.RequiredPoints;
    Talent.CurrentRank++;

    return true;
}

bool UProgressionComponent::IsTalentUnlocked(const FString& TalentID) const
{
    return UnlockedTalents.Contains(TalentID);
}

int32 UProgressionComponent::GetTalentRank(const FString& TalentID) const
{
    if (TalentTree.Contains(TalentID))
    {
        return TalentTree[TalentID].CurrentRank;
    }
    return 0;
}

TArray<FTalentNode> UProgressionComponent::GetUnlockedTalents() const
{
    TArray<FTalentNode> Result;
    for (const FString& TalentID : UnlockedTalents)
    {
        if (TalentTree.Contains(TalentID))
        {
            Result.Add(TalentTree[TalentID]);
        }
    }
    return Result;
}

// ========== STAT BONUSES ==========

float UProgressionComponent::GetTotalStatBonus(const FString& StatName) const
{
    float TotalBonus = 1.0f; // Multiplicative

    for (const FString& TalentID : UnlockedTalents)
    {
        if (TalentTree.Contains(TalentID))
        {
            const FTalentNode& Talent = TalentTree[TalentID];
            const float* BonusValue = Talent.StatBonuses.Find(StatName);
            if (BonusValue)
            {
                TotalBonus *= (*BonusValue * Talent.CurrentRank);
            }
        }
    }

    return TotalBonus;
}

TMap<FString, float> UProgressionComponent::GetAllStatBonuses() const
{
    TMap<FString, float> AllBonuses;

    for (const FString& TalentID : UnlockedTalents)
    {
        if (TalentTree.Contains(TalentID))
        {
            const FTalentNode& Talent = TalentTree[TalentID];
            for (const auto& Pair : Talent.StatBonuses)
            {
                if (AllBonuses.Contains(Pair.Key))
                {
                    AllBonuses[Pair.Key] *= (Pair.Value * Talent.CurrentRank);
                }
                else
                {
                    AllBonuses.Add(Pair.Key, Pair.Value * Talent.CurrentRank);
                }
            }
        }
    }

    return AllBonuses;
}

// ========== PRESTIGE/RESET ==========

void UProgressionComponent::PrestigeReset()
{
    // Increment prestige level
    PrestigeLevel++;

    // Reset character level
    Level = 1;
    Experience = 0;
    CalculateExperienceToNextLevel();

    // Reset skills
    InitializeSkills();

    // Reset attributes but give bonus points
    InitializeAttributes();
    AttributePoints = PrestigeLevel * 10; // Bonus points for prestiging

    // Reset talents
    UnlockedTalents.Empty();
    TalentPoints = 0;

    // Reset talent tree
    for (auto& Pair : TalentTree)
    {
        Pair.Value.bIsUnlocked = false;
        Pair.Value.CurrentRank = 0;
    }
}

// ========== PRIVATE METHODS ==========

void UProgressionComponent::LevelUp()
{
    Level++;

    // Award attribute and talent points
    AttributePoints += AttributePointsPerLevel;
    TalentPoints += TalentPointsPerLevel;

    // Recalculate XP needed for next level
    CalculateExperienceToNextLevel();

    OnLevelUp.Broadcast(Level);
}

void UProgressionComponent::SkillLevelUp(ESkillType SkillType)
{
    if (!Skills.Contains(SkillType)) return;

    FSkillData& Skill = Skills[SkillType];
    Skill.Level++;

    CalculateSkillExperienceToNextLevel(Skill);

    OnSkillLevelUp.Broadcast(SkillType, Skill.Level);
}

void UProgressionComponent::CalculateExperienceToNextLevel()
{
    // Exponential curve
    ExperienceToNextLevel = FMath::FloorToInt(100.0f * FMath::Pow(ExperienceCurveMultiplier, Level - 1));
}

void UProgressionComponent::CalculateSkillExperienceToNextLevel(FSkillData& Skill)
{
    // Similar exponential curve for skills
    Skill.ExperienceToNextLevel = FMath::FloorToInt(100.0f * FMath::Pow(1.15f, Skill.Level - 1));
}

void UProgressionComponent::InitializeSkills()
{
    // Initialize all skills at level 1
    Skills.Empty();

    TArray<ESkillType> AllSkillTypes =
    {
        ESkillType::SK_OneHanded,
        ESkillType::SK_TwoHanded,
        ESkillType::SK_Archery,
        ESkillType::SK_Magic,
        ESkillType::SK_Explosion,
        ESkillType::SK_Defense,
        ESkillType::SK_Crafting,
        ESkillType::SK_Alchemy,
        ESkillType::SK_Stealth,
        ESkillType::SK_Survival
    };

    for (ESkillType SkillType : AllSkillTypes)
    {
        FSkillData NewSkill;
        NewSkill.SkillType = SkillType;
        NewSkill.Level = 1;
        NewSkill.Experience = 0;
        NewSkill.ExperienceToNextLevel = 100;
        NewSkill.TotalUses = 0;

        Skills.Add(SkillType, NewSkill);
    }
}

void UProgressionComponent::InitializeAttributes()
{
    // Initialize all attributes
    Attributes.Empty();

    Attributes.Add(EAttributeType::AT_Strength, 10);
    Attributes.Add(EAttributeType::AT_Dexterity, 10);
    Attributes.Add(EAttributeType::AT_Intelligence, 10);
    Attributes.Add(EAttributeType::AT_Vitality, 10);
    Attributes.Add(EAttributeType::AT_Luck, 10);
}

bool UProgressionComponent::CanUnlockTalent(const FString& TalentID) const
{
    if (!TalentTree.Contains(TalentID)) return false;
    if (IsTalentUnlocked(TalentID)) return false;

    const FTalentNode& Talent = TalentTree[TalentID];

    // Check level requirement
    if (Level < Talent.RequiredLevel) return false;

    // Check talent points
    if (TalentPoints < Talent.RequiredPoints) return false;

    // Check prerequisites
    for (const FString& PrereqID : Talent.Prerequisites)
    {
        if (!IsTalentUnlocked(PrereqID)) return false;
    }

    return true;
}
