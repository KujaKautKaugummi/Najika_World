// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "AudioMixerDevice.h"
#include "Sound/SoundWaveProcedural.h"
#include "NajikaVoiceTypes.h"
#include "NajikaVoicePlayback.generated.h"

/**
 * Handles audio playback for received voice data
 * Features:
 * - Real-time audio playback
 * - Jitter buffer for network delay compensation
 * - Packet loss concealment
 * - Opus decoding
 * - 3D spatial audio support
 */
UCLASS(BlueprintType)
class NAJIKAVOICESYSTEM_API UNajikaVoicePlayback : public UObject
{
	GENERATED_BODY()

public:
	UNajikaVoicePlayback();

	/**
	 * Initialize the playback system
	 * @param SampleRate Audio sample rate (Hz)
	 * @param NumChannels Number of audio channels (1 = Mono, 2 = Stereo)
	 * @return True if initialization successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	bool Initialize(int32 SampleRate = 48000, int32 NumChannels = 1);

	/**
	 * Queue audio packet for playback
	 * @param Packet Audio packet to play
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void QueueAudioPacket(const FNajikaAudioPacket& Packet);

	/**
	 * Start audio playback
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void StartPlayback();

	/**
	 * Stop audio playback
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void StopPlayback();

	/**
	 * Pause audio playback
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void PausePlayback();

	/**
	 * Resume paused playback
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void ResumePlayback();

	/**
	 * Check if currently playing
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	bool IsPlaying() const { return bIsPlaying; }

	/**
	 * Set playback volume (0.0 - 1.0)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetVolume(float Volume);

	/**
	 * Get current playback volume
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	float GetVolume() const { return PlaybackVolume; }

	/**
	 * Set jitter buffer size (in milliseconds)
	 * Larger buffer = more delay but better quality
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetJitterBufferSize(int32 BufferSizeMs);

	/**
	 * Get current jitter buffer size
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	int32 GetJitterBufferSize() const { return JitterBufferSizeMs; }

	/**
	 * Clear all queued audio packets
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void ClearBuffer();

	/**
	 * Get number of packets currently in buffer
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice")
	int32 GetBufferedPacketCount() const { return PacketQueue.Num(); }

	/**
	 * Enable/disable 3D spatial audio
	 * @param bEnable Enable spatial audio
	 * @param Location 3D position of audio source
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void SetSpatialAudio(bool bEnable, FVector Location = FVector::ZeroVector);

	/**
	 * Update 3D audio source location
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void UpdateSpatialLocation(FVector Location);

	/**
	 * Shutdown and release resources
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice")
	void Shutdown();

protected:
	/** Decode Opus audio packet */
	TArray<float> DecodeOpusPacket(const TArray<uint8>& EncodedData);

	/** Handle packet loss by concealing missing data */
	void ConcealPacketLoss(TArray<float>& AudioData);

	/** Process audio before playback */
	void ProcessAudioForPlayback(TArray<float>& AudioData);

	/** Get next packet from jitter buffer */
	bool GetNextPacket(FNajikaAudioPacket& OutPacket);

private:
	/** Sample rate (Hz) */
	int32 SampleRate;

	/** Number of channels */
	int32 NumChannels;

	/** Playback volume (0.0 - 1.0) */
	float PlaybackVolume;

	/** Is currently playing */
	bool bIsPlaying;

	/** Jitter buffer size (milliseconds) */
	int32 JitterBufferSizeMs;

	/** Packet queue (jitter buffer) */
	TArray<FNajikaAudioPacket> PacketQueue;

	/** Expected next sequence number */
	int32 ExpectedSequenceNumber;

	/** Last played packet timestamp */
	int64 LastPacketTimestamp;

	/** Procedural sound wave for dynamic audio */
	UPROPERTY()
	USoundWaveProcedural* SoundWave;

	/** Audio component for playback */
	UPROPERTY()
	UAudioComponent* AudioComponent;

	/** 3D spatial audio enabled */
	bool bSpatialAudioEnabled;

	/** 3D audio source location */
	FVector SpatialLocation;

	/** Critical section for thread-safe packet queue access */
	FCriticalSection PacketQueueLock;
};
