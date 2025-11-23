// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "NajikaGameMode.generated.h"

/**
 * Game Mode for Najika Digivice
 *
 * Features:
 * - Single player mode (player + Najika character)
 * - Save/load system
 * - Room management
 * - Battle transitions
 */
UCLASS()
class NAJIKADIGIVICE_API ANajikaGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	ANajikaGameMode();

protected:
	virtual void BeginPlay() override;

public:
	// ============================================================
	// ROOM SYSTEM
	// ============================================================

	/** Current room name */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Room")
	FString CurrentRoom = TEXT("Wohnzimmer");

	/** Available rooms */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Room")
	TArray<FString> AvailableRooms;

	/** Change to different room */
	UFUNCTION(BlueprintCallable, Category = "Najika|Room")
	void ChangeRoom(const FString& RoomName);

	/** Load room from backend */
	UFUNCTION(BlueprintCallable, Category = "Najika|Room")
	void LoadRoomsFromBackend();

	// ============================================================
	// SAVE/LOAD SYSTEM
	// ============================================================

	/** Save game to backend */
	UFUNCTION(BlueprintCallable, Category = "Najika|Save")
	void SaveGame();

	/** Load game from backend */
	UFUNCTION(BlueprintCallable, Category = "Najika|Save")
	void LoadGame();

	/** Auto-save interval (seconds) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Save")
	float AutoSaveInterval = 60.0f;

	/** Enable auto-save */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Save")
	bool bEnableAutoSave = true;

	// ============================================================
	// BATTLE SYSTEM
	// ============================================================

	/** Start battle mode */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void StartBattle();

	/** End battle mode */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void EndBattle();

	/** Is currently in battle */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Battle")
	bool bIsInBattle = false;

	// ============================================================
	// GAME STATE
	// ============================================================

	/** Total play time (seconds) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Stats")
	float TotalPlayTime = 0.0f;

	/** Session start time */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Stats")
	float SessionStartTime = 0.0f;

protected:
	/** Auto-save timer */
	FTimerHandle AutoSaveTimerHandle;

	/** Start auto-save timer */
	void StartAutoSave();
};
