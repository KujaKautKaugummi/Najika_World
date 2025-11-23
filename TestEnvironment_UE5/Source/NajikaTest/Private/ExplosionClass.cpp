// ExplosionClass.cpp
// Implementation of the Explosion Class - standalone, never mixed with other elements

#include "ExplosionClass.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "DrawDebugHelpers.h"

AExplosionClass::AExplosionClass()
{
    PrimaryActorTick.bCanEverTick = true;
}

void AExplosionClass::BeginPlay()
{
    Super::BeginPlay();
}

void AExplosionClass::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    UpdateExhaustion(DeltaTime);
    UpdateCharging(DeltaTime);
}

void AExplosionClass::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    // Bind inputs for explosion abilities
    PlayerInputComponent->BindAction("GrosseExplosion", IE_Pressed, this, &AExplosionClass::CastGrosseExplosion);
    PlayerInputComponent->BindAction("VierfachExplosion", IE_Pressed, this, &AExplosionClass::CastVierfachExplosion);
    PlayerInputComponent->BindAction("MiniExplosion", IE_Pressed, this, &AExplosionClass::CastMiniExplosion);
    PlayerInputComponent->BindAction("OmegaExplosion", IE_Pressed, this, &AExplosionClass::CastOmegaExplosion);

    // Charging system
    PlayerInputComponent->BindAction("ChargeExplosion", IE_Pressed, this, &AExplosionClass::StartCharging);
    PlayerInputComponent->BindAction("ChargeExplosion", IE_Released, this, &AExplosionClass::ReleaseExplosion);
}

// ========== CORE EXPLOSION ABILITIES ==========

void AExplosionClass::CastGrosseExplosion()
{
    if (IsExhausted())
    {
        UE_LOG(LogTemp, Warning, TEXT("Cannot cast - still exhausted! %.1fs remaining"), ExhaustionState.ExhaustionDuration);
        return;
    }

    // Apply talent bonuses
    float effectiveRadius = GrossExplosionRadius * GetExplosionRadiusMultiplier();
    float effectiveDamage = GrossExplosionDamage * GetExplosionDamageMultiplier();

    // Spawn explosion at character location
    FVector explosionLocation = GetActorLocation();
    SpawnExplosionEffect(explosionLocation, effectiveRadius, effectiveDamage);

    // Apply exhaustion (long duration for Große Explosion)
    ApplyExhaustion(GrossExplosionExhaustion, 0.0f);

    UE_LOG(LogTemp, Log, TEXT("GROSSE EXPLOSION! Radius: %.1f, Damage: %.1f, Exhaustion: %.1fs"),
           effectiveRadius, effectiveDamage, GrossExplosionExhaustion);
}

void AExplosionClass::CastVierfachExplosion()
{
    if (IsExhausted())
    {
        UE_LOG(LogTemp, Warning, TEXT("Cannot cast - still exhausted!"));
        return;
    }

    // Cast 4 serial explosions with delay
    VierfachExplosionCount = 0;

    // Schedule 4 explosions
    FTimerHandle timerHandle;
    for (int32 i = 0; i < 4; i++)
    {
        float delay = i * VierfachExplosionDelay;

        FTimerDelegate timerDelegate;
        timerDelegate.BindLambda([this, i]()
        {
            float effectiveRadius = VierfachExplosionRadius * GetExplosionRadiusMultiplier();
            float effectiveDamage = VierfachExplosionDamage * GetExplosionDamageMultiplier();

            // Offset each explosion slightly
            FVector offset = FVector(
                FMath::RandRange(-200.0f, 200.0f),
                FMath::RandRange(-200.0f, 200.0f),
                0.0f
            );

            FVector explosionLocation = GetActorLocation() + offset;
            SpawnExplosionEffect(explosionLocation, effectiveRadius, effectiveDamage);

            UE_LOG(LogTemp, Log, TEXT("Vierfach Explosion %d/4 - Radius: %.1f, Damage: %.1f"),
                   i + 1, effectiveRadius, effectiveDamage);
        });

        GetWorldTimerManager().SetTimer(timerHandle, timerDelegate, delay, false);
    }

    // Apply exhaustion after all explosions
    ApplyExhaustion(3.0f, 0.0f); // Moderate exhaustion
}

