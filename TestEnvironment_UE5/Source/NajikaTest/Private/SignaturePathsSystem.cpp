// SignaturePathsSystem.cpp
// Implementation of Signature Paths - Each weapon has ONE unique legendary move

#include "SignaturePathsSystem.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "DrawDebugHelpers.h"

ASignaturePathsSystem::ASignaturePathsSystem()
{
    PrimaryActorTick.bCanEverTick = false;
}

void ASignaturePathsSystem::BeginPlay()
{
    Super::BeginPlay();

    InitializeSignatureMoves();
    InitializeWeaponTalents();
}

// ========== INITIALIZATION ==========

void ASignaturePathsSystem::InitializeSignatureMoves()
{
    // Explosion (Class) - Omega-Explosion
    FSignatureMove omegaExplosion;
    omegaExplosion.MoveName = "Omega-Explosion";
    omegaExplosion.MoveDescription = "Massive 600% AoE explosion with 30s -50% regen";
    omegaExplosion.BaseDamage = 2000.0f;
    omegaExplosion.CooldownDuration = 60.0f;
    omegaExplosion.ChargeTime = 3.0f;
    omegaExplosion.ExhaustionDuration = 30.0f;
    omegaExplosion.SignaturePathBonus = 1.35f;
    omegaExplosion.OtherPathsPenalty = 0.825f;
    SignatureMoves.Add(EWeaponType::WT_Explosion, omegaExplosion);

    // Schwert - Ultimativer Schnitt
    FSignatureMove ultimativerSchnitt;
    ultimativerSchnitt.MoveName = "Ultimativer Schnitt";
    ultimativerSchnitt.MoveDescription = "Single-target massive damage with perfect timing window";
    ultimativerSchnitt.BaseDamage = 1500.0f;
    ultimativerSchnitt.CooldownDuration = 30.0f;
    ultimativerSchnitt.ChargeTime = 1.5f;
    ultimativerSchnitt.ExhaustionDuration = 3.0f;
    ultimativerSchnitt.bHasIFrames = true;
    ultimativerSchnitt.IFrameDuration = 0.5f;
    ultimativerSchnitt.bRequiresSetup = true;
    ultimativerSchnitt.SetupHitsRequired = 3;
    SignatureMoves.Add(EWeaponType::WT_Schwert, ultimativerSchnitt);

    // Speer - Himmelsdurchbohrer
    FSignatureMove himmelsdurchbohrer;
    himmelsdurchbohrer.MoveName = "Himmelsdurchbohrer";
    himmelsdurchbohrer.MoveDescription = "Vertical leap + downward pierce with shockwave";
    himmelsdurchbohrer.BaseDamage = 1200.0f;
    himmelsdurchbohrer.CooldownDuration = 25.0f;
    himmelsdurchbohrer.ChargeTime = 1.0f;
    himmelsdurchbohrer.ExhaustionDuration = 2.0f;
    himmelsdurchbohrer.bRequiresSetup = false;
    SignatureMoves.Add(EWeaponType::WT_Speer, himmelsdurchbohrer);

    // Axt - Spalter
    FSignatureMove spalter;
    spalter.MoveName = "Spalter";
    spalter.MoveDescription = "Overhead cleave that splits enemies and ground";
    spalter.BaseDamage = 1800.0f;
    spalter.CooldownDuration = 35.0f;
    spalter.ChargeTime = 2.0f;
    spalter.ExhaustionDuration = 4.0f;
    SignatureMoves.Add(EWeaponType::WT_Axt, spalter);

    // Hammer - Zertrümmerer
    FSignatureMove zertruemmerer;
    zertruemmerer.MoveName = "Zertrümmerer";
    zertruemmerer.MoveDescription = "Ground slam with AoE stun and damage";
    zertruemmerer.BaseDamage = 1600.0f;
    zertruemmerer.CooldownDuration = 30.0f;
    zertruemmerer.ChargeTime = 1.8f;
    zertruemmerer.ExhaustionDuration = 3.0f;
    SignatureMoves.Add(EWeaponType::WT_Hammer, zertruemmerer);

    // Bogen - Zenit-Schuss
    FSignatureMove zenitSchuss;
    zenitSchuss.MoveName = "Zenit-Schuss";
    zenitSchuss.MoveDescription = "Perfect precision shot from maximum range";
    zenitSchuss.BaseDamage = 2500.0f;
    zenitSchuss.CooldownDuration = 40.0f;
    zenitSchuss.ChargeTime = 3.0f;
    zenitSchuss.ExhaustionDuration = 2.0f;
    zenitSchuss.bRequiresSetup = true;
    zenitSchuss.SetupHitsRequired = 5;
    SignatureMoves.Add(EWeaponType::WT_Bogen, zenitSchuss);

    // Armbrust - Präzisions-Schuss
    FSignatureMove praezisionsSchuss;
    praezisionsSchuss.MoveName = "Präzisions-Schuss";
    praezisionsSchuss.MoveDescription = "Instant piercing shot through all enemies in line";
    praezisionsSchuss.BaseDamage = 1300.0f;
    praezisionsSchuss.CooldownDuration = 20.0f;
    praezisionsSchuss.ChargeTime = 0.5f;
    praezisionsSchuss.ExhaustionDuration = 1.0f;
    SignatureMoves.Add(EWeaponType::WT_Armbrust, praezisionsSchuss);

    // Stab (Magic) - Arkane Kaskade
    FSignatureMove arkaneKaskade;
    arkaneKaskade.MoveName = "Arkane Kaskade";
    arkaneKaskade.MoveDescription = "Channeled spell that chains between enemies";
    arkaneKaskade.BaseDamage = 1400.0f;
    arkaneKaskade.CooldownDuration = 35.0f;
    arkaneKaskade.ChargeTime = 2.5f;
    arkaneKaskade.ExhaustionDuration = 5.0f;
    SignatureMoves.Add(EWeaponType::WT_Stab, arkaneKaskade);

    // Dolch - Schatten-Durchschlag
    FSignatureMove schattenDurchschlag;
    schattenDurchschlag.MoveName = "Schatten-Durchschlag";
    schattenDurchschlag.MoveDescription = "Dash through enemy dealing massive backstab damage";
    schattenDurchschlag.BaseDamage = 2200.0f;
    schattenDurchschlag.CooldownDuration = 25.0f;
    schattenDurchschlag.ChargeTime = 0.8f;
    schattenDurchschlag.ExhaustionDuration = 2.0f;
    schattenDurchschlag.bHasIFrames = true;
    schattenDurchschlag.IFrameDuration = 0.8f;
    schattenDurchschlag.bRequiresSetup = true;
    schattenDurchschlag.SetupHitsRequired = 4;
    SignatureMoves.Add(EWeaponType::WT_Dolch, schattenDurchschlag);

    // Sense - Ernte der Seelen
    FSignatureMove ernteDerSeelen;
    ernteDerSeelen.MoveName = "Ernte der Seelen";
    ernteDerSeelen.MoveDescription = "Wide sweep that heals for damage dealt";
    ernteDerSeelen.BaseDamage = 1100.0f;
    ernteDerSeelen.CooldownDuration = 30.0f;
    ernteDerSeelen.ChargeTime = 1.5f;
    ernteDerSeelen.ExhaustionDuration = 2.0f;
    SignatureMoves.Add(EWeaponType::WT_Sense, ernteDerSeelen);

    // Peitsche - Kettengeißel
    FSignatureMove kettengeissel;
    kettengeissel.MoveName = "Kettengeißel";
    kettengeissel.MoveDescription = "Rapid multi-hit combo in cone area";
    kettengeissel.BaseDamage = 900.0f;
    kettengeissel.CooldownDuration = 20.0f;
    kettengeissel.ChargeTime = 1.0f;
    kettengeissel.ExhaustionDuration = 2.0f;
    SignatureMoves.Add(EWeaponType::WT_Peitsche, kettengeissel);

    UE_LOG(LogTemp, Log, TEXT("Initialized %d Signature Moves"), SignatureMoves.Num());
}

