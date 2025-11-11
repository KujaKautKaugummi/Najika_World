// NajikaCharacter.h
// COMPLETE Character Controller - connects ALL systems!
// This is the main player character that uses all implemented systems

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ExplosionClass.h"
#include "FortniteMovementComponent.h"
#include "SignaturePathsSystem.h"
#include "NajikaCharacter.generated.h"

// Forward declarations
class UInventoryComponent;
class UProgressionComponent;
class UCombatComponent;
class UStatusEffectsComponent;
class UEquipmentComponent;

UCLASS()
class NAJIKATEST_API ANajikaCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ANajikaCharacter(const FObjectInitializer& ObjectInitializer);

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    // ========== HEALTH & DAMAGE ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Health")
    void TakeDamageCustom(float Damage, AActor* DamageCauser);

    UFUNCTION(BlueprintCallable, Category = "Character|Health")
    void Heal(float Amount);

    UFUNCTION(BlueprintPure, Category = "Character|Health")
    float GetHealth() const { return CurrentHealth; }

    UFUNCTION(BlueprintPure, Category = "Character|Health")
    float GetMaxHealth() const { return MaxHealth; }

    UFUNCTION(BlueprintPure, Category = "Character|Health")
    float GetHealthPercent() const { return CurrentHealth / MaxHealth; }

    UFUNCTION(BlueprintPure, Category = "Character|Health")
    bool IsAlive() const { return CurrentHealth > 0.0f; }

    // ========== STAMINA ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Stamina")
    bool ConsumeStamina(float Amount);

    UFUNCTION(BlueprintPure, Category = "Character|Stamina")
    float GetStamina() const { return CurrentStamina; }

    UFUNCTION(BlueprintPure, Category = "Character|Stamina")
    float GetMaxStamina() const { return MaxStamina; }

    UFUNCTION(BlueprintPure, Category = "Character|Stamina")
    float GetStaminaPercent() const { return CurrentStamina / MaxStamina; }

    // ========== MANA (for magic users) ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Mana")
    bool ConsumeMana(float Amount);

    UFUNCTION(BlueprintPure, Category = "Character|Mana")
    float GetMana() const { return CurrentMana; }

    UFUNCTION(BlueprintPure, Category = "Character|Mana")
    float GetMaxMana() const { return MaxMana; }

    // ========== COMBAT ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Combat")
    void Attack();

    UFUNCTION(BlueprintCallable, Category = "Character|Combat")
    void Block(bool bStartBlock);

    UFUNCTION(BlueprintPure, Category = "Character|Combat")
    bool IsBlocking() const { return bIsBlocking; }

    UFUNCTION(BlueprintPure, Category = "Character|Combat")
    bool IsAttacking() const { return bIsAttacking; }

    // ========== EQUIPMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Equipment")
    void EquipWeapon(EWeaponType WeaponType);

    UFUNCTION(BlueprintCallable, Category = "Character|Equipment")
    void UnequipWeapon();

    UFUNCTION(BlueprintPure, Category = "Character|Equipment")
    EWeaponType GetCurrentWeapon() const { return CurrentWeapon; }

    // ========== EXPLOSION ABILITIES ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Explosion")
    void CastExplosion(int32 VariantIndex);

    UFUNCTION(BlueprintCallable, Category = "Character|Explosion")
    void StartChargingExplosion();

    UFUNCTION(BlueprintCallable, Category = "Character|Explosion")
    void ReleaseExplosion();

    UFUNCTION(BlueprintPure, Category = "Character|Explosion")
    bool CanUseExplosion() const;

    // ========== MOVEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Movement")
    void StartSprint();

    UFUNCTION(BlueprintCallable, Category = "Character|Movement")
    void StopSprint();

    UFUNCTION(BlueprintCallable, Category = "Character|Movement")
    void TrySlide();

    UFUNCTION(BlueprintCallable, Category = "Character|Movement")
    void TryDash(FVector Direction);

    UFUNCTION(BlueprintCallable, Category = "Character|Movement")
    void TryVault();

    UFUNCTION(BlueprintPure, Category = "Character|Movement")
    UFortniteMovementComponent* GetFortniteMovement() const { return FortniteMovement; }

    // ========== SIGNATURE MOVES ==========

    UFUNCTION(BlueprintCallable, Category = "Character|SignatureMove")
    void CastSignatureMove();

    UFUNCTION(BlueprintPure, Category = "Character|SignatureMove")
    bool CanCastSignatureMove() const;

    // ========== STATS ==========

    UFUNCTION(BlueprintPure, Category = "Character|Stats")
    int32 GetLevel() const { return Level; }

    UFUNCTION(BlueprintPure, Category = "Character|Stats")
    int32 GetExperience() const { return Experience; }

    UFUNCTION(BlueprintCallable, Category = "Character|Stats")
    void AddExperience(int32 Amount);

    // ========== DEATH & RESPAWN ==========

    UFUNCTION(BlueprintCallable, Category = "Character|Death")
    void Die();

    UFUNCTION(BlueprintCallable, Category = "Character|Death")
    void Respawn(FVector RespawnLocation);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnCharacterDied);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHealthChanged, float, NewHealth);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLevelUp, int32, NewLevel);

    UPROPERTY(BlueprintAssignable, Category = "Character|Events")
    FOnCharacterDied OnCharacterDied;

    UPROPERTY(BlueprintAssignable, Category = "Character|Events")
    FOnHealthChanged OnHealthChanged;

    UPROPERTY(BlueprintAssignable, Category = "Character|Events")
    FOnLevelUp OnLevelUp;

protected:
    // ========== COMPONENTS ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UFortniteMovementComponent* FortniteMovement;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UInventoryComponent* Inventory;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UProgressionComponent* Progression;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UCombatComponent* Combat;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStatusEffectsComponent* StatusEffects;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UEquipmentComponent* Equipment;

    // ========== BASE STATS ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Character|Stats")
    float MaxHealth = 100.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Stats")
    float CurrentHealth = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Character|Stats")
    float MaxStamina = 100.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Stats")
    float CurrentStamina = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Character|Stats")
    float MaxMana = 100.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Stats")
    float CurrentMana = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Character|Stats")
    float HealthRegenRate = 1.0f;  // HP per second

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Character|Stats")
    float StaminaRegenRate = 10.0f;  // Stamina per second

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Character|Stats")
    float ManaRegenRate = 5.0f;  // Mana per second

    // ========== PROGRESSION ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Progression")
    int32 Level = 1;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Progression")
    int32 Experience = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Character|Progression")
    int32 ExperienceToNextLevel = 100;

    // ========== COMBAT STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Combat")
    bool bIsBlocking = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Combat")
    bool bIsAttacking = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Combat")
    EWeaponType CurrentWeapon = EWeaponType::WT_Schwert;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Character|Combat")
    int32 ComboCounter = 0;

private:
    // ========== REGENERATION ==========

    void RegenerateHealth(float DeltaTime);
    void RegenerateStamina(float DeltaTime);
    void RegenerateMana(float DeltaTime);

    // ========== LEVEL UP ==========

    void CheckLevelUp();
    void LevelUp();

    // ========== INPUT HANDLERS ==========

    void MoveForward(float Value);
    void MoveRight(float Value);
    void Turn(float Value);
    void LookUp(float Value);
};
