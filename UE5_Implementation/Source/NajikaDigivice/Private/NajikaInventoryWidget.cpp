// Copyright Claude Code. All Rights Reserved.

#include "NajikaInventoryWidget.h"
#include "Components/ScrollBox.h"
#include "Components/Button.h"
#include "Components/TextBlock.h"
#include "Components/Image.h"
#include "Components/GridPanel.h"
#include "NajikaCharacter.h"
#include "NajikaPlayerState.h"
#include "NajikaHttpClient.h"

void UNajikaInventoryWidget::NativeConstruct()
{
	Super::NativeConstruct();

	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Inventory initialized"));

	// Bind category buttons
	if (AllButton) AllButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnAllClicked);
	if (FoodButton) FoodButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnFoodClicked);
	if (EquipmentButton) EquipmentButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnEquipmentClicked);
	if (MaterialsButton) MaterialsButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnMaterialsClicked);
	if (KeyItemsButton) KeyItemsButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnKeyItemsClicked);

	// Bind action buttons
	if (UseButton) UseButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnUseClicked);
	if (EquipButton) EquipButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnEquipClicked);
	if (DropButton) DropButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnDropClicked);
	if (CloseButton) CloseButton->OnClicked.AddDynamic(this, &UNajikaInventoryWidget::OnCloseClicked);

	// Initialize inventory
	RefreshInventory();
}

// ============================================================
// INVENTORY MANAGEMENT
// ============================================================

void UNajikaInventoryWidget::RefreshInventory()
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Refreshing inventory..."));

	// TODO: Load inventory from backend or game state
	// For now, populate with dummy data for testing
	InventoryItems.Empty();

	// Example items
	FNajikaItem AppleItem;
	AppleItem.ItemID = TEXT("apple");
	AppleItem.Name = TEXT("Apfel");
	AppleItem.Type = TEXT("food");
	AppleItem.Description = TEXT("Ein saftiger roter Apfel. Stellt +20 Hunger wieder her.");
	AppleItem.Value = 20;
	InventoryItems.Add(AppleItem);

	FNajikaItem SwordItem;
	SwordItem.ItemID = TEXT("iron_sword");
	SwordItem.Name = TEXT("Eisenschwert");
	SwordItem.Type = TEXT("equipment");
	SwordItem.Description = TEXT("Ein einfaches Eisenschwert. ATK +10");
	SwordItem.Value = 10;
	InventoryItems.Add(SwordItem);

	// Populate grid
	PopulateItemGrid();

	// Update UI
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaPlayerState* PS = PC->GetPlayerState<ANajikaPlayerState>();
		if (PS)
		{
			if (InventorySlotsText)
			{
				InventorySlotsText->SetText(FText::FromString(FString::Printf(TEXT("%d/%d"), InventoryItems.Num(), PS->InventorySlots)));
			}

			if (CurrencyText)
			{
				CurrencyText->SetText(FText::FromString(FString::Printf(TEXT("%d Bits"), PS->Currency)));
			}
		}
	}
}

void UNajikaInventoryWidget::AddItem(const FNajikaItem& Item, int32 Quantity)
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Adding item: %s x%d"), *Item.Name, Quantity);

	// Check if item already exists (stackable)
	bool bFound = false;
	for (FNajikaItem& ExistingItem : InventoryItems)
	{
		if (ExistingItem.ItemID == Item.ItemID)
		{
			// Stack item (not implemented in FNajikaItem yet, but would increment count)
			bFound = true;
			break;
		}
	}

	if (!bFound)
	{
		InventoryItems.Add(Item);
	}

	RefreshInventory();
}

void UNajikaInventoryWidget::RemoveItem(const FString& ItemID, int32 Quantity)
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Removing item: %s x%d"), *ItemID, Quantity);

	InventoryItems.RemoveAll([&ItemID](const FNajikaItem& Item)
	{
		return Item.ItemID == ItemID;
	});

	RefreshInventory();
}

// ============================================================
// ITEM ACTIONS
// ============================================================

void UNajikaInventoryWidget::UseItem()
{
	if (SelectedItemID.IsEmpty())
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] No item selected"));
		return;
	}

	FNajikaItem* SelectedItem = InventoryItems.FindByPredicate([this](const FNajikaItem& Item)
	{
		return Item.ItemID == SelectedItemID;
	});

	if (!SelectedItem)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] Selected item not found"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Using item: %s"), *SelectedItem->Name);

	// Handle item use based on type
	if (SelectedItem->Type == TEXT("food"))
	{
		// Feed Najika
		APlayerController* PC = GetOwningPlayer();
		if (PC)
		{
			ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
			if (Najika)
			{
				Najika->Feed();
			}
		}

		// Remove item
		RemoveItem(SelectedItemID, 1);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] Cannot use item of type: %s"), *SelectedItem->Type);
	}
}

void UNajikaInventoryWidget::EquipItem()
{
	if (SelectedItemID.IsEmpty())
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] No item selected"));
		return;
	}

	FNajikaItem* SelectedItem = InventoryItems.FindByPredicate([this](const FNajikaItem& Item)
	{
		return Item.ItemID == SelectedItemID;
	});

	if (!SelectedItem)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] Selected item not found"));
		return;
	}

	if (SelectedItem->Type != TEXT("equipment"))
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] Cannot equip non-equipment item"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Equipping item: %s"), *SelectedItem->Name);

	// Equip via backend
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika && Najika->BackendClient)
		{
			// Determine slot (simple heuristic - would be better to have slot data in item)
			FString Slot = TEXT("weapon"); // Default to weapon

			FOnNajikaActionResponse Delegate;
			Najika->BackendClient->EquipItem(SelectedItemID, Slot, Delegate);
		}
	}
}

