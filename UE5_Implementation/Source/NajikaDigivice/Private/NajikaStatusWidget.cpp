// Copyright Claude Code. All Rights Reserved.

#include "NajikaStatusWidget.h"
#include "Components/ProgressBar.h"
#include "Components/TextBlock.h"
#include "Components/Image.h"
#include "Components/Button.h"
#include "NajikaCharacter.h"
#include "NajikaHttpClient.h"

void UNajikaStatusWidget::NativeConstruct()
{
	Super::NativeConstruct();

	UE_LOG(LogTemp, Log, TEXT("[NajikaStatusWidget] Status widget initialized"));

	// Bind button events
	if (CloseButton)
	{
		CloseButton->OnClicked.AddDynamic(this, &UNajikaStatusWidget::OnCloseButtonClicked);
	}

	if (RefreshButton)
	{
		RefreshButton->OnClicked.AddDynamic(this, &UNajikaStatusWidget::OnRefreshButtonClicked);
	}

	// Auto-refresh on open
	RefreshStatus();
}

// ============================================================
// UPDATE FUNCTIONS
// ============================================================

void UNajikaStatusWidget::UpdateStatusDisplay(const FNajikaState& NajikaState, const FNajikaLivingState& LivingState)
{
	// ============================================================
	// UPDATE STATS
	// ============================================================

	if (StrengthText)
	{
		StrengthText->SetText(FText::FromString(FString::Printf(TEXT("Stärke: %d"), NajikaState.Strength)));
	}

	if (IntelligenceText)
	{
		IntelligenceText->SetText(FText::FromString(FString::Printf(TEXT("Intelligenz: %d"), NajikaState.Intelligence)));
	}

	if (DexterityText)
	{
		DexterityText->SetText(FText::FromString(FString::Printf(TEXT("Geschick: %d"), NajikaState.Dexterity)));
	}

	if (CharismaText)
	{
		CharismaText->SetText(FText::FromString(FString::Printf(TEXT("Charisma: %d"), NajikaState.Charisma)));
	}

	// ============================================================
	// UPDATE NEEDS
	// ============================================================

	UpdateProgressBar(HungerBar, NajikaState.Hunger);
	UpdateProgressBar(ThirstBar, NajikaState.Thirst);
	UpdateProgressBar(EnergyBar, NajikaState.Energy);
	UpdateProgressBar(HygieneBar, NajikaState.Hygiene);
	UpdateProgressBar(HappinessBar, NajikaState.Happiness);

	if (HungerValueText)
	{
		HungerValueText->SetText(FText::FromString(FString::Printf(TEXT("%.0f%%"), NajikaState.Hunger)));
		HungerValueText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Hunger)));
	}

	if (ThirstValueText)
	{
		ThirstValueText->SetText(FText::FromString(FString::Printf(TEXT("%.0f%%"), NajikaState.Thirst)));
		ThirstValueText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Thirst)));
	}

	if (EnergyValueText)
	{
		EnergyValueText->SetText(FText::FromString(FString::Printf(TEXT("%.0f%%"), NajikaState.Energy)));
		EnergyValueText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Energy)));
	}

	if (HygieneValueText)
	{
		HygieneValueText->SetText(FText::FromString(FString::Printf(TEXT("%.0f%%"), NajikaState.Hygiene)));
		HygieneValueText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Hygiene)));
	}

	if (HappinessValueText)
	{
		HappinessValueText->SetText(FText::FromString(FString::Printf(TEXT("%.0f%%"), NajikaState.Happiness)));
		HappinessValueText->SetColorAndOpacity(FSlateColor(GetStatusColor(NajikaState.Happiness)));
	}

	// ============================================================
	// UPDATE GROWTH & PROGRESSION
	// ============================================================

	if (LevelText)
	{
		LevelText->SetText(FText::FromString(FString::Printf(TEXT("Level %d"), NajikaState.Level)));
	}

	if (XPText)
	{
		// XP calculation (simple formula: 100 * Level^1.5)
		int32 XPToNext = FMath::RoundToInt(100.0f * FMath::Pow(NajikaState.Level + 1, 1.5f));
		XPText->SetText(FText::FromString(FString::Printf(TEXT("%d / %d XP"), NajikaState.XP, XPToNext)));
	}

	if (XPBar)
	{
		int32 XPToNext = FMath::RoundToInt(100.0f * FMath::Pow(NajikaState.Level + 1, 1.5f));
		UpdateProgressBar(XPBar, static_cast<float>(NajikaState.XP), static_cast<float>(XPToNext));
	}

	if (EvolutionStageText)
	{
		FString GermanStage = TranslateGerman(NajikaState.EvolutionStage);
		EvolutionStageText->SetText(FText::FromString(FString::Printf(TEXT("Entwicklung: %s"), *GermanStage)));
	}

	// ============================================================
	// UPDATE CARE TRACKING
	// ============================================================

	if (CareMistakesText)
	{
		CareMistakesText->SetText(FText::FromString(FString::Printf(TEXT("Pflegefehler: %d"), NajikaState.CareMistakes)));

		// Color based on mistakes (red if > 10)
		FLinearColor Color = NajikaState.CareMistakes > 10 ? FLinearColor::Red : FLinearColor::White;
		CareMistakesText->SetColorAndOpacity(FSlateColor(Color));
	}

	if (WeightText)
	{
		WeightText->SetText(FText::FromString(FString::Printf(TEXT("Gewicht: %.1f kg"), NajikaState.Weight)));
	}

	UpdateProgressBar(DisciplineBar, NajikaState.Discipline);
	if (DisciplineText)
	{
		DisciplineText->SetText(FText::FromString(FString::Printf(TEXT("Disziplin: %.0f%%"), NajikaState.Discipline)));
	}

	UpdateProgressBar(FatigueBar, NajikaState.Fatigue);
	if (FatigueText)
	{
		FatigueText->SetText(FText::FromString(FString::Printf(TEXT("Müdigkeit: %.0f%%"), NajikaState.Fatigue)));
	}

	// ============================================================
	// UPDATE EQUIPMENT
	// ============================================================

	if (WeaponText)
	{
		FString Weapon = NajikaState.Equipment.Weapon.IsEmpty() ? TEXT("Keine") : NajikaState.Equipment.Weapon;
		WeaponText->SetText(FText::FromString(Weapon));
	}

	if (ArmorText)
	{
		FString Armor = NajikaState.Equipment.Armor.IsEmpty() ? TEXT("Keine") : NajikaState.Equipment.Armor;
		ArmorText->SetText(FText::FromString(Armor));
	}

	if (AccessoryText)
	{
		FString Accessory = NajikaState.Equipment.Accessory.IsEmpty() ? TEXT("Keine") : NajikaState.Equipment.Accessory;
		AccessoryText->SetText(FText::FromString(Accessory));
	}

	// ============================================================
	// UPDATE LIVING SYSTEM STATE
	// ============================================================

	if (MoodText)
	{
		FString MoodEmoji = GetMoodEmoji(LivingState.CurrentMood);
		FString GermanMood = TranslateGerman(LivingState.CurrentMood);
		MoodText->SetText(FText::FromString(FString::Printf(TEXT("Stimmung: %s %s"), *GermanMood, *MoodEmoji)));
	}

	UpdateProgressBar(MoodIntensityBar, static_cast<float>(LivingState.MoodIntensity));
	if (MoodIntensityBar)
	{
		// Set bar color based on mood
		FLinearColor MoodColor = FLinearColor::White;
		if (LivingState.CurrentMood == TEXT("happy")) MoodColor = FLinearColor::Green;
		else if (LivingState.CurrentMood == TEXT("sad")) MoodColor = FLinearColor(0.3f, 0.3f, 1.0f); // Blue
		else if (LivingState.CurrentMood == TEXT("angry")) MoodColor = FLinearColor::Red;
		else if (LivingState.CurrentMood == TEXT("excited")) MoodColor = FLinearColor::Yellow;

		MoodIntensityBar->SetFillColorAndOpacity(MoodColor);
	}

	if (ActivityText)
	{
		FString Activity = LivingState.CurrentActivity.IsEmpty() ? TEXT("Nichts") : TranslateGerman(LivingState.CurrentActivity);
		ActivityText->SetText(FText::FromString(FString::Printf(TEXT("Aktivität: %s"), *Activity)));
	}

	if (EmotionalBondText)
	{
		EmotionalBondText->SetText(FText::FromString(FString::Printf(TEXT("Gefühlsbindung: %d"), LivingState.EmotionalBond)));
	}

	if (RelationshipStageText)
	{
		FString GermanStage = TranslateGerman(LivingState.RelationshipStage);
		RelationshipStageText->SetText(FText::FromString(FString::Printf(TEXT("Beziehung: %s"), *GermanStage)));
	}

	UpdateProgressBar(AutonomyLevelBar, static_cast<float>(LivingState.AutonomyLevel));
	if (AutonomyLevelText)
	{
		AutonomyLevelText->SetText(FText::FromString(FString::Printf(TEXT("Autonomie: %d%%"), LivingState.AutonomyLevel)));
	}

	UE_LOG(LogTemp, Verbose, TEXT("[NajikaStatusWidget] Status display updated"));
}

