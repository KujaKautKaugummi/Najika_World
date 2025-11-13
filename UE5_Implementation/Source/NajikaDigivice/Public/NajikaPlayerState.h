// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "NajikaBackendTypes.h"
#include "NajikaPlayerState.generated.h"

/**
 * Player State for Najika Digivice
 *
 * Replicated per-player state (multiplayer-ready design)
 * Stores player-specific data like level, inventory, stats
 */
UCLASS()
class NAJIKADIGIVICE_API ANajikaPlayerState : public APlayerState
{
	GENERATED_BODY()

public:
	ANajikaPlayerState();

	virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

	// ============================================================
	// PLAYER PROGRESSION
	// ============================================================

	/** Player level */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Progression")
	int32 Level = 1;

	/** Player XP */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Progression")
	int32 XP = 0;

	/** XP required for next level */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Progression")
	int32 XPToNextLevel = 100;

	/** Total play time for this player (seconds) */
	UPROPERTY(Replicated, BlueprintReadOnly, Category = "Najika|Progression")
	float PlayerPlayTime = 0.0f;

	// ============================================================
	// PLAYER RESOURCES
	// ============================================================

	/** Player currency (Bits) */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Resources")
	int32 Currency = 1000;

	/** Player gems (premium currency) */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Resources")
	int32 Gems = 0;

	/** Inventory slot count */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Resources")
	int32 InventorySlots = 20;

	// ============================================================
	// NAJIKA STATE (Cached from backend)
	// ============================================================

	/** Najika's current state (synced from backend) */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|State")
	FNajikaState NajikaState;

	/** Living system state (synced from backend) */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|State")
	FNajikaLivingState LivingState;

	/** Last sync time */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|State")
	float LastSyncTime = 0.0f;

	// ============================================================
	// PLAYER STATISTICS
	// ============================================================

	/** Total battles won */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 BattlesWon = 0;

	/** Total battles lost */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 BattlesLost = 0;

	/** Total enemies defeated */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 EnemiesDefeated = 0;

	/** Total damage dealt */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 TotalDamageDealt = 0;

	/** Total damage taken */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 TotalDamageTaken = 0;

	/** Times fed Najika */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 TimesFed = 0;

	/** Times trained Najika */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 TimesTrained = 0;

	/** Times praised Najika */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 TimesPraised = 0;

	/** Times scolded Najika */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 TimesScolded = 0;

	/** Total chat messages sent */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 ChatMessagesSent = 0;

	/** Total voice calls made */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Stats")
	int32 VoiceCallsMade = 0;

	// ============================================================
	// ACHIEVEMENTS & MILESTONES
	// ============================================================

	/** Unlocked achievements (IDs) */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Achievements")
	TArray<FString> UnlockedAchievements;

	/** Discovered rooms */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Achievements")
	TArray<FString> DiscoveredRooms;

	/** Completed quests */
	UPROPERTY(Replicated, BlueprintReadWrite, Category = "Najika|Achievements")
	TArray<FString> CompletedQuests;

	// ============================================================
	// FUNCTIONS
	// ============================================================

	/**
	 * Add XP to player
	 * @param Amount XP amount
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Progression")
	void AddXP(int32 Amount);

	/**
	 * Add currency to player
	 * @param Amount Currency amount
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Resources")
	void AddCurrency(int32 Amount);

	/**
	 * Remove currency from player
	 * @param Amount Currency amount
	 * @return True if successful (had enough currency)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Resources")
	bool RemoveCurrency(int32 Amount);

	/**
	 * Unlock achievement
	 * @param AchievementID Achievement ID
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Achievements")
	void UnlockAchievement(const FString& AchievementID);

	/**
	 * Check if achievement is unlocked
	 * @param AchievementID Achievement ID
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Achievements")
	bool HasAchievement(const FString& AchievementID) const;

	/**
	 * Discover room
	 * @param RoomName Room name
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Achievements")
	void DiscoverRoom(const FString& RoomName);

	/**
	 * Update Najika state from backend
	 * @param NewState New Najika state
	 * @param NewLivingState New living state
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|State")
	void UpdateNajikaState(const FNajikaState& NewState, const FNajikaLivingState& NewLivingState);

	/**
	 * Get level progress (0.0-1.0)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Progression")
	float GetLevelProgress() const;

	/**
	 * Get win rate (0.0-1.0)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Stats")
	float GetWinRate() const;

	/**
	 * Get care mistakes total
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Stats")
	int32 GetCareMistakes() const { return NajikaState.CareMistakes; }

protected:
	virtual void BeginPlay() override;

private:
	/** Calculate XP required for level */
	int32 CalculateXPForLevel(int32 TargetLevel) const;

	/** Level up player */
	void LevelUp();
};
