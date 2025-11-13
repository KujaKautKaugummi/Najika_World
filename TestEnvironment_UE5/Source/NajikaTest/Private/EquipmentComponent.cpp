// EquipmentComponent.cpp
// Complete Equipment System Implementation

#include "EquipmentComponent.h"

UEquipmentComponent::UEquipmentComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UEquipmentComponent::BeginPlay()
{
    Super::BeginPlay();

    // Initialize all equipment slots as empty
    EquippedItems.Add(EEquipmentSlot::ES_Head, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Chest, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Legs, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Feet, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Hands, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_MainHand, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_OffHand, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Back, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Accessory1, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Accessory2, FEquippedItem());
    EquippedItems.Add(EEquipmentSlot::ES_Accessory3, FEquippedItem());
}

// ========== EQUIP/UNEQUIP ==========

bool UEquipmentComponent::EquipItem(const FItemData& Item, EEquipmentSlot Slot)
{
    if (!CanEquipItem(Item, Slot)) return false;

    // Create equipped item
    FEquippedItem NewEquippedItem;
    NewEquippedItem.ItemData = Item;
    NewEquippedItem.Slot = Slot;
    NewEquippedItem.Stats = Item.Stats;
    NewEquippedItem.MaxDurability = 100; // TODO: Get from item data
    NewEquippedItem.Durability = NewEquippedItem.MaxDurability;

    // Unequip existing item in slot (if any)
    if (IsSlotEquipped(Slot))
    {
        UnequipItem(Slot);
    }

    // Equip new item
    EquippedItems[Slot] = NewEquippedItem;

    // Update stats and set bonuses
    CalculateStats();
    CheckSetBonuses();
    UpdateVisualEquipment();

    // Broadcast event
    OnItemEquipped.Broadcast(Slot, Item);

    return true;
}

bool UEquipmentComponent::UnequipItem(EEquipmentSlot Slot)
{
    if (!IsSlotEquipped(Slot)) return false;

    // Clear the slot
    EquippedItems[Slot] = FEquippedItem();

    // Update stats and set bonuses
    CalculateStats();
    CheckSetBonuses();
    UpdateVisualEquipment();

    // Broadcast event
    OnItemUnequipped.Broadcast(Slot);

    return true;
}

void UEquipmentComponent::UnequipAll()
{
    for (auto& Pair : EquippedItems)
    {
        if (!Pair.Value.IsEmpty())
        {
            UnequipItem(Pair.Key);
        }
    }
}

bool UEquipmentComponent::SwapEquipment(EEquipmentSlot Slot1, EEquipmentSlot Slot2)
{
    if (!EquippedItems.Contains(Slot1) || !EquippedItems.Contains(Slot2)) return false;

    FEquippedItem Temp = EquippedItems[Slot1];
    EquippedItems[Slot1] = EquippedItems[Slot2];
    EquippedItems[Slot2] = Temp;

    // Update slot references
    EquippedItems[Slot1].Slot = Slot1;
    EquippedItems[Slot2].Slot = Slot2;

    CalculateStats();
    CheckSetBonuses();
    UpdateVisualEquipment();

    return true;
}

// ========== QUERIES ==========

FEquippedItem UEquipmentComponent::GetEquippedItem(EEquipmentSlot Slot) const
{
    if (EquippedItems.Contains(Slot))
    {
        return EquippedItems[Slot];
    }
    return FEquippedItem();
}

bool UEquipmentComponent::IsSlotEquipped(EEquipmentSlot Slot) const
{
    return EquippedItems.Contains(Slot) && !EquippedItems[Slot].IsEmpty();
}

bool UEquipmentComponent::CanEquipItem(const FItemData& Item, EEquipmentSlot Slot) const
{
    // Check if item category matches slot
    // For simplicity, allowing all items in all slots (can be customized)
    return true;
}

// ========== STATS ==========

float UEquipmentComponent::GetTotalStat(const FString& StatName) const
{
    float TotalStat = 0.0f;

    // Sum stats from all equipped items
    for (const auto& Pair : EquippedItems)
    {
        if (!Pair.Value.IsEmpty())
        {
            const float* StatValue = Pair.Value.Stats.Find(StatName);
            if (StatValue)
            {
                TotalStat += *StatValue;
            }
        }
    }

    // Add set bonus stats
    TotalStat += GetSetBonusStat(StatName);

    return TotalStat;
}

TMap<FString, float> UEquipmentComponent::GetAllStats() const
{
    TMap<FString, float> AllStats;

    // Collect all unique stat names and sum them
    for (const auto& Pair : EquippedItems)
    {
        if (!Pair.Value.IsEmpty())
        {
            for (const auto& StatPair : Pair.Value.Stats)
            {
                if (AllStats.Contains(StatPair.Key))
                {
                    AllStats[StatPair.Key] += StatPair.Value;
                }
                else
                {
                    AllStats.Add(StatPair.Key, StatPair.Value);
                }
            }
        }
    }

    // Add set bonus stats
    TArray<FSetBonus> ActiveSetBonuses = GetActiveSetBonuses();
    for (const FSetBonus& SetBonus : ActiveSetBonuses)
    {
        for (const auto& BonusPair : SetBonus.Bonuses)
        {
            if (AllStats.Contains(BonusPair.Key))
            {
                AllStats[BonusPair.Key] *= BonusPair.Value; // Multiply for percentage bonuses
            }
            else
            {
                AllStats.Add(BonusPair.Key, BonusPair.Value);
            }
        }
    }

    return AllStats;
}

