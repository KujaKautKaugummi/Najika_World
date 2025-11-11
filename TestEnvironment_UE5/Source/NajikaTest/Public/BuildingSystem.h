// BuildingSystem.h
// Complete Building/Housing System with placement, upgrading, furniture, permissions

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "BuildingSystem.generated.h"

// Building Type
UENUM(BlueprintType)
enum class EBuildingType : uint8
{
    BT_House UMETA(DisplayName = "House"),
    BT_Workshop UMETA(DisplayName = "Workshop"),
    BT_Farm UMETA(DisplayName = "Farm"),
    BT_Storage UMETA(DisplayName = "Storage"),
    BT_Defense UMETA(DisplayName = "Defense Tower"),
    BT_Decoration UMETA(DisplayName = "Decoration"),
    BT_Furniture UMETA(DisplayName = "Furniture"),
    BT_Utility UMETA(DisplayName = "Utility")
};

// Building State
UENUM(BlueprintType)
enum class EBuildingState : uint8
{
    BS_Blueprint UMETA(DisplayName = "Blueprint (Preview)"),
    BS_UnderConstruction UMETA(DisplayName = "Under Construction"),
    BS_Complete UMETA(DisplayName = "Complete"),
    BS_Damaged UMETA(DisplayName = "Damaged"),
    BS_Upgrading UMETA(DisplayName = "Upgrading")
};

// Placement Result
UENUM(BlueprintType)
enum class EPlacementResult : uint8
{
    PR_Success UMETA(DisplayName = "Success"),
    PR_InvalidLocation UMETA(DisplayName = "Invalid Location"),
    PR_Obstructed UMETA(DisplayName = "Obstructed"),
    PR_OutOfBounds UMETA(DisplayName = "Out of Buildable Area"),
    PR_InsufficientResources UMETA(DisplayName = "Insufficient Resources"),
    PR_NoPermission UMETA(DisplayName = "No Permission")
};

// Building Data
USTRUCT(BlueprintType)
struct FBuildingData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BuildingID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BuildingName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EBuildingType Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TSubclassOf<AActor> BuildingClass;  // 3D model blueprint

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, int32> ConstructionCost;  // MaterialID -> Quantity

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float ConstructionTime = 10.0f;  // Seconds

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxLevel = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector Size = FVector(500, 500, 300);  // Collision box

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RequiredBuildingID;  // Prerequisite

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bCanRotate = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bSnapToGrid = true;
};

// Placed Building Instance
USTRUCT(BlueprintType)
struct FPlacedBuilding
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString InstanceID;

    UPROPERTY(BlueprintReadWrite)
    FString BuildingID;

    UPROPERTY(BlueprintReadWrite)
    FVector Location;

    UPROPERTY(BlueprintReadWrite)
    FRotator Rotation;

    UPROPERTY(BlueprintReadWrite)
    int32 Level = 1;

    UPROPERTY(BlueprintReadWrite)
    EBuildingState State = EBuildingState::BS_Blueprint;

    UPROPERTY(BlueprintReadWrite)
    float Health = 100.0f;

    UPROPERTY(BlueprintReadWrite)
    float MaxHealth = 100.0f;

    UPROPERTY(BlueprintReadWrite)
    FString OwnerPlayerID;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> AllowedPlayerIDs;  // Permissions

    UPROPERTY(BlueprintReadWrite)
    FDateTime PlacedTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime CompletionTime;

    UPROPERTY(BlueprintReadWrite)
    AActor* SpawnedActor = nullptr;

    float GetHealthPercent() const { return MaxHealth > 0.0f ? Health / MaxHealth : 0.0f; }
};

// Building Plot
USTRUCT(BlueprintType)
struct FBuildingPlot
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString PlotID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector Center;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FVector Size = FVector(10000, 10000, 1000);  // 100x100x10 meters

    UPROPERTY(BlueprintReadWrite)
    FString OwnerPlayerID;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> PlacedBuildingIDs;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxBuildings = 50;

    UPROPERTY(BlueprintReadWrite)
    bool bIsPublic = false;  // Anyone can visit

    bool IsFull() const { return PlacedBuildingIDs.Num() >= MaxBuildings; }
    bool IsInBounds(const FVector& Location) const;
};

UCLASS()
class NAJIKATEST_API ABuildingSystem : public AActor
{
    GENERATED_BODY()

public:
    ABuildingSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== PLACEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Building|Placement")
    void StartPlacementMode(const FString& BuildingID, const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "Building|Placement")
    void CancelPlacementMode();

    UFUNCTION(BlueprintCallable, Category = "Building|Placement")
    EPlacementResult PlaceBuilding(const FVector& Location, const FRotator& Rotation, const FString& PlotID);

    UFUNCTION(BlueprintPure, Category = "Building|Placement")
    bool IsInPlacementMode() const { return bInPlacementMode; }

