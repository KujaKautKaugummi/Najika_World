// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "IWebSocket.h"
#include "OPTIONAL_NajikaWebSocketReconnect.generated.h"

// ============================================================================
// OPTIONAL: WebSocket Reconnection Logic
// ============================================================================
//
// HINWEIS: Diese Klasse ist OPTIONAL und wurde nachträglich hinzugefügt
// zur Verbesserung der WebSocket-Verbindungsstabilität.
//
// Features:
// - Automatische Reconnection bei Verbindungsabbruch
// - Exponential Backoff (2s, 4s, 8s, 16s, max 30s)
// - Packet Queue während Disconnect
// - State Synchronization nach Reconnect
// - Max Retry Limit (10 Versuche)
//
// Usage:
//   UNajikaWebSocketReconnect* WSReconnect = NewObject<UNajikaWebSocketReconnect>(this);
//   WSReconnect->Initialize(WebSocketURL, JWTToken);
//   WSReconnect->OnConnected.AddDynamic(this, &UMyClass::OnConnected);
//   WSReconnect->OnMessage.AddDynamic(this, &UMyClass::OnMessage);
//   WSReconnect->Connect();
//
// ============================================================================

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnWSConnected);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnWSDisconnected);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWSMessage, const FString&, Message);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWSError, const FString&, Error);

UENUM(BlueprintType)
enum class EWebSocketState : uint8
{
	Disconnected UMETA(DisplayName = "Disconnected"),
	Connecting UMETA(DisplayName = "Connecting"),
	Connected UMETA(DisplayName = "Connected"),
	Reconnecting UMETA(DisplayName = "Reconnecting"),
	Failed UMETA(DisplayName = "Failed")
};

/**
 * OPTIONAL: WebSocket mit automatischer Reconnection Logic
 */
UCLASS(BlueprintType)
class NAJIKAVOICESYSTEM_API UNajikaWebSocketReconnect : public UObject
{
	GENERATED_BODY()

public:
	UNajikaWebSocketReconnect();

	// ========================================================================
	// INITIALIZATION
	// ========================================================================

	/**
	 * Initialize WebSocket connection parameters
	 * @param URL WebSocket URL (e.g., ws://localhost:8000/ws/voice/room_123)
	 * @param Token JWT authentication token
	 * @param MaxRetries Maximum reconnection attempts (default: 10)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|WebSocket")
	void Initialize(const FString& URL, const FString& Token, int32 MaxRetries = 10);

	/**
	 * Connect to WebSocket server
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|WebSocket")
	void Connect();

	/**
	 * Disconnect from WebSocket server
	 * @param bGraceful If true, send close message before disconnecting
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|WebSocket")
	void Disconnect(bool bGraceful = true);

	// ========================================================================
	// MESSAGING
	// ========================================================================

	/**
	 * Send message to server
	 * If disconnected, message is queued and sent after reconnect
	 * @param Message JSON message as string
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|WebSocket")
	void SendMessage(const FString& Message);

	/**
	 * Send binary data to server
	 * @param Data Binary data
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|WebSocket")
	void SendBinary(const TArray<uint8>& Data);

	// ========================================================================
	// STATE
	// ========================================================================

	/**
	 * Get current connection state
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice|WebSocket")
	EWebSocketState GetState() const { return State; }

	/**
	 * Check if connected
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice|WebSocket")
	bool IsConnected() const { return State == EWebSocketState::Connected; }

	/**
	 * Check if reconnecting
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice|WebSocket")
	bool IsReconnecting() const { return State == EWebSocketState::Reconnecting; }

	/**
	 * Get number of reconnection attempts
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice|WebSocket")
	int32 GetReconnectAttempts() const { return ReconnectAttempts; }

	/**
	 * Get queued message count
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice|WebSocket")
	int32 GetQueuedMessageCount() const { return MessageQueue.Num(); }

	// ========================================================================
	// DELEGATES
	// ========================================================================

	/** Called when connection established */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|WebSocket")
	FOnWSConnected OnConnected;

	/** Called when connection lost */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|WebSocket")
	FOnWSDisconnected OnDisconnected;

	/** Called when message received */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|WebSocket")
	FOnWSMessage OnMessage;

	/** Called on error */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|WebSocket")
	FOnWSError OnError;

private:
	// ========================================================================
	// WEBSOCKET CALLBACKS
	// ========================================================================

	void OnWebSocketConnected();
	void OnWebSocketConnectionError(const FString& Error);
	void OnWebSocketClosed(int32 StatusCode, const FString& Reason, bool bWasClean);
	void OnWebSocketMessage(const FString& Message);
	void OnWebSocketBinaryMessage(const void* Data, SIZE_T Size, SIZE_T BytesRemaining);

	// ========================================================================
	// RECONNECTION LOGIC
	// ========================================================================

	void StartReconnect();
	void CancelReconnect();
	void DoReconnect();
	float GetBackoffDelay() const;

	// ========================================================================
	// MESSAGE QUEUE
	// ========================================================================

	void QueueMessage(const FString& Message);
	void FlushMessageQueue();
	void ClearMessageQueue();

	// ========================================================================
	// MEMBERS
	// ========================================================================

	TSharedPtr<IWebSocket> WebSocket;

	FString WebSocketURL;
	FString AuthToken;

	EWebSocketState State;

	int32 MaxReconnectAttempts;
	int32 ReconnectAttempts;
	FTimerHandle ReconnectTimerHandle;

	TArray<FString> MessageQueue;
	static constexpr int32 MaxQueueSize = 100;

	bool bIsReconnecting;
	bool bManualDisconnect;
	bool bInitialized;

	// Backoff configuration
	float BaseBackoffDelay;       // 2.0 seconds
	float MaxBackoffDelay;        // 30.0 seconds
	float BackoffMultiplier;      // 2.0 (exponential)
};
