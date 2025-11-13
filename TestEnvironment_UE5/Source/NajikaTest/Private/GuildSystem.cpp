// GuildSystem.cpp
#include "GuildSystem.h"
UGuildSystem::UGuildSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UGuildSystem::BeginPlay() { Super::BeginPlay(); }

bool UGuildSystem::CreateGuild(const FString& GuildName, const FString& GuildTag) {
    if (IsInGuild()) return false;
    
    CurrentGuild.GuildID = FGuid::NewGuid().ToString();
    CurrentGuild.GuildName = GuildName;
    CurrentGuild.GuildTag = GuildTag;
    CurrentGuild.LeaderID = GetOwner() ? GetOwner()->GetName() : "";
    CurrentGuild.CreationDate = FDateTime::Now();
    
    FGuildMember Leader;
    Leader.PlayerID = CurrentGuild.LeaderID;
    Leader.Rank = EGuildRank::GR_Leader;
    Leader.JoinDate = FDateTime::Now();
    CurrentGuild.Members.Add(Leader.PlayerID, Leader);
    
    bIsInGuild = true;
    OnGuildJoined.Broadcast(CurrentGuild.GuildID);
    return true;
}

bool UGuildSystem::InviteMember(const FString& PlayerID) {
    if (!IsGuildLeader() && !IsGuildOfficer()) return false;
    OnGuildInviteSent.Broadcast(PlayerID);
    return true;
}

bool UGuildSystem::KickMember(const FString& PlayerID) {
    if (!IsGuildLeader() && !IsGuildOfficer()) return false;
    if (PlayerID == CurrentGuild.LeaderID) return false;
    
    CurrentGuild.Members.Remove(PlayerID);
    OnMemberKicked.Broadcast(PlayerID);
    return true;
}

bool UGuildSystem::LeaveGuild() {
    if (!IsInGuild()) return false;
    bIsInGuild = false;
    OnGuildLeft.Broadcast();
    return true;
}

bool UGuildSystem::IsGuildLeader() const {
    if (!IsInGuild()) return false;
    FString MyID = GetOwner() ? GetOwner()->GetName() : "";
    return CurrentGuild.LeaderID == MyID;
}

bool UGuildSystem::IsGuildOfficer() const {
    if (!IsInGuild()) return false;
    FString MyID = GetOwner() ? GetOwner()->GetName() : "";
    if (CurrentGuild.Members.Contains(MyID)) {
        return CurrentGuild.Members[MyID].Rank == EGuildRank::GR_Officer;
    }
    return false;
}
