// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "AudioCapture.h"
#include "NajikaVoiceTypes.h"
#include "NajikaVoiceCapture.generated.h"

/**
 * Handles microphone input capture and processing
 * Features:
 * - Real-time audio capture
 * - Voice Activity Detection (VAD)
 * - Noise suppression
 * - Echo cancellation
 * - Automatic Gain Control (AGC)
 * - Opus encoding for network transmission
 */
UCLASS(BlueprintType)
class NAJIKAVOICESYSTEM_API UNajikaVoiceCapture : public UObject
{
	GENERATED_BODY()

public:
	UNajikaVoiceCapture();

	/**
	 * Initialize the voice capture system
	 * @param Config Configuration settings for voice capture
	 * @return True if initialization successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	bool Initialize(const FNajikaVoiceCaptureConfig& Config);

	/**
	 * Start capturing audio from microphone
	 * @return True if started successfully
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	bool StartCapture();

	/**
	 * Stop capturing audio
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void StopCapture();

	/**
	 * Pause audio capture (can be resumed)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void PauseCapture();

	/**
	 * Resume paused audio capture
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void ResumeCapture();

	/**
	 * Check if currently capturing
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsCapturing() const { return CaptureState == EVoiceCaptureState::Capturing; }

	/**
	 * Get current capture state
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	EVoiceCaptureState GetCaptureState() const { return CaptureState; }

	/**
	 * Update configuration during runtime
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void UpdateConfiguration(const FNajikaVoiceCaptureConfig& NewConfig);

	/**
	 * Set microphone input gain (0.0 - 2.0)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetInputGain(float Gain);

	/**
	 * Get current input gain
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	float GetInputGain() const { return Config.InputGain; }

	/**
	 * Enable/disable voice activity detection
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetVADEnabled(bool bEnabled);

	/**
	 * Set VAD sensitivity
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetVADSensitivity(EVADSensitivity Sensitivity);

	/**
	 * Enable/disable noise suppression
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetNoiseSuppressionEnabled(bool bEnabled);

	/**
	 * Enable/disable echo cancellation
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetEchoCancellationEnabled(bool bEnabled);

	/**
	 * Get current audio level (0.0 - 1.0)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	float GetCurrentAudioLevel() const { return CurrentAudioLevel; }

	/**
	 * Check if voice is currently being detected
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsVoiceDetected() const { return bVoiceDetected; }

	/**
	 * Get list of available microphone devices
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	TArray<FString> GetAvailableMicrophones();

	/**
	 * Select microphone device by index
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	bool SelectMicrophone(int32 DeviceIndex);

	/**
	 * Shutdown and release resources
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void Shutdown();

public:
	// Delegates

	/** Fired when capture state changes */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice")
	FOnVoiceCaptureStateChanged OnCaptureStateChanged;

	/** Fired when encoded audio packet is ready */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice")
	FOnAudioPacketReady OnAudioPacketReady;

	/** Fired when voice activity is detected/stopped */
	UPROPERTY(BlueprintAssignable, Category = "Najika|Voice")
	FOnVoiceActivityDetected OnVoiceActivityDetected;

protected:
	/** Process captured audio buffer */
	void ProcessAudioBuffer(const float* AudioData, int32 NumSamples);

	/** Apply voice activity detection */
	bool DetectVoiceActivity(const float* AudioData, int32 NumSamples);

	/** Apply noise suppression */
	void ApplyNoiseSuppression(float* AudioData, int32 NumSamples);

	/** Apply echo cancellation */
	void ApplyEchoCancellation(float* AudioData, int32 NumSamples);

	/** Apply automatic gain control */
	void ApplyAutomaticGainControl(float* AudioData, int32 NumSamples);

	/** Encode audio to Opus format */
	TArray<uint8> EncodeToOpus(const float* AudioData, int32 NumSamples);

	/** Calculate RMS (Root Mean Square) audio level */
	float CalculateAudioLevel(const float* AudioData, int32 NumSamples);

	/** Update capture state */
	void SetCaptureState(EVoiceCaptureState NewState);

	/** Audio capture callback */
	void OnAudioCaptured(const void* AudioData, int32 NumFrames, int32 NumChannels, int32 SampleRate, double StreamTime, bool bOverflow);

private:
	/** Current configuration */
	FNajikaVoiceCaptureConfig Config;

	/** Current capture state */
	EVoiceCaptureState CaptureState;

	/** Audio capture object */
	TSharedPtr<Audio::FAudioCapture> AudioCapture;

	/** Current audio level (0.0 - 1.0) */
	float CurrentAudioLevel;

	/** Is voice currently detected */
	bool bVoiceDetected;

	/** Audio buffer for processing */
	TArray<float> AudioBuffer;

	/** Packet sequence number */
	int32 PacketSequenceNumber;

	/** Timestamp of capture start */
	int64 CaptureStartTime;

	/** VAD threshold (calculated from sensitivity) */
	float VADThreshold;

	/** Noise floor estimate */
	float NoiseFloor;

	/** AGC target level */
	float AGCTargetLevel;

	/** Echo cancellation filter state */
	TArray<float> EchoFilterState;

	/** Selected microphone device index */
	int32 SelectedMicrophoneIndex;
};
