// Copyright Claude Code. All Rights Reserved.

#include "NajikaGameState.h"
#include "Net/UnrealNetwork.h"

ANajikaGameState::ANajikaGameState()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = true;

	// Initialize world time to noon
	TimeOfDay = 0.5f;
	WorldTime = 0.0f;
	DayNumber = 1;
}

void ANajikaGameState::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
	Super::GetLifetimeReplicatedProps(OutLifetimeProps);

	// Replicate world state
	DOREPLIFETIME(ANajikaGameState, CurrentRoom);
	DOREPLIFETIME(ANajikaGameState, WorldTime);
	DOREPLIFETIME(ANajikaGameState, DayNumber);
	DOREPLIFETIME(ANajikaGameState, TimeOfDay);
	DOREPLIFETIME(ANajikaGameState, Weather);

	// Replicate session state
	DOREPLIFETIME(ANajikaGameState, TotalPlayTime);
	DOREPLIFETIME(ANajikaGameState, ActivePlayerCount);
	DOREPLIFETIME(ANajikaGameState, bIsGamePaused);

	// Replicate events
	DOREPLIFETIME(ANajikaGameState, ActiveEvent);
	DOREPLIFETIME(ANajikaGameState, EventStartTime);
	DOREPLIFETIME(ANajikaGameState, EventDuration);

	// Replicate battle state
	DOREPLIFETIME(ANajikaGameState, bIsBattleActive);
	DOREPLIFETIME(ANajikaGameState, BattleWave);
	DOREPLIFETIME(ANajikaGameState, EnemiesRemaining);
}

void ANajikaGameState::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogTemp, Log, TEXT("[NajikaGameState] Game started - Room: %s, Day: %d"), *CurrentRoom, DayNumber);
}

void ANajikaGameState::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// Only server updates time
	if (!HasAuthority())
	{
		return;
	}

	// Update world time if not paused
	if (!bIsGamePaused)
	{
		UpdateWorldTime(DeltaTime);
	}

	// Update event progress
	if (!ActiveEvent.IsEmpty())
	{
		float ElapsedTime = WorldTime - EventStartTime;
		EventProgress = FMath::Clamp(ElapsedTime / EventDuration, 0.0f, 1.0f);

		// Auto-end event when duration expires
		if (EventProgress >= 1.0f)
		{
			EndEvent();
		}
	}
}

// ============================================================
// WORLD TIME
// ============================================================

void ANajikaGameState::UpdateWorldTime(float DeltaTime)
{
	// Update total play time
	TotalPlayTime += DeltaTime;
	WorldTime += DeltaTime;

	// Update time of day (0.0 - 1.0, wraps around)
	// TimeScale = 60 means 1 minute real-time = 1 hour in-game
	float DayLength = 86400.0f / TimeScale; // 86400 seconds = 24 hours
	float TimeIncrement = DeltaTime / DayLength;

	TimeOfDay += TimeIncrement;

	// Wrap around midnight
	if (TimeOfDay >= 1.0f)
	{
		TimeOfDay -= 1.0f;
		DayNumber++;
		UE_LOG(LogTemp, Log, TEXT("[NajikaGameState] New day: %d"), DayNumber);
	}
}

void ANajikaGameState::SetCurrentRoom(const FString& NewRoom)
{
	if (CurrentRoom != NewRoom)
	{
		FString OldRoom = CurrentRoom;
		CurrentRoom = NewRoom;
		UE_LOG(LogTemp, Log, TEXT("[NajikaGameState] Room changed: %s -> %s"), *OldRoom, *NewRoom);
	}
}

// ============================================================
// EVENTS
// ============================================================

void ANajikaGameState::StartEvent(const FString& EventName, float Duration)
{
	ActiveEvent = EventName;
	EventStartTime = WorldTime;
	EventDuration = Duration;
	EventProgress = 0.0f;

	UE_LOG(LogTemp, Log, TEXT("[NajikaGameState] Event started: %s (%.1f seconds)"), *EventName, Duration);
}

void ANajikaGameState::EndEvent()
{
	if (!ActiveEvent.IsEmpty())
	{
		UE_LOG(LogTemp, Log, TEXT("[NajikaGameState] Event ended: %s"), *ActiveEvent);
		ActiveEvent = TEXT("");
		EventProgress = 0.0f;
	}
}

// ============================================================
// TIME FORMATTING
// ============================================================

FString ANajikaGameState::GetFormattedTime() const
{
	// Convert TimeOfDay (0.0-1.0) to HH:MM format
	int32 TotalMinutes = FMath::RoundToInt(TimeOfDay * 1440.0f); // 1440 minutes in 24 hours
	int32 Hours = TotalMinutes / 60;
	int32 Minutes = TotalMinutes % 60;

	return FString::Printf(TEXT("%02d:%02d"), Hours, Minutes);
}

FString ANajikaGameState::GetDayPhase() const
{
	// Dawn: 05:00-07:00 (0.208-0.292)
	// Day: 07:00-18:00 (0.292-0.750)
	// Dusk: 18:00-20:00 (0.750-0.833)
	// Night: 20:00-05:00 (0.833-0.208)

	if (TimeOfDay >= 0.208f && TimeOfDay < 0.292f)
	{
		return TEXT("dawn");
	}
	else if (TimeOfDay >= 0.292f && TimeOfDay < 0.750f)
	{
		return TEXT("day");
	}
	else if (TimeOfDay >= 0.750f && TimeOfDay < 0.833f)
	{
		return TEXT("dusk");
	}
	else
	{
		return TEXT("night");
	}
}
