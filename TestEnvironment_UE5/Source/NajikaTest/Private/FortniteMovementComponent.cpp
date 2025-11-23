// FortniteMovementComponent.cpp
// Implementation of Fortnite-Style Movement System

#include "FortniteMovementComponent.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "Kismet/KismetSystemLibrary.h"
#include "DrawDebugHelpers.h"

UFortniteMovementComponent::UFortniteMovementComponent()
{
    PrimaryComponentTick.bCanEverTick = true;

    // Set default movement values
    MaxWalkSpeed = 600.0f;
    JumpZVelocity = 600.0f;
    AirControl = 0.35f;
    GravityScale = 1.5f;
}

void UFortniteMovementComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    // Update current movement state
    switch (MovementState)
    {
        case EMovementState::MS_Sprinting:
            UpdateSprint(DeltaTime);
            break;

        case EMovementState::MS_Sliding:
            UpdateSlide(DeltaTime);
            break;

        case EMovementState::MS_Dashing:
            UpdateDash(DeltaTime);
            break;

        case EMovementState::MS_Vaulting:
            UpdateVault(DeltaTime);
            break;

        case EMovementState::MS_Mantling:
            UpdateMantle(DeltaTime);
            break;

        case EMovementState::MS_WallClimbing:
            UpdateWallClimb(DeltaTime);
            break;

        default:
            break;
    }

    // Update I-Frames
    UpdateIFrames(DeltaTime);
}

// ========== SPRINT ==========

void UFortniteMovementComponent::StartSprint()
{
    if (MovementState == EMovementState::MS_Normal && !IsFalling())
    {
        SetMovementState(EMovementState::MS_Sprinting);
        MaxWalkSpeed *= Config.SprintSpeedMultiplier;

        UE_LOG(LogTemp, Log, TEXT("Started sprinting - Speed: %.1f"), MaxWalkSpeed);
    }
}

void UFortniteMovementComponent::StopSprint()
{
    if (MovementState == EMovementState::MS_Sprinting)
    {
        SetMovementState(EMovementState::MS_Normal);
        MaxWalkSpeed /= Config.SprintSpeedMultiplier;

        UE_LOG(LogTemp, Log, TEXT("Stopped sprinting - Speed: %.1f"), MaxWalkSpeed);
    }
}

void UFortniteMovementComponent::UpdateSprint(float DeltaTime)
{
    // Sprint ends if not moving or in air
    if (Velocity.Size() < 100.0f || IsFalling())
    {
        StopSprint();
    }
}

// ========== SLIDE ==========

void UFortniteMovementComponent::StartSlide()
{
    if (!CanSlide())
    {
        return;
    }

    SetMovementState(EMovementState::MS_Sliding);
    SlideTimeRemaining = Config.SlideDuration;
    SlideLastUsedTime = GetWorld()->GetTimeSeconds();

    // Activate I-Frames if configured
    if (Config.bSlideHasIFrames)
    {
        ActivateIFrames(Config.SlideIFrameDuration);
    }

    // Set slide velocity
    FVector slideDirection = Velocity.GetSafeNormal();
    Velocity = slideDirection * Config.SlideSpeed;

    UE_LOG(LogTemp, Log, TEXT("Started sliding! I-Frames: %s"), Config.bSlideHasIFrames ? TEXT("YES") : TEXT("NO"));
}

void UFortniteMovementComponent::StopSlide()
{
    if (MovementState == EMovementState::MS_Sliding)
    {
        SetMovementState(EMovementState::MS_Normal);
        SlideTimeRemaining = 0.0f;

        UE_LOG(LogTemp, Log, TEXT("Stopped sliding"));
    }
}

bool UFortniteMovementComponent::CanSlide() const
{
    if (MovementState != EMovementState::MS_Sprinting)
    {
        return false;
    }

    float currentTime = GetWorld()->GetTimeSeconds();
    float timeSinceLastSlide = currentTime - SlideLastUsedTime;

    return timeSinceLastSlide >= Config.SlideCooldown;
}

void UFortniteMovementComponent::UpdateSlide(float DeltaTime)
{
    SlideTimeRemaining -= DeltaTime;

    if (SlideTimeRemaining <= 0.0f)
    {
        StopSlide();
    }

    // Maintain slide velocity
    FVector slideDirection = Velocity.GetSafeNormal();
    Velocity = slideDirection * Config.SlideSpeed;
}

// ========== DASH ==========

