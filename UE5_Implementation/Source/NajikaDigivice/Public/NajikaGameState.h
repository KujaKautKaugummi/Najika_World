// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameStateBase.h"
#include "NajikaGameState.generated.h"

/**
 * Game State for Najika Digivice
 *
 * Replicated game state shared across all clients (multiplayer-ready design)
 * Stores world-level state like time, room, active events
 */
UCLASS()
class NAJIKADIGIVICE_API ANajikaGameState : public AGameStateBase
{
	GENERATED_BODY()

public:
	ANajikaGameState();

	virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

	// ============================================================
	// WORLD STATE
	// ============================================================

	/** Current room (replicated) */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|World")
	FString CurrentRoom = TEXT("Wohnzimmer");

	/** World time (in-game seconds since start) */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|World")
	float WorldTime = 0.0f;

	/** Current day number */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|World")
	int32 DayNumber = 1;

	/** Current time of day (0.0 = midnight, 0.5 = noon, 1.0 = midnight) */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|World")
	float TimeOfDay = 0.5f;

	/** Weather state (clear, cloudy, rainy, stormy) */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|World")
	FString Weather = TEXT("clear");

	// ============================================================
	// GAME SESSION
	// ============================================================

	/** Total session play time (seconds) */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Session")
	float TotalPlayTime = 0.0f;

	/** Number of active players */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Session")
	int32 ActivePlayerCount = 0;

	/** Is game paused */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Session")
	bool bIsGamePaused = false;

	// ============================================================
	// WORLD EVENTS
	// ============================================================

	/** Active world event (birthday, festival, invasion, etc.) */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Events")
	FString ActiveEvent = TEXT("");

	/** Event start time */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Events")
	float EventStartTime = 0.0f;

	/** Event duration (seconds) */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Events")
	float EventDuration = 0.0f;

	/** Event progress (0.0 - 1.0) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Events")
	float EventProgress = 0.0f;

	// ============================================================
	// BATTLE STATE (Replicated)
	// ============================================================

	/** Is battle active */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Battle")
	bool bIsBattleActive = false;

	/** Current battle wave */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Battle")
	int32 BattleWave = 0;

	/** Number of enemies remaining */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Battle")
	int32 EnemiesRemaining = 0;

	// ============================================================
	// FUNCTIONS
	// ============================================================

	/**
	 * Update world time (called by GameMode every tick)
	 * @param DeltaTime Delta time in seconds
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|World")
	void UpdateWorldTime(float DeltaTime);

	/**
	 * Set current room
	 * @param NewRoom Room name
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|World")
	void SetCurrentRoom(const FString& NewRoom);

	/**
	 * Start world event
	 * @param EventName Event name
	 * @param Duration Event duration in seconds
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Events")
	void StartEvent(const FString& EventName, float Duration);

	/**
	 * End current event
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Events")
	void EndEvent();

	/**
	 * Get formatted time string (HH:MM)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|World")
	FString GetFormattedTime() const;

	/**
	 * Get day/night phase (dawn, day, dusk, night)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|World")
	FString GetDayPhase() const;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

private:
	/** Day/night cycle speed (1.0 = real-time, 60.0 = 1 minute = 1 hour) */
	UPROPERTY(EditDefaultsOnly, Category = "Najika|World")
	float TimeScale = 60.0f;
};
