// MountSystem.h
// Complete Mount/Riding System with speeds, stamina, abilities, customization

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MountSystem.generated.h"

// Mount Type
UENUM(BlueprintType)
enum class EMountType : uint8
{
    MT_Ground UMETA(DisplayName = "Ground Mount"),
    MT_Flying UMETA(DisplayName = "Flying Mount"),
    MT_Aquatic UMETA(DisplayName = "Aquatic Mount"),
    MT_Amphibious UMETA(DisplayName = "Amphibious (Land+Water)"),
    MT_Special UMETA(DisplayName = "Special (Can do all)")
};

// Mount Rarity
UENUM(BlueprintType)
enum class EMountRarity : uint8
{
    MR_Common UMETA(DisplayName = "Common"),
    MR_Uncommon UMETA(DisplayName = "Uncommon"),
    MR_Rare UMETA(DisplayName = "Rare"),
    MR_Epic UMETA(DisplayName = "Epic"),
    MR_Legendary UMETA(DisplayName = "Legendary")
};

// Mount State
UENUM(BlueprintType)
enum class EMountState : uint8
{
    MS_Idle UMETA(DisplayName = "Idle"),
    MS_Walking UMETA(DisplayName = "Walking"),
    MS_Running UMETA(DisplayName = "Running"),
    MS_Sprinting UMETA(DisplayName = "Sprinting"),
    MS_Flying UMETA(DisplayName = "Flying"),
    MS_Swimming UMETA(DisplayName = "Swimming"),
    MS_Jumping UMETA(DisplayName = "Jumping"),
    MS_Dismounted UMETA(DisplayName = "Dismounted")
};

// Mount Ability
USTRUCT(BlueprintType)
struct FMountAbility
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AbilityID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AbilityName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Cooldown = 30.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float StaminaCost = 20.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SpeedBoost = 1.5f;  // Multiplier

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Duration = 10.0f;

    UPROPERTY(BlueprintReadWrite)
    float LastUsedTime = 0.0f;

    bool IsOnCooldown(float CurrentTime) const { return (CurrentTime - LastUsedTime) < Cooldown; }
};

// Mount Stats
USTRUCT(BlueprintType)
struct FMountStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float BaseSpeed = 600.0f;  // 6 m/s

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SprintSpeed = 1200.0f;  // 12 m/s

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Stamina = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MaxStamina = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float StaminaRegen = 10.0f;  // Per second

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float StaminaDrainRate = 5.0f;  // Per second when sprinting

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float JumpHeight = 300.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float CarryCapacity = 100.0f;  // Extra inventory weight

    float GetStaminaPercent() const { return MaxStamina > 0.0f ? Stamina / MaxStamina : 0.0f; }
    bool CanSprint() const { return Stamina > 20.0f; }
};

// Mount Customization
USTRUCT(BlueprintType)
struct FMountCustomization
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FLinearColor PrimaryColor = FLinearColor::White;

    UPROPERTY(BlueprintReadWrite)
    FLinearColor SecondaryColor = FLinearColor::White;

    UPROPERTY(BlueprintReadWrite)
    FString SaddleID;

    UPROPERTY(BlueprintReadWrite)
    FString ArmorID;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> AccessoryIDs;  // Banners, ribbons, etc.
};

// Mount Data
USTRUCT(BlueprintType)
struct FMountData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString MountID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString MountName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EMountType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EMountRarity Rarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSubclassOf<APawn> MountClass;  // 3D model/blueprint

    UPROPERTY(BlueprintReadWrite)
    FMountStats Stats;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FMountAbility> Abilities;

    UPROPERTY(BlueprintReadWrite)
    FMountCustomization Customization;

    UPROPERTY(BlueprintReadWrite)
    bool bIsOwned = false;

    UPROPERTY(BlueprintReadWrite)
    bool bIsActive = false;

    UPROPERTY(BlueprintReadWrite)
    FDateTime UnlockedDate;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RequiredQuestID;  // Unlock via quest

    bool CanFly() const { return Type == EMountType::MT_Flying || Type == EMountType::MT_Special; }
    bool CanSwim() const { return Type == EMountType::MT_Aquatic || Type == EMountType::MT_Amphibious || Type == EMountType::MT_Special; }
};

UCLASS()
class NAJIKATEST_API AMountSystem : public ACharacter
{
    GENERATED_BODY()

public:
    AMountSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== MOUNT/DISMOUNT ==========

    UFUNCTION(BlueprintCallable, Category = "Mount|Control")
    void MountUp(const FString& MountID, AActor* Rider);

    UFUNCTION(BlueprintCallable, Category = "Mount|Control")
    void Dismount();

    UFUNCTION(BlueprintPure, Category = "Mount|Control")
    bool IsMounted() const { return bIsMounted; }

    UFUNCTION(BlueprintPure, Category = "Mount|Control")
    FMountData GetCurrentMount() const { return CurrentMountData; }

    // ========== MOVEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Mount|Movement")
    void StartSprint();

    UFUNCTION(BlueprintCallable, Category = "Mount|Movement")
    void StopSprint();

    UFUNCTION(BlueprintCallable, Category = "Mount|Movement")
    void StartFlying();

    UFUNCTION(BlueprintCallable, Category = "Mount|Movement")
    void StopFlying();

