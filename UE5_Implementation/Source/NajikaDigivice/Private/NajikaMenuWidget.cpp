// Copyright Claude Code. All Rights Reserved.

#include "NajikaMenuWidget.h"
#include "Components/Button.h"
#include "Components/TextBlock.h"
#include "Components/Slider.h"
#include "Components/CheckBox.h"
#include "Components/WidgetSwitcher.h"
#include "NajikaGameMode.h"
#include "NajikaCharacter.h"
#include "NajikaHttpClient.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/GameUserSettings.h"
#include "TimerManager.h"

void UNajikaMenuWidget::NativeConstruct()
{
	Super::NativeConstruct();

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Menu initialized"));

	// Bind main menu buttons
	if (ContinueButton) ContinueButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnContinueClicked);
	if (StatusButton) StatusButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnStatusClicked);
	if (ChatButton) ChatButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnChatClicked);
	if (InventoryButton) InventoryButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnInventoryClicked);
	if (SettingsButton) SettingsButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnSettingsClicked);
	if (SaveButton) SaveButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnSaveClicked);
	if (LoadButton) LoadButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnLoadClicked);
	if (QuitButton) QuitButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnQuitClicked);

	// Bind settings buttons
	if (BackButton) BackButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnBackClicked);
	if (GraphicsUpButton) GraphicsUpButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnGraphicsUpClicked);
	if (GraphicsDownButton) GraphicsDownButton->OnClicked.AddDynamic(this, &UNajikaMenuWidget::OnGraphicsDownClicked);

	// Bind settings sliders
	if (MasterVolumeSlider) MasterVolumeSlider->OnValueChanged.AddDynamic(this, &UNajikaMenuWidget::OnMasterVolumeChanged);
	if (MusicVolumeSlider) MusicVolumeSlider->OnValueChanged.AddDynamic(this, &UNajikaMenuWidget::OnMusicVolumeChanged);
	if (SFXVolumeSlider) SFXVolumeSlider->OnValueChanged.AddDynamic(this, &UNajikaMenuWidget::OnSFXVolumeChanged);

	// Bind settings checkboxes
	if (FullscreenCheckBox) FullscreenCheckBox->OnCheckStateChanged.AddDynamic(this, &UNajikaMenuWidget::OnFullscreenChanged);
	if (VSyncCheckBox) VSyncCheckBox->OnCheckStateChanged.AddDynamic(this, &UNajikaMenuWidget::OnVSyncChanged);

	// Load current settings
	LoadSettings();

	// Start on main menu page
	ShowMainMenu();
}

// ============================================================
// MENU DISPLAY
// ============================================================

void UNajikaMenuWidget::ShowMenu()
{
	SetVisibility(ESlateVisibility::Visible);

	// Pause game
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		UGameplayStatics::SetGamePaused(GetWorld(), true);
		PC->bShowMouseCursor = true;
		PC->SetInputMode(FInputModeUIOnly());
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Menu shown (game paused)"));
}

void UNajikaMenuWidget::HideMenu()
{
	// Resume game
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		UGameplayStatics::SetGamePaused(GetWorld(), false);
		PC->bShowMouseCursor = false;
		PC->SetInputMode(FInputModeGameOnly());
	}

	RemoveFromParent();

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Menu hidden (game resumed)"));
}

void UNajikaMenuWidget::ShowSettings()
{
	if (MenuSwitcher)
	{
		MenuSwitcher->SetActiveWidgetIndex(1); // Switch to settings page
		UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Settings page shown"));
	}
}

void UNajikaMenuWidget::ShowMainMenu()
{
	if (MenuSwitcher)
	{
		MenuSwitcher->SetActiveWidgetIndex(0); // Switch to main menu page
		UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Main menu page shown"));
	}
}

// ============================================================
// SAVE/LOAD
// ============================================================

void UNajikaMenuWidget::SaveGame()
{
	ANajikaGameMode* GameMode = Cast<ANajikaGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
	if (!GameMode)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaMenuWidget] GameMode not found"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Saving game..."));
	GameMode->SaveGame();

	// Also save to backend
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika && Najika->BackendClient)
		{
			FOnNajikaActionResponse Delegate;
			Delegate.BindDynamic(this, &UNajikaMenuWidget::OnSaveComplete);
			Najika->BackendClient->SaveState(Delegate);
		}
	}
}

