// CookingSystem.h
// Complete Cooking System with recipes, quality, buffs, skill progression
// Works alongside CraftingSystem but separate from it

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "CookingSystem.generated.h"

// Cooking Method
UENUM(BlueprintType)
enum class ECookingMethod : uint8
{
    CM_Grilling UMETA(DisplayName = "Grilling"),
    CM_Boiling UMETA(DisplayName = "Boiling"),
    CM_Frying UMETA(DisplayName = "Frying"),
    CM_Baking UMETA(DisplayName = "Baking"),
    CM_Roasting UMETA(DisplayName = "Roasting"),
    CM_Stewing UMETA(DisplayName = "Stewing"),
    CM_Raw UMETA(DisplayName = "Raw/No Cooking")
};

// Food Quality
UENUM(BlueprintType)
enum class EFoodQuality : uint8
{
    FQ_Burnt UMETA(DisplayName = "Burnt"),
    FQ_Poor UMETA(DisplayName = "Poor"),
    FQ_Normal UMETA(DisplayName = "Normal"),
    FQ_Good UMETA(DisplayName = "Good"),
    FQ_Excellent UMETA(DisplayName = "Excellent"),
    FQ_Masterwork UMETA(DisplayName = "Masterwork")
};

// Food Category
UENUM(BlueprintType)
enum class EFoodCategory : uint8
{
    FC_Meal UMETA(DisplayName = "Meal"),
    FC_Snack UMETA(DisplayName = "Snack"),
    FC_Drink UMETA(DisplayName = "Drink"),
    FC_Dessert UMETA(DisplayName = "Dessert"),
    FC_Ingredient UMETA(DisplayName = "Ingredient"),
    FC_Special UMETA(DisplayName = "Special/Buff Food")
};

// Cooking Recipe
USTRUCT(BlueprintType)
struct FCookingRecipe
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RecipeID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RecipeName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EFoodCategory Category;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    ECookingMethod Method;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, int32> RequiredIngredients;  // ItemID -> Quantity

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ResultItemID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 ResultQuantity = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float CookingTime = 5.0f;  // Seconds

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 XPReward = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float PerfectWindowStart = 0.4f;  // 40% of cooking time

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float PerfectWindowEnd = 0.6f;  // 60% of cooking time

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> BuffEffects;  // "Health": 20.0 (heal 20 HP)

    UPROPERTY(BlueprintReadWrite)
    bool bDiscovered = false;
};

// Cooked Food Item
USTRUCT(BlueprintType)
struct FCookedFood
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString RecipeID;

    UPROPERTY(BlueprintReadWrite)
    EFoodQuality Quality;

    UPROPERTY(BlueprintReadWrite)
    float BuffMultiplier = 1.0f;  // Based on quality

    UPROPERTY(BlueprintReadWrite)
    FDateTime CookedTime;

    UPROPERTY(BlueprintReadWrite)
    FString CookedByPlayerName;

    float GetBuffValue(const FString& BuffType, float BaseValue) const
    {
        return BaseValue * BuffMultiplier;
    }
};

// Cooking Station
USTRUCT(BlueprintType)
struct FCookingStation
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString StationID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString StationName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<ECookingMethod> SupportedMethods;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float QualityBonus = 0.0f;  // Better stations = better quality

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SpeedMultiplier = 1.0f;  // Some stations cook faster

    UPROPERTY(BlueprintReadWrite)
    bool bInUse = false;
};

UCLASS()
class NAJIKATEST_API ACookingSystem : public AActor
{
    GENERATED_BODY()

public:
    ACookingSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== COOKING ACTIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Cooking|Actions")
    void StartCooking(const FString& RecipeID, const FString& StationID = "");

    UFUNCTION(BlueprintCallable, Category = "Cooking|Actions")
    void StopCooking();

    UFUNCTION(BlueprintCallable, Category = "Cooking|Actions")
    void FinishCooking();  // Player chooses to finish

    UFUNCTION(BlueprintPure, Category = "Cooking|Actions")
    bool IsCooking() const { return bCooking; }

    UFUNCTION(BlueprintPure, Category = "Cooking|Actions")
    float GetCookingProgress() const { return CookingProgress; }

    // ========== RECIPE MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Cooking|Recipes")
    void LearnRecipe(const FString& RecipeID);

    UFUNCTION(BlueprintPure, Category = "Cooking|Recipes")
    bool KnowsRecipe(const FString& RecipeID) const;

    UFUNCTION(BlueprintPure, Category = "Cooking|Recipes")
    TArray<FCookingRecipe> GetKnownRecipes() const;

