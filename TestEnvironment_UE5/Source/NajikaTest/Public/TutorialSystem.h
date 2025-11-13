// TutorialSystem.h
// Complete Tutorial/Onboarding System with steps, hints, tooltips, progression tracking

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "TutorialSystem.generated.h"

// Tutorial Step Type
UENUM(BlueprintType)
enum class ETutorialStepType : uint8
{
    TS_Message UMETA(DisplayName = "Show Message"),
    TS_Highlight UMETA(DisplayName = "Highlight UI Element"),
    TS_WaitForInput UMETA(DisplayName = "Wait for Input"),
    TS_WaitForAction UMETA(DisplayName = "Wait for Action"),
    TS_PlayVideo UMETA(DisplayName = "Play Video"),
    TS_SpawnHelper UMETA(DisplayName = "Spawn Helper NPC"),
    TS_Custom UMETA(DisplayName = "Custom Event")
};

// Tutorial Category
UENUM(BlueprintType)
enum class ETutorialCategory : uint8
{
    TC_Basics UMETA(DisplayName = "Basics"),
    TC_Combat UMETA(DisplayName = "Combat"),
    TC_Crafting UMETA(DisplayName = "Crafting"),
    TC_Social UMETA(DisplayName = "Social/Multiplayer"),
    TC_Advanced UMETA(DisplayName = "Advanced Mechanics"),
    TC_Optional UMETA(DisplayName = "Optional Tips")
};

// Tooltip Position
UENUM(BlueprintType)
enum class ETooltipPosition : uint8
{
    TP_Top UMETA(DisplayName = "Top"),
    TP_Bottom UMETA(DisplayName = "Bottom"),
    TP_Left UMETA(DisplayName = "Left"),
    TP_Right UMETA(DisplayName = "Right"),
    TP_Center UMETA(DisplayName = "Center")
};

// Tutorial Step
USTRUCT(BlueprintType)
struct FTutorialStep
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString StepID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ETutorialStepType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Title;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Message;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Image = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString VideoPath;  // For video tutorials

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString HighlightWidgetName;  // UI element to highlight

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString WaitForActionID;  // Action to wait for (e.g., "OpenInventory")

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString WaitForInputKey;  // Input key to wait for (e.g., "I")

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCanSkip = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float AutoAdvanceDelay = 0.0f;  // Auto-advance after X seconds (0 = disabled)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector HelperSpawnLocation;  // For helper NPC

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSubclassOf<AActor> HelperClass;

    UPROPERTY(BlueprintReadWrite)
    bool bCompleted = false;
};

// Tutorial Sequence
USTRUCT(BlueprintType)
struct FTutorialSequence
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString SequenceID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString SequenceName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ETutorialCategory Category;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FTutorialStep> Steps;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bMandatory = false;  // Must complete before progressing

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bShowOnlyOnce = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TriggerEventID;  // Auto-start on this event

    UPROPERTY(BlueprintReadWrite)
    bool bCompleted = false;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentStepIndex = 0;

    bool IsComplete() const { return bCompleted; }
    int32 GetProgress() const { return CurrentStepIndex; }
    int32 GetTotalSteps() const { return Steps.Num(); }
    float GetProgressPercent() const { return Steps.Num() > 0 ? (float)CurrentStepIndex / (float)Steps.Num() : 0.0f; }
};

// Tooltip Data
USTRUCT(BlueprintType)
struct FTooltip
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TooltipID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Title;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ETooltipPosition Position = ETooltipPosition::TP_Bottom;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DisplayDuration = 5.0f;  // 0 = infinite

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bShowOnlyOnce = true;

    UPROPERTY(BlueprintReadWrite)
    bool bHasBeenShown = false;
};

// Hint Data
USTRUCT(BlueprintType)
struct FHint
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString HintID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString HintText;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ETutorialCategory Category;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TriggerCondition;  // When to show (e.g., "PlayerLevel >= 10")

    UPROPERTY(BlueprintReadWrite)
    bool bHasBeenShown = false;
};

UCLASS()
class NAJIKATEST_API ATutorialSystem : public AActor
{
    GENERATED_BODY()

public:
    ATutorialSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== TUTORIAL MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Management")
    void StartTutorial(const FString& SequenceID);

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Management")
    void AdvanceTutorial();

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Management")
    void SkipCurrentStep();

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Management")
    void CompleteTutorial(const FString& SequenceID);

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Management")
    void ResetTutorial(const FString& SequenceID);

    UFUNCTION(BlueprintPure, Category = "Tutorial|Management")
    bool IsTutorialActive() const { return bTutorialActive; }

    UFUNCTION(BlueprintPure, Category = "Tutorial|Management")
    FString GetActiveTutorialID() const { return ActiveSequenceID; }