void ASignaturePathsSystem::InitializeWeaponTalents()
{
    // Initialize talent trees for all weapons
    TArray<EWeaponType> allWeapons = {
        EWeaponType::WT_Explosion,
        EWeaponType::WT_Schwert,
        EWeaponType::WT_Speer,
        EWeaponType::WT_Axt,
        EWeaponType::WT_Hammer,
        EWeaponType::WT_Bogen,
        EWeaponType::WT_Armbrust,
        EWeaponType::WT_Stab,
        EWeaponType::WT_Dolch,
        EWeaponType::WT_Sense,
        EWeaponType::WT_Peitsche
    };

    for (EWeaponType weaponType : allWeapons)
    {
        FWeaponTalents talents;
        talents.WeaponType = weaponType;
        talents.BaseDamageBonus = 1.0f;
        talents.AttackSpeedBonus = 1.0f;
        talents.SignatureMoveBonus = 1.0f;
        talents.CooldownReduction = 1.0f;
        talents.TalentPoints = 0;

        WeaponTalentsMap.Add(weaponType, talents);
        SignatureMoveCooldowns.Add(weaponType, 0.0f);
        SetupHitCounters.Add(weaponType, 0);
    }
}

// ========== SIGNATURE MOVES IMPLEMENTATION ==========

