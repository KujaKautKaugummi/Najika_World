// InventoryComponent.cpp
// Complete Inventory System Implementation

#include "InventoryComponent.h"
#include "GameFramework/Actor.h"

UInventoryComponent::UInventoryComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UInventoryComponent::BeginPlay()
{
    Super::BeginPlay();

    // Initialize empty slots
    InventorySlots.SetNum(MaxSlots);
    for (int32 i = 0; i < MaxSlots; i++)
    {
        InventorySlots[i].SlotIndex = i;
        InventorySlots[i].Quantity = 0;
    }
}

// ========== ADD/REMOVE ITEMS ==========

bool UInventoryComponent::AddItem(const FItemData& Item, int32 Quantity)
{
    if (Quantity <= 0) return false;

    // Check if we can add the item
    if (!CanAddItem(Item, Quantity)) return false;

    int32 RemainingQuantity = Quantity;

    // Try to stack with existing items first (if auto-stack enabled)
    if (bAutoStack && Item.MaxStackSize > 1)
    {
        int32 PartialStackSlot = FindPartialStack(Item.ItemID);
        while (PartialStackSlot != -1 && RemainingQuantity > 0)
        {
            FInventorySlot& Slot = InventorySlots[PartialStackSlot];
            int32 SpaceInStack = Slot.GetRemainingSpace();
            int32 ToAdd = FMath::Min(SpaceInStack, RemainingQuantity);

            Slot.Quantity += ToAdd;
            RemainingQuantity -= ToAdd;

            // Look for next partial stack if needed
            if (RemainingQuantity > 0)
            {
                PartialStackSlot = FindPartialStack(Item.ItemID);
            }
            else
            {
                break;
            }
        }
    }

    // Add remaining to new slots
    while (RemainingQuantity > 0)
    {
        int32 EmptySlot = FindEmptySlot();
        if (EmptySlot == -1) break; // No more space

        int32 ToAdd = FMath::Min(Item.MaxStackSize, RemainingQuantity);

        InventorySlots[EmptySlot].ItemData = Item;
        InventorySlots[EmptySlot].Quantity = ToAdd;
        InventorySlots[EmptySlot].SlotIndex = EmptySlot;

        RemainingQuantity -= ToAdd;
    }

    // Broadcast events
    if (RemainingQuantity < Quantity) // At least some items added
    {
        OnItemAdded.Broadcast(Item, Quantity - RemainingQuantity);
        OnInventoryChanged.Broadcast();
    }

    return RemainingQuantity == 0; // True if all items added
}

bool UInventoryComponent::RemoveItem(const FString& ItemID, int32 Quantity)
{
    if (Quantity <= 0) return false;

    int32 TotalCount = GetItemCount(ItemID);
    if (TotalCount < Quantity) return false; // Not enough items

    int32 RemainingToRemove = Quantity;

    // Remove from slots (last to first to maintain slot order)
    for (int32 i = InventorySlots.Num() - 1; i >= 0 && RemainingToRemove > 0; i--)
    {
        FInventorySlot& Slot = InventorySlots[i];
        if (Slot.ItemData.ItemID == ItemID && Slot.Quantity > 0)
        {
            int32 ToRemove = FMath::Min(Slot.Quantity, RemainingToRemove);
            Slot.Quantity -= ToRemove;
            RemainingToRemove -= ToRemove;

            // Clear slot if empty
            if (Slot.Quantity <= 0)
            {
                Slot.ItemData = FItemData();
                Slot.Quantity = 0;
            }
        }
    }

    // Broadcast events
    OnItemRemoved.Broadcast(ItemID, Quantity);
    OnInventoryChanged.Broadcast();

    return true;
}

