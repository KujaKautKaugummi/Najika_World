// ChatSystem.h
// Vollständiges Chat-System für Multiplayer mit Kanälen, Filtern, Emotes

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ChatSystem.generated.h"

// Chat-Kanal
UENUM(BlueprintType)
enum class EChatChannel : uint8
{
    CC_Say UMETA(DisplayName = "Say (Lokal)"),
    CC_Yell UMETA(DisplayName = "Yell (Weit)"),
    CC_Whisper UMETA(DisplayName = "Whisper (Privat)"),
    CC_Party UMETA(DisplayName = "Party"),
    CC_Guild UMETA(DisplayName = "Guild"),
    CC_Trade UMETA(DisplayName = "Trade"),
    CC_Global UMETA(DisplayName = "Global"),
    CC_System UMETA(DisplayName = "System"),
    CC_Combat UMETA(DisplayName = "Combat Log"),
    CC_Emote UMETA(DisplayName = "Emote")
};

// Nachrichten-Typ
UENUM(BlueprintType)
enum class EMessageType : uint8
{
    MT_Normal UMETA(DisplayName = "Normal"),
    MT_System UMETA(DisplayName = "System"),
    MT_Warning UMETA(DisplayName = "Warning"),
    MT_Error UMETA(DisplayName = "Error"),
    MT_Achievement UMETA(DisplayName = "Achievement"),
    MT_Loot UMETA(DisplayName = "Loot"),
    MT_Combat UMETA(DisplayName = "Combat")
};

// Chat-Nachricht
USTRUCT(BlueprintType)
struct FChatMessage
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString MessageID;

    UPROPERTY(BlueprintReadWrite)
    EChatChannel Channel;

    UPROPERTY(BlueprintReadWrite)
    EMessageType Type;

    UPROPERTY(BlueprintReadWrite)
    FString SenderID;

    UPROPERTY(BlueprintReadWrite)
    FString SenderName;

    UPROPERTY(BlueprintReadWrite)
    FString ReceiverID;  // Für Whisper

    UPROPERTY(BlueprintReadWrite)
    FString Message;

    UPROPERTY(BlueprintReadWrite)
    FLinearColor Color = FLinearColor::White;

    UPROPERTY(BlueprintReadWrite)
    FDateTime Timestamp;

    UPROPERTY(BlueprintReadWrite)
    bool bIsFiltered = false;  // Durch Profanity-Filter

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> MentionedPlayerIDs;  // @Spielername
};

// Chat-Filter
USTRUCT(BlueprintType)
struct FChatFilter
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bFilterProfanity = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bFilterSpam = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bFilterLinks = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SpamThresholdSeconds = 2.0f;  // Min. Zeit zwischen Nachrichten

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> BannedWords;
};

// Emote-Daten
USTRUCT(BlueprintType)
struct FEmote
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EmoteID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EmoteName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EmoteCommand;  // /wave, /dance, etc.

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AnimationName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TextOutput;  // "{PlayerName} winkt."

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bHasSound = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bRequiresTarget = false;
};

UCLASS()
class NAJIKATEST_API AChatSystem : public AActor
{
    GENERATED_BODY()

public:
    AChatSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== NACHRICHTEN SENDEN ==========

    UFUNCTION(BlueprintCallable, Category = "Chat|Send")
    void SendMessage(const FString& SenderID, EChatChannel Channel, const FString& Message, const FString& ReceiverID = "");

    UFUNCTION(BlueprintCallable, Category = "Chat|Send")
    void SendSystemMessage(EChatChannel Channel, const FString& Message, EMessageType Type = EMessageType::MT_System);

    UFUNCTION(BlueprintCallable, Category = "Chat|Send")
    void SendWhisper(const FString& SenderID, const FString& ReceiverID, const FString& Message);

    UFUNCTION(BlueprintCallable, Category = "Chat|Send")
    void BroadcastToChannel(EChatChannel Channel, const FString& Message, EMessageType Type = EMessageType::MT_Normal);

    // ========== NACHRICHTEN EMPFANGEN ==========

    UFUNCTION(BlueprintPure, Category = "Chat|Receive")
    TArray<FChatMessage> GetMessages(const FString& PlayerID, EChatChannel Channel) const;

    UFUNCTION(BlueprintPure, Category = "Chat|Receive")
    TArray<FChatMessage> GetRecentMessages(const FString& PlayerID, int32 Count = 50) const;

    UFUNCTION(BlueprintPure, Category = "Chat|Receive")
    TArray<FChatMessage> GetUnreadMessages(const FString& PlayerID) const;

    UFUNCTION(BlueprintCallable, Category = "Chat|Receive")
    void MarkAsRead(const FString& PlayerID, const FString& MessageID);

    // ========== KANAL-MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Chat|Channels")
    void JoinChannel(const FString& PlayerID, EChatChannel Channel);

    UFUNCTION(BlueprintCallable, Category = "Chat|Channels")
    void LeaveChannel(const FString& PlayerID, EChatChannel Channel);