void AExplosionClass::CastMiniExplosion()
{
    float currentTime = GetWorld()->GetTimeSeconds();

    // Check cooldown (spam-capable but not instant)
    if (currentTime - LastExplosionTime < MiniExplosionCooldown)
    {
        return;
    }

    if (IsExhausted())
    {
        UE_LOG(LogTemp, Warning, TEXT("Cannot cast - exhausted!"));
        return;
    }

    float effectiveRadius = MiniExplosionRadius * GetExplosionRadiusMultiplier();
    float effectiveDamage = MiniExplosionDamage * GetExplosionDamageMultiplier();

    FVector explosionLocation = GetActorLocation();
    SpawnExplosionEffect(explosionLocation, effectiveRadius, effectiveDamage);

    LastExplosionTime = currentTime;

    UE_LOG(LogTemp, Log, TEXT("MINI-EXPLOSION! Radius: %.1f, Damage: %.1f"),
           effectiveRadius, effectiveDamage);
}

void AExplosionClass::CastOmegaExplosion()
{
    if (IsExhausted())
    {
        UE_LOG(LogTemp, Warning, TEXT("Cannot cast OMEGA - still exhausted!"));
        return;
    }

    if (!bOmegaExplosionReady)
    {
        UE_LOG(LogTemp, Warning, TEXT("OMEGA EXPLOSION not ready! Build up energy first!"));
        return;
    }

    // OMEGA EXPLOSION: 600% AoE, 30s -50% Regen
    float effectiveRadius = OmegaExplosionRadius * GetExplosionRadiusMultiplier();
    float effectiveDamage = OmegaExplosionDamage * GetExplosionDamageMultiplier();

    FVector explosionLocation = GetActorLocation();
    SpawnExplosionEffect(explosionLocation, effectiveRadius, effectiveDamage);

    // Apply MASSIVE exhaustion with regeneration penalty
    ApplyExhaustion(OmegaExplosionExhaustion, OmegaExplosionRegenPenalty);

    bOmegaExplosionReady = false;

    UE_LOG(LogTemp, Warning, TEXT("⚠️ OMEGA EXPLOSION!!! ⚠️ Radius: %.1f, Damage: %.1f, Exhaustion: %.1fs with -50%% Regen"),
           effectiveRadius, effectiveDamage, OmegaExplosionExhaustion);
}

// ========== CHARGING SYSTEM ==========

void AExplosionClass::StartCharging()
{
    if (IsExhausted())
    {
        return;
    }

    bIsCharging = true;
    ChargeProgress = 0.0f;

    UE_LOG(LogTemp, Log, TEXT("Started charging explosion..."));
}

void AExplosionClass::StopCharging()
{
    bIsCharging = false;
}

void AExplosionClass::ReleaseExplosion()
{
    if (!bIsCharging)
    {
        return;
    }

    bIsCharging = false;

    // Charge percentage determines explosion power
    float chargePercent = ChargeProgress / MaxCharge;

    if (chargePercent < 0.3f)
    {
        // Low charge = Mini Explosion
        CastMiniExplosion();
    }
    else if (chargePercent < 0.7f)
    {
        // Medium charge = Standard explosion
        CastGrosseExplosion();
    }
    else if (chargePercent >= 1.0f)
    {
        // Full charge = Omega ready
        bOmegaExplosionReady = true;
        UE_LOG(LogTemp, Warning, TEXT("✨ OMEGA EXPLOSION READY! ✨"));
    }
    else
    {
        // High charge = Große Explosion
        CastGrosseExplosion();
    }
}

