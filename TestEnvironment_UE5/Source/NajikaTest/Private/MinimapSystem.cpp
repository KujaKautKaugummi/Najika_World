// MinimapSystem.cpp
#include "MinimapSystem.h"
UMinimapSystem::UMinimapSystem() { PrimaryComponentTick.bCanEverTick = true; }
void UMinimapSystem::BeginPlay() { Super::BeginPlay(); }
void UMinimapSystem::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) {
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    UpdateMinimap();
}
void UMinimapSystem::AddMapMarker(const FMapMarker& Marker) {
    MapMarkers.Add(Marker);
    OnMarkerAdded.Broadcast(Marker);
}
void UMinimapSystem::RemoveMapMarker(const FString& MarkerID) {
    for (int32 i = MapMarkers.Num() - 1; i >= 0; i--) {
        if (MapMarkers[i].MarkerID == MarkerID) {
            MapMarkers.RemoveAt(i);
            OnMarkerRemoved.Broadcast(MarkerID);
            break;
        }
    }
}
void UMinimapSystem::UpdateMinimap() {
    // Update logic here
}
