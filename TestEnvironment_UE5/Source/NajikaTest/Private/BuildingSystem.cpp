// BuildingSystem.cpp
#include "BuildingSystem.h"
UBuildingSystem::UBuildingSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UBuildingSystem::BeginPlay() { Super::BeginPlay(); }
bool UBuildingSystem::PlaceBuilding(TSubclassOf<AActor> BuildingClass, FVector Location) {
    if (!CanPlaceBuilding(Location)) return false;
    AActor* Building = GetWorld()->SpawnActor<AActor>(BuildingClass, Location, FRotator::ZeroRotator);
    if (Building) {
        PlacedBuildings.Add(Building);
        OnBuildingPlaced.Broadcast(Building);
        return true;
    }
    return false;
}
bool UBuildingSystem::RemoveBuilding(AActor* Building) {
    if (!Building) return false;
    PlacedBuildings.Remove(Building);
    Building->Destroy();
    OnBuildingRemoved.Broadcast();
    return true;
}
bool UBuildingSystem::CanPlaceBuilding(FVector Location) const {
    return true; // Simplified
}
