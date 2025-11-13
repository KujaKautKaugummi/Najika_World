// BankSystem.h
// Complete Bank/Storage System with multiple tabs, sorting, account types

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "BankSystem.generated.h"

// Bank Account Type
UENUM(BlueprintType)
enum class EBankAccountType : uint8
{
    BA_Personal UMETA(DisplayName = "Personal"),
    BA_Shared UMETA(DisplayName = "Shared (Account-Wide)"),
    BA_Guild UMETA(DisplayName = "Guild Bank")
};

// Storage Tab
USTRUCT(BlueprintType)
struct FStorageTab
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TabID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString TabName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 SlotCount = 50;

    UPROPERTY(BlueprintReadWrite)
    TMap<int32, FString> StoredItems;  // SlotIndex -> ItemInstanceID

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    bool bIsLocked = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 UnlockCost = 0;  // Gold cost to unlock

    int32 GetUsedSlots() const { return StoredItems.Num(); }
    int32 GetFreeSlots() const { return SlotCount - GetUsedSlots(); }
    bool IsFull() const { return GetFreeSlots() <= 0; }
};

// Bank Account
USTRUCT(BlueprintType)
struct FBankAccount
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString AccountID;

    UPROPERTY(BlueprintReadWrite)
    FString OwnerPlayerID;  // Or Guild ID for guild banks

    UPROPERTY(BlueprintReadWrite)
    EBankAccountType Type;

    UPROPERTY(BlueprintReadWrite)
    TArray<FStorageTab> Tabs;

    UPROPERTY(BlueprintReadWrite)
    int32 StoredGold = 0;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> AuthorizedPlayerIDs;  // Who can access

    UPROPERTY(BlueprintReadWrite)
    FDateTime LastAccessed;

    int32 GetTotalSlots() const;
    int32 GetUsedSlots() const;
};

// Bank Transaction
USTRUCT(BlueprintType)
struct FBankTransaction
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString ItemID;

    UPROPERTY(BlueprintReadWrite)
    int32 Quantity;

    UPROPERTY(BlueprintReadWrite)
    bool bDeposit;  // true = deposit, false = withdraw

    UPROPERTY(BlueprintReadWrite)
    FDateTime Timestamp;
};

UCLASS()
class NAJIKATEST_API ABankSystem : public AActor
{
    GENERATED_BODY()

public:
    ABankSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== ACCOUNT MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Bank|Account")
    FString CreateAccount(const FString& OwnerPlayerID, EBankAccountType Type);

    UFUNCTION(BlueprintCallable, Category = "Bank|Account")
    void DeleteAccount(const FString& AccountID);

    UFUNCTION(BlueprintPure, Category = "Bank|Account")
    FBankAccount GetAccount(const FString& AccountID) const;

    UFUNCTION(BlueprintPure, Category = "Bank|Account")
    FString GetPlayerAccount(const FString& PlayerID, EBankAccountType Type) const;

    UFUNCTION(BlueprintPure, Category = "Bank|Account")
    bool HasAccess(const FString& AccountID, const FString& PlayerID) const;

    // ========== DEPOSIT/WITHDRAW ==========

    UFUNCTION(BlueprintCallable, Category = "Bank|Items")
    bool DepositItem(const FString& AccountID, const FString& PlayerID, const FString& ItemID, int32 Quantity, const FString& TabID = "");

    UFUNCTION(BlueprintCallable, Category = "Bank|Items")
    bool WithdrawItem(const FString& AccountID, const FString& PlayerID, const FString& ItemID, int32 Quantity);

    UFUNCTION(BlueprintCallable, Category = "Bank|Items")
    bool MoveItem(const FString& AccountID, int32 FromSlot, int32 ToSlot, const FString& FromTabID, const FString& ToTabID);

    UFUNCTION(BlueprintPure, Category = "Bank|Items")
    int32 GetItemCount(const FString& AccountID, const FString& ItemID) const;

    // ========== GOLD ==========

    UFUNCTION(BlueprintCallable, Category = "Bank|Gold")
    bool DepositGold(const FString& AccountID, const FString& PlayerID, int32 Amount);

    UFUNCTION(BlueprintCallable, Category = "Bank|Gold")
    bool WithdrawGold(const FString& AccountID, const FString& PlayerID, int32 Amount);

    UFUNCTION(BlueprintPure, Category = "Bank|Gold")
    int32 GetStoredGold(const FString& AccountID) const;

