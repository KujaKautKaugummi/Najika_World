// WorldEventSystem.h
// Vollständiges Weltevent-System mit zeitbasierten Events, Invasionen, Bosses

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "WorldEventSystem.generated.h"

// Event-Typ
UENUM(BlueprintType)
enum class EWorldEventType : uint8
{
    WE_Invasion UMETA(DisplayName = "Monster-Invasion"),
    WE_WorldBoss UMETA(DisplayName = "Weltboss"),
    WE_Treasure UMETA(DisplayName = "Schatzjagd"),
    WE_Tournament UMETA(DisplayName = "Turnier"),
    WE_Festival UMETA(DisplayName = "Festival"),
    WE_Seasonal UMETA(DisplayName = "Saisonales Event"),
    WE_Random UMETA(DisplayName = "Zufälliges Event"),
    WE_Apocalypse UMETA(DisplayName = "Apokalypse (Endgame)")
};

// Event-Status
UENUM(BlueprintType)
enum class EEventStatus : uint8
{
    ES_Scheduled UMETA(DisplayName = "Geplant"),
    ES_Starting UMETA(DisplayName = "Startet bald"),
    ES_Active UMETA(DisplayName = "Aktiv"),
    ES_Ending UMETA(DisplayName = "Endet bald"),
    ES_Completed UMETA(DisplayName = "Abgeschlossen"),
    ES_Failed UMETA(DisplayName = "Fehlgeschlagen")
};

// Event-Schwierigkeit
UENUM(BlueprintType)
enum class EEventDifficulty : uint8
{
    ED_Easy UMETA(DisplayName = "Einfach"),
    ED_Normal UMETA(DisplayName = "Normal"),
    ED_Hard UMETA(DisplayName = "Schwer"),
    ED_Heroic UMETA(DisplayName = "Heroisch"),
    ED_Mythic UMETA(DisplayName = "Mythisch")
};

// Event-Phase
USTRUCT(BlueprintType)
struct FEventPhase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString PhaseID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString PhaseName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Duration = 300.0f;  // 5 Minuten

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> SpawnEnemyIDs;  // Feinde spawnen

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FVector> SpawnLocations;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ObjectiveText;  // "Verteidige die Stadt!"

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bSpawnBoss = false;

    UPROPERTY(BlueprintReadWrite)
    bool bCompleted = false;
};

// Weltevent-Daten
USTRUCT(BlueprintType)
struct FWorldEvent
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EventID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString EventName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EWorldEventType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EEventDifficulty Difficulty;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FEventPhase> Phases;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector EventLocation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float EventRadius = 10000.0f;  // 100 Meter Radius

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinPlayers = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxPlayers = 50;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RecommendedLevel = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, int32> Rewards;  // ItemID -> Quantity

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 GoldReward = 1000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 XPReward = 500;

    UPROPERTY(BlueprintReadWrite)
    EEventStatus Status = EEventStatus::ES_Scheduled;

    UPROPERTY(BlueprintReadWrite)
    FDateTime ScheduledStartTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime ActualStartTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime EndTime;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentPhaseIndex = 0;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> ParticipantPlayerIDs;

    UPROPERTY(BlueprintReadWrite)
    int32 Score = 0;  // Event-Score

    bool IsActive() const { return Status == EEventStatus::ES_Active; }
    bool IsScheduled() const { return Status == EEventStatus::ES_Scheduled; }
};

// Event-Belohnung
USTRUCT(BlueprintType)
struct FEventReward
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    int32 Contribution = 0;  // Beitrag zum Event

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, int32> ReceivedItems;

    UPROPERTY(BlueprintReadWrite)
    int32 ReceivedGold = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 ReceivedXP = 0;
};

UCLASS()
class NAJIKATEST_API AWorldEventSystem : public AActor
{
    GENERATED_BODY()

public:
    AWorldEventSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== EVENT-MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Management")
    void StartEvent(const FString& EventID);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Management")
    void EndEvent(const FString& EventID, bool bSuccess);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Management")
    void CancelEvent(const FString& EventID);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Management")
    void ScheduleEvent(const FString& EventID, const FDateTime& StartTime);

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Management")
    TArray<FWorldEvent> GetActiveEvents() const;

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Management")
    TArray<FWorldEvent> GetScheduledEvents() const;

