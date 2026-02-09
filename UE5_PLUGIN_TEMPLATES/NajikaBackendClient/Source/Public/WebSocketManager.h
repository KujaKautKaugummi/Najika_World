// Copyright Model 1 - Najika Digivice APK

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "IWebSocket.h"
#include "WebSocketManager.generated.h"

// ============================================
// DELEGATES
// ============================================

/**
 * Called when WebSocket connects
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnWebSocketConnected);

/**
 * Called when WebSocket disconnects
 * @param Reason - Disconnect reason
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWebSocketDisconnected, const FString&, Reason);

/**
 * Called when message is received
 * @param Message - JSON message from server
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWebSocketMessage, const FString&, Message);

/**
 * Called on WebSocket error
 * @param Error - Error message
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWebSocketError, const FString&, Error);

// ============================================
// WEBSOCKET MANAGER
// ============================================

/**
 * WebSocket Manager for real-time communication with Najika backend
 *
 * Features:
 * - Persistent WebSocket connection
 * - Real-time state updates
 * - Proactive messages from Najika
 * - Living system events
 * - Auto-reconnect on disconnect
 *
 * Usage:
 *   UWebSocketManager* WS = NewObject<UWebSocketManager>();
 *   WS->Connect("ws://127.0.0.1:8000/ws");
 *   WS->OnWebSocketMessage.AddDynamic(this, &AMyActor::HandleMessage);
 */
UCLASS(Blueprintable)
class NAJIKABACKENDCLIENT_API UWebSocketManager : public UObject
{
	GENERATED_BODY()

public:
	// ============================================
	// CONFIGURATION
	// ============================================

	/**
	 * WebSocket URL
	 * Default: ws://127.0.0.1:8000/ws
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|WebSocket|Config")
	FString WebSocketURL = TEXT("ws://127.0.0.1:8000/ws");

	/**
	 * Auto-reconnect on disconnect
	 * Default: true
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|WebSocket|Config")
	bool bAutoReconnect = true;

	/**
	 * Reconnect delay (seconds)
	 * Default: 5.0 seconds
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|WebSocket|Config")
	float ReconnectDelay = 5.0f;

	/**
	 * Heartbeat interval (seconds)
	 * Default: 30.0 seconds
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|WebSocket|Config")
	float HeartbeatInterval = 30.0f;

	// ============================================
	// EVENTS
	// ============================================

	UPROPERTY(BlueprintAssignable, Category = "Najika|WebSocket|Events")
	FOnWebSocketConnected OnConnected;

	UPROPERTY(BlueprintAssignable, Category = "Najika|WebSocket|Events")
	FOnWebSocketDisconnected OnDisconnected;

	UPROPERTY(BlueprintAssignable, Category = "Najika|WebSocket|Events")
	FOnWebSocketMessage OnMessageReceived;

	UPROPERTY(BlueprintAssignable, Category = "Najika|WebSocket|Events")
	FOnWebSocketError OnError;

	// ============================================
	// CONNECTION CONTROL
	// ============================================

	/**
	 * Connect to WebSocket server
	 * @param URL - WebSocket URL (optional, uses WebSocketURL if not provided)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|WebSocket")
	void Connect(const FString& URL = TEXT(""));

	/**
	 * Disconnect from WebSocket server
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|WebSocket")
	void Disconnect();

	/**
	 * Is WebSocket connected?
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|WebSocket")
	bool IsConnected() const;

	/**
	 * Send message to server
	 * @param Message - JSON message string
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|WebSocket")
	void SendMessage(const FString& Message);

	/**
	 * Send JSON object to server
	 * @param Type - Message type
	 * @param Data - Message data (JSON object as string)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|WebSocket")
	void SendJSON(const FString& Type, const FString& Data);

	// ============================================
	// INITIALIZATION
	// ============================================

	virtual void BeginDestroy() override;

private:
	// ============================================
	// INTERNAL STATE
	// ============================================

	/** WebSocket instance */
	TSharedPtr<IWebSocket> WebSocket;

	/** Is currently connected? */
	bool bIsConnected = false;

	/** Heartbeat timer handle */
	FTimerHandle HeartbeatTimer;

	/** Reconnect timer handle */
	FTimerHandle ReconnectTimer;

	// ============================================
	// WEBSOCKET CALLBACKS
	// ============================================

	void OnConnectedCallback();
	void OnDisconnectedCallback(int32 StatusCode, const FString& Reason, bool bWasClean);
	void OnMessageCallback(const FString& Message);
	void OnErrorCallback(const FString& Error);

	// ============================================
	// HEARTBEAT
	// ============================================

	void StartHeartbeat();
	void StopHeartbeat();
	void SendHeartbeat();

	// ============================================
	// AUTO-RECONNECT
	// ============================================

	void ScheduleReconnect();
	void AttemptReconnect();
};
