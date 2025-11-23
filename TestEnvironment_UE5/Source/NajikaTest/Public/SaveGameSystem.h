// SaveGameSystem.h
// Complete Save/Load System with multiple slots, auto-save, cloud backup

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "InventoryComponent.h"
#include "ProgressionComponent.h"
#include "SaveGameSystem.generated.h"

// Save Slot Info
USTRUCT(BlueprintType)
struct FSaveSlotInfo
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString SlotName;

    UPROPERTY(BlueprintReadWrite)
    int32 SlotIndex = 0;

    UPROPERTY(BlueprintReadWrite)
    FDateTime LastSaveTime;

    UPROPERTY(BlueprintReadWrite)
    int32 PlayerLevel = 1;

    UPROPERTY(BlueprintReadWrite)
    FString CurrentLocation;

    UPROPERTY(BlueprintReadWrite)
    float PlayTime = 0.0f;  // Total playtime in seconds

    UPROPERTY(BlueprintReadWrite)
    bool bIsAutoSave = false;
};

// Complete Player Data
USTRUCT(BlueprintType)
struct FPlayerSaveData
{
    GENERATED_BODY()

    // Character State
    UPROPERTY(BlueprintReadWrite)
    FVector PlayerLocation = FVector::ZeroVector;

    UPROPERTY(BlueprintReadWrite)
    FRotator PlayerRotation = FRotator::ZeroRotator;

    UPROPERTY(BlueprintReadWrite)
    float Health = 100.0f;

    UPROPERTY(BlueprintReadWrite)
    float Stamina = 100.0f;

    UPROPERTY(BlueprintReadWrite)
    float Mana = 100.0f;

    // Progression
    UPROPERTY(BlueprintReadWrite)
    int32 Level = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 Experience = 0;

    UPROPERTY(BlueprintReadWrite)
    TMap<EAttributeType, int32> Attributes;

    UPROPERTY(BlueprintReadWrite)
    TMap<ESkillType, FSkillData> Skills;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> UnlockedTalents;

    // Inventory
    UPROPERTY(BlueprintReadWrite)
    TArray<FInventorySlot> InventorySlots;

    UPROPERTY(BlueprintReadWrite)
    int32 Gold = 0;

    // Equipment
    UPROPERTY(BlueprintReadWrite)
    TMap<FString, FString> EquippedItems;  // Slot -> ItemID

    // Quests
    UPROPERTY(BlueprintReadWrite)
    TArray<FString> CompletedQuests;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> ActiveQuests;

    // World State
    UPROPERTY(BlueprintReadWrite)
    FString CurrentMap;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> DiscoveredLocations;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, bool> WorldFlags;  // "BossDead_ForestKing": true

    // Statistics
    UPROPERTY(BlueprintReadWrite)
    float TotalPlayTime = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    int32 EnemiesKilled = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 Deaths = 0;

    UPROPERTY(BlueprintReadWrite)
    float DistanceTraveled = 0.0f;
};

UCLASS()
class NAJIKATEST_API USaveGameSystem : public USaveGame
{
    GENERATED_BODY()

public:
    USaveGameSystem();

    // ========== SAVE DATA ==========

    UPROPERTY(BlueprintReadWrite, Category = "SaveGame")
    FSaveSlotInfo SlotInfo;

    UPROPERTY(BlueprintReadWrite, Category = "SaveGame")
    FPlayerSaveData PlayerData;

    // ========== SAVE/LOAD ==========

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static bool SaveGame(USaveGameSystem* SaveGameObject, const FString& SlotName, int32 UserIndex = 0);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static USaveGameSystem* LoadGame(const FString& SlotName, int32 UserIndex = 0);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static bool DeleteSaveGame(const FString& SlotName, int32 UserIndex = 0);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static bool DoesSaveGameExist(const FString& SlotName, int32 UserIndex = 0);

    // ========== SLOT MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static TArray<FSaveSlotInfo> GetAllSaveSlots();

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static FSaveSlotInfo GetSaveSlotInfo(const FString& SlotName);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static int32 GetMaxSaveSlots() { return 10; }

    // ========== AUTO-SAVE ==========

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static void AutoSave(USaveGameSystem* SaveGameObject);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static USaveGameSystem* LoadAutoSave();

    // ========== QUICK SAVE/LOAD ==========

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static void QuickSave(USaveGameSystem* SaveGameObject);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    static USaveGameSystem* QuickLoad();

    // ========== DATA HELPERS ==========

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    void CapturePlayerData(AActor* PlayerCharacter);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    void RestorePlayerData(AActor* PlayerCharacter);

    UFUNCTION(BlueprintCallable, Category = "SaveGame")
    void UpdatePlayTime(float DeltaTime);

protected:
    // Save slot names
    static const FString AutoSaveSlotName;
    static const FString QuickSaveSlotName;
};

// Save Game Manager (Actor placed in level)
UCLASS()
class NAJIKATEST_API ASaveGameManager : public AActor
{
    GENERATED_BODY()

public:
    ASaveGameManager();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== AUTO-SAVE ==========

    UFUNCTION(BlueprintCallable, Category = "SaveManager")
    void EnableAutoSave(bool bEnable);

    UFUNCTION(BlueprintCallable, Category = "SaveManager")
    void TriggerAutoSave();

    UFUNCTION(BlueprintPure, Category = "SaveManager")
    bool IsAutoSaveEnabled() const { return bAutoSaveEnabled; }

    // ========== CURRENT SAVE ==========

    UFUNCTION(BlueprintCallable, Category = "SaveManager")
    void SetCurrentSaveSlot(const FString& SlotName);

    UFUNCTION(BlueprintPure, Category = "SaveManager")
    FString GetCurrentSaveSlot() const { return CurrentSaveSlot; }

    UFUNCTION(BlueprintCallable, Category = "SaveManager")
    void SaveCurrentGame();

    UFUNCTION(BlueprintCallable, Category = "SaveManager")
    void LoadCurrentGame();

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnGameSaved);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnGameLoaded);

    UPROPERTY(BlueprintAssignable, Category = "SaveManager|Events")
    FOnGameSaved OnGameSaved;

    UPROPERTY(BlueprintAssignable, Category = "SaveManager|Events")
    FOnGameLoaded OnGameLoaded;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SaveManager|Config")
    bool bAutoSaveEnabled = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SaveManager|Config")
    float AutoSaveInterval = 300.0f;  // 5 minutes

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SaveManager|Config")
    bool bSaveOnCheckpoint = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SaveManager|Config")
    bool bSaveOnLevelTransition = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SaveManager|State")
    FString CurrentSaveSlot = "Slot1";

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SaveManager|State")
    float TimeSinceLastAutoSave = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SaveManager|State")
    USaveGameSystem* CurrentSaveGame = nullptr;

private:
    void UpdateAutoSave(float DeltaTime);
};