    UFUNCTION(BlueprintPure, Category = "Mount|Movement")
    bool CanFly() const { return CurrentMountData.CanFly(); }

    UFUNCTION(BlueprintPure, Category = "Mount|Movement")
    bool IsSprinting() const { return bIsSprinting; }

    UFUNCTION(BlueprintPure, Category = "Mount|Movement")
    bool IsFlying() const { return CurrentState == EMountState::MS_Flying; }

    // ========== STAMINA ==========

    UFUNCTION(BlueprintPure, Category = "Mount|Stamina")
    float GetStamina() const { return CurrentMountData.Stats.Stamina; }

    UFUNCTION(BlueprintPure, Category = "Mount|Stamina")
    float GetMaxStamina() const { return CurrentMountData.Stats.MaxStamina; }

    UFUNCTION(BlueprintPure, Category = "Mount|Stamina")
    float GetStaminaPercent() const { return CurrentMountData.Stats.GetStaminaPercent(); }

    UFUNCTION(BlueprintCallable, Category = "Mount|Stamina")
    void RegenerateStamina(float Amount);

    UFUNCTION(BlueprintCallable, Category = "Mount|Stamina")
    void DrainStamina(float Amount);

    // ========== ABILITIES ==========

    UFUNCTION(BlueprintCallable, Category = "Mount|Abilities")
    void UseAbility(int32 AbilityIndex);

    UFUNCTION(BlueprintPure, Category = "Mount|Abilities")
    TArray<FMountAbility> GetAbilities() const { return CurrentMountData.Abilities; }

    UFUNCTION(BlueprintPure, Category = "Mount|Abilities")
    bool CanUseAbility(int32 AbilityIndex) const;

    // ========== MOUNT COLLECTION ==========

    UFUNCTION(BlueprintCallable, Category = "Mount|Collection")
    void UnlockMount(const FString& MountID);

    UFUNCTION(BlueprintPure, Category = "Mount|Collection")
    bool IsMountOwned(const FString& MountID) const;

    UFUNCTION(BlueprintPure, Category = "Mount|Collection")
    TArray<FMountData> GetOwnedMounts() const;

    UFUNCTION(BlueprintPure, Category = "Mount|Collection")
    int32 GetMountCount() const;

    // ========== CUSTOMIZATION ==========

    UFUNCTION(BlueprintCallable, Category = "Mount|Customization")
    void SetMountColor(const FString& MountID, FLinearColor PrimaryColor, FLinearColor SecondaryColor);

    UFUNCTION(BlueprintCallable, Category = "Mount|Customization")
    void EquipSaddle(const FString& MountID, const FString& SaddleID);

    UFUNCTION(BlueprintCallable, Category = "Mount|Customization")
    void EquipArmor(const FString& MountID, const FString& ArmorID);

    UFUNCTION(BlueprintCallable, Category = "Mount|Customization")
    void AddAccessory(const FString& MountID, const FString& AccessoryID);

    UFUNCTION(BlueprintPure, Category = "Mount|Customization")
    FMountCustomization GetCustomization(const FString& MountID) const;

    // ========== MOUNT STATS ==========

    UFUNCTION(BlueprintPure, Category = "Mount|Stats")
    float GetCurrentSpeed() const;

    UFUNCTION(BlueprintPure, Category = "Mount|Stats")
    float GetCarryCapacity() const { return CurrentMountData.Stats.CarryCapacity; }

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMountSummoned, FString, MountID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMountDismissed, FString, MountID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMountUnlocked, FString, MountID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAbilityUsed, FString, MountID, FString, AbilityID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnStaminaDepleted, FString, MountID);

    UPROPERTY(BlueprintAssignable, Category = "Mount|Events")
    FOnMountSummoned OnMountSummoned;

    UPROPERTY(BlueprintAssignable, Category = "Mount|Events")
    FOnMountDismissed OnMountDismissed;

    UPROPERTY(BlueprintAssignable, Category = "Mount|Events")
    FOnMountUnlocked OnMountUnlocked;

    UPROPERTY(BlueprintAssignable, Category = "Mount|Events")
    FOnAbilityUsed OnAbilityUsed;

    UPROPERTY(BlueprintAssignable, Category = "Mount|Events")
    FOnStaminaDepleted OnStaminaDepleted;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mount|Config")
    TMap<FString, FMountData> AvailableMounts;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mount|Config")
    float MountSummonTime = 2.0f;  // Casting time

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mount|Config")
    bool bCanMountInCombat = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mount|Config")
    bool bDismountOnDamage = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mount|Config")
    float DismountDamageThreshold = 10.0f;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mount|State")
    bool bIsMounted = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mount|State")
    bool bIsSprinting = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mount|State")
    EMountState CurrentState = EMountState::MS_Dismounted;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mount|State")
    FMountData CurrentMountData;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mount|State")
    AActor* RiderActor = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mount|State")
    TMap<FString, FMountData> OwnedMounts;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mount|State")
    float ActiveAbilityEndTime = 0.0f;

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateStamina(float DeltaTime);
    void UpdateMovementSpeed();
    void ApplyAbilityEffects(const FMountAbility& Ability);
    void CheckDismountConditions(float DeltaTime);
    bool CanMountNow() const;
};
