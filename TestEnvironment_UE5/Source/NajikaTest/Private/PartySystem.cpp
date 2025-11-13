// PartySystem.cpp
#include "PartySystem.h"
UPartySystem::UPartySystem() { PrimaryComponentTick.bCanEverTick = false; }
void UPartySystem::BeginPlay() { Super::BeginPlay(); }

bool UPartySystem::CreateParty() {
    if (IsInParty()) return false;
    
    CurrentParty.PartyID = FGuid::NewGuid().ToString();
    CurrentParty.LeaderID = GetOwner() ? GetOwner()->GetName() : "";
    CurrentParty.Members.Empty();
    CurrentParty.Members.Add(CurrentParty.LeaderID);
    bIsInParty = true;
    
    OnPartyCreated.Broadcast(CurrentParty.PartyID);
    return true;
}

bool UPartySystem::InvitePlayer(const FString& PlayerID) {
    if (!IsPartyLeader()) return false;
    if (CurrentParty.Members.Num() >= MaxPartySize) return false;
    
    OnPartyInviteSent.Broadcast(PlayerID);
    return true;
}

bool UPartySystem::KickMember(const FString& PlayerID) {
    if (!IsPartyLeader()) return false;
    if (PlayerID == CurrentParty.LeaderID) return false;
    
    CurrentParty.Members.Remove(PlayerID);
    OnMemberKicked.Broadcast(PlayerID);
    return true;
}

bool UPartySystem::LeaveParty() {
    if (!IsInParty()) return false;
    
    FString MyID = GetOwner() ? GetOwner()->GetName() : "";
    CurrentParty.Members.Remove(MyID);
    
    if (IsPartyLeader() && CurrentParty.Members.Num() > 0) {
        CurrentParty.LeaderID = CurrentParty.Members[0];
    }
    
    bIsInParty = false;
    OnPartyLeft.Broadcast();
    return true;
}

bool UPartySystem::IsPartyLeader() const {
    if (!IsInParty()) return false;
    FString MyID = GetOwner() ? GetOwner()->GetName() : "";
    return CurrentParty.LeaderID == MyID;
}
