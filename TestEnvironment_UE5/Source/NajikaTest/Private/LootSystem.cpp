// LootSystem.cpp
#include "LootSystem.h"
ULootSystem::ULootSystem() { PrimaryComponentTick.bCanEverTick = false; }
void ULootSystem::BeginPlay() { Super::BeginPlay(); }
TArray<FLootDrop> ULootSystem::GenerateLoot(const FString& LootTableID) {
    TArray<FLootDrop> Loot;
    if (!LootTables.Contains(LootTableID)) return Loot;
    
    FLootTable& Table = LootTables[LootTableID];
    for (const FLootEntry& Entry : Table.Entries) {
        float Roll = FMath::FRand();
        if (Roll <= Entry.DropChance) {
            FLootDrop Drop;
            Drop.ItemID = Entry.ItemID;
            Drop.Quantity = FMath::RandRange(Entry.MinQuantity, Entry.MaxQuantity);
            Drop.Rarity = Entry.Rarity;
            Loot.Add(Drop);
        }
    }
    return Loot;
}
