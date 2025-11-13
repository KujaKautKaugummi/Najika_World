// GuildSystem.h
// Complete Guild/Clan System with ranks, permissions, bank, activities

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GuildSystem.generated.h"

// Guild Rank
UENUM(BlueprintType)
enum class EGuildRank : uint8
{
    GR_GuildMaster UMETA(DisplayName = "Guild Master"),
    GR_Officer UMETA(DisplayName = "Officer"),
    GR_Veteran UMETA(DisplayName = "Veteran"),
    GR_Member UMETA(DisplayName = "Member"),
    GR_Recruit UMETA(DisplayName = "Recruit")
};

// Guild Permission
UENUM(BlueprintType)
enum class EGuildPermission : uint8
{
    GP_Invite UMETA(DisplayName = "Invite Members"),
    GP_Kick UMETA(DisplayName = "Kick Members"),
    GP_Promote UMETA(DisplayName = "Promote Members"),
    GP_Demote UMETA(DisplayName = "Demote Members"),
    GP_EditMOTD UMETA(DisplayName = "Edit MOTD"),
    GP_UseBank UMETA(DisplayName = "Use Guild Bank"),
    GP_WithdrawBank UMETA(DisplayName = "Withdraw from Bank"),
    GP_ManageRanks UMETA(DisplayName = "Manage Ranks"),
    GP_DeclareWar UMETA(DisplayName = "Declare War"),
    GP_ManageAlliances UMETA(DisplayName = "Manage Alliances")
};

// Guild Member Data
USTRUCT(BlueprintType)
struct FGuildMember
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString PlayerName;

    UPROPERTY(BlueprintReadWrite)
    EGuildRank Rank = EGuildRank::GR_Recruit;

    UPROPERTY(BlueprintReadWrite)
    int32 ContributionPoints = 0;

    UPROPERTY(BlueprintReadWrite)
    FDateTime JoinDate;

    UPROPERTY(BlueprintReadWrite)
    FDateTime LastOnline;

    UPROPERTY(BlueprintReadWrite)
    bool bIsOnline = false;

    UPROPERTY(BlueprintReadWrite)
    FString PersonalNote;
};

// Guild Data
USTRUCT(BlueprintType)
struct FGuild
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString GuildID;

    UPROPERTY(BlueprintReadWrite)
    FString GuildName;

    UPROPERTY(BlueprintReadWrite)
    FString GuildTag;  // [TAG]

    UPROPERTY(BlueprintReadWrite)
    FString MOTD;  // Message of the Day

    UPROPERTY(BlueprintReadWrite)
    FString Description;

    UPROPERTY(BlueprintReadWrite)
    UTexture2D* Emblem = nullptr;

    UPROPERTY(BlueprintReadWrite)
    TArray<FGuildMember> Members;

    UPROPERTY(BlueprintReadWrite)
    int32 MaxMembers = 50;

    UPROPERTY(BlueprintReadWrite)
    int32 Level = 1;

    UPROPERTY(BlueprintReadWrite)
    int32 Experience = 0;

    UPROPERTY(BlueprintReadWrite)
    int32 BankGold = 0;

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, int32> BankItems;  // ItemID -> Quantity

    UPROPERTY(BlueprintReadWrite)
    TMap<EGuildRank, TArray<EGuildPermission>> RankPermissions;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> AllyGuildIDs;

    UPROPERTY(BlueprintReadWrite)
    TArray<FString> EnemyGuildIDs;

    UPROPERTY(BlueprintReadWrite)
    FDateTime CreatedDate;

    int32 GetMemberCount() const { return Members.Num(); }
    bool IsFull() const { return Members.Num() >= MaxMembers; }
    FGuildMember* GetMember(const FString& PlayerID);
    FGuildMember* GetGuildMaster();
};

UCLASS()
class NAJIKATEST_API AGuildSystem : public AActor
{
    GENERATED_BODY()

public:
    AGuildSystem();

protected:
    virtual void BeginPlay() override;

public:
    // ========== GUILD CREATION ==========

