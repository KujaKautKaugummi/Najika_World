// FortniteMovementComponent.h
// Fortnite-Style Movement System for Najika Test Environment
// Sprint → Slide → Dash → Vault → Mantle → Wall-Climb

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "FortniteMovementComponent.generated.h"

UENUM(BlueprintType)
enum class EMovementState : uint8
{
    MS_Normal UMETA(DisplayName = "Normal"),
    MS_Sprinting UMETA(DisplayName = "Sprinting"),
    MS_Sliding UMETA(DisplayName = "Sliding"),
    MS_Dashing UMETA(DisplayName = "Dashing"),
    MS_Vaulting UMETA(DisplayName = "Vaulting"),
    MS_Mantling UMETA(DisplayName = "Mantling"),
    MS_WallClimbing UMETA(DisplayName = "Wall Climbing")
};

USTRUCT(BlueprintType)
struct FMovementConfig
{
    GENERATED_BODY()

    // Sprint
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SprintSpeedMultiplier = 1.8f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SprintFOVIncrease = 10.0f;

    // Slide
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SlideDuration = 1.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SlideSpeed = 1200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SlideCooldown = 2.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bSlideHasIFrames = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SlideIFrameDuration = 0.3f;

    // Dash
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DashDistance = 500.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DashDuration = 0.2f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DashCooldown = 3.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bDashHasIFrames = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DashIFrameDuration = 0.2f;

    // Vault
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float VaultHeight = 150.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float VaultDistance = 200.0f;

    // Mantle
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MantleHeight = 250.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MantleDuration = 0.5f;

    // Wall Climb
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float WallClimbSpeed = 300.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MaxWallClimbStamina = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float WallClimbStaminaDrain = 20.0f;
};

UCLASS()
class NAJIKATEST_API UFortniteMovementComponent : public UCharacterMovementComponent
{
    GENERATED_BODY()

public:
    UFortniteMovementComponent();

    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    // ========== SPRINT ==========

    UFUNCTION(BlueprintCallable, Category = "Movement|Sprint")
    void StartSprint();

    UFUNCTION(BlueprintCallable, Category = "Movement|Sprint")
    void StopSprint();

    UFUNCTION(BlueprintPure, Category = "Movement|Sprint")
    bool IsSprinting() const { return MovementState == EMovementState::MS_Sprinting; }

    // ========== SLIDE ==========

    UFUNCTION(BlueprintCallable, Category = "Movement|Slide")
    void StartSlide();

    UFUNCTION(BlueprintCallable, Category = "Movement|Slide")
    void StopSlide();

    UFUNCTION(BlueprintPure, Category = "Movement|Slide")
    bool IsSliding() const { return MovementState == EMovementState::MS_Sliding; }

    UFUNCTION(BlueprintPure, Category = "Movement|Slide")
    bool CanSlide() const;

    // ========== DASH ==========

    UFUNCTION(BlueprintCallable, Category = "Movement|Dash")
    void Dash(FVector Direction);

    UFUNCTION(BlueprintPure, Category = "Movement|Dash")
    bool IsDashing() const { return MovementState == EMovementState::MS_Dashing; }

    UFUNCTION(BlueprintPure, Category = "Movement|Dash")
    bool CanDash() const;

    // ========== VAULT ==========

    UFUNCTION(BlueprintCallable, Category = "Movement|Vault")
    void TryVault();

    UFUNCTION(BlueprintPure, Category = "Movement|Vault")
    bool CanVault() const;

    // ========== MANTLE ==========

    UFUNCTION(BlueprintCallable, Category = "Movement|Mantle")
    void TryMantle();

    UFUNCTION(BlueprintPure, Category = "Movement|Mantle")
    bool CanMantle() const;

    // ========== WALL CLIMB ==========

    UFUNCTION(BlueprintCallable, Category = "Movement|WallClimb")
    void StartWallClimb();

    UFUNCTION(BlueprintCallable, Category = "Movement|WallClimb")
    void StopWallClimb();

    UFUNCTION(BlueprintPure, Category = "Movement|WallClimb")
    bool IsWallClimbing() const { return MovementState == EMovementState::MS_WallClimbing; }

    UFUNCTION(BlueprintPure, Category = "Movement|WallClimb")
    bool CanWallClimb() const;

    // ========== I-FRAMES ==========

    UFUNCTION(BlueprintPure, Category = "Movement|IFrames")
    bool HasIFrames() const { return bHasIFrames; }

    UFUNCTION(BlueprintCallable, Category = "Movement|IFrames")
    void ActivateIFrames(float Duration);

    UFUNCTION(BlueprintCallable, Category = "Movement|IFrames")
    void DeactivateIFrames();

    // ========== STATE ==========

    UFUNCTION(BlueprintPure, Category = "Movement|State")
    EMovementState GetMovementState() const { return MovementState; }

    UFUNCTION(BlueprintPure, Category = "Movement|State")
    float GetWallClimbStamina() const { return WallClimbStamina; }

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement|Config")
    FMovementConfig Config;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Movement|State")
    EMovementState MovementState = EMovementState::MS_Normal;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Movement|State")
    bool bHasIFrames = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Movement|State")
    float IFrameTimeRemaining = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Movement|State")
    float WallClimbStamina = 100.0f;

    // ========== TIMERS ==========

    float SlideTimeRemaining = 0.0f;
    float SlideLastUsedTime = 0.0f;

    float DashTimeRemaining = 0.0f;
    float DashLastUsedTime = 0.0f;
    FVector DashDirection = FVector::ZeroVector;

    float VaultTimeRemaining = 0.0f;

    float MantleTimeRemaining = 0.0f;
    FVector MantleTargetLocation = FVector::ZeroVector;

    FVector WallNormal = FVector::ZeroVector;

private:
    // ========== UPDATE FUNCTIONS ==========

    void UpdateSprint(float DeltaTime);
    void UpdateSlide(float DeltaTime);
    void UpdateDash(float DeltaTime);
    void UpdateVault(float DeltaTime);
    void UpdateMantle(float DeltaTime);
    void UpdateWallClimb(float DeltaTime);
    void UpdateIFrames(float DeltaTime);

    // ========== HELPER FUNCTIONS ==========

    bool CheckForVaultableObstacle(FVector& OutVaultTarget) const;
    bool CheckForMantleableEdge(FVector& OutMantleTarget) const;
    bool CheckForWall(FVector& OutWallNormal) const;

    void SetMovementState(EMovementState NewState);
};
