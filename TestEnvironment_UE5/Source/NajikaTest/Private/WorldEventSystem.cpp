// WorldEventSystem.cpp - From Batch 5 headers
#include "WorldEventSystem.h"
UWorldEventSystem::UWorldEventSystem() { PrimaryComponentTick.bCanEverTick = true; }
void UWorldEventSystem::BeginPlay() { Super::BeginPlay(); }
void UWorldEventSystem::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) {
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    UpdateActiveEvents(DeltaTime);
}
bool UWorldEventSystem::StartEvent(const FString& EventID) {
    if (EventDatabase.Contains(EventID)) {
        FWorldEvent Event = EventDatabase[EventID];
        Event.Status = EEventStatus::ES_Active;
        ActiveEvents.Add(Event);
        OnEventStarted.Broadcast(Event);
        return true;
    }
    return false;
}
void UWorldEventSystem::UpdateActiveEvents(float DeltaTime) {
    for (FWorldEvent& Event : ActiveEvents) {
        if (Event.Status == EEventStatus::ES_Active) {
            Event.TimeRemaining -= DeltaTime;
            if (Event.TimeRemaining <= 0.0f) {
                Event.Status = EEventStatus::ES_Completed;
                OnEventCompleted.Broadcast(Event);
            }
        }
    }
}