    UFUNCTION(BlueprintCallable, Category = "Guild|Management")
    FString CreateGuild(const FString& GuildName, const FString& GuildTag, const FString& FounderPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Guild|Management")
    void DisbandGuild(const FString& GuildID, const FString& GuildMasterID);

    UFUNCTION(BlueprintPure, Category = "Guild|Management")
    bool DoesGuildExist(const FString& GuildID) const;

    UFUNCTION(BlueprintPure, Category = "Guild|Management")
    bool IsGuildNameTaken(const FString& GuildName) const;

    // ========== MEMBERSHIP ==========

    UFUNCTION(BlueprintCallable, Category = "Guild|Membership")
    void InvitePlayer(const FString& GuildID, const FString& InviterID, const FString& InviteeID);

    UFUNCTION(BlueprintCallable, Category = "Guild|Membership")
    void AcceptInvite(const FString& PlayerID, const FString& GuildID);

    UFUNCTION(BlueprintCallable, Category = "Guild|Membership")
    void DeclineInvite(const FString& PlayerID, const FString& GuildID);

    UFUNCTION(BlueprintCallable, Category = "Guild|Membership")
    void LeaveGuild(const FString& PlayerID);

    UFUNCTION(BlueprintCallable, Category = "Guild|Membership")
    void KickMember(const FString& GuildID, const FString& KickerID, const FString& TargetID);

    UFUNCTION(BlueprintPure, Category = "Guild|Membership")
    FString GetPlayerGuild(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Guild|Membership")
    bool IsInGuild(const FString& PlayerID) const;

    // ========== RANKS & PERMISSIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Guild|Ranks")
    void PromoteMember(const FString& GuildID, const FString& PromoterID, const FString& TargetID);

    UFUNCTION(BlueprintCallable, Category = "Guild|Ranks")
    void DemoteMember(const FString& GuildID, const FString& DemoterID, const FString& TargetID);

    UFUNCTION(BlueprintCallable, Category = "Guild|Ranks")
    void TransferLeadership(const FString& GuildID, const FString& CurrentLeaderID, const FString& NewLeaderID);

    UFUNCTION(BlueprintPure, Category = "Guild|Ranks")
    bool HasPermission(const FString& GuildID, const FString& PlayerID, EGuildPermission Permission) const;

    // ========== GUILD INFO ==========

    UFUNCTION(BlueprintPure, Category = "Guild|Info")
    FGuild GetGuild(const FString& GuildID) const;

    UFUNCTION(BlueprintPure, Category = "Guild|Info")
    TArray<FGuildMember> GetGuildMembers(const FString& GuildID) const;

    UFUNCTION(BlueprintPure, Category = "Guild|Info")
    FString GetGuildMOTD(const FString& GuildID) const;

    UFUNCTION(BlueprintCallable, Category = "Guild|Info")
    void SetGuildMOTD(const FString& GuildID, const FString& PlayerID, const FString& NewMOTD);

    // ========== GUILD BANK ==========

    UFUNCTION(BlueprintCallable, Category = "Guild|Bank")
    void DepositGold(const FString& GuildID, const FString& PlayerID, int32 Amount);

    UFUNCTION(BlueprintCallable, Category = "Guild|Bank")
    void WithdrawGold(const FString& GuildID, const FString& PlayerID, int32 Amount);

    UFUNCTION(BlueprintCallable, Category = "Guild|Bank")
    void DepositItem(const FString& GuildID, const FString& PlayerID, const FString& ItemID, int32 Quantity);

    UFUNCTION(BlueprintCallable, Category = "Guild|Bank")
    void WithdrawItem(const FString& GuildID, const FString& PlayerID, const FString& ItemID, int32 Quantity);

    UFUNCTION(BlueprintPure, Category = "Guild|Bank")
    int32 GetBankGold(const FString& GuildID) const;

    // ========== PROGRESSION ==========

    UFUNCTION(BlueprintCallable, Category = "Guild|Progression")
    void AddGuildXP(const FString& GuildID, int32 XP);

    UFUNCTION(BlueprintCallable, Category = "Guild|Progression")
    void AddContribution(const FString& GuildID, const FString& PlayerID, int32 Points);

    UFUNCTION(BlueprintPure, Category = "Guild|Progression")
    int32 GetGuildLevel(const FString& GuildID) const;

    UFUNCTION(BlueprintPure, Category = "Guild|Progression")
    int32 GetMemberContribution(const FString& GuildID, const FString& PlayerID) const;

    // ========== RELATIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Guild|Relations")
    void ProposeAlliance(const FString& GuildID1, const FString& GuildID2);

    UFUNCTION(BlueprintCallable, Category = "Guild|Relations")
    void AcceptAlliance(const FString& GuildID1, const FString& GuildID2);

    UFUNCTION(BlueprintCallable, Category = "Guild|Relations")
    void BreakAlliance(const FString& GuildID1, const FString& GuildID2);

    UFUNCTION(BlueprintCallable, Category = "Guild|Relations")
    void DeclareWar(const FString& GuildID1, const FString& GuildID2);

    UFUNCTION(BlueprintPure, Category = "Guild|Relations")
    bool AreAllied(const FString& GuildID1, const FString& GuildID2) const;

    UFUNCTION(BlueprintPure, Category = "Guild|Relations")
    bool AreAtWar(const FString& GuildID1, const FString& GuildID2) const;

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnGuildCreated, FString, GuildID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnGuildDisbanded, FString, GuildID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMemberJoined, FString, GuildID, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMemberLeft, FString, GuildID, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnGuildLevelUp, FString, GuildID, int32, NewLevel);

    UPROPERTY(BlueprintAssignable, Category = "Guild|Events")
    FOnGuildCreated OnGuildCreated;

    UPROPERTY(BlueprintAssignable, Category = "Guild|Events")
    FOnGuildDisbanded OnGuildDisbanded;

    UPROPERTY(BlueprintAssignable, Category = "Guild|Events")
    FOnMemberJoined OnMemberJoined;

    UPROPERTY(BlueprintAssignable, Category = "Guild|Events")
    FOnMemberLeft OnMemberLeft;

    UPROPERTY(BlueprintAssignable, Category = "Guild|Events")
    FOnGuildLevelUp OnGuildLevelUp;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Guild|Config")
    int32 CreationCost = 10000;  // Gold cost to create guild

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Guild|Config")
    int32 DefaultMaxMembers = 50;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Guild|Config")
    int32 XPPerLevel = 1000;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Guild|Config")
    int32 MaxGuildLevel = 10;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Guild|State")
    TMap<FString, FGuild> Guilds;  // GuildID -> Guild

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Guild|State")
    TMap<FString, FString> PlayerToGuild;  // PlayerID -> GuildID

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Guild|State")
    TMap<FString, TArray<FString>> PendingInvites;  // PlayerID -> GuildIDs

private:
    // ========== HELPER FUNCTIONS ==========

    FString GenerateGuildID() const;
    void InitializeDefaultPermissions(FGuild& Guild);
    void CheckGuildLevelUp(FGuild& Guild);
};
