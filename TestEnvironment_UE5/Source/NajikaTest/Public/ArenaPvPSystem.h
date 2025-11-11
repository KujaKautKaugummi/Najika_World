// ArenaPvPSystem.h
// Vollständiges PvP-Arena-System mit Ranked, Turnier-Modi, Elo-Rating

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ArenaPvPSystem.generated.h"

// Arena-Modus
UENUM(BlueprintType)
enum class EArenaMode : uint8
{
    AM_Duel UMETA(DisplayName = "1v1 Duell"),
    AM_TwoVsTwo UMETA(DisplayName = "2v2"),
    AM_ThreeVsThree UMETA(DisplayName = "3v3"),
    AM_FiveVsFive UMETA(DisplayName = "5v5"),
    AM_FreeForAll UMETA(DisplayName = "Free-for-All"),
    AM_TeamDeathmatch UMETA(DisplayName = "Team Deathmatch"),
    AM_CaptureTheFlag UMETA(DisplayName = "Capture the Flag")
};

// Match-Status
UENUM(BlueprintType)
enum class EMatchStatus : uint8
{
    MS_Waiting UMETA(DisplayName = "Warte auf Spieler"),
    MS_Preparation UMETA(DisplayName = "Vorbereitung"),
    MS_InProgress UMETA(DisplayName = "Läuft"),
    MS_Finished UMETA(DisplayName = "Beendet")
};

// Ranking-Typ
UENUM(BlueprintType)
enum class ERankingType : uint8
{
    RT_Casual UMETA(DisplayName = "Casual (Kein Rating)"),
    RT_Ranked UMETA(DisplayName = "Ranked (Elo-System)")
};

// Spieler-Rang
UENUM(BlueprintType)
enum class EPlayerRank : uint8
{
    PR_Bronze UMETA(DisplayName = "Bronze"),
    PR_Silver UMETA(DisplayName = "Silber"),
    PR_Gold UMETA(DisplayName = "Gold"),
    PR_Platinum UMETA(DisplayName = "Platin"),
    PR_Diamond UMETA(DisplayName = "Diamant"),
    PR_Master UMETA(DisplayName = "Meister"),
    PR_Grandmaster UMETA(DisplayName = "Großmeister"),
    PR_Legend UMETA(DisplayName = "Legende")
};

// Match-Statistiken
USTRUCT(BlueprintType)
struct FMatchStats
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    int32 Kills = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 Deaths = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 Assists = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 DamageDealt = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 DamageTaken = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 HealingDone = 0;

    UPROPERTY(BlueprintReadWrite)
    float SurvivalTime = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    bool bWon = false;

    float GetKDRatio() const { return Deaths > 0 ? (float)Kills / (float)Deaths : (float)Kills; }
};

// Arena-Match
USTRUCT(BlueprintType)
struct FArenaMatch
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString MatchID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EArenaMode Mode;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ERankingType RankingType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ArenaMapID;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> Team1PlayerIDs;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> Team2PlayerIDs;

    UPROPERTY(BlueprintReadWrite)
    EMatchStatus Status = EMatchStatus::MS_Waiting;

    UPROPERTY(BlueprintReadWrite)
    int32 Team1Score = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 Team2Score = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 ScoreLimit = 10;  // First to X

    UPROPERTY(BlueprintReadWrite)
    float TimeLimit = 600.0f;  // 10 Minuten

    UPROPERTY(BlueprintReadWrite)
    float ElapsedTime = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, FMatchStats> PlayerStats;

    UPROPERTY(BlueprintReadWrite)
    FDateTime StartTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime EndTime;

    bool IsFinished() const { return Status == EMatchStatus::MS_Finished; }
    int32 GetWinningTeam() const { return Team1Score > Team2Score ? 1 : 2; }
};

// Spieler-Elo-Daten
USTRUCT(BlueprintType)
struct FPlayerElo
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    int32 Elo = 1000;  // Start-Elo

    UPROPERTY(BlueprintReadWrite)
    int32 Wins = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 Losses = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 WinStreak = 0;

    UPROPERTY(BlueprintReadWrite)
    EPlayerRank Rank = EPlayerRank::PR_Bronze;

    UPROPERTY(BlueprintReadWrite)
    int32 HighestElo = 1000;

    float GetWinRate() const
    {
        int32 Total = Wins + Losses;
        return Total > 0 ? (float)Wins / (float)Total : 0.0f;
    }

    EPlayerRank CalculateRank() const;
};

