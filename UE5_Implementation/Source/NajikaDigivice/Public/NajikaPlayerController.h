// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "NajikaPlayerController.generated.h"

// Forward declarations
class UInputMappingContext;
class ANajikaCharacter;

/**
 * Player Controller for Najika Digivice
 *
 * Features:
 * - Enhanced Input System setup
 * - Touch controls for mobile
 * - Camera mode switching
 * - UI management
 * - Pause/Menu handling
 */
UCLASS()
class NAJIKADIGIVICE_API ANajikaPlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	ANajikaPlayerController();

protected:
	virtual void BeginPlay() override;
	virtual void SetupInputComponent() override;

public:
	virtual void Tick(float DeltaTime) override;

	// ============================================================
	// ENHANCED INPUT
	// ============================================================

	/** Input Mapping Context */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
	UInputMappingContext* DefaultMappingContext;

	/** Input priority */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
	int32 InputPriority = 0;

	// ============================================================
	// CONTROLLED CHARACTER
	// ============================================================

	/** Get controlled Najika character */
	UFUNCTION(BlueprintPure, Category = "Najika")
	ANajikaCharacter* GetNajikaCharacter() const;

	// ============================================================
	// CAMERA CONTROL
	// ============================================================

	/** Switch camera mode (Third/First/Orbit) */
	UFUNCTION(BlueprintCallable, Category = "Najika|Camera")
	void SwitchCameraMode();

	/** Face camera towards Najika */
	UFUNCTION(BlueprintCallable, Category = "Najika|Camera")
	void FaceNajika();

	// ============================================================
	// TOUCH CONTROLS (MOBILE)
	// ============================================================

	/** Enable/disable touch controls */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Input|Touch")
	bool bEnableTouchControls = true;

	/** Virtual joystick visibility */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Input|Touch")
	bool bShowVirtualJoystick = false;

	/** Initialize touch controls */
	UFUNCTION(BlueprintCallable, Category = "Input|Touch")
	void InitializeTouchControls();

	// ============================================================
	// UI MANAGEMENT
	// ============================================================

	/** Show/hide main HUD */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ToggleHUD();

	/** Show/hide chat UI */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ToggleChat();

	/** Show/hide inventory UI */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ToggleInventory();

	/** Show/hide pause menu */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void TogglePauseMenu();

	/** Is game paused */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|UI")
	bool bIsGamePaused = false;

	// ============================================================
	// CARE ACTIONS (Quick Access)
	// ============================================================

	/** Quick feed action */
	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void QuickFeed();

	/** Quick drink action */
	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void QuickDrink();

	/** Quick praise action */
	UFUNCTION(BlueprintCallable, Category = "Najika|Actions")
	void QuickPraise();

	// ============================================================
	// INTERACTION SYSTEM
	// ============================================================

	/** Interact with object in front of character */
	UFUNCTION(BlueprintCallable, Category = "Najika|Interaction")
	void Interact();

	/** Currently interactable object */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Interaction")
	AActor* CurrentInteractable = nullptr;

	/** Interaction range (cm) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Interaction")
	float InteractionRange = 200.0f;

protected:
	/** Check for interactable objects in front of character */
	void CheckForInteractables();

	/** Currently controlled Najika character */
	UPROPERTY()
	ANajikaCharacter* ControlledNajika = nullptr;
};
