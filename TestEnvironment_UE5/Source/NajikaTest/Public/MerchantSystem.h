// MerchantSystem.h
// Complete Merchant/Trading System with shops, bartering, reputation discounts

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MerchantSystem.generated.h"

// Shop Type
UENUM(BlueprintType)
enum class EShopType : uint8
{
    ST_General UMETA(DisplayName = "General Store"),
    ST_Weapon UMETA(DisplayName = "Weapon Shop"),
    ST_Armor UMETA(DisplayName = "Armor Shop"),
    ST_Alchemy UMETA(DisplayName = "Alchemy Shop"),
    ST_Magic UMETA(DisplayName = "Magic Shop"),
    ST_Blacksmith UMETA(DisplayName = "Blacksmith"),
    ST_Tavern UMETA(DisplayName = "Tavern/Inn"),
    ST_Stable UMETA(DisplayName = "Stable (Mounts)"),
    ST_Fence UMETA(DisplayName = "Fence (Stolen Goods)"),
    ST_Special UMETA(DisplayName = "Special/Unique")
};

// Transaction Type
UENUM(BlueprintType)
enum class ETransactionType : uint8
{
    TT_Buy UMETA(DisplayName = "Buy from Merchant"),
    TT_Sell UMETA(DisplayName = "Sell to Merchant"),
    TT_Repair UMETA(DisplayName = "Repair Item"),
    TT_Trade UMETA(DisplayName = "Player-to-Player Trade")
};

// Shop Item
USTRUCT(BlueprintType)
struct FShopItem
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ItemID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 BasePrice = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Stock = -1;  // -1 = Infinite

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxStock = -1;  // Max stock for restocking

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float RestockTime = 86400.0f;  // 24 hours in seconds

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredLevel = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredReputation = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString RequiredQuestID;  // Unlock after quest completion

    UPROPERTY(BlueprintReadWrite)
    FDateTime LastRestockTime;

    bool IsAvailable() const { return Stock != 0; }
    bool IsInfiniteStock() const { return Stock == -1; }
};

// Shop Definition
USTRUCT(BlueprintType)
struct FShop
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ShopID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString ShopName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EShopType ShopType;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FShopItem> Inventory;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float BuyPriceMultiplier = 1.0f;  // Markup

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float SellPriceMultiplier = 0.5f;  // How much merchant pays (50% of base)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float RepairCostMultiplier = 0.3f;  // Repair cost = 30% of item value

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MerchantGold = 10000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bBuysItems = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bSellsItems = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bRepairsItems = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bAcceptsStolenGoods = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString FactionID;  // For reputation discounts
};

// Trade Offer (Player-to-Player)
USTRUCT(BlueprintType)
struct FTradeOffer
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> OfferedItemIDs;

    UPROPERTY(BlueprintReadWrite)
    TArray<int32> OfferedQuantities;

    UPROPERTY(BlueprintReadWrite)
    int32 OfferedGold = 0;

    UPROPERTY(BlueprintReadWrite)
    bool bAccepted = false;

    UPROPERTY(BlueprintReadWrite)
    bool bLocked = false;  // Locked in, waiting for other player
};

// Transaction Record
USTRUCT(BlueprintType)
struct FTransactionRecord
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    ETransactionType Type;

    UPROPERTY(BlueprintReadWrite)
    FString ItemID;

    UPROPERTY(BlueprintReadWrite)
    int32 Quantity;

    UPROPERTY(BlueprintReadWrite)
    int32 Price;

    UPROPERTY(BlueprintReadWrite)
    FDateTime Timestamp;

    UPROPERTY(BlueprintReadWrite)
    FString ShopID;
};

UCLASS()
class NAJIKATEST_API AMerchantSystem : public AActor
{
    GENERATED_BODY()

public:
    AMerchantSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== SHOP MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Merchant|Shop")
    void OpenShop(const FString& ShopID, APlayerController* Customer);

    UFUNCTION(BlueprintCallable, Category = "Merchant|Shop")
    void CloseShop();

    UFUNCTION(BlueprintPure, Category = "Merchant|Shop")
    bool IsShopOpen() const { return bShopOpen; }

    UFUNCTION(BlueprintPure, Category = "Merchant|Shop")
    FShop GetShop(const FString& ShopID) const;

    UFUNCTION(BlueprintPure, Category = "Merchant|Shop")
    TArray<FShopItem> GetAvailableItems(const FString& ShopID, APlayerController* Customer) const;

    // ========== BUYING ==========

    UFUNCTION(BlueprintCallable, Category = "Merchant|Buy")
    bool BuyItem(const FString& ShopID, const FString& ItemID, int32 Quantity, APlayerController* Customer);

    UFUNCTION(BlueprintPure, Category = "Merchant|Buy")
    int32 GetBuyPrice(const FString& ShopID, const FString& ItemID, APlayerController* Customer) const;

    UFUNCTION(BlueprintPure, Category = "Merchant|Buy")
    bool CanAffordItem(const FString& ShopID, const FString& ItemID, int32 Quantity, APlayerController* Customer) const;

    // ========== SELLING ==========

    UFUNCTION(BlueprintCallable, Category = "Merchant|Sell")
    bool SellItem(const FString& ShopID, const FString& ItemID, int32 Quantity, APlayerController* Customer);

