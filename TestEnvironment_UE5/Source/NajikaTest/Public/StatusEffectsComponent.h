// StatusEffectsComponent.h
// Complete Status Effects System: Buffs, Debuffs, DoT, HoT, Stuns, etc.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "StatusEffectsComponent.generated.h"

// Status Effect Type
UENUM(BlueprintType)
enum class EStatusEffectType : uint8
{
    SE_Buff UMETA(DisplayName = "Buff"),
    SE_Debuff UMETA(DisplayName = "Debuff"),
    SE_DamageOverTime UMETA(DisplayName = "Damage Over Time"),
    SE_HealOverTime UMETA(DisplayName = "Heal Over Time"),
    SE_Stun UMETA(DisplayName = "Stun"),
    SE_Root UMETA(DisplayName = "Root"),
    SE_Slow UMETA(DisplayName = "Slow"),
    SE_Silence UMETA(DisplayName = "Silence"),
    SE_Blind UMETA(DisplayName = "Blind"),
    SE_Invulnerable UMETA(DisplayName = "Invulnerable")
};

// Status Effect
USTRUCT(BlueprintType)
struct FStatusEffect
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EffectID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EffectName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EStatusEffectType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Duration = 5.0f;

    UPROPERTY(BlueprintReadWrite)
    float TimeRemaining = 5.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float TickInterval = 1.0f;  // For DoT/HoT

    UPROPERTY(BlueprintReadWrite)
    float TimeSinceLastTick = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float TickDamage = 0.0f;  // Damage per tick (DoT)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float TickHeal = 0.0f;  // Heal per tick (HoT)

    // Stat Modifiers
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> StatModifiers;  // "Damage": 1.5 (50% increase), "Speed": 0.7 (30% decrease)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxStacks = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentStacks = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCanBeRemoved = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsPermanent = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(BlueprintReadWrite)
    AActor* Caster = nullptr;

    bool IsExpired() const { return !bIsPermanent && TimeRemaining <= 0.0f; }
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class NAJIKATEST_API UStatusEffectsComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UStatusEffectsComponent();

protected:
    virtual void BeginPlay() override;

public:
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    // ========== APPLY/REMOVE EFFECTS ==========

    UFUNCTION(BlueprintCallable, Category = "StatusEffects")
    void ApplyStatusEffect(const FStatusEffect& Effect);

    UFUNCTION(BlueprintCallable, Category = "StatusEffects")
    void RemoveStatusEffect(const FString& EffectID);

    UFUNCTION(BlueprintCallable, Category = "StatusEffects")
    void RemoveAllStatusEffects();

    UFUNCTION(BlueprintCallable, Category = "StatusEffects")
    void RemoveEffectsByType(EStatusEffectType Type);

    UFUNCTION(BlueprintCallable, Category = "StatusEffects")
    void ClearNegativeEffects();  // Remove all debuffs

    UFUNCTION(BlueprintCallable, Category = "StatusEffects")
    void ClearPositiveEffects();  // Remove all buffs

    // ========== QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "StatusEffects")
    bool HasStatusEffect(const FString& EffectID) const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects")
    bool HasEffectType(EStatusEffectType Type) const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects")
    FStatusEffect GetStatusEffect(const FString& EffectID) const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects")
    TArray<FStatusEffect> GetAllStatusEffects() const { return ActiveEffects; }

    UFUNCTION(BlueprintPure, Category = "StatusEffects")
    TArray<FStatusEffect> GetEffectsByType(EStatusEffectType Type) const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects")
    int32 GetEffectStacks(const FString& EffectID) const;

    // ========== SPECIAL CONDITIONS ==========

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool IsStunned() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool IsRooted() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool IsSlowed() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool IsSilenced() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool IsBlind() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool IsInvulnerable() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool CanMove() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool CanAttack() const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Conditions")
    bool CanCast() const;

    // ========== STAT MODIFIERS ==========

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Stats")
    float GetStatModifier(const FString& StatName) const;

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Stats")
    TMap<FString, float> GetAllStatModifiers() const;

    // ========== IMMUNITY ==========

    UFUNCTION(BlueprintCallable, Category = "StatusEffects|Immunity")
    void AddImmunity(EStatusEffectType Type);

    UFUNCTION(BlueprintCallable, Category = "StatusEffects|Immunity")
    void RemoveImmunity(EStatusEffectType Type);

    UFUNCTION(BlueprintPure, Category = "StatusEffects|Immunity")
    bool IsImmuneToEffect(EStatusEffectType Type) const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnStatusEffectApplied, FStatusEffect, Effect);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnStatusEffectRemoved, FString, EffectID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnStatusEffectTick, FString, EffectID, float, Value);

    UPROPERTY(BlueprintAssignable, Category = "StatusEffects|Events")
    FOnStatusEffectApplied OnStatusEffectApplied;

    UPROPERTY(BlueprintAssignable, Category = "StatusEffects|Events")
    FOnStatusEffectRemoved OnStatusEffectRemoved;

    UPROPERTY(BlueprintAssignable, Category = "StatusEffects|Events")
    FOnStatusEffectTick OnStatusEffectTick;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "StatusEffects|Config")
    int32 MaxSimultaneousEffects = 20;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "StatusEffects|Config")
    bool bStackSameName = true;  // Allow stacking same effect

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "StatusEffects|Config")
    bool bRefreshDuration = true;  // Refresh duration when same effect applied

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "StatusEffects|State")
    TArray<FStatusEffect> ActiveEffects;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "StatusEffects|State")
    TArray<EStatusEffectType> Immunities;

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateEffects(float DeltaTime);
    void ProcessEffectTick(FStatusEffect& Effect, float DeltaTime);
    void RemoveExpiredEffects();
    FStatusEffect* FindEffect(const FString& EffectID);
    bool CanApplyEffect(const FStatusEffect& Effect) const;
    void StackEffect(FStatusEffect& ExistingEffect, const FStatusEffect& NewEffect);
};
