// MountSystem.cpp
#include "MountSystem.h"
UMountSystem::UMountSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UMountSystem::BeginPlay() { Super::BeginPlay(); }
bool UMountSystem::Mount(const FString& MountID) {
    if (MountCollection.Contains(MountID) && !bIsMounted) {
        CurrentMount = MountCollection[MountID];
        bIsMounted = true;
        OnMounted.Broadcast(MountID);
        return true;
    }
    return false;
}
void UMountSystem::Dismount() {
    if (bIsMounted) {
        bIsMounted = false;
        OnDismounted.Broadcast();
    }
}
float UMountSystem::GetMountSpeed() const {
    return bIsMounted ? CurrentMount.SpeedBonus : 1.0f;
}
