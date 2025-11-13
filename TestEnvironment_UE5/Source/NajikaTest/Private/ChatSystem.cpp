// ChatSystem.cpp
#include "ChatSystem.h"
UChatSystem::UChatSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UChatSystem::BeginPlay() { Super::BeginPlay(); }

bool UChatSystem::SendMessage(const FString& Message, EChatChannel Channel) {
    if (Message.IsEmpty() || Message.Len() > MaxMessageLength) return false;
    if (IsSpamming()) return false;
    
    FChatMessage NewMessage;
    NewMessage.MessageID = FGuid::NewGuid().ToString();
    NewMessage.Channel = Channel;
    NewMessage.Message = FilterProfanity(Message);
    NewMessage.Timestamp = FDateTime::Now();
    
    MessageHistory.Add(NewMessage);
    if (MessageHistory.Num() > MaxMessageHistory) MessageHistory.RemoveAt(0);
    
    LastMessageTime = FDateTime::Now();
    MessagesSentRecently++;
    
    OnMessageReceived.Broadcast(NewMessage);
    return true;
}

bool UFriendSystem::SendWhisper(const FString& RecipientID, const FString& Message) {
    return SendMessage(Message, EChatChannel::CC_Whisper);
}

bool UFriendSystem::MutePlayer(const FString& PlayerID) {
    if (!MutedPlayers.Contains(PlayerID)) {
        MutedPlayers.Add(PlayerID);
        return true;
    }
    return false;
}

FString UFriendSystem::FilterProfanity(const FString& Message) const {
    // Simple profanity filter - replace with actual filter in production
    return Message;
}

bool UFriendSystem::IsSpamming() const {
    return MessagesSentRecently > MaxMessagesPerMinute;
}
