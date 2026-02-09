// NajikaCharacter.cpp
// COMPLETE Character Controller Implementation

#include "NajikaCharacter.h"
#include "InventoryComponent.h"
#include "ProgressionComponent.h"
#include "CombatComponent.h"
#include "StatusEffectsComponent.h"
#include "EquipmentComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/CapsuleComponent.h"

ANajikaCharacter::ANajikaCharacter(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer.SetDefaultSubobjectClass<UFortniteMovementComponent>(ACharacter::CharacterMovementComponentName))
{
    PrimaryActorTick.bCanEverTick = true;

    // Create components
    FortniteMovement = Cast<UFortniteMovementComponent>(GetCharacterMovement());

    Inventory = CreateDefaultSubobject<UInventoryComponent>(TEXT("Inventory"));
    Progression = CreateDefaultSubobject<UProgressionComponent>(TEXT("Progression"));
    Combat = CreateDefaultSubobject<UCombatComponent>(TEXT("Combat"));
    StatusEffects = CreateDefaultSubobject<UStatusEffectsComponent>(TEXT("StatusEffects"));
    Equipment = CreateDefaultSubobject<UEquipmentComponent>(TEXT("Equipment"));

    // Set default values
    CurrentHealth = MaxHealth;
    CurrentStamina = MaxStamina;
    CurrentMana = MaxMana;
}

void ANajikaCharacter::BeginPlay()
{
    Super::BeginPlay();

    // Initialize health/stamina/mana to max
    CurrentHealth = MaxHealth;
    CurrentStamina = MaxStamina;
    CurrentMana = MaxMana;
}

void ANajikaCharacter::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    // Regenerate resources
    RegenerateHealth(DeltaTime);
    RegenerateStamina(DeltaTime);
    RegenerateMana(DeltaTime);
}

void ANajikaCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    // Movement
    PlayerInputComponent->BindAxis("MoveForward", this, &ANajikaCharacter::MoveForward);
    PlayerInputComponent->BindAxis("MoveRight", this, &ANajikaCharacter::MoveRight);
    PlayerInputComponent->BindAxis("Turn", this, &ANajikaCharacter::Turn);
    PlayerInputComponent->BindAxis("LookUp", this, &ANajikaCharacter::LookUp);

    // Actions
    PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);
    PlayerInputComponent->BindAction("Jump", IE_Released, this, &ACharacter::StopJumping);

    PlayerInputComponent->BindAction("Sprint", IE_Pressed, this, &ANajikaCharacter::StartSprint);
    PlayerInputComponent->BindAction("Sprint", IE_Released, this, &ANajikaCharacter::StopSprint);

    PlayerInputComponent->BindAction("Attack", IE_Pressed, this, &ANajikaCharacter::Attack);
    PlayerInputComponent->BindAction("Block", IE_Pressed, this, [this]() { Block(true); });
    PlayerInputComponent->BindAction("Block", IE_Released, this, [this]() { Block(false); });

    PlayerInputComponent->BindAction("Slide", IE_Pressed, this, &ANajikaCharacter::TrySlide);
    PlayerInputComponent->BindAction("Vault", IE_Pressed, this, &ANajikaCharacter::TryVault);

    PlayerInputComponent->BindAction("SignatureMove", IE_Pressed, this, &ANajikaCharacter::CastSignatureMove);
}

// ========== HEALTH & DAMAGE ==========

void ANajikaCharacter::TakeDamageCustom(float Damage, AActor* DamageCauser)
{
    if (!IsAlive()) return;

    // Apply damage reduction from blocking
    if (bIsBlocking && Combat)
    {
        Damage *= 0.3f; // 70% damage reduction when blocking
    }

    // Apply damage
    CurrentHealth = FMath::Max(0.0f, CurrentHealth - Damage);

    // Broadcast event
    OnHealthChanged.Broadcast(CurrentHealth);

    // Check for death
    if (CurrentHealth <= 0.0f)
    {
        Die();
    }
}

