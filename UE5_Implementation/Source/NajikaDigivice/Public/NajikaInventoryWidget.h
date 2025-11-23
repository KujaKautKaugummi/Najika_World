// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "NajikaBackendTypes.h"
#include "NajikaInventoryWidget.generated.h"

class UScrollBox;
class UButton;
class UTextBlock;
class UImage;
class UGridPanel;

/**
 * Inventory Widget for Najika Digivice
 *
 * Features:
 * - Grid-based item display
 * - Item categories (All, Food, Equipment, Materials, Key Items)
 * - Item details panel (name, description, stats)
 * - Use/Equip/Drop actions
 * - Stack count display
 * - Sort options (Name, Type, Rarity)
 * - Search/filter functionality
 *
 * Usage:
 * - Create Blueprint child class (WBP_NajikaInventory)
 * - Show via PlayerController menu
 */
UCLASS()
class NAJIKADIGIVICE_API UNajikaInventoryWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	virtual void NativeConstruct() override;

	// ============================================================
	// INVENTORY UI
	// ============================================================

	/** Item grid panel */
	UPROPERTY(meta = (BindWidget))
	UGridPanel* ItemGrid;

	/** Item details panel name */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ItemNameText;

	/** Item details description */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ItemDescriptionText;

	/** Item details type */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ItemTypeText;

	/** Item details icon */
	UPROPERTY(meta = (BindWidget))
	UImage* ItemIconImage;

	/** Item count text (e.g., "x5") */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* ItemCountText;

	// ============================================================
	// CATEGORY FILTERS
	// ============================================================

	/** All items button */
	UPROPERTY(meta = (BindWidget))
	UButton* AllButton;

	/** Food category button */
	UPROPERTY(meta = (BindWidget))
	UButton* FoodButton;

	/** Equipment category button */
	UPROPERTY(meta = (BindWidget))
	UButton* EquipmentButton;

	/** Materials category button */
	UPROPERTY(meta = (BindWidget))
	UButton* MaterialsButton;

	/** Key items button */
	UPROPERTY(meta = (BindWidget))
	UButton* KeyItemsButton;

	// ============================================================
	// ACTION BUTTONS
	// ============================================================

	/** Use item button */
	UPROPERTY(meta = (BindWidget))
	UButton* UseButton;

	/** Equip item button */
	UPROPERTY(meta = (BindWidget))
	UButton* EquipButton;

	/** Drop item button */
	UPROPERTY(meta = (BindWidget))
	UButton* DropButton;

	/** Close button */
	UPROPERTY(meta = (BindWidget))
	UButton* CloseButton;

	// ============================================================
	// INFO TEXT
	// ============================================================

	/** Inventory slots text (e.g., "15/20") */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* InventorySlotsText;

	/** Currency text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* CurrencyText;

	// ============================================================
	// SETTINGS
	// ============================================================

	/** Item widget class (Blueprint) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Inventory")
	TSubclassOf<UUserWidget> ItemWidgetClass;

	/** Max inventory slots */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Inventory")
	int32 MaxInventorySlots = 20;

	/** Grid columns */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Inventory")
	int32 GridColumns = 5;

	// ============================================================
	// FUNCTIONS
	// ============================================================

	/**
	 * Refresh inventory from game state
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void RefreshInventory();

	/**
	 * Add item to inventory
	 * @param Item Item to add
	 * @param Quantity Quantity to add
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void AddItem(const FNajikaItem& Item, int32 Quantity = 1);

	/**
	 * Remove item from inventory
	 * @param ItemID Item ID to remove
	 * @param Quantity Quantity to remove
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void RemoveItem(const FString& ItemID, int32 Quantity = 1);

	/**
	 * Use selected item
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void UseItem();

	/**
	 * Equip selected item
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void EquipItem();

	/**
	 * Drop selected item
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void DropItem();

	/**
	 * Filter inventory by category
	 * @param Category Category name (all, food, equipment, materials, key)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void FilterByCategory(const FString& Category);

	/**
	 * Select item
	 * @param ItemID Item ID
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
	void SelectItem(const FString& ItemID);

protected:
	// Button handlers
	UFUNCTION()
	void OnAllClicked();

	UFUNCTION()
	void OnFoodClicked();

	UFUNCTION()
	void OnEquipmentClicked();

	UFUNCTION()
	void OnMaterialsClicked();

	UFUNCTION()
	void OnKeyItemsClicked();

	UFUNCTION()
	void OnUseClicked();

	UFUNCTION()
	void OnEquipClicked();

	UFUNCTION()
	void OnDropClicked();

	UFUNCTION()
	void OnCloseClicked();

	// Helper functions
	void PopulateItemGrid();
	void UpdateItemDetails(const FNajikaItem& Item);
	void ClearItemDetails();

	// Inventory data
	TArray<FNajikaItem> InventoryItems;
	FString SelectedItemID;
	FString CurrentCategory = TEXT("all");
};
