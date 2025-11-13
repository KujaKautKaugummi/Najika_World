// Copyright Claude Code. All Rights Reserved.

#include "NajikaHUDWidget.h"
#include "Components/ProgressBar.h"
#include "Components/TextBlock.h"
#include "Components/Button.h"
#include "Components/Image.h"
#include "Components/Overlay.h"
#include "Components/CanvasPanel.h"
#include "NajikaCharacter.h"
#include "NajikaPlayerController.h"
#include "TimerManager.h"

void UNajikaHUDWidget::NativeConstruct()
{
	Super::NativeConstruct();

	UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] HUD initialized"));

	// Bind button click events
	if (FeedButton)
	{
		FeedButton->OnClicked.AddDynamic(this, &UNajikaHUDWidget::OnFeedClicked);
	}

	if (DrinkButton)
	{
		DrinkButton->OnClicked.AddDynamic(this, &UNajikaHUDWidget::OnDrinkClicked);
	}

	if (WashButton)
	{
		WashButton->OnClicked.AddDynamic(this, &UNajikaHUDWidget::OnWashClicked);
	}

	if (SleepButton)
	{
		SleepButton->OnClicked.AddDynamic(this, &UNajikaHUDWidget::OnSleepClicked);
	}

	if (TrainButton)
	{
		TrainButton->OnClicked.AddDynamic(this, &UNajikaHUDWidget::OnTrainClicked);
	}

	// Hide combat UI by default
	SetCombatUIVisible(false);

	// Hide notification by default
	if (NotificationOverlay)
	{
		NotificationOverlay->SetVisibility(ESlateVisibility::Collapsed);
	}

	// Detect platform and show/hide touch controls
	#if PLATFORM_ANDROID || PLATFORM_IOS
		SetTouchControlsVisible(true);
	#else
		SetTouchControlsVisible(false);
	#endif
}

void UNajikaHUDWidget::NativeTick(const FGeometry& MyGeometry, float InDeltaTime)
{
	Super::NativeTick(MyGeometry, InDeltaTime);

	// Auto-update from Character state
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			// Update Najika status
			UpdateFromNajikaState(Najika->CurrentState, Najika->LivingState);

			// Update combat UI
			UpdateCombatUI(Najika->CurrentHP, Najika->MaxHP, Najika->Stamina, Najika->MaxStamina);
		}
	}
}

// ============================================================
// BUTTON HANDLERS
// ============================================================

void UNajikaHUDWidget::OnFeedClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] Feed button clicked"));

	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			Najika->Feed();
			ShowNotification(TEXT("Najika gefüttert! 🍖"), 2.0f);
		}
	}
}

void UNajikaHUDWidget::OnDrinkClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] Drink button clicked"));

	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			Najika->Drink();
			ShowNotification(TEXT("Najika hat getrunken! 💧"), 2.0f);
		}
	}
}

void UNajikaHUDWidget::OnWashClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] Wash button clicked"));

	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			Najika->Wash();
			ShowNotification(TEXT("Najika gewaschen! 🛁"), 2.0f);
		}
	}
}

void UNajikaHUDWidget::OnSleepClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] Sleep button clicked"));

	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			Najika->Sleep();
			ShowNotification(TEXT("Najika schläft! 😴"), 2.0f);
		}
	}
}

void UNajikaHUDWidget::OnTrainClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] Train button clicked"));

	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			// Default to strength training (can be changed in Blueprint)
			Najika->Train(TEXT("strength"));
			ShowNotification(TEXT("Training gestartet! 💪"), 2.0f);
		}
	}
}

// ============================================================
// UPDATE FUNCTIONS
// ============================================================

void UNajikaHUDWidget::UpdateFromNajikaState(const FNajikaState& NajikaState, const FNajikaLivingState& LivingState)
{
	// Update need bars
	UpdateProgressBar(HungerBar, NajikaState.Hunger);
	UpdateProgressBar(ThirstBar, NajikaState.Thirst);
	UpdateProgressBar(EnergyBar, NajikaState.Energy);
	UpdateProgressBar(HygieneBar, NajikaState.Hygiene);
	UpdateProgressBar(HappinessBar, NajikaState.Happiness);

	// Update need text
	if (HungerText)
	{
		HungerText->SetText(FText::FromString(FString::Printf(TEXT("Hunger: %.0f%%"), NajikaState.Hunger)));
		HungerText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Hunger)));
	}

	if (ThirstText)
	{
		ThirstText->SetText(FText::FromString(FString::Printf(TEXT("Durst: %.0f%%"), NajikaState.Thirst)));
		ThirstText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Thirst)));
	}

	if (EnergyText)
	{
		EnergyText->SetText(FText::FromString(FString::Printf(TEXT("Energie: %.0f%%"), NajikaState.Energy)));
		EnergyText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Energy)));
	}

	if (HygieneText)
	{
		HygieneText->SetText(FText::FromString(FString::Printf(TEXT("Hygiene: %.0f%%"), NajikaState.Hygiene)));
		HygieneText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Hygiene)));
	}

	if (HappinessText)
	{
		HappinessText->SetText(FText::FromString(FString::Printf(TEXT("Glück: %.0f%%"), NajikaState.Happiness)));
		HappinessText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Happiness)));
	}
}

