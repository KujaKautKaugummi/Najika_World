// DungeonSystem.h
// Vollständiges Dungeon/Instanz-System mit Schwierigkeitsgraden, Checkpoints, Bestenlisten

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "DungeonSystem.generated.h"

// Dungeon-Typ
UENUM(BlueprintType)
enum class EDungeonType : uint8
{
    DT_Solo UMETA(DisplayName = "Solo"),
    DT_Party UMETA(DisplayName = "Party (2-5 Spieler)"),
    DT_Raid UMETA(DisplayName = "Raid (6-20 Spieler)"),
    DT_PvP UMETA(DisplayName = "PvP"),
    DT_Endless UMETA(DisplayName = "Endlos")
};

// Dungeon-Schwierigkeit
UENUM(BlueprintType)
enum class EDungeonDifficulty : uint8
{
    DD_Normal UMETA(DisplayName = "Normal"),
    DD_Hard UMETA(DisplayName = "Schwer"),
    DD_Heroic UMETA(DisplayName = "Heroisch"),
    DD_Mythic UMETA(DisplayName = "Mythisch"),
    DD_MythicPlus UMETA(DisplayName = "Mythisch+")
};

// Dungeon-Status
UENUM(BlueprintType)
enum class EDungeonStatus : uint8
{
    DS_NotStarted UMETA(DisplayName = "Nicht gestartet"),
    DS_InProgress UMETA(DisplayName = "Läuft"),
    DS_Paused UMETA(DisplayName = "Pausiert"),
    DS_Completed UMETA(DisplayName = "Abgeschlossen"),
    DS_Failed UMETA(DisplayName = "Fehlgeschlagen"),
    DS_Abandoned UMETA(DisplayName = "Abgebrochen")
};

// Checkpoint
USTRUCT(BlueprintType)
struct FDungeonCheckpoint
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString CheckpointID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString CheckpointName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector RespawnLocation;

    UPROPERTY(BlueprintReadWrite)
    bool bActivated = false;

    UPROPERTY(BlueprintReadWrite)
    FDateTime ActivatedTime;
};

// Boss-Encounter
USTRUCT(BlueprintType)
struct FBossEncounter
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BossID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BossName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSubclassOf<AActor> BossClass;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector SpawnLocation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, int32> LootTable;  // ItemID -> Drop chance %

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 BaseXP = 1000;

    UPROPERTY(BlueprintReadWrite)
    bool bDefeated = false;

    UPROPERTY(BlueprintReadWrite)
    FDateTime DefeatTime;

    UPROPERTY(BlueprintReadWrite)
    float BestTime = 0.0f;  // Rekordzeit
};

// Dungeon-Daten
USTRUCT(BlueprintType)
struct FDungeon
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString DungeonID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString DungeonName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EDungeonType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<EDungeonDifficulty> AvailableDifficulties;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinPlayers = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxPlayers = 5;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RecommendedLevel = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float TimeLimit = 3600.0f;  // 1 Stunde

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FDungeonCheckpoint> Checkpoints;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FBossEncounter> Bosses;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString MapName;  // Level to load

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxDeaths = 0;  // 0 = unlimited

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bAllowRespawn = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bHasLeaderboard = true;
};

// Dungeon-Instanz
USTRUCT(BlueprintType)
struct FDungeonInstance
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString InstanceID;

    UPROPERTY(BlueprintReadWrite)
    FString DungeonID;

    UPROPERTY(BlueprintReadWrite)
    EDungeonDifficulty Difficulty;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> PartyMemberIDs;

    UPROPERTY(BlueprintReadWrite)
    FString LeaderID;

    UPROPERTY(BlueprintReadWrite)
    EDungeonStatus Status = EDungeonStatus::DS_NotStarted;

    UPROPERTY(BlueprintReadWrite)
    FDateTime StartTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime EndTime;

    UPROPERTY(BlueprintReadWrite)
    float ElapsedTime = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentCheckpointIndex = 0;

    UPROPERTY(BlueprintReadWrite)
    TArray<int32> DefeatedBossIndices;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, int32> PlayerDeaths;  // PlayerID -> Death count

    UPROPERTY(BlueprintReadWrite)
    int32 TotalScore = 0;

    bool IsComplete() const { return Status == EDungeonStatus::DS_Completed; }
    bool IsActive() const { return Status == EDungeonStatus::DS_InProgress; }
};

// Leaderboard-Eintrag
USTRUCT(BlueprintType)
struct FDungeonLeaderboardEntry
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    int32 Rank;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> PartyMemberNames;

    UPROPERTY(BlueprintReadWrite)
    float CompletionTime;

    UPROPERTY(BlueprintReadWrite)
    int32 Score;

    UPROPERTY(BlueprintReadWrite)
    FDateTime DateAchieved;
};