// ========== SET BONUSES ==========

TArray<FSetBonus> UEquipmentComponent::GetActiveSetBonuses() const
{
    TArray<FSetBonus> ActiveBonuses;
    TMap<FString, int32> SetPieceCounts;

    // Count equipped items per set
    for (const auto& Pair : EquippedItems)
    {
        if (!Pair.Value.IsEmpty() && !Pair.Value.SetName.IsEmpty())
        {
            if (SetPieceCounts.Contains(Pair.Value.SetName))
            {
                SetPieceCounts[Pair.Value.SetName]++;
            }
            else
            {
                SetPieceCounts.Add(Pair.Value.SetName, 1);
            }
        }
    }

    // Check which set bonuses are active
    for (const auto& SetPair : SetPieceCounts)
    {
        if (SetBonuses.Contains(SetPair.Key))
        {
            const FSetBonus& SetBonus = SetBonuses[SetPair.Key];
            if (SetPair.Value >= SetBonus.RequiredPieces)
            {
                ActiveBonuses.Add(SetBonus);
            }
        }
    }

    return ActiveBonuses;
}

bool UEquipmentComponent::HasSetBonus(const FString& SetName) const
{
    return GetSetPieceCount(SetName) >= (SetBonuses.Contains(SetName) ? SetBonuses[SetName].RequiredPieces : 999);
}

int32 UEquipmentComponent::GetSetPieceCount(const FString& SetName) const
{
    int32 Count = 0;
    for (const auto& Pair : EquippedItems)
    {
        if (!Pair.Value.IsEmpty() && Pair.Value.SetName == SetName)
        {
            Count++;
        }
    }
    return Count;
}

float UEquipmentComponent::GetSetBonusStat(const FString& StatName) const
{
    float BonusStat = 1.0f; // Multiplicative bonus (1.0 = no bonus)
    TArray<FSetBonus> ActiveBonuses = GetActiveSetBonuses();

    for (const FSetBonus& Bonus : ActiveBonuses)
    {
        const float* BonusValue = Bonus.Bonuses.Find(StatName);
        if (BonusValue)
        {
            BonusStat *= *BonusValue;
        }
    }

    return BonusStat;
}

// ========== DURABILITY ==========

void UEquipmentComponent::DamageEquipment(EEquipmentSlot Slot, int32 Amount)
{
    if (!bEnableDurability) return;
    if (!IsSlotEquipped(Slot)) return;

    FEquippedItem& Item = EquippedItems[Slot];
    Item.Durability = FMath::Max(0, Item.Durability - Amount);

    // Check if equipment is broken
    if (Item.Durability <= 0)
    {
        OnEquipmentBroken.Broadcast(Slot);
    }
}

void UEquipmentComponent::RepairEquipment(EEquipmentSlot Slot, int32 Amount)
{
    if (!IsSlotEquipped(Slot)) return;

    FEquippedItem& Item = EquippedItems[Slot];
    Item.Durability = FMath::Min(Item.MaxDurability, Item.Durability + Amount);
}

void UEquipmentComponent::RepairAll(int32 Amount)
{
    for (auto& Pair : EquippedItems)
    {
        if (!Pair.Value.IsEmpty())
        {
            Pair.Value.Durability = FMath::Min(Pair.Value.MaxDurability, Pair.Value.Durability + Amount);
        }
    }
}

bool UEquipmentComponent::IsEquipmentBroken(EEquipmentSlot Slot) const
{
    if (!IsSlotEquipped(Slot)) return false;
    return EquippedItems[Slot].Durability <= 0;
}

// ========== VISUAL ==========

void UEquipmentComponent::UpdateVisualEquipment()
{
    // TODO: Update character mesh with equipped items
    // This would update skeletal mesh components, materials, etc.
}

void UEquipmentComponent::HideHelmet(bool bHide)
{
    bHideHelmetEnabled = bHide;
    UpdateVisualEquipment();
}

// ========== HELPER FUNCTIONS ==========

void UEquipmentComponent::CalculateStats()
{
    // Stats are calculated on-demand via GetTotalStat()
    // This function can be used for caching if needed
}

void UEquipmentComponent::CheckSetBonuses()
{
    TArray<FSetBonus> ActiveBonuses = GetActiveSetBonuses();

    // Notify about activated set bonuses
    for (const FSetBonus& Bonus : ActiveBonuses)
    {
        OnSetBonusActivated.Broadcast(Bonus);
    }
}

void UEquipmentComponent::ApplySetBonus(const FSetBonus& SetBonus)
{
    // Set bonuses are applied automatically via GetAllStats()
}

void UEquipmentComponent::RemoveSetBonus(const FSetBonus& SetBonus)
{
    // Set bonuses are removed automatically when equipment changes
}

EEquipmentSlot UEquipmentComponent::GetSlotForItemCategory(EItemCategory Category) const
{
    // Map item category to equipment slot
    switch (Category)
    {
        case EItemCategory::IC_Weapon:
            return EEquipmentSlot::ES_MainHand;
        case EItemCategory::IC_Armor:
            return EEquipmentSlot::ES_Chest;
        default:
            return EEquipmentSlot::ES_Accessory1;
    }
}
