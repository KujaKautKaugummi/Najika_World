// EnemyAIController.h
// Complete Enemy AI System: Behavior States, Combat, Patrolling, Aggro

#pragma once

#include "CoreMinimal.h"
#include "AIController.h"
#include "EnemyAIController.generated.h"

// AI State
UENUM(BlueprintType)
enum class EAIState : uint8
{
    AS_Idle UMETA(DisplayName = "Idle"),
    AS_Patrol UMETA(DisplayName = "Patrol"),
    AS_Chase UMETA(DisplayName = "Chase"),
    AS_Attack UMETA(DisplayName = "Attack"),
    AS_Flee UMETA(DisplayName = "Flee"),
    AS_Dead UMETA(DisplayName = "Dead"),
    AS_Stunned UMETA(DisplayName = "Stunned")
};

// AI Difficulty
UENUM(BlueprintType)
enum class EAIDifficulty : uint8
{
    AD_Easy UMETA(DisplayName = "Easy"),
    AD_Normal UMETA(DisplayName = "Normal"),
    AD_Hard UMETA(DisplayName = "Hard"),
    AD_Elite UMETA(DisplayName = "Elite"),
    AD_Boss UMETA(DisplayName = "Boss")
};

UCLASS()
class NAJIKATEST_API AEnemyAIController : public AAIController
{
    GENERATED_BODY()

public:
    AEnemyAIController();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;
    virtual void OnPossess(APawn* InPawn) override;

    // ========== STATE MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|State")
    void SetAIState(EAIState NewState);

    UFUNCTION(BlueprintPure, Category = "EnemyAI|State")
    EAIState GetAIState() const { return CurrentState; }

    // ========== PATROL ==========

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Patrol")
    void StartPatrol();

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Patrol")
    void AddPatrolPoint(FVector Point);

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Patrol")
    void ClearPatrolPoints();

    // ========== AGGRO/CHASE ==========

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Aggro")
    void AggroTarget(AActor* Target);

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Aggro")
    void LoseAggro();

    UFUNCTION(BlueprintPure, Category = "EnemyAI|Aggro")
    AActor* GetCurrentTarget() const { return CurrentTarget; }

    UFUNCTION(BlueprintPure, Category = "EnemyAI|Aggro")
    bool HasTarget() const { return CurrentTarget != nullptr; }

    // ========== COMBAT ==========

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Combat")
    void AttackTarget();

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Combat")
    void UseSpecialAbility(int32 AbilityIndex);

    UFUNCTION(BlueprintPure, Category = "EnemyAI|Combat")
    bool IsInAttackRange() const;

    UFUNCTION(BlueprintPure, Category = "EnemyAI|Combat")
    float GetDistanceToTarget() const;

    // ========== PERCEPTION ==========

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Perception")
    void DetectEnemies();

    UFUNCTION(BlueprintPure, Category = "EnemyAI|Perception")
    bool CanSeeTarget(AActor* Target) const;

    UFUNCTION(BlueprintPure, Category = "EnemyAI|Perception")
    TArray<AActor*> GetVisibleEnemies() const;

    // ========== BEHAVIOR ==========

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Behavior")
    void FleeFromTarget(AActor* ThreatTarget);

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Behavior")
    void ReturnToSpawnPoint();

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Behavior")
    void CallForHelp(float Radius);

    // ========== DIFFICULTY ==========

    UFUNCTION(BlueprintCallable, Category = "EnemyAI|Difficulty")
    void SetDifficulty(EAIDifficulty Difficulty);

    UFUNCTION(BlueprintPure, Category = "EnemyAI|Difficulty")
    EAIDifficulty GetDifficulty() const { return Difficulty; }

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnStateChanged, EAIState, NewState);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTargetAcquired, AActor*, Target);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnTargetLost);

    UPROPERTY(BlueprintAssignable, Category = "EnemyAI|Events")
    FOnStateChanged OnStateChanged;

    UPROPERTY(BlueprintAssignable, Category = "EnemyAI|Events")
    FOnTargetAcquired OnTargetAcquired;

    UPROPERTY(BlueprintAssignable, Category = "EnemyAI|Events")
    FOnTargetLost OnTargetLost;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float DetectionRadius = 1000.0f;  // 10 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float AttackRange = 200.0f;  // 2 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float LoseAggroDistance = 2000.0f;  // 20 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float AttackCooldown = 2.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float PatrolSpeed = 200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float ChaseSpeed = 400.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float FleeSpeed = 500.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    float FleeHealthThreshold = 0.2f;  // Flee at 20% HP

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    bool bCanFlee = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    bool bCallForHelp = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "EnemyAI|Config")
    EAIDifficulty Difficulty = EAIDifficulty::AD_Normal;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EnemyAI|State")
    EAIState CurrentState = EAIState::AS_Idle;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EnemyAI|State")
    AActor* CurrentTarget = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EnemyAI|State")
    TArray<FVector> PatrolPoints;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EnemyAI|State")
    int32 CurrentPatrolIndex = 0;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EnemyAI|State")
    FVector SpawnLocation = FVector::ZeroVector;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EnemyAI|State")
    float LastAttackTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "EnemyAI|State")
    bool bIsStunned = false;

private:
    // ========== BEHAVIOR FUNCTIONS ==========

    void UpdateIdleState(float DeltaTime);
    void UpdatePatrolState(float DeltaTime);
    void UpdateChaseState(float DeltaTime);
    void UpdateAttackState(float DeltaTime);
    void UpdateFleeState(float DeltaTime);

    void MoveToNextPatrolPoint();
    bool ShouldFlee() const;
    void UpdateMovementSpeed();

    // ========== PERCEPTION ==========

    AActor* FindNearestEnemy();
    bool LineOfSightCheck(AActor* Target) const;
};