UCLASS()
class NAJIKATEST_API ADungeonSystem : public AActor
{
    GENERATED_BODY()

public:
    ADungeonSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== INSTANZ-ERSTELLUNG ==========

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Instance")
    FString CreateInstance(const FString& DungeonID, EDungeonDifficulty Difficulty, const TArray<FString>& PartyMemberIDs);

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Instance")
    void StartInstance(const FString& InstanceID);

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Instance")
    void EndInstance(const FString& InstanceID, bool bSuccess);

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Instance")
    void AbandonInstance(const FString& InstanceID);

    UFUNCTION(BlueprintPure, Category = "Dungeon|Instance")
    FDungeonInstance GetInstance(const FString& InstanceID) const;

    // ========== PROGRESSION ==========

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Progression")
    void ActivateCheckpoint(const FString& InstanceID, int32 CheckpointIndex);

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Progression")
    void DefeatBoss(const FString& InstanceID, int32 BossIndex);

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Progression")
    void RecordPlayerDeath(const FString& InstanceID, const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Dungeon|Progression")
    int32 GetPlayerDeaths(const FString& InstanceID, const FString& PlayerID) const;

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Progression")
    void AddScore(const FString& InstanceID, int32 Score);

    // ========== RESPAWN ==========

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Respawn")
    FVector GetRespawnLocation(const FString& InstanceID) const;

    UFUNCTION(BlueprintPure, Category = "Dungeon|Respawn")
    bool CanRespawn(const FString& InstanceID, const FString& PlayerID) const;

    // ========== LEADERBOARD ==========

    UFUNCTION(BlueprintPure, Category = "Dungeon|Leaderboard")
    TArray<FDungeonLeaderboardEntry> GetLeaderboard(const FString& DungeonID, EDungeonDifficulty Difficulty, int32 TopCount = 10) const;

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Leaderboard")
    void SubmitScore(const FString& InstanceID);

    UFUNCTION(BlueprintPure, Category = "Dungeon|Leaderboard")
    int32 GetPlayerRank(const FString& DungeonID, const FString& PlayerID, EDungeonDifficulty Difficulty) const;

    // ========== QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "Dungeon|Query")
    FDungeon GetDungeon(const FString& DungeonID) const;

    UFUNCTION(BlueprintPure, Category = "Dungeon|Query")
    TArray<FDungeon> GetAvailableDungeons(int32 PlayerLevel) const;

    UFUNCTION(BlueprintPure, Category = "Dungeon|Query")
    FString GetPlayerInstance(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Dungeon|Query")
    bool IsPlayerInDungeon(const FString& PlayerID) const;

    // ========== MATCHMAKING ==========

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Matchmaking")
    void QueueForDungeon(const FString& PlayerID, const FString& DungeonID, EDungeonDifficulty Difficulty);

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Matchmaking")
    void LeaveQueue(const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Dungeon|Matchmaking")
    bool IsInQueue(const FString& PlayerID) const;

    // ========== DUNGEON-CREATION ==========

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Creation")
    void RegisterDungeon(const FDungeon& Dungeon);

    UFUNCTION(BlueprintCallable, Category = "Dungeon|Creation")
    void UnregisterDungeon(const FString& DungeonID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnInstanceCreated, FString, InstanceID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnInstanceStarted, FString, InstanceID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnInstanceCompleted, FString, InstanceID, bool, bSuccess);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnCheckpointReached, FString, InstanceID, int32, CheckpointIndex);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnBossDefeated, FString, InstanceID, FString, BossID);

    UPROPERTY(BlueprintAssignable, Category = "Dungeon|Events")
    FOnInstanceCreated OnInstanceCreated;

    UPROPERTY(BlueprintAssignable, Category = "Dungeon|Events")
    FOnInstanceStarted OnInstanceStarted;

    UPROPERTY(BlueprintAssignable, Category = "Dungeon|Events")
    FOnInstanceCompleted OnInstanceCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Dungeon|Events")
    FOnCheckpointReached OnCheckpointReached;

    UPROPERTY(BlueprintAssignable, Category = "Dungeon|Events")
    FOnBossDefeated OnBossDefeated;

protected:
    // ========== KONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dungeon|Config")
    TMap<FString, FDungeon> RegisteredDungeons;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dungeon|Config")
    float InstanceCleanupDelay = 300.0f;  // 5 Minuten nach Ende

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dungeon|Config")
    bool bAutoMatchmaking = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dungeon|State")
    TMap<FString, FDungeonInstance> ActiveInstances;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dungeon|State")
    TMap<FString, FString> PlayerToInstance;  // PlayerID -> InstanceID

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dungeon|State")
    TMap<FString, TArray<FDungeonLeaderboardEntry>> Leaderboards;  // DungeonID+Difficulty -> Entries

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dungeon|State")
    TArray<FString> MatchmakingQueue;

private:
    // ========== HELPER FUNCTIONS ==========

    FString GenerateInstanceID() const;
    void ProcessMatchmaking();
    void CleanupFinishedInstances();
    int32 CalculateFinalScore(const FDungeonInstance& Instance) const;
};