void UNajikaMenuWidget::LoadGame()
{
	ANajikaGameMode* GameMode = Cast<ANajikaGameMode>(UGameplayStatics::GetGameMode(GetWorld()));
	if (!GameMode)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaMenuWidget] GameMode not found"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Loading game..."));
	GameMode->LoadGame();

	ShowStatusMessage(TEXT("Spiel geladen!"), 3.0f);
}

// ============================================================
// SETTINGS
// ============================================================

void UNajikaMenuWidget::ApplySettings()
{
	UGameUserSettings* Settings = UGameUserSettings::GetGameUserSettings();
	if (!Settings) return;

	// Apply graphics quality
	Settings->SetOverallScalabilityLevel(GraphicsQuality);

	// Apply and save settings
	Settings->ApplySettings(false);
	SaveSettings();

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Settings applied"));
	ShowStatusMessage(TEXT("Einstellungen gespeichert!"), 2.0f);
}

void UNajikaMenuWidget::LoadSettings()
{
	UGameUserSettings* Settings = UGameUserSettings::GetGameUserSettings();
	if (!Settings) return;

	// Load graphics quality
	GraphicsQuality = Settings->GetOverallScalabilityLevel();
	if (GraphicsQualityText)
	{
		TArray<FString> QualityNames = {TEXT("Niedrig"), TEXT("Mittel"), TEXT("Hoch"), TEXT("Episch")};
		int32 Index = FMath::Clamp(GraphicsQuality, 0, 3);
		GraphicsQualityText->SetText(FText::FromString(QualityNames[Index]));
	}

	// Load fullscreen
	if (FullscreenCheckBox)
	{
		FullscreenCheckBox->SetIsChecked(Settings->GetFullscreenMode() != EWindowMode::Windowed);
	}

	// Load VSync
	if (VSyncCheckBox)
	{
		VSyncCheckBox->SetIsChecked(Settings->IsVSyncEnabled());
	}

	// Load volume settings (placeholder - would use actual audio settings)
	if (MasterVolumeSlider) MasterVolumeSlider->SetValue(0.8f);
	if (MusicVolumeSlider) MusicVolumeSlider->SetValue(0.7f);
	if (SFXVolumeSlider) SFXVolumeSlider->SetValue(0.8f);

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Settings loaded"));
}

void UNajikaMenuWidget::SaveSettings()
{
	UGameUserSettings* Settings = UGameUserSettings::GetGameUserSettings();
	if (!Settings) return;

	Settings->SaveSettings();
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Settings saved to disk"));
}

// ============================================================
// BUTTON HANDLERS - MAIN MENU
// ============================================================

void UNajikaMenuWidget::OnContinueClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Continue clicked"));
	HideMenu();
}

void UNajikaMenuWidget::OnStatusClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Status clicked"));
	// TODO: Open status widget (Blueprint implementation)
	ShowStatusMessage(TEXT("Status-Bildschirm öffnen..."), 2.0f);
}

void UNajikaMenuWidget::OnChatClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Chat clicked"));
	// TODO: Open chat widget (Blueprint implementation)
	ShowStatusMessage(TEXT("Chat öffnen..."), 2.0f);
}

void UNajikaMenuWidget::OnInventoryClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Inventory clicked"));
	// TODO: Open inventory widget (Blueprint implementation)
	ShowStatusMessage(TEXT("Inventar öffnen..."), 2.0f);
}

void UNajikaMenuWidget::OnSettingsClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Settings clicked"));
	ShowSettings();
}

void UNajikaMenuWidget::OnSaveClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Save clicked"));
	SaveGame();
}

void UNajikaMenuWidget::OnLoadClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Load clicked"));
	LoadGame();
}

void UNajikaMenuWidget::OnQuitClicked()
{
	UE_LOG(LogTemp, Warning, TEXT("[NajikaMenuWidget] Quit clicked"));

	// Save before quit
	SaveGame();

	// Quit to main menu or exit application
	UGameplayStatics::OpenLevel(GetWorld(), FName(TEXT("MainMenu")));
}

