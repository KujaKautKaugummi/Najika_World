// FactionSystem.cpp
#include "FactionSystem.h"
UFactionSystem::UFactionSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UFactionSystem::BeginPlay() { Super::BeginPlay(); }
void UFactionSystem::ModifyReputation(const FString& FactionID, int32 Amount) {
    if (!FactionReputation.Contains(FactionID)) {
        FactionReputation.Add(FactionID, 0);
    }
    FactionReputation[FactionID] = FMath::Clamp(FactionReputation[FactionID] + Amount, -10000, 10000);
    OnReputationChanged.Broadcast(FactionID, FactionReputation[FactionID]);
}
int32 UFactionSystem::GetReputation(const FString& FactionID) const {
    return FactionReputation.Contains(FactionID) ? FactionReputation[FactionID] : 0;
}
EFactionStanding UFactionSystem::GetStanding(const FString& FactionID) const {
    int32 Rep = GetReputation(FactionID);
    if (Rep >= 3000) return EFactionStanding::FS_Exalted;
    if (Rep >= 2000) return EFactionStanding::FS_Revered;
    if (Rep >= 1000) return EFactionStanding::FS_Honored;
    if (Rep >= 0) return EFactionStanding::FS_Friendly;
    if (Rep >= -1000) return EFactionStanding::FS_Neutral;
    if (Rep >= -2000) return EFactionStanding::FS_Unfriendly;
    return EFactionStanding::FS_Hated;
}
