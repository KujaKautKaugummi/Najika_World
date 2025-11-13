// PetSystem.cpp
#include "PetSystem.h"
UPetSystem::UPetSystem() { PrimaryComponentTick.bCanEverTick = true; }
void UPetSystem::BeginPlay() { Super::BeginPlay(); }
void UPetSystem::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) {
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    if (ActivePet.IsValid()) {
        UpdatePetHappiness(DeltaTime);
    }
}
bool UPetSystem::SummonPet(const FString& PetID) {
    if (PetCollection.Contains(PetID)) {
        ActivePet = PetCollection[PetID];
        OnPetSummoned.Broadcast(PetID);
        return true;
    }
    return false;
}
void UPetSystem::DismissPet() {
    ActivePet = FPetData();
    OnPetDismissed.Broadcast();
}
void UPetSystem::FeedPet(const FString& FoodItemID) {
    if (ActivePet.IsValid()) {
        ActivePet.Happiness = FMath::Min(100.0f, ActivePet.Happiness + 10.0f);
        OnPetFed.Broadcast(FoodItemID);
    }
}
void UPetSystem::UpdatePetHappiness(float DeltaTime) {
    if (ActivePet.IsValid()) {
        ActivePet.Happiness = FMath::Max(0.0f, ActivePet.Happiness - HappinessDecayRate * DeltaTime);
    }
}
