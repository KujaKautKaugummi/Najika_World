// StatusEffectsComponent.cpp
// Complete Status Effects System Implementation

#include "StatusEffectsComponent.h"

UStatusEffectsComponent::UStatusEffectsComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UStatusEffectsComponent::BeginPlay()
{
    Super::BeginPlay();
}

void UStatusEffectsComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    UpdateEffects(DeltaTime);
}

// ========== APPLY/REMOVE EFFECTS ==========

void UStatusEffectsComponent::ApplyStatusEffect(const FStatusEffect& Effect)
{
    if (!CanApplyEffect(Effect)) return;

    // Check immunity
    if (IsImmuneToEffect(Effect.Type)) return;

    // Check if effect already exists
    FStatusEffect* ExistingEffect = FindEffect(Effect.EffectID);

    if (ExistingEffect)
    {
        // Stack or refresh
        if (bStackSameName && ExistingEffect->CurrentStacks < Effect.MaxStacks)
        {
            StackEffect(*ExistingEffect, Effect);
        }
        else if (bRefreshDuration)
        {
            ExistingEffect->TimeRemaining = Effect.Duration;
        }
    }
    else
    {
        // Add new effect
        if (ActiveEffects.Num() >= MaxSimultaneousEffects)
        {
            // Remove oldest effect
            ActiveEffects.RemoveAt(0);
        }

        FStatusEffect NewEffect = Effect;
        NewEffect.TimeRemaining = Effect.Duration;
        NewEffect.TimeSinceLastTick = 0.0f;
        NewEffect.CurrentStacks = 1;

        ActiveEffects.Add(NewEffect);

        OnStatusEffectApplied.Broadcast(NewEffect);
    }
}

void UStatusEffectsComponent::RemoveStatusEffect(const FString& EffectID)
{
    for (int32 i = ActiveEffects.Num() - 1; i >= 0; i--)
    {
        if (ActiveEffects[i].EffectID == EffectID)
        {
            if (ActiveEffects[i].bCanBeRemoved)
            {
                ActiveEffects.RemoveAt(i);
                OnStatusEffectRemoved.Broadcast(EffectID);
            }
        }
    }
}

void UStatusEffectsComponent::RemoveAllStatusEffects()
{
    for (int32 i = ActiveEffects.Num() - 1; i >= 0; i--)
    {
        if (ActiveEffects[i].bCanBeRemoved)
        {
            FString EffectID = ActiveEffects[i].EffectID;
            ActiveEffects.RemoveAt(i);
            OnStatusEffectRemoved.Broadcast(EffectID);
        }
    }
}

void UStatusEffectsComponent::RemoveEffectsByType(EStatusEffectType Type)
{
    for (int32 i = ActiveEffects.Num() - 1; i >= 0; i--)
    {
        if (ActiveEffects[i].Type == Type && ActiveEffects[i].bCanBeRemoved)
        {
            FString EffectID = ActiveEffects[i].EffectID;
            ActiveEffects.RemoveAt(i);
            OnStatusEffectRemoved.Broadcast(EffectID);
        }
    }
}

void UStatusEffectsComponent::ClearNegativeEffects()
{
    TArray<EStatusEffectType> NegativeTypes =
    {
        EStatusEffectType::SE_Debuff,
        EStatusEffectType::SE_DamageOverTime,
        EStatusEffectType::SE_Stun,
        EStatusEffectType::SE_Root,
        EStatusEffectType::SE_Slow,
        EStatusEffectType::SE_Silence,
        EStatusEffectType::SE_Blind
    };

    for (EStatusEffectType Type : NegativeTypes)
    {
        RemoveEffectsByType(Type);
    }
}

void UStatusEffectsComponent::ClearPositiveEffects()
{
    TArray<EStatusEffectType> PositiveTypes =
    {
        EStatusEffectType::SE_Buff,
        EStatusEffectType::SE_HealOverTime,
        EStatusEffectType::SE_Invulnerable
    };

    for (EStatusEffectType Type : PositiveTypes)
    {
        RemoveEffectsByType(Type);
    }
}

// ========== QUERIES ==========

bool UStatusEffectsComponent::HasStatusEffect(const FString& EffectID) const
{
    for (const FStatusEffect& Effect : ActiveEffects)
    {
        if (Effect.EffectID == EffectID)
        {
            return true;
        }
    }
    return false;
}

bool UStatusEffectsComponent::HasEffectType(EStatusEffectType Type) const
{
    for (const FStatusEffect& Effect : ActiveEffects)
    {
        if (Effect.Type == Type)
        {
            return true;
        }
    }
    return false;
}

FStatusEffect UStatusEffectsComponent::GetStatusEffect(const FString& EffectID) const
{
    for (const FStatusEffect& Effect : ActiveEffects)
    {
        if (Effect.EffectID == EffectID)
        {
            return Effect;
        }
    }
    return FStatusEffect();
}

TArray<FStatusEffect> UStatusEffectsComponent::GetEffectsByType(EStatusEffectType Type) const
{
    TArray<FStatusEffect> Result;
    for (const FStatusEffect& Effect : ActiveEffects)
    {
        if (Effect.Type == Type)
        {
            Result.Add(Effect);
        }
    }
    return Result;
}

int32 UStatusEffectsComponent::GetEffectStacks(const FString& EffectID) const
{
    for (const FStatusEffect& Effect : ActiveEffects)
    {
        if (Effect.EffectID == EffectID)
        {
            return Effect.CurrentStacks;
        }
    }
    return 0;
}

// ========== SPECIAL CONDITIONS ==========

bool UStatusEffectsComponent::IsStunned() const
{
    return HasEffectType(EStatusEffectType::SE_Stun);
}

