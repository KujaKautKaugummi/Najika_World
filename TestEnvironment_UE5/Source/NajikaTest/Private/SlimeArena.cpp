// SlimeArena.cpp - Slime battle system (Hard Rule #7 - anonymized learning)
#include "SlimeArena.h"
USlimeArena::USlimeArena() { PrimaryComponentTick.bCanEverTick = false; }
void USlimeArena::BeginPlay() { Super::BeginPlay(); }
void USlimeArena::StartBattle(const FSlimeData& PlayerSlime, const FSlimeData& OpponentSlime) {
    CurrentBattle.BattleID = FGuid::NewGuid().ToString();
    CurrentBattle.PlayerSlime = PlayerSlime;
    CurrentBattle.OpponentSlime = OpponentSlime;
    CurrentBattle.BattleStatus = EBattleStatus::BS_InProgress;
    OnBattleStarted.Broadcast(CurrentBattle.BattleID);
}
void USlimeArena::ExecuteMove(const FSlimeMove& Move) {
    OnMoveExecuted.Broadcast(Move.MoveName);
}
void USlimeArena::EndBattle(bool bPlayerWon) {
    CurrentBattle.BattleStatus = bPlayerWon ? EBattleStatus::BS_PlayerWin : EBattleStatus::BS_PlayerLoss;
    OnBattleEnded.Broadcast(CurrentBattle.BattleID, bPlayerWon);
}
