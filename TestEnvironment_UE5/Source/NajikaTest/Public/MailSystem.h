// MailSystem.h
// Complete Mail/Messaging System for player communication and item transfers

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MailSystem.generated.h"

// Mail Type
UENUM(BlueprintType)
enum class EMailType : uint8
{
    MT_PlayerMail UMETA(DisplayName = "Player Mail"),
    MT_SystemMail UMETA(DisplayName = "System Mail"),
    MT_GuildMail UMETA(DisplayName = "Guild Mail"),
    MT_QuestReward UMETA(DisplayName = "Quest Reward"),
    MT_AuctionResult UMETA(DisplayName = "Auction Result"),
    MT_AdminMessage UMETA(DisplayName = "Admin Message")
};

// Mail Priority
UENUM(BlueprintType)
enum class EMailPriority : uint8
{
    MP_Normal UMETA(DisplayName = "Normal"),
    MP_Important UMETA(DisplayName = "Important"),
    MP_Urgent UMETA(DisplayName = "Urgent")
};

// Mail Attachment
USTRUCT(BlueprintType)
struct FMailAttachment
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString ItemID;

    UPROPERTY(BlueprintReadWrite)
    int32 Quantity = 1;

    UPROPERTY(BlueprintReadWrite)
    bool bClaimed = false;
};

// Mail Message
USTRUCT(BlueprintType)
struct FMailMessage
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString MailID;

    UPROPERTY(BlueprintReadWrite)
    EMailType Type;

    UPROPERTY(BlueprintReadWrite)
    EMailPriority Priority = EMailPriority::MP_Normal;

    UPROPERTY(BlueprintReadWrite)
    FString FromPlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString FromPlayerName;

    UPROPERTY(BlueprintReadWrite)
    FString ToPlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString Subject;

    UPROPERTY(BlueprintReadWrite)
    FString Body;

    UPROPERTY(BlueprintReadWrite)
    int32 AttachedGold = 0;

    UPROPERTY(BlueprintReadWrite)
    TArray<FMailAttachment> Attachments;

    UPROPERTY(BlueprintReadWrite)
    FDateTime SentTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime ExpiryTime;  // Auto-delete after

    UPROPERTY(BlueprintReadWrite)
    bool bRead = false;

    UPROPERTY(BlueprintReadWrite)
    bool bReturned = false;

    UPROPERTY(BlueprintReadWrite)
    bool bHasAttachments = false;

    bool IsExpired() const { return FDateTime::Now() > ExpiryTime; }
    bool HasUnclaimedAttachments() const;
};

UCLASS()
class NAJIKATEST_API AMailSystem : public AActor
{
    GENERATED_BODY()

public:
    AMailSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== SENDING MAIL ==========

    UFUNCTION(BlueprintCallable, Category = "Mail|Send")
    FString SendMail(const FString& FromPlayerID, const FString& ToPlayerID, const FString& Subject, const FString& Body);

    UFUNCTION(BlueprintCallable, Category = "Mail|Send")
    void SendSystemMail(const FString& ToPlayerID, const FString& Subject, const FString& Body);

    UFUNCTION(BlueprintCallable, Category = "Mail|Send")
    void SendGuildMail(const FString& GuildID, const FString& FromPlayerID, const FString& Subject, const FString& Body);

    UFUNCTION(BlueprintCallable, Category = "Mail|Send")
    void AttachItem(const FString& MailID, const FString& ItemID, int32 Quantity);

    UFUNCTION(BlueprintCallable, Category = "Mail|Send")
    void AttachGold(const FString& MailID, int32 Gold);

    // ========== RECEIVING MAIL ==========

    UFUNCTION(BlueprintPure, Category = "Mail|Receive")
    TArray<FMailMessage> GetInbox(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Mail|Receive")
    TArray<FMailMessage> GetUnreadMail(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Mail|Receive")
    int32 GetUnreadCount(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Mail|Receive")
    FMailMessage GetMail(const FString& MailID) const;

    UFUNCTION(BlueprintCallable, Category = "Mail|Receive")
    void MarkAsRead(const FString& MailID);

    // ========== ATTACHMENTS ==========

    UFUNCTION(BlueprintCallable, Category = "Mail|Attachments")
    bool ClaimAttachments(const FString& MailID, const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "Mail|Attachments")
    bool ClaimGold(const FString& MailID, const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Mail|Attachments")
    bool HasUnclaimedAttachments(const FString& MailID) const;

    // ========== MAIL MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Mail|Management")
    void DeleteMail(const FString& MailID);

    UFUNCTION(BlueprintCallable, Category = "Mail|Management")
    void DeleteAllRead(const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "Mail|Management")
    void ReturnMail(const FString& MailID);  // Return to sender with attachments

    UFUNCTION(BlueprintCallable, Category = "Mail|Management")
    void CleanupExpiredMail();

    // ========== BLOCKING ==========

    UFUNCTION(BlueprintCallable, Category = "Mail|Blocking")
    void BlockPlayer(const FString& PlayerID, const FString& BlockedPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Mail|Blocking")
    void UnblockPlayer(const FString& PlayerID, const FString& BlockedPlayerID);

    UFUNCTION(BlueprintPure, Category = "Mail|Blocking")
    bool IsBlocked(const FString& PlayerID, const FString& BlockedPlayerID) const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMailReceived, FString, PlayerID, FMailMessage, Mail);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMailRead, FString, PlayerID, FString, MailID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAttachmentsClaimed, FString, PlayerID, FString, MailID);

    UPROPERTY(BlueprintAssignable, Category = "Mail|Events")
    FOnMailReceived OnMailReceived;

    UPROPERTY(BlueprintAssignable, Category = "Mail|Events")
    FOnMailRead OnMailRead;

    UPROPERTY(BlueprintAssignable, Category = "Mail|Events")
    FOnAttachmentsClaimed OnAttachmentsClaimed;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mail|Config")
    int32 MaxMailPerPlayer = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mail|Config")
    float DefaultExpiryDays = 30.0f;  // 30 days

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mail|Config")
    int32 MaxAttachmentsPerMail = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mail|Config")
    int32 MailSendCost = 10;  // Gold cost to send mail

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mail|Config")
    bool bAllowPlayerMail = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mail|Config")
    bool bRequireOnlineForNotification = false;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mail|State")
    TMap<FString, TArray<FMailMessage>> PlayerInboxes;  // PlayerID -> Mails

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mail|State")
    TMap<FString, TArray<FString>> BlockedPlayers;  // PlayerID -> Blocked PlayerIDs

private:
    // ========== HELPER FUNCTIONS ==========

    FString GenerateMailID() const;
    void NotifyPlayer(const FString& PlayerID, const FMailMessage& Mail);
    bool CanSendMail(const FString& FromPlayerID, const FString& ToPlayerID) const;
};
