// BankSystem.cpp - Complete implementation
#include "BankSystem.h"

UBankSystem::UBankSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UBankSystem::BeginPlay() { Super::BeginPlay(); BankSlots.SetNum(MaxBankSlots); }

bool UBankSystem::DepositItem(const FItemData& Item, int32 Quantity) {
    for (FInventorySlot& Slot : BankSlots) {
        if (Slot.ItemData.ItemID == Item.ItemID && !Slot.IsFull()) {
            int32 ToAdd = FMath::Min(Slot.GetRemainingSpace(), Quantity);
            Slot.Quantity += ToAdd;
            Quantity -= ToAdd;
            if (Quantity == 0) return true;
        }
    }
    for (FInventorySlot& Slot : BankSlots) {
        if (Slot.Quantity == 0) {
            Slot.ItemData = Item;
            Slot.Quantity = FMath::Min(Item.MaxStackSize, Quantity);
            Quantity -= Slot.Quantity;
            if (Quantity == 0) return true;
        }
    }
    return false;
}

bool UBankSystem::WithdrawItem(const FString& ItemID, int32 Quantity) {
    for (FInventorySlot& Slot : BankSlots) {
        if (Slot.ItemData.ItemID == ItemID) {
            int32 ToRemove = FMath::Min(Slot.Quantity, Quantity);
            Slot.Quantity -= ToRemove;
            Quantity -= ToRemove;
            if (Slot.Quantity == 0) Slot.ItemData = FItemData();
            if (Quantity == 0) return true;
        }
    }
    return false;
}

int32 UBankSystem::GetItemCount(const FString& ItemID) const {
    int32 Count = 0;
    for (const FInventorySlot& Slot : BankSlots) {
        if (Slot.ItemData.ItemID == ItemID) Count += Slot.Quantity;
    }
    return Count;
}

bool UBankSystem::DepositGold(int32 Amount) {
    if (Amount <= 0) return false;
    StoredGold += Amount;
    return true;
}

bool UBankSystem::WithdrawGold(int32 Amount) {
    if (Amount <= 0 || StoredGold < Amount) return false;
    StoredGold -= Amount;
    return true;
}

void UBankSystem::UpgradeBankSize(int32 AdditionalSlots) {
    MaxBankSlots += AdditionalSlots;
    BankSlots.SetNum(MaxBankSlots);
}
