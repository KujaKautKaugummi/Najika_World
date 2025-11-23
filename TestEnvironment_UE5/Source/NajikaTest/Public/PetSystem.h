// PetSystem.h
// Complete Pet/Companion System with leveling, abilities, loyalty, behaviors

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "PetSystem.generated.h"

// Pet Type
UENUM(BlueprintType)
enum class EPetType : uint8
{
    PT_Combat UMETA(DisplayName = "Combat"),
    PT_Gathering UMETA(DisplayName = "Gathering"),
    PT_Support UMETA(DisplayName = "Support/Healer"),
    PT_Tank UMETA(DisplayName = "Tank"),
    PT_Companion UMETA(DisplayName = "Companion (Cosmetic)")
};

// Pet Behavior
UENUM(BlueprintType)
enum class EPetBehavior : uint8
{
    PB_Passive UMETA(DisplayName = "Passive (Don't Attack)"),
    PB_Defensive UMETA(DisplayName = "Defensive (Attack if Attacked)"),
    PB_Aggressive UMETA(DisplayName = "Aggressive (Attack on Sight)"),
    PB_Assist UMETA(DisplayName = "Assist (Attack Owner's Target)")
};

// Pet State
UENUM(BlueprintType)
enum class EPetState : uint8
{
    PS_Following UMETA(DisplayName = "Following"),
    PS_Staying UMETA(DisplayName = "Staying"),
    PS_Attacking UMETA(DisplayName = "Attacking"),
    PS_Gathering UMETA(DisplayName = "Gathering"),
    PS_Returning UMETA(DisplayName = "Returning"),
    PS_Dismissed UMETA(DisplayName = "Dismissed")
};

// Pet Rarity
UENUM(BlueprintType)
enum class EPetRarity : uint8
{
    PR_Common UMETA(DisplayName = "Common"),
    PR_Uncommon UMETA(DisplayName = "Uncommon"),
    PR_Rare UMETA(DisplayName = "Rare"),
    PR_Epic UMETA(DisplayName = "Epic"),
    PR_Legendary UMETA(DisplayName = "Legendary"),
    PR_Mythic UMETA(DisplayName = "Mythic")
};

// Pet Ability
USTRUCT(BlueprintType)
struct FPetAbility
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AbilityID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AbilityName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Cooldown = 10.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Damage = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float HealAmount = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> Buffs;  // "Damage": 1.2 (20% increase)

    UPROPERTY(BlueprintReadWrite)
    float LastUsedTime = 0.0f;

    bool IsOnCooldown(float CurrentTime) const { return (CurrentTime - LastUsedTime) < Cooldown; }
};

// Pet Stats
USTRUCT(BlueprintType)
struct FPetStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Health = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MaxHealth = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Damage = 10.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Defense = 5.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Speed = 400.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float AttackSpeed = 1.0f;  // Attacks per second

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float GatherSpeed = 1.0f;  // Gathering multiplier

    float GetHealthPercent() const { return MaxHealth > 0.0f ? Health / MaxHealth : 0.0f; }
};

// Pet Data
USTRUCT(BlueprintType)
struct FPetData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString PetID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString PetName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EPetType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EPetRarity Rarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSubclassOf<APawn> PetClass;  // 3D model/blueprint

    UPROPERTY(BlueprintReadWrite)
    int32 Level = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 Experience = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 Loyalty = 50;  // 0-100

    UPROPERTY(BlueprintReadWrite)
    FPetStats Stats;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FPetAbility> Abilities;

    UPROPERTY(BlueprintReadWrite)
    EPetBehavior Behavior = EPetBehavior::PB_Defensive;

    UPROPERTY(BlueprintReadWrite)
    EPetState State = EPetState::PS_Dismissed;

    UPROPERTY(BlueprintReadWrite)
    FDateTime LastFed;

    UPROPERTY(BlueprintReadWrite)
    bool bIsHungry = false;

    UPROPERTY(BlueprintReadWrite)
    bool bIsSummoned = false;

    int32 GetXPForNextLevel() const { return Level * 100; }
    float GetXPPercent() const { return (float)Experience / (float)GetXPForNextLevel(); }
};

UCLASS()
class NAJIKATEST_API APetSystem : public ACharacter
{
    GENERATED_BODY()

public:
    APetSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== PET MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Pet|Management")
    void SummonPet(const FString& PetID, AActor* Owner);

    UFUNCTION(BlueprintCallable, Category = "Pet|Management")
    void DismissPet();

    UFUNCTION(BlueprintCallable, Category = "Pet|Management")
    void TamePet(const FString& PetSpeciesID, AActor* Tamer);

    UFUNCTION(BlueprintCallable, Category = "Pet|Management")
    void ReleasePet(const FString& PetID);

    UFUNCTION(BlueprintPure, Category = "Pet|Management")
    bool IsSummoned() const { return PetData.bIsSummoned; }

    // ========== PET COMMANDS ==========

    UFUNCTION(BlueprintCallable, Category = "Pet|Commands")
    void CommandFollow();

    UFUNCTION(BlueprintCallable, Category = "Pet|Commands")
    void CommandStay();

    UFUNCTION(BlueprintCallable, Category = "Pet|Commands")
    void CommandAttack(AActor* Target);

    UFUNCTION(BlueprintCallable, Category = "Pet|Commands")
    void CommandReturn();

    UFUNCTION(BlueprintCallable, Category = "Pet|Commands")
    void CommandGather(AActor* Resource);

    UFUNCTION(BlueprintCallable, Category = "Pet|Commands")
    void SetBehavior(EPetBehavior NewBehavior);

