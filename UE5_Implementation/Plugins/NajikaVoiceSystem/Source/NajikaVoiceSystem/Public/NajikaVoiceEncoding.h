// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "NajikaVoiceTypes.h"
#include "NajikaVoiceEncoding.generated.h"

/**
 * Audio encoding/decoding utility functions
 * Provides conversion between different audio formats
 */
UCLASS()
class NAJIKAVOICESYSTEM_API UNajikaVoiceEncoding : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/**
	 * Encode float audio samples to Opus format
	 * @param AudioData Float samples (-1.0 to 1.0)
	 * @param SampleRate Sample rate (Hz)
	 * @param Quality Encoding quality
	 * @return Encoded Opus data
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|Encoding")
	static TArray<uint8> EncodeToOpus(const TArray<float>& AudioData, int32 SampleRate, EVoiceQuality Quality);

	/**
	 * Decode Opus audio data to float samples
	 * @param OpusData Encoded Opus data
	 * @param SampleRate Sample rate (Hz)
	 * @return Decoded float samples
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|Encoding")
	static TArray<float> DecodeFromOpus(const TArray<uint8>& OpusData, int32 SampleRate);

	/**
	 * Convert float samples to 16-bit PCM
	 * @param AudioData Float samples (-1.0 to 1.0)
	 * @return PCM data (int16 as bytes)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|Encoding")
	static TArray<uint8> FloatToPCM16(const TArray<float>& AudioData);

	/**
	 * Convert 16-bit PCM to float samples
	 * @param PCMData PCM data (int16 as bytes)
	 * @return Float samples
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|Encoding")
	static TArray<float> PCM16ToFloat(const TArray<uint8>& PCMData);

	/**
	 * Resample audio data
	 * @param AudioData Input audio samples
	 * @param SourceSampleRate Input sample rate
	 * @param TargetSampleRate Output sample rate
	 * @return Resampled audio
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|Encoding")
	static TArray<float> ResampleAudio(const TArray<float>& AudioData, int32 SourceSampleRate, int32 TargetSampleRate);

	/**
	 * Convert mono to stereo
	 * @param MonoData Mono audio samples
	 * @return Stereo audio (interleaved L/R)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|Encoding")
	static TArray<float> MonoToStereo(const TArray<float>& MonoData);

	/**
	 * Convert stereo to mono
	 * @param StereoData Stereo audio (interleaved L/R)
	 * @return Mono audio (averaged)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Voice|Encoding")
	static TArray<float> StereoToMono(const TArray<float>& StereoData);

	/**
	 * Calculate optimal bitrate for quality setting
	 * @param Quality Voice quality preset
	 * @param NumChannels Number of audio channels
	 * @return Bitrate in bits/second
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice|Encoding")
	static int32 GetBitrateForQuality(EVoiceQuality Quality, int32 NumChannels = 1);

	/**
	 * Get sample rate for quality setting
	 * @param Quality Voice quality preset
	 * @return Sample rate in Hz
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Voice|Encoding")
	static int32 GetSampleRateForQuality(EVoiceQuality Quality);
};
