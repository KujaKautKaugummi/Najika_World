// AuctionHouseSystem.h
// Vollständiges Auktionshaus-System mit Geboten, Sofortkauf, Gebühren

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AuctionHouseSystem.generated.h"

// Auktions-Status
UENUM(BlueprintType)
enum class EAuctionStatus : uint8
{
    AS_Active UMETA(DisplayName = "Aktiv"),
    AS_Sold UMETA(DisplayName = "Verkauft"),
    AS_Expired UMETA(DisplayName = "Abgelaufen"),
    AS_Cancelled UMETA(DisplayName = "Abgebrochen")
};

// Auktions-Dauer
UENUM(BlueprintType)
enum class EAuctionDuration : uint8
{
    AD_12Hours UMETA(DisplayName = "12 Stunden"),
    AD_24Hours UMETA(DisplayName = "24 Stunden"),
    AD_48Hours UMETA(DisplayName = "48 Stunden"),
    AD_7Days UMETA(DisplayName = "7 Tage")
};

// Gebot
USTRUCT(BlueprintType)
struct FBid
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString BidderID;

    UPROPERTY(BlueprintReadWrite)
    FString BidderName;

    UPROPERTY(BlueprintReadWrite)
    int32 BidAmount;

    UPROPERTY(BlueprintReadWrite)
    FDateTime BidTime;
};

// Auktion
USTRUCT(BlueprintType)
struct FAuction
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString AuctionID;

    UPROPERTY(BlueprintReadWrite)
    FString SellerID;

    UPROPERTY(BlueprintReadWrite)
    FString SellerName;

    UPROPERTY(BlueprintReadWrite)
    FString ItemID;

    UPROPERTY(BlueprintReadWrite)
    int32 Quantity = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 StartingBid;

    UPROPERTY(BlueprintReadWrite)
    int32 CurrentBid;

    UPROPERTY(BlueprintReadWrite)
    int32 BuyoutPrice = 0;  // 0 = kein Sofortkauf

    UPROPERTY(BlueprintReadWrite)
    TArray<FBid> BidHistory;

    UPROPERTY(BlueprintReadWrite)
    EAuctionStatus Status = EAuctionStatus::AS_Active;

    UPROPERTY(BlueprintReadWrite)
    FDateTime StartTime;

    UPROPERTY(BlueprintReadWrite)
    FDateTime EndTime;

    UPROPERTY(BlueprintReadWrite)
    EAuctionDuration Duration;

    UPROPERTY(BlueprintReadWrite)
    int32 ListingFee = 0;  // Einstellgebühr

    UPROPERTY(BlueprintReadWrite)
    int32 SalesTax = 0;  // Verkaufsgebühr (%)

    bool IsExpired() const { return FDateTime::Now() > EndTime; }
    bool HasBuyout() const { return BuyoutPrice > 0; }
    FString GetHighestBidder() const { return BidHistory.Num() > 0 ? BidHistory.Last().BidderID : ""; }
};

// Auktionshaus-Filter
USTRUCT(BlueprintType)
struct FAuctionFilter
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString SearchTerm;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Category;  // Waffe, Rüstung, etc.

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinLevel = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxLevel = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MinPrice = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MaxPrice = 999999;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bBuyoutOnly = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString Rarity;  // Common, Rare, etc.
};

UCLASS()
class NAJIKATEST_API AAuctionHouseSystem : public AActor
{
    GENERATED_BODY()

public:
    AAuctionHouseSystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== AUKTION ERSTELLEN ==========

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Create")
    FString CreateAuction(const FString& SellerID, const FString& ItemID, int32 Quantity, int32 StartingBid, int32 BuyoutPrice, EAuctionDuration Duration);

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Create")
    void CancelAuction(const FString& AuctionID, const FString& SellerID);

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Create")
    int32 CalculateListingFee(int32 StartingBid, EAuctionDuration Duration) const;

    // ========== BIETEN ==========

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Bidding")
    bool PlaceBid(const FString& AuctionID, const FString& BidderID, int32 BidAmount);

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Bidding")
    bool Buyout(const FString& AuctionID, const FString& BuyerID);

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Bidding")
    int32 GetMinimumBid(const FString& AuctionID) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Bidding")
    bool IsHighestBidder(const FString& AuctionID, const FString& PlayerID) const;