void ANajikaCharacter::Heal(float Amount)
{
    if (!IsAlive()) return;

    CurrentHealth = FMath::Min(MaxHealth, CurrentHealth + Amount);
    OnHealthChanged.Broadcast(CurrentHealth);
}

// ========== STAMINA ==========

bool ANajikaCharacter::ConsumeStamina(float Amount)
{
    if (CurrentStamina >= Amount)
    {
        CurrentStamina -= Amount;
        return true;
    }
    return false;
}

// ========== MANA ==========

bool ANajikaCharacter::ConsumeMana(float Amount)
{
    if (CurrentMana >= Amount)
    {
        CurrentMana -= Amount;
        return true;
    }
    return false;
}

// ========== COMBAT ==========

void ANajikaCharacter::Attack()
{
    if (!IsAlive() || bIsAttacking || bIsBlocking) return;

    bIsAttacking = true;
    ComboCounter++;

    // Delegate to Combat Component
    if (Combat)
    {
        Combat->PerformAttack(CurrentWeapon, ComboCounter);
    }

    // Reset attack state after animation (use timer)
    FTimerHandle TimerHandle;
    GetWorld()->GetTimerManager().SetTimer(TimerHandle, [this]()
    {
        bIsAttacking = false;

        // Reset combo after 2 seconds of no attacks
        FTimerHandle ComboTimerHandle;
        GetWorld()->GetTimerManager().SetTimer(ComboTimerHandle, [this]()
        {
            ComboCounter = 0;
        }, 2.0f, false);

    }, 0.5f, false); // 0.5s attack duration
}

void ANajikaCharacter::Block(bool bStartBlock)
{
    if (!IsAlive()) return;

    bIsBlocking = bStartBlock;
}

// ========== EQUIPMENT ==========

void ANajikaCharacter::EquipWeapon(EWeaponType WeaponType)
{
    CurrentWeapon = WeaponType;

    if (Equipment)
    {
        Equipment->EquipWeapon(WeaponType);
    }
}

void ANajikaCharacter::UnequipWeapon()
{
    CurrentWeapon = EWeaponType::WT_Schwert; // Default

    if (Equipment)
    {
        Equipment->UnequipWeapon();
    }
}

// ========== EXPLOSION ABILITIES ==========

void ANajikaCharacter::CastExplosion(int32 VariantIndex)
{
    if (!CanUseExplosion()) return;

    // Find ExplosionClass component
    UExplosionClass* ExplosionComp = FindComponentByClass<UExplosionClass>();
    if (ExplosionComp)
    {
        ExplosionComp->CastExplosion(VariantIndex);
    }
}

void ANajikaCharacter::StartChargingExplosion()
{
    if (!CanUseExplosion()) return;

    UExplosionClass* ExplosionComp = FindComponentByClass<UExplosionClass>();
    if (ExplosionComp)
    {
        ExplosionComp->StartCharging();
    }
}

void ANajikaCharacter::ReleaseExplosion()
{
    UExplosionClass* ExplosionComp = FindComponentByClass<UExplosionClass>();
    if (ExplosionComp)
    {
        ExplosionComp->ReleaseExplosion();
    }
}

bool ANajikaCharacter::CanUseExplosion() const
{
    if (!IsAlive()) return false;

    UExplosionClass* ExplosionComp = FindComponentByClass<UExplosionClass>();
    if (!ExplosionComp) return false;

    return !ExplosionComp->IsExhausted();
}

// ========== MOVEMENT ==========

void ANajikaCharacter::StartSprint()
{
    if (FortniteMovement)
    {
        FortniteMovement->StartSprint();
    }
}

void ANajikaCharacter::StopSprint()
{
    if (FortniteMovement)
    {
        FortniteMovement->StopSprint();
    }
}

void ANajikaCharacter::TrySlide()
{
    if (FortniteMovement && ConsumeStamina(15.0f))
    {
        FortniteMovement->StartSlide();
    }
}

void ANajikaCharacter::TryDash(FVector Direction)
{
    if (FortniteMovement && ConsumeStamina(20.0f))
    {
        FortniteMovement->PerformDash(Direction);
    }
}

