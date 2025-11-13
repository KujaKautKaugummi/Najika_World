// Copyright Claude Code. All Rights Reserved.

#include "NajikaCharacter.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/InputComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/Controller.h"
#include "GameFramework/SpringArmComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "NajikaHttpClient.h"

ANajikaCharacter::ANajikaCharacter()
{
	// Set this character to call Tick() every frame
	PrimaryActorTick.bCanEverTick = true;

	// Set size for collision capsule
	GetCapsuleComponent()->InitCapsuleSize(42.0f, 96.0f);

	// Don't rotate when the controller rotates. Let that just affect the camera.
	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	// Configure character movement
	GetCharacterMovement()->bOrientRotationToMovement = true; // Character moves in the direction of input...
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 500.0f, 0.0f); // ...at this rotation rate

	// Note: For faster iteration times these variables, and many more, can be tweaked in the Character Blueprint
	// instead of recompiling to adjust them
	GetCharacterMovement()->JumpZVelocity = 700.0f;
	GetCharacterMovement()->AirControl = 0.35f;
	GetCharacterMovement()->MaxWalkSpeed = 500.0f;
	GetCharacterMovement()->MinAnalogWalkSpeed = 20.0f;
	GetCharacterMovement()->BrakingDecelerationWalking = 2000.0f;

	// Create camera boom (pulls in towards the player if there is a collision)
	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 400.0f; // The camera follows at this distance behind the character
	CameraBoom->bUsePawnControlRotation = true; // Rotate the arm based on the controller

	// Create follow camera
	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName); // Attach camera to end of boom
	FollowCamera->bUsePawnControlRotation = false; // Camera does not rotate relative to arm

	// Initialize state
	CurrentState = FNajikaState();
	LivingState = FNajikaLivingState();
}

void ANajikaCharacter::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] BeginPlay - Najika character spawned"));

	// Initialize backend client
	InitializeBackend();

	// Start state sync
	SyncStateFromBackend();
}

void ANajikaCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Auto-sync state from backend
	TimeSinceLastSync += DeltaTime;
	if (TimeSinceLastSync >= StateSyncInterval)
	{
		SyncStateFromBackend();
		TimeSinceLastSync = 0.0f;
	}

	// Regenerate stamina
	if (Stamina < MaxStamina && !bIsDodgeRolling)
	{
		Stamina = FMath::Clamp(Stamina + (StaminaRegenRate * DeltaTime), 0.0f, MaxStamina);
	}

	// End dodge roll after duration
	if (bIsDodgeRolling)
	{
		// Dodge roll duration is ~0.5 seconds (handled by animation)
		// This flag is reset by animation notify or timer
	}
}

void ANajikaCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	// Legacy input bindings (for non-Enhanced Input)
	PlayerInputComponent->BindAxis("MoveForward", this, &ANajikaCharacter::MoveForward);
	PlayerInputComponent->BindAxis("MoveRight", this, &ANajikaCharacter::MoveRight);
	PlayerInputComponent->BindAxis("Turn", this, &ANajikaCharacter::Turn);
	PlayerInputComponent->BindAxis("LookUp", this, &ANajikaCharacter::LookUp);
	PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ANajikaCharacter::Jump);
	PlayerInputComponent->BindAction("Jump", IE_Released, this, &ACharacter::StopJumping);

	// TODO: Enhanced Input bindings (when Input Actions are created in Blueprint)
	// if (UEnhancedInputComponent* EnhancedInputComponent = CastChecked<UEnhancedInputComponent>(PlayerInputComponent))
	// {
	//     EnhancedInputComponent->BindAction(MoveAction, ETriggerEvent::Triggered, this, &ANajikaCharacter::Move);
	//     EnhancedInputComponent->BindAction(LookAction, ETriggerEvent::Triggered, this, &ANajikaCharacter::Look);
	//     EnhancedInputComponent->BindAction(JumpAction, ETriggerEvent::Triggered, this, &ANajikaCharacter::Jump);
	// }
}

// ============================================================
// BACKEND INTEGRATION
// ============================================================

void ANajikaCharacter::InitializeBackend()
{
	if (!BackendClient)
	{
		BackendClient = NewObject<UNajikaHttpClient>(this);
		BackendClient->Initialize(BackendURL);
		UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Backend client initialized: %s"), *BackendURL);
	}
}

