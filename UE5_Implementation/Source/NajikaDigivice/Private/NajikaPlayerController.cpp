// Copyright Claude Code. All Rights Reserved.

#include "NajikaPlayerController.h"
#include "EnhancedInputSubsystems.h"
#include "EnhancedInputComponent.h"
#include "NajikaCharacter.h"
#include "Engine/World.h"
#include "DrawDebugHelpers.h"

ANajikaPlayerController::ANajikaPlayerController()
{
	bShowMouseCursor = false;
	bEnableClickEvents = false;
	bEnableMouseOverEvents = false;

	// Enable input by default
	bShowMouseCursor = false;
}

void ANajikaPlayerController::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] BeginPlay"));

	// Add Input Mapping Context
	if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(GetLocalPlayer()))
	{
		if (DefaultMappingContext)
		{
			Subsystem->AddMappingContext(DefaultMappingContext, InputPriority);
			UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Enhanced Input Mapping Context added"));
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("[NajikaPlayerController] DefaultMappingContext is not set!"));
		}
	}

	// Cache controlled character
	ControlledNajika = Cast<ANajikaCharacter>(GetPawn());

	// Initialize touch controls on mobile
	InitializeTouchControls();
}

void ANajikaPlayerController::SetupInputComponent()
{
	Super::SetupInputComponent();

	// Legacy input setup (if not using Enhanced Input)
	if (InputComponent)
	{
		// Bind actions here if needed (or use Enhanced Input in BeginPlay)
	}
}

void ANajikaPlayerController::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Update cached character reference
	if (!ControlledNajika || ControlledNajika != GetPawn())
	{
		ControlledNajika = Cast<ANajikaCharacter>(GetPawn());
	}

	// Check for interactables in front of character
	CheckForInteractables();
}

// ============================================================
// CONTROLLED CHARACTER
// ============================================================

ANajikaCharacter* ANajikaPlayerController::GetNajikaCharacter() const
{
	if (ControlledNajika)
	{
		return ControlledNajika;
	}

	// Fallback: try to get from pawn
	return Cast<ANajikaCharacter>(GetPawn());
}

// ============================================================
// CAMERA CONTROL
// ============================================================

void ANajikaPlayerController::SwitchCameraMode()
{
	ANajikaCharacter* Najika = GetNajikaCharacter();
	if (Najika)
	{
		Najika->SwitchCameraMode();
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Camera mode switched"));
	}
}

void ANajikaPlayerController::FaceNajika()
{
	ANajikaCharacter* Najika = GetNajikaCharacter();
	if (Najika)
	{
		// Rotate controller to face Najika
		FVector CharacterLocation = Najika->GetActorLocation();
		FVector CameraLocation = PlayerCameraManager->GetCameraLocation();

		FRotator LookAtRotation = (CharacterLocation - CameraLocation).Rotation();
		SetControlRotation(LookAtRotation);

		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Camera facing Najika"));
	}
}

// ============================================================
// TOUCH CONTROLS (MOBILE)
// ============================================================

void ANajikaPlayerController::InitializeTouchControls()
{
	// Check if running on mobile platform
	#if PLATFORM_ANDROID || PLATFORM_IOS
		bEnableTouchControls = true;
		bShowVirtualJoystick = true;
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Mobile platform detected - Touch controls enabled"));
	#else
		bEnableTouchControls = false;
		bShowVirtualJoystick = false;
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Desktop platform - Touch controls disabled"));
	#endif

	// TODO: Create virtual joystick widgets (implemented in Blueprint)
}

// ============================================================
// UI MANAGEMENT
// ============================================================

void ANajikaPlayerController::ToggleHUD()
{
	// TODO: Implement HUD toggle (Blueprint)
	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Toggle HUD (implement in Blueprint)"));
}

void ANajikaPlayerController::ToggleChat()
{
	// TODO: Implement Chat UI toggle (Blueprint)
	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Toggle Chat (implement in Blueprint)"));
}

void ANajikaPlayerController::ToggleInventory()
{
	// TODO: Implement Inventory UI toggle (Blueprint)
	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Toggle Inventory (implement in Blueprint)"));
}

void ANajikaPlayerController::TogglePauseMenu()
{
	bIsGamePaused = !bIsGamePaused;

	if (bIsGamePaused)
	{
		// Pause game
		SetPause(true);
		bShowMouseCursor = true;
		SetInputMode(FInputModeUIOnly());
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Game paused"));
	}
	else
	{
		// Unpause game
		SetPause(false);
		bShowMouseCursor = false;
		SetInputMode(FInputModeGameOnly());
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Game unpaused"));
	}

	// TODO: Show/hide pause menu widget (Blueprint)
}

// ============================================================
// CARE ACTIONS (QUICK ACCESS)
// ============================================================

void ANajikaPlayerController::QuickFeed()
{
	ANajikaCharacter* Najika = GetNajikaCharacter();
	if (Najika)
	{
		Najika->Feed();
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Quick Feed"));
	}
}

void ANajikaPlayerController::QuickDrink()
{
	ANajikaCharacter* Najika = GetNajikaCharacter();
	if (Najika)
	{
		Najika->GiveDrink();
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Quick Drink"));
	}
}

void ANajikaPlayerController::QuickPraise()
{
	ANajikaCharacter* Najika = GetNajikaCharacter();
	if (Najika)
	{
		Najika->Praise();
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Quick Praise"));
	}
}

// ============================================================
// INTERACTION SYSTEM
// ============================================================

void ANajikaPlayerController::Interact()
{
	if (CurrentInteractable)
	{
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerController] Interacting with: %s"), *CurrentInteractable->GetName());

		// TODO: Trigger interaction interface (implement in Blueprint)
		// Example: IInteractable::Execute_Interact(CurrentInteractable, GetNajikaCharacter());
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaPlayerController] No interactable object nearby"));
	}
}

void ANajikaPlayerController::CheckForInteractables()
{
	ANajikaCharacter* Najika = GetNajikaCharacter();
	if (!Najika)
	{
		CurrentInteractable = nullptr;
		return;
	}

	// Trace forward from character
	FVector Start = Najika->GetActorLocation();
	FVector Forward = Najika->GetActorForwardVector();
	FVector End = Start + (Forward * InteractionRange);

	// Perform line trace
	FHitResult HitResult;
	FCollisionQueryParams QueryParams;
	QueryParams.AddIgnoredActor(Najika);

	bool bHit = GetWorld()->LineTraceSingleByChannel(
		HitResult,
		Start,
		End,
		ECC_Visibility,
		QueryParams
	);

	if (bHit && HitResult.GetActor())
	{
		// Check if actor is interactable (has IInteractable interface or specific tag)
		AActor* HitActor = HitResult.GetActor();

		if (HitActor->ActorHasTag(FName("Interactable")))
		{
			if (CurrentInteractable != HitActor)
			{
				CurrentInteractable = HitActor;
				UE_LOG(LogTemp, Verbose, TEXT("[NajikaPlayerController] Interactable found: %s"), *HitActor->GetName());
			}
		}
		else
		{
			CurrentInteractable = nullptr;
		}
	}
	else
	{
		CurrentInteractable = nullptr;
	}

	// Debug draw (optional)
	#if WITH_EDITOR
	if (bHit)
	{
		DrawDebugLine(GetWorld(), Start, End, FColor::Green, false, 0.1f, 0, 1.0f);
	}
	else
	{
		DrawDebugLine(GetWorld(), Start, End, FColor::Red, false, 0.1f, 0, 1.0f);
	}
	#endif
}
