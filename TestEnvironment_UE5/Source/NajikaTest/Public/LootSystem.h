// LootSystem.h
// Complete Loot System: Drops, Rarity, Loot Tables, Treasure Chests

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InventoryComponent.h"
#include "LootSystem.generated.h"

// Loot Entry
USTRUCT(BlueprintType)
struct FLootEntry
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ItemID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float DropChance = 1.0f;  // 0.0-1.0 (0% - 100%)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinQuantity = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxQuantity = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EItemRarity RequiredRarity = EItemRarity::IR_Common;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bGuaranteedDrop = false;
};

// Loot Table
USTRUCT(BlueprintType)
struct FLootTable
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TableID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FLootEntry> LootEntries;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinDrops = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxDrops = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float RareDropBonus = 0.0f;  // Luck modifier

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinGold = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxGold = 10;
};

// Dropped Loot Result
USTRUCT(BlueprintType)
struct FLootDrop
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    TArray<FItemData> Items;

    UPROPERTY(BlueprintReadWrite)
    TArray<int32> Quantities;

    UPROPERTY(BlueprintReadWrite)
    int32 Gold = 0;
};

UCLASS()
class NAJIKATEST_API ALootSystem : public AActor
{
    GENERATED_BODY()

public:
    ALootSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== LOOT GENERATION ==========

    UFUNCTION(BlueprintCallable, Category = "Loot")
    FLootDrop GenerateLoot(const FString& LootTableID, float LuckModifier = 0.0f);

    UFUNCTION(BlueprintCallable, Category = "Loot")
    FLootDrop GenerateLootFromEnemy(const FString& EnemyID, int32 PlayerLevel, float LuckModifier = 0.0f);

    UFUNCTION(BlueprintCallable, Category = "Loot")
    FLootDrop GenerateLootFromChest(const FString& ChestType, float LuckModifier = 0.0f);

    // ========== LOOT SPAWNING ==========

    UFUNCTION(BlueprintCallable, Category = "Loot|Spawn")
    void SpawnLoot(const FLootDrop& Loot, FVector Location);

    UFUNCTION(BlueprintCallable, Category = "Loot|Spawn")
    void SpawnLootActor(const FItemData& Item, int32 Quantity, FVector Location);

    // ========== LOOT TABLES ==========

    UFUNCTION(BlueprintPure, Category = "Loot|Tables")
    bool HasLootTable(const FString& TableID) const;

    UFUNCTION(BlueprintCallable, Category = "Loot|Tables")
    void AddLootTable(const FString& TableID, const FLootTable& Table);

    UFUNCTION(BlueprintPure, Category = "Loot|Tables")
    FLootTable GetLootTable(const FString& TableID) const;

    // ========== RARITY ROLLING ==========

    UFUNCTION(BlueprintPure, Category = "Loot|Rarity")
    EItemRarity RollRarity(float LuckModifier = 0.0f) const;

    UFUNCTION(BlueprintPure, Category = "Loot|Rarity")
    float GetRarityChance(EItemRarity Rarity, float LuckModifier = 0.0f) const;

    // ========== LUCK SYSTEM ==========

    UFUNCTION(BlueprintPure, Category = "Loot|Luck")
    float CalculateLuckModifier(AActor* LootingActor) const;

    // ========== BOSS LOOT ==========

    UFUNCTION(BlueprintCallable, Category = "Loot|Boss")
    FLootDrop GenerateBossLoot(const FString& BossID, int32 PlayerLevel);

    // ========== TREASURE CHESTS ==========

    UFUNCTION(BlueprintCallable, Category = "Loot|Chest")
    FLootDrop OpenChest(const FString& ChestID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLootGenerated, FLootDrop, Loot);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnLootSpawned, FItemData, Item, FVector, Location);

    UPROPERTY(BlueprintAssignable, Category = "Loot|Events")
    FOnLootGenerated OnLootGenerated;

    UPROPERTY(BlueprintAssignable, Category = "Loot|Events")
    FOnLootSpawned OnLootSpawned;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Loot|Config")
    TMap<FString, FLootTable> LootTables;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Loot|Config")
    TSubclassOf<AActor> LootActorClass;

    // Rarity Chances (base values, modified by luck)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Loot|Rarity")
    float CommonChance = 0.70f;  // 70%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Loot|Rarity")
    float UncommonChance = 0.20f;  // 20%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Loot|Rarity")
    float RareChance = 0.07f;  // 7%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Loot|Rarity")
    float EpicChance = 0.025f;  // 2.5%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Loot|Rarity")
    float LegendaryChance = 0.005f;  // 0.5%

private:
    // ========== HELPER FUNCTIONS ==========

    TArray<FLootEntry> RollLootEntries(const FLootTable& Table, float LuckModifier);
    int32 RollGold(const FLootTable& Table);
    int32 RollQuantity(const FLootEntry& Entry);
    bool RollDropChance(float Chance, float LuckModifier);
    FItemData GetItemData(const FString& ItemID) const;
};

// Loot Actor (pickupable item in world)
UCLASS()
class NAJIKATEST_API ALootActor : public AActor
{
    GENERATED_BODY()

public:
    ALootActor();

protected:
    virtual void BeginPlay() override;

public:
    // ========== SETUP ==========

    UFUNCTION(BlueprintCallable, Category = "LootActor")
    void SetLootData(const FItemData& Item, int32 Quantity);

    // ========== PICKUP ==========

    UFUNCTION(BlueprintCallable, Category = "LootActor")
    void PickUp(AActor* PickingActor);

    UFUNCTION(BlueprintPure, Category = "LootActor")
    bool CanBePickedUp() const;

    // ========== AUTO-PICKUP ==========

    UFUNCTION(BlueprintCallable, Category = "LootActor")
    void EnableAutoPickup(float Radius);

protected:
    // ========== COMPONENTS ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class UStaticMeshComponent* MeshComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class USphereComponent* PickupRadius;

    // ========== DATA ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LootActor")
    FItemData ItemData;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LootActor")
    int32 Quantity = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LootActor")
    bool bAutoPickup = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LootActor")
    float AutoPickupRadius = 200.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LootActor")
    float DespawnTime = 300.0f;  // 5 minutes

    UPROPERTY(BlueprintReadOnly, Category = "LootActor")
    float TimeAlive = 0.0f;

private:
    UFUNCTION()
    void OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
                       UPrimitiveComponent* OtherComp, int32 OtherBodyIndex,
                       bool bFromSweep, const FHitResult& SweepResult);
};
