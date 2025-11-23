// DialogueSystem.h
// Complete NPC Dialogue System with branching conversations, choices, conditions

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "DialogueSystem.generated.h"

// Dialogue Node Type
UENUM(BlueprintType)
enum class EDialogueNodeType : uint8
{
    DN_NPC UMETA(DisplayName = "NPC Line"),
    DN_PlayerChoice UMETA(DisplayName = "Player Choice"),
    DN_Branch UMETA(DisplayName = "Conditional Branch"),
    DN_Action UMETA(DisplayName = "Action/Event"),
    DN_End UMETA(DisplayName = "End Dialogue")
};

// Dialogue Condition Type
UENUM(BlueprintType)
enum class EDialogueConditionType : uint8
{
    DC_QuestActive UMETA(DisplayName = "Quest Active"),
    DC_QuestComplete UMETA(DisplayName = "Quest Complete"),
    DC_ItemInInventory UMETA(DisplayName = "Has Item"),
    DC_PlayerLevel UMETA(DisplayName = "Player Level"),
    DC_FactionReputation UMETA(DisplayName = "Faction Reputation"),
    DC_SkillLevel UMETA(DisplayName = "Skill Level"),
    DC_Flag UMETA(DisplayName = "World Flag"),
    DC_Gold UMETA(DisplayName = "Has Gold")
};

// Dialogue Action Type
UENUM(BlueprintType)
enum class EDialogueActionType : uint8
{
    DA_GiveQuest UMETA(DisplayName = "Give Quest"),
    DA_CompleteQuest UMETA(DisplayName = "Complete Quest"),
    DA_GiveItem UMETA(DisplayName = "Give Item"),
    DA_TakeItem UMETA(DisplayName = "Take Item"),
    DA_GiveGold UMETA(DisplayName = "Give Gold"),
    DA_TakeGold UMETA(DisplayName = "Take Gold"),
    DA_SetFlag UMETA(DisplayName = "Set Flag"),
    DA_OpenShop UMETA(DisplayName = "Open Shop"),
    DA_StartCombat UMETA(DisplayName = "Start Combat"),
    DA_PlayAnimation UMETA(DisplayName = "Play Animation")
};

// Dialogue Condition
USTRUCT(BlueprintType)
struct FDialogueCondition
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EDialogueConditionType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TargetID;  // QuestID, ItemID, FactionID, etc.

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredValue = 0;  // Level, count, reputation, etc.

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bInvert = false;  // Check for NOT condition
};

// Dialogue Action
USTRUCT(BlueprintType)
struct FDialogueAction
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EDialogueActionType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TargetID;  // QuestID, ItemID, ShopID, etc.

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Value = 0;  // Amount, count, etc.

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString AnimationName;  // For PlayAnimation
};

// Player Choice
USTRUCT(BlueprintType)
struct FDialogueChoice
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ChoiceText;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString NextNodeID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FDialogueCondition> Conditions;  // Choice only available if conditions met

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FDialogueAction> Actions;  // Execute when choice is selected

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCloseDialogue = false;  // Close dialogue after this choice
};

// Dialogue Node
USTRUCT(BlueprintType)
struct FDialogueNode
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString NodeID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EDialogueNodeType NodeType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString NPCText;  // What the NPC says

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString NPCName;  // Who is speaking

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* NPCPortrait = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FDialogueChoice> PlayerChoices;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FDialogueCondition> Conditions;  // Node only shown if conditions met

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FDialogueAction> Actions;  // Execute when node is shown

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString NextNodeID;  // For auto-advance (non-choice nodes)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString VoiceFile;  // Audio file for voice acting

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float AutoAdvanceDelay = 0.0f;  // Auto-advance after X seconds (0 = disabled)
};

// Dialogue Tree
USTRUCT(BlueprintType)
struct FDialogueTree
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString DialogueID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString DialogueName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString StartNodeID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, FDialogueNode> Nodes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCanBeRepeated = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bSaveHistory = true;  // Save dialogue history for player
};

UCLASS()
class NAJIKATEST_API ADialogueSystem : public AActor
{
    GENERATED_BODY()

public:
    ADialogueSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== DIALOGUE MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Dialogue")
    void StartDialogue(const FString& DialogueID, AActor* NPCActor, APlayerController* Player);

    UFUNCTION(BlueprintCallable, Category = "Dialogue")
    void EndDialogue();