void UFortniteMovementComponent::Dash(FVector Direction)
{
    if (!CanDash())
    {
        return;
    }

    SetMovementState(EMovementState::MS_Dashing);
    DashTimeRemaining = Config.DashDuration;
    DashLastUsedTime = GetWorld()->GetTimeSeconds();
    DashDirection = Direction.GetSafeNormal();

    // Activate I-Frames if configured
    if (Config.bDashHasIFrames)
    {
        ActivateIFrames(Config.DashIFrameDuration);
    }

    UE_LOG(LogTemp, Log, TEXT("DASH! Direction: %s, I-Frames: %s"),
           *DashDirection.ToString(),
           Config.bDashHasIFrames ? TEXT("YES") : TEXT("NO"));
}

bool UFortniteMovementComponent::CanDash() const
{
    if (MovementState == EMovementState::MS_Sliding ||
        MovementState == EMovementState::MS_Dashing)
    {
        return false;
    }

    float currentTime = GetWorld()->GetTimeSeconds();
    float timeSinceLastDash = currentTime - DashLastUsedTime;

    return timeSinceLastDash >= Config.DashCooldown;
}

void UFortniteMovementComponent::UpdateDash(float DeltaTime)
{
    DashTimeRemaining -= DeltaTime;

    if (DashTimeRemaining <= 0.0f)
    {
        SetMovementState(EMovementState::MS_Normal);
        DashDirection = FVector::ZeroVector;
        return;
    }

    // Apply dash velocity
    float dashSpeed = Config.DashDistance / Config.DashDuration;
    Velocity = DashDirection * dashSpeed;
}

// ========== VAULT ==========

void UFortniteMovementComponent::TryVault()
{
    if (!CanVault())
    {
        return;
    }

    FVector vaultTarget;
    if (!CheckForVaultableObstacle(vaultTarget))
    {
        return;
    }

    SetMovementState(EMovementState::MS_Vaulting);
    VaultTimeRemaining = 0.3f;

    // Launch character over obstacle
    FVector launchVelocity = (vaultTarget - GetCharacterOwner()->GetActorLocation()).GetSafeNormal();
    launchVelocity.Z = 1.5f;
    launchVelocity *= 800.0f;

    GetCharacterOwner()->LaunchCharacter(launchVelocity, true, true);

    UE_LOG(LogTemp, Log, TEXT("Vaulting! Target: %s"), *vaultTarget.ToString());
}

bool UFortniteMovementComponent::CanVault() const
{
    return MovementState == EMovementState::MS_Sprinting || MovementState == EMovementState::MS_Normal;
}

bool UFortniteMovementComponent::CheckForVaultableObstacle(FVector& OutVaultTarget) const
{
    if (!GetCharacterOwner())
    {
        return false;
    }

    FVector start = GetCharacterOwner()->GetActorLocation();
    FVector forward = GetCharacterOwner()->GetActorForwardVector();
    FVector end = start + forward * Config.VaultDistance;

    FHitResult hitResult;
    FCollisionQueryParams queryParams;
    queryParams.AddIgnoredActor(GetCharacterOwner());

    bool bHit = GetWorld()->LineTraceSingleByChannel(
        hitResult,
        start,
        end,
        ECC_Visibility,
        queryParams
    );

    if (bHit && hitResult.ImpactPoint.Z - start.Z <= Config.VaultHeight)
    {
        OutVaultTarget = hitResult.ImpactPoint + FVector(0, 0, Config.VaultHeight);
        return true;
    }

    return false;
}

void UFortniteMovementComponent::UpdateVault(float DeltaTime)
{
    VaultTimeRemaining -= DeltaTime;

    if (VaultTimeRemaining <= 0.0f)
    {
        SetMovementState(EMovementState::MS_Normal);
    }
}

// ========== MANTLE ==========

void UFortniteMovementComponent::TryMantle()
{
    if (!CanMantle())
    {
        return;
    }

    FVector mantleTarget;
    if (!CheckForMantleableEdge(mantleTarget))
    {
        return;
    }

    SetMovementState(EMovementState::MS_Mantling);
    MantleTimeRemaining = Config.MantleDuration;
    MantleTargetLocation = mantleTarget;

    UE_LOG(LogTemp, Log, TEXT("Mantling! Target: %s"), *mantleTarget.ToString());
}

bool UFortniteMovementComponent::CanMantle() const
{
    return IsFalling() || MovementState == EMovementState::MS_Normal;
}

bool UFortniteMovementComponent::CheckForMantleableEdge(FVector& OutMantleTarget) const
{
    if (!GetCharacterOwner())
    {
        return false;
    }

    FVector start = GetCharacterOwner()->GetActorLocation();
    FVector forward = GetCharacterOwner()->GetActorForwardVector();
    FVector end = start + forward * 150.0f;
    end.Z += Config.MantleHeight;

    FHitResult hitResult;
    FCollisionQueryParams queryParams;
    queryParams.AddIgnoredActor(GetCharacterOwner());

    bool bHit = GetWorld()->LineTraceSingleByChannel(
        hitResult,
        start,
        end,
        ECC_Visibility,
        queryParams
    );

    if (bHit)
    {
        OutMantleTarget = hitResult.ImpactPoint + FVector(0, 0, 100.0f);
        return true;
    }

    return false;
}

