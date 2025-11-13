// FriendSystem.h
// Vollständiges Freunde-System mit Online-Status, Einladungen, Favoriten

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "FriendSystem.generated.h"

// Freundschafts-Status
UENUM(BlueprintType)
enum class EFriendshipStatus : uint8
{
    FS_None UMETA(DisplayName = "Keine Beziehung"),
    FS_RequestSent UMETA(DisplayName = "Anfrage gesendet"),
    FS_RequestReceived UMETA(DisplayName = "Anfrage erhalten"),
    FS_Friends UMETA(DisplayName = "Freunde"),
    FS_BestFriends UMETA(DisplayName = "Beste Freunde"),
    FS_Blocked UMETA(DisplayName = "Blockiert")
};

// Online-Status
UENUM(BlueprintType)
enum class EOnlineStatus : uint8
{
    OS_Offline UMETA(DisplayName = "Offline"),
    OS_Online UMETA(DisplayName = "Online"),
    OS_Away UMETA(DisplayName = "Abwesend"),
    OS_Busy UMETA(DisplayName = "Beschäftigt"),
    OS_InCombat UMETA(DisplayName = "Im Kampf"),
    OS_InDungeon UMETA(DisplayName = "In Dungeon"),
    OS_Trading UMETA(DisplayName = "Handelt")
};

// Freundes-Daten
USTRUCT(BlueprintType)
struct FFriendData
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString PlayerName;

    UPROPERTY(BlueprintReadWrite)
    int32 Level = 1;

    UPROPERTY(BlueprintReadWrite)
    EOnlineStatus OnlineStatus = EOnlineStatus::OS_Offline;

    UPROPERTY(BlueprintReadWrite)
    EFriendshipStatus RelationshipStatus = EFriendshipStatus::FS_None;

    UPROPERTY(BlueprintReadWrite)
    FDateTime FriendsSince;

    UPROPERTY(BlueprintReadWrite)
    FDateTime LastOnline;

    UPROPERTY(BlueprintReadWrite)
    FString CurrentActivity;  // "In Party", "Fishing", etc.

    UPROPERTY(BlueprintReadWrite)
    FString PersonalNote;  // Private Notiz über Freund

    UPROPERTY(BlueprintReadWrite)
    bool bIsFavorite = false;

    UPROPERTY(BlueprintReadWrite)
    bool bAllowPartyInvites = true;

    UPROPERTY(BlueprintReadWrite)
    bool bAllowWhispers = true;

    bool IsOnline() const { return OnlineStatus != EOnlineStatus::OS_Offline; }
};

// Freundschafts-Anfrage
USTRUCT(BlueprintType)
struct FFriendRequest
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString RequestID;

    UPROPERTY(BlueprintReadWrite)
    FString FromPlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString FromPlayerName;

    UPROPERTY(BlueprintReadWrite)
    FString ToPlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString Message;  // Optional message

    UPROPERTY(BlueprintReadWrite)
    FDateTime SentTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime ExpiryTime;

    bool IsExpired() const { return FDateTime::Now() > ExpiryTime; }
};

UCLASS()
class NAJIKATEST_API AFriendSystem : public AActor
{
    GENERATED_BODY()

public:
    AFriendSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== FREUNDSCHAFTS-ANFRAGEN ==========

    UFUNCTION(BlueprintCallable, Category = "Friends|Requests")
    void SendFriendRequest(const FString& FromPlayerID, const FString& ToPlayerID, const FString& Message = "");

    UFUNCTION(BlueprintCallable, Category = "Friends|Requests")
    void AcceptFriendRequest(const FString& PlayerID, const FString& RequestID);

    UFUNCTION(BlueprintCallable, Category = "Friends|Requests")
    void DeclineFriendRequest(const FString& PlayerID, const FString& RequestID);

    UFUNCTION(BlueprintCallable, Category = "Friends|Requests")
    void CancelFriendRequest(const FString& RequestID);

