// EnemyAIController.cpp
#include "EnemyAIController.h"
#include "BehaviorTree/BehaviorTree.h"
#include "BehaviorTree/BlackboardComponent.h"
AEnemyAIController::AEnemyAIController() { }
void AEnemyAIController::BeginPlay() {
    Super::BeginPlay();
    if (BehaviorTree) {
        RunBehaviorTree(BehaviorTree);
    }
}
void AEnemyAIController::OnPossess(APawn* InPawn) {
    Super::OnPossess(InPawn);
}
void AEnemyAIController::SetTargetActor(AActor* NewTarget) {
    TargetActor = NewTarget;
    if (GetBlackboardComponent()) {
        GetBlackboardComponent()->SetValueAsObject("TargetActor", NewTarget);
    }
}
void AEnemyAIController::SetBehaviorState(EEnemyBehavior NewState) {
    CurrentBehavior = NewState;
    OnBehaviorChanged.Broadcast(NewState);
}
