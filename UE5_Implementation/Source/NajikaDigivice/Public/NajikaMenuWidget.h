// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "NajikaMenuWidget.generated.h"

class UButton;
class UTextBlock;
class USlider;
class UCheckBox;
class UWidgetSwitcher;

/**
 * Menu Widget for Najika Digivice
 *
 * Main pause menu with options:
 * - Continue (resume game)
 * - Status (open status screen)
 * - Chat (open chat window)
 * - Inventory (open inventory)
 * - Settings (graphics, audio, controls)
 * - Save Game
 * - Load Game
 * - Quit to Main Menu
 *
 * Usage:
 * - Create Blueprint child class (WBP_NajikaMenu)
 * - Show via PlayerController (ESC/Pause button)
 */
UCLASS()
class NAJIKADIGIVICE_API UNajikaMenuWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	virtual void NativeConstruct() override;

	// ============================================================
	// MAIN MENU BUTTONS
	// ============================================================

	/** Continue button */
	UPROPERTY(meta = (BindWidget))
	UButton* ContinueButton;

	/** Status button */
	UPROPERTY(meta = (BindWidget))
	UButton* StatusButton;

	/** Chat button */
	UPROPERTY(meta = (BindWidget))
	UButton* ChatButton;

	/** Inventory button */
	UPROPERTY(meta = (BindWidget))
	UButton* InventoryButton;

	/** Settings button */
	UPROPERTY(meta = (BindWidget))
	UButton* SettingsButton;

	/** Save game button */
	UPROPERTY(meta = (BindWidget))
	UButton* SaveButton;

	/** Load game button */
	UPROPERTY(meta = (BindWidget))
	UButton* LoadButton;

	/** Quit button */
	UPROPERTY(meta = (BindWidget))
	UButton* QuitButton;

	// ============================================================
	// SETTINGS UI
	// ============================================================

	/** Widget switcher (Main Menu <-> Settings) */
	UPROPERTY(meta = (BindWidget))
	UWidgetSwitcher* MenuSwitcher;

	/** Master volume slider */
	UPROPERTY(meta = (BindWidget))
	USlider* MasterVolumeSlider;

	/** Music volume slider */
	UPROPERTY(meta = (BindWidget))
	USlider* MusicVolumeSlider;

	/** SFX volume slider */
	UPROPERTY(meta = (BindWidget))
	USlider* SFXVolumeSlider;

	/** Fullscreen checkbox */
	UPROPERTY(meta = (BindWidget))
	UCheckBox* FullscreenCheckBox;

	/** VSync checkbox */
	UPROPERTY(meta = (BindWidget))
	UCheckBox* VSyncCheckBox;

	/** Graphics quality text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* GraphicsQualityText;

	/** Graphics quality up button */
	UPROPERTY(meta = (BindWidget))
	UButton* GraphicsUpButton;

	/** Graphics quality down button */
	UPROPERTY(meta = (BindWidget))
	UButton* GraphicsDownButton;

	/** Back to menu button (from settings) */
	UPROPERTY(meta = (BindWidget))
	UButton* BackButton;

	// ============================================================
	// INFO TEXT
	// ============================================================

	/** Status text (e.g., "Game Saved!") */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* StatusText;

	// ============================================================
	// FUNCTIONS
	// ============================================================

	/**
	 * Show menu (pause game)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ShowMenu();

	/**
	 * Hide menu (resume game)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void HideMenu();

	/**
	 * Show settings page
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ShowSettings();

	/**
	 * Show main menu page
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ShowMainMenu();

	/**
	 * Save game
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void SaveGame();

	/**
	 * Load game
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void LoadGame();

	/**
	 * Apply settings
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|UI")
	void ApplySettings();

protected:
	// Button handlers
	UFUNCTION()
	void OnContinueClicked();

	UFUNCTION()
	void OnStatusClicked();

	UFUNCTION()
	void OnChatClicked();

	UFUNCTION()
	void OnInventoryClicked();

	UFUNCTION()
	void OnSettingsClicked();

	UFUNCTION()
	void OnSaveClicked();

	UFUNCTION()
	void OnLoadClicked();

	UFUNCTION()
	void OnQuitClicked();

	UFUNCTION()
	void OnBackClicked();

	UFUNCTION()
	void OnGraphicsUpClicked();

	UFUNCTION()
	void OnGraphicsDownClicked();

	// Settings handlers
	UFUNCTION()
	void OnMasterVolumeChanged(float Value);

	UFUNCTION()
	void OnMusicVolumeChanged(float Value);

	UFUNCTION()
	void OnSFXVolumeChanged(float Value);

	UFUNCTION()
	void OnFullscreenChanged(bool bIsChecked);

	UFUNCTION()
	void OnVSyncChanged(bool bIsChecked);

	// Backend callbacks
	UFUNCTION()
	void OnSaveComplete(bool bSuccess, FString Message);

	// Helper functions
	void ShowStatusMessage(const FString& Message, float Duration = 3.0f);
	void LoadSettings();
	void SaveSettings();

	// Settings state
	int32 GraphicsQuality = 2; // 0=Low, 1=Medium, 2=High, 3=Epic
	FTimerHandle StatusMessageTimerHandle;
};
