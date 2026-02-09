// FishingSystem.cpp
#include "FishingSystem.h"
UFishingSystem::UFishingSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UFishingSystem::BeginPlay() { Super::BeginPlay(); }
void UFishingSystem::StartFishing() {
    bIsFishing = true;
    FishingTime = 0.0f;
    OnFishingStarted.Broadcast();
}
void UFishingSystem::StopFishing() {
    bIsFishing = false;
    OnFishingStopped.Broadcast();
}
void UFishingSystem::CatchFish() {
    if (bIsFishing) {
        FString FishID = "CommonFish";
        OnFishCaught.Broadcast(FishID);
        StopFishing();
    }
}
