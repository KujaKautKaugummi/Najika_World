// SignaturePathsSystem.h
// Signature Paths - Each weapon/class has ONE unique legendary move
// Section 2.2 from PDF: Jede Waffe/Klasse hat EINEN Signature-Move

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SignaturePathsSystem.generated.h"

// Weapon Types
UENUM(BlueprintType)
enum class EWeaponType : uint8
{
    WT_Explosion UMETA(DisplayName = "Explosion (Class)"),
    WT_Schwert UMETA(DisplayName = "Schwert"),
    WT_Speer UMETA(DisplayName = "Speer"),
    WT_Axt UMETA(DisplayName = "Axt"),
    WT_Hammer UMETA(DisplayName = "Hammer"),
    WT_Bogen UMETA(DisplayName = "Bogen"),
    WT_Armbrust UMETA(DisplayName = "Armbrust"),
    WT_Stab UMETA(DisplayName = "Stab (Magic)"),
    WT_Dolch UMETA(DisplayName = "Dolch"),
    WT_Sense UMETA(DisplayName = "Sense"),
    WT_Peitsche UMETA(DisplayName = "Peitsche")
};

// Signature Move Data
USTRUCT(BlueprintType)
struct FSignatureMove
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString MoveName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString MoveDescription;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float BaseDamage = 500.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float CooldownDuration = 30.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ChargeTime = 2.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ExhaustionDuration = 5.0f;

    // Trade-offs: Bonus for signature path, penalty for others
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SignaturePathBonus = 1.35f;  // +35%

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float OtherPathsPenalty = 0.825f;  // -17.5%

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bHasIFrames = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float IFrameDuration = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bRequiresSetup = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 SetupHitsRequired = 0;
};

// Talent Tree for each weapon
USTRUCT(BlueprintType)
struct FWeaponTalents
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EWeaponType WeaponType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float BaseDamageBonus = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float AttackSpeedBonus = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SignatureMoveBonus = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float CooldownReduction = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 TalentPoints = 0;
};

UCLASS()
class NAJIKATEST_API ASignaturePathsSystem : public AActor
{
    GENERATED_BODY()

public:
    ASignaturePathsSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== SIGNATURE MOVES ==========

    // Explosion Class (already implemented in ExplosionClass)
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Explosion")
    void CastOmegaExplosion();

    // Schwert - Ultimativer Schnitt
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Schwert")
    void CastUltimativerSchnitt();

    // Speer - Himmelsdurchbohrer
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Speer")
    void CastHimmelsdurchbohrer();

    // Axt - Spalter
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Axt")
    void CastSpalter();

    // Hammer - Zertrümmerer
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Hammer")
    void CastZertruemmerer();

    // Bogen - Zenit-Schuss
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Bogen")
    void CastZenitSchuss();

    // Armbrust - Präzisions-Schuss
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Armbrust")
    void CastPraezisionsSchuss();

    // Stab (Magic) - Arkane Kaskade
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Stab")
    void CastArkaneKaskade();

    // Dolch - Schatten-Durchschlag
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Dolch")
    void CastSchattenDurchschlag();

    // Sense - Ernte der Seelen
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Sense")
    void CastErnteDerSeelen();

    // Peitsche - Kettengeißel
    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Peitsche")
    void CastKettengeissel();

    // ========== WEAPON SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Weapon")
    void EquipWeapon(EWeaponType WeaponType);

    UFUNCTION(BlueprintPure, Category = "SignaturePaths|Weapon")
    EWeaponType GetCurrentWeapon() const { return CurrentWeapon; }

    UFUNCTION(BlueprintPure, Category = "SignaturePaths|Weapon")
    bool CanUseSignatureMove() const;

    UFUNCTION(BlueprintPure, Category = "SignaturePaths|Weapon")
    float GetSignatureMoveCooldownRemaining() const;

    // ========== TALENT SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Talents")
    void InvestTalentPoint(EWeaponType WeaponType, const FString& TalentName);

    UFUNCTION(BlueprintPure, Category = "SignaturePaths|Talents")
    FWeaponTalents GetWeaponTalents(EWeaponType WeaponType) const;

    UFUNCTION(BlueprintPure, Category = "SignaturePaths|Talents")
    float GetDamageMultiplier(EWeaponType WeaponType) const;

    // ========== SETUP SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "SignaturePaths|Setup")
    void AddSetupHit(EWeaponType WeaponType);

    UFUNCTION(BlueprintPure, Category = "SignaturePaths|Setup")
    int32 GetSetupHits(EWeaponType WeaponType) const;

    UFUNCTION(BlueprintPure, Category = "SignaturePaths|Setup")
    bool IsSignatureMoveReady(EWeaponType WeaponType) const;

protected:
    // ========== SIGNATURE MOVE DATABASE ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SignaturePaths|Config")
    TMap<EWeaponType, FSignatureMove> SignatureMoves;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SignaturePaths|Config")
    TMap<EWeaponType, FWeaponTalents> WeaponTalentsMap;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SignaturePaths|State")
    EWeaponType CurrentWeapon = EWeaponType::WT_Schwert;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SignaturePaths|State")
    TMap<EWeaponType, float> SignatureMoveCooldowns;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SignaturePaths|State")
    TMap<EWeaponType, int32> SetupHitCounters;

private:
    // ========== HELPER FUNCTIONS ==========

    void InitializeSignatureMoves();
    void InitializeWeaponTalents();

    void ExecuteSignatureMove(EWeaponType WeaponType);
    void ApplyCooldown(EWeaponType WeaponType, float Duration);

    float GetCurrentTime() const;
};
