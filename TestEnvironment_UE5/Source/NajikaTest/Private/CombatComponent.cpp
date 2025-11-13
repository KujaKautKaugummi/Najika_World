// CombatComponent.cpp
// Complete Combat System Implementation - PvE/PvP Separation (Hard Rule #4!)

#include "CombatComponent.h"
#include "StatusEffectsComponent.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"

UCombatComponent::UCombatComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UCombatComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UCombatComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    UpdateComboTimer(DeltaTime);
}

// ========== ATTACK ==========

void UCombatComponent::Attack()
{
    if (!CanAttack()) return;

    bIsAttacking = true;
    LastAttackTime = GetWorld()->GetTimeSeconds();

    // Get current combo attack
    if (ComboChain.Num() > 0)
    {
        int32 ComboIndex = FMath::Min(CurrentComboCount, ComboChain.Num() - 1);
        FComboAttack& ComboAttack = ComboChain[ComboIndex];

        // Perform attack trace
        PerformAttackTrace();

        // Increment combo
        CurrentComboCount++;
        ComboTimer = ComboAttack.ComboWindow;

        OnAttackPerformed.Broadcast(ComboIndex);
    }

    // Reset attack state
    FTimerHandle TimerHandle;
    GetWorld()->GetTimerManager().SetTimer(TimerHandle, [this]()
    {
        bIsAttacking = false;
    }, AttackCooldown, false);
}

void UCombatComponent::HeavyAttack()
{
    if (!CanAttack()) return;

    // Heavy attack is 150% damage but slower
    bIsAttacking = true;
    LastAttackTime = GetWorld()->GetTimeSeconds();

    PerformAttackTrace();

    // Reset attack state
    FTimerHandle TimerHandle;
    GetWorld()->GetTimerManager().SetTimer(TimerHandle, [this]()
    {
        bIsAttacking = false;
    }, AttackCooldown * 1.5f, false);
}

void UCombatComponent::ChargedAttack(float ChargeAmount)
{
    if (!CanAttack()) return;

    // Charged attack scales with charge amount (0.0 - 1.0)
    ChargeAmount = FMath::Clamp(ChargeAmount, 0.0f, 1.0f);

    bIsAttacking = true;
    LastAttackTime = GetWorld()->GetTimeSeconds();

    PerformAttackTrace();

    FTimerHandle TimerHandle;
    GetWorld()->GetTimerManager().SetTimer(TimerHandle, [this]()
    {
        bIsAttacking = false;
    }, AttackCooldown, false);
}

bool UCombatComponent::CanAttack() const
{
    if (bIsAttacking) return false;

    // Check cooldown
    if (GetWorld()->GetTimeSeconds() - LastAttackTime < AttackCooldown) return false;

    // Check status effects
    AActor* Owner = GetOwner();
    if (Owner)
    {
        UStatusEffectsComponent* StatusEffects = Owner->FindComponentByClass<UStatusEffectsComponent>();
        if (StatusEffects && !StatusEffects->CanAttack()) return false;
    }

    return true;
}

// ========== COMBO SYSTEM ==========

void UCombatComponent::ContinueCombo()
{
    if (ComboTimer > 0.0f)
    {
        Attack();
    }
}

void UCombatComponent::ResetCombo()
{
    CurrentComboCount = 0;
    ComboTimer = 0.0f;

    OnComboReset.Broadcast();
}

// ========== DEFENSE ==========

void UCombatComponent::StartBlock()
{
    bIsBlocking = true;
}

void UCombatComponent::StopBlock()
{
    bIsBlocking = false;
}

void UCombatComponent::Parry()
{
    if (!CanParry()) return;

    bCanParry = true;

    // Parry window
    FTimerHandle TimerHandle;
    GetWorld()->GetTimerManager().SetTimer(TimerHandle, [this]()
    {
        bCanParry = false;
    }, ParryWindow, false);
}

bool UCombatComponent::CanParry() const
{
    return !bIsAttacking && !bIsBlocking;
}

void UCombatComponent::Dodge(FVector Direction)
{
    if (!CanDodge()) return;

    LastDodgeTime = GetWorld()->GetTimeSeconds();

    // Add invulnerability frames during dodge
    AActor* Owner = GetOwner();
    if (Owner)
    {
        UStatusEffectsComponent* StatusEffects = Owner->FindComponentByClass<UStatusEffectsComponent>();
        if (StatusEffects)
        {
            FStatusEffect InvulEffect;
            InvulEffect.EffectID = "dodge_invuln";
            InvulEffect.EffectName = "Dodge I-Frames";
            InvulEffect.Type = EStatusEffectType::SE_Invulnerable;
            InvulEffect.Duration = 0.2f; // 200ms i-frames
            InvulEffect.bCanBeRemoved = false;

            StatusEffects->ApplyStatusEffect(InvulEffect);
        }
    }
}

bool UCombatComponent::CanDodge() const
{
    if (GetWorld()->GetTimeSeconds() - LastDodgeTime < DodgeCooldown) return false;

    AActor* Owner = GetOwner();
    if (Owner)
    {
        UStatusEffectsComponent* StatusEffects = Owner->FindComponentByClass<UStatusEffectsComponent>();
        if (StatusEffects && !StatusEffects->CanMove()) return false;
    }

    return true;
}

// ========== DAMAGE CALCULATION ==========

