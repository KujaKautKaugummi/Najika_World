// NajikaVoiceClient.h
// Voice Call System with WebSocket support

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Interfaces/IHttpRequest.h"
#include "IWebSocket.h"
#include "NajikaVoiceClient.generated.h"

// Delegates
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnVoiceResponse, const FString&, ResponseText, const TArray<uint8>&, AudioData);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnVoiceCallStarted, const FString&, SessionId);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnVoiceCallEnded);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnTranscription, const FString&, TranscribedText);

/**
 * Voice Call Client for Najika
 * Handles STT (Whisper) and TTS (Edge/Coqui) via Backend
 */
UCLASS()
class NAJIKABACKEND_API UNajikaVoiceClient : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    // ============================================
    // VOICE CALL MANAGEMENT
    // ============================================

    /** Start a voice call with Najika */
    UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
    void StartVoiceCall();

    /** End the current voice call */
    UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
    void EndVoiceCall();

    /** Send audio data to backend for processing */
    UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
    void SendAudio(const TArray<uint8>& AudioData);

    /** Request TTS for text (without STT) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
    void RequestTTS(const FString& Text);

    /** Check if voice call is active */
    UFUNCTION(BlueprintPure, Category = "Najika|Voice")
    bool IsVoiceCallActive() const { return bIsCallActive; }

    // ============================================
    // EVENTS
    // ============================================

    /** Called when Najika responds with voice */
    UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
    FOnVoiceResponse OnVoiceResponse;

    /** Called when voice call starts */
    UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
    FOnVoiceCallStarted OnVoiceCallStarted;

    /** Called when voice call ends */
    UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
    FOnVoiceCallEnded OnVoiceCallEnded;

    /** Called when user speech is transcribed */
    UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
    FOnTranscription OnTranscription;

private:
    // Backend URL
    FString BackendURL = TEXT("http://127.0.0.1:8000");

    // WebSocket for real-time voice
    TSharedPtr<IWebSocket> WebSocket;
    bool bIsConnected = false;
    bool bIsCallActive = false;
    FString CurrentSessionId;

    // HTTP helpers
    void SendHTTPRequest(const FString& Endpoint, const FString& Verb, const FString& Content,
                         TFunction<void(FHttpResponsePtr)> OnSuccess);

    // WebSocket handlers
    void ConnectWebSocket();
    void DisconnectWebSocket();
    void OnWebSocketConnected();
    void OnWebSocketMessage(const FString& Message);
    void OnWebSocketClosed(int32 StatusCode, const FString& Reason, bool bWasClean);
    void OnWebSocketError(const FString& Error);

    // Audio helpers
    TArray<uint8> DecodeBase64Audio(const FString& Base64String);
    FString EncodeAudioBase64(const TArray<uint8>& AudioData);
};
