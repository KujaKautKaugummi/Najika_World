// QuestSystem.cpp
// Complete Quest System Implementation

#include "QuestSystem.h"
#include "InventoryComponent.h"
#include "ProgressionComponent.h"

UQuestSystem::UQuestSystem()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UQuestSystem::BeginPlay()
{
    Super::BeginPlay();
}

// ========== QUEST MANAGEMENT ==========

bool UQuestSystem::StartQuest(const FString& QuestID)
{
    if (!QuestDatabase.Contains(QuestID)) return false;
    if (IsQuestActive(QuestID) || IsQuestCompleted(QuestID)) return false;

    FQuest& Quest = QuestDatabase[QuestID];

    // Check prerequisites
    if (!CanStartQuest(QuestID)) return false;

    // Start quest
    Quest.Status = EQuestStatus::QS_Active;
    ActiveQuests.Add(QuestID);

    // Reset objectives
    for (FQuestObjective& Objective : Quest.Objectives)
    {
        Objective.CurrentCount = 0;
        Objective.bIsCompleted = false;
    }

    OnQuestStarted.Broadcast(Quest);
    return true;
}

bool UQuestSystem::CompleteQuest(const FString& QuestID)
{
    if (!IsQuestActive(QuestID)) return false;
    if (!AreAllObjectivesComplete(QuestID)) return false;

    FQuest& Quest = QuestDatabase[QuestID];
    Quest.Status = EQuestStatus::QS_Completed;

    OnQuestCompleted.Broadcast(Quest);
    return true;
}

bool UQuestSystem::TurnInQuest(const FString& QuestID)
{
    if (!IsQuestCompleted(QuestID)) return false;

    FQuest& Quest = QuestDatabase[QuestID];
    Quest.Status = EQuestStatus::QS_TurnedIn;

    // Remove from active
    ActiveQuests.Remove(QuestID);
    CompletedQuests.Add(QuestID);

    // Award rewards
    GiveQuestRewards(Quest.Reward);

    OnQuestTurnedIn.Broadcast(Quest);
    return true;
}

bool UQuestSystem::AbandonQuest(const FString& QuestID)
{
    if (!IsQuestActive(QuestID)) return false;

    FQuest& Quest = QuestDatabase[QuestID];
    if (!Quest.bCanAbandon) return false;

    Quest.Status = EQuestStatus::QS_NotStarted;
    ActiveQuests.Remove(QuestID);

    OnQuestAbandoned.Broadcast(QuestID);
    return true;
}

// ========== OBJECTIVE TRACKING ==========

void UQuestSystem::UpdateObjective(const FString& QuestID, const FString& ObjectiveID, int32 Progress)
{
    if (!QuestDatabase.Contains(QuestID)) return;

    FQuest& Quest = QuestDatabase[QuestID];
    if (Quest.Status != EQuestStatus::QS_Active) return;

    for (FQuestObjective& Objective : Quest.Objectives)
    {
        if (Objective.ObjectiveID == ObjectiveID)
        {
            Objective.CurrentCount = FMath::Min(Objective.CurrentCount + Progress, Objective.RequiredCount);

            if (Objective.IsComplete() && !Objective.bIsCompleted)
            {
                Objective.bIsCompleted = true;
                OnObjectiveCompleted.Broadcast(QuestID, ObjectiveID);
            }

            // Check if all objectives complete
            if (AreAllObjectivesComplete(QuestID))
            {
                CompleteQuest(QuestID);
            }

            break;
        }
    }
}

void UQuestSystem::TrackKill(const FString& EnemyID)
{
    for (const FString& QuestID : ActiveQuests)
    {
        if (!QuestDatabase.Contains(QuestID)) continue;

        FQuest& Quest = QuestDatabase[QuestID];
        for (FQuestObjective& Objective : Quest.Objectives)
        {
            if (Objective.Type == EObjectiveType::OT_Kill && Objective.TargetID == EnemyID)
            {
                UpdateObjective(QuestID, Objective.ObjectiveID, 1);
            }
        }
    }
}

void UQuestSystem::TrackItemCollected(const FString& ItemID, int32 Amount)
{
    for (const FString& QuestID : ActiveQuests)
    {
        if (!QuestDatabase.Contains(QuestID)) continue;

        FQuest& Quest = QuestDatabase[QuestID];
        for (FQuestObjective& Objective : Quest.Objectives)
        {
            if (Objective.Type == EObjectiveType::OT_Collect && Objective.TargetID == ItemID)
            {
                UpdateObjective(QuestID, Objective.ObjectiveID, Amount);
            }
        }
    }
}