void UNajikaStatusWidget::RefreshStatus()
{
	APlayerController* PC = GetOwningPlayer();
	if (!PC) return;

	ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
	if (!Najika || !Najika->BackendClient) return;

	UE_LOG(LogTemp, Log, TEXT("[NajikaStatusWidget] Refreshing status from backend..."));

	FOnNajikaStatusResponse Delegate;
	Delegate.BindDynamic(this, &UNajikaStatusWidget::OnStatusReceived);
	Najika->BackendClient->GetNajikaStatus(Delegate);
}

// ============================================================
// BUTTON HANDLERS
// ============================================================

void UNajikaStatusWidget::OnCloseButtonClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaStatusWidget] Close button clicked"));
	RemoveFromParent();
}

void UNajikaStatusWidget::OnRefreshButtonClicked()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaStatusWidget] Refresh button clicked"));
	RefreshStatus();
}

// ============================================================
// BACKEND CALLBACKS
// ============================================================

void UNajikaStatusWidget::OnStatusReceived(FNajikaState NajikaState, FNajikaLivingState LivingState)
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaStatusWidget] Status received from backend"));
	UpdateStatusDisplay(NajikaState, LivingState);
}

// ============================================================
// HELPER FUNCTIONS
// ============================================================

void UNajikaStatusWidget::UpdateProgressBar(UProgressBar* Bar, float Value, float Max)
{
	if (!Bar) return;

	float Percent = Max > 0.0f ? FMath::Clamp(Value / Max, 0.0f, 1.0f) : 0.0f;
	Bar->SetPercent(Percent);
	Bar->SetFillColorAndOpacity(GetStatusColor(Percent * 100.0f));
}

