// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "Http.h"
#include "NajikaVoiceTypes.h"
#include "NajikaWhisperClient.generated.h"

/**
 * Client for Whisper AI speech-to-text service
 * Sends audio data to backend and receives transcription
 */
UCLASS(BlueprintType)
class NAJIKAVOICESYSTEM_API UNajikaWhisperClient : public UObject
{
	GENERATED_BODY()

public:
	UNajikaWhisperClient();

	/**
	 * Initialize Whisper client
	 * @param BackendURL URL of backend server (e.g., "http://localhost:8000")
	 * @return True if initialization successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	bool Initialize(const FString& BackendURL = TEXT("http://localhost:8000"));

	/**
	 * Transcribe audio data to text
	 * @param AudioData Raw audio data (PCM format)
	 * @param SampleRate Audio sample rate (Hz)
	 * @param LanguageCode Target language (e.g., "en", "ja", "de", "auto")
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void TranscribeAudio(const TArray<uint8>& AudioData, int32 SampleRate = 48000, const FString& LanguageCode = TEXT("auto"));

	/**
	 * Transcribe audio packet to text
	 * @param Packet Audio packet to transcribe
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void TranscribePacket(const FNajikaAudioPacket& Packet);

	/**
	 * Set backend URL
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetBackendURL(const FString& URL);

	/**
	 * Get current backend URL
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	FString GetBackendURL() const { return BackendURL; }

	/**
	 * Check if currently processing a request
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsProcessing() const { return bIsProcessing; }

public:
	/** Fired when transcription is complete */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice")
	FOnWhisperTranscriptionComplete OnTranscriptionComplete;

protected:
	/** Handle HTTP response */
	void OnTranscriptionResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);

	/** Parse Whisper API response */
	FNajikaWhisperResult ParseResponse(const FString& ResponseContent);

private:
	/** Backend server URL */
	FString BackendURL;

	/** Is currently processing */
	bool bIsProcessing;

	/** Request start time */
	double RequestStartTime;

	/** HTTP module reference */
	FHttpModule* HttpModule;
};
