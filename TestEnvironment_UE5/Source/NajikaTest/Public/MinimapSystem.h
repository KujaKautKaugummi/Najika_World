// MinimapSystem.h
// Complete Minimap/Compass System with POIs, fog of war, waypoints, tracking

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MinimapSystem.generated.h"

// POI (Point of Interest) Type
UENUM(BlueprintType)
enum class EPOIType : uint8
{
    POI_Quest UMETA(DisplayName = "Quest Marker"),
    POI_Waypoint UMETA(DisplayName = "Player Waypoint"),
    POI_NPC UMETA(DisplayName = "NPC"),
    POI_Merchant UMETA(DisplayName = "Merchant/Shop"),
    POI_Enemy UMETA(DisplayName = "Enemy"),
    POI_Resource UMETA(DisplayName = "Resource Node"),
    POI_Treasure UMETA(DisplayName = "Treasure"),
    POI_Portal UMETA(DisplayName = "Portal/Teleport"),
    POI_PartyMember UMETA(DisplayName = "Party Member"),
    POI_Custom UMETA(DisplayName = "Custom")
};

// Map Marker Priority
UENUM(BlueprintType)
enum class EMarkerPriority : uint8
{
    MP_Low UMETA(DisplayName = "Low"),
    MP_Medium UMETA(DisplayName = "Medium"),
    MP_High UMETA(DisplayName = "High"),
    MP_Critical UMETA(DisplayName = "Critical")
};

// Point of Interest
USTRUCT(BlueprintType)
struct FPOI
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString POIID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString POIName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EPOIType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector WorldLocation;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    UTexture2D* Icon = nullptr;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FLinearColor Color = FLinearColor::White;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EMarkerPriority Priority = EMarkerPriority::MP_Medium;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MinZoomLevel = 0.0f;  // Only show when zoomed in enough

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bShowOnMinimap = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bShowOnWorldMap = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bShowOnCompass = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bTrackDistance = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bPersistent = false;  // Save across sessions

    UPROPERTY(BlueprintReadWrite)
    AActor* TrackedActor = nullptr;  // Dynamic tracking

    UPROPERTY(BlueprintReadWrite)
    bool bDiscovered = false;
};

// Fog of War Cell
USTRUCT(BlueprintType)
struct FFogCell
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FVector2D CellCoordinates;

    UPROPERTY(BlueprintReadWrite)
    bool bExplored = false;

    UPROPERTY(BlueprintReadWrite)
    FDateTime ExploredTime;
};

// Waypoint Data
USTRUCT(BlueprintType)
struct FWaypoint
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString WaypointID;

    UPROPERTY(BlueprintReadWrite)
    FString Name;

    UPROPERTY(BlueprintReadWrite)
    FVector Location;

    UPROPERTY(BlueprintReadWrite)
    FLinearColor Color = FLinearColor::Yellow;

    UPROPERTY(BlueprintReadWrite)
    FDateTime CreatedTime;

    UPROPERTY(BlueprintReadWrite)
    bool bShowPath = true;  // Show navigation path
};

UCLASS()
class NAJIKATEST_API AMinimapSystem : public AActor
{
    GENERATED_BODY()

public:
    AMinimapSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== POI MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Minimap|POI")
    void AddPOI(const FPOI& POI);

    UFUNCTION(BlueprintCallable, Category = "Minimap|POI")
    void RemovePOI(const FString& POIID);

    UFUNCTION(BlueprintCallable, Category = "Minimap|POI")
    void UpdatePOILocation(const FString& POIID, const FVector& NewLocation);

    UFUNCTION(BlueprintPure, Category = "Minimap|POI")
    TArray<FPOI> GetPOIsInRadius(const FVector& Center, float Radius) const;

    UFUNCTION(BlueprintPure, Category = "Minimap|POI")
    TArray<FPOI> GetPOIsByType(EPOIType Type) const;

    UFUNCTION(BlueprintPure, Category = "Minimap|POI")
    FPOI GetPOI(const FString& POIID) const;

    UFUNCTION(BlueprintCallable, Category = "Minimap|POI")
    void DiscoverPOI(const FString& POIID);

    // ========== WAYPOINT SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "Minimap|Waypoint")
    void SetWaypoint(const FVector& Location, const FString& Name = "Waypoint");

    UFUNCTION(BlueprintCallable, Category = "Minimap|Waypoint")
    void ClearWaypoint();

    UFUNCTION(BlueprintPure, Category = "Minimap|Waypoint")
    bool HasActiveWaypoint() const { return ActiveWaypoint.WaypointID != ""; }

    UFUNCTION(BlueprintPure, Category = "Minimap|Waypoint")
    FWaypoint GetActiveWaypoint() const { return ActiveWaypoint; }

    UFUNCTION(BlueprintPure, Category = "Minimap|Waypoint")
    float GetDistanceToWaypoint(const FVector& PlayerLocation) const;

    // ========== FOG OF WAR ==========

    UFUNCTION(BlueprintCallable, Category = "Minimap|FogOfWar")
    void EnableFogOfWar(bool bEnable);