bool UInventoryComponent::RemoveItemAtSlot(int32 SlotIndex, int32 Quantity)
{
    if (SlotIndex < 0 || SlotIndex >= InventorySlots.Num()) return false;

    FInventorySlot& Slot = InventorySlots[SlotIndex];
    if (Slot.Quantity < Quantity) return false;

    FString ItemID = Slot.ItemData.ItemID;
    Slot.Quantity -= Quantity;

    // Clear slot if empty
    if (Slot.Quantity <= 0)
    {
        Slot.ItemData = FItemData();
        Slot.Quantity = 0;
    }

    OnItemRemoved.Broadcast(ItemID, Quantity);
    OnInventoryChanged.Broadcast();

    return true;
}

void UInventoryComponent::ClearInventory()
{
    for (FInventorySlot& Slot : InventorySlots)
    {
        Slot.ItemData = FItemData();
        Slot.Quantity = 0;
    }

    OnInventoryChanged.Broadcast();
}

// ========== ITEM QUERIES ==========

bool UInventoryComponent::HasItem(const FString& ItemID, int32 MinQuantity) const
{
    return GetItemCount(ItemID) >= MinQuantity;
}

int32 UInventoryComponent::GetItemCount(const FString& ItemID) const
{
    int32 TotalCount = 0;
    for (const FInventorySlot& Slot : InventorySlots)
    {
        if (Slot.ItemData.ItemID == ItemID)
        {
            TotalCount += Slot.Quantity;
        }
    }
    return TotalCount;
}

FInventorySlot UInventoryComponent::GetItemAtSlot(int32 SlotIndex) const
{
    if (SlotIndex >= 0 && SlotIndex < InventorySlots.Num())
    {
        return InventorySlots[SlotIndex];
    }
    return FInventorySlot();
}

TArray<FInventorySlot> UInventoryComponent::GetItemsByCategory(EItemCategory Category) const
{
    TArray<FInventorySlot> FilteredItems;
    for (const FInventorySlot& Slot : InventorySlots)
    {
        if (Slot.Quantity > 0 && Slot.ItemData.Category == Category)
        {
            FilteredItems.Add(Slot);
        }
    }
    return FilteredItems;
}

// ========== ITEM MANAGEMENT ==========

bool UInventoryComponent::MoveItem(int32 FromSlot, int32 ToSlot)
{
    if (FromSlot < 0 || FromSlot >= InventorySlots.Num()) return false;
    if (ToSlot < 0 || ToSlot >= InventorySlots.Num()) return false;
    if (FromSlot == ToSlot) return false;

    // Swap slots
    FInventorySlot Temp = InventorySlots[FromSlot];
    InventorySlots[FromSlot] = InventorySlots[ToSlot];
    InventorySlots[ToSlot] = Temp;

    // Update slot indices
    InventorySlots[FromSlot].SlotIndex = FromSlot;
    InventorySlots[ToSlot].SlotIndex = ToSlot;

    OnInventoryChanged.Broadcast();
    return true;
}

bool UInventoryComponent::SplitStack(int32 SlotIndex, int32 SplitAmount)
{
    if (SlotIndex < 0 || SlotIndex >= InventorySlots.Num()) return false;

    FInventorySlot& SourceSlot = InventorySlots[SlotIndex];
    if (SourceSlot.Quantity <= SplitAmount) return false; // Can't split entire stack
    if (SplitAmount <= 0) return false;

    // Find empty slot for split
    int32 EmptySlot = FindEmptySlot();
    if (EmptySlot == -1) return false;

    // Split the stack
    SourceSlot.Quantity -= SplitAmount;

    InventorySlots[EmptySlot].ItemData = SourceSlot.ItemData;
    InventorySlots[EmptySlot].Quantity = SplitAmount;
    InventorySlots[EmptySlot].SlotIndex = EmptySlot;

    OnInventoryChanged.Broadcast();
    return true;
}

