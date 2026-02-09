// Copyright Model 1 - Najika Digivice APK

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "Http.h"
#include "AudioCapture.h"
#include "Sound/SoundWaveProcedural.h"
#include "VoiceCallManager.generated.h"

// ============================================
// DELEGATES (Callbacks)
// ============================================

/**
 * Called when voice call starts successfully
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnVoiceCallStarted);

/**
 * Called when voice call ends
 * @param Duration - Call duration in seconds
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnVoiceCallEnded, float, Duration);

/**
 * Called when user speech is recognized
 * @param Text - Recognized text from Whisper STT
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnSpeechRecognized, const FString&, Text);

/**
 * Called when Najika responds with TTS audio
 * @param AudioData - Sound wave to play
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnNajikaResponse, USoundWave*, AudioData);

/**
 * Called on voice call error
 * @param ErrorMessage - Error description
 */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnVoiceCallError, const FString&, ErrorMessage);

// ============================================
// VOICE CALL MANAGER
// ============================================

/**
 * Voice Call Manager for Najika Voice Calls
 *
 * Features:
 * - Microphone capture (Android + Desktop)
 * - Audio streaming to backend (POST /api/voice_call/audio)
 * - Whisper STT recognition
 * - TTS audio playback (Megumin voice!)
 * - Real-time conversation
 *
 * Usage:
 *   UVoiceCallManager* VoiceCall = NewObject<UVoiceCallManager>();
 *   VoiceCall->StartVoiceCall();
 *   VoiceCall->OnSpeechRecognized.AddDynamic(this, &AMyActor::HandleSpeech);
 */
UCLASS(Blueprintable)
class NAJIKAVOICESYSTEM_API UVoiceCallManager : public UObject
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
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	FString BaseURL = TEXT("http://127.0.0.1:8000");

	/**
	 * Audio capture sample rate (Hz)
	 * Default: 16000 (Whisper optimal)
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	int32 SampleRate = 16000;

	/**
	 * Audio buffer size (samples)
	 * Default: 4096
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	int32 BufferSize = 4096;

	/**
	 * Voice Activity Detection threshold (0-1)
	 * Default: 0.02 (2%)
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	float VADThreshold = 0.02f;

	/**
	 * Silence duration to auto-stop recording (seconds)
	 * Default: 2.0 seconds
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Voice|Config")
	float SilenceDuration = 2.0f;

	// ============================================
	// EVENTS
	// ============================================

	/**
	 * Called when voice call starts
	 */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
	FOnVoiceCallStarted OnVoiceCallStarted;

	/**
	 * Called when voice call ends
	 */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
	FOnVoiceCallEnded OnVoiceCallEnded;

	/**
	 * Called when speech is recognized
	 */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
	FOnSpeechRecognized OnSpeechRecognized;

	/**
	 * Called when Najika responds
	 */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
	FOnNajikaResponse OnNajikaResponse;

	/**
	 * Called on error
	 */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice|Events")
	FOnVoiceCallError OnVoiceCallError;

	// ============================================
	// VOICE CALL CONTROL
	// ============================================

	/**
	 * Start voice call with Najika
	 *
	 * 1. Request microphone permission (Android)
	 * 2. Start audio capture
	 * 3. Send POST /api/voice_call/start
	 * 4. Begin streaming audio
	 *
	 * @return True if call started successfully
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	bool StartVoiceCall();

	/**
	 * End voice call
	 *
	 * 1. Stop audio capture
	 * 2. Send POST /api/voice_call/end
	 * 3. Cleanup resources
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void EndVoiceCall();

	/**
	 * Is voice call currently active?
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsCallActive() const { return bIsCallActive; }

	/**
	 * Get current call duration (seconds)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	float GetCallDuration() const;

	/**
	 * Manually send audio chunk to backend
	 * (Usually automatic, but can be called manually)
	 *
	 * @param AudioData - Raw audio data (PCM 16-bit)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SendAudioChunk(const TArray<uint8>& AudioData);

	// ============================================
	// MICROPHONE CONTROL
	// ============================================

	/**
	 * Check if microphone permission is granted (Android)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool HasMicrophonePermission() const;

	/**
	 * Request microphone permission (Android)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void RequestMicrophonePermission();

	/**
	 * Get current audio level (0-1)
	 * Useful for UI visualization
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	float GetAudioLevel() const { return CurrentAudioLevel; }

	// ============================================
	// INITIALIZATION
	// ============================================

	/**
	 * Initialize voice call system
	 */
	virtual void Initialize();

	/**
	 * Shutdown voice call system
	 */
	virtual void Shutdown();

private:
	// ============================================
	// INTERNAL STATE
	// ============================================

	/** Is call currently active? */
	bool bIsCallActive = false;

	/** Call start time */
	double CallStartTime = 0.0;

	/** Audio capture device */
	TSharedPtr<Audio::FAudioCapture> AudioCapture;

	/** Audio buffer for streaming */
	TArray<float> AudioBuffer;

	/** Current audio level (for visualization) */
	float CurrentAudioLevel = 0.0f;

	/** Silence timer (for auto-stop) */
	float SilenceTimer = 0.0f;

	// ============================================
	// AUDIO CAPTURE CALLBACKS
	// ============================================

	/**
	 * Called when audio data is captured from microphone
	 * @param InAudio - Audio buffer
	 * @param NumSamples - Number of samples
	 * @param NumChannels - Number of channels
	 */
	void OnAudioCapture(const float* InAudio, int32 NumSamples, int32 NumChannels);

	/**
	 * Process captured audio
	 * - Convert to Base64
	 * - Send to backend
	 * - Check for silence
	 */
	void ProcessAudioBuffer(const TArray<float>& Buffer);

	/**
	 * Calculate audio level (RMS)
	 */
	float CalculateAudioLevel(const TArray<float>& Buffer);

	/**
	 * Detect voice activity
	 * @return True if voice detected
	 */
	bool DetectVoiceActivity(float AudioLevel);

	// ============================================
	// BACKEND COMMUNICATION
	// ============================================

	/**
	 * Send audio chunk to backend
	 * POST /api/voice_call/audio
	 */
	void SendAudioToBackend(const TArray<uint8>& AudioData);

	/**
	 * Handle STT response from backend
	 */
	void HandleSTTResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful);

	/**
	 * Handle TTS audio from backend
	 */
	void HandleTTSAudio(const FString& AudioPath);

	/**
	 * Download and play TTS audio
	 */
	void DownloadAndPlayAudio(const FString& AudioURL);

	// ============================================
	// AUDIO PLAYBACK
	// ============================================

	/**
	 * Play audio response from Najika
	 * @param AudioData - WAV audio data
	 */
	void PlayAudioResponse(const TArray<uint8>& AudioData);

	/**
	 * Create sound wave from audio data
	 */
	USoundWaveProcedural* CreateSoundWaveFromData(const TArray<uint8>& AudioData);
};