FLinearColor UNajikaStatusWidget::GetStatusColor(float Value) const
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

FString UNajikaStatusWidget::GetMoodEmoji(const FString& Mood) const
{
	if (Mood == TEXT("happy")) return TEXT("😊");
	if (Mood == TEXT("sad")) return TEXT("😢");
	if (Mood == TEXT("angry")) return TEXT("😠");
	if (Mood == TEXT("excited")) return TEXT("🤩");
	if (Mood == TEXT("tired")) return TEXT("😴");
	if (Mood == TEXT("hungry")) return TEXT("😋");
	if (Mood == TEXT("lonely")) return TEXT("🥺");
	if (Mood == TEXT("playful")) return TEXT("😁");
	if (Mood == TEXT("curious")) return TEXT("🤔");
	if (Mood == TEXT("neutral")) return TEXT("😐");
	return TEXT("😊");
}

FString UNajikaStatusWidget::TranslateGerman(const FString& EnglishText) const
{
	// Simple translation map
	static TMap<FString, FString> Translations = {
		{TEXT("base"), TEXT("Basis")},
		{TEXT("rookie"), TEXT("Anfänger")},
		{TEXT("champion"), TEXT("Champion")},
		{TEXT("ultimate"), TEXT("Ultimativ")},
		{TEXT("mega"), TEXT("Mega")},
		{TEXT("happy"), TEXT("Glücklich")},
		{TEXT("sad"), TEXT("Traurig")},
		{TEXT("angry"), TEXT("Wütend")},
		{TEXT("excited"), TEXT("Aufgeregt")},
		{TEXT("tired"), TEXT("Müde")},
		{TEXT("hungry"), TEXT("Hungrig")},
		{TEXT("lonely"), TEXT("Einsam")},
		{TEXT("playful"), TEXT("Verspielt")},
		{TEXT("curious"), TEXT("Neugierig")},
		{TEXT("neutral"), TEXT("Neutral")},
		{TEXT("getting_to_know"), TEXT("Kennenlernen")},
		{TEXT("friend"), TEXT("Freund")},
		{TEXT("close_friend"), TEXT("Enger Freund")},
		{TEXT("partner"), TEXT("Partner")},
		{TEXT("soulmate"), TEXT("Seelenverwandte")},
		{TEXT("reading"), TEXT("Lesen")},
		{TEXT("training"), TEXT("Training")},
		{TEXT("exploring"), TEXT("Erkunden")},
		{TEXT("resting"), TEXT("Ruhen")},
		{TEXT("playing"), TEXT("Spielen")},
	};

	const FString* Translation = Translations.Find(EnglishText);
	return Translation ? *Translation : EnglishText;
}
