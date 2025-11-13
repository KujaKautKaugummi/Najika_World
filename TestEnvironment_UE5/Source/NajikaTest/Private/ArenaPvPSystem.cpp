// ArenaPvPSystem.cpp - From Batch 5 headers
#include "ArenaPvPSystem.h"
UArenaPvPSystem::UArenaPvPSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UArenaPvPSystem::BeginPlay() { Super::BeginPlay(); }
bool UArenaPvPSystem::QueueForMatch(EArenaMode Mode) {
    if (bIsInQueue) return false;
    bIsInQueue = true;
    QueuedMode = Mode;
    OnMatchmakingStarted.Broadcast(Mode);
    return true;
}
void UArenaPvPSystem::LeaveQueue() {
    bIsInQueue = false;
    OnMatchmakingCancelled.Broadcast();
}
void UArenaPvPSystem::UpdateElo(int32 EloDelta) {
    CurrentElo += EloDelta;
    CurrentElo = FMath::Clamp(CurrentElo, 0, 5000);
    OnEloUpdated.Broadcast(CurrentElo);
}
EPlayerRank UArenaPvPSystem::GetCurrentRank() const {
    if (CurrentElo >= 3000) return EPlayerRank::PR_Legend;
    if (CurrentElo >= 2500) return EPlayerRank::PR_Diamond;
    if (CurrentElo >= 2000) return EPlayerRank::PR_Platinum;
    if (CurrentElo >= 1500) return EPlayerRank::PR_Gold;
    if (CurrentElo >= 1000) return EPlayerRank::PR_Silver;
    return EPlayerRank::PR_Bronze;
}
