// CookingSystem.cpp
#include "CookingSystem.h"
UCookingSystem::UCookingSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UCookingSystem::BeginPlay() { Super::BeginPlay(); }
bool UCookingSystem::CookRecipe(const FString& RecipeID) {
    if (!CookingRecipes.Contains(RecipeID)) return false;
    OnFoodCooked.Broadcast(RecipeID);
    return true;
}
bool UCookingSystem::LearnCookingRecipe(const FString& RecipeID) {
    if (KnownRecipes.Contains(RecipeID)) return false;
    KnownRecipes.Add(RecipeID);
    return true;
}