// ============================================================
// BUTTON HANDLERS - SETTINGS
// ============================================================

void UNajikaMenuWidget::OnBackClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Back clicked"));
	ApplySettings();
	ShowMainMenu();
}

void UNajikaMenuWidget::OnGraphicsUpClicked()
{
	GraphicsQuality = FMath::Clamp(GraphicsQuality + 1, 0, 3);

	TArray<FString> QualityNames = {TEXT("Niedrig"), TEXT("Mittel"), TEXT("Hoch"), TEXT("Episch")};
	if (GraphicsQualityText)
	{
		GraphicsQualityText->SetText(FText::FromString(QualityNames[GraphicsQuality]));
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Graphics quality: %d"), GraphicsQuality);
}

void UNajikaMenuWidget::OnGraphicsDownClicked()
{
	GraphicsQuality = FMath::Clamp(GraphicsQuality - 1, 0, 3);

	TArray<FString> QualityNames = {TEXT("Niedrig"), TEXT("Mittel"), TEXT("Hoch"), TEXT("Episch")};
	if (GraphicsQualityText)
	{
		GraphicsQualityText->SetText(FText::FromString(QualityNames[GraphicsQuality]));
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Graphics quality: %d"), GraphicsQuality);
}

// ============================================================
// SETTINGS HANDLERS
// ============================================================

void UNajikaMenuWidget::OnMasterVolumeChanged(float Value)
{
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaMenuWidget] Master volume: %.2f"), Value);
	// TODO: Apply to audio system (Blueprint implementation)
}

void UNajikaMenuWidget::OnMusicVolumeChanged(float Value)
{
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaMenuWidget] Music volume: %.2f"), Value);
	// TODO: Apply to music mixer (Blueprint implementation)
}

void UNajikaMenuWidget::OnSFXVolumeChanged(float Value)
{
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaMenuWidget] SFX volume: %.2f"), Value);
	// TODO: Apply to SFX mixer (Blueprint implementation)
}

void UNajikaMenuWidget::OnFullscreenChanged(bool bIsChecked)
{
	UGameUserSettings* Settings = UGameUserSettings::GetGameUserSettings();
	if (!Settings) return;

	EWindowMode::Type Mode = bIsChecked ? EWindowMode::Fullscreen : EWindowMode::Windowed;
	Settings->SetFullscreenMode(Mode);

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Fullscreen: %s"), bIsChecked ? TEXT("On") : TEXT("Off"));
}

void UNajikaMenuWidget::OnVSyncChanged(bool bIsChecked)
{
	UGameUserSettings* Settings = UGameUserSettings::GetGameUserSettings();
	if (!Settings) return;

	Settings->SetVSyncEnabled(bIsChecked);

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] VSync: %s"), bIsChecked ? TEXT("On") : TEXT("Off"));
}

// ============================================================
// BACKEND CALLBACKS
// ============================================================

void UNajikaMenuWidget::OnSaveComplete(bool bSuccess, FString Message)
{
	if (bSuccess)
	{
		UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Save successful: %s"), *Message);
		ShowStatusMessage(TEXT("Spiel gespeichert!"), 3.0f);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaMenuWidget] Save failed: %s"), *Message);
		ShowStatusMessage(TEXT("Speichern fehlgeschlagen!"), 3.0f);
	}
}

// ============================================================
// HELPERS
// ============================================================

void UNajikaMenuWidget::ShowStatusMessage(const FString& Message, float Duration)
{
	if (!StatusText) return;

	StatusText->SetText(FText::FromString(Message));
	StatusText->SetVisibility(ESlateVisibility::Visible);

	UE_LOG(LogTemp, Log, TEXT("[NajikaMenuWidget] Status: %s"), *Message);

	// Clear existing timer
	if (GetWorld()->GetTimerManager().IsTimerActive(StatusMessageTimerHandle))
	{
		GetWorld()->GetTimerManager().ClearTimer(StatusMessageTimerHandle);
	}

	// Hide after duration
	GetWorld()->GetTimerManager().SetTimer(
		StatusMessageTimerHandle,
		[this]()
		{
			if (StatusText)
			{
				StatusText->SetVisibility(ESlateVisibility::Collapsed);
			}
		},
		Duration,
		false
	);
}