    UFUNCTION(BlueprintPure, Category = "Chat|Channels")
    TArray<EChatChannel> GetJoinedChannels(const FString& PlayerID) const;

    UFUNCTION(BlueprintCallable, Category = "Chat|Channels")
    void MuteChannel(const FString& PlayerID, EChatChannel Channel);

    UFUNCTION(BlueprintCallable, Category = "Chat|Channels")
    void UnmuteChannel(const FString& PlayerID, EChatChannel Channel);

    // ========== FILTER ==========

    UFUNCTION(BlueprintCallable, Category = "Chat|Filter")
    FString FilterMessage(const FString& Message, const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Chat|Filter")
    bool IsSpam(const FString& PlayerID) const;

    UFUNCTION(BlueprintCallable, Category = "Chat|Filter")
    void ReportMessage(const FString& ReporterID, const FString& MessageID, const FString& Reason);

    // ========== EMOTES ==========

    UFUNCTION(BlueprintCallable, Category = "Chat|Emotes")
    void PlayEmote(const FString& PlayerID, const FString& EmoteCommand, AActor* Target = nullptr);

    UFUNCTION(BlueprintPure, Category = "Chat|Emotes")
    TArray<FEmote> GetAvailableEmotes() const { return AvailableEmotes; }

    UFUNCTION(BlueprintPure, Category = "Chat|Emotes")
    FEmote GetEmoteByCommand(const FString& Command) const;

    // ========== BLOCKING ==========

    UFUNCTION(BlueprintCallable, Category = "Chat|Blocking")
    void BlockPlayer(const FString& PlayerID, const FString& BlockedPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Chat|Blocking")
    void UnblockPlayer(const FString& PlayerID, const FString& BlockedPlayerID);

    UFUNCTION(BlueprintPure, Category = "Chat|Blocking")
    bool IsPlayerBlocked(const FString& PlayerID, const FString& BlockedPlayerID) const;

    // ========== HISTORY ==========

    UFUNCTION(BlueprintCallable, Category = "Chat|History")
    void ClearHistory(const FString& PlayerID, EChatChannel Channel);

    UFUNCTION(BlueprintCallable, Category = "Chat|History")
    void ClearAllHistory(const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Chat|History")
    int32 GetMessageCount(const FString& PlayerID, EChatChannel Channel) const;

    // ========== COMMANDS ==========

    UFUNCTION(BlueprintCallable, Category = "Chat|Commands")
    void ParseCommand(const FString& PlayerID, const FString& Command);

    UFUNCTION(BlueprintCallable, Category = "Chat|Commands")
    void RegisterCommand(const FString& Command, const FString& Description);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMessageReceived, FString, PlayerID, FChatMessage, Message);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnWhisperReceived, FString, FromPlayerID, FString, ToPlayerID, FString, Message);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnEmotePlayed, FString, PlayerID, FString, EmoteID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPlayerMentioned, FString, MentionedPlayerID, FChatMessage, Message);

    UPROPERTY(BlueprintAssignable, Category = "Chat|Events")
    FOnMessageReceived OnMessageReceived;

    UPROPERTY(BlueprintAssignable, Category = "Chat|Events")
    FOnWhisperReceived OnWhisperReceived;

    UPROPERTY(BlueprintAssignable, Category = "Chat|Events")
    FOnEmotePlayed OnEmotePlayed;

    UPROPERTY(BlueprintAssignable, Category = "Chat|Events")
    FOnPlayerMentioned OnPlayerMentioned;

protected:
    // ========== KONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chat|Config")
    FChatFilter Filter;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chat|Config")
    int32 MaxMessageLength = 256;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chat|Config")
    int32 MaxHistoryPerChannel = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chat|Config")
    float SayRange = 1000.0f;  // 10 Meter

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chat|Config")
    float YellRange = 5000.0f;  // 50 Meter

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chat|Config")
    TArray<FEmote> AvailableEmotes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chat|Config")
    TMap<EChatChannel, FLinearColor> ChannelColors;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Chat|State")
    TMap<FString, TArray<FChatMessage>> PlayerMessages;  // PlayerID -> Messages

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Chat|State")
    TMap<FString, TArray<EChatChannel>> PlayerChannels;  // PlayerID -> Joined Channels

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Chat|State")
    TMap<FString, TArray<FString>> BlockedPlayers;  // PlayerID -> Blocked PlayerIDs

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Chat|State")
    TMap<FString, FDateTime> LastMessageTime;  // PlayerID -> Last Message Time (Anti-Spam)

private:
    // ========== HELPER FUNCTIONS ==========

    void AddMessageToHistory(const FString& PlayerID, const FChatMessage& Message);
    bool CheckSpamProtection(const FString& PlayerID);
    void ProcessMentions(FChatMessage& Message);
    FString GenerateMessageID() const;
    void NotifyMentionedPlayers(const FChatMessage& Message);
};
