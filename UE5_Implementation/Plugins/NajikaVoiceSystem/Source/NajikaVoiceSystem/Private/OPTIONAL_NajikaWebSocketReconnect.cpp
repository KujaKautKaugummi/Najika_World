// Copyright Najika Development Team. All Rights Reserved.

#include "OPTIONAL_NajikaWebSocketReconnect.h"
#include "WebSocketsModule.h"
#include "IWebSocket.h"
#include "TimerManager.h"

// ============================================================================
// CONSTRUCTION
// ============================================================================

UNajikaWebSocketReconnect::UNajikaWebSocketReconnect()
	: State(EWebSocketState::Disconnected)
	, MaxReconnectAttempts(10)
	, ReconnectAttempts(0)
	, bIsReconnecting(false)
	, bManualDisconnect(false)
	, bInitialized(false)
	, BaseBackoffDelay(2.0f)
	, MaxBackoffDelay(30.0f)
	, BackoffMultiplier(2.0f)
{
}

// ============================================================================
// INITIALIZATION
// ============================================================================

void UNajikaWebSocketReconnect::Initialize(const FString& URL, const FString& Token, int32 MaxRetries)
{
	WebSocketURL = URL;
	AuthToken = Token;
	MaxReconnectAttempts = MaxRetries;
	bInitialized = true;

	UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] WebSocketReconnect initialized: URL=%s, MaxRetries=%d"), *URL, MaxRetries);
}

// ============================================================================
// CONNECTION
// ============================================================================

void UNajikaWebSocketReconnect::Connect()
{
	if (!bInitialized)
	{
		UE_LOG(LogTemp, Error, TEXT("[OPTIONAL] WebSocketReconnect not initialized! Call Initialize() first."));
		OnError.Broadcast(TEXT("Not initialized"));
		return;
	}

	if (State == EWebSocketState::Connected || State == EWebSocketState::Connecting)
	{
		UE_LOG(LogTemp, Warning, TEXT("[OPTIONAL] Already connected or connecting"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Connecting to WebSocket: %s"), *WebSocketURL);

	State = EWebSocketState::Connecting;
	bManualDisconnect = false;

	// Create WebSocket
	FString URLWithToken = WebSocketURL;
	if (!AuthToken.IsEmpty())
	{
		URLWithToken += FString::Printf(TEXT("?token=%s"), *AuthToken);
	}

	WebSocket = FWebSocketsModule::Get().CreateWebSocket(URLWithToken, TEXT("ws"));

	// Bind callbacks
	WebSocket->OnConnected().AddUObject(this, &UNajikaWebSocketReconnect::OnWebSocketConnected);
	WebSocket->OnConnectionError().AddUObject(this, &UNajikaWebSocketReconnect::OnWebSocketConnectionError);
	WebSocket->OnClosed().AddUObject(this, &UNajikaWebSocketReconnect::OnWebSocketClosed);
	WebSocket->OnMessage().AddUObject(this, &UNajikaWebSocketReconnect::OnWebSocketMessage);
	WebSocket->OnBinaryMessage().AddUObject(this, &UNajikaWebSocketReconnect::OnWebSocketBinaryMessage);

	// Connect
	WebSocket->Connect();
}

void UNajikaWebSocketReconnect::Disconnect(bool bGraceful)
{
	UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Disconnecting WebSocket (graceful=%d)"), bGraceful);

	bManualDisconnect = true;
	CancelReconnect();
	ClearMessageQueue();

	if (WebSocket && WebSocket->IsConnected())
	{
		if (bGraceful)
		{
			// Send leave message
			SendMessage(TEXT("{\"type\":\"leave\"}"));
		}

		WebSocket->Close();
	}

	State = EWebSocketState::Disconnected;
}

// ============================================================================
// WEBSOCKET CALLBACKS
// ============================================================================

void UNajikaWebSocketReconnect::OnWebSocketConnected()
{
	UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] WebSocket connected!"));

	State = EWebSocketState::Connected;
	ReconnectAttempts = 0;
	bIsReconnecting = false;

	// Flush queued messages
	FlushMessageQueue();

	// Notify
	OnConnected.Broadcast();
}

void UNajikaWebSocketReconnect::OnWebSocketConnectionError(const FString& Error)
{
	UE_LOG(LogTemp, Error, TEXT("[OPTIONAL] WebSocket connection error: %s"), *Error);

	State = EWebSocketState::Failed;

	OnError.Broadcast(Error);

	// Attempt reconnect
	if (!bManualDisconnect && ReconnectAttempts < MaxReconnectAttempts)
	{
		StartReconnect();
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("[OPTIONAL] Max reconnect attempts reached or manual disconnect"));
		ClearMessageQueue();
	}
}

void UNajikaWebSocketReconnect::OnWebSocketClosed(int32 StatusCode, const FString& Reason, bool bWasClean)
{
	UE_LOG(LogTemp, Warning, TEXT("[OPTIONAL] WebSocket closed: Code=%d, Reason=%s, Clean=%d"),
		StatusCode, *Reason, bWasClean);

	bool bWasConnected = (State == EWebSocketState::Connected);

	State = EWebSocketState::Disconnected;

	OnDisconnected.Broadcast();

	// Attempt reconnect if not manual disconnect and was previously connected
	if (!bManualDisconnect && bWasConnected && ReconnectAttempts < MaxReconnectAttempts)
	{
		StartReconnect();
	}
	else if (bManualDisconnect)
	{
		UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Manual disconnect, not reconnecting"));
		ClearMessageQueue();
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("[OPTIONAL] Max reconnect attempts reached"));
		ClearMessageQueue();
	}
}

