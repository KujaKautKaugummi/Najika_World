// PartySystem.h
// Complete Party/Group System for Co-op Multiplayer
// Supports: Party formation, XP/Loot sharing, Leader abilities, Party buffs

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PartySystem.generated.h"

// Party Role
UENUM(BlueprintType)
enum class EPartyRole : uint8
{
    PR_Leader UMETA(DisplayName = "Leader"),
    PR_Member UMETA(DisplayName = "Member"),
    PR_Invited UMETA(DisplayName = "Invited (Pending)")
};

// Loot Distribution Mode
UENUM(BlueprintType)
enum class ELootDistribution : uint8
{
    LD_FreeForAll UMETA(DisplayName = "Free for All"),
    LD_RoundRobin UMETA(DisplayName = "Round Robin"),
    LD_NeedBeforeGreed UMETA(DisplayName = "Need Before Greed"),
    LD_MasterLoot UMETA(DisplayName = "Master Looter"),
    LD_Personal UMETA(DisplayName = "Personal Loot")
};

// XP Distribution Mode
UENUM(BlueprintType)
enum class EXPDistribution : uint8
{
    XD_Equal UMETA(DisplayName = "Equal Split"),
    XD_ByLevel UMETA(DisplayName = "By Level (Higher = More)"),
    XD_ByDamage UMETA(DisplayName = "By Damage Contribution"),
    XD_ByProximity UMETA(DisplayName = "Nearby Members Only")
};

// Party Member Data
USTRUCT(BlueprintType)
struct FPartyMember
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString PlayerName;

    UPROPERTY(BlueprintReadWrite)
    EPartyRole Role;

    UPROPERTY(BlueprintReadWrite)
    int32 Level;

    UPROPERTY(BlueprintReadWrite)
    float CurrentHealth;

    UPROPERTY(BlueprintReadWrite)
    float MaxHealth;

    UPROPERTY(BlueprintReadWrite)
    float CurrentMana;

    UPROPERTY(BlueprintReadWrite)
    float MaxMana;

    UPROPERTY(BlueprintReadWrite)
    FVector Location;

    UPROPERTY(BlueprintReadWrite)
    bool bIsOnline = true;

    UPROPERTY(BlueprintReadWrite)
    bool bIsReady = false;

    UPROPERTY(BlueprintReadWrite)
    FDateTime JoinTime;

    bool IsLeader() const { return Role == EPartyRole::PR_Leader; }
    bool IsInvited() const { return Role == EPartyRole::PR_Invited; }
    float GetHealthPercent() const { return MaxHealth > 0.0f ? CurrentHealth / MaxHealth : 0.0f; }
    float GetManaPercent() const { return MaxMana > 0.0f ? CurrentMana / MaxMana : 0.0f; }
};

// Party Buff
USTRUCT(BlueprintType)
struct FPartyBuff
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BuffID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString BuffName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 RequiredMembers = 2;  // Minimum party size to activate

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TMap<FString, float> StatBonuses;  // "Damage": 1.1 (10% bonus)

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float XPBonus = 0.0f;  // Additional XP multiplier

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float LootBonus = 0.0f;  // Additional loot quality

    bool IsActive(int32 PartySize) const { return PartySize >= RequiredMembers; }
};

// Party Invitation
USTRUCT(BlueprintType)
struct FPartyInvitation
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString FromPlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString FromPlayerName;

    UPROPERTY(BlueprintReadWrite)
    FString ToPlayerID;

    UPROPERTY(BlueprintReadWrite)
    FString PartyID;

    UPROPERTY(BlueprintReadWrite)
    FDateTime InviteTime;

    UPROPERTY(BlueprintReadWrite)
    float ExpiryTime = 60.0f;  // 60 seconds to accept

    bool IsExpired() const
    {
        FTimespan Elapsed = FDateTime::Now() - InviteTime;
        return Elapsed.GetTotalSeconds() > ExpiryTime;
    }
};

