// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "NajikaBackendTypes.h"
#include "NajikaHttpClient.generated.h"

/**
 * HTTP Client for Najika Backend Communication
 * Handles all REST API endpoints documented in BACKEND_COMPLETE_API_REFERENCE.md
 *
 * Usage:
 *   UNajikaHttpClient* Client = NewObject<UNajikaHttpClient>();
 *   Client->Initialize("http://127.0.0.1:8000");
 *   Client->SendChatMessage("Hello Najika!", ResponseDelegate);
 */
UCLASS(BlueprintType)
class NAJIKABACKENDCLIENT_API UNajikaHttpClient : public UObject
{
	GENERATED_BODY()

public:
	UNajikaHttpClient();

	/**
	 * Initialize HTTP Client
	 * @param InBaseURL Base URL of backend (e.g. http://127.0.0.1:8000)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void Initialize(const FString& InBaseURL = TEXT("http://127.0.0.1:8000"));

	/**
	 * Get current base URL
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Backend")
	FString GetBaseURL() const { return BaseURL; }

	// ============================================================
	// CHAT & CONVERSATION
	// ============================================================

	/**
	 * Send Chat Message to Najika (POST /api/chat)
	 * @param Message User message
	 * @param OnResponse Callback delegate with response, Najika state, and living state
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void SendChatMessage(const FString& Message, FOnNajikaChatResponse OnResponse);

	/**
	 * Get Conversation History (GET /api/chat/history)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void GetChatHistory(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Get Bond Status (GET /api/bond/status)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void GetBondStatus(FOnNajikaHTTPResponse OnResponse);

	// ============================================================
	// NAJIKA CARE SYSTEM
	// ============================================================

	/**
	 * Get Najika Status (GET /api/najika/status)
	 * @param OnResponse Callback delegate with Najika state and living state
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void GetNajikaStatus(FOnNajikaStatusResponse OnResponse);

	/**
	 * Feed Najika (POST /api/najika/feed)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void FeedNajika(FOnNajikaActionResponse OnResponse);

	/**
	 * Give Najika Drink (POST /api/najika/drink)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void GiveDrink(FOnNajikaActionResponse OnResponse);

	/**
	 * Wash Najika (POST /api/najika/wash)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void WashNajika(FOnNajikaActionResponse OnResponse);

	/**
	 * Put Najika to Sleep (POST /api/najika/sleep)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void PutToSleep(FOnNajikaActionResponse OnResponse);

	/**
	 * Train Najika (POST /api/najika/train)
	 * @param TrainingType Type of training (strength, intelligence, dexterity, charisma)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void TrainNajika(const FString& TrainingType, FOnNajikaActionResponse OnResponse);

	/**
	 * Praise Najika (POST /api/najika/praise)
	 * Increases happiness, decreases discipline (Digimon World style)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void PraiseNajika(FOnNajikaActionResponse OnResponse);

	/**
	 * Scold Najika (POST /api/najika/scold)
	 * Increases discipline, decreases happiness
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void ScoldNajika(FOnNajikaActionResponse OnResponse);

	// ============================================================
	// EQUIPMENT SYSTEM
	// ============================================================

	/**
	 * Equip Item to Najika (POST /api/najika/equip)
	 * @param ItemID Item ID to equip
	 * @param Slot Equipment slot (weapon, armor, accessory)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Equipment")
	void EquipItem(const FString& ItemID, const FString& Slot, FOnNajikaActionResponse OnResponse);

	/**
	 * Unequip Item from Najika (POST /api/najika/unequip)
	 * @param Slot Equipment slot to unequip
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Equipment")
	void UnequipItem(const FString& Slot, FOnNajikaActionResponse OnResponse);

	/**
	 * Get Najika's Equipment (GET /api/najika/equipment)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Equipment")
	void GetEquipment(FOnNajikaHTTPResponse OnResponse);

	// ============================================================
	// BATTLE SYSTEM
	// ============================================================

	/**
	 * Start Battle (POST /api/battle/start)
	 * @param OnResponse Callback delegate with battle state and enemies
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void StartBattle(FOnBattleStartResponse OnResponse);

	/**
	 * Get Battle Status (GET /api/battle/status)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void GetBattleStatus(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Perform Battle Action (POST /api/battle/action)
	 * @param ActionType Action type (attack, skill, item, defend)
	 * @param Target Enemy index
	 * @param SkillID Skill ID (if action = skill)
	 * @param ItemID Item ID (if action = item)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void BattleAction(const FString& ActionType, int32 Target, const FString& SkillID, const FString& ItemID, FOnBattleActionResponse OnResponse);

	/**
	 * Get Battle Skills (GET /api/battle/skills)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void GetBattleSkills(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Reset Battle (POST /api/battle/reset)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Battle")
	void ResetBattle(FOnNajikaActionResponse OnResponse);

	// ============================================================
	// VOICE CALL SYSTEM
	// ============================================================

	/**
	 * Start Voice Call (POST /api/voice_call/start)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|VoiceCall")
	void StartVoiceCall(FOnNajikaActionResponse OnResponse);

	/**
	 * Send Audio for STT Processing (POST /api/voice_call/audio)
	 * @param AudioDataBase64 Base64-encoded audio data (WAV format)
	 * @param OnResponse Callback delegate with transcribed text, Najika response, and response audio
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|VoiceCall")
	void SendVoiceCallAudio(const FString& AudioDataBase64, FOnVoiceCallAudioResponse OnResponse);

	/**
	 * End Voice Call (POST /api/voice_call/end)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|VoiceCall")
	void EndVoiceCall(FOnNajikaActionResponse OnResponse);

	/**
	 * Get Voice Call Stats (GET /api/voice_call/stats)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|VoiceCall")
	void GetVoiceCallStats(FOnNajikaHTTPResponse OnResponse);

	// ============================================================
	// LIVING SYSTEM (AUTONOMY)
	// ============================================================

	/**
	 * Get Living State (GET /api/living/state)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Living")
	void GetLivingState(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Check for Proactive Message (GET /api/living/proactive)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Living")
	void CheckProactiveMessage(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Check Activity Completion (GET /api/living/activity/check)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Living")
	void CheckActivityCompletion(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Start Autonomous Activity (POST /api/living/activity/start)
	 * @param Activity Activity name (reading, training, exploring, resting, playing)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Living")
	void StartActivity(const FString& Activity, FOnNajikaActionResponse OnResponse);

	// ============================================================
	// SYSTEM STATUS
	// ============================================================

	/**
	 * Get System Status (GET /api/status)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|System")
	void GetSystemStatus(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Get Available Rooms (GET /api/rooms)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|System")
	void GetRooms(FOnNajikaHTTPResponse OnResponse);

	/**
	 * Save State to Disk (GET /api/save)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|System")
	void SaveState(FOnNajikaActionResponse OnResponse);

	/**
	 * Get Complete State (GET /api/state)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|System")
	void GetCompleteState(FOnNajikaHTTPResponse OnResponse);

	// ============================================================
	// MINI-GAMES
	// ============================================================

	/**
	 * Submit Rhythm Game Score (POST /api/minigame/rhythm)
	 * @param Score Score achieved
	 * @param Accuracy Accuracy (0.0-1.0)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Minigames")
	void SubmitRhythmScore(int32 Score, float Accuracy, FOnNajikaActionResponse OnResponse);

	/**
	 * Interact with Garden (POST /api/minigame/garden)
	 * @param Action Garden action (plant, water, harvest)
	 * @param ItemID Item ID (e.g., tomato_seeds)
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Minigames")
	void GardenAction(const FString& Action, const FString& ItemID, FOnNajikaActionResponse OnResponse);

	/**
	 * Submit Reflex Test Result (POST /api/minigame/reflex)
	 * @param ReactionTimeMS Reaction time in milliseconds
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Minigames")
	void SubmitReflexScore(int32 ReactionTimeMS, FOnNajikaActionResponse OnResponse);

	// ============================================================
	// GENERIC HTTP METHODS
	// ============================================================

	/**
	 * Generic POST Request
	 * @param Endpoint Endpoint path (e.g. /api/chat)
	 * @param JsonData Request body as JSON string
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void PostRequest(const FString& Endpoint, const FString& JsonData, FOnNajikaHTTPResponse OnResponse);

	/**
	 * Generic GET Request
	 * @param Endpoint Endpoint path
	 * @param OnResponse Callback delegate
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Backend")
	void GetRequest(const FString& Endpoint, FOnNajikaHTTPResponse OnResponse);

private:
	// Internal callback handlers
	void OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaHTTPResponse Callback);
	void OnChatRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaChatResponse Callback);
	void OnStatusRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaStatusResponse Callback);
	void OnActionRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaActionResponse Callback);
	void OnBattleStartRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnBattleStartResponse Callback);
	void OnBattleActionRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnBattleActionResponse Callback);
	void OnVoiceCallAudioRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnVoiceCallAudioResponse Callback);

	// Helper functions
	TSharedPtr<FJsonObject> ParseJsonResponse(const FString& JsonString);
	FNajikaState ParseNajikaState(TSharedPtr<FJsonObject> JsonObject);
	FNajikaLivingState ParseLivingState(TSharedPtr<FJsonObject> JsonObject);
	FNajikaBattleState ParseBattleState(TSharedPtr<FJsonObject> JsonObject);
	TArray<FNajikaEnemy> ParseEnemies(TSharedPtr<FJsonValue> JsonValue);

	FString BaseURL;
};
