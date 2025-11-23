// Copyright Model 1 - Najika Digivice APK

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "Http.h"
#include "Json.h"
#include "NajikaAPIClient.generated.h"

// ============================================
// DELEGATES (Callbacks)
// ============================================

/**
 * Called when chat response is received
 * @param Response - Najika's response text
 * @param bSuccess - Whether request succeeded
 */
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnChatResponse, const FString&, Response, bool, bSuccess);

/**
 * Called when Najika status is received
 * @param Hunger - Hunger level (0-100)
 * @param Energy - Energy level (0-100)
 * @param Happiness - Happiness level (0-100)
 * @param bSuccess - Whether request succeeded
 */
DECLARE_DYNAMIC_DELEGATE_FourParams(FOnNajikaStatus, int32, Hunger, int32, Energy, int32, Happiness, bool, bSuccess);

/**
 * Called when action (feed/drink/wash) completes
 * @param Message - Response message from Najika
 * @param bSuccess - Whether request succeeded
 */
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnActionResponse, const FString&, Message, bool, bSuccess);

/**
 * Called when TTS audio is received
 * @param AudioData - Base64-encoded WAV audio
 * @param bSuccess - Whether request succeeded
 */
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnTTSResponse, const FString&, AudioData, bool, bSuccess);

// ============================================
// NAJIKA API CLIENT
// ============================================

/**
 * HTTP Client for Najika Python Backend
 *
 * Connects to: http://127.0.0.1:8000
 *
 * Features:
 * - Chat with Najika (POST /api/chat)
 * - Get Najika Status (GET /api/najika/status)
 * - Feed/Drink/Wash Najika (POST /api/najika/*)
 * - Text-to-Speech (POST /api/tts)
 * - Battle System (POST /api/battle/*)
 *
 * Usage:
 *   UNajikaAPIClient* Client = NewObject<UNajikaAPIClient>();
 *   Client->SendChatMessage("Hello Najika!", MyDelegate);
 */
UCLASS(Blueprintable)
class NAJIKABACKENDCLIENT_API UNajikaAPIClient : public UObject
{
	GENERATED_BODY()

public:
	// ============================================
	// CONFIGURATION
	// ============================================

	/**
	 * Backend server URL
	 * Default: http://127.0.0.1:8000
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Config")
	FString BaseURL = TEXT("http://127.0.0.1:8000");

	/**
	 * Request timeout in seconds
	 * Default: 30 seconds
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Config")
	float RequestTimeout = 30.0f;

	// ============================================
	// CHAT SYSTEM
	// ============================================

	/**
	 * Send chat message to Najika
	 *
	 * @param Message - Your message to Najika
	 * @param Callback - Called when response is received
	 *
	 * Backend Endpoint: POST /api/chat
	 * Request Body: {"message": "Hello Najika!"}
	 * Response: {"response": "Hi! ...", "ok": true}
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void SendChatMessage(const FString& Message, FOnChatResponse Callback);

	// ============================================
	// NAJIKA STATUS & CARE
	// ============================================

	/**
	 * Get Najika's current status (hunger, energy, happiness)
	 *
	 * @param Callback - Called when status is received
	 *
	 * Backend Endpoint: GET /api/najika/status
	 * Response: {"hunger": 85, "energy": 90, "happiness": 95, ...}
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Status")
	void GetNajikaStatus(FOnNajikaStatus Callback);

	/**
	 * Feed Najika (increases hunger)
	 *
	 * @param Callback - Called when action completes
	 *
	 * Backend Endpoint: POST /api/najika/feed
	 * Response: {"ok": true, "hunger": 100, "message": "Mmm, delicious!"}
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void FeedNajika(FOnActionResponse Callback);

	/**
	 * Give water to Najika (increases energy)
	 *
	 * @param Callback - Called when action completes
	 *
	 * Backend Endpoint: POST /api/najika/drink
	 * Response: {"ok": true, "energy": 100, "message": "Refreshing!"}
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void GiveWaterToNajika(FOnActionResponse Callback);

	/**
	 * Wash Najika (increases hygiene)
	 *
	 * @param Callback - Called when action completes
	 *
	 * Backend Endpoint: POST /api/najika/wash
	 * Response: {"ok": true, "hygiene": 100, "message": "I'm clean now!"}
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Care")
	void WashNajika(FOnActionResponse Callback);

	// ============================================
	// TEXT-TO-SPEECH
	// ============================================

	/**
	 * Generate speech audio from text (Megumin voice!)
	 *
	 * @param Text - Text to convert to speech
	 * @param Callback - Called when audio is generated
	 *
	 * Backend Endpoint: POST /api/tts
	 * Request Body: {"text": "EXPLOSION!"}
	 * Response: {"ok": true, "audio": "/backend/voices/output_123.wav"}
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|TTS")
	void GenerateTTS(const FString& Text, FOnTTSResponse Callback);

	// ============================================
	// HELPER FUNCTIONS (Private)
	// ============================================

private:
	/**
	 * Create HTTP request with proper headers
	 * @param Endpoint - API endpoint (e.g. "/api/chat")
	 * @param Verb - HTTP verb (GET, POST, etc.)
	 * @return HTTP request object
	 */
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> CreateRequest(const FString& Endpoint, const FString& Verb = TEXT("GET"));

	/**
	 * Handle HTTP response
	 * @param Request - Original HTTP request
	 * @param Response - HTTP response received
	 * @param bWasSuccessful - Whether request succeeded
	 */
	void HandleResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);

	/**
	 * Parse JSON response
	 * @param ResponseString - JSON string from server
	 * @return Parsed JSON object
	 */
	TSharedPtr<FJsonObject> ParseJSON(const FString& ResponseString);

	// Store delegates for callbacks
	TMap<FHttpRequestPtr, FOnChatResponse> ChatDelegates;
	TMap<FHttpRequestPtr, FOnNajikaStatus> StatusDelegates;
	TMap<FHttpRequestPtr, FOnActionResponse> ActionDelegates;
	TMap<FHttpRequestPtr, FOnTTSResponse> TTSDelegates;
};