// Party Data
USTRUCT(BlueprintType)
struct FParty
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString PartyID;

    UPROPERTY(BlueprintReadWrite)
    TArray<FPartyMember> Members;

    UPROPERTY(BlueprintReadWrite)
    int32 MaxMembers = 5;

    UPROPERTY(BlueprintReadWrite)
    ELootDistribution LootMode = ELootDistribution::LD_RoundRobin;

    UPROPERTY(BlueprintReadWrite)
    EXPDistribution XPMode = EXPDistribution::XD_Equal;

    UPROPERTY(BlueprintReadWrite)
    int32 LootRoundRobinIndex = 0;

    UPROPERTY(BlueprintReadWrite)
    bool bAllowJoinRequests = true;

    UPROPERTY(BlueprintReadWrite)
    bool bShareQuests = true;

    UPROPERTY(BlueprintReadWrite)
    FDateTime CreationTime;

    int32 GetMemberCount() const { return Members.Num(); }
    bool IsFull() const { return Members.Num() >= MaxMembers; }
    FPartyMember* GetLeader();
    bool HasMember(const FString& PlayerID) const;
};

UCLASS()
class NAJIKATEST_API APartySystem : public AActor
{
    GENERATED_BODY()

public:
    APartySystem();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== PARTY MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Party|Management")
    FString CreateParty(const FString& LeaderPlayerID);

    UFUNCTION(BlueprintCallable, Category = "Party|Management")
    void DisbandParty(const FString& PartyID);

    UFUNCTION(BlueprintCallable, Category = "Party|Management")
    bool LeaveParty(const FString& PlayerID);

    UFUNCTION(BlueprintPure, Category = "Party|Management")
    FParty GetParty(const FString& PartyID) const;

    UFUNCTION(BlueprintPure, Category = "Party|Management")
    FString GetPlayerParty(const FString& PlayerID) const;

    UFUNCTION(BlueprintPure, Category = "Party|Management")
    bool IsInParty(const FString& PlayerID) const;

    // ========== INVITATIONS ==========

    UFUNCTION(BlueprintCallable, Category = "Party|Invite")
    void InvitePlayer(const FString& PartyID, const FString& InviterID, const FString& InviteeID);

    UFUNCTION(BlueprintCallable, Category = "Party|Invite")
    void AcceptInvite(const FString& PlayerID, const FString& PartyID);

    UFUNCTION(BlueprintCallable, Category = "Party|Invite")
    void DeclineInvite(const FString& PlayerID, const FString& PartyID);

    UFUNCTION(BlueprintPure, Category = "Party|Invite")
    TArray<FPartyInvitation> GetPendingInvites(const FString& PlayerID) const;

    // ========== MEMBER MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "Party|Members")
    void KickMember(const FString& PartyID, const FString& LeaderID, const FString& TargetID);

    UFUNCTION(BlueprintCallable, Category = "Party|Members")
    void PromoteToLeader(const FString& PartyID, const FString& CurrentLeaderID, const FString& NewLeaderID);

    UFUNCTION(BlueprintCallable, Category = "Party|Members")
    void SetMemberReady(const FString& PlayerID, bool bReady);

    UFUNCTION(BlueprintPure, Category = "Party|Members")
    TArray<FPartyMember> GetPartyMembers(const FString& PartyID) const;

    UFUNCTION(BlueprintPure, Category = "Party|Members")
    bool AreAllMembersReady(const FString& PartyID) const;

    // ========== LOOT DISTRIBUTION ==========

    UFUNCTION(BlueprintCallable, Category = "Party|Loot")
    void SetLootMode(const FString& PartyID, ELootDistribution Mode);

    UFUNCTION(BlueprintCallable, Category = "Party|Loot")
    FString GetLootRecipient(const FString& PartyID, const FString& ItemID);

    UFUNCTION(BlueprintCallable, Category = "Party|Loot")
    void DistributeLoot(const FString& PartyID, const TArray<FString>& ItemIDs);

    // ========== XP DISTRIBUTION ==========