void ANajikaCharacter::SyncStateFromBackend()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaCharacter] Cannot sync state - Backend client not initialized"));
		return;
	}

	// Bind delegate and request status
	FOnNajikaStatusResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnStatusReceived);
	BackendClient->GetNajikaStatus(Delegate);
}

void ANajikaCharacter::OnStatusReceived(FNajikaState NajikaState, FNajikaLivingState NewLivingState)
{
	// Update local state
	CurrentState = NajikaState;
	LivingState = NewLivingState;

	// Update combat stats
	CurrentHP = FMath::Clamp((int32)NajikaState.Happiness, 0, MaxHP); // Map happiness to HP for now

	// Broadcast events
	OnStateUpdated.Broadcast(CurrentState);
	OnLivingStateUpdated.Broadcast(LivingState);

	UE_LOG(LogTemp, Verbose, TEXT("[NajikaCharacter] State synced - Hunger: %.1f, Energy: %.1f, Mood: %s"),
		NajikaState.Hunger, NajikaState.Energy, *NewLivingState.CurrentMood);
}

void ANajikaCharacter::OnActionComplete(bool bSuccess, FString Message)
{
	if (bSuccess)
	{
		UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Action complete: %s"), *Message);
		// Refresh state after action
		SyncStateFromBackend();
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaCharacter] Action failed: %s"), *Message);
	}
}

// ============================================================
// CARE ACTIONS
// ============================================================

void ANajikaCharacter::Feed()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot feed - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Feeding Najika..."));
	PlayEatAnimation();

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->FeedNajika(Delegate);
}

void ANajikaCharacter::GiveDrink()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot give drink - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Giving Najika water..."));
	PlayDrinkAnimation();

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->GiveDrink(Delegate);
}

void ANajikaCharacter::Wash()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot wash - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Washing Najika..."));
	PlayWashAnimation();

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->WashNajika(Delegate);
}

void ANajikaCharacter::Sleep()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot sleep - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Putting Najika to sleep..."));
	PlaySleepAnimation();

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->PutToSleep(Delegate);
}

void ANajikaCharacter::Train(const FString& StatType)
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot train - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Training %s..."), *StatType);
	PlayTrainAnimation();

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->TrainNajika(StatType, Delegate);
}

void ANajikaCharacter::Praise()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot praise - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Praising Najika..."));
	PlayPraiseAnimation();

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->PraiseNajika(Delegate);
}

void ANajikaCharacter::Scold()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot scold - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Scolding Najika..."));
	PlayScoldAnimation();

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->ScoldNajika(Delegate);
}

// ============================================================
// MOVEMENT & INPUT
// ============================================================

void ANajikaCharacter::MoveForward(float Value)
{
	if ((Controller != nullptr) && (Value != 0.0f))
	{
		// Find out which way is forward
		const FRotator Rotation = Controller->GetControlRotation();
		const FRotator YawRotation(0, Rotation.Yaw, 0);

		// Get forward vector
		const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
		AddMovementInput(Direction, Value);
	}
}

void ANajikaCharacter::MoveRight(float Value)
{
	if ((Controller != nullptr) && (Value != 0.0f))
	{
		// Find out which way is right
		const FRotator Rotation = Controller->GetControlRotation();
		const FRotator YawRotation(0, Rotation.Yaw, 0);

		// Get right vector
		const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);
		AddMovementInput(Direction, Value);
	}
}

void ANajikaCharacter::Turn(float Value)
{
	AddControllerYawInput(Value);
}

void ANajikaCharacter::LookUp(float Value)
{
	AddControllerPitchInput(Value);
}

void ANajikaCharacter::Move(const FInputActionValue& Value)
{
	// Input is a Vector2D
	FVector2D MovementVector = Value.Get<FVector2D>();

	if (Controller != nullptr)
	{
		// Find out which way is forward
		const FRotator Rotation = Controller->GetControlRotation();
		const FRotator YawRotation(0, Rotation.Yaw, 0);

		// Get forward vector
		const FVector ForwardDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);

		// Get right vector
		const FVector RightDirection = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y);

		// Add movement
		AddMovementInput(ForwardDirection, MovementVector.Y);
		AddMovementInput(RightDirection, MovementVector.X);
	}
}