UCLASS()
class NAJIKATEST_API AArenaPvPSystem : public AActor
{
    GENERATED_BODY()

public:
    AArenaPvPSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== MATCHMAKING ==========

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Matchmaking")
    void QueueForMatch(const FString& PlayerID, EArenaMode Mode, ERankingType RankingType);

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Matchmaking")
    void LeaveQueue(const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Matchmaking")
    bool IsInQueue(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Matchmaking")
    int32 GetQueueSize(EArenaMode Mode, ERankingType RankingType) const;

    // ========== MATCH-MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Match")
    FString CreateMatch(EArenaMode Mode, ERankingType RankingType, const TArray<FString>& Team1, const TArray<FString>& Team2);

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Match")
    void StartMatch(const FString& MatchID);

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Match")
    void EndMatch(const FString& MatchID);

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Match")
    void ForfeitMatch(const FString& MatchID, const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Match")
    FArenaMatch GetMatch(const FString& MatchID) const;

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Match")
    FString GetPlayerMatch(const FString& PlayerID) const;

    // ========== SCORING ==========

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Scoring")
    void RecordKill(const FString& MatchID, const FString& KillerID, const FString& VictimID, const FString& AssistID = "");

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Scoring")
    void AddTeamScore(const FString& MatchID, int32 Team, int32 Points);

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Scoring")
    void RecordDamage(const FString& MatchID, const FString& PlayerID, int32 Damage);

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Scoring")
    void RecordHealing(const FString& MatchID, const FString& PlayerID, int32 Healing);

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Scoring")
    FMatchStats GetPlayerStats(const FString& MatchID, const FString& PlayerID) const;

    // ========== ELO-SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Elo")
    void UpdateElo(const FString& MatchID);

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Elo")
    FPlayerElo GetPlayerElo(const FString& PlayerID, EArenaMode Mode) const;

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Elo")
    int32 CalculateEloChange(int32 PlayerElo, int32 OpponentElo, bool bWon) const;

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Elo")
    EPlayerRank GetPlayerRank(const FString& PlayerID, EArenaMode Mode) const;

    // ========== LEADERBOARD ==========

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Leaderboard")
    TArray<FPlayerElo> GetLeaderboard(EArenaMode Mode, int32 TopCount = 100) const;

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Leaderboard")
    int32 GetPlayerRankPosition(const FString& PlayerID, EArenaMode Mode) const;

    // ========== STATISTIKEN ==========

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Stats")
    TArray<FArenaMatch> GetPlayerMatchHistory(const FString& PlayerID, int32 Count = 10) const;

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Stats")
    int32 GetTotalMatches(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Stats")
    float GetOverallWinRate(const FString& PlayerID) const;

    // ========== BELOHNUNGEN ==========

    UFUNCTION(BlueprintCallable, Category = "ArenaPvP|Rewards")
    void DistributeMatchRewards(const FString& MatchID);

    UFUNCTION(BlueprintPure, Category = "ArenaPvP|Rewards")
    int32 CalculateReward(const FPlayerElo& PlayerData, bool bWon) const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMatchCreated, FString, MatchID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMatchStarted, FString, MatchID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMatchEnded, FString, MatchID, int32, WinningTeam);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnPlayerKill, FString, KillerID, FString, VictimID, FString, MatchID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnRankUp, FString, PlayerID, EPlayerRank, NewRank);

    UPROPERTY(BlueprintAssignable, Category = "ArenaPvP|Events")
    FOnMatchCreated OnMatchCreated;

    UPROPERTY(BlueprintAssignable, Category = "ArenaPvP|Events")
    FOnMatchStarted OnMatchStarted;

    UPROPERTY(BlueprintAssignable, Category = "ArenaPvP|Events")
    FOnMatchEnded OnMatchEnded;

    UPROPERTY(BlueprintAssignable, Category = "ArenaPvP|Events")
    FOnPlayerKill OnPlayerKill;

    UPROPERTY(BlueprintAssignable, Category = "ArenaPvP|Events")
    FOnRankUp OnRankUp;

protected:
    // ========== KONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaPvP|Config")
    int32 EloKFactor = 32;  // Elo change multiplier

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaPvP|Config")
    int32 BaseWinReward = 100;  // Gold

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaPvP|Config")
    int32 BaseLoseReward = 25;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaPvP|Config")
    float MatchmakingEloRange = 200.0f;  // +/- Elo for matchmaking

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ArenaPvP|Config")
    float PreparationTime = 30.0f;  // 30 Sekunden prep

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ArenaPvP|State")
    TMap<FString, FArenaMatch> ActiveMatches;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ArenaPvP|State")
    TMap<EArenaMode, TArray<FString>> MatchmakingQueues;  // Mode -> PlayerIDs

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ArenaPvP|State")
    TMap<FString, TMap<EArenaMode, FPlayerElo>> PlayerEloData;  // PlayerID -> (Mode -> Elo)

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "ArenaPvP|State")
    TArray<FArenaMatch> MatchHistory;

private:
    // ========== HELPER FUNCTIONS ==========

    void ProcessMatchmaking();
    FString GenerateMatchID() const;
    void CheckMatchEnd(FArenaMatch& Match);
    TArray<FString> FindMatchForPlayer(const FString& PlayerID, EArenaMode Mode, ERankingType RankingType);
    void UpdatePlayerRank(FPlayerElo& PlayerData);
};
