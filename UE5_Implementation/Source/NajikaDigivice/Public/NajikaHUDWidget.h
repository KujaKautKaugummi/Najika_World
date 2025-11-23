// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "NajikaBackendTypes.h"
#include "NajikaHUDWidget.generated.h"

class UProgressBar;
class UTextBlock;
class UButton;
class UImage;
class UOverlay;
class UCanvasPanel;

/**
 * Main HUD Widget for Najika Digivice
 *
 * Features:
 * - Najika status bars (Hunger, Thirst, Energy, Hygiene, Happiness)
 * - Quick action buttons (Feed, Drink, Wash, Sleep, Train)
 * - Room display
 * - Time display
 * - HP/Stamina display (combat)
 * - Mobile touch controls
 * - Notification system
 *
 * Usage:
 * - Create Blueprint child class (WBP_NajikaHUD)
 * - Bind UI elements via meta=(BindWidget)
 * - Add to viewport in PlayerController::BeginPlay()
 */
UCLASS()
class NAJIKADIGIVICE_API UNajikaHUDWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	virtual void NativeConstruct() override;
	virtual void NativeTick(const FGeometry& MyGeometry, float InDeltaTime) override;

	// ============================================================
	// STATUS BARS (Needs)
	// ============================================================

	/** Hunger bar (0-100) */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* HungerBar;

	/** Thirst bar (0-100) */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* ThirstBar;

	/** Energy bar (0-100) */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* EnergyBar;

	/** Hygiene bar (0-100) */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* HygieneBar;

	/** Happiness bar (0-100) */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* HappinessBar;

	// ============================================================
	// STATUS TEXT LABELS
	// ============================================================

	/** Hunger text (e.g., "Hunger: 85%") */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* HungerText;

	/** Thirst text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ThirstText;

	/** Energy text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* EnergyText;

	/** Hygiene text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* HygieneText;

	/** Happiness text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* HappinessText;

	// ============================================================
	// QUICK ACTION BUTTONS
	// ============================================================

	/** Feed button */
	UPROPERTY(meta = (BindWidget))
	UButton* FeedButton;

	/** Drink button */
	UPROPERTY(meta = (BindWidget))
	UButton* DrinkButton;

	/** Wash button */
	UPROPERTY(meta = (BindWidget))
	UButton* WashButton;

	/** Sleep button */
	UPROPERTY(meta = (BindWidget))
	UButton* SleepButton;

	/** Train button */
	UPROPERTY(meta = (BindWidget))
	UButton* TrainButton;

	// ============================================================
	// COMBAT UI (visible during battle)
	// ============================================================

	/** HP bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* HPBar;

	/** Stamina bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* StaminaBar;

	/** HP text (e.g., "HP: 85/100") */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* HPText;

	/** Stamina text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* StaminaText;

	/** Combat UI overlay (hidden when not in battle) */
	UPROPERTY(meta = (BindWidget))
	UOverlay* CombatOverlay;

	// ============================================================
	// WORLD INFO
	// ============================================================

	/** Current room text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* RoomText;

	/** Current time text (HH:MM) */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* TimeText;

	/** Current day text (Day 1) */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* DayText;

	/** Weather icon */
	UPROPERTY(meta = (BindWidget))
	UImage* WeatherIcon;

	// ============================================================
	// PLAYER INFO
	// ============================================================

	/** Player level text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* LevelText;

	/** Player XP bar */
	UPROPERTY(meta = (BindWidget))
	UProgressBar* XPBar;

	/** Currency text (Bits) */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* CurrencyText;

	// ============================================================
	// MOBILE TOUCH CONTROLS
	// ============================================================

	/** Virtual joystick overlay (visible on mobile) */
	UPROPERTY(meta = (BindWidget))
	UCanvasPanel* TouchControlsPanel;

	/** Show/hide touch controls */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void SetTouchControlsVisible(bool bVisible);

	// ============================================================
	// NOTIFICATION SYSTEM
	// ============================================================

	/** Notification text (top-center) */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* NotificationText;

	/** Notification overlay (fades in/out) */
	UPROPERTY(meta = (BindWidget))
	UOverlay* NotificationOverlay;

	/**
	 * Show notification message
	 * @param Message Notification text
	 * @param Duration Display duration (seconds)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ShowNotification(const FString& Message, float Duration = 3.0f);

	// ============================================================
	// UPDATE FUNCTIONS
	// ============================================================

	/**
	 * Update all UI elements from Najika state
	 * @param NajikaState Current Najika state
	 * @param LivingState Current living state
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void UpdateFromNajikaState(const FNajikaState& NajikaState, const FNajikaLivingState& LivingState);

	/**
	 * Update combat UI (HP, Stamina)
	 * @param CurrentHP Current HP
	 * @param MaxHP Max HP
	 * @param CurrentStamina Current Stamina
	 * @param MaxStamina Max Stamina
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void UpdateCombatUI(int32 CurrentHP, int32 MaxHP, float CurrentStamina, float MaxStamina);

	/**
	 * Update player info (Level, XP, Currency)
	 * @param Level Player level
	 * @param XP Current XP
	 * @param XPToNext XP required for next level
	 * @param Currency Player currency
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void UpdatePlayerInfo(int32 Level, int32 XP, int32 XPToNext, int32 Currency);

	/**
	 * Update world info (Room, Time, Day, Weather)
	 * @param RoomName Current room
	 * @param Time Formatted time (HH:MM)
	 * @param Day Current day
	 * @param Weather Weather state
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void UpdateWorldInfo(const FString& RoomName, const FString& Time, int32 Day, const FString& Weather);

	/**
	 * Set combat UI visibility
	 * @param bVisible Show/hide combat UI
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void SetCombatUIVisible(bool bVisible);

protected:
	// Button click handlers
	UFUNCTION()
	void OnFeedClicked();

	UFUNCTION()
	void OnDrinkClicked();

	UFUNCTION()
	void OnWashClicked();

	UFUNCTION()
	void OnSleepClicked();

	UFUNCTION()
	void OnTrainClicked();

	// Helper functions
	void UpdateProgressBar(UProgressBar* Bar, float Value, float Max = 100.0f);
	void UpdateTextBlock(UTextBlock* Text, const FString& Content);
	FLinearColor GetStatusColor(float Value) const;

	// Notification timer
	FTimerHandle NotificationTimerHandle;
	void HideNotification();
};
