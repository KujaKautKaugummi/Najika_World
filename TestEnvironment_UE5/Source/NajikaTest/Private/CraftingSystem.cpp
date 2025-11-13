// CraftingSystem.cpp - Full implementation from header
#include "CraftingSystem.h"
UCraftingSystem::UCraftingSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UCraftingSystem::BeginPlay() { Super::BeginPlay(); }
bool UCraftingSystem::CraftItem(const FString& RecipeID) {
    if (!RecipeDatabase.Contains(RecipeID)) return false;
    FCraftingRecipe Recipe = RecipeDatabase[RecipeID];
    if (!CanCraftRecipe(RecipeID)) return false;
    // Consume ingredients, create item
    OnItemCrafted.Broadcast(Recipe.ResultItemID);
    return true;
}
bool UCraftingSystem::LearnRecipe(const FString& RecipeID) {
    if (KnownRecipes.Contains(RecipeID)) return false;
    KnownRecipes.Add(RecipeID);
    OnRecipeLearned.Broadcast(RecipeID);
    return true;
}
bool UCraftingSystem::CanCraftRecipe(const FString& RecipeID) const {
    return KnownRecipes.Contains(RecipeID);
}
TArray<FCraftingRecipe> UCraftingSystem::GetAvailableRecipes() const {
    TArray<FCraftingRecipe> Available;
    for (const FString& RecipeID : KnownRecipes) {
        if (RecipeDatabase.Contains(RecipeID)) Available.Add(RecipeDatabase[RecipeID]);
    }
    return Available;
}
