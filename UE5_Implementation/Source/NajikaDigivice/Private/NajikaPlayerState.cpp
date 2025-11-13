// Copyright Claude Code. All Rights Reserved.

#include "NajikaPlayerState.h"
#include "Net/UnrealNetwork.h"

ANajikaPlayerState::ANajikaPlayerState()
{
	// Set default player name
	SetPlayerName(TEXT("Player"));

	// Initialize defaults
	Level = 1;
	XP = 0;
	XPToNextLevel = CalculateXPForLevel(2);

	Currency = 1000;
	Gems = 0;
	InventorySlots = 20;

	// Initialize Najika state to defaults (will be synced from backend)
	NajikaState = FNajikaState();
	LivingState = FNajikaLivingState();
}

void ANajikaPlayerState::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
	Super::GetLifetimeReplicatedProps(OutLifetimeProps);

	// Replicate progression
	DOREPLIFETIME(ANajikaPlayerState, Level);
	DOREPLIFETIME(ANajikaPlayerState, XP);
	DOREPLIFETIME(ANajikaPlayerState, PlayerPlayTime);

	// Replicate resources
	DOREPLIFETIME(ANajikaPlayerState, Currency);
	DOREPLIFETIME(ANajikaPlayerState, Gems);
	DOREPLIFETIME(ANajikaPlayerState, InventorySlots);

	// Replicate Najika state
	DOREPLIFETIME(ANajikaPlayerState, NajikaState);
	DOREPLIFETIME(ANajikaPlayerState, LivingState);

	// Replicate statistics
	DOREPLIFETIME(ANajikaPlayerState, BattlesWon);
	DOREPLIFETIME(ANajikaPlayerState, BattlesLost);
	DOREPLIFETIME(ANajikaPlayerState, EnemiesDefeated);
	DOREPLIFETIME(ANajikaPlayerState, TotalDamageDealt);
	DOREPLIFETIME(ANajikaPlayerState, TotalDamageTaken);
	DOREPLIFETIME(ANajikaPlayerState, TimesFed);
	DOREPLIFETIME(ANajikaPlayerState, TimesTrained);
	DOREPLIFETIME(ANajikaPlayerState, TimesPraised);
	DOREPLIFETIME(ANajikaPlayerState, TimesScolded);
	DOREPLIFETIME(ANajikaPlayerState, ChatMessagesSent);
	DOREPLIFETIME(ANajikaPlayerState, VoiceCallsMade);

	// Replicate achievements
	DOREPLIFETIME(ANajikaPlayerState, UnlockedAchievements);
	DOREPLIFETIME(ANajikaPlayerState, DiscoveredRooms);
	DOREPLIFETIME(ANajikaPlayerState, CompletedQuests);
}

void ANajikaPlayerState::BeginPlay()
{
	Super::BeginPlay();

	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerState] Player initialized - Name: %s, Level: %d"), *GetPlayerName(), Level);
}

// ============================================================
// PROGRESSION
// ============================================================

void ANajikaPlayerState::AddXP(int32 Amount)
{
	if (Amount <= 0) return;

	XP += Amount;
	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerState] +%d XP (Total: %d/%d)"), Amount, XP, XPToNextLevel);

	// Check for level up
	while (XP >= XPToNextLevel)
	{
		LevelUp();
	}
}

void ANajikaPlayerState::LevelUp()
{
	Level++;
	XP -= XPToNextLevel;
	XPToNextLevel = CalculateXPForLevel(Level + 1);

	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerState] LEVEL UP! Level %d reached (Next: %d XP)"), Level, XPToNextLevel);

	// TODO: Trigger level up UI, rewards, etc. (Blueprint)
}

int32 ANajikaPlayerState::CalculateXPForLevel(int32 TargetLevel) const
{
	// Exponential XP curve (similar to Pokemon/Digimon World)
	// Formula: 100 * Level^1.5
	return FMath::RoundToInt(100.0f * FMath::Pow(TargetLevel, 1.5f));
}

float ANajikaPlayerState::GetLevelProgress() const
{
	if (XPToNextLevel <= 0) return 0.0f;
	return static_cast<float>(XP) / static_cast<float>(XPToNextLevel);
}

// ============================================================
// RESOURCES
// ============================================================

void ANajikaPlayerState::AddCurrency(int32 Amount)
{
	if (Amount <= 0) return;

	Currency += Amount;
	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerState] +%d Bits (Total: %d)"), Amount, Currency);
}

bool ANajikaPlayerState::RemoveCurrency(int32 Amount)
{
	if (Amount <= 0) return false;

	if (Currency < Amount)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaPlayerState] Not enough currency (Need: %d, Have: %d)"), Amount, Currency);
		return false;
	}

	Currency -= Amount;
	UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerState] -%d Bits (Total: %d)"), Amount, Currency);
	return true;
}

// ============================================================
// ACHIEVEMENTS
// ============================================================

void ANajikaPlayerState::UnlockAchievement(const FString& AchievementID)
{
	if (AchievementID.IsEmpty()) return;

	if (!UnlockedAchievements.Contains(AchievementID))
	{
		UnlockedAchievements.Add(AchievementID);
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerState] Achievement unlocked: %s"), *AchievementID);

		// TODO: Trigger achievement notification UI (Blueprint)
	}
}

bool ANajikaPlayerState::HasAchievement(const FString& AchievementID) const
{
	return UnlockedAchievements.Contains(AchievementID);
}

void ANajikaPlayerState::DiscoverRoom(const FString& RoomName)
{
	if (RoomName.IsEmpty()) return;

	if (!DiscoveredRooms.Contains(RoomName))
	{
		DiscoveredRooms.Add(RoomName);
		UE_LOG(LogTemp, Log, TEXT("[NajikaPlayerState] Room discovered: %s"), *RoomName);

		// Award XP for discovery
		AddXP(50);

		// Check for achievement (discover all rooms)
		if (DiscoveredRooms.Num() >= 12) // 12 total rooms
		{
			UnlockAchievement(TEXT("explorer"));
		}
	}
}

// ============================================================
// NAJIKA STATE SYNC
// ============================================================

void ANajikaPlayerState::UpdateNajikaState(const FNajikaState& NewState, const FNajikaLivingState& NewLivingState)
{
	NajikaState = NewState;
	LivingState = NewLivingState;
	LastSyncTime = GetWorld()->GetTimeSeconds();

	UE_LOG(LogTemp, Verbose, TEXT("[NajikaPlayerState] Najika state synced - HP: %.1f, Mood: %s"),
		NajikaState.Hunger, *NewLivingState.CurrentMood);
}

// ============================================================
// STATISTICS
// ============================================================

float ANajikaPlayerState::GetWinRate() const
{
	int32 TotalBattles = BattlesWon + BattlesLost;
	if (TotalBattles == 0) return 0.0f;

	return static_cast<float>(BattlesWon) / static_cast<float>(TotalBattles);
}
