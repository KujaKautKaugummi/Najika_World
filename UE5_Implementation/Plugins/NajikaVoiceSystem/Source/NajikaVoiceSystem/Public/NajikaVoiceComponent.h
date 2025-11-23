// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "NajikaVoiceTypes.h"
#include "NajikaVoiceCapture.h"
#include "NajikaVoicePlayback.h"
#include "NajikaWhisperClient.h"
#include "NajikaVoiceComponent.generated.h"

/**
 * Main component for voice chat functionality
 * Combines capture, playback, and transcription in one easy-to-use component
 *
 * Usage:
 * 1. Add to PlayerController or Character
 * 2. Call Initialize()
 * 3. Use StartVoiceCall() to begin voice chat
 * 4. Use StopVoiceCall() to end voice chat
 */
UCLASS(ClassGroup=(Najika), meta=(BlueprintSpawnableComponent))
class NAJIKAVOICESYSTEM_API UNajikaVoiceComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UNajikaVoiceComponent();

protected:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

public:
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	/**
	 * Initialize voice system
	 * @param BackendURL Backend server URL for Whisper AI
	 * @param Config Voice capture configuration
	 * @return True if initialization successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	bool Initialize(const FString& BackendURL = TEXT("http://localhost:8000"), const FNajikaVoiceCaptureConfig& Config = FNajikaVoiceCaptureConfig());

	/**
	 * Start a voice call
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void StartVoiceCall();

	/**
	 * Stop the current voice call
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void StopVoiceCall();

	/**
	 * Check if voice call is active
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsInCall() const { return CallState == EVoiceCallState::InCall; }

	/**
	 * Get current call state
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	EVoiceCallState GetCallState() const { return CallState; }

	/**
	 * Start push-to-talk (hold to talk)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void StartPushToTalk();

	/**
	 * Stop push-to-talk (release button)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void StopPushToTalk();

	/**
	 * Is push-to-talk currently active
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsPushToTalkActive() const { return bPushToTalkActive; }

	/**
	 * Enable/disable voice activity detection mode
	 * When enabled, audio is sent automatically when voice detected
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetVADMode(bool bEnabled);

	/**
	 * Set microphone input gain
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetMicrophoneGain(float Gain);

	/**
	 * Set playback volume
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetPlaybackVolume(float Volume);

	/**
	 * Get current audio input level (0.0 - 1.0)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	float GetInputLevel() const;

	/**
	 * Get call statistics
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	FNajikaVoiceCallStats GetCallStats() const { return CallStats; }

	/**
	 * Enable automatic transcription of voice
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetAutoTranscribeEnabled(bool bEnabled);

	/**
	 * Manually trigger transcription of last audio buffer
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void TranscribeLastAudio();

	/**
	 * Mute/unmute microphone
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetMicrophoneMuted(bool bMuted);

	/**
	 * Is microphone muted
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsMicrophoneMuted() const { return bMicrophoneMuted; }

	/**
	 * Mute/unmute playback
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetPlaybackMuted(bool bMuted);

	/**
	 * Is playback muted
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsPlaybackMuted() const { return bPlaybackMuted; }

public:
	// Configuration

	/** Auto-initialize on BeginPlay */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	bool bAutoInitialize = true;

	/** Backend URL for Whisper AI */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	FString BackendURL = TEXT("http://localhost:8000");

	/** Voice capture configuration */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	FNajikaVoiceCaptureConfig CaptureConfig;

	/** Enable push-to-talk mode (default: false = VAD mode) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	bool bUsePushToTalk = false;

	/** Enable automatic transcription */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	bool bAutoTranscribe = false;

public:
	// Delegates

	/** Fired when call state changes */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice")
	FOnVoiceCallStateChanged OnVoiceCallStateChanged;

	/** Fired when voice activity is detected */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice")
	FOnVoiceActivityDetected OnVoiceActivityDetected;

	/** Fired when transcription is complete */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice")
	FOnWhisperTranscriptionComplete OnTranscriptionComplete;

protected:
	/** Handle audio packet ready for sending */
	UFUNCTION()
	void OnAudioPacketReady(const FNajikaAudioPacket& Packet);

	/** Handle transcription complete */
	UFUNCTION()
	void OnWhisperTranscriptionComplete(const FNajikaWhisperResult& Result);

	/** Handle voice activity detected */
	UFUNCTION()
	void OnVoiceDetected(bool bDetected);

	/** Update call statistics */
	void UpdateCallStats(float DeltaTime);

	/** Set call state */
	void SetCallState(EVoiceCallState NewState);

private:
	/** Voice capture system */
	UPROPERTY()
	UNajikaVoiceCapture* VoiceCapture;

	/** Voice playback system */
	UPROPERTY()
	UNajikaVoicePlayback* VoicePlayback;

	/** Whisper AI client */
	UPROPERTY()
	UNajikaWhisperClient* WhisperClient;

	/** Current call state */
	EVoiceCallState CallState;

	/** Is push-to-talk currently active */
	bool bPushToTalkActive;

	/** Is microphone muted */
	bool bMicrophoneMuted;

	/** Is playback muted */
	bool bPlaybackMuted;

	/** Call statistics */
	FNajikaVoiceCallStats CallStats;

	/** Last audio packet for transcription */
	FNajikaAudioPacket LastAudioPacket;

	/** Call start time */
	float CallStartTime;
};