    // ========== STEP TRACKING ==========

    UFUNCTION(BlueprintPure, Category = "Tutorial|Steps")
    FTutorialStep GetCurrentStep() const;

    UFUNCTION(BlueprintPure, Category = "Tutorial|Steps")
    int32 GetCurrentStepIndex() const;

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Steps")
    void CompleteStep(const FString& StepID);

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Steps")
    void OnActionPerformed(const FString& ActionID);

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Steps")
    void OnInputReceived(const FString& InputKey);

    // ========== PROGRESS QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "Tutorial|Progress")
    bool IsTutorialCompleted(const FString& SequenceID) const;

    UFUNCTION(BlueprintPure, Category = "Tutorial|Progress")
    TArray<FString> GetCompletedTutorials() const { return CompletedTutorials; }

    UFUNCTION(BlueprintPure, Category = "Tutorial|Progress")
    float GetTutorialProgress(const FString& SequenceID) const;

    UFUNCTION(BlueprintPure, Category = "Tutorial|Progress")
    int32 GetOverallTutorialCompletion() const;

    // ========== TOOLTIPS ==========

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Tooltips")
    void ShowTooltip(const FString& TooltipID);

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Tooltips")
    void HideTooltip();

    UFUNCTION(BlueprintPure, Category = "Tutorial|Tooltips")
    bool ShouldShowTooltip(const FString& TooltipID) const;

    // ========== HINTS ==========

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Hints")
    void ShowHint(const FString& HintID);

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Hints")
    void CheckAndShowContextualHints();

    UFUNCTION(BlueprintPure, Category = "Tutorial|Hints")
    TArray<FHint> GetAvailableHints() const;

    // ========== TUTORIAL CREATION ==========

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Creation")
    void RegisterTutorial(const FTutorialSequence& Tutorial);

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Creation")
    void UnregisterTutorial(const FString& SequenceID);

    UFUNCTION(BlueprintPure, Category = "Tutorial|Creation")
    FTutorialSequence GetTutorial(const FString& SequenceID) const;

    // ========== SETTINGS ==========

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Settings")
    void SetTutorialsEnabled(bool bEnabled);

    UFUNCTION(BlueprintPure, Category = "Tutorial|Settings")
    bool AreTutorialsEnabled() const { return bTutorialsEnabled; }

    UFUNCTION(BlueprintCallable, Category = "Tutorial|Settings")
    void ResetAllTutorials();

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTutorialStarted, FString, SequenceID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTutorialCompleted, FString, SequenceID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnStepChanged, FString, SequenceID, int32, StepIndex);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTooltipShown, FString, TooltipID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHintShown, FString, HintID);

    UPROPERTY(BlueprintAssignable, Category = "Tutorial|Events")
    FOnTutorialStarted OnTutorialStarted;

    UPROPERTY(BlueprintAssignable, Category = "Tutorial|Events")
    FOnTutorialCompleted OnTutorialCompleted;

    UPROPERTY(BlueprintAssignable, Category = "Tutorial|Events")
    FOnStepChanged OnStepChanged;

    UPROPERTY(BlueprintAssignable, Category = "Tutorial|Events")
    FOnTooltipShown OnTooltipShown;

    UPROPERTY(BlueprintAssignable, Category = "Tutorial|Events")
    FOnHintShown OnHintShown;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tutorial|Config")
    TMap<FString, FTutorialSequence> Tutorials;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tutorial|Config")
    TMap<FString, FTooltip> Tooltips;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tutorial|Config")
    TArray<FHint> Hints;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tutorial|Config")
    bool bTutorialsEnabled = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tutorial|Config")
    bool bShowTooltipsByDefault = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tutorial|Config")
    bool bShowHintsByDefault = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Tutorial|Config")
    float AutoCheckHintsInterval = 5.0f;  // Check for contextual hints every 5 seconds

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Tutorial|State")
    bool bTutorialActive = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Tutorial|State")
    FString ActiveSequenceID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Tutorial|State")
    TArray<FString> CompletedTutorials;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Tutorial|State")
    TArray<FString> ShownTooltips;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Tutorial|State")
    TArray<FString> ShownHints;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Tutorial|State")
    float TimeSinceLastHintCheck = 0.0f;

private:
    // ========== HELPER FUNCTIONS ==========

    void ProcessCurrentStep(float DeltaTime);
    void CheckAutoAdvance(float DeltaTime);
    void HighlightUIElement(const FString& WidgetName);
    void ClearUIHighlight();
    bool EvaluateCondition(const FString& Condition) const;
    void SpawnHelperNPC(const FTutorialStep& Step);
};