    UFUNCTION(BlueprintPure, Category = "Merchant|Sell")
    int32 GetSellPrice(const FString& ShopID, const FString& ItemID) const;

    UFUNCTION(BlueprintPure, Category = "Merchant|Sell")
    bool WillBuyItem(const FString& ShopID, const FString& ItemID) const;

    // ========== REPAIRING ==========

    UFUNCTION(BlueprintCallable, Category = "Merchant|Repair")
    bool RepairItem(const FString& ShopID, const FString& ItemID, APlayerController* Customer);

    UFUNCTION(BlueprintPure, Category = "Merchant|Repair")
    int32 GetRepairCost(const FString& ShopID, const FString& ItemID) const;

    UFUNCTION(BlueprintCallable, Category = "Merchant|Repair")
    void RepairAllItems(const FString& ShopID, APlayerController* Customer);

    // ========== REPUTATION DISCOUNTS ==========

    UFUNCTION(BlueprintPure, Category = "Merchant|Reputation")
    float GetReputationDiscount(const FString& ShopID, APlayerController* Customer) const;

    UFUNCTION(BlueprintPure, Category = "Merchant|Reputation")
    int32 GetAdjustedPrice(int32 BasePrice, float Discount) const;

    // ========== RESTOCKING ==========

    UFUNCTION(BlueprintCallable, Category = "Merchant|Restock")
    void RestockShop(const FString& ShopID);

    UFUNCTION(BlueprintCallable, Category = "Merchant|Restock")
    void RestockAllShops();

    // ========== PLAYER-TO-PLAYER TRADING ==========

    UFUNCTION(BlueprintCallable, Category = "Merchant|Trade")
    void InitiateTrade(APlayerController* Player1, APlayerController* Player2);

    UFUNCTION(BlueprintCallable, Category = "Merchant|Trade")
    void UpdateTradeOffer(APlayerController* Player, const FTradeOffer& Offer);

    UFUNCTION(BlueprintCallable, Category = "Merchant|Trade")
    void LockTradeOffer(APlayerController* Player);

    UFUNCTION(BlueprintCallable, Category = "Merchant|Trade")
    void AcceptTrade(APlayerController* Player);

    UFUNCTION(BlueprintCallable, Category = "Merchant|Trade")
    void CancelTrade();

    UFUNCTION(BlueprintPure, Category = "Merchant|Trade")
    bool IsTradeActive() const { return bTradeActive; }

    // ========== TRANSACTION HISTORY ==========

    UFUNCTION(BlueprintPure, Category = "Merchant|History")
    TArray<FTransactionRecord> GetTransactionHistory() const { return TransactionHistory; }

    UFUNCTION(BlueprintCallable, Category = "Merchant|History")
    void ClearTransactionHistory();

    // ========== SHOP CREATION ==========

    UFUNCTION(BlueprintCallable, Category = "Merchant|Creation")
    void RegisterShop(const FShop& Shop);

    UFUNCTION(BlueprintCallable, Category = "Merchant|Creation")
    void UnregisterShop(const FString& ShopID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnShopOpened, FString, ShopID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnShopClosed);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnItemPurchased, FString, ItemID, int32, Quantity, int32, Price);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnItemSold, FString, ItemID, int32, Quantity, int32, Price);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnTradeCompleted);

    UPROPERTY(BlueprintAssignable, Category = "Merchant|Events")
    FOnShopOpened OnShopOpened;

    UPROPERTY(BlueprintAssignable, Category = "Merchant|Events")
    FOnShopClosed OnShopClosed;

    UPROPERTY(BlueprintAssignable, Category = "Merchant|Events")
    FOnItemPurchased OnItemPurchased;

    UPROPERTY(BlueprintAssignable, Category = "Merchant|Events")
    FOnItemSold OnItemSold;

    UPROPERTY(BlueprintAssignable, Category = "Merchant|Events")
    FOnTradeCompleted OnTradeCompleted;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Merchant|Config")
    TMap<FString, FShop> Shops;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Merchant|Config")
    float GlobalRestockInterval = 86400.0f;  // 24 hours

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Merchant|Config")
    float ReputationDiscountPerLevel = 0.01f;  // 1% per reputation level

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Merchant|Config")
    float MaxReputationDiscount = 0.25f;  // Max 25% discount

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Merchant|Config")
    bool bStolenGoodsMarkup = true;  // Fences charge more

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Merchant|Config")
    float StolenGoodsMarkup = 1.5f;  // 50% more expensive at fence

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    bool bShopOpen = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    FString CurrentShopID;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    APlayerController* CurrentCustomer = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    bool bTradeActive = false;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    APlayerController* TradePlayer1 = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    APlayerController* TradePlayer2 = nullptr;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    FTradeOffer TradeOffer1;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    FTradeOffer TradeOffer2;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Merchant|State")
    TArray<FTransactionRecord> TransactionHistory;

private:
    // ========== HELPER FUNCTIONS ==========

    void AddTransactionRecord(ETransactionType Type, const FString& ItemID, int32 Quantity, int32 Price, const FString& ShopID);
    void UpdateShopStock(const FString& ShopID, const FString& ItemID, int32 Delta);
    void UpdateMerchantGold(const FString& ShopID, int32 Delta);
    bool CheckItemRequirements(const FShopItem& ShopItem, APlayerController* Customer) const;
    void ExecuteTrade();
};