    UFUNCTION(BlueprintPure, Category = "Friends|Requests")
    TArray<FFriendRequest> GetPendingRequests(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Requests")
    int32 GetPendingRequestCount(const FString& PlayerID) const;

    // ========== FREUNDE VERWALTEN ==========

    UFUNCTION(BlueprintCallable, Category = "Friends|Management")
    void RemoveFriend(const FString& PlayerID, const FString& FriendID);

    UFUNCTION(BlueprintCallable, Category = "Friends|Management")
    void BlockPlayer(const FString& PlayerID, const FString& BlockedPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Friends|Management")
    void UnblockPlayer(const FString& PlayerID, const FString& BlockedPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Friends|Management")
    void SetFavorite(const FString& PlayerID, const FString& FriendID, bool bIsFavorite);

    UFUNCTION(BlueprintCallable, Category = "Friends|Management")
    void SetPersonalNote(const FString& PlayerID, const FString& FriendID, const FString& Note);

    // ========== FREUNDE ABFRAGEN ==========

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    TArray<FFriendData> GetFriendsList(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    TArray<FFriendData> GetOnlineFriends(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    TArray<FFriendData> GetFavoriteFriends(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    FFriendData GetFriend(const FString& PlayerID, const FString& FriendID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    bool IsFriend(const FString& PlayerID, const FString& OtherPlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    bool IsBlocked(const FString& PlayerID, const FString& OtherPlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    int32 GetFriendCount(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Query")
    int32 GetOnlineFriendCount(const FString& PlayerID) const;

    // ========== ONLINE-STATUS ==========

    UFUNCTION(BlueprintCallable, Category = "Friends|Status")
    void SetOnlineStatus(const FString& PlayerID, EOnlineStatus Status);

    UFUNCTION(BlueprintCallable, Category = "Friends|Status")
    void SetActivity(const FString& PlayerID, const FString& Activity);

    UFUNCTION(BlueprintPure, Category = "Friends|Status")
    EOnlineStatus GetOnlineStatus(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Friends|Status")
    FString GetActivity(const FString& PlayerID) const;

    UFUNCTION(BlueprintCallable, Category = "Friends|Status")
    void UpdatePlayerLevel(const FString& PlayerID, int32 NewLevel);

    // ========== EINSTELLUNGEN ==========

    UFUNCTION(BlueprintCallable, Category = "Friends|Settings")
    void SetAllowPartyInvites(const FString& PlayerID, const FString& FriendID, bool bAllow);

    UFUNCTION(BlueprintCallable, Category = "Friends|Settings")
    void SetAllowWhispers(const FString& PlayerID, const FString& FriendID, bool bAllow);

    // ========== SUCHE ==========

    UFUNCTION(BlueprintPure, Category = "Friends|Search")
    TArray<FFriendData> SearchFriends(const FString& PlayerID, const FString& SearchTerm) const;

    UFUNCTION(BlueprintCallable, Category = "Friends|Search")
    void FindPlayerByName(const FString& PlayerName);

    // ========== EMPFEHLUNGEN ==========

    UFUNCTION(BlueprintPure, Category = "Friends|Recommendations")
    TArray<FString> GetFriendRecommendations(const FString& PlayerID) const;  // Mutual friends, guild members, etc.

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnFriendRequestReceived, FString, PlayerID, FFriendRequest, Request);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnFriendAdded, FString, PlayerID, FString, FriendID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnFriendRemoved, FString, PlayerID, FString, FriendID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnFriendOnline, FString, PlayerID, FString, FriendID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnFriendOffline, FString, PlayerID, FString, FriendID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnFriendStatusChanged, FString, PlayerID, FString, FriendID, EOnlineStatus, NewStatus);

    UPROPERTY(BlueprintAssignable, Category = "Friends|Events")
    FOnFriendRequestReceived OnFriendRequestReceived;

    UPROPERTY(BlueprintAssignable, Category = "Friends|Events")
    FOnFriendAdded OnFriendAdded;

    UPROPERTY(BlueprintAssignable, Category = "Friends|Events")
    FOnFriendRemoved OnFriendRemoved;

    UPROPERTY(BlueprintAssignable, Category = "Friends|Events")
    FOnFriendOnline OnFriendOnline;

    UPROPERTY(BlueprintAssignable, Category = "Friends|Events")
    FOnFriendOffline OnFriendOffline;

    UPROPERTY(BlueprintAssignable, Category = "Friends|Events")
    FOnFriendStatusChanged OnFriendStatusChanged;

protected:
    // ========== KONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Friends|Config")
    int32 MaxFriends = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Friends|Config")
    float RequestExpiryDays = 7.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Friends|Config")
    bool bNotifyOnFriendOnline = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Friends|Config")
    bool bShowOnlineStatus = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Friends|Config")
    float AutoAwayMinutes = 5.0f;  // Auto-away nach 5 Minuten

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Friends|State")
    TMap<FString, TArray<FFriendData>> PlayerFriends;  // PlayerID -> Friends

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Friends|State")
    TArray<FFriendRequest> PendingRequests;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Friends|State")
    TMap<FString, EOnlineStatus> PlayerStatus;  // PlayerID -> Status

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Friends|State")
    TMap<FString, FString> PlayerActivity;  // PlayerID -> Activity

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Friends|State")
    TMap<FString, FDateTime> LastActivityTime;  // For auto-away

private:
    // ========== HELPER FUNCTIONS ==========

    void AddFriendship(const FString& PlayerID1, const FString& PlayerID2);
    void RemoveFriendship(const FString& PlayerID1, const FString& PlayerID2);
    FString GenerateRequestID() const;
    void CleanupExpiredRequests();
    void NotifyFriends(const FString& PlayerID, EOnlineStatus NewStatus);
    void CheckAutoAway();
};