FHitInfo UCombatComponent::CalculateDamage(float BaseDamage, EDamageType DamageType, AActor* Target)
{
    FHitInfo HitInfo;
    HitInfo.Damage = BaseDamage;
    HitInfo.DamageType = DamageType;
    HitInfo.Attacker = GetOwner();
    HitInfo.Victim = Target;

    // Apply attack power
    HitInfo.Damage *= (AttackPower / 100.0f);

    // Critical hit check
    if (RollCritical())
    {
        HitInfo.bIsCritical = true;
        HitInfo.Damage *= CriticalMultiplier;
    }

    // PvP damage reduction (Hard Rule #4!)
    if (bIsPvPEnabled && Target)
    {
        // Check if target is player
        if (Target->GetClass()->IsChildOf(APawn::StaticClass()))
        {
            HitInfo.Damage *= PvPDamageMultiplier;
        }
    }

    // Apply damage reduction from target
    float DamageReduction = CalculateDamageReduction(Target, DamageType);
    HitInfo.Damage *= (1.0f - DamageReduction);

    return HitInfo;
}

void UCombatComponent::ApplyDamage(AActor* Target, const FHitInfo& HitInfo)
{
    if (!Target) return;

    // Apply damage via UE4's damage system
    UGameplayStatics::ApplyDamage(Target, HitInfo.Damage, nullptr, GetOwner(), UDamageType::StaticClass());

    OnDamageDealt.Broadcast(HitInfo);
}

// ========== HIT DETECTION ==========

TArray<AActor*> UCombatComponent::SweepForEnemies(float Radius, float Angle)
{
    TArray<AActor*> HitActors;

    AActor* Owner = GetOwner();
    if (!Owner) return HitActors;

    FVector StartLocation = Owner->GetActorLocation();
    FVector ForwardVector = Owner->GetActorForwardVector();

    // Sphere overlap
    TArray<FOverlapResult> Overlaps;
    FCollisionQueryParams QueryParams;
    QueryParams.AddIgnoredActor(Owner);

    GetWorld()->OverlapMultiByChannel(
        Overlaps,
        StartLocation,
        FQuat::Identity,
        ECC_Pawn,
        FCollisionShape::MakeSphere(Radius),
        QueryParams
    );

    // Filter by angle
    for (const FOverlapResult& Overlap : Overlaps)
    {
        AActor* HitActor = Overlap.GetActor();
        if (!HitActor) continue;

        FVector ToTarget = (HitActor->GetActorLocation() - StartLocation).GetSafeNormal();
        float Dot = FVector::DotProduct(ForwardVector, ToTarget);
        float AngleDeg = FMath::RadiansToDegrees(FMath::Acos(Dot));

        if (AngleDeg <= Angle / 2.0f)
        {
            HitActors.Add(HitActor);
        }
    }

    return HitActors;
}

bool UCombatComponent::CheckHit(AActor* Target, const FVector& HitLocation)
{
    if (!Target) return false;

    // Simple distance check
    AActor* Owner = GetOwner();
    if (!Owner) return false;

    float Distance = FVector::Dist(Owner->GetActorLocation(), Target->GetActorLocation());
    return Distance <= 200.0f; // 2m attack range
}

// ========== LOCK-ON TARGET ==========

void UCombatComponent::LockOnTarget(AActor* Target)
{
    LockOnTarget = Target;
}

void UCombatComponent::ClearLockOnTarget()
{
    LockOnTarget = nullptr;
}

// ========== HELPER FUNCTIONS ==========

void UCombatComponent::UpdateComboTimer(float DeltaTime)
{
    if (ComboTimer > 0.0f)
    {
        ComboTimer -= DeltaTime;

        if (ComboTimer <= 0.0f)
        {
            ResetCombo();
        }
    }
}

bool UCombatComponent::RollCritical() const
{
    float RandomValue = FMath::FRand();
    return RandomValue <= CriticalChance;
}

float UCombatComponent::CalculateDamageReduction(AActor* Target, EDamageType DamageType) const
{
    if (!Target) return 0.0f;

    // Get target's combat component
    UCombatComponent* TargetCombat = Target->FindComponentByClass<UCombatComponent>();
    if (!TargetCombat) return 0.0f;

    float Reduction = 0.0f;

    // Apply defense reduction
    float DefenseValue = TargetCombat->GetDefense();
    Reduction = DefenseValue / (DefenseValue + 100.0f); // Diminishing returns

    // Check blocking
    if (TargetCombat->IsBlocking())
    {
        Reduction += BlockReduction;
    }

    // True damage ignores defense
    if (DamageType == EDamageType::DT_True)
    {
        Reduction = 0.0f;
    }

    return FMath::Clamp(Reduction, 0.0f, 0.95f); // Max 95% reduction
}

void UCombatComponent::PerformAttackTrace()
{
    // Perform attack hit detection
    TArray<AActor*> HitEnemies = SweepForEnemies(200.0f, 90.0f);

    for (AActor* Enemy : HitEnemies)
    {
        FHitInfo HitInfo = CalculateDamage(AttackPower, EDamageType::DT_Physical, Enemy);
        ApplyDamage(Enemy, HitInfo);
    }
}

void UCombatComponent::PerformAttack(EWeaponType WeaponType, int32 ComboIndex)
{
    // This is called by NajikaCharacter
    Attack();
}
