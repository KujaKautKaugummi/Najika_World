// Copyright Claude Code. All Rights Reserved.

#include "NajikaGameMode.h"
#include "NajikaPlayerController.h"
#include "NajikaCharacter.h"
#include "TimerManager.h"

ANajikaGameMode::ANajikaGameMode()
{
	// Set default pawn and controller classes
	DefaultPawnClass = ANajikaCharacter::StaticClass();
	PlayerControllerClass = ANajikaPlayerController::StaticClass();

	// Initialize available rooms
	AvailableRooms = {
		TEXT("Wohnzimmer"),
		TEXT("Schlafzimmer"),
		TEXT("Küche"),
		TEXT("Badezimmer"),
		TEXT("Garten"),
		TEXT("Musikraum"),
		TEXT("Medizin"),
		TEXT("Terminal"),
		TEXT("Studieren & Crafting"),
		TEXT("Trainingszimmer"),
		TEXT("Kampfarena"),
		TEXT("Schwarze Mühle – Keller")
	};
}

void ANajikaGameMode::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Game started - Room: %s"), *CurrentRoom);

	// Record session start time
	SessionStartTime = GetWorld()->GetTimeSeconds();

	// Start auto-save if enabled
	if (bEnableAutoSave)
	{
		StartAutoSave();
	}

	// Load rooms from backend
	LoadRoomsFromBackend();
}

// ============================================================
// ROOM SYSTEM
// ============================================================

void ANajikaGameMode::ChangeRoom(const FString& RoomName)
{
	if (!AvailableRooms.Contains(RoomName))
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaGameMode] Room '%s' not available"), *RoomName);
		return;
	}

	CurrentRoom = RoomName;
	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Changed to room: %s"), *CurrentRoom);

	// TODO: Load room level/assets (implement in Blueprint or with Level Streaming)
	// Example: LoadStreamLevel(RoomName);
}

void ANajikaGameMode::LoadRoomsFromBackend()
{
	// TODO: Fetch rooms from backend API (/api/rooms)
	// For now, rooms are hardcoded in constructor
	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] %d rooms available"), AvailableRooms.Num());
}

// ============================================================
// SAVE/LOAD SYSTEM
// ============================================================

void ANajikaGameMode::SaveGame()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Saving game..."));

	// TODO: Save game state via backend API (/api/save)
	// This triggers backend to save STATE to disk

	// For now, just log
	TotalPlayTime += (GetWorld()->GetTimeSeconds() - SessionStartTime);
	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Game saved - Total playtime: %.1f seconds"), TotalPlayTime);
}

void ANajikaGameMode::LoadGame()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Loading game..."));

	// TODO: Load game state from backend API (/api/state)
	// This restores STATE from disk

	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Game loaded"));
}

void ANajikaGameMode::StartAutoSave()
{
	if (bEnableAutoSave && AutoSaveInterval > 0.0f)
	{
		GetWorld()->GetTimerManager().SetTimer(
			AutoSaveTimerHandle,
			this,
			&ANajikaGameMode::SaveGame,
			AutoSaveInterval,
			true // Loop
		);

		UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Auto-save started (interval: %.1f seconds)"), AutoSaveInterval);
	}
}

// ============================================================
// BATTLE SYSTEM
// ============================================================

void ANajikaGameMode::StartBattle()
{
	if (bIsInBattle)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaGameMode] Already in battle!"));
		return;
	}

	bIsInBattle = true;
	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Battle started"));

	// TODO: Trigger battle UI, disable room movement, etc. (Blueprint)
}

void ANajikaGameMode::EndBattle()
{
	if (!bIsInBattle)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaGameMode] Not in battle!"));
		return;
	}

	bIsInBattle = false;
	UE_LOG(LogTemp, Log, TEXT("[NajikaGameMode] Battle ended"));

	// TODO: Hide battle UI, enable room movement, etc. (Blueprint)
}