void ASignaturePathsSystem::CastOmegaExplosion()
{
    ExecuteSignatureMove(EWeaponType::WT_Explosion);
}

void ASignaturePathsSystem::CastUltimativerSchnitt()
{
    ExecuteSignatureMove(EWeaponType::WT_Schwert);
}

void ASignaturePathsSystem::CastHimmelsdurchbohrer()
{
    ExecuteSignatureMove(EWeaponType::WT_Speer);
}

void ASignaturePathsSystem::CastSpalter()
{
    ExecuteSignatureMove(EWeaponType::WT_Axt);
}

void ASignaturePathsSystem::CastZertruemmerer()
{
    ExecuteSignatureMove(EWeaponType::WT_Hammer);
}

void ASignaturePathsSystem::CastZenitSchuss()
{
    ExecuteSignatureMove(EWeaponType::WT_Bogen);
}

void ASignaturePathsSystem::CastPraezisionsSchuss()
{
    ExecuteSignatureMove(EWeaponType::WT_Armbrust);
}

void ASignaturePathsSystem::CastArkaneKaskade()
{
    ExecuteSignatureMove(EWeaponType::WT_Stab);
}

void ASignaturePathsSystem::CastSchattenDurchschlag()
{
    ExecuteSignatureMove(EWeaponType::WT_Dolch);
}

void ASignaturePathsSystem::CastErnteDerSeelen()
{
    ExecuteSignatureMove(EWeaponType::WT_Sense);
}

void ASignaturePathsSystem::CastKettengeissel()
{
    ExecuteSignatureMove(EWeaponType::WT_Peitsche);
}

// ========== WEAPON SYSTEM ==========

void ASignaturePathsSystem::EquipWeapon(EWeaponType WeaponType)
{
    CurrentWeapon = WeaponType;

    const FSignatureMove* signatureMove = SignatureMoves.Find(WeaponType);
    if (signatureMove)
    {
        UE_LOG(LogTemp, Log, TEXT("Equipped: %s - Signature Move: %s"),
               *UEnum::GetValueAsString(WeaponType),
               *signatureMove->MoveName);
    }
}

bool ASignaturePathsSystem::CanUseSignatureMove() const
{
    const FSignatureMove* signatureMove = SignatureMoves.Find(CurrentWeapon);
    if (!signatureMove)
    {
        return false;
    }

    // Check cooldown
    const float* cooldownTime = SignatureMoveCooldowns.Find(CurrentWeapon);
    if (cooldownTime && *cooldownTime > GetCurrentTime())
    {
        return false;
    }

    // Check setup requirements
    if (signatureMove->bRequiresSetup)
    {
        const int32* setupHits = SetupHitCounters.Find(CurrentWeapon);
        if (!setupHits || *setupHits < signatureMove->SetupHitsRequired)
        {
            return false;
        }
    }

    return true;
}

float ASignaturePathsSystem::GetSignatureMoveCooldownRemaining() const
{
    const float* cooldownTime = SignatureMoveCooldowns.Find(CurrentWeapon);
    if (!cooldownTime)
    {
        return 0.0f;
    }

    float remaining = *cooldownTime - GetCurrentTime();
    return FMath::Max(0.0f, remaining);
}

// ========== TALENT SYSTEM ==========

void ASignaturePathsSystem::InvestTalentPoint(EWeaponType WeaponType, const FString& TalentName)
{
    FWeaponTalents* talents = WeaponTalentsMap.Find(WeaponType);
    if (!talents)
    {
        return;
    }

    talents->TalentPoints++;

    if (TalentName == "BaseDamage")
    {
        talents->BaseDamageBonus += 0.05f;  // +5% per point
    }
    else if (TalentName == "AttackSpeed")
    {
        talents->AttackSpeedBonus += 0.03f;  // +3% per point
    }
    else if (TalentName == "SignatureMove")
    {
        talents->SignatureMoveBonus += 0.08f;  // +8% per point
    }
    else if (TalentName == "CooldownReduction")
    {
        talents->CooldownReduction -= 0.05f;  // -5% cooldown per point
    }

    UE_LOG(LogTemp, Log, TEXT("Invested talent point in %s for %s"),
           *TalentName,
           *UEnum::GetValueAsString(WeaponType));
}

