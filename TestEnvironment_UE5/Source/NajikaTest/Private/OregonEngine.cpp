// OregonEngine.cpp - Oregon procedural event engine
#include "OregonEngine.h"
UOregonEngine::UOregonEngine() { PrimaryComponentTick.bCanEverTick = false; }
void UOregonEngine::BeginPlay() { Super::BeginPlay(); }
FOregonEvent UOregonEngine::GenerateEvent() {
    FOregonEvent Event;
    Event.EventID = FGuid::NewGuid().ToString();
    Event.Biome = static_cast<EBiomeType>(FMath::RandRange(0, 6));
    Event.Weather = static_cast<EWeatherType>(FMath::RandRange(0, 6));
    Event.TimeOfDay = static_cast<ETimeOfDay>(FMath::RandRange(0, 4));
    Event.Hazard = static_cast<EHazardType>(FMath::RandRange(0, 7));
    Event.Description = "Procedural event in progress";
    return Event;
}
void UOregonEngine::SpawnEvent(const FOregonEvent& Event) {
    OnEventSpawned.Broadcast(Event);
}