    UFUNCTION(BlueprintPure, Category = "Building|Placement")
    bool CanPlaceAt(const FVector& Location, const FRotator& Rotation, const FString& PlotID) const;

    // ========== CONSTRUCTION ==========

    UFUNCTION(BlueprintCallable, Category = "Building|Construction")
    void StartConstruction(const FString& InstanceID);

    UFUNCTION(BlueprintPure, Category = "Building|Construction")
    float GetConstructionProgress(const FString& InstanceID) const;

    UFUNCTION(BlueprintCallable, Category = "Building|Construction")
    void SpeedUpConstruction(const FString& InstanceID, float Multiplier);

    // ========== BUILDING MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Building|Management")
    void DemolishBuilding(const FString& InstanceID, const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "Building|Management")
    void UpgradeBuilding(const FString& InstanceID);

    UFUNCTION(BlueprintCallable, Category = "Building|Management")
    void RepairBuilding(const FString& InstanceID, float Amount);

    UFUNCTION(BlueprintPure, Category = "Building|Management")
    FPlacedBuilding GetBuilding(const FString& InstanceID) const;

    UFUNCTION(BlueprintPure, Category = "Building|Management")
    TArray<FPlacedBuilding> GetPlayerBuildings(const FString& PlayerID) const;

    // ========== DAMAGE SYSTEM ==========

    UFUNCTION(BlueprintCallable, Category = "Building|Damage")
    void DamageBuilding(const FString& InstanceID, float Damage);

    UFUNCTION(BlueprintPure, Category = "Building|Damage")
    bool IsBuildingDestroyed(const FString& InstanceID) const;

    // ========== PERMISSIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Building|Permissions")
    void GrantPermission(const FString& InstanceID, const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "Building|Permissions")
    void RevokePermission(const FString& InstanceID, const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Building|Permissions")
    bool HasPermission(const FString& InstanceID, const FString& PlayerID) const;

    // ========== PLOTS ==========

    UFUNCTION(BlueprintCallable, Category = "Building|Plots")
    FString CreatePlot(const FVector& Center, const FVector& Size, const FString& OwnerPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Building|Plots")
    void DeletePlot(const FString& PlotID);

    UFUNCTION(BlueprintPure, Category = "Building|Plots")
    FBuildingPlot GetPlot(const FString& PlotID) const;

    UFUNCTION(BlueprintPure, Category = "Building|Plots")
    FString GetPlotAtLocation(const FVector& Location) const;

    // ========== BLUEPRINTS/RECIPES ==========

    UFUNCTION(BlueprintCallable, Category = "Building|Blueprints")
    void LearnBlueprint(const FString& BuildingID, const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Building|Blueprints")
    bool KnowsBlueprint(const FString& BuildingID, const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Building|Blueprints")
    TArray<FBuildingData> GetKnownBlueprints(const FString& PlayerID) const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnBuildingPlaced, FString, InstanceID, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnBuildingComplete, FString, InstanceID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnBuildingDemolished, FString, InstanceID, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnBuildingUpgraded, FString, InstanceID, int32, NewLevel);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnBuildingDestroyed, FString, InstanceID);

    UPROPERTY(BlueprintAssignable, Category = "Building|Events")
    FOnBuildingPlaced OnBuildingPlaced;

    UPROPERTY(BlueprintAssignable, Category = "Building|Events")
    FOnBuildingComplete OnBuildingComplete;

    UPROPERTY(BlueprintAssignable, Category = "Building|Events")
    FOnBuildingDemolished OnBuildingDemolished;

    UPROPERTY(BlueprintAssignable, Category = "Building|Events")
    FOnBuildingUpgraded OnBuildingUpgraded;

    UPROPERTY(BlueprintAssignable, Category = "Building|Events")
    FOnBuildingDestroyed OnBuildingDestroyed;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building|Config")
    TMap<FString, FBuildingData> BuildingDatabase;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building|Config")
    float GridSize = 100.0f;  // 1 meter snap grid

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building|Config")
    bool bRequirePlots = true;  // Can only build in owned plots

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building|Config")
    float DemolishRefundPercent = 0.5f;  // 50% materials back

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Building|Config")
    bool bEnableBuildingDamage = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Building|State")
    TMap<FString, FPlacedBuilding> PlacedBuildings;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Building|State")
    TMap<FString, FBuildingPlot> Plots;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Building|State")
    bool bInPlacementMode = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Building|State")
    FString CurrentBuildingID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Building|State")
    FString CurrentPlayerID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Building|State")
    TMap<FString, TArray<FString>> PlayerBlueprints;  // PlayerID -> BuildingIDs

private:
    // ========== HELPER FUNCTIONS ==========

    FVector SnapToGrid(const FVector& Location) const;
    bool CheckObstructions(const FVector& Location, const FVector& Size, const FString& ExcludeInstanceID = "") const;
    void SpawnBuildingActor(FPlacedBuilding& Building);
    void UpdateConstructionProgress(float DeltaTime);
    FString GenerateInstanceID() const;
};