FWeaponTalents ASignaturePathsSystem::GetWeaponTalents(EWeaponType WeaponType) const
{
    const FWeaponTalents* talents = WeaponTalentsMap.Find(WeaponType);
    return talents ? *talents : FWeaponTalents();
}

float ASignaturePathsSystem::GetDamageMultiplier(EWeaponType WeaponType) const
{
    const FWeaponTalents* talents = WeaponTalentsMap.Find(WeaponType);
    if (!talents)
    {
        return 1.0f;
    }

    const FSignatureMove* signatureMove = SignatureMoves.Find(WeaponType);
    if (!signatureMove)
    {
        return talents->BaseDamageBonus;
    }

    // Apply signature path bonus/penalty
    float multiplier = talents->BaseDamageBonus;

    if (WeaponType == CurrentWeapon)
    {
        multiplier *= signatureMove->SignaturePathBonus;
    }
    else
    {
        multiplier *= signatureMove->OtherPathsPenalty;
    }

    return multiplier;
}

// ========== SETUP SYSTEM ==========

void ASignaturePathsSystem::AddSetupHit(EWeaponType WeaponType)
{
    int32* setupHits = SetupHitCounters.Find(WeaponType);
    if (!setupHits)
    {
        return;
    }

    (*setupHits)++;

    const FSignatureMove* signatureMove = SignatureMoves.Find(WeaponType);
    if (signatureMove && signatureMove->bRequiresSetup)
    {
        UE_LOG(LogTemp, Log, TEXT("Setup Hit: %d/%d for %s"),
               *setupHits,
               signatureMove->SetupHitsRequired,
               *UEnum::GetValueAsString(WeaponType));

        if (*setupHits >= signatureMove->SetupHitsRequired)
        {
            UE_LOG(LogTemp, Warning, TEXT("✨ SIGNATURE MOVE READY: %s ✨"),
                   *signatureMove->MoveName);
        }
    }
}

int32 ASignaturePathsSystem::GetSetupHits(EWeaponType WeaponType) const
{
    const int32* setupHits = SetupHitCounters.Find(WeaponType);
    return setupHits ? *setupHits : 0;
}

bool ASignaturePathsSystem::IsSignatureMoveReady(EWeaponType WeaponType) const
{
    const FSignatureMove* signatureMove = SignatureMoves.Find(WeaponType);
    if (!signatureMove)
    {
        return false;
    }

    if (!signatureMove->bRequiresSetup)
    {
        return true;
    }

    const int32* setupHits = SetupHitCounters.Find(WeaponType);
    return setupHits && *setupHits >= signatureMove->SetupHitsRequired;
}

// ========== HELPER FUNCTIONS ==========

void ASignaturePathsSystem::ExecuteSignatureMove(EWeaponType WeaponType)
{
    const FSignatureMove* signatureMove = SignatureMoves.Find(WeaponType);
    if (!signatureMove)
    {
        UE_LOG(LogTemp, Error, TEXT("No signature move found for weapon type"));
        return;
    }

    if (!CanUseSignatureMove())
    {
        UE_LOG(LogTemp, Warning, TEXT("Cannot use signature move - cooldown or setup not ready"));
        return;
    }

    // Calculate final damage
    float finalDamage = signatureMove->BaseDamage * GetDamageMultiplier(WeaponType);

    // Apply cooldown
    ApplyCooldown(WeaponType, signatureMove->CooldownDuration);

    // Reset setup counter
    if (signatureMove->bRequiresSetup)
    {
        SetupHitCounters[WeaponType] = 0;
    }

    UE_LOG(LogTemp, Warning, TEXT("⚡ SIGNATURE MOVE: %s - Damage: %.1f ⚡"),
           *signatureMove->MoveName,
           finalDamage);

    // TODO: Execute actual move logic, VFX, SFX, etc.
}

void ASignaturePathsSystem::ApplyCooldown(EWeaponType WeaponType, float Duration)
{
    const FWeaponTalents* talents = WeaponTalentsMap.Find(WeaponType);
    if (talents)
    {
        Duration *= talents->CooldownReduction;
    }

    float cooldownEndTime = GetCurrentTime() + Duration;
    SignatureMoveCooldowns[WeaponType] = cooldownEndTime;

    UE_LOG(LogTemp, Log, TEXT("Cooldown applied: %.1fs"), Duration);
}

float ASignaturePathsSystem::GetCurrentTime() const
{
    return GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
}