void UNajikaWebSocketReconnect::OnWebSocketMessage(const FString& Message)
{
	// Broadcast message to listeners
	OnMessage.Broadcast(Message);
}

void UNajikaWebSocketReconnect::OnWebSocketBinaryMessage(const void* Data, SIZE_T Size, SIZE_T BytesRemaining)
{
	UE_LOG(LogTemp, Verbose, TEXT("[OPTIONAL] Received binary message: %lld bytes"), Size);
	// Handle binary if needed
}

// ============================================================================
// RECONNECTION LOGIC
// ============================================================================

void UNajikaWebSocketReconnect::StartReconnect()
{
	if (bIsReconnecting)
	{
		UE_LOG(LogTemp, Warning, TEXT("[OPTIONAL] Reconnect already in progress"));
		return;
	}

	ReconnectAttempts++;
	bIsReconnecting = true;
	State = EWebSocketState::Reconnecting;

	float Delay = GetBackoffDelay();

	UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Reconnect attempt %d/%d in %.1f seconds..."),
		ReconnectAttempts, MaxReconnectAttempts, Delay);

	// Schedule reconnect
	GetWorld()->GetTimerManager().SetTimer(
		ReconnectTimerHandle,
		this,
		&UNajikaWebSocketReconnect::DoReconnect,
		Delay,
		false
	);
}

void UNajikaWebSocketReconnect::CancelReconnect()
{
	if (bIsReconnecting)
	{
		UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Cancelling reconnect timer"));
		GetWorld()->GetTimerManager().ClearTimer(ReconnectTimerHandle);
		bIsReconnecting = false;
	}
}

void UNajikaWebSocketReconnect::DoReconnect()
{
	UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Attempting reconnect..."));

	bIsReconnecting = false;

	// Close old connection if exists
	if (WebSocket)
	{
		WebSocket->Close();
		WebSocket.Reset();
	}

	// Try connecting again
	Connect();
}

float UNajikaWebSocketReconnect::GetBackoffDelay() const
{
	// Exponential backoff: 2s, 4s, 8s, 16s, 30s (max)
	float Delay = BaseBackoffDelay * FMath::Pow(BackoffMultiplier, ReconnectAttempts - 1);
	return FMath::Min(Delay, MaxBackoffDelay);
}

// ============================================================================
// MESSAGING
// ============================================================================

void UNajikaWebSocketReconnect::SendMessage(const FString& Message)
{
	if (State == EWebSocketState::Connected && WebSocket && WebSocket->IsConnected())
	{
		// Send immediately
		WebSocket->Send(Message);
	}
	else
	{
		// Queue for later
		QueueMessage(Message);
	}
}

void UNajikaWebSocketReconnect::SendBinary(const TArray<uint8>& Data)
{
	if (State == EWebSocketState::Connected && WebSocket && WebSocket->IsConnected())
	{
		WebSocket->Send(Data.GetData(), Data.Num(), true);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[OPTIONAL] Cannot send binary while disconnected (queuing not supported for binary)"));
	}
}

// ============================================================================
// MESSAGE QUEUE
// ============================================================================

void UNajikaWebSocketReconnect::QueueMessage(const FString& Message)
{
	if (MessageQueue.Num() >= MaxQueueSize)
	{
		UE_LOG(LogTemp, Warning, TEXT("[OPTIONAL] Message queue full, dropping oldest message"));
		MessageQueue.RemoveAt(0);
	}

	MessageQueue.Add(Message);
	UE_LOG(LogTemp, Verbose, TEXT("[OPTIONAL] Queued message (queue size: %d)"), MessageQueue.Num());
}

void UNajikaWebSocketReconnect::FlushMessageQueue()
{
	if (MessageQueue.Num() == 0)
	{
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Flushing %d queued messages"), MessageQueue.Num());

	for (const FString& Message : MessageQueue)
	{
		if (WebSocket && WebSocket->IsConnected())
		{
			WebSocket->Send(Message);
		}
	}

	MessageQueue.Empty();
}

void UNajikaWebSocketReconnect::ClearMessageQueue()
{
	if (MessageQueue.Num() > 0)
	{
		UE_LOG(LogTemp, Log, TEXT("[OPTIONAL] Clearing %d queued messages"), MessageQueue.Num());
		MessageQueue.Empty();
	}
}