bool UStatusEffectsComponent::IsRooted() const
{
    return HasEffectType(EStatusEffectType::SE_Root);
}

bool UStatusEffectsComponent::IsSlowed() const
{
    return HasEffectType(EStatusEffectType::SE_Slow);
}

bool UStatusEffectsComponent::IsSilenced() const
{
    return HasEffectType(EStatusEffectType::SE_Silence);
}

bool UStatusEffectsComponent::IsBlind() const
{
    return HasEffectType(EStatusEffectType::SE_Blind);
}

bool UStatusEffectsComponent::IsInvulnerable() const
{
    return HasEffectType(EStatusEffectType::SE_Invulnerable);
}

bool UStatusEffectsComponent::CanMove() const
{
    return !IsStunned() && !IsRooted();
}

bool UStatusEffectsComponent::CanAttack() const
{
    return !IsStunned() && !IsSilenced();
}

bool UStatusEffectsComponent::CanCast() const
{
    return !IsStunned() && !IsSilenced();
}

// ========== STAT MODIFIERS ==========

float UStatusEffectsComponent::GetStatModifier(const FString& StatName) const
{
    float Modifier = 1.0f; // Multiplicative

    for (const FStatusEffect& Effect : ActiveEffects)
    {
        const float* StatMod = Effect.StatModifiers.Find(StatName);
        if (StatMod)
        {
            Modifier *= (*StatMod * Effect.CurrentStacks);
        }
    }

    return Modifier;
}

TMap<FString, float> UStatusEffectsComponent::GetAllStatModifiers() const
{
    TMap<FString, float> AllModifiers;

    for (const FStatusEffect& Effect : ActiveEffects)
    {
        for (const auto& Pair : Effect.StatModifiers)
        {
            if (AllModifiers.Contains(Pair.Key))
            {
                AllModifiers[Pair.Key] *= (Pair.Value * Effect.CurrentStacks);
            }
            else
            {
                AllModifiers.Add(Pair.Key, Pair.Value * Effect.CurrentStacks);
            }
        }
    }

    return AllModifiers;
}

// ========== IMMUNITY ==========

void UStatusEffectsComponent::AddImmunity(EStatusEffectType Type)
{
    if (!Immunities.Contains(Type))
    {
        Immunities.Add(Type);

        // Remove all active effects of this type
        RemoveEffectsByType(Type);
    }
}

void UStatusEffectsComponent::RemoveImmunity(EStatusEffectType Type)
{
    Immunities.Remove(Type);
}

bool UStatusEffectsComponent::IsImmuneToEffect(EStatusEffectType Type) const
{
    return Immunities.Contains(Type);
}

// ========== HELPER FUNCTIONS ==========

void UStatusEffectsComponent::UpdateEffects(float DeltaTime)
{
    for (FStatusEffect& Effect : ActiveEffects)
    {
        // Update duration
        if (!Effect.bIsPermanent)
        {
            Effect.TimeRemaining -= DeltaTime;
        }

        // Process ticks (DoT/HoT)
        ProcessEffectTick(Effect, DeltaTime);
    }

    // Remove expired effects
    RemoveExpiredEffects();
}

void UStatusEffectsComponent::ProcessEffectTick(FStatusEffect& Effect, float DeltaTime)
{
    if (Effect.Type != EStatusEffectType::SE_DamageOverTime &&
        Effect.Type != EStatusEffectType::SE_HealOverTime)
    {
        return;
    }

    Effect.TimeSinceLastTick += DeltaTime;

    while (Effect.TimeSinceLastTick >= Effect.TickInterval)
    {
        Effect.TimeSinceLastTick -= Effect.TickInterval;

        // Process tick
        if (Effect.Type == EStatusEffectType::SE_DamageOverTime && Effect.TickDamage > 0.0f)
        {
            OnStatusEffectTick.Broadcast(Effect.EffectID, -Effect.TickDamage);
        }
        else if (Effect.Type == EStatusEffectType::SE_HealOverTime && Effect.TickHeal > 0.0f)
        {
            OnStatusEffectTick.Broadcast(Effect.EffectID, Effect.TickHeal);
        }
    }
}

void UStatusEffectsComponent::RemoveExpiredEffects()
{
    for (int32 i = ActiveEffects.Num() - 1; i >= 0; i--)
    {
        if (ActiveEffects[i].IsExpired())
        {
            FString EffectID = ActiveEffects[i].EffectID;
            ActiveEffects.RemoveAt(i);
            OnStatusEffectRemoved.Broadcast(EffectID);
        }
    }
}

FStatusEffect* UStatusEffectsComponent::FindEffect(const FString& EffectID)
{
    for (FStatusEffect& Effect : ActiveEffects)
    {
        if (Effect.EffectID == EffectID)
        {
            return &Effect;
        }
    }
    return nullptr;
}

bool UStatusEffectsComponent::CanApplyEffect(const FStatusEffect& Effect) const
{
    // Check immunity
    if (IsImmuneToEffect(Effect.Type)) return false;

    // Check max effects
    if (ActiveEffects.Num() >= MaxSimultaneousEffects && !HasStatusEffect(Effect.EffectID))
    {
        // Only allow if effect already exists
        return false;
    }

    return true;
}

void UStatusEffectsComponent::StackEffect(FStatusEffect& ExistingEffect, const FStatusEffect& NewEffect)
{
    ExistingEffect.CurrentStacks = FMath::Min(ExistingEffect.CurrentStacks + 1, NewEffect.MaxStacks);

    if (bRefreshDuration)
    {
        ExistingEffect.TimeRemaining = NewEffect.Duration;
    }
}