bool UInventoryComponent::MergeStacks(int32 Slot1, int32 Slot2)
{
    if (Slot1 < 0 || Slot1 >= InventorySlots.Num()) return false;
    if (Slot2 < 0 || Slot2 >= InventorySlots.Num()) return false;
    if (Slot1 == Slot2) return false;

    FInventorySlot& Stack1 = InventorySlots[Slot1];
    FInventorySlot& Stack2 = InventorySlots[Slot2];

    // Check if items are the same
    if (Stack1.ItemData.ItemID != Stack2.ItemData.ItemID) return false;

    // Calculate merge
    int32 SpaceInStack1 = Stack1.GetRemainingSpace();
    int32 ToTransfer = FMath::Min(SpaceInStack1, Stack2.Quantity);

    Stack1.Quantity += ToTransfer;
    Stack2.Quantity -= ToTransfer;

    // Clear second stack if empty
    if (Stack2.Quantity <= 0)
    {
        Stack2.ItemData = FItemData();
        Stack2.Quantity = 0;
    }

    OnInventoryChanged.Broadcast();
    return true;
}

bool UInventoryComponent::DropItem(int32 SlotIndex, int32 Quantity)
{
    if (SlotIndex < 0 || SlotIndex >= InventorySlots.Num()) return false;

    FInventorySlot& Slot = InventorySlots[SlotIndex];
    if (Slot.Quantity < Quantity) return false;

    // Check if item can be dropped
    if (!Slot.ItemData.bCanDrop) return false;
    if (Slot.ItemData.bIsQuestItem && !bAllowQuestItemDrop) return false;

    // Remove item
    RemoveItemAtSlot(SlotIndex, Quantity);

    // TODO: Spawn physical item in world

    return true;
}

// ========== INVENTORY INFO ==========

int32 UInventoryComponent::GetEmptySlots() const
{
    int32 EmptyCount = 0;
    for (const FInventorySlot& Slot : InventorySlots)
    {
        if (Slot.Quantity == 0)
        {
            EmptyCount++;
        }
    }
    return EmptyCount;
}

bool UInventoryComponent::IsFull() const
{
    return GetEmptySlots() == 0;
}

float UInventoryComponent::GetCurrentWeight() const
{
    float TotalWeight = 0.0f;
    for (const FInventorySlot& Slot : InventorySlots)
    {
        if (Slot.Quantity > 0)
        {
            TotalWeight += Slot.ItemData.Weight * Slot.Quantity;
        }
    }
    return TotalWeight;
}

// ========== USE ITEMS ==========

void UInventoryComponent::UseItem(int32 SlotIndex)
{
    if (SlotIndex < 0 || SlotIndex >= InventorySlots.Num()) return;

    FInventorySlot& Slot = InventorySlots[SlotIndex];
    if (Slot.Quantity <= 0) return;

    // TODO: Implement item use logic (consumables, etc.)
    // For now, just remove consumable items
    if (Slot.ItemData.Category == EItemCategory::IC_Consumable)
    {
        RemoveItemAtSlot(SlotIndex, 1);
    }
}

void UInventoryComponent::EquipItem(int32 SlotIndex)
{
    if (SlotIndex < 0 || SlotIndex >= InventorySlots.Num()) return;

    FInventorySlot& Slot = InventorySlots[SlotIndex];
    if (Slot.Quantity <= 0) return;

    // TODO: Delegate to EquipmentComponent
    // This requires equipment system integration
}

// ========== SORTING ==========

void UInventoryComponent::SortByName()
{
    InventorySlots.Sort([](const FInventorySlot& A, const FInventorySlot& B)
    {
        if (A.Quantity == 0) return false; // Empty slots last
        if (B.Quantity == 0) return true;
        return A.ItemData.ItemName < B.ItemData.ItemName;
    });

    // Update slot indices
    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        InventorySlots[i].SlotIndex = i;
    }

    OnInventoryChanged.Broadcast();
}