    UFUNCTION(BlueprintCallable, Category = "Dialogue")
    void SelectChoice(int32 ChoiceIndex);

    UFUNCTION(BlueprintCallable, Category = "Dialogue")
    void AdvanceDialogue();  // For auto-advance or "Continue" button

    UFUNCTION(BlueprintPure, Category = "Dialogue")
    bool IsDialogueActive() const { return bDialogueActive; }

    // ========== CURRENT STATE ==========

    UFUNCTION(BlueprintPure, Category = "Dialogue|State")
    FDialogueNode GetCurrentNode() const;

    UFUNCTION(BlueprintPure, Category = "Dialogue|State")
    TArray<FDialogueChoice> GetAvailableChoices() const;

    UFUNCTION(BlueprintPure, Category = "Dialogue|State")
    FString GetCurrentSpeaker() const;

    UFUNCTION(BlueprintPure, Category = "Dialogue|State")
    UTexture2D* GetCurrentPortrait() const;

    // ========== CONDITION CHECKING ==========

    UFUNCTION(BlueprintPure, Category = "Dialogue|Conditions")
    bool CheckCondition(const FDialogueCondition& Condition, APlayerController* Player) const;

    UFUNCTION(BlueprintPure, Category = "Dialogue|Conditions")
    bool CheckAllConditions(const TArray<FDialogueCondition>& Conditions, APlayerController* Player) const;

    // ========== ACTION EXECUTION ==========

    UFUNCTION(BlueprintCallable, Category = "Dialogue|Actions")
    void ExecuteAction(const FDialogueAction& Action, APlayerController* Player);

    UFUNCTION(BlueprintCallable, Category = "Dialogue|Actions")
    void ExecuteActions(const TArray<FDialogueAction>& Actions, APlayerController* Player);

    // ========== DIALOGUE HISTORY ==========

    UFUNCTION(BlueprintPure, Category = "Dialogue|History")
    bool HasSeenDialogue(const FString& DialogueID) const;

    UFUNCTION(BlueprintPure, Category = "Dialogue|History")
    TArray<FString> GetDialogueHistory() const { return DialogueHistory; }

    UFUNCTION(BlueprintCallable, Category = "Dialogue|History")
    void ClearDialogueHistory();

    // ========== DIALOGUE CREATION ==========

    UFUNCTION(BlueprintCallable, Category = "Dialogue|Creation")
    void RegisterDialogue(const FDialogueTree& Dialogue);

    UFUNCTION(BlueprintCallable, Category = "Dialogue|Creation")
    void UnregisterDialogue(const FString& DialogueID);

    UFUNCTION(BlueprintPure, Category = "Dialogue|Creation")
    FDialogueTree GetDialogue(const FString& DialogueID) const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnDialogueStarted, FString, DialogueID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnDialogueEnded);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNodeChanged, FDialogueNode, NewNode);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnChoiceSelected, int32, ChoiceIndex);

    UPROPERTY(BlueprintAssignable, Category = "Dialogue|Events")
    FOnDialogueStarted OnDialogueStarted;

    UPROPERTY(BlueprintAssignable, Category = "Dialogue|Events")
    FOnDialogueEnded OnDialogueEnded;

    UPROPERTY(BlueprintAssignable, Category = "Dialogue|Events")
    FOnNodeChanged OnNodeChanged;

    UPROPERTY(BlueprintAssignable, Category = "Dialogue|Events")
    FOnChoiceSelected OnChoiceSelected;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dialogue|Config")
    TMap<FString, FDialogueTree> Dialogues;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dialogue|Config")
    bool bPauseGameDuringDialogue = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dialogue|Config")
    bool bShowSubtitles = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dialogue|Config")
    float DefaultTextSpeed = 50.0f;  // Characters per second

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dialogue|State")
    bool bDialogueActive = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dialogue|State")
    FString CurrentDialogueID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dialogue|State")
    FString CurrentNodeID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dialogue|State")
    AActor* CurrentNPC = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dialogue|State")
    APlayerController* CurrentPlayer = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Dialogue|State")
    TArray<FString> DialogueHistory;  // DialogueIDs that player has seen

private:
    // ========== HELPER FUNCTIONS ==========

    void NavigateToNode(const FString& NodeID);
    FDialogueNode* FindNode(const FString& NodeID);
    void ProcessNodeActions(const FDialogueNode& Node);
    TArray<FDialogueChoice> FilterAvailableChoices(const TArray<FDialogueChoice>& Choices);
};