    // ========== PET STATS ==========

    UFUNCTION(BlueprintPure, Category = "Pet|Stats")
    FPetData GetPetData() const { return PetData; }

    UFUNCTION(BlueprintPure, Category = "Pet|Stats")
    int32 GetLevel() const { return PetData.Level; }

    UFUNCTION(BlueprintPure, Category = "Pet|Stats")
    int32 GetLoyalty() const { return PetData.Loyalty; }

    UFUNCTION(BlueprintCallable, Category = "Pet|Stats")
    void HealPet(float Amount);

    UFUNCTION(BlueprintCallable, Category = "Pet|Stats")
    void DamagePet(float Amount);

    // ========== PROGRESSION ==========

    UFUNCTION(BlueprintCallable, Category = "Pet|Progression")
    void AddExperience(int32 XP);

    UFUNCTION(BlueprintCallable, Category = "Pet|Progression")
    void LevelUp();

    UFUNCTION(BlueprintPure, Category = "Pet|Progression")
    int32 GetExperience() const { return PetData.Experience; }

    UFUNCTION(BlueprintPure, Category = "Pet|Progression")
    int32 GetXPForNextLevel() const { return PetData.GetXPForNextLevel(); }

    // ========== LOYALTY SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "Pet|Loyalty")
    void AddLoyalty(int32 Amount);

    UFUNCTION(BlueprintCallable, Category = "Pet|Loyalty")
    void FeedPet(const FString& FoodItemID);

    UFUNCTION(BlueprintPure, Category = "Pet|Loyalty")
    bool IsHungry() const { return PetData.bIsHungry; }

    UFUNCTION(BlueprintPure, Category = "Pet|Loyalty")
    float GetTimeSinceLastFed() const;

    // ========== ABILITIES ==========

    UFUNCTION(BlueprintCallable, Category = "Pet|Abilities")
    void UseAbility(int32 AbilityIndex);

    UFUNCTION(BlueprintPure, Category = "Pet|Abilities")
    TArray<FPetAbility> GetAvailableAbilities() const;

    UFUNCTION(BlueprintPure, Category = "Pet|Abilities")
    bool CanUseAbility(int32 AbilityIndex) const;

    // ========== AI BEHAVIOR ==========

    UFUNCTION(BlueprintCallable, Category = "Pet|AI")
    void UpdatePetBehavior(float DeltaTime);

    UFUNCTION(BlueprintCallable, Category = "Pet|AI")
    void FindAndAttackNearestEnemy();

    UFUNCTION(BlueprintPure, Category = "Pet|AI")
    AActor* GetOwner() const { return OwnerActor; }

    UFUNCTION(BlueprintPure, Category = "Pet|AI")
    AActor* GetCurrentTarget() const { return CurrentTarget; }

    // ========== INVENTORY INTEGRATION ==========

    UFUNCTION(BlueprintCallable, Category = "Pet|Inventory")
    void DepositGatheredItems();

    UFUNCTION(BlueprintPure, Category = "Pet|Inventory")
    TArray<FString> GetGatheredItems() const { return GatheredItems; }

    UFUNCTION(BlueprintCallable, Category = "Pet|Inventory")
    void ClearGatheredItems();

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPetSummoned, FString, PetID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPetDismissed, FString, PetID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPetLevelUp, FString, PetID, int32, NewLevel);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPetLoyaltyChanged, FString, PetID, int32, NewLoyalty);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPetDeath, FString, PetID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAbilityUsed, FString, PetID, FString, AbilityID);

    UPROPERTY(BlueprintAssignable, Category = "Pet|Events")
    FOnPetSummoned OnPetSummoned;

    UPROPERTY(BlueprintAssignable, Category = "Pet|Events")
    FOnPetDismissed OnPetDismissed;

    UPROPERTY(BlueprintAssignable, Category = "Pet|Events")
    FOnPetLevelUp OnPetLevelUp;

    UPROPERTY(BlueprintAssignable, Category = "Pet|Events")
    FOnPetLoyaltyChanged OnPetLoyaltyChanged;

    UPROPERTY(BlueprintAssignable, Category = "Pet|Events")
    FOnPetDeath OnPetDeath;

    UPROPERTY(BlueprintAssignable, Category = "Pet|Events")
    FOnAbilityUsed OnAbilityUsed;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pet|Config")
    float FollowDistance = 200.0f;  // 2 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pet|Config")
    float AggroRange = 1000.0f;  // 10 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pet|Config")
    float AttackRange = 150.0f;  // 1.5 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pet|Config")
    float HungerInterval = 3600.0f;  // 1 hour

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pet|Config")
    int32 LoyaltyDecayPerHour = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pet|Config")
    int32 FeedLoyaltyGain = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Pet|Config")
    float StatsPerLevel = 10.0f;  // Each level = +10 to all stats

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pet|State")
    FPetData PetData;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pet|State")
    AActor* OwnerActor = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pet|State")
    AActor* CurrentTarget = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pet|State")
    FVector StayLocation = FVector::ZeroVector;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pet|State")
    TArray<FString> GatheredItems;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Pet|State")
    float TimeSinceLastFeed = 0.0f;

private:
    // ========== HELPER FUNCTIONS ==========

    void FollowOwner(float DeltaTime);
    void AttackTarget(float DeltaTime);
    void UpdateHunger(float DeltaTime);
    void UpdateLoyaltyDecay(float DeltaTime);
    void ApplyLevelUpBonuses();
    bool IsInRange(AActor* Target, float Range) const;
};