    // ========== TABS ==========

    UFUNCTION(BlueprintCallable, Category = "Bank|Tabs")
    void AddTab(const FString& AccountID, const FString& TabName, int32 SlotCount);

    UFUNCTION(BlueprintCallable, Category = "Bank|Tabs")
    void RemoveTab(const FString& AccountID, const FString& TabID);

    UFUNCTION(BlueprintCallable, Category = "Bank|Tabs")
    void UnlockTab(const FString& AccountID, const FString& TabID, const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "Bank|Tabs")
    void RenameTab(const FString& AccountID, const FString& TabID, const FString& NewName);

    UFUNCTION(BlueprintPure, Category = "Bank|Tabs")
    TArray<FStorageTab> GetTabs(const FString& AccountID) const;

    // ========== CAPACITY ==========

    UFUNCTION(BlueprintCallable, Category = "Bank|Capacity")
    void UpgradeCapacity(const FString& AccountID, const FString& TabID, int32 AdditionalSlots);

    UFUNCTION(BlueprintPure, Category = "Bank|Capacity")
    int32 GetTotalCapacity(const FString& AccountID) const;

    UFUNCTION(BlueprintPure, Category = "Bank|Capacity")
    int32 GetUsedCapacity(const FString& AccountID) const;

    UFUNCTION(BlueprintPure, Category = "Bank|Capacity")
    int32 GetFreeCapacity(const FString& AccountID) const;

    // ========== SORTING ==========

    UFUNCTION(BlueprintCallable, Category = "Bank|Sorting")
    void SortTab(const FString& AccountID, const FString& TabID, const FString& SortMethod);

    UFUNCTION(BlueprintCallable, Category = "Bank|Sorting")
    void CompactTab(const FString& AccountID, const FString& TabID);  // Remove gaps

    // ========== SEARCH ==========

    UFUNCTION(BlueprintPure, Category = "Bank|Search")
    TArray<FString> SearchItems(const FString& AccountID, const FString& SearchTerm) const;

    UFUNCTION(BlueprintPure, Category = "Bank|Search")
    TMap<FString, int32> GetAllStoredItems(const FString& AccountID) const;  // ItemID -> Total Quantity

    // ========== PERMISSIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Bank|Permissions")
    void GrantAccess(const FString& AccountID, const FString& TargetPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Bank|Permissions")
    void RevokeAccess(const FString& AccountID, const FString& TargetPlayerID);

    // ========== TRANSACTION HISTORY ==========

    UFUNCTION(BlueprintPure, Category = "Bank|History")
    TArray<FBankTransaction> GetTransactionHistory(const FString& AccountID) const;

    UFUNCTION(BlueprintCallable, Category = "Bank|History")
    void ClearTransactionHistory(const FString& AccountID);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnItemDeposited, FString, AccountID, FString, ItemID, int32, Quantity);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnItemWithdrawn, FString, AccountID, FString, ItemID, int32, Quantity);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnTabUnlocked, FString, AccountID, FString, TabID);

    UPROPERTY(BlueprintAssignable, Category = "Bank|Events")
    FOnItemDeposited OnItemDeposited;

    UPROPERTY(BlueprintAssignable, Category = "Bank|Events")
    FOnItemWithdrawn OnItemWithdrawn;

    UPROPERTY(BlueprintAssignable, Category = "Bank|Events")
    FOnTabUnlocked OnTabUnlocked;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Bank|Config")
    int32 DefaultTabCount = 3;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Bank|Config")
    int32 DefaultSlotsPerTab = 50;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Bank|Config")
    int32 MaxTabs = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Bank|Config")
    int32 TabUnlockCost = 5000;  // Gold per tab

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Bank|Config")
    int32 SlotUpgradeCost = 100;  // Gold per slot

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Bank|Config")
    int32 MaxTransactionHistory = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Bank|Config")
    bool bSharedBankEnabled = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Bank|State")
    TMap<FString, FBankAccount> Accounts;  // AccountID -> Account

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Bank|State")
    TMap<FString, TArray<FBankTransaction>> TransactionHistory;  // AccountID -> Transactions

private:
    // ========== HELPER FUNCTIONS ==========

    FString GenerateAccountID() const;
    int32 FindFreeSlot(FStorageTab& Tab) const;
    void LogTransaction(const FString& AccountID, const FBankTransaction& Transaction);
    void StackItems(FStorageTab& Tab, const FString& ItemID);
};
