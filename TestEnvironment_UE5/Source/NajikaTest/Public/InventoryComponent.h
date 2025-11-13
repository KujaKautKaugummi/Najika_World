// InventoryComponent.h
// Complete Inventory System with items, stacks, weight, categories

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "InventoryComponent.generated.h"

// Item Category
UENUM(BlueprintType)
enum class EItemCategory : uint8
{
    IC_Weapon UMETA(DisplayName = "Weapon"),
    IC_Armor UMETA(DisplayName = "Armor"),
    IC_Consumable UMETA(DisplayName = "Consumable"),
    IC_Material UMETA(DisplayName = "Material"),
    IC_Quest UMETA(DisplayName = "Quest Item"),
    IC_Misc UMETA(DisplayName = "Miscellaneous")
};

// Item Rarity (from CraftingSystem)
UENUM(BlueprintType)
enum class EItemRarity : uint8
{
    IR_Common UMETA(DisplayName = "Common"),
    IR_Uncommon UMETA(DisplayName = "Uncommon"),
    IR_Rare UMETA(DisplayName = "Rare"),
    IR_Epic UMETA(DisplayName = "Epic"),
    IR_Legendary UMETA(DisplayName = "Legendary")
};

// Item Definition
USTRUCT(BlueprintType)
struct FItemData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ItemID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ItemName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EItemCategory Category;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EItemRarity Rarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxStackSize = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Weight = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Value = 10;  // Gold value

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsQuestItem = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCanDrop = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCanSell = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> Stats;  // "Damage": 50.0, "Defense": 20.0
};

// Item Stack (inventory slot)
USTRUCT(BlueprintType)
struct FInventorySlot
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FItemData ItemData;

    UPROPERTY(BlueprintReadWrite)
    int32 Quantity = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 SlotIndex = -1;

    bool IsEmpty() const { return Quantity <= 0; }
    bool IsFull() const { return Quantity >= ItemData.MaxStackSize; }
    int32 GetRemainingSpace() const { return ItemData.MaxStackSize - Quantity; }
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class NAJIKATEST_API UInventoryComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UInventoryComponent();

protected:
    virtual void BeginPlay() override;

public:
    // ========== ADD/REMOVE ITEMS ==========

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool AddItem(const FItemData& Item, int32 Quantity = 1);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool RemoveItem(const FString& ItemID, int32 Quantity = 1);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool RemoveItemAtSlot(int32 SlotIndex, int32 Quantity = 1);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void ClearInventory();

    // ========== ITEM QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "Inventory")
    bool HasItem(const FString& ItemID, int32 MinQuantity = 1) const;

    UFUNCTION(BlueprintPure, Category = "Inventory")
    int32 GetItemCount(const FString& ItemID) const;

    UFUNCTION(BlueprintPure, Category = "Inventory")
    FInventorySlot GetItemAtSlot(int32 SlotIndex) const;

    UFUNCTION(BlueprintPure, Category = "Inventory")
    TArray<FInventorySlot> GetAllItems() const { return InventorySlots; }

    UFUNCTION(BlueprintPure, Category = "Inventory")
    TArray<FInventorySlot> GetItemsByCategory(EItemCategory Category) const;

    // ========== ITEM MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool MoveItem(int32 FromSlot, int32 ToSlot);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool SplitStack(int32 SlotIndex, int32 SplitAmount);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool MergeStacks(int32 Slot1, int32 Slot2);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool DropItem(int32 SlotIndex, int32 Quantity = 1);

    // ========== INVENTORY INFO ==========

    UFUNCTION(BlueprintPure, Category = "Inventory")
    int32 GetMaxSlots() const { return MaxSlots; }

    UFUNCTION(BlueprintPure, Category = "Inventory")
    int32 GetEmptySlots() const;

    UFUNCTION(BlueprintPure, Category = "Inventory")
    bool IsFull() const;

    UFUNCTION(BlueprintPure, Category = "Inventory")
    float GetCurrentWeight() const;

    UFUNCTION(BlueprintPure, Category = "Inventory")
    float GetMaxWeight() const { return MaxWeight; }

    UFUNCTION(BlueprintPure, Category = "Inventory")
    bool IsOverweight() const { return GetCurrentWeight() > MaxWeight; }

    // ========== USE ITEMS ==========

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void UseItem(int32 SlotIndex);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void EquipItem(int32 SlotIndex);

    // ========== SORTING ==========

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void SortByName();

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void SortByRarity();

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void SortByCategory();

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void SortByWeight();

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnItemAdded, FItemData, Item, int32, Quantity);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnItemRemoved, FString, ItemID, int32, Quantity);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnInventoryChanged);

    UPROPERTY(BlueprintAssignable, Category = "Inventory|Events")
    FOnItemAdded OnItemAdded;

    UPROPERTY(BlueprintAssignable, Category = "Inventory|Events")
    FOnItemRemoved OnItemRemoved;

    UPROPERTY(BlueprintAssignable, Category = "Inventory|Events")
    FOnInventoryChanged OnInventoryChanged;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inventory|Config")
    int32 MaxSlots = 40;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inventory|Config")
    float MaxWeight = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inventory|Config")
    bool bEnableWeightLimit = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inventory|Config")
    bool bAutoStack = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Inventory|Config")
    bool bAllowQuestItemDrop = false;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Inventory|State")
    TArray<FInventorySlot> InventorySlots;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Inventory|State")
    int32 Gold = 0;

private:
    // ========== HELPER FUNCTIONS ==========

    int32 FindEmptySlot() const;
    int32 FindItemSlot(const FString& ItemID) const;
    int32 FindPartialStack(const FString& ItemID) const;
    bool CanAddItem(const FItemData& Item, int32 Quantity) const;
    void CompactInventory();
};
