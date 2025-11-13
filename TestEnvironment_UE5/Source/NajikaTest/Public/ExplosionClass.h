// ExplosionClass.h
// Model 2 Prototype - Explosion as STANDALONE CLASS (NEVER mixed with other elements)
// Hard Rule #3: Explosion ≠ Weave – Explosion ist EIGENE KLASSE
// Trade-off: +30-40% Explosion talents, -15-20% on all other talent trees

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ExplosionClass.generated.h"

// Explosion variant types - Section 2.2
UENUM(BlueprintType)
enum class EExplosionVariant : uint8
{
    EV_Gross UMETA(DisplayName = "Große Explosion"),      // Huge AoE, long exhaustion
    EV_Vierfach UMETA(DisplayName = "4-fach Explosion"),  // 4x serial, smaller radius
    EV_Mini UMETA(DisplayName = "Mini-Explosion")         // Spam-capable, setup for finisher
};

// Exhaustion state - core mechanic for Explosion class
USTRUCT(BlueprintType)
struct FExhaustionState
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    bool bIsExhausted = false;

    UPROPERTY(BlueprintReadOnly)
    float ExhaustionDuration = 0.0f;

    UPROPERTY(BlueprintReadOnly)
    float RegenerationPenalty = 0.0f;  // -50% during Omega-Explosion
};

// Talent progression for Explosion class
USTRUCT(BlueprintType)
struct FExplosionTalents
{
    GENERATED_BODY()

    // Explosion-specific talents (+30-40% bonus)
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ExplosionDamageBonus = 1.35f;  // 35% bonus (within 30-40% range)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ExplosionRadiusBonus = 1.35f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ExplosionChargeSpeedBonus = 1.35f;

    // Other talent trees (-15-20% penalty)
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MeleeEffectiveness = 0.825f;  // 17.5% reduction

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float RangedEffectiveness = 0.825f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MagicEffectiveness = 0.825f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DefenseEffectiveness = 0.825f;
};

UCLASS()
class NAJIKATEST_API AExplosionClass : public ACharacter
{
    GENERATED_BODY()

public:
    AExplosionClass();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    // ========== CORE EXPLOSION ABILITIES ==========

    // Große Explosion - Massive AoE with long exhaustion
    UFUNCTION(BlueprintCallable, Category = "Explosion|Abilities")
    void CastGrosseExplosion();

    // 4-fach Explosion - Four serial explosions with smaller radius
    UFUNCTION(BlueprintCallable, Category = "Explosion|Abilities")
    void CastVierfachExplosion();

    // Mini-Explosion - Spam-capable, setup move for combos
    UFUNCTION(BlueprintCallable, Category = "Explosion|Abilities")
    void CastMiniExplosion();

    // Omega-Explosion - Ultimate (600% AoE, 30s -50% Regen)
    UFUNCTION(BlueprintCallable, Category = "Explosion|Ultimate")
    void CastOmegaExplosion();

    // ========== CHARGING SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "Explosion|Charge")
    void StartCharging();

    UFUNCTION(BlueprintCallable, Category = "Explosion|Charge")
    void StopCharging();

    UFUNCTION(BlueprintCallable, Category = "Explosion|Charge")
    void ReleaseExplosion();

    // ========== EXHAUSTION SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "Explosion|Exhaustion")
    void ApplyExhaustion(float Duration, float RegenPenalty);

    UFUNCTION(BlueprintPure, Category = "Explosion|Exhaustion")
    bool IsExhausted() const { return ExhaustionState.bIsExhausted; }

    UFUNCTION(BlueprintPure, Category = "Explosion|Exhaustion")
    float GetExhaustionTimeRemaining() const { return ExhaustionState.ExhaustionDuration; }

    // ========== TALENT SYSTEM ==========

    UFUNCTION(BlueprintPure, Category = "Explosion|Talents")
    float GetExplosionDamageMultiplier() const;

    UFUNCTION(BlueprintPure, Category = "Explosion|Talents")
    float GetExplosionRadiusMultiplier() const;

    UFUNCTION(BlueprintCallable, Category = "Explosion|Talents")
    void UpgradeTalent(const FString& TalentName, float Amount);

protected:
    // ========== PROPERTIES ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Explosion|Config")
    EExplosionVariant CurrentVariant = EExplosionVariant::EV_Gross;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Explosion|Config")
    FExplosionTalents Talents;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Explosion|State")
    FExhaustionState ExhaustionState;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Explosion|Charge")
    float ChargeProgress = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Explosion|Charge")
    bool bIsCharging = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Explosion|Charge")
    float ChargeRate = 1.0f;  // Modified by talents

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Explosion|Charge")
    float MaxCharge = 100.0f;

    // Explosion variant parameters
    UPROPERTY(EditAnywhere, Category = "Explosion|GroßeExplosion")
    float GrossExplosionRadius = 1000.0f;  // 10 meters

    UPROPERTY(EditAnywhere, Category = "Explosion|GroßeExplosion")
    float GrossExplosionDamage = 500.0f;

    UPROPERTY(EditAnywhere, Category = "Explosion|GroßeExplosion")
    float GrossExplosionExhaustion = 8.0f;  // 8 seconds

    UPROPERTY(EditAnywhere, Category = "Explosion|VierfachExplosion")
    float VierfachExplosionRadius = 400.0f;  // 4 meters each

    UPROPERTY(EditAnywhere, Category = "Explosion|VierfachExplosion")
    float VierfachExplosionDamage = 150.0f;  // Per explosion

    UPROPERTY(EditAnywhere, Category = "Explosion|VierfachExplosion")
    float VierfachExplosionDelay = 0.25f;  // Between explosions

    UPROPERTY(EditAnywhere, Category = "Explosion|MiniExplosion")
    float MiniExplosionRadius = 200.0f;  // 2 meters

    UPROPERTY(EditAnywhere, Category = "Explosion|MiniExplosion")
    float MiniExplosionDamage = 80.0f;

    UPROPERTY(EditAnywhere, Category = "Explosion|MiniExplosion")
    float MiniExplosionCooldown = 0.5f;  // Spam-capable

    UPROPERTY(EditAnywhere, Category = "Explosion|OmegaExplosion")
    float OmegaExplosionRadius = 2500.0f;  // 600% AoE

    UPROPERTY(EditAnywhere, Category = "Explosion|OmegaExplosion")
    float OmegaExplosionDamage = 2000.0f;

    UPROPERTY(EditAnywhere, Category = "Explosion|OmegaExplosion")
    float OmegaExplosionExhaustion = 30.0f;  // 30 seconds -50% regen

    UPROPERTY(EditAnywhere, Category = "Explosion|OmegaExplosion")
    float OmegaExplosionRegenPenalty = 0.5f;  // -50%

private:
    // Internal state tracking
    int32 VierfachExplosionCount = 0;
    float LastExplosionTime = 0.0f;
    bool bOmegaExplosionReady = false;

    // Helper functions
    void SpawnExplosionEffect(FVector Location, float Radius, float Damage);
    void UpdateExhaustion(float DeltaTime);
    void UpdateCharging(float DeltaTime);
};