void UNajikaInventoryWidget::DropItem()
{
	if (SelectedItemID.IsEmpty())
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] No item selected"));
		return;
	}

	FNajikaItem* SelectedItem = InventoryItems.FindByPredicate([this](const FNajikaItem& Item)
	{
		return Item.ItemID == SelectedItemID;
	});

	if (!SelectedItem)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaInventoryWidget] Selected item not found"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Dropping item: %s"), *SelectedItem->Name);

	// Remove item
	RemoveItem(SelectedItemID, 1);
	ClearItemDetails();
}

// ============================================================
// FILTERING
// ============================================================

void UNajikaInventoryWidget::FilterByCategory(const FString& Category)
{
	CurrentCategory = Category;
	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Filtering by category: %s"), *Category);
	PopulateItemGrid();
}

// ============================================================
// ITEM SELECTION
// ============================================================

void UNajikaInventoryWidget::SelectItem(const FString& ItemID)
{
	SelectedItemID = ItemID;

	FNajikaItem* Item = InventoryItems.FindByPredicate([&ItemID](const FNajikaItem& I)
	{
		return I.ItemID == ItemID;
	});

	if (Item)
	{
		UpdateItemDetails(*Item);
	}
}

// ============================================================
// BUTTON HANDLERS - CATEGORIES
// ============================================================

void UNajikaInventoryWidget::OnAllClicked()
{
	FilterByCategory(TEXT("all"));
}

void UNajikaInventoryWidget::OnFoodClicked()
{
	FilterByCategory(TEXT("food"));
}

void UNajikaInventoryWidget::OnEquipmentClicked()
{
	FilterByCategory(TEXT("equipment"));
}

void UNajikaInventoryWidget::OnMaterialsClicked()
{
	FilterByCategory(TEXT("materials"));
}

void UNajikaInventoryWidget::OnKeyItemsClicked()
{
	FilterByCategory(TEXT("key"));
}

// ============================================================
// BUTTON HANDLERS - ACTIONS
// ============================================================

void UNajikaInventoryWidget::OnUseClicked()
{
	UseItem();
}

void UNajikaInventoryWidget::OnEquipClicked()
{
	EquipItem();
}

void UNajikaInventoryWidget::OnDropClicked()
{
	DropItem();
}

void UNajikaInventoryWidget::OnCloseClicked()
{
	RemoveFromParent();
}

// ============================================================
// HELPERS
// ============================================================

void UNajikaInventoryWidget::PopulateItemGrid()
{
	if (!ItemGrid) return;

	ItemGrid->ClearChildren();

	int32 Row = 0;
	int32 Column = 0;

	for (const FNajikaItem& Item : InventoryItems)
	{
		// Filter by category
		if (CurrentCategory != TEXT("all") && Item.Type != CurrentCategory)
		{
			continue;
		}

		// Create item widget (Blueprint implementation)
		if (ItemWidgetClass)
		{
			UUserWidget* ItemWidget = CreateWidget<UUserWidget>(GetWorld(), ItemWidgetClass);
			if (ItemWidget)
			{
				// TODO: Set item data on widget (Blueprint should expose function)
				ItemGrid->AddChildToGrid(ItemWidget, Row, Column);

				Column++;
				if (Column >= GridColumns)
				{
					Column = 0;
					Row++;
				}
			}
		}
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Populated grid with %d items"), InventoryItems.Num());
}

void UNajikaInventoryWidget::UpdateItemDetails(const FNajikaItem& Item)
{
	if (ItemNameText)
	{
		ItemNameText->SetText(FText::FromString(Item.Name));
	}

	if (ItemDescriptionText)
	{
		ItemDescriptionText->SetText(FText::FromString(Item.Description));
	}

	if (ItemTypeText)
	{
		// Translate type to German
		TMap<FString, FString> TypeNames = {
			{TEXT("food"), TEXT("Nahrung")},
			{TEXT("equipment"), TEXT("Ausrüstung")},
			{TEXT("materials"), TEXT("Materialien")},
			{TEXT("key"), TEXT("Schlüsselitem")}
		};

		FString TypeName = TypeNames.Contains(Item.Type) ? TypeNames[Item.Type] : Item.Type;
		ItemTypeText->SetText(FText::FromString(TypeName));
	}

	// TODO: Load item icon (Blueprint implementation)

	UE_LOG(LogTemp, Log, TEXT("[NajikaInventoryWidget] Selected item: %s"), *Item.Name);
}

void UNajikaInventoryWidget::ClearItemDetails()
{
	if (ItemNameText) ItemNameText->SetText(FText::GetEmpty());
	if (ItemDescriptionText) ItemDescriptionText->SetText(FText::GetEmpty());
	if (ItemTypeText) ItemTypeText->SetText(FText::GetEmpty());
	if (ItemIconImage) ItemIconImage->SetVisibility(ESlateVisibility::Collapsed);

	SelectedItemID = TEXT("");
}
