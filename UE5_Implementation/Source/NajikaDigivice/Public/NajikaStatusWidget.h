// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "NajikaBackendTypes.h"
#include "NajikaStatusWidget.generated.h"

class UProgressBar;
class UTextBlock;
class UImage;
class UButton;

/**
 * Status Widget for Najika Digivice
 *
 * Detailed status screen showing:
 * - Najika stats (Strength, Intelligence, Dexterity, Charisma)
 * - Needs (Hunger, Thirst, Energy, Hygiene, Happiness)
 * - Equipment (Weapon, Armor, Accessory)
 * - Level/XP progress
 * - Care mistakes
 * - Weight and discipline
 * - Current mood and activity
 *
 * Usage:
 * - Create Blueprint child class (WBP_NajikaStatus)
 * - Show via PlayerController menu
 */
UCLASS()
class NAJIKADIGIVICE_API UNajikaStatusWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	virtual void NativeConstruct() override;

	// ============================================================
	// STATS
	// ============================================================

	/** Strength stat text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* StrengthText;

	/** Intelligence stat text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* IntelligenceText;

	/** Dexterity stat text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* DexterityText;

	/** Charisma stat text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* CharismaText;

	// ============================================================
	// NEEDS
	// ============================================================

	/** Hunger bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* HungerBar;

	/** Thirst bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* ThirstBar;

	/** Energy bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* EnergyBar;

	/** Hygiene bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* HygieneBar;

	/** Happiness bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* HappinessBar;

	/** Hunger text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* HungerValueText;

	/** Thirst text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ThirstValueText;

	/** Energy text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* EnergyValueText;

	/** Hygiene text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* HygieneValueText;

	/** Happiness text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* HappinessValueText;

	// ============================================================
	// GROWTH & PROGRESSION
	// ============================================================

	/** Level text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* LevelText;

	/** XP bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* XPBar;

	/** XP text (e.g., "250/500") */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* XPText;

	/** Evolution stage text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* EvolutionStageText;

	// ============================================================
	// CARE TRACKING
	// ============================================================

	/** Care mistakes text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* CareMistakesText;

	/** Weight text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* WeightText;

	/** Discipline bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* DisciplineBar;

	/** Discipline text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* DisciplineText;

	/** Fatigue bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* FatigueBar;

	/** Fatigue text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* FatigueText;

	// ============================================================
	// EQUIPMENT
	// ============================================================

	/** Weapon text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* WeaponText;

	/** Armor text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ArmorText;

	/** Accessory text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* AccessoryText;

	/** Weapon icon */
	UPROPERTY(meta = (BindWidget))
	UImage* WeaponIcon;

	/** Armor icon */
	UPROPERTY(meta = (BindWidget))
	UImage* ArmorIcon;

	/** Accessory icon */
	UPROPERTY(meta = (BindWidget))
	UImage* AccessoryIcon;

	// ============================================================
	// LIVING SYSTEM STATE
	// ============================================================

	/** Current mood text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* MoodText;

	/** Mood intensity bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* MoodIntensityBar;

	/** Current activity text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ActivityText;

	/** Emotional bond text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* EmotionalBondText;

	/** Relationship stage text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* RelationshipStageText;

	/** Autonomy level bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* AutonomyLevelBar;

	/** Autonomy level text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* AutonomyLevelText;

	// ============================================================
	// BUTTONS
	// ============================================================

	/** Close button */
	UPROPERTY(meta = (BindWidget))
	UButton* CloseButton;

	/** Refresh button */
	UPROPERTY(meta = (BindWidget))
	UButton* RefreshButton;

	// ============================================================
	// FUNCTIONS
	// ============================================================

	/**
	 * Update all UI elements from Najika state
	 * @param NajikaState Current Najika state
	 * @param LivingState Current living state
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void UpdateStatusDisplay(const FNajikaState& NajikaState, const FNajikaLivingState& LivingState);

	/**
	 * Refresh status from backend
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void RefreshStatus();

protected:
	// Button handlers
	UFUNCTION()
	void OnCloseButtonClicked();

	UFUNCTION()
	void OnRefreshButtonClicked();

	// Backend callback
	UFUNCTION()
	void OnStatusReceived(FNajikaState NajikaState, FNajikaLivingState LivingState);

	// Helper functions
	void UpdateProgressBar(UProgressBar* Bar, float Value, float Max = 100.0f);
	FLinearColor GetStatusColor(float Value) const;
	FString GetMoodEmoji(const FString& Mood) const;
	FString TranslateGerman(const FString& EnglishText) const;
};
