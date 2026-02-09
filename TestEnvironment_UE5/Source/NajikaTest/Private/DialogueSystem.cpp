// DialogueSystem.cpp
// NPC Dialogue System Implementation

#include "DialogueSystem.h"
#include "QuestSystem.h"
#include "InventoryComponent.h"

ADialogueSystem::ADialogueSystem()
{
    PrimaryActorTick.bCanEverTick = false;
}

void ADialogueSystem::BeginPlay()
{
    Super::BeginPlay();
}

// ========== DIALOGUE CONTROL ==========

void ADialogueSystem::StartDialogue(const FString& DialogueID, AActor* PlayerActor)
{
    if (!DialogueDatabase.Contains(DialogueID)) return;

    CurrentDialogue = DialogueDatabase[DialogueID];
    CurrentPlayer = PlayerActor;
    CurrentNodeIndex = 0;
    bIsActive = true;

    // Show first node
    ShowCurrentNode();

    OnDialogueStarted.Broadcast(DialogueID);
}

void ADialogueSystem::ShowCurrentNode()
{
    if (!bIsActive || CurrentNodeIndex >= CurrentDialogue.Nodes.Num()) return;

    FDialogueNode& Node = CurrentDialogue.Nodes[CurrentNodeIndex];

    // Check conditions
    if (!CheckConditions(Node.Conditions))
    {
        // Skip to next node
        AdvanceDialogue(Node.NextNodeID);
        return;
    }

    // Execute actions
    ExecuteActions(Node.Actions);

    // Show node to UI
    OnNodeShown.Broadcast(Node);

    // Auto-advance if configured
    if (Node.AutoAdvanceDelay > 0.0f)
    {
        FTimerHandle TimerHandle;
        GetWorld()->GetTimerManager().SetTimer(TimerHandle, [this, Node]()
        {
            AdvanceDialogue(Node.NextNodeID);
        }, Node.AutoAdvanceDelay, false);
    }
}

void ADialogueSystem::SelectChoice(int32 ChoiceIndex)
{
    if (!bIsActive || CurrentNodeIndex >= CurrentDialogue.Nodes.Num()) return;

    FDialogueNode& Node = CurrentDialogue.Nodes[CurrentNodeIndex];
    if (ChoiceIndex < 0 || ChoiceIndex >= Node.PlayerChoices.Num()) return;

    FDialogueChoice& Choice = Node.PlayerChoices[ChoiceIndex];

    // Check choice conditions
    if (!CheckConditions(Choice.Conditions)) return;

    // Execute choice actions
    ExecuteActions(Choice.Actions);

    OnChoiceSelected.Broadcast(ChoiceIndex, Choice.ChoiceText);

    // Advance or close
    if (Choice.bCloseDialogue)
    {
        EndDialogue();
    }
    else
    {
        AdvanceDialogue(Choice.NextNodeID);
    }
}

void ADialogueSystem::AdvanceDialogue(const FString& NextNodeID)
{
    if (NextNodeID.IsEmpty())
    {
        EndDialogue();
        return;
    }

    // Find next node
    for (int32 i = 0; i < CurrentDialogue.Nodes.Num(); i++)
    {
        if (CurrentDialogue.Nodes[i].NodeID == NextNodeID)
        {
            CurrentNodeIndex = i;
            ShowCurrentNode();
            return;
        }
    }

    // Node not found - end dialogue
    EndDialogue();
}

void ADialogueSystem::EndDialogue()
{
    bIsActive = false;
    OnDialogueEnded.Broadcast();
}

// ========== HELPERS ==========

bool ADialogueSystem::CheckConditions(const TArray<FDialogueCondition>& Conditions) const
{
    if (!CurrentPlayer) return true; // No conditions = always true

    for (const FDialogueCondition& Condition : Conditions)
    {
        bool ConditionMet = false;

        switch (Condition.Type)
        {
            case EDialogueConditionType::DC_QuestActive:
            {
                UQuestSystem* QuestSystem = CurrentPlayer->FindComponentByClass<UQuestSystem>();
                ConditionMet = QuestSystem && QuestSystem->IsQuestActive(Condition.TargetID);
                break;
            }
            case EDialogueConditionType::DC_QuestComplete:
            {
                UQuestSystem* QuestSystem = CurrentPlayer->FindComponentByClass<UQuestSystem>();
                ConditionMet = QuestSystem && QuestSystem->IsQuestCompleted(Condition.TargetID);
                break;
            }
            case EDialogueConditionType::DC_ItemInInventory:
            {
                UInventoryComponent* Inventory = CurrentPlayer->FindComponentByClass<UInventoryComponent>();
                ConditionMet = Inventory && Inventory->HasItem(Condition.TargetID, Condition.RequiredValue);
                break;
            }
            default:
                ConditionMet = true; // Unknown conditions pass
        }

        // Apply invert
        if (Condition.bInvert) ConditionMet = !ConditionMet;

        // All conditions must be met
        if (!ConditionMet) return false;
    }

    return true;
}

void ADialogueSystem::ExecuteActions(const TArray<FDialogueAction>& Actions)
{
    if (!CurrentPlayer) return;

    for (const FDialogueAction& Action : Actions)
    {
        switch (Action.Type)
        {
            case EDialogueActionType::DA_GiveQuest:
            {
                UQuestSystem* QuestSystem = CurrentPlayer->FindComponentByClass<UQuestSystem>();
                if (QuestSystem)
                {
                    QuestSystem->StartQuest(Action.TargetID);
                }
                break;
            }
            case EDialogueActionType::DA_CompleteQuest:
            {
                UQuestSystem* QuestSystem = CurrentPlayer->FindComponentByClass<UQuestSystem>();
                if (QuestSystem)
                {
                    QuestSystem->CompleteQuest(Action.TargetID);
                }
                break;
            }
            case EDialogueActionType::DA_GiveItem:
            {
                UInventoryComponent* Inventory = CurrentPlayer->FindComponentByClass<UInventoryComponent>();
                if (Inventory)
                {
                    FItemData Item;
                    Item.ItemID = Action.TargetID;
                    Inventory->AddItem(Item, Action.Value);
                }
                break;
            }
            case EDialogueActionType::DA_GiveGold:
            {
                UInventoryComponent* Inventory = CurrentPlayer->FindComponentByClass<UInventoryComponent>();
                if (Inventory)
                {
                    Inventory->Gold += Action.Value;
                }
                break;
            }
            default:
                break;
        }
    }
}

FDialogueNode ADialogueSystem::GetCurrentNode() const
{
    if (bIsActive && CurrentNodeIndex < CurrentDialogue.Nodes.Num())
    {
        return CurrentDialogue.Nodes[CurrentNodeIndex];
    }
    return FDialogueNode();
}

TArray<FDialogueChoice> ADialogueSystem::GetAvailableChoices() const
{
    TArray<FDialogueChoice> Result;

    if (!bIsActive || CurrentNodeIndex >= CurrentDialogue.Nodes.Num()) return Result;

    const FDialogueNode& Node = CurrentDialogue.Nodes[CurrentNodeIndex];
    for (const FDialogueChoice& Choice : Node.PlayerChoices)
    {
        if (CheckConditions(Choice.Conditions))
        {
            Result.Add(Choice);
        }
    }

    return Result;
}