void ANajikaCharacter::Look(const FInputActionValue& Value)
{
	// Input is a Vector2D
	FVector2D LookAxisVector = Value.Get<FVector2D>();

	if (Controller != nullptr)
	{
		// Add yaw and pitch input to controller
		AddControllerYawInput(LookAxisVector.X);
		AddControllerPitchInput(LookAxisVector.Y);
	}
}

void ANajikaCharacter::Jump()
{
	Super::Jump();
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaCharacter] Jump"));
}

void ANajikaCharacter::DodgeRoll()
{
	if (bIsDodgeRolling)
	{
		return; // Already rolling
	}

	if (Stamina < 20.0f)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaCharacter] Not enough stamina to dodge roll"));
		return;
	}

	bIsDodgeRolling = true;
	Stamina -= 20.0f;

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Dodge roll! Stamina: %.1f"), Stamina);

	// Play dodge animation (Blueprint implementation)
	// Animation will trigger event to reset bIsDodgeRolling flag

	// Set timer to reset flag (fallback if animation notify doesn't fire)
	FTimerHandle DodgeTimerHandle;
	GetWorld()->GetTimerManager().SetTimer(DodgeTimerHandle, [this]()
	{
		bIsDodgeRolling = false;
	}, 0.5f, false);
}

// ============================================================
// COMBAT
// ============================================================

void ANajikaCharacter::TakeDamage(int32 Damage)
{
	CurrentHP = FMath::Clamp(CurrentHP - Damage, 0, MaxHP);
	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Took %d damage! HP: %d/%d"), Damage, CurrentHP, MaxHP);

	if (CurrentHP <= 0)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaCharacter] Najika defeated!"));
		// TODO: Trigger defeat logic (respawn, game over, etc.)
	}
}

void ANajikaCharacter::Heal(int32 Amount)
{
	CurrentHP = FMath::Clamp(CurrentHP + Amount, 0, MaxHP);
	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Healed %d HP! HP: %d/%d"), Amount, CurrentHP, MaxHP);
}

// ============================================================
// EQUIPMENT
// ============================================================

void ANajikaCharacter::EquipItem(const FString& ItemID, const FString& Slot)
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot equip - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Equipping %s to %s slot"), *ItemID, *Slot);

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->EquipItem(ItemID, Slot, Delegate);
}

void ANajikaCharacter::UnequipItem(const FString& Slot)
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaCharacter] Cannot unequip - Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Unequipping from %s slot"), *Slot);

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &ANajikaCharacter::OnActionComplete);
	BackendClient->UnequipItem(Slot, Delegate);
}

// ============================================================
// CAMERA MODES
// ============================================================

void ANajikaCharacter::SwitchCameraMode()
{
	CurrentCameraMode = (CurrentCameraMode + 1) % 3; // Cycle through 0, 1, 2
	SetCameraMode(CurrentCameraMode);
}

void ANajikaCharacter::SetCameraMode(int32 Mode)
{
	CurrentCameraMode = Mode;

	switch (Mode)
	{
	case 0: // Third Person
		CameraBoom->TargetArmLength = 400.0f;
		CameraBoom->SocketOffset = FVector(0.0f, 0.0f, 0.0f);
		CameraBoom->bUsePawnControlRotation = true;
		UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Camera Mode: Third Person"));
		break;

	case 1: // First Person
		CameraBoom->TargetArmLength = 0.0f;
		CameraBoom->SocketOffset = FVector(0.0f, 50.0f, 80.0f); // Eye level
		CameraBoom->bUsePawnControlRotation = true;
		UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Camera Mode: First Person"));
		break;

	case 2: // Orbit (Free Camera)
		CameraBoom->TargetArmLength = 600.0f;
		CameraBoom->SocketOffset = FVector(0.0f, 0.0f, 100.0f);
		CameraBoom->bUsePawnControlRotation = true;
		UE_LOG(LogTemp, Log, TEXT("[NajikaCharacter] Camera Mode: Orbit"));
		break;

	default:
		break;
	}
}
