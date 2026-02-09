// NajikaAPIClient.h
// Main HTTP Client for Najika Backend Communication

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Interfaces/IHttpRequest.h"
#include "NajikaAPIClient.generated.h"

// Delegates for async responses
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnChatResponse, const FString&, Response, const FString&, Mood);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNajikaStatusReceived, const FString&, StatusJson);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnBattleUpdate, const FString&, BattleState, bool, IsPlayerTurn);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnQuestUpdate, const FString&, QuestJson);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAPIError, const FString&, ErrorMessage);

/**
 * Main API Client for communicating with Najika Python Backend
 * Usage: Get from GameInstance subsystem
 */
UCLASS()
class NAJIKABACKEND_API UNajikaAPIClient : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // ============================================
    // CORE CHAT
    // ============================================

    /** Send chat message to Najika */
    UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
    void SendChatMessage(const FString& Message);

    /** Get chat history */
    UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
    void GetChatHistory();

    // ============================================
    // NAJIKA STATUS (Tamagotchi)
    // ============================================

    /** Get Najika's current status */
    UFUNCTION(BlueprintCallable, Category = "Najika|Status")
    void GetNajikaStatus();

    /** Feed Najika */
    UFUNCTION(BlueprintCallable, Category = "Najika|Care")
    void FeedNajika();

    /** Give Najika a drink */
    UFUNCTION(BlueprintCallable, Category = "Najika|Care")
    void GiveDrink();

    /** Wash Najika */
    UFUNCTION(BlueprintCallable, Category = "Najika|Care")
    void WashNajika();

    /** Put Najika to sleep */
    UFUNCTION(BlueprintCallable, Category = "Najika|Care")
    void SleepNajika();

    /** Praise Najika (increases bond) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Care")
    void PraiseNajika();

    // ============================================
    // BATTLE SYSTEM
    // ============================================

    /** Start a battle */
    UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
    void StartBattle(const FString& EnemyId);

    /** Get current battle status */
    UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
    void GetBattleStatus();

    /** Perform battle action */
    UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
    void BattleAction(const FString& ActionType, const FString& TargetId = "");

    /** Use skill in battle */
    UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
    void UseSkill(const FString& SkillId);

    // ============================================
    // QUEST SYSTEM
    // ============================================

    /** Get active quests */
    UFUNCTION(BlueprintCallable, Category = "Najika|Quests")
    void GetActiveQuests();

    /** Get available quests */
    UFUNCTION(BlueprintCallable, Category = "Najika|Quests")
    void GetAvailableQuests();

    /** Start a quest */
    UFUNCTION(BlueprintCallable, Category = "Najika|Quests")
    void StartQuest(const FString& QuestId);

    /** Complete a quest */
    UFUNCTION(BlueprintCallable, Category = "Najika|Quests")
    void CompleteQuest(const FString& QuestId);

    // ============================================
    // SHOP & ECONOMY
    // ============================================

    /** Get player gold */
    UFUNCTION(BlueprintCallable, Category = "Najika|Economy")
    void GetPlayerGold();

    /** Buy item from shop */
    UFUNCTION(BlueprintCallable, Category = "Najika|Economy")
    void BuyItem(const FString& ItemId, int32 Quantity = 1);

    // ============================================
    // EVENTS
    // ============================================

    UPROPERTY(BlueprintAssignable, Category = "Najika|Events")
    FOnChatResponse OnChatResponse;

    UPROPERTY(BlueprintAssignable, Category = "Najika|Events")
    FOnNajikaStatusReceived OnNajikaStatusReceived;

    UPROPERTY(BlueprintAssignable, Category = "Najika|Events")
    FOnBattleUpdate OnBattleUpdate;

    UPROPERTY(BlueprintAssignable, Category = "Najika|Events")
    FOnQuestUpdate OnQuestUpdate;

    UPROPERTY(BlueprintAssignable, Category = "Najika|Events")
    FOnAPIError OnAPIError;

    // ============================================
    // CONFIGURATION
    // ============================================

    /** Set backend URL (default: http://127.0.0.1:8000) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Config")
    void SetBackendURL(const FString& URL);

    /** Get current backend URL */
    UFUNCTION(BlueprintPure, Category = "Najika|Config")
    FString GetBackendURL() const { return BackendURL; }

    /** Check if backend is reachable */
    UFUNCTION(BlueprintCallable, Category = "Najika|Config")
    void CheckBackendConnection();

private:
    // Backend URL - ALWAYS localhost for security!
    FString BackendURL = TEXT("http://127.0.0.1:8000");

    // Player ID
    FString PlayerId = TEXT("player_1");

    // HTTP Request helpers
    void SendGETRequest(const FString& Endpoint, TFunction<void(FHttpResponsePtr)> OnSuccess);
    void SendPOSTRequest(const FString& Endpoint, const FString& JsonBody, TFunction<void(FHttpResponsePtr)> OnSuccess);

    void OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess, TFunction<void(FHttpResponsePtr)> OnSuccess);

    // Parse helpers
    TSharedPtr<FJsonObject> ParseJsonResponse(const FString& JsonString);
};
