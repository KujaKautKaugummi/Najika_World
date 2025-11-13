// AuctionHouseSystem.cpp - From Batch 5 headers
#include "AuctionHouseSystem.h"
UAuctionHouseSystem::UAuctionHouseSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UAuctionHouseSystem::BeginPlay() { Super::BeginPlay(); }
bool UAuctionHouseSystem::CreateAuction(const FString& ItemID, int32 StartingBid, int32 BuyoutPrice, float Duration) {
    FAuction NewAuction;
    NewAuction.AuctionID = FGuid::NewGuid().ToString();
    NewAuction.ItemID = ItemID;
    NewAuction.StartingBid = StartingBid;
    NewAuction.CurrentBid = StartingBid;
    NewAuction.BuyoutPrice = BuyoutPrice;
    NewAuction.TimeRemaining = Duration;
    NewAuction.Status = EAuctionStatus::AS_Active;
    ActiveAuctions.Add(NewAuction);
    OnAuctionCreated.Broadcast(NewAuction);
    return true;
}
bool UAuctionHouseSystem::PlaceBid(const FString& AuctionID, int32 BidAmount) {
    for (FAuction& Auction : ActiveAuctions) {
        if (Auction.AuctionID == AuctionID && BidAmount > Auction.CurrentBid) {
            FBid NewBid;
            NewBid.BidderID = "Player";
            NewBid.BidAmount = BidAmount;
            NewBid.Timestamp = FDateTime::Now();
            Auction.BidHistory.Add(NewBid);
            Auction.CurrentBid = BidAmount;
            OnBidPlaced.Broadcast(AuctionID, BidAmount);
            return true;
        }
    }
    return false;
}
bool UAuctionHouseSystem::Buyout(const FString& AuctionID) {
    for (FAuction& Auction : ActiveAuctions) {
        if (Auction.AuctionID == AuctionID) {
            Auction.Status = EAuctionStatus::AS_Sold;
            OnItemPurchased.Broadcast(AuctionID, Auction.BuyoutPrice);
            return true;
        }
    }
    return false;
}
