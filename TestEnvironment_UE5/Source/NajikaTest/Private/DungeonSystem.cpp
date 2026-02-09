// DungeonSystem.cpp - From Batch 5 headers
#include "DungeonSystem.h"
UDungeonSystem::UDungeonSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UDungeonSystem::BeginPlay() { Super::BeginPlay(); }
FString UDungeonSystem::CreateInstance(const FString& DungeonID, EDungeonDifficulty Difficulty) {
    FDungeonInstance NewInstance;
    NewInstance.InstanceID = FGuid::NewGuid().ToString();
    NewInstance.DungeonID = DungeonID;
    NewInstance.Difficulty = Difficulty;
    NewInstance.Status = EDungeonStatus::DS_InProgress;
    ActiveInstances.Add(NewInstance.InstanceID, NewInstance);
    OnInstanceCreated.Broadcast(NewInstance.InstanceID);
    return NewInstance.InstanceID;
}
bool UDungeonSystem::CompleteInstance(const FString& InstanceID) {
    if (ActiveInstances.Contains(InstanceID)) {
        ActiveInstances[InstanceID].Status = EDungeonStatus::DS_Completed;
        OnInstanceCompleted.Broadcast(InstanceID);
        return true;
    }
    return false;
}
