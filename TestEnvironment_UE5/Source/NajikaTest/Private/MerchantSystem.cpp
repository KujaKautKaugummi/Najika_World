// MerchantSystem.cpp
#include "MerchantSystem.h"
AMerchantSystem::AMerchantSystem() { PrimaryActorTick.bCanEverTick = false; }
void AMerchantSystem::BeginPlay() { Super::BeginPlay(); }
bool AMerchantSystem::BuyItem(const FString& ItemID, int32 Quantity) {
    for (const FMerchantItem& Item : Inventory) {
        if (Item.ItemID == ItemID && Item.Stock >= Quantity) {
            int32 TotalCost = Item.Price * Quantity;
            OnItemPurchased.Broadcast(ItemID, TotalCost);
            return true;
        }
    }
    return false;
}
bool AMerchantSystem::SellItem(const FString& ItemID, int32 Quantity) {
    OnItemSold.Broadcast(ItemID, 0);
    return true;
}