void UNajikaHUDWidget::UpdateCombatUI(int32 CurrentHP, int32 MaxHP, float CurrentStamina, float MaxStamina)
{
	// Update HP bar
	UpdateProgressBar(HPBar, static_cast<float>(CurrentHP), static_cast<float>(MaxHP));

	// Update Stamina bar
	UpdateProgressBar(StaminaBar, CurrentStamina, MaxStamina);

	// Update HP text
	if (HPText)
	{
		HPText->SetText(FText::FromString(FString::Printf(TEXT("HP: %d/%d"), CurrentHP, MaxHP)));

		float HPPercent = MaxHP > 0 ? (static_cast<float>(CurrentHP) / static_cast<float>(MaxHP)) * 100.0f : 0.0f;
		HPText->SetColorAndOpacity(FSlateColor(GetStatusColor(HPPercent)));
	}

	// Update Stamina text
	if (StaminaText)
	{
		StaminaText->SetText(FText::FromString(FString::Printf(TEXT("Stamina: %.0f/%.0f"), CurrentStamina, MaxStamina)));

		float StaminaPercent = MaxStamina > 0 ? (CurrentStamina / MaxStamina) * 100.0f : 0.0f;
		StaminaText->SetColorAndOpacity(FSlateColor(GetStatusColor(StaminaPercent)));
	}
}

void UNajikaHUDWidget::UpdatePlayerInfo(int32 Level, int32 XP, int32 XPToNext, int32 Currency)
{
	// Update level text
	if (LevelText)
	{
		LevelText->SetText(FText::FromString(FString::Printf(TEXT("Level %d"), Level)));
	}

	// Update XP bar
	UpdateProgressBar(XPBar, static_cast<float>(XP), static_cast<float>(XPToNext));

	// Update currency text
	if (CurrencyText)
	{
		CurrencyText->SetText(FText::FromString(FString::Printf(TEXT("%d Bits"), Currency)));
	}
}

void UNajikaHUDWidget::UpdateWorldInfo(const FString& RoomName, const FString& Time, int32 Day, const FString& Weather)
{
	// Update room text
	if (RoomText)
	{
		RoomText->SetText(FText::FromString(RoomName));
	}

	// Update time text
	if (TimeText)
	{
		TimeText->SetText(FText::FromString(Time));
	}

	// Update day text
	if (DayText)
	{
		DayText->SetText(FText::FromString(FString::Printf(TEXT("Tag %d"), Day)));
	}

	// Weather icon update (Blueprint-implementable)
	// TODO: Load weather icon texture based on Weather string
}

void UNajikaHUDWidget::SetCombatUIVisible(bool bVisible)
{
	if (CombatOverlay)
	{
		CombatOverlay->SetVisibility(bVisible ? ESlateVisibility::Visible : ESlateVisibility::Collapsed);
	}
}

void UNajikaHUDWidget::SetTouchControlsVisible(bool bVisible)
{
	if (TouchControlsPanel)
	{
		TouchControlsPanel->SetVisibility(bVisible ? ESlateVisibility::Visible : ESlateVisibility::Collapsed);
		UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] Touch controls: %s"), bVisible ? TEXT("Visible") : TEXT("Hidden"));
	}
}

// ============================================================
// NOTIFICATION SYSTEM
// ============================================================

void UNajikaHUDWidget::ShowNotification(const FString& Message, float Duration)
{
	if (!NotificationOverlay || !NotificationText)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaHUDWidget] Notification widgets not bound"));
		return;
	}

	// Set notification text
	NotificationText->SetText(FText::FromString(Message));

	// Show notification overlay
	NotificationOverlay->SetVisibility(ESlateVisibility::Visible);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHUDWidget] Notification: %s (%.1fs)"), *Message, Duration);

	// Clear existing timer
	if (GetWorld()->GetTimerManager().IsTimerActive(NotificationTimerHandle))
	{
		GetWorld()->GetTimerManager().ClearTimer(NotificationTimerHandle);
	}

	// Set timer to hide notification
	GetWorld()->GetTimerManager().SetTimer(
		NotificationTimerHandle,
		this,
		&UNajikaHUDWidget::HideNotification,
		Duration,
		false
	);
}

void UNajikaHUDWidget::HideNotification()
{
	if (NotificationOverlay)
	{
		NotificationOverlay->SetVisibility(ESlateVisibility::Collapsed);
	}
}

// ============================================================
// HELPER FUNCTIONS
// ============================================================

void UNajikaHUDWidget::UpdateProgressBar(UProgressBar* Bar, float Value, float Max)
{
	if (!Bar) return;

	float Percent = Max > 0.0f ? FMath::Clamp(Value / Max, 0.0f, 1.0f) : 0.0f;
	Bar->SetPercent(Percent);

	// Set color based on value (green > yellow > orange > red)
	Bar->SetFillColorAndOpacity(GetStatusColor(Percent * 100.0f));
}

void UNajikaHUDWidget::UpdateTextBlock(UTextBlock* Text, const FString& Content)
{
	if (!Text) return;
	Text->SetText(FText::FromString(Content));
}

FLinearColor UNajikaHUDWidget::GetStatusColor(float Value) const
{
	// Green (>75%), Yellow (50-75%), Orange (25-50%), Red (<25%)
	if (Value >= 75.0f)
	{
		return FLinearColor::Green;
	}
	else if (Value >= 50.0f)
	{
		return FLinearColor::Yellow;
	}
	else if (Value >= 25.0f)
	{
		return FLinearColor(1.0f, 0.5f, 0.0f); // Orange
	}
	else
	{
		return FLinearColor::Red;
	}
}
