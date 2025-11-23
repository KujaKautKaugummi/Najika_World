// EquipmentComponent.h
// Complete Equipment System: Armor, Weapons, Accessories, Stats, Sets

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "InventoryComponent.h"
#include "EquipmentComponent.generated.h"

// Equipment Slot
UENUM(BlueprintType)
enum class EEquipmentSlot : uint8
{
    ES_Head UMETA(DisplayName = "Head"),
    ES_Chest UMETA(DisplayName = "Chest"),
    ES_Legs UMETA(DisplayName = "Legs"),
    ES_Feet UMETA(DisplayName = "Feet"),
    ES_Hands UMETA(DisplayName = "Hands"),
    ES_MainHand UMETA(DisplayName = "Main Hand (Weapon)"),
    ES_OffHand UMETA(DisplayName = "Off Hand (Shield)"),
    ES_Back UMETA(DisplayName = "Back (Cloak)"),
    ES_Accessory1 UMETA(DisplayName = "Accessory 1"),
    ES_Accessory2 UMETA(DisplayName = "Accessory 2"),
    ES_Accessory3 UMETA(DisplayName = "Accessory 3")
};

// Equipment Set Bonus
USTRUCT(BlueprintType)
struct FSetBonus
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString SetName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredPieces = 2;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> Bonuses;  // "Damage": 1.1 (10% increase)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BonusDescription;
};

// Equipped Item Data
USTRUCT(BlueprintType)
struct FEquippedItem
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FItemData ItemData;

    UPROPERTY(BlueprintReadWrite)
    EEquipmentSlot Slot;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, float> Stats;  // "Attack": 50, "Defense": 20

    UPROPERTY(BlueprintReadWrite)
    FString SetName;  // For set bonuses

    UPROPERTY(BlueprintReadWrite)
    int32 Durability = 100;

    UPROPERTY(BlueprintReadWrite)
    int32 MaxDurability = 100;

    bool IsEmpty() const { return ItemData.ItemID.IsEmpty(); }
    float GetDurabilityPercent() const { return (float)Durability / (float)MaxDurability; }
};

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class NAJIKATEST_API UEquipmentComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UEquipmentComponent();

protected:
    virtual void BeginPlay() override;

public:
    // ========== EQUIP/UNEQUIP ==========

    UFUNCTION(BlueprintCallable, Category = "Equipment")
    bool EquipItem(const FItemData& Item, EEquipmentSlot Slot);

    UFUNCTION(BlueprintCallable, Category = "Equipment")
    bool UnequipItem(EEquipmentSlot Slot);

    UFUNCTION(BlueprintCallable, Category = "Equipment")
    void UnequipAll();

    UFUNCTION(BlueprintCallable, Category = "Equipment")
    bool SwapEquipment(EEquipmentSlot Slot1, EEquipmentSlot Slot2);

    // ========== QUERIES ==========

    UFUNCTION(BlueprintPure, Category = "Equipment")
    FEquippedItem GetEquippedItem(EEquipmentSlot Slot) const;

    UFUNCTION(BlueprintPure, Category = "Equipment")
    bool IsSlotEquipped(EEquipmentSlot Slot) const;

    UFUNCTION(BlueprintPure, Category = "Equipment")
    TMap<EEquipmentSlot, FEquippedItem> GetAllEquipment() const { return EquippedItems; }

    UFUNCTION(BlueprintPure, Category = "Equipment")
    bool CanEquipItem(const FItemData& Item, EEquipmentSlot Slot) const;

    // ========== STATS ==========

    UFUNCTION(BlueprintPure, Category = "Equipment|Stats")
    float GetTotalStat(const FString& StatName) const;

    UFUNCTION(BlueprintPure, Category = "Equipment|Stats")
    TMap<FString, float> GetAllStats() const;

    UFUNCTION(BlueprintPure, Category = "Equipment|Stats")
    float GetAttackPower() const { return GetTotalStat("Attack"); }

    UFUNCTION(BlueprintPure, Category = "Equipment|Stats")
    float GetDefense() const { return GetTotalStat("Defense"); }

    UFUNCTION(BlueprintPure, Category = "Equipment|Stats")
    float GetMagicPower() const { return GetTotalStat("Magic"); }

    // ========== SET BONUSES ==========

    UFUNCTION(BlueprintPure, Category = "Equipment|SetBonus")
    TArray<FSetBonus> GetActiveSetBonuses() const;

    UFUNCTION(BlueprintPure, Category = "Equipment|SetBonus")
    bool HasSetBonus(const FString& SetName) const;

    UFUNCTION(BlueprintPure, Category = "Equipment|SetBonus")
    int32 GetSetPieceCount(const FString& SetName) const;

    UFUNCTION(BlueprintPure, Category = "Equipment|SetBonus")
    float GetSetBonusStat(const FString& StatName) const;

    // ========== DURABILITY ==========

    UFUNCTION(BlueprintCallable, Category = "Equipment|Durability")
    void DamageEquipment(EEquipmentSlot Slot, int32 Amount);

    UFUNCTION(BlueprintCallable, Category = "Equipment|Durability")
    void RepairEquipment(EEquipmentSlot Slot, int32 Amount);

    UFUNCTION(BlueprintCallable, Category = "Equipment|Durability")
    void RepairAll(int32 Amount);

    UFUNCTION(BlueprintPure, Category = "Equipment|Durability")
    bool IsEquipmentBroken(EEquipmentSlot Slot) const;

    // ========== VISUAL ==========

    UFUNCTION(BlueprintCallable, Category = "Equipment|Visual")
    void UpdateVisualEquipment();

    UFUNCTION(BlueprintCallable, Category = "Equipment|Visual")
    void HideHelmet(bool bHide);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnItemEquipped, EEquipmentSlot, Slot, FItemData, Item);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnItemUnequipped, EEquipmentSlot, Slot);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSetBonusActivated, FSetBonus, SetBonus);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnEquipmentBroken, EEquipmentSlot, Slot);

    UPROPERTY(BlueprintAssignable, Category = "Equipment|Events")
    FOnItemEquipped OnItemEquipped;

    UPROPERTY(BlueprintAssignable, Category = "Equipment|Events")
    FOnItemUnequipped OnItemUnequipped;

    UPROPERTY(BlueprintAssignable, Category = "Equipment|Events")
    FOnSetBonusActivated OnSetBonusActivated;

    UPROPERTY(BlueprintAssignable, Category = "Equipment|Events")
    FOnEquipmentBroken OnEquipmentBroken;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equipment|Config")
    TMap<FString, FSetBonus> SetBonuses;  // All available set bonuses

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equipment|Config")
    bool bEnableDurability = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equipment|Config")
    float DurabilityLossPerHit = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equipment|Config")
    bool bHideHelmetEnabled = false;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Equipment|State")
    TMap<EEquipmentSlot, FEquippedItem> EquippedItems;

private:
    // ========== HELPER FUNCTIONS ==========

    void CalculateStats();
    void CheckSetBonuses();
    void ApplySetBonus(const FSetBonus& SetBonus);
    void RemoveSetBonus(const FSetBonus& SetBonus);
    EEquipmentSlot GetSlotForItemCategory(EItemCategory Category) const;
};
