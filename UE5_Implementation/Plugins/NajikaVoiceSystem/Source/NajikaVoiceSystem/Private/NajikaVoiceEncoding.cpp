// Copyright Najika Development Team. All Rights Reserved.

#include "NajikaVoiceEncoding.h"

TArray<uint8> UNajikaVoiceEncoding::EncodeToOpus(const TArray<float>& AudioData, int32 SampleRate, EVoiceQuality Quality)
{
	// Placeholder implementation - convert to PCM16
	// In production, use libopus for actual Opus encoding

	if (AudioData.Num() == 0)
	{
		return TArray<uint8>();
	}

	// For now, just convert to PCM16
	TArray<uint8> EncodedData = FloatToPCM16(AudioData);

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceEncoding: Encoded %d float samples to %d bytes (Opus placeholder)"),
		AudioData.Num(), EncodedData.Num());

	return EncodedData;
}

TArray<float> UNajikaVoiceEncoding::DecodeFromOpus(const TArray<uint8>& OpusData, int32 SampleRate)
{
	// Placeholder implementation - convert from PCM16
	// In production, use libopus for actual Opus decoding

	if (OpusData.Num() == 0)
	{
		return TArray<float>();
	}

	// For now, just convert from PCM16
	TArray<float> DecodedData = PCM16ToFloat(OpusData);

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceEncoding: Decoded %d bytes to %d float samples (Opus placeholder)"),
		OpusData.Num(), DecodedData.Num());

	return DecodedData;
}

TArray<uint8> UNajikaVoiceEncoding::FloatToPCM16(const TArray<float>& AudioData)
{
	TArray<uint8> PCMData;
	PCMData.Reserve(AudioData.Num() * sizeof(int16));

	for (float Sample : AudioData)
	{
		// Clamp and convert to int16
		Sample = FMath::Clamp(Sample, -1.0f, 1.0f);
		int16 PCMSample = (int16)(Sample * 32767.0f);

		// Little-endian encoding
		PCMData.Add((uint8)(PCMSample & 0xFF));
		PCMData.Add((uint8)((PCMSample >> 8) & 0xFF));
	}

	return PCMData;
}

TArray<float> UNajikaVoiceEncoding::PCM16ToFloat(const TArray<uint8>& PCMData)
{
	TArray<float> AudioData;
	int32 NumSamples = PCMData.Num() / sizeof(int16);
	AudioData.Reserve(NumSamples);

	for (int32 i = 0; i < NumSamples; i++)
	{
		int32 ByteIndex = i * 2;

		// Little-endian decoding
		int16 PCMSample = (int16)(PCMData[ByteIndex] | (PCMData[ByteIndex + 1] << 8));

		// Convert to float
		float Sample = (float)PCMSample / 32767.0f;
		AudioData.Add(Sample);
	}

	return AudioData;
}

TArray<float> UNajikaVoiceEncoding::ResampleAudio(const TArray<float>& AudioData, int32 SourceSampleRate, int32 TargetSampleRate)
{
	if (SourceSampleRate == TargetSampleRate)
	{
		return AudioData;
	}

	if (AudioData.Num() == 0 || SourceSampleRate <= 0 || TargetSampleRate <= 0)
	{
		return TArray<float>();
	}

	// Calculate resampling ratio
	float ResampleRatio = (float)TargetSampleRate / (float)SourceSampleRate;
	int32 OutputSize = FMath::CeilToInt(AudioData.Num() * ResampleRatio);

	TArray<float> ResampledData;
	ResampledData.Reserve(OutputSize);

	// Linear interpolation resampling
	for (int32 i = 0; i < OutputSize; i++)
	{
		float SourceIndex = (float)i / ResampleRatio;
		int32 Index1 = FMath::FloorToInt(SourceIndex);
		int32 Index2 = FMath::Min(Index1 + 1, AudioData.Num() - 1);
		float Fraction = SourceIndex - Index1;

		float Sample = FMath::Lerp(AudioData[Index1], AudioData[Index2], Fraction);
		ResampledData.Add(Sample);
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceEncoding: Resampled from %d Hz to %d Hz (%d → %d samples)"),
		SourceSampleRate, TargetSampleRate, AudioData.Num(), ResampledData.Num());

	return ResampledData;
}

TArray<float> UNajikaVoiceEncoding::MonoToStereo(const TArray<float>& MonoData)
{
	TArray<float> StereoData;
	StereoData.Reserve(MonoData.Num() * 2);

	// Duplicate each mono sample to L and R channels
	for (float Sample : MonoData)
	{
		StereoData.Add(Sample); // Left
		StereoData.Add(Sample); // Right
	}

	return StereoData;
}

TArray<float> UNajikaVoiceEncoding::StereoToMono(const TArray<float>& StereoData)
{
	if (StereoData.Num() == 0)
	{
		return TArray<float>();
	}

	TArray<float> MonoData;
	int32 NumFrames = StereoData.Num() / 2;
	MonoData.Reserve(NumFrames);

	// Average L and R channels
	for (int32 i = 0; i < NumFrames; i++)
	{
		float Left = StereoData[i * 2];
		float Right = StereoData[i * 2 + 1];
		float Mono = (Left + Right) * 0.5f;
		MonoData.Add(Mono);
	}

	return MonoData;
}

int32 UNajikaVoiceEncoding::GetBitrateForQuality(EVoiceQuality Quality, int32 NumChannels)
{
	int32 BaseBitrate = 0;

	switch (Quality)
	{
	case EVoiceQuality::Low:
		BaseBitrate = 16000; // 16 kbps
		break;
	case EVoiceQuality::Medium:
		BaseBitrate = 24000; // 24 kbps
		break;
	case EVoiceQuality::High:
		BaseBitrate = 64000; // 64 kbps
		break;
	default:
		BaseBitrate = 24000;
		break;
	}

	// Adjust for channels
	return BaseBitrate * NumChannels;
}

int32 UNajikaVoiceEncoding::GetSampleRateForQuality(EVoiceQuality Quality)
{
	switch (Quality)
	{
	case EVoiceQuality::Low:
		return 8000; // 8 kHz
	case EVoiceQuality::Medium:
		return 16000; // 16 kHz
	case EVoiceQuality::High:
		return 48000; // 48 kHz
	default:
		return 16000;
	}
}