    // ========== EVENT-PROGRESSION ==========

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Progression")
    void AdvancePhase(const FString& EventID);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Progression")
    void CompletePhase(const FString& EventID, int32 PhaseIndex);

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Progression")
    FEventPhase GetCurrentPhase(const FString& EventID) const;

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Progression")
    int32 GetPhaseIndex(const FString& EventID) const;

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Progression")
    void AddEventScore(const FString& EventID, int32 Score);

    // ========== TEILNAHME ==========

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Participation")
    void JoinEvent(const FString& EventID, const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Participation")
    void LeaveEvent(const FString& EventID, const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Participation")
    bool IsParticipating(const FString& EventID, const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Participation")
    int32 GetParticipantCount(const FString& EventID) const;

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Participation")
    void AddContribution(const FString& EventID, const FString& PlayerID, int32 Contribution);

    // ========== BELOHNUNGEN ==========

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Rewards")
    void DistributeRewards(const FString& EventID);

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Rewards")
    FEventReward CalculateReward(const FString& EventID, const FString& PlayerID) const;

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Rewards")
    void ClaimReward(const FString& EventID, const FString& PlayerID);

    // ========== QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Query")
    FWorldEvent GetEvent(const FString& EventID) const;

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Query")
    TArray<FWorldEvent> GetEventsNearLocation(const FVector& Location, float Radius) const;

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Query")
    TArray<FWorldEvent> GetEventsByType(EWorldEventType Type) const;

    UFUNCTION(BlueprintPure, Category = "WorldEvents|Query")
    bool IsEventActive(const FString& EventID) const;

    // ========== ZEITBASIERTE EVENTS ==========

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Scheduling")
    void SetRecurringEvent(const FString& EventID, float IntervalHours);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Scheduling")
    void SetDailyEvent(const FString& EventID, int32 Hour, int32 Minute);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Scheduling")
    void SetWeeklyEvent(const FString& EventID, int32 DayOfWeek, int32 Hour);

    // ========== EVENT-CREATION ==========

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Creation")
    void RegisterEvent(const FWorldEvent& Event);

    UFUNCTION(BlueprintCallable, Category = "WorldEvents|Creation")
    void UnregisterEvent(const FString& EventID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnEventStarted, FWorldEvent, Event);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnEventEnded, FString, EventID, bool, bSuccess);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPhaseChanged, FString, EventID, int32, NewPhaseIndex);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnPlayerJoinedEvent, FString, EventID, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnEventScheduled, FWorldEvent, Event);

    UPROPERTY(BlueprintAssignable, Category = "WorldEvents|Events")
    FOnEventStarted OnEventStarted;

    UPROPERTY(BlueprintAssignable, Category = "WorldEvents|Events")
    FOnEventEnded OnEventEnded;

    UPROPERTY(BlueprintAssignable, Category = "WorldEvents|Events")
    FOnPhaseChanged OnPhaseChanged;

    UPROPERTY(BlueprintAssignable, Category = "WorldEvents|Events")
    FOnPlayerJoinedEvent OnPlayerJoinedEvent;

    UPROPERTY(BlueprintAssignable, Category = "WorldEvents|Events")
    FOnEventScheduled OnEventScheduled;

protected:
    // ========== KONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WorldEvents|Config")
    TMap<FString, FWorldEvent> RegisteredEvents;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WorldEvents|Config")
    float EventCheckInterval = 60.0f;  // Prüfe jede Minute

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WorldEvents|Config")
    bool bAutoStartScheduledEvents = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WorldEvents|Config")
    int32 MaxConcurrentEvents = 3;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "WorldEvents|State")
    TMap<FString, FWorldEvent> ActiveEvents;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "WorldEvents|State")
    TMap<FString, TMap<FString, int32>> PlayerContributions;  // EventID -> (PlayerID -> Contribution)

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "WorldEvents|State")
    TMap<FString, TArray<FString>> RecurringEvents;  // Type -> EventIDs

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateScheduledEvents();
    void SpawnEventEnemies(const FEventPhase& Phase, const FVector& EventLocation);
    void ProcessEventPhase(FWorldEvent& Event, float DeltaTime);
    void NotifyNearbyPlayers(const FWorldEvent& Event);
};