void UQuestSystem::TrackLocationReached(const FString& LocationID)
{
    for (const FString& QuestID : ActiveQuests)
    {
        if (!QuestDatabase.Contains(QuestID)) continue;

        FQuest& Quest = QuestDatabase[QuestID];
        for (FQuestObjective& Objective : Quest.Objectives)
        {
            if (Objective.Type == EObjectiveType::OT_Reach && Objective.TargetID == LocationID)
            {
                UpdateObjective(QuestID, Objective.ObjectiveID, 1);
            }
        }
    }
}

// ========== QUERIES ==========

bool UQuestSystem::IsQuestActive(const FString& QuestID) const
{
    return ActiveQuests.Contains(QuestID);
}

bool UQuestSystem::IsQuestCompleted(const FString& QuestID) const
{
    return CompletedQuests.Contains(QuestID);
}

FQuest UQuestSystem::GetQuest(const FString& QuestID) const
{
    if (QuestDatabase.Contains(QuestID))
    {
        return QuestDatabase[QuestID];
    }
    return FQuest();
}

TArray<FQuest> UQuestSystem::GetActiveQuests() const
{
    TArray<FQuest> Result;
    for (const FString& QuestID : ActiveQuests)
    {
        if (QuestDatabase.Contains(QuestID))
        {
            Result.Add(QuestDatabase[QuestID]);
        }
    }
    return Result;
}

TArray<FQuest> UQuestSystem::GetAvailableQuests() const
{
    TArray<FQuest> Result;
    for (const auto& Pair : QuestDatabase)
    {
        if (CanStartQuest(Pair.Key))
        {
            Result.Add(Pair.Value);
        }
    }
    return Result;
}

// ========== HELPER FUNCTIONS ==========

bool UQuestSystem::CanStartQuest(const FString& QuestID) const
{
    if (!QuestDatabase.Contains(QuestID)) return false;

    const FQuest& Quest = QuestDatabase[QuestID];

    // Check if already completed
    if (!Quest.bIsRepeatable && CompletedQuests.Contains(QuestID)) return false;

    // Check level requirement
    AActor* Owner = GetOwner();
    if (Owner)
    {
        UProgressionComponent* Progression = Owner->FindComponentByClass<UProgressionComponent>();
        if (Progression && Progression->GetLevel() < Quest.RequiredLevel) return false;
    }

    // Check prerequisites
    for (const FString& PrereqID : Quest.PrerequisiteQuests)
    {
        if (!IsQuestCompleted(PrereqID)) return false;
    }

    return true;
}

bool UQuestSystem::AreAllObjectivesComplete(const FString& QuestID) const
{
    if (!QuestDatabase.Contains(QuestID)) return false;

    const FQuest& Quest = QuestDatabase[QuestID];
    for (const FQuestObjective& Objective : Quest.Objectives)
    {
        if (!Objective.bIsOptional && !Objective.IsComplete())
        {
            return false;
        }
    }
    return true;
}

void UQuestSystem::GiveQuestRewards(const FQuestReward& Reward)
{
    AActor* Owner = GetOwner();
    if (!Owner) return;

    // Give XP
    if (Reward.Experience > 0)
    {
        UProgressionComponent* Progression = Owner->FindComponentByClass<UProgressionComponent>();
        if (Progression)
        {
            Progression->AddExperience(Reward.Experience);
        }
    }

    // Give Gold
    if (Reward.Gold > 0)
    {
        UInventoryComponent* Inventory = Owner->FindComponentByClass<UInventoryComponent>();
        if (Inventory)
        {
            Inventory->Gold += Reward.Gold;
        }
    }

    // Give Items
    if (Reward.ItemRewards.Num() > 0)
    {
        UInventoryComponent* Inventory = Owner->FindComponentByClass<UInventoryComponent>();
        if (Inventory)
        {
            for (int32 i = 0; i < Reward.ItemRewards.Num(); i++)
            {
                FItemData Item;
                Item.ItemID = Reward.ItemRewards[i];
                int32 Quantity = i < Reward.ItemQuantities.Num() ? Reward.ItemQuantities[i] : 1;
                Inventory->AddItem(Item, Quantity);
            }
        }
    }
}
