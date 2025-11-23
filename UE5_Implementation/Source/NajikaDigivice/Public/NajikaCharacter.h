// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "NajikaBackendTypes.h"
#include "NajikaCharacter.generated.h"

// Forward declarations
class UNajikaHttpClient;
class USpringArmComponent;
class UCameraComponent;
class UInputMappingContext;
class UInputAction;
struct FInputActionValue;

/**
 * Main Najika Character Class
 *
 * Features:
 * - WASD movement with rotation
 * - Jump & dodge roll
 * - Backend state synchronization
 * - Care actions (feed, wash, sleep, train)
 * - Equipment system
 * - Animation state machine integration
 *
 * Usage:
 *   - Place in level or spawn dynamically
 *   - Automatically initializes backend client
 *   - Syncs state every 5 seconds
 */
UCLASS()
class NAJIKADIGIVICE_API ANajikaCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	ANajikaCharacter();

protected:
	virtual void BeginPlay() override;

public:
	virtual void Tick(float DeltaTime) override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	// ============================================================
	// COMPONENTS
	// ============================================================

	/** Camera boom positioning the camera behind the character */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	USpringArmComponent* CameraBoom;

	/** Follow camera */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	UCameraComponent* FollowCamera;

	// ============================================================
	// BACKEND INTEGRATION
	// ============================================================

	/** HTTP Client for backend communication */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Backend")
	UNajikaHttpClient* BackendClient;

	/** Backend base URL */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Backend")
	FString BackendURL = TEXT("http://127.0.0.1:8000");

	/** Auto-sync state interval (seconds) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Backend")
	float StateSyncInterval = 5.0f;

	/** Initialize backend client connection */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void InitializeBackend();

	/** Sync state from backend (automatic polling) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void SyncStateFromBackend();

	// ============================================================
	// NAJIKA STATE
	// ============================================================

	/** Current Najika state (synced from backend) */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|State")
	FNajikaState CurrentState;

	/** Current living state (synced from backend) */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|State")
	FNajikaLivingState LivingState;

	/** Event dispatchers for state changes */
	DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnStateUpdated, FNajikaState, NewState);
	UPROPERTY(BlueprintAssignable, Category = "Najika|Events")
	FOnStateUpdated OnStateUpdated;

	DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLivingStateUpdated, FNajikaLivingState, NewLivingState);
	UPROPERTY(BlueprintAssignable, Category = "Najika|Events")
	FOnLivingStateUpdated OnLivingStateUpdated;

	// ============================================================
	// CARE ACTIONS
	// ============================================================

	/** Feed Najika (increases hunger) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void Feed();

	/** Give Najika water (increases thirst) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void GiveDrink();

	/** Wash Najika (increases hygiene) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void Wash();

	/** Put Najika to sleep (restores energy) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void Sleep();

	/** Train specific stat */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void Train(const FString& StatType);

	/** Praise Najika (Digimon World style - increases happiness, decreases discipline) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void Praise();

	/** Scold Najika (increases discipline, decreases happiness) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void Scold();

	// ============================================================
	// ANIMATIONS
	// ============================================================

	/** Play eat animation (implemented in Blueprint) */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayEatAnimation();

	/** Play drink animation */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayDrinkAnimation();

	/** Play wash animation */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayWashAnimation();

	/** Play sleep animation */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlaySleepAnimation();

	/** Play train animation */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayTrainAnimation();

	/** Play praise reaction animation */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayPraiseAnimation();

	/** Play scold reaction animation */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayScoldAnimation();

	/** Play idle animation */
	UFUNCTION(BlueprintImplementableEvent, Category = "Najika|Animation")
	void PlayIdleAnimation();

	// ============================================================
	// MOVEMENT & INPUT
	// ============================================================

	/** Move forward/backward */
	void MoveForward(float Value);

	/** Move right/left */
	void MoveRight(float Value);

	/** Turn camera */
	void Turn(float Value);

	/** Look up/down */
	void LookUp(float Value);

	/** Enhanced Input: Move action */
	void Move(const FInputActionValue& Value);

	/** Enhanced Input: Look action */
	void Look(const FInputActionValue& Value);

	/** Jump */
	virtual void Jump() override;

	/** Dodge roll (combat mechanic) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Combat")
	void DodgeRoll();

	/** Is currently dodge rolling */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Combat")
	bool bIsDodgeRolling = false;

	// ============================================================
	// COMBAT
	// ============================================================

	/** Current HP (local, synced from battle state) */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Combat")
	int32 CurrentHP = 100;

	/** Max HP */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Combat")
	int32 MaxHP = 100;

	/** Stamina (for dodge, attacks) */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Combat")
	float Stamina = 100.0f;

	/** Max Stamina */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Combat")
	float MaxStamina = 100.0f;

	/** Stamina regeneration rate (per second) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Combat")
	float StaminaRegenRate = 10.0f;

	/** Take damage */
	UFUNCTION(BlueprintCallable, Category = "Najika|Combat")
	void TakeDamage(int32 Damage);

	/** Heal */
	UFUNCTION(BlueprintCallable, Category = "Najika|Combat")
	void Heal(int32 Amount);

	// ============================================================
	// EQUIPMENT
	// ============================================================

	/** Equip item to slot */
	UFUNCTION(BlueprintCallable, Category = "Najika|Equipment")
	void EquipItem(const FString& ItemID, const FString& Slot);

	/** Unequip item from slot */
	UFUNCTION(BlueprintCallable, Category = "Najika|Equipment")
	void UnequipItem(const FString& Slot);

	// ============================================================
	// CAMERA MODES
	// ============================================================

	/** Current camera mode */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Camera")
	int32 CurrentCameraMode = 0; // 0 = Third Person, 1 = First Person, 2 = Orbit

	/** Switch camera mode */
	UFUNCTION(BlueprintCallable, Category = "Najika|Camera")
	void SwitchCameraMode();

	/** Set specific camera mode */
	UFUNCTION(BlueprintCallable, Category = "Najika|Camera")
	void SetCameraMode(int32 Mode);

protected:
	// Internal state sync timer
	float TimeSinceLastSync = 0.0f;

	// Callback handlers for backend responses
	UFUNCTION()
	void OnStatusReceived(FNajikaState NajikaState, FNajikaLivingState NewLivingState);

	UFUNCTION()
	void OnActionComplete(bool bSuccess, FString Message);
};