    UFUNCTION(BlueprintPure, Category = "Cooking|Recipes")
    TArray<FCookingRecipe> GetRecipesByCategory(EFoodCategory Category) const;

    UFUNCTION(BlueprintPure, Category = "Cooking|Recipes")
    bool CanCookRecipe(const FString& RecipeID) const;

    // ========== QUALITY SYSTEM ==========

    UFUNCTION(BlueprintPure, Category = "Cooking|Quality")
    EFoodQuality CalculateQuality(float Progress, float SkillLevel) const;

    UFUNCTION(BlueprintPure, Category = "Cooking|Quality")
    float GetQualityMultiplier(EFoodQuality Quality) const;

    UFUNCTION(BlueprintPure, Category = "Cooking|Quality")
    bool IsInPerfectWindow() const;

    // ========== COOKING SKILL ==========

    UFUNCTION(BlueprintPure, Category = "Cooking|Skill")
    int32 GetCookingLevel() const { return CookingLevel; }

    UFUNCTION(BlueprintPure, Category = "Cooking|Skill")
    int32 GetCookingXP() const { return CookingXP; }

    UFUNCTION(BlueprintCallable, Category = "Cooking|Skill")
    void AddCookingXP(int32 XP);

    // ========== FOOD CONSUMPTION ==========

    UFUNCTION(BlueprintCallable, Category = "Cooking|Consume")
    void ConsumeFood(const FCookedFood& Food, AActor* Consumer);

    UFUNCTION(BlueprintCallable, Category = "Cooking|Consume")
    void ApplyFoodBuffs(const FCookedFood& Food, AActor* Target);

    // ========== STATIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Cooking|Stations")
    void RegisterCookingStation(const FCookingStation& Station);

    UFUNCTION(BlueprintPure, Category = "Cooking|Stations")
    FCookingStation GetNearestStation(const FVector& Location, ECookingMethod Method) const;

    UFUNCTION(BlueprintPure, Category = "Cooking|Stations")
    bool CanUseStation(const FString& StationID, ECookingMethod Method) const;

    // ========== DISCOVERY ==========

    UFUNCTION(BlueprintCallable, Category = "Cooking|Discovery")
    void DiscoverRecipeByExperiment(const TArray<FString>& IngredientIDs);

    UFUNCTION(BlueprintPure, Category = "Cooking|Discovery")
    int32 GetRecipesDiscovered() const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnCookingStarted, FString, RecipeID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnCookingFinished, FString, RecipeID, EFoodQuality, Quality, FString, ResultItemID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnRecipeLearned, FString, RecipeID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnCookingLevelUp, int32, NewLevel);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnFoodBurnt, FString, RecipeID);

    UPROPERTY(BlueprintAssignable, Category = "Cooking|Events")
    FOnCookingStarted OnCookingStarted;

    UPROPERTY(BlueprintAssignable, Category = "Cooking|Events")
    FOnCookingFinished OnCookingFinished;

    UPROPERTY(BlueprintAssignable, Category = "Cooking|Events")
    FOnRecipeLearned OnRecipeLearned;

    UPROPERTY(BlueprintAssignable, Category = "Cooking|Events")
    FOnCookingLevelUp OnCookingLevelUp;

    UPROPERTY(BlueprintAssignable, Category = "Cooking|Events")
    FOnFoodBurnt OnFoodBurnt;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    TMap<FString, FCookingRecipe> AllRecipes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    TMap<FString, FCookingStation> CookingStations;

    // Quality multipliers
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    float BurntMultiplier = 0.25f;  // 25% effect

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    float PoorMultiplier = 0.5f;  // 50%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    float NormalMultiplier = 1.0f;  // 100%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    float GoodMultiplier = 1.25f;  // 125%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    float ExcellentMultiplier = 1.5f;  // 150%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    float MasterworkMultiplier = 2.0f;  // 200%

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    float BurntThreshold = 0.9f;  // >90% = burnt

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Cooking|Config")
    int32 XPPerLevel = 100;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    bool bCooking = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    FString CurrentRecipeID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    FString CurrentStationID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    float CookingProgress = 0.0f;  // 0-1

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    float CookingTimer = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    TArray<FString> KnownRecipes;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    int32 CookingLevel = 1;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    int32 CookingXP = 0;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cooking|State")
    TMap<FString, int32> RecipeUseCounts;  // RecipeID -> Times Cooked

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateCooking(float DeltaTime);
    void CompleteCooking(EFoodQuality Quality);
    void CheckLevelUp();
    bool HasRequiredIngredients(const FCookingRecipe& Recipe) const;
    void ConsumeIngredients(const FCookingRecipe& Recipe);
    FString FindMatchingRecipe(const TArray<FString>& IngredientIDs) const;
};