void ANajikaCharacter::TryVault()
{
    if (FortniteMovement && ConsumeStamina(10.0f))
    {
        FortniteMovement->TryVault();
    }
}

// ========== SIGNATURE MOVES ==========

void ANajikaCharacter::CastSignatureMove()
{
    if (!CanCastSignatureMove()) return;

    USignaturePathsSystem* SignatureSystem = FindComponentByClass<USignaturePathsSystem>();
    if (SignatureSystem)
    {
        SignatureSystem->CastSignatureMove(CurrentWeapon);
    }
}

bool ANajikaCharacter::CanCastSignatureMove() const
{
    if (!IsAlive()) return false;

    USignaturePathsSystem* SignatureSystem = FindComponentByClass<USignaturePathsSystem>();
    if (!SignatureSystem) return false;

    return SignatureSystem->CanCastSignatureMove(CurrentWeapon);
}

// ========== STATS ==========

void ANajikaCharacter::AddExperience(int32 Amount)
{
    Experience += Amount;
    CheckLevelUp();

    if (Progression)
    {
        Progression->AddExperience(Amount);
    }
}

// ========== DEATH & RESPAWN ==========

void ANajikaCharacter::Die()
{
    if (CurrentHealth > 0.0f) return; // Already dead check

    CurrentHealth = 0.0f;
    OnCharacterDied.Broadcast();

    // Disable input
    DisableInput(nullptr);

    // Ragdoll or death animation
    GetMesh()->SetSimulatePhysics(true);
}

void ANajikaCharacter::Respawn(FVector RespawnLocation)
{
    // Reset health and resources
    CurrentHealth = MaxHealth;
    CurrentStamina = MaxStamina;
    CurrentMana = MaxMana;

    // Re-enable input
    EnableInput(nullptr);

    // Stop ragdoll
    GetMesh()->SetSimulatePhysics(false);

    // Teleport to respawn location
    SetActorLocation(RespawnLocation);

    OnHealthChanged.Broadcast(CurrentHealth);
}

// ========== PRIVATE METHODS ==========

void ANajikaCharacter::RegenerateHealth(float DeltaTime)
{
    if (!IsAlive()) return;

    // Don't regen during combat
    if (bIsAttacking || bIsBlocking) return;

    CurrentHealth = FMath::Min(MaxHealth, CurrentHealth + HealthRegenRate * DeltaTime);
}

void ANajikaCharacter::RegenerateStamina(float DeltaTime)
{
    // Don't regen while sprinting
    if (FortniteMovement && FortniteMovement->IsSprinting()) return;

    CurrentStamina = FMath::Min(MaxStamina, CurrentStamina + StaminaRegenRate * DeltaTime);
}

void ANajikaCharacter::RegenerateMana(float DeltaTime)
{
    CurrentMana = FMath::Min(MaxMana, CurrentMana + ManaRegenRate * DeltaTime);
}

void ANajikaCharacter::CheckLevelUp()
{
    while (Experience >= ExperienceToNextLevel)
    {
        Experience -= ExperienceToNextLevel;
        LevelUp();
    }
}

void ANajikaCharacter::LevelUp()
{
    Level++;
    OnLevelUp.Broadcast(Level);

    // Increase stats on level up
    MaxHealth += 10.0f;
    MaxStamina += 5.0f;
    MaxMana += 5.0f;

    // Fully heal on level up
    CurrentHealth = MaxHealth;
    CurrentStamina = MaxStamina;
    CurrentMana = MaxMana;

    // Increase XP requirement for next level
    ExperienceToNextLevel = FMath::FloorToInt(ExperienceToNextLevel * 1.2f);
}

// ========== INPUT HANDLERS ==========

void ANajikaCharacter::MoveForward(float Value)
{
    if (Controller && Value != 0.0f && !bIsAttacking)
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0, Rotation.Yaw, 0);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);

        AddMovementInput(Direction, Value);
    }
}

void ANajikaCharacter::MoveRight(float Value)
{
    if (Controller && Value != 0.0f && !bIsAttacking)
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0, Rotation.Yaw, 0);
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