    // ========== SUCHEN & BROWSEN ==========

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Browse")
    TArray<FAuction> SearchAuctions(const FAuctionFilter& Filter) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Browse")
    TArray<FAuction> GetRecentAuctions(int32 Count = 20) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Browse")
    TArray<FAuction> GetEndingSoonAuctions(int32 Count = 20) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Browse")
    FAuction GetAuction(const FString& AuctionID) const;

    // ========== SPIELER-AUKTIONEN ==========

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Player")
    TArray<FAuction> GetPlayerAuctions(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Player")
    TArray<FAuction> GetPlayerBids(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Player")
    int32 GetActiveAuctionCount(const FString& PlayerID) const;

    // ========== ABSCHLUSS ==========

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Complete")
    void CompleteAuction(const FString& AuctionID);

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Complete")
    void ClaimItem(const FString& AuctionID, const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Complete")
    void ClaimGold(const FString& AuctionID, const FString& SellerID);

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Complete")
    void RefundBidders(const FString& AuctionID);

    // ========== STATISTIKEN ==========

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Stats")
    int32 GetAveragePrice(const FString& ItemID) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Stats")
    TArray<FAuction> GetRecentSales(const FString& ItemID, int32 Count = 10) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Stats")
    int32 GetTotalListings() const { return ActiveAuctions.Num(); }

    // ========== GEBÜHREN ==========

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Fees")
    int32 CalculateSalesTax(int32 SalePrice) const;

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Fees")
    int32 CalculateSellerProfit(int32 SalePrice) const;

    // ========== WATCHLIST ==========

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Watchlist")
    void AddToWatchlist(const FString& PlayerID, const FString& AuctionID);

    UFUNCTION(BlueprintCallable, Category = "AuctionHouse|Watchlist")
    void RemoveFromWatchlist(const FString& PlayerID, const FString& AuctionID);

    UFUNCTION(BlueprintPure, Category = "AuctionHouse|Watchlist")
    TArray<FAuction> GetWatchlist(const FString& PlayerID) const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAuctionCreated, FString, AuctionID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnNewBid, FString, AuctionID, int32, BidAmount);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAuctionSold, FString, AuctionID, FString, BuyerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAuctionExpired, FString, AuctionID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnOutbid, FString, PlayerID, FString, AuctionID);

    UPROPERTY(BlueprintAssignable, Category = "AuctionHouse|Events")
    FOnAuctionCreated OnAuctionCreated;

    UPROPERTY(BlueprintAssignable, Category = "AuctionHouse|Events")
    FOnNewBid OnNewBid;

    UPROPERTY(BlueprintAssignable, Category = "AuctionHouse|Events")
    FOnAuctionSold OnAuctionSold;

    UPROPERTY(BlueprintAssignable, Category = "AuctionHouse|Events")
    FOnAuctionExpired OnAuctionExpired;

    UPROPERTY(BlueprintAssignable, Category = "AuctionHouse|Events")
    FOnOutbid OnOutbid;

protected:
    // ========== KONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AuctionHouse|Config")
    float ListingFeePercent = 0.05f;  // 5% Einstellgebühr

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AuctionHouse|Config")
    float SalesTaxPercent = 0.10f;  // 10% Verkaufsgebühr

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AuctionHouse|Config")
    int32 MaxActiveAuctionsPerPlayer = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AuctionHouse|Config")
    int32 MinimumBidIncrement = 1;  // Mind. 1 Gold mehr bieten

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AuctionHouse|Config")
    float BidIncrementPercent = 0.05f;  // 5% mehr als aktuelles Gebot

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AuctionHouse|Config")
    bool bAllowBuyout = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AuctionHouse|Config")
    bool bRefundListingFeeOnCancel = false;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "AuctionHouse|State")
    TMap<FString, FAuction> ActiveAuctions;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "AuctionHouse|State")
    TArray<FAuction> CompletedAuctions;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "AuctionHouse|State")
    TMap<FString, TArray<FString>> PlayerWatchlists;  // PlayerID -> AuctionIDs

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "AuctionHouse|State")
    TMap<FString, TMap<FString, int32>> PendingClaims;  // PlayerID -> (AuctionID -> Gold/Items)

private:
    // ========== HELPER FUNCTIONS ==========

    void CheckExpiredAuctions();
    FString GenerateAuctionID() const;
    void NotifyOutbid(const FString& PlayerID, const FString& AuctionID);
    void TransferItem(const FAuction& Auction, const FString& ToPlayerID);
    void TransferGold(const FString& ToPlayerID, int32 Amount);
    float GetDurationHours(EAuctionDuration Duration) const;
};