    UFUNCTION(BlueprintCallable, Category = "Party|XP")
    void SetXPMode(const FString& PartyID, EXPDistribution Mode);

    UFUNCTION(BlueprintCallable, Category = "Party|XP")
    void DistributeXP(const FString& PartyID, int32 TotalXP, const FVector& KillLocation);

    UFUNCTION(BlueprintPure, Category = "Party|XP")
    int32 CalculateMemberXPShare(const FString& PartyID, const FString& PlayerID, int32 TotalXP) const;

    // ========== PARTY BUFFS ==========

    UFUNCTION(BlueprintPure, Category = "Party|Buffs")
    TArray<FPartyBuff> GetActivePartyBuffs(const FString& PartyID) const;

    UFUNCTION(BlueprintPure, Category = "Party|Buffs")
    float GetPartyXPBonus(const FString& PartyID) const;

    UFUNCTION(BlueprintPure, Category = "Party|Buffs")
    float GetPartyLootBonus(const FString& PartyID) const;

    // ========== PROXIMITY CHECKS ==========

    UFUNCTION(BlueprintPure, Category = "Party|Proximity")
    TArray<FPartyMember> GetNearbyMembers(const FString& PartyID, const FVector& Location, float Radius) const;

    UFUNCTION(BlueprintPure, Category = "Party|Proximity")
    bool IsPartyNearby(const FString& PartyID, const FVector& Location, float Radius) const;

    // ========== MEMBER STATE UPDATES ==========

    UFUNCTION(BlueprintCallable, Category = "Party|State")
    void UpdateMemberState(const FString& PlayerID, float CurrentHP, float MaxHP, float CurrentMP, float MaxMP, const FVector& Location);

    // ========== EVENTS ==========

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPartyCreated, FString, PartyID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnPartyDisbanded, FString, PartyID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMemberJoined, FString, PartyID, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMemberLeft, FString, PartyID, FString, PlayerID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnInviteReceived, FString, FromPlayerID, FString, ToPlayerID, FString, PartyID);
    DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnLeaderChanged, FString, PartyID, FString, NewLeaderID);

    UPROPERTY(BlueprintAssignable, Category = "Party|Events")
    FOnPartyCreated OnPartyCreated;

    UPROPERTY(BlueprintAssignable, Category = "Party|Events")
    FOnPartyDisbanded OnPartyDisbanded;

    UPROPERTY(BlueprintAssignable, Category = "Party|Events")
    FOnMemberJoined OnMemberJoined;

    UPROPERTY(BlueprintAssignable, Category = "Party|Events")
    FOnMemberLeft OnMemberLeft;

    UPROPERTY(BlueprintAssignable, Category = "Party|Events")
    FOnInviteReceived OnInviteReceived;

    UPROPERTY(BlueprintAssignable, Category = "Party|Events")
    FOnLeaderChanged OnLeaderChanged;

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Party|Config")
    int32 DefaultMaxMembers = 5;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Party|Config")
    float XPProximityRadius = 5000.0f;  // 50 meters

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Party|Config")
    float PartyXPBonus = 0.1f;  // 10% bonus XP in party

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Party|Config")
    float InviteExpiryTime = 60.0f;  // 60 seconds

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Party|Config")
    TArray<FPartyBuff> PartyBuffs;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Party|State")
    TMap<FString, FParty> Parties;  // PartyID -> Party

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Party|State")
    TMap<FString, FString> PlayerToParty;  // PlayerID -> PartyID

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Party|State")
    TArray<FPartyInvitation> PendingInvites;

private:
    // ========== HELPER FUNCTIONS ==========

    void AddMemberToParty(const FString& PartyID, const FPartyMember& Member);
    void RemoveMemberFromParty(const FString& PartyID, const FString& PlayerID);
    void CleanupExpiredInvites();
    FString GeneratePartyID() const;
    void NotifyPartyMembersStateUpdate(const FString& PartyID, const FString& PlayerID);
};