void UInventoryComponent::SortByRarity()
{
    InventorySlots.Sort([](const FInventorySlot& A, const FInventorySlot& B)
    {
        if (A.Quantity == 0) return false;
        if (B.Quantity == 0) return true;
        return A.ItemData.Rarity > B.ItemData.Rarity; // Legendary first
    });

    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        InventorySlots[i].SlotIndex = i;
    }

    OnInventoryChanged.Broadcast();
}

void UInventoryComponent::SortByCategory()
{
    InventorySlots.Sort([](const FInventorySlot& A, const FInventorySlot& B)
    {
        if (A.Quantity == 0) return false;
        if (B.Quantity == 0) return true;
        return A.ItemData.Category < B.ItemData.Category;
    });

    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        InventorySlots[i].SlotIndex = i;
    }

    OnInventoryChanged.Broadcast();
}

void UInventoryComponent::SortByWeight()
{
    InventorySlots.Sort([](const FInventorySlot& A, const FInventorySlot& B)
    {
        if (A.Quantity == 0) return false;
        if (B.Quantity == 0) return true;
        return A.ItemData.Weight > B.ItemData.Weight; // Heaviest first
    });

    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        InventorySlots[i].SlotIndex = i;
    }

    OnInventoryChanged.Broadcast();
}

// ========== HELPER FUNCTIONS ==========

int32 UInventoryComponent::FindEmptySlot() const
{
    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        if (InventorySlots[i].Quantity == 0)
        {
            return i;
        }
    }
    return -1;
}

int32 UInventoryComponent::FindItemSlot(const FString& ItemID) const
{
    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        if (InventorySlots[i].ItemData.ItemID == ItemID && InventorySlots[i].Quantity > 0)
        {
            return i;
        }
    }
    return -1;
}

int32 UInventoryComponent::FindPartialStack(const FString& ItemID) const
{
    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        const FInventorySlot& Slot = InventorySlots[i];
        if (Slot.ItemData.ItemID == ItemID && Slot.Quantity > 0 && !Slot.IsFull())
        {
            return i;
        }
    }
    return -1;
}

bool UInventoryComponent::CanAddItem(const FItemData& Item, int32 Quantity) const
{
    // Check weight limit
    if (bEnableWeightLimit)
    {
        float NewWeight = GetCurrentWeight() + (Item.Weight * Quantity);
        if (NewWeight > MaxWeight) return false;
    }

    // Check if we have space (either empty slots or stackable slots)
    if (Item.MaxStackSize > 1 && bAutoStack)
    {
        // Calculate required slots with stacking
        int32 AvailableStackSpace = 0;

        // Count space in partial stacks
        for (const FInventorySlot& Slot : InventorySlots)
        {
            if (Slot.ItemData.ItemID == Item.ItemID && Slot.Quantity > 0)
            {
                AvailableStackSpace += Slot.GetRemainingSpace();
            }
        }

        // Count empty slots
        int32 EmptySlotCount = GetEmptySlots();
        int32 TotalSpace = AvailableStackSpace + (EmptySlotCount * Item.MaxStackSize);

        return TotalSpace >= Quantity;
    }
    else
    {
        // No stacking - need one slot per item
        return GetEmptySlots() >= Quantity;
    }
}

void UInventoryComponent::CompactInventory()
{
    // Move all items to front, remove empty slots
    TArray<FInventorySlot> CompactedSlots;

    for (const FInventorySlot& Slot : InventorySlots)
    {
        if (Slot.Quantity > 0)
        {
            CompactedSlots.Add(Slot);
        }
    }

    // Fill remaining with empty slots
    while (CompactedSlots.Num() < MaxSlots)
    {
        FInventorySlot EmptySlot;
        EmptySlot.SlotIndex = CompactedSlots.Num();
        CompactedSlots.Add(EmptySlot);
    }

    InventorySlots = CompactedSlots;

    // Update slot indices
    for (int32 i = 0; i < InventorySlots.Num(); i++)
    {
        InventorySlots[i].SlotIndex = i;
    }

    OnInventoryChanged.Broadcast();
}
