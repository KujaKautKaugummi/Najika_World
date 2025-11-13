// OpenWorldManager.h
// Open World Management System for 500x500m world
// Handles: Biomes, Weather, Day/Night, Streaming, NPCs

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "OpenWorldManager.generated.h"

// Biome Type (from Oregon-Engine)
UENUM(BlueprintType)
enum class EWorldBiome : uint8
{
    WB_Forest UMETA(DisplayName = "Wald"),
    WB_Mountain UMETA(DisplayName = "Berg"),
    WB_Desert UMETA(DisplayName = "Wüste"),
    WB_Snow UMETA(DisplayName = "Schnee"),
    WB_Swamp UMETA(DisplayName = "Sumpf"),
    WB_Volcano UMETA(DisplayName = "Vulkan"),
    WB_Ocean UMETA(DisplayName = "Ozean")
};

// Weather Type
UENUM(BlueprintType)
enum class EWorldWeather : uint8
{
    WW_Clear UMETA(DisplayName = "Klar"),
    WW_Rain UMETA(DisplayName = "Regen"),
    WW_Storm UMETA(DisplayName = "Sturm"),
    WW_Snow UMETA(DisplayName = "Schnee"),
    WW_Fog UMETA(DisplayName = "Nebel"),
    WW_Sandstorm UMETA(DisplayName = "Sandsturm"),
    WW_Heatwave UMETA(DisplayName = "Hitze")
};

// Time of Day
UENUM(BlueprintType)
enum class ETimeOfDay : uint8
{
    TD_Morning UMETA(DisplayName = "Morgen (6-12)"),
    TD_Noon UMETA(DisplayName = "Mittag (12-15)"),
    TD_Evening UMETA(DisplayName = "Abend (15-20)"),
    TD_Night UMETA(DisplayName = "Nacht (20-24)"),
    TD_Midnight UMETA(DisplayName = "Mitternacht (0-6)")
};

// World Chunk (for streaming)
USTRUCT(BlueprintType)
struct FWorldChunk
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FVector ChunkLocation;

    UPROPERTY(BlueprintReadWrite)
    int32 ChunkSize = 10000;  // 100x100m per chunk = 25 chunks for 500x500m

    UPROPERTY(BlueprintReadWrite)
    EWorldBiome Biome;

    UPROPERTY(BlueprintReadWrite)
    bool bIsLoaded = false;

    UPROPERTY(BlueprintReadWrite)
    TArray<AActor*> SpawnedActors;
};

// World State
USTRUCT(BlueprintType)
struct FWorldState
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    EWorldWeather CurrentWeather = EWorldWeather::WW_Clear;

    UPROPERTY(BlueprintReadWrite)
    ETimeOfDay TimeOfDay = ETimeOfDay::TD_Morning;

    UPROPERTY(BlueprintReadWrite)
    float WorldTime = 6.0f;  // 0-24 hours

    UPROPERTY(BlueprintReadWrite)
    int32 DayNumber = 1;

    UPROPERTY(BlueprintReadWrite)
    float Temperature = 20.0f;

    UPROPERTY(BlueprintReadWrite)
    float WindSpeed = 0.0f;
};

UCLASS()
class NAJIKAGAME_API AOpenWorldManager : public AActor
{
    GENERATED_BODY()

public:
    AOpenWorldManager();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== WORLD STREAMING ==========

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Streaming")
    void LoadChunk(const FVector& ChunkLocation);

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Streaming")
    void UnloadChunk(const FVector& ChunkLocation);

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Streaming")
    void UpdateChunksAroundPlayer(APawn* Player, float LoadRadius);

    UFUNCTION(BlueprintPure, Category = "OpenWorld|Streaming")
    TArray<FWorldChunk> GetLoadedChunks() const { return LoadedChunks; }

    // ========== WEATHER SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Weather")
    void SetWeather(EWorldWeather NewWeather);

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Weather")
    void TransitionWeather(EWorldWeather TargetWeather, float TransitionDuration);

    UFUNCTION(BlueprintPure, Category = "OpenWorld|Weather")
    EWorldWeather GetCurrentWeather() const { return WorldState.CurrentWeather; }

    // ========== TIME SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Time")
    void SetWorldTime(float NewTime);

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Time")
    void SetTimeScale(float NewScale);

    UFUNCTION(BlueprintPure, Category = "OpenWorld|Time")
    float GetWorldTime() const { return WorldState.WorldTime; }

    UFUNCTION(BlueprintPure, Category = "OpenWorld|Time")
    ETimeOfDay GetTimeOfDay() const { return WorldState.TimeOfDay; }

    UFUNCTION(BlueprintPure, Category = "OpenWorld|Time")
    int32 GetDayNumber() const { return WorldState.DayNumber; }

    // ========== BIOME SYSTEM ==========

    UFUNCTION(BlueprintPure, Category = "OpenWorld|Biome")
    EWorldBiome GetBiomeAtLocation(const FVector& Location) const;

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|Biome")
    void GenerateBiomeMap();

    // ========== NPC SPAWNING ==========

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|NPCs")
    void SpawnNPCsInChunk(const FWorldChunk& Chunk);

    UFUNCTION(BlueprintCallable, Category = "OpenWorld|NPCs")
    void DespawnNPCsInChunk(const FWorldChunk& Chunk);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeatherChanged, EWorldWeather, NewWeather);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTimeOfDayChanged, ETimeOfDay, NewTimeOfDay);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnChunkLoaded, FWorldChunk, Chunk);

    UPROPERTY(BlueprintAssignable, Category = "OpenWorld|Events")
    FOnWeatherChanged OnWeatherChanged;

    UPROPERTY(BlueprintAssignable, Category = "OpenWorld|Events")
    FOnTimeOfDayChanged OnTimeOfDayChanged;

    UPROPERTY(BlueprintAssignable, Category = "OpenWorld|Events")
    FOnChunkLoaded OnChunkLoaded;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenWorld|Config")
    int32 WorldSize = 50000;  // 500x500m in cm

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenWorld|Config")
    int32 ChunkSize = 10000;  // 100x100m per chunk

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenWorld|Config")
    float TimeScale = 1.0f;  // 1.0 = real-time, 10.0 = 10x faster

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenWorld|Config")
    float ChunkLoadRadius = 20000.0f;  // 200m load radius

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenWorld|Config")
    float ChunkUnloadRadius = 25000.0f;  // 250m unload radius

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenWorld|Config")
    bool bDynamicWeather = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenWorld|Config")
    float WeatherTransitionTime = 60.0f;  // 1 minute

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "OpenWorld|State")
    FWorldState WorldState;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "OpenWorld|State")
    TArray<FWorldChunk> LoadedChunks;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "OpenWorld|State")
    TMap<FVector, EWorldBiome> BiomeMap;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "OpenWorld|State")
    EWorldWeather TargetWeather = EWorldWeather::WW_Clear;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "OpenWorld|State")
    float WeatherTransitionProgress = 0.0f;

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateTimeOfDay(float DeltaTime);
    void UpdateWeather(float DeltaTime);
    void UpdateChunkStreaming();

    FVector GetChunkLocationFromWorldLocation(const FVector& WorldLocation) const;
    ETimeOfDay CalculateTimeOfDay(float WorldTime) const;
    void ApplyWeatherEffects(EWorldWeather Weather);

    TArray<FVector> GetChunksInRadius(const FVector& Center, float Radius) const;
};
