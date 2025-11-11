// BackendConnector.h
// Backend Integration: secure-hub (5010) + game-core (7010)
// Zero-Trust: Services bind ONLY to 127.0.0.1!

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Http.h"
#include "BackendConnector.generated.h"

// API Response
USTRUCT(BlueprintType)
struct FAPIResponse
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    bool bSuccess = false;

    UPROPERTY(BlueprintReadWrite)
    int32 StatusCode = 0;

    UPROPERTY(BlueprintReadWrite)
    FString ResponseBody;

    UPROPERTY(BlueprintReadWrite)
    FString ErrorMessage;
};

// Slime Registration Data
USTRUCT(BlueprintType)
struct FSlimeRegistrationData
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString SlimeName;

    UPROPERTY(BlueprintReadWrite)
    int32 Level;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> Moves;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, float> Stats;
};

// Player Stats for Backend
USTRUCT(BlueprintType)
struct FPlayerBackendStats
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    int32 Level;

    UPROPERTY(BlueprintReadWrite)
    int32 TotalPlayTime;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, int32> Achievements;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> UnlockedContent;
};

UCLASS()
class NAJIKATEST_API ABackendConnector : public AActor
{
    GENERATED_BODY()

public:
    ABackendConnector();

protected:
    virtual void BeginPlay() override;

public:
    // ========== SECURE-HUB (Port 5010) ==========

    // Health Check
    UFUNCTION(BlueprintCallable, Category = "Backend|SecureHub")
    void CheckHealth();

    // QR Code Generation
    UFUNCTION(BlueprintCallable, Category = "Backend|SecureHub")
    void GenerateQRCode(const FString& Data);

    // Vault Access
    UFUNCTION(BlueprintCallable, Category = "Backend|SecureHub")
    void AccessVault(const FString& VaultKey);

    // Push Notifications
    UFUNCTION(BlueprintCallable, Category = "Backend|SecureHub")
    void SendPushNotification(const FString& Title, const FString& Message);

    // ========== GAME-CORE (Port 7010) ==========

    // Assets
    UFUNCTION(BlueprintCallable, Category = "Backend|GameCore")
    void FetchAssets();

    // Oregon Events
    UFUNCTION(BlueprintCallable, Category = "Backend|GameCore")
    void FetchOregonEvent();

    UFUNCTION(BlueprintCallable, Category = "Backend|GameCore")
    void SubmitEventChoice(const FString& EventID, const FString& Choice);

    // Combat Data
    UFUNCTION(BlueprintCallable, Category = "Backend|GameCore")
    void SubmitCombatStats(const TMap<FString, float>& Stats);

    // ========== SLIME ARENA API ==========

    // POST /api/slime/register
    UFUNCTION(BlueprintCallable, Category = "Backend|SlimeArena")
    void RegisterSlime(const FSlimeRegistrationData& SlimeData);

    // POST /api/slime/duel
    UFUNCTION(BlueprintCallable, Category = "Backend|SlimeArena")
    void RequestDuel(const FString& SlimeID, const FString& OpponentID);

    // GET /api/slime/meta
    UFUNCTION(BlueprintCallable, Category = "Backend|SlimeArena")
    void FetchSlimeMetaData();

    // ========== PLAYER DATA ==========

    UFUNCTION(BlueprintCallable, Category = "Backend|Player")
    void SyncPlayerData(const FPlayerBackendStats& PlayerStats);

    UFUNCTION(BlueprintCallable, Category = "Backend|Player")
    void FetchPlayerData(const FString& PlayerID);

    // ========== CONNECTION ==========

    UFUNCTION(BlueprintPure, Category = "Backend|Connection")
    bool IsConnected() const { return bIsConnected; }

    UFUNCTION(BlueprintCallable, Category = "Backend|Connection")
    void TestConnection();

    UFUNCTION(BlueprintPure, Category = "Backend|Connection")
    FString GetSecureHubURL() const { return SecureHubURL; }

    UFUNCTION(BlueprintPure, Category = "Backend|Connection")
    FString GetGameCoreURL() const { return GameCoreURL; }

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAPIResponse, FAPIResponse, Response);

    UPROPERTY(BlueprintAssignable, Category = "Backend|Events")
    FOnAPIResponse OnHealthCheckComplete;

    UPROPERTY(BlueprintAssignable, Category = "Backend|Events")
    FOnAPIResponse OnQRCodeGenerated;

    UPROPERTY(BlueprintAssignable, Category = "Backend|Events")
    FOnAPIResponse OnSlimeRegistered;

    UPROPERTY(BlueprintAssignable, Category = "Backend|Events")
    FOnAPIResponse OnDuelRequested;

    UPROPERTY(BlueprintAssignable, Category = "Backend|Events")
    FOnAPIResponse OnEventFetched;

protected:
    // ========== CONFIGURATION ==========

    // Zero-Trust: ONLY 127.0.0.1!
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Backend|Config")
    FString SecureHubURL = "http://127.0.0.1:5010";

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Backend|Config")
    FString GameCoreURL = "http://127.0.0.1:7010";

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Backend|Config")
    FString OwnerToken = "";  // X-OWNER-TOKEN for admin routes

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Backend|Config")
    float RequestTimeout = 10.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Backend|Config")
    bool bUseOwnerGate = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Backend|State")
    bool bIsConnected = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Backend|State")
    float LastPingTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Backend|State")
    int32 FailedRequestCount = 0;

private:
    // ========== HTTP HELPERS ==========

    void SendRequest(const FString& URL, const FString& Verb, const FString& Payload, TFunction<void(FAPIResponse)> Callback);

    void OnResponseReceived(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, TFunction<void(FAPIResponse)> Callback);

    FString BuildURL(const FString& BaseURL, const FString& Endpoint) const;

    TSharedRef<IHttpRequest> CreateRequest(const FString& URL, const FString& Verb, const FString& Payload);

    // ========== HTTP MODULE ==========

    FHttpModule* HttpModule;
};
