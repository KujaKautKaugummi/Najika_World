// CraftingSystem.h
// Crafting Pipeline: Rohstoffe → Veredeln → Herstellen → Verzaubern → Fein-Tuning
// Section 2.4 from PDF: Deep crafting with real-world herbal knowledge (Lore only!)

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "CraftingSystem.generated.h"

// Item Rarity
UENUM(BlueprintType)
enum class EItemRarity : uint8
{
    IR_Common UMETA(DisplayName = "Gewöhnlich"),
    IR_Uncommon UMETA(DisplayName = "Ungewöhnlich"),
    IR_Rare UMETA(DisplayName = "Selten"),
    IR_Epic UMETA(DisplayName = "Episch"),
    IR_Legendary UMETA(DisplayName = "Legendär")
};

// Crafting Stage
UENUM(BlueprintType)
enum class ECraftingStage : uint8
{
    CS_RawMaterial UMETA(DisplayName = "Rohstoff"),
    CS_Refined UMETA(DisplayName = "Veredelt"),
    CS_Crafted UMETA(DisplayName = "Hergestellt"),
    CS_Enchanted UMETA(DisplayName = "Verzaubert"),
    CS_FineTuned UMETA(DisplayName = "Fein-Tuned")
};

// Herb/Material Type (Real-world inspired, LORE ONLY!)
UENUM(BlueprintType)
enum class EHerbType : uint8
{
    H_Weidenrinde UMETA(DisplayName = "Weidenrinde"),
    H_Ingwer UMETA(DisplayName = "Ingwer"),
    H_Honig UMETA(DisplayName = "Honig"),
    H_Arnika UMETA(DisplayName = "Arnika"),
    H_Jiaogulan UMETA(DisplayName = "Jiaogulan"),
    H_Kamille UMETA(DisplayName = "Kamille"),
    H_Lavendel UMETA(DisplayName = "Lavendel"),
    H_Pfefferminze UMETA(DisplayName = "Pfefferminze"),
    H_Salbei UMETA(DisplayName = "Salbei"),
    H_Baldrian UMETA(DisplayName = "Baldrian")
};

// Crafting Material
USTRUCT(BlueprintType)
struct FCraftingMaterial
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString MaterialName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EHerbType HerbType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EItemRarity Rarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Quantity = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString LoreDescription;  // LORE ONLY - NO real medical advice!

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> FlavorBuffs;  // Gameplay effects (lore-based)
};

// Crafting Recipe
USTRUCT(BlueprintType)
struct FCraftingRecipe
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RecipeName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FCraftingMaterial> RequiredMaterials;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ECraftingStage RequiredStage;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ResultItemName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ECraftingStage ResultStage;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EItemRarity ResultRarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float CraftingTime = 5.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> ResultStats;
};

// Crafted Item
USTRUCT(BlueprintType)
struct FCraftedItem
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ItemName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ECraftingStage CraftingStage;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EItemRarity Rarity;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> Stats;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> Enchantments;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Quality = 100;  // 0-100%

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString CrafterName;
};

UCLASS()
class NAJIKATEST_API ACraftingSystem : public AActor
{
    GENERATED_BODY()

public:
    ACraftingSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== CRAFTING PIPELINE ==========

    // Stage 1: Rohstoffe sammeln
    UFUNCTION(BlueprintCallable, Category = "Crafting|Stage1")
    void GatherRawMaterial(EHerbType HerbType, int32 Amount);

    // Stage 2: Veredeln (Refine)
    UFUNCTION(BlueprintCallable, Category = "Crafting|Stage2")
    bool RefineMaterial(const FCraftingMaterial& Material);

    // Stage 3: Herstellen (Craft)
    UFUNCTION(BlueprintCallable, Category = "Crafting|Stage3")
    bool CraftItem(const FCraftingRecipe& Recipe);

    // Stage 4: Verzaubern (Enchant)
    UFUNCTION(BlueprintCallable, Category = "Crafting|Stage4")
    bool EnchantItem(FCraftedItem& Item, const FString& EnchantmentName);

    // Stage 5: Fein-Tuning
    UFUNCTION(BlueprintCallable, Category = "Crafting|Stage5")
    bool FineTuneItem(FCraftedItem& Item, const FString& StatName, float Bonus);

    // ========== RECIPE MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Crafting|Recipes")
    void LearnRecipe(const FString& RecipeName);

    UFUNCTION(BlueprintPure, Category = "Crafting|Recipes")
    bool HasRecipe(const FString& RecipeName) const;

    UFUNCTION(BlueprintPure, Category = "Crafting|Recipes")
    TArray<FCraftingRecipe> GetAvailableRecipes() const;

    UFUNCTION(BlueprintPure, Category = "Crafting|Recipes")
    bool CanCraftRecipe(const FCraftingRecipe& Recipe) const;

    // ========== INVENTORY ==========

    UFUNCTION(BlueprintCallable, Category = "Crafting|Inventory")
    void AddMaterial(const FCraftingMaterial& Material);

    UFUNCTION(BlueprintCallable, Category = "Crafting|Inventory")
    void RemoveMaterial(EHerbType HerbType, int32 Amount);

    UFUNCTION(BlueprintPure, Category = "Crafting|Inventory")
    int32 GetMaterialCount(EHerbType HerbType) const;

    UFUNCTION(BlueprintPure, Category = "Crafting|Inventory")
    TArray<FCraftedItem> GetCraftedItems() const { return CraftedItems; }

    // ========== ALCHEMY (LORE-BASED) ==========

    UFUNCTION(BlueprintCallable, Category = "Crafting|Alchemy")
    FCraftedItem CreatePotion(const TArray<EHerbType>& Herbs);

    UFUNCTION(BlueprintPure, Category = "Crafting|Alchemy")
    FString GetHerbLoreDescription(EHerbType HerbType) const;

    UFUNCTION(BlueprintPure, Category = "Crafting|Alchemy")
    TMap<FString, float> GetHerbFlavorBuffs(EHerbType HerbType) const;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Crafting|Config")
    TMap<FString, FCraftingRecipe> AllRecipes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Crafting|Config")
    TMap<EHerbType, FCraftingMaterial> HerbDatabase;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Crafting|Config")
    bool bShowRealWorldAdvice = false;  // ALWAYS FALSE - Lore only!

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Crafting|State")
    TMap<EHerbType, int32> MaterialInventory;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Crafting|State")
    TArray<FCraftedItem> CraftedItems;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Crafting|State")
    TArray<FString> KnownRecipes;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Crafting|State")
    int32 CraftingLevel = 1;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Crafting|State")
    int32 CraftingXP = 0;

private:
    // ========== HELPER FUNCTIONS ==========

    void InitializeHerbDatabase();
    void InitializeRecipes();

    bool HasRequiredMaterials(const FCraftingRecipe& Recipe) const;
    void ConsumeMaterials(const FCraftingRecipe& Recipe);
    void AddCraftingXP(int32 Amount);

    FCraftingMaterial GetHerbData(EHerbType HerbType) const;
};