void AExplosionClass::UpdateCharging(float DeltaTime)
{
    if (!bIsCharging)
    {
        return;
    }

    // Apply talent bonus to charge rate
    float effectiveChargeRate = ChargeRate * Talents.ExplosionChargeSpeedBonus;

    ChargeProgress += effectiveChargeRate * DeltaTime * 10.0f; // 10 = charge speed multiplier
    ChargeProgress = FMath::Clamp(ChargeProgress, 0.0f, MaxCharge);

    // Visual feedback (could trigger particle effects)
    if (FMath::Fmod(ChargeProgress, 10.0f) < 0.1f)
    {
        UE_LOG(LogTemp, Log, TEXT("Charging: %.0f%%"), (ChargeProgress / MaxCharge) * 100.0f);
    }
}

// ========== EXHAUSTION SYSTEM ==========

void AExplosionClass::ApplyExhaustion(float Duration, float RegenPenalty)
{
    ExhaustionState.bIsExhausted = true;
    ExhaustionState.ExhaustionDuration = Duration;
    ExhaustionState.RegenerationPenalty = RegenPenalty;

    UE_LOG(LogTemp, Warning, TEXT("Exhausted for %.1fs (Regen: -%.0f%%)"), Duration, RegenPenalty * 100.0f);
}

void AExplosionClass::UpdateExhaustion(float DeltaTime)
{
    if (!ExhaustionState.bIsExhausted)
    {
        return;
    }

    ExhaustionState.ExhaustionDuration -= DeltaTime;

    if (ExhaustionState.ExhaustionDuration <= 0.0f)
    {
        // Recovery!
        ExhaustionState.bIsExhausted = false;
        ExhaustionState.ExhaustionDuration = 0.0f;
        ExhaustionState.RegenerationPenalty = 0.0f;

        UE_LOG(LogTemp, Log, TEXT("✅ Recovered from exhaustion!"));
    }
}

// ========== TALENT SYSTEM ==========

float AExplosionClass::GetExplosionDamageMultiplier() const
{
    return Talents.ExplosionDamageBonus;
}

float AExplosionClass::GetExplosionRadiusMultiplier() const
{
    return Talents.ExplosionRadiusBonus;
}

void AExplosionClass::UpgradeTalent(const FString& TalentName, float Amount)
{
    if (TalentName == "ExplosionDamage")
    {
        Talents.ExplosionDamageBonus += Amount;
        UE_LOG(LogTemp, Log, TEXT("Upgraded Explosion Damage: +%.2f%% (Total: %.2f%%)"),
               Amount * 100.0f, Talents.ExplosionDamageBonus * 100.0f);
    }
    else if (TalentName == "ExplosionRadius")
    {
        Talents.ExplosionRadiusBonus += Amount;
        UE_LOG(LogTemp, Log, TEXT("Upgraded Explosion Radius: +%.2f%% (Total: %.2f%%)"),
               Amount * 100.0f, Talents.ExplosionRadiusBonus * 100.0f);
    }
    else if (TalentName == "ExplosionChargeSpeed")
    {
        Talents.ExplosionChargeSpeedBonus += Amount;
        UE_LOG(LogTemp, Log, TEXT("Upgraded Charge Speed: +%.2f%% (Total: %.2f%%)"),
               Amount * 100.0f, Talents.ExplosionChargeSpeedBonus * 100.0f);
    }
}

// ========== HELPER FUNCTIONS ==========

void AExplosionClass::SpawnExplosionEffect(FVector Location, float Radius, float Damage)
{
    if (!GetWorld())
    {
        return;
    }

    // Debug visualization
    DrawDebugSphere(
        GetWorld(),
        Location,
        Radius,
        32,
        FColor::Red,
        false,
        2.0f,
        0,
        5.0f
    );

    // Apply damage to actors in radius
    TArray<AActor*> overlappingActors;
    UGameplayStatics::ApplyRadialDamage(
        GetWorld(),
        Damage,
        Location,
        Radius,
        UDamageType::StaticClass(),
        TArray<AActor*>(),
        this,
        nullptr,
        true
    );

    // TODO: Spawn particle effects, sound effects, camera shake
    // UGameplayStatics::SpawnEmitterAtLocation(GetWorld(), ExplosionParticle, Location);
    // UGameplayStatics::PlaySoundAtLocation(GetWorld(), ExplosionSound, Location);
}