    UFUNCTION(BlueprintCallable, Category = "Minimap|FogOfWar")
    void RevealArea(const FVector& WorldLocation, float Radius);

    UFUNCTION(BlueprintPure, Category = "Minimap|FogOfWar")
    bool IsAreaExplored(const FVector& WorldLocation) const;

    UFUNCTION(BlueprintPure, Category = "Minimap|FogOfWar")
    float GetExplorationPercent() const;

    UFUNCTION(BlueprintCallable, Category = "Minimap|FogOfWar")
    void ClearFogOfWar();

    // ========== MINIMAP SETTINGS ==========

    UFUNCTION(BlueprintCallable, Category = "Minimap|Settings")
    void SetMinimapZoom(float ZoomLevel);

    UFUNCTION(BlueprintPure, Category = "Minimap|Settings")
    float GetMinimapZoom() const { return CurrentZoom; }

    UFUNCTION(BlueprintCallable, Category = "Minimap|Settings")
    void SetMinimapRotation(bool bRotate);

    UFUNCTION(BlueprintCallable, Category = "Minimap|Settings")
    void SetMinimapSize(float Size);

    UFUNCTION(BlueprintCallable, Category = "Minimap|Settings")
    void ToggleMinimap();

    UFUNCTION(BlueprintPure, Category = "Minimap|Settings")
    bool IsMinimapVisible() const { return bMinimapVisible; }

    // ========== COMPASS ==========

    UFUNCTION(BlueprintPure, Category = "Minimap|Compass")
    float GetPlayerHeading() const;

    UFUNCTION(BlueprintPure, Category = "Minimap|Compass")
    FVector2D GetCompassDirection(const FVector& TargetLocation, const FVector& PlayerLocation, float PlayerYaw) const;

    UFUNCTION(BlueprintPure, Category = "Minimap|Compass")
    TArray<FPOI> GetPOIsOnCompass(const FVector& PlayerLocation, float PlayerYaw, float ViewAngle = 120.0f) const;

    // ========== TRACKING ==========

    UFUNCTION(BlueprintCallable, Category = "Minimap|Tracking")
    void TrackActor(AActor* Actor, EPOIType Type, const FString& Name = "Tracked");

    UFUNCTION(BlueprintCallable, Category = "Minimap|Tracking")
    void UntrackActor(AActor* Actor);

    UFUNCTION(BlueprintPure, Category = "Minimap|Tracking")
    TArray<AActor*> GetTrackedActors() const;

    // ========== WORLD MAP ==========

    UFUNCTION(BlueprintCallable, Category = "Minimap|WorldMap")
    void OpenWorldMap();

    UFUNCTION(BlueprintCallable, Category = "Minimap|WorldMap")
    void CloseWorldMap();

    UFUNCTION(BlueprintPure, Category = "Minimap|WorldMap")
    bool IsWorldMapOpen() const { return bWorldMapOpen; }

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPOIDiscovered, FPOI, POI);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWaypointSet, FVector, Location);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnWaypointReached);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAreaExplored, float, ExplorationPercent);

    UPROPERTY(BlueprintAssignable, Category = "Minimap|Events")
    FOnPOIDiscovered OnPOIDiscovered;

    UPROPERTY(BlueprintAssignable, Category = "Minimap|Events")
    FOnWaypointSet OnWaypointSet;

    UPROPERTY(BlueprintAssignable, Category = "Minimap|Events")
    FOnWaypointReached OnWaypointReached;

    UPROPERTY(BlueprintAssignable, Category = "Minimap|Events")
    FOnAreaExplored OnAreaExplored;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    float DefaultZoom = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    float MinZoom = 0.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    float MaxZoom = 3.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    float MinimapRadius = 1000.0f;  // 10 meters visible radius

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    bool bRotateWithPlayer = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    bool bEnableFogOfWar = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    float FogCellSize = 1000.0f;  // 10x10 meter cells

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    float AutoRevealRadius = 1500.0f;  // 15 meters auto-reveal

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    float WaypointReachedDistance = 200.0f;  // 2 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Minimap|Config")
    int32 MaxPOIsOnMinimap = 50;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Minimap|State")
    TMap<FString, FPOI> POIs;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Minimap|State")
    FWaypoint ActiveWaypoint;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Minimap|State")
    TMap<FVector2D, FFogCell> FogOfWarCells;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Minimap|State")
    float CurrentZoom = 1.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Minimap|State")
    bool bMinimapVisible = true;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Minimap|State")
    bool bWorldMapOpen = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Minimap|State")
    TMap<AActor*, FString> TrackedActorPOIs;  // Actor -> POIID

private:
    // ========== HELPER FUNCTIONS ==========

    FVector2D WorldToMinimapCoordinates(const FVector& WorldLocation, const FVector& PlayerLocation) const;
    FVector2D GetFogCellCoordinates(const FVector& WorldLocation) const;
    void UpdateTrackedActors();
    void CheckWaypointReached(const FVector& PlayerLocation);
    void UpdateFogOfWar(const FVector& PlayerLocation);
};