void UFortniteMovementComponent::UpdateMantle(float DeltaTime)
{
    MantleTimeRemaining -= DeltaTime;

    if (MantleTimeRemaining <= 0.0f)
    {
        GetCharacterOwner()->SetActorLocation(MantleTargetLocation);
        SetMovementState(EMovementState::MS_Normal);
        return;
    }

    // Lerp to target
    float alpha = 1.0f - (MantleTimeRemaining / Config.MantleDuration);
    FVector currentLocation = GetCharacterOwner()->GetActorLocation();
    FVector newLocation = FMath::Lerp(currentLocation, MantleTargetLocation, alpha);
    GetCharacterOwner()->SetActorLocation(newLocation);
}

// ========== WALL CLIMB ==========

void UFortniteMovementComponent::StartWallClimb()
{
    if (!CanWallClimb())
    {
        return;
    }

    FVector wallNormal;
    if (!CheckForWall(wallNormal))
    {
        return;
    }

    SetMovementState(EMovementState::MS_WallClimbing);
    WallNormal = wallNormal;
    WallClimbStamina = Config.MaxWallClimbStamina;

    // Set gravity to 0 for wall climbing
    GravityScale = 0.0f;

    UE_LOG(LogTemp, Log, TEXT("Started wall climbing! Wall Normal: %s"), *WallNormal.ToString());
}

void UFortniteMovementComponent::StopWallClimb()
{
    if (MovementState == EMovementState::MS_WallClimbing)
    {
        SetMovementState(EMovementState::MS_Normal);
        GravityScale = 1.5f;
        WallNormal = FVector::ZeroVector;

        UE_LOG(LogTemp, Log, TEXT("Stopped wall climbing"));
    }
}

bool UFortniteMovementComponent::CanWallClimb() const
{
    return (MovementState == EMovementState::MS_Normal || IsFalling()) && WallClimbStamina > 0.0f;
}

bool UFortniteMovementComponent::CheckForWall(FVector& OutWallNormal) const
{
    if (!GetCharacterOwner())
    {
        return false;
    }

    FVector start = GetCharacterOwner()->GetActorLocation();
    FVector forward = GetCharacterOwner()->GetActorForwardVector();
    FVector end = start + forward * 100.0f;

    FHitResult hitResult;
    FCollisionQueryParams queryParams;
    queryParams.AddIgnoredActor(GetCharacterOwner());

    bool bHit = GetWorld()->LineTraceSingleByChannel(
        hitResult,
        start,
        end,
        ECC_Visibility,
        queryParams
    );

    if (bHit)
    {
        OutWallNormal = hitResult.ImpactNormal;
        return true;
    }

    return false;
}

void UFortniteMovementComponent::UpdateWallClimb(float DeltaTime)
{
    // Drain stamina
    WallClimbStamina -= Config.WallClimbStaminaDrain * DeltaTime;

    if (WallClimbStamina <= 0.0f)
    {
        StopWallClimb();
        return;
    }

    // Check if still on wall
    FVector wallNormal;
    if (!CheckForWall(wallNormal))
    {
        StopWallClimb();
        return;
    }

    // Apply climbing velocity
    FVector climbDirection = FVector::UpVector;
    Velocity = climbDirection * Config.WallClimbSpeed;
}

// ========== I-FRAMES ==========

void UFortniteMovementComponent::ActivateIFrames(float Duration)
{
    bHasIFrames = true;
    IFrameTimeRemaining = Duration;

    UE_LOG(LogTemp, Warning, TEXT("⚡ I-FRAMES ACTIVE for %.2fs!"), Duration);
}

void UFortniteMovementComponent::DeactivateIFrames()
{
    bHasIFrames = false;
    IFrameTimeRemaining = 0.0f;

    UE_LOG(LogTemp, Log, TEXT("I-Frames ended"));
}

void UFortniteMovementComponent::UpdateIFrames(float DeltaTime)
{
    if (!bHasIFrames)
    {
        return;
    }

    IFrameTimeRemaining -= DeltaTime;

    if (IFrameTimeRemaining <= 0.0f)
    {
        DeactivateIFrames();
    }
}

// ========== HELPER FUNCTIONS ==========

void UFortniteMovementComponent::SetMovementState(EMovementState NewState)
{
    if (MovementState == NewState)
    {
        return;
    }

    EMovementState oldState = MovementState;
    MovementState = NewState;

    UE_LOG(LogTemp, Log, TEXT("Movement State: %d → %d"), (int32)oldState, (int32)NewState);
}
