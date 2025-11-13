// TutorialSystem.cpp
// Tutorial/Onboarding System Implementation

#include "TutorialSystem.h"

ATutorialSystem::ATutorialSystem()
{
    PrimaryActorTick.bCanEverTick = false;
}

void ATutorialSystem::BeginPlay()
{
    Super::BeginPlay();
}

// ========== TUTORIAL CONTROL ==========

void ATutorialSystem::StartTutorial(const FString& SequenceID)
{
    if (!TutorialDatabase.Contains(SequenceID)) return;
    if (CompletedTutorials.Contains(SequenceID)) return; // Already completed

    CurrentTutorial = TutorialDatabase[SequenceID];
    CurrentTutorial.CurrentStepIndex = 0;
    bIsActive = true;

    OnTutorialStarted.Broadcast(SequenceID);

    ShowCurrentStep();
}

void ATutorialSystem::ShowCurrentStep()
{
    if (!bIsActive || CurrentTutorial.CurrentStepIndex >= CurrentTutorial.Steps.Num())
    {
        // Tutorial complete
        CompleteTutorial();
        return;
    }

    FTutorialStep& Step = CurrentTutorial.Steps[CurrentTutorial.CurrentStepIndex];

    // Show step to UI
    OnStepShown.Broadcast(Step);

    // Auto-advance if configured
    if (Step.AutoAdvanceDelay > 0.0f)
    {
        FTimerHandle TimerHandle;
        GetWorld()->GetTimerManager().SetTimer(TimerHandle, [this]()
        {
            NextStep();
        }, Step.AutoAdvanceDelay, false);
    }

    // Spawn helper if needed
    if (Step.Type == ETutorialStepType::TS_SpawnHelper && Step.HelperClass)
    {
        FActorSpawnParameters SpawnParams;
        GetWorld()->SpawnActor<AActor>(Step.HelperClass, Step.HelperSpawnLocation, FRotator::ZeroRotator, SpawnParams);
    }
}

void ATutorialSystem::NextStep()
{
    if (!bIsActive) return;

    if (CurrentTutorial.CurrentStepIndex < CurrentTutorial.Steps.Num())
    {
        CurrentTutorial.Steps[CurrentTutorial.CurrentStepIndex].bCompleted = true;
        OnStepCompleted.Broadcast(CurrentTutorial.CurrentStepIndex);
    }

    CurrentTutorial.CurrentStepIndex++;
    ShowCurrentStep();
}

void ATutorialSystem::SkipCurrentStep()
{
    if (!bIsActive) return;

    if (CurrentTutorial.CurrentStepIndex < CurrentTutorial.Steps.Num())
    {
        FTutorialStep& Step = CurrentTutorial.Steps[CurrentTutorial.CurrentStepIndex];
        if (Step.bCanSkip)
        {
            NextStep();
        }
    }
}

void ATutorialSystem::CompleteTutorial()
{
    if (!bIsActive) return;

    CurrentTutorial.bCompleted = true;
    CompletedTutorials.Add(CurrentTutorial.SequenceID);
    bIsActive = false;

    OnTutorialCompleted.Broadcast(CurrentTutorial.SequenceID);
}

void ATutorialSystem::CancelTutorial()
{
    bIsActive = false;
    OnTutorialCancelled.Broadcast(CurrentTutorial.SequenceID);
}

// ========== ACTION TRACKING ==========

void ATutorialSystem::NotifyActionPerformed(const FString& ActionID)
{
    if (!bIsActive || CurrentTutorial.CurrentStepIndex >= CurrentTutorial.Steps.Num()) return;

    FTutorialStep& Step = CurrentTutorial.Steps[CurrentTutorial.CurrentStepIndex];

    if (Step.Type == ETutorialStepType::TS_WaitForAction && Step.WaitForActionID == ActionID)
    {
        NextStep();
    }
}

void ATutorialSystem::NotifyInputPressed(const FString& InputKey)
{
    if (!bIsActive || CurrentTutorial.CurrentStepIndex >= CurrentTutorial.Steps.Num()) return;

    FTutorialStep& Step = CurrentTutorial.Steps[CurrentTutorial.CurrentStepIndex];

    if (Step.Type == ETutorialStepType::TS_WaitForInput && Step.WaitForInputKey == InputKey)
    {
        NextStep();
    }
}

// ========== TOOLTIPS ==========

void ATutorialSystem::ShowTooltip(const FString& TooltipID)
{
    if (TooltipDatabase.Contains(TooltipID))
    {
        FTooltip Tooltip = TooltipDatabase[TooltipID];
        OnTooltipShown.Broadcast(Tooltip);
    }
}

void ATutorialSystem::HideTooltip(const FString& TooltipID)
{
    OnTooltipHidden.Broadcast(TooltipID);
}

// ========== QUERIES ==========

bool ATutorialSystem::IsTutorialCompleted(const FString& SequenceID) const
{
    return CompletedTutorials.Contains(SequenceID);
}

FTutorialSequence ATutorialSystem::GetCurrentTutorial() const
{
    return CurrentTutorial;
}

FTutorialStep ATutorialSystem::GetCurrentStep() const
{
    if (bIsActive && CurrentTutorial.CurrentStepIndex < CurrentTutorial.Steps.Num())
    {
        return CurrentTutorial.Steps[CurrentTutorial.CurrentStepIndex];
    }
    return FTutorialStep();
}

TArray<FTutorialSequence> ATutorialSystem::GetAvailableTutorials() const
{
    TArray<FTutorialSequence> Result;
    for (const auto& Pair : TutorialDatabase)
    {
        if (!IsTutorialCompleted(Pair.Key))
        {
            Result.Add(Pair.Value);
        }
    }
    return Result;
}

float ATutorialSystem::GetTutorialProgress(const FString& SequenceID) const
{
    if (TutorialDatabase.Contains(SequenceID))
    {
        return TutorialDatabase[SequenceID].GetProgressPercent();
    }
    return 0.0f;
}
