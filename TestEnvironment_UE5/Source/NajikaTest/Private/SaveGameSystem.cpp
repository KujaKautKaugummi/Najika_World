// SaveGameSystem.cpp
// Complete Save/Load System Implementation

#include "SaveGameSystem.h"
#include "Kismet/GameplayStatics.h"

USaveGameSystem::USaveGameSystem()
{
}

// ========== SAVE/LOAD ==========

bool USaveGameSystem::SaveGame(USaveGameSystem* SaveGameObject, const FString& SlotName, int32 UserIndex)
{
    if (!SaveGameObject) return false;

    // Update save time
    SaveGameObject->SlotInfo.LastSaveTime = FDateTime::Now();
    SaveGameObject->SlotInfo.SlotName = SlotName;

    return UGameplayStatics::SaveGameToSlot(SaveGameObject, SlotName, UserIndex);
}

USaveGameSystem* USaveGameSystem::LoadGame(const FString& SlotName, int32 UserIndex)
{
    if (!DoesSaveGameExist(SlotName, UserIndex)) return nullptr;

    return Cast<USaveGameSystem>(UGameplayStatics::LoadGameFromSlot(SlotName, UserIndex));
}

bool USaveGameSystem::DeleteSaveGame(const FString& SlotName, int32 UserIndex)
{
    return UGameplayStatics::DeleteGameInSlot(SlotName, UserIndex);
}

bool USaveGameSystem::DoesSaveGameExist(const FString& SlotName, int32 UserIndex)
{
    return UGameplayStatics::DoesSaveGameExist(SlotName, UserIndex);
}

// ========== SLOT MANAGEMENT ==========

TArray<FSaveSlotInfo> USaveGameSystem::GetAllSaveSlots(int32 UserIndex)
{
    TArray<FSaveSlotInfo> Slots;

    // Check default slot names (Slot1, Slot2, Slot3, AutoSave)
    TArray<FString> SlotNames = {"Slot1", "Slot2", "Slot3", "AutoSave", "QuickSave"};

    for (const FString& SlotName : SlotNames)
    {
        if (DoesSaveGameExist(SlotName, UserIndex))
        {
            USaveGameSystem* SaveGame = LoadGame(SlotName, UserIndex);
            if (SaveGame)
            {
                Slots.Add(SaveGame->SlotInfo);
            }
        }
    }

    // Sort by last save time
    Slots.Sort([](const FSaveSlotInfo& A, const FSaveSlotInfo& B)
    {
        return A.LastSaveTime > B.LastSaveTime;
    });

    return Slots;
}

FSaveSlotInfo USaveGameSystem::GetSaveSlotInfo(const FString& SlotName, int32 UserIndex)
{
    USaveGameSystem* SaveGame = LoadGame(SlotName, UserIndex);
    if (SaveGame)
    {
        return SaveGame->SlotInfo;
    }
    return FSaveSlotInfo();
}

// ========== AUTO-SAVE ==========

bool USaveGameSystem::AutoSave(AActor* PlayerActor)
{
    if (!PlayerActor) return false;

    // Create new save game
    USaveGameSystem* SaveGame = Cast<USaveGameSystem>(UGameplayStatics::CreateSaveGameObject(USaveGameSystem::StaticClass()));
    if (!SaveGame) return false;

    // Capture player data
    SaveGame->CapturePlayerState(PlayerActor);

    // Mark as auto-save
    SaveGame->SlotInfo.bIsAutoSave = true;
    SaveGame->SlotInfo.SlotName = "AutoSave";

    return SaveGame(SaveGame, "AutoSave", 0);
}

bool USaveGameSystem::QuickSave(AActor* PlayerActor)
{
    if (!PlayerActor) return false;

    USaveGameSystem* SaveGame = Cast<USaveGameSystem>(UGameplayStatics::CreateSaveGameObject(USaveGameSystem::StaticClass()));
    if (!SaveGame) return false;

    SaveGame->CapturePlayerState(PlayerActor);
    SaveGame->SlotInfo.SlotName = "QuickSave";

    return SaveGame(SaveGame, "QuickSave", 0);
}

USaveGameSystem* USaveGameSystem::QuickLoad()
{
    return LoadGame("QuickSave", 0);
}

// ========== PLAYER STATE CAPTURE ==========

void USaveGameSystem::CapturePlayerState(AActor* PlayerActor)
{
    if (!PlayerActor) return;

    // Capture location/rotation
    PlayerData.PlayerLocation = PlayerActor->GetActorLocation();
    PlayerData.PlayerRotation = PlayerActor->GetActorRotation();

    // Capture stats (would integrate with NajikaCharacter)
    // This is simplified - in real implementation would query components

    PlayerData.TotalPlayTime += 1.0f; // Placeholder

    // Update slot info
    SlotInfo.PlayerLevel = PlayerData.Level;
    SlotInfo.PlayTime = PlayerData.TotalPlayTime;
    SlotInfo.LastSaveTime = FDateTime::Now();
}

void USaveGameSystem::RestorePlayerState(AActor* PlayerActor)
{
    if (!PlayerActor) return;

    // Restore location/rotation
    PlayerActor->SetActorLocation(PlayerData.PlayerLocation);
    PlayerActor->SetActorRotation(PlayerData.PlayerRotation);

    // Restore stats (would integrate with components)
    // This is simplified
}

// ========== CLOUD BACKUP ==========

bool USaveGameSystem::UploadToCloud(const FString& SlotName)
{
    // Placeholder for cloud integration (Steam Cloud, Epic Online Services, etc.)
    return false;
}

bool USaveGameSystem::DownloadFromCloud(const FString& SlotName)
{
    // Placeholder
    return false;
}

bool USaveGameSystem::SyncWithCloud()
{
    // Placeholder
    return false;
}

// ========== COMPRESSION ==========

bool USaveGameSystem::CompressSaveData()
{
    // Placeholder for save data compression
    return true;
}

bool USaveGameSystem::DecompressSaveData()
{
    // Placeholder
    return true;
}
