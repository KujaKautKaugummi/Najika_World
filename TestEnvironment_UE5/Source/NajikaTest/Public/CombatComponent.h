// CombatComponent.h
// Complete Combat System: Damage, Hit Detection, Combos, Parry, Critical Hits

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "CombatComponent.generated.h"

// Damage Type
UENUM(BlueprintType)
enum class EDamageType : uint8
{
    DT_Physical UMETA(DisplayName = "Physical"),
    DT_Magical UMETA(DisplayName = "Magical"),
    DT_Fire UMETA(DisplayName = "Fire"),
    DT_Ice UMETA(DisplayName = "Ice"),
    DT_Lightning UMETA(DisplayName = "Lightning"),
    DT_Poison UMETA(DisplayName = "Poison"),
    DT_True UMETA(DisplayName = "True Damage")  // Ignores defense
};

// Hit Result Info
USTRUCT(BlueprintType)
struct FHitInfo
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    float Damage = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    EDamageType DamageType = EDamageType::DT_Physical;

    UPROPERTY(BlueprintReadWrite)
    bool bIsCritical = false;

    UPROPERTY(BlueprintReadWrite)
    bool bIsBlocked = false;

    UPROPERTY(BlueprintReadWrite)
    bool bIsParried = false;

    UPROPERTY(BlueprintReadWrite)
    AActor* Attacker = nullptr;

    UPROPERTY(BlueprintReadWrite)
    AActor* Victim = nullptr;

    UPROPERTY(BlueprintReadWrite)
    FVector HitLocation = FVector::ZeroVector;
};

// Combo Attack Data
USTRUCT(BlueprintType)
struct FComboAttack
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 ComboIndex = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Damage = 50.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DamageMultiplier = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float AttackSpeed = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ComboWindow = 0.5f;  // Time to continue combo

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AnimationName;
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class NAJIKATEST_API UCombatComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UCombatComponent();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    // ========== ATTACK ==========

    UFUNCTION(BlueprintCallable, Category = "Combat|Attack")
    void Attack();

    UFUNCTION(BlueprintCallable, Category = "Combat|Attack")
    void HeavyAttack();

    UFUNCTION(BlueprintCallable, Category = "Combat|Attack")
    void ChargedAttack(float ChargeAmount);

    UFUNCTION(BlueprintPure, Category = "Combat|Attack")
    bool CanAttack() const;

    UFUNCTION(BlueprintPure, Category = "Combat|Attack")
    bool IsAttacking() const { return bIsAttacking; }

    // ========== COMBO SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "Combat|Combo")
    void ContinueCombo();

    UFUNCTION(BlueprintCallable, Category = "Combat|Combo")
    void ResetCombo();

    UFUNCTION(BlueprintPure, Category = "Combat|Combo")
    int32 GetCurrentComboCount() const { return CurrentComboCount; }

    UFUNCTION(BlueprintPure, Category = "Combat|Combo")
    bool IsInCombo() const { return CurrentComboCount > 0; }

    // ========== DEFENSE ==========

    UFUNCTION(BlueprintCallable, Category = "Combat|Defense")
    void StartBlock();

    UFUNCTION(BlueprintCallable, Category = "Combat|Defense")
    void StopBlock();

    UFUNCTION(BlueprintPure, Category = "Combat|Defense")
    bool IsBlocking() const { return bIsBlocking; }

    UFUNCTION(BlueprintCallable, Category = "Combat|Defense")
    void Parry();

    UFUNCTION(BlueprintPure, Category = "Combat|Defense")
    bool CanParry() const;

    UFUNCTION(BlueprintCallable, Category = "Combat|Defense")
    void Dodge(FVector Direction);

    UFUNCTION(BlueprintPure, Category = "Combat|Defense")
    bool CanDodge() const;

    // ========== DAMAGE CALCULATION ==========

    UFUNCTION(BlueprintCallable, Category = "Combat|Damage")
    FHitInfo CalculateDamage(float BaseDamage, EDamageType DamageType, AActor* Target);

    UFUNCTION(BlueprintCallable, Category = "Combat|Damage")
    void ApplyDamage(AActor* Target, const FHitInfo& HitInfo);

    UFUNCTION(BlueprintPure, Category = "Combat|Damage")
    float GetCriticalChance() const { return CriticalChance; }

    UFUNCTION(BlueprintPure, Category = "Combat|Damage")
    float GetCriticalMultiplier() const { return CriticalMultiplier; }

    // ========== HIT DETECTION ==========

    UFUNCTION(BlueprintCallable, Category = "Combat|HitDetection")
    TArray<AActor*> SweepForEnemies(float Radius, float Angle);

    UFUNCTION(BlueprintCallable, Category = "Combat|HitDetection")
    bool CheckHit(AActor* Target, const FVector& HitLocation);

    // ========== LOCK-ON TARGET ==========

    UFUNCTION(BlueprintCallable, Category = "Combat|LockOn")
    void LockOnTarget(AActor* Target);

    UFUNCTION(BlueprintCallable, Category = "Combat|LockOn")
    void ClearLockOnTarget();

    UFUNCTION(BlueprintPure, Category = "Combat|LockOn")
    AActor* GetLockOnTarget() const { return LockOnTarget; }

    UFUNCTION(BlueprintPure, Category = "Combat|LockOn")
    bool HasLockOnTarget() const { return LockOnTarget != nullptr; }

    // ========== STATS ==========

    UFUNCTION(BlueprintPure, Category = "Combat|Stats")
    float GetAttackPower() const { return AttackPower; }

    UFUNCTION(BlueprintCallable, Category = "Combat|Stats")
    void SetAttackPower(float NewValue) { AttackPower = NewValue; }

    UFUNCTION(BlueprintPure, Category = "Combat|Stats")
    float GetDefense() const { return Defense; }

    UFUNCTION(BlueprintCallable, Category = "Combat|Stats")
    void SetDefense(float NewValue) { Defense = NewValue; }

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAttackPerformed, int32, ComboIndex);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDamageDealt, FHitInfo, HitInfo);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnParrySuccess);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnComboReset);

    UPROPERTY(BlueprintAssignable, Category = "Combat|Events")
    FOnAttackPerformed OnAttackPerformed;

    UPROPERTY(BlueprintAssignable, Category = "Combat|Events")
    FOnDamageDealt OnDamageDealt;

    UPROPERTY(BlueprintAssignable, Category = "Combat|Events")
    FOnParrySuccess OnParrySuccess;

    UPROPERTY(BlueprintAssignable, Category = "Combat|Events")
    FOnComboReset OnComboReset;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float AttackPower = 50.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float Defense = 20.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float CriticalChance = 0.10f;  // 10%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float CriticalMultiplier = 2.0f;  // 2x damage

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float BlockReduction = 0.5f;  // 50% damage reduction when blocking

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float ParryWindow = 0.3f;  // 300ms perfect parry window

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float AttackCooldown = 0.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    float DodgeCooldown = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Config")
    TArray<FComboAttack> ComboChain;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    bool bIsAttacking = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    bool bIsBlocking = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    bool bCanParry = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    int32 CurrentComboCount = 0;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    float ComboTimer = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    float LastAttackTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    float LastDodgeTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat|State")
    AActor* LockOnTarget = nullptr;

    // PvE/PvP Scaling (Hard Rule #4!)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|PvP")
    float PvPDamageMultiplier = 0.5f;  // 50% damage in PvP

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|PvP")
    bool bIsPvPEnabled = false;

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateComboTimer(float DeltaTime);
    bool RollCritical() const;
    float CalculateDamageReduction(AActor* Target, EDamageType DamageType) const;
    void PerformAttackTrace();
};
