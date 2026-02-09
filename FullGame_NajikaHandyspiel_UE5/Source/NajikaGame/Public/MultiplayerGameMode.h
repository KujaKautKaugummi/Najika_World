// MultiplayerGameMode.h
// Online Multiplayer Game Mode for Najika Handyspiel
// Supports: Dedicated Server, Peer-to-Peer, Matchmaking

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "MultiplayerGameMode.generated.h"

// Server Type
UENUM(BlueprintType)
enum class EServerType : uint8
{
    ST_Dedicated UMETA(DisplayName = "Dedicated Server"),
    ST_ListenServer UMETA(DisplayName = "Listen Server (P2P)"),
    ST_Standalone UMETA(DisplayName = "Single Player")
};

// Match State
UENUM(BlueprintType)
enum class EMatchState : uint8
{
    MS_Lobby UMETA(DisplayName = "Lobby"),
    MS_Starting UMETA(DisplayName = "Starting"),
    MS_InProgress UMETA(DisplayName = "In Progress"),
    MS_Ending UMETA(DisplayName = "Ending"),
    MS_Finished UMETA(DisplayName = "Finished")
};

// Player Session Data
USTRUCT(BlueprintType)
struct FPlayerSessionData
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString PlayerName;

    UPROPERTY(BlueprintReadWrite)
    int32 Level;

    UPROPERTY(BlueprintReadWrite)
    int32 Ping;

    UPROPERTY(BlueprintReadWrite)
    bool bIsReady;

    UPROPERTY(BlueprintReadWrite)
    FDateTime JoinTime;
};

UCLASS()
class NAJIKAGAME_API AMultiplayerGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    AMultiplayerGameMode();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

    // ========== PLAYER MANAGEMENT ==========

    virtual void PostLogin(APlayerController* NewPlayer) override;
    virtual void Logout(AController* Exiting) override;

    UFUNCTION(BlueprintCallable, Category = "Multiplayer|Players")
    int32 GetPlayerCount() const;

    UFUNCTION(BlueprintPure, Category = "Multiplayer|Players")
    TArray<FPlayerSessionData> GetActivePlayers() const { return ActivePlayers; }

    // ========== MATCH MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Multiplayer|Match")
    void StartMatch();

    UFUNCTION(BlueprintCallable, Category = "Multiplayer|Match")
    void EndMatch();

    UFUNCTION(BlueprintPure, Category = "Multiplayer|Match")
    EMatchState GetMatchState() const { return CurrentMatchState; }

    // ========== SERVER SETTINGS ==========

    UFUNCTION(BlueprintPure, Category = "Multiplayer|Server")
    EServerType GetServerType() const { return ServerType; }

    UFUNCTION(BlueprintPure, Category = "Multiplayer|Server")
    int32 GetMaxPlayers() const { return MaxPlayers; }

    UFUNCTION(BlueprintCallable, Category = "Multiplayer|Server")
    void SetMaxPlayers(int32 NewMax);

    // ========== MATCHMAKING ==========

    UFUNCTION(BlueprintCallable, Category = "Multiplayer|Matchmaking")
    void FindMatch(int32 PreferredPlayerCount);

    UFUNCTION(BlueprintCallable, Category = "Multiplayer|Matchmaking")
    void CancelMatchmaking();

    // ========== VOICE CHAT ==========

    UFUNCTION(BlueprintCallable, Category = "Multiplayer|Voice")
    void EnableVoiceChat(bool bEnable);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPlayerJoined, FPlayerSessionData, PlayerData);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPlayerLeft, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnMatchStarted);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnMatchEnded);

    UPROPERTY(BlueprintAssignable, Category = "Multiplayer|Events")
    FOnPlayerJoined OnPlayerJoined;

    UPROPERTY(BlueprintAssignable, Category = "Multiplayer|Events")
    FOnPlayerLeft OnPlayerLeft;

    UPROPERTY(BlueprintAssignable, Category = "Multiplayer|Events")
    FOnMatchStarted OnMatchStarted;

    UPROPERTY(BlueprintAssignable, Category = "Multiplayer|Events")
    FOnMatchEnded OnMatchEnded;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Multiplayer|Config")
    EServerType ServerType = EServerType::ST_Dedicated;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Multiplayer|Config")
    int32 MaxPlayers = 50;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Multiplayer|Config")
    int32 MinPlayersToStart = 2;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Multiplayer|Config")
    float MatchDuration = 3600.0f;  // 1 hour

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Multiplayer|Config")
    bool bEnableVoiceChat = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Multiplayer|Config")
    bool bEnableCrossPlay = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Multiplayer|State")
    EMatchState CurrentMatchState = EMatchState::MS_Lobby;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Multiplayer|State")
    TArray<FPlayerSessionData> ActivePlayers;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Multiplayer|State")
    float MatchTimer = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Multiplayer|State")
    int32 ReadyPlayerCount = 0;

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateMatchTimer(float DeltaTime);
    void CheckStartConditions();
    void BroadcastPlayerJoined(const FPlayerSessionData& PlayerData);
    void BroadcastPlayerLeft(const FString& PlayerID);
};
