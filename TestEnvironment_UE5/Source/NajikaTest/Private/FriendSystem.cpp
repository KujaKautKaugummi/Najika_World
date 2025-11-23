// FriendSystem.cpp
#include "FriendSystem.h"
UFriendSystem::UFriendSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UFriendSystem::BeginPlay() { Super::BeginPlay(); }

bool UFriendSystem::AddFriend(const FString& PlayerID) {
    if (Friends.Num() >= MaxFriends) return false;
    if (IsFriend(PlayerID)) return false;
    
    FFriendData NewFriend;
    NewFriend.PlayerID = PlayerID;
    NewFriend.RelationshipStatus = EFriendshipStatus::FS_Pending;
    NewFriend.FriendsSince = FDateTime::Now();
    Friends.Add(PlayerID, NewFriend);
    OnFriendAdded.Broadcast(PlayerID);
    return true;
}

bool UFriendSystem::RemoveFriend(const FString& PlayerID) {
    if (!Friends.Contains(PlayerID)) return false;
    Friends.Remove(PlayerID);
    OnFriendRemoved.Broadcast(PlayerID);
    return true;
}

bool UFriendSystem::IsFriend(const FString& PlayerID) const {
    return Friends.Contains(PlayerID);
}

FFriendData UFriendSystem::GetFriendData(const FString& PlayerID) const {
    if (Friends.Contains(PlayerID)) return Friends[PlayerID];
    return FFriendData();
}

TArray<FFriendData> UFriendSystem::GetOnlineFriends() const {
    TArray<FFriendData> Online;
    for (const auto& Pair : Friends) {
        if (Pair.Value.OnlineStatus == EOnlineStatus::OS_Online || Pair.Value.OnlineStatus == EOnlineStatus::OS_InGame) {
            Online.Add(Pair.Value);
        }
    }
    return Online;
}
