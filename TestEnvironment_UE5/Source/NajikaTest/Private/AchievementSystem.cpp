// AchievementSystem.cpp
#include "AchievementSystem.h"
UAchievementSystem::UAchievementSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UAchievementSystem::BeginPlay() { Super::BeginPlay(); }
bool UAchievementSystem::UnlockAchievement(const FString& AchievementID) {
    if (UnlockedAchievements.Contains(AchievementID)) return false;
    UnlockedAchievements.Add(AchievementID);
    if (AchievementDatabase.Contains(AchievementID)) {
        OnAchievementUnlocked.Broadcast(AchievementDatabase[AchievementID]);
    }
    return true;
}
void UAchievementSystem::UpdateProgress(const FString& AchievementID, int32 Progress) {
    if (AchievementDatabase.Contains(AchievementID)) {
        FAchievement& Achievement = AchievementDatabase[AchievementID];
        Achievement.CurrentProgress = FMath::Min(Achievement.CurrentProgress + Progress, Achievement.RequiredProgress);
        if (Achievement.CurrentProgress >= Achievement.RequiredProgress) {
            UnlockAchievement(AchievementID);
        }
    }
}
bool UAchievementSystem::IsAchievementUnlocked(const FString& AchievementID) const {
    return UnlockedAchievements.Contains(AchievementID);
}
TArray<FAchievement> UAchievementSystem::GetUnlockedAchievements() const {
    TArray<FAchievement> Result;
    for (const FString& ID : UnlockedAchievements) {
        if (AchievementDatabase.Contains(ID)) Result.Add(AchievementDatabase[ID]);
    }
    return Result;
}
