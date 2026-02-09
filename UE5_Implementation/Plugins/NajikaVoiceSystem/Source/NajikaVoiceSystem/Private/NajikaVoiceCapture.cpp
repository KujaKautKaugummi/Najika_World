// Copyright Najika Development Team. All Rights Reserved.

#include "NajikaVoiceCapture.h"
#include "AudioDevice.h"
#include "Engine/Engine.h"
#include "HAL/PlatformTime.h"
#include "Misc/DateTime.h"

UNajikaVoiceCapture::UNajikaVoiceCapture()
	: CaptureState(EVoiceCaptureState::Stopped)
	, CurrentAudioLevel(0.0f)
	, bVoiceDetected(false)
	, PacketSequenceNumber(0)
	, CaptureStartTime(0)
	, VADThreshold(0.02f)
	, NoiseFloor(0.01f)
	, AGCTargetLevel(0.5f)
	, SelectedMicrophoneIndex(0)
{
}

bool UNajikaVoiceCapture::Initialize(const FNajikaVoiceCaptureConfig& InConfig)
{
	Config = InConfig;

	// Calculate VAD threshold based on sensitivity
	switch (Config.VADSensitivity)
	{
	case EVADSensitivity::Low:
		VADThreshold = 0.05f;
		break;
	case EVADSensitivity::Medium:
		VADThreshold = 0.02f;
		break;
	case EVADSensitivity::High:
		VADThreshold = 0.01f;
		break;
	}

	// Create audio capture object
	AudioCapture = MakeShared<Audio::FAudioCapture>();

	if (!AudioCapture.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceCapture: Failed to create AudioCapture"));
		SetCaptureState(EVoiceCaptureState::Error);
		return false;
	}

	// Open default audio capture device
	Audio::FAudioCaptureDeviceParams Params;
	Params.DeviceIndex = SelectedMicrophoneIndex;

	if (!AudioCapture->OpenAudioCaptureStream(Params))
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceCapture: Failed to open audio capture stream"));
		SetCaptureState(EVoiceCaptureState::Error);
		return false;
	}

	// Reserve buffer space
	AudioBuffer.Reserve(Config.BufferSize * Config.NumChannels);

	SetCaptureState(EVoiceCaptureState::Stopped);
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Initialized successfully (SampleRate: %d, BufferSize: %d)"),
		Config.SampleRate, Config.BufferSize);

	return true;
}

bool UNajikaVoiceCapture::StartCapture()
{
	if (CaptureState == EVoiceCaptureState::Capturing)
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoiceCapture: Already capturing"));
		return true;
	}

	if (!AudioCapture.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceCapture: Not initialized"));
		return false;
	}

	SetCaptureState(EVoiceCaptureState::Starting);

	// Set audio callback
	AudioCapture->OnAudioCapture = [this](const void* AudioData, int32 NumFrames, int32 NumChannels, int32 SampleRate, double StreamTime, bool bOverflow)
	{
		OnAudioCaptured(AudioData, NumFrames, NumChannels, SampleRate, StreamTime, bOverflow);
	};

	// Start the stream
	if (!AudioCapture->StartCapturingAudio())
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceCapture: Failed to start capturing"));
		SetCaptureState(EVoiceCaptureState::Error);
		return false;
	}

	CaptureStartTime = FDateTime::Now().ToUnixTimestamp() * 1000; // milliseconds
	PacketSequenceNumber = 0;

	SetCaptureState(EVoiceCaptureState::Capturing);
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Started capturing"));

	return true;
}

void UNajikaVoiceCapture::StopCapture()
{
	if (CaptureState == EVoiceCaptureState::Stopped)
	{
		return;
	}

	if (AudioCapture.IsValid())
	{
		AudioCapture->StopCapturingAudio();
	}

	bVoiceDetected = false;
	CurrentAudioLevel = 0.0f;

	SetCaptureState(EVoiceCaptureState::Stopped);
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Stopped capturing"));
}

void UNajikaVoiceCapture::PauseCapture()
{
	if (CaptureState != EVoiceCaptureState::Capturing)
	{
		return;
	}

	if (AudioCapture.IsValid())
	{
		AudioCapture->StopCapturingAudio();
	}

	SetCaptureState(EVoiceCaptureState::Paused);
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Paused"));
}

void UNajikaVoiceCapture::ResumeCapture()
{
	if (CaptureState != EVoiceCaptureState::Paused)
	{
		return;
	}

	if (AudioCapture.IsValid() && AudioCapture->StartCapturingAudio())
	{
		SetCaptureState(EVoiceCaptureState::Capturing);
		UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Resumed"));
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceCapture: Failed to resume"));
		SetCaptureState(EVoiceCaptureState::Error);
	}
}

void UNajikaVoiceCapture::UpdateConfiguration(const FNajikaVoiceCaptureConfig& NewConfig)
{
	bool bWasCapturing = (CaptureState == EVoiceCaptureState::Capturing);

	if (bWasCapturing)
	{
		StopCapture();
	}

	Config = NewConfig;

	// Update VAD threshold
	switch (Config.VADSensitivity)
	{
	case EVADSensitivity::Low:
		VADThreshold = 0.05f;
		break;
	case EVADSensitivity::Medium:
		VADThreshold = 0.02f;
		break;
	case EVADSensitivity::High:
		VADThreshold = 0.01f;
		break;
	}

	if (bWasCapturing)
	{
		StartCapture();
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Configuration updated"));
}

void UNajikaVoiceCapture::SetInputGain(float Gain)
{
	Config.InputGain = FMath::Clamp(Gain, 0.0f, 2.0f);
}

void UNajikaVoiceCapture::SetVADEnabled(bool bEnabled)
{
	Config.bEnableVAD = bEnabled;
}

void UNajikaVoiceCapture::SetVADSensitivity(EVADSensitivity Sensitivity)
{
	Config.VADSensitivity = Sensitivity;

	switch (Sensitivity)
	{
	case EVADSensitivity::Low:
		VADThreshold = 0.05f;
		break;
	case EVADSensitivity::Medium:
		VADThreshold = 0.02f;
		break;
	case EVADSensitivity::High:
		VADThreshold = 0.01f;
		break;
	}
}

void UNajikaVoiceCapture::SetNoiseSuppressionEnabled(bool bEnabled)
{
	Config.bEnableNoiseSuppression = bEnabled;
}

void UNajikaVoiceCapture::SetEchoCancellationEnabled(bool bEnabled)
{
	Config.bEnableEchoCancellation = bEnabled;
}

TArray<FString> UNajikaVoiceCapture::GetAvailableMicrophones()
{
	TArray<FString> DeviceNames;

	if (AudioCapture.IsValid())
	{
		TArray<Audio::FCaptureDeviceInfo> DeviceInfos;
		AudioCapture->GetCaptureDevicesAvailable(DeviceInfos);

		for (const Audio::FCaptureDeviceInfo& Info : DeviceInfos)
		{
			DeviceNames.Add(Info.DeviceName);
		}
	}

	return DeviceNames;
}

bool UNajikaVoiceCapture::SelectMicrophone(int32 DeviceIndex)
{
	bool bWasCapturing = (CaptureState == EVoiceCaptureState::Capturing);

	if (bWasCapturing)
	{
		StopCapture();
	}

	SelectedMicrophoneIndex = DeviceIndex;

	if (AudioCapture.IsValid())
	{
		AudioCapture->CloseAudioCaptureStream();

		Audio::FAudioCaptureDeviceParams Params;
		Params.DeviceIndex = DeviceIndex;

		if (!AudioCapture->OpenAudioCaptureStream(Params))
		{
			UE_LOG(LogTemp, Error, TEXT("NajikaVoiceCapture: Failed to open device %d"), DeviceIndex);
			return false;
		}
	}

	if (bWasCapturing)
	{
		StartCapture();
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Selected microphone %d"), DeviceIndex);
	return true;
}

void UNajikaVoiceCapture::Shutdown()
{
	StopCapture();

	if (AudioCapture.IsValid())
	{
		AudioCapture->CloseAudioCaptureStream();
		AudioCapture.Reset();
	}

	AudioBuffer.Empty();
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceCapture: Shutdown"));
}

void UNajikaVoiceCapture::ProcessAudioBuffer(const float* AudioData, int32 NumSamples)
{
	if (NumSamples == 0)
	{
		return;
	}

	// Copy to working buffer
	TArray<float> WorkingBuffer;
	WorkingBuffer.SetNumUninitialized(NumSamples);
	FMemory::Memcpy(WorkingBuffer.GetData(), AudioData, NumSamples * sizeof(float));

	// Apply input gain
	if (Config.InputGain != 1.0f)
	{
		for (int32 i = 0; i < NumSamples; i++)
		{
			WorkingBuffer[i] *= Config.InputGain;
		}
	}

	// Apply noise suppression
	if (Config.bEnableNoiseSuppression)
	{
		ApplyNoiseSuppression(WorkingBuffer.GetData(), NumSamples);
	}

	// Apply echo cancellation
	if (Config.bEnableEchoCancellation)
	{
		ApplyEchoCancellation(WorkingBuffer.GetData(), NumSamples);
	}

	// Apply automatic gain control
	if (Config.bEnableAGC)
	{
		ApplyAutomaticGainControl(WorkingBuffer.GetData(), NumSamples);
	}

	// Calculate audio level
	CurrentAudioLevel = CalculateAudioLevel(WorkingBuffer.GetData(), NumSamples);

	// Voice activity detection
	bool bVoiceDetectedNow = false;
	if (Config.bEnableVAD)
	{
		bVoiceDetectedNow = DetectVoiceActivity(WorkingBuffer.GetData(), NumSamples);
	}
	else
	{
		bVoiceDetectedNow = true; // Always send if VAD disabled
	}

	// Update voice detection state
	if (bVoiceDetectedNow != bVoiceDetected)
	{
		bVoiceDetected = bVoiceDetectedNow;
		OnVoiceActivityDetected.Broadcast(bVoiceDetected);
	}

	// Only encode and send if voice detected or VAD disabled
	if (bVoiceDetectedNow)
	{
		// Encode to Opus
		TArray<uint8> EncodedData = EncodeToOpus(WorkingBuffer.GetData(), NumSamples);

		// Create packet
		FNajikaAudioPacket Packet;
		Packet.AudioData = EncodedData;
		Packet.SequenceNumber = PacketSequenceNumber++;
		Packet.Timestamp = FDateTime::Now().ToUnixTimestamp() * 1000;
		Packet.SampleRate = Config.SampleRate;
		Packet.NumChannels = Config.NumChannels;
		Packet.EncodingFormat = EVoiceEncodingFormat::Opus;
		Packet.bContainsVoice = bVoiceDetectedNow;

		// Broadcast packet
		OnAudioPacketReady.Broadcast(Packet);
	}
}

bool UNajikaVoiceCapture::DetectVoiceActivity(const float* AudioData, int32 NumSamples)
{
	// Simple energy-based VAD
	float Energy = 0.0f;

	for (int32 i = 0; i < NumSamples; i++)
	{
		Energy += AudioData[i] * AudioData[i];
	}

	Energy /= NumSamples;
	Energy = FMath::Sqrt(Energy); // RMS

	// Update noise floor estimate (simple exponential moving average)
	if (Energy < NoiseFloor)
	{
		NoiseFloor = NoiseFloor * 0.99f + Energy * 0.01f;
	}

	// Voice detected if energy is above threshold + noise floor
	return (Energy > (NoiseFloor + VADThreshold));
}

void UNajikaVoiceCapture::ApplyNoiseSuppression(float* AudioData, int32 NumSamples)
{
	// Simple noise gate - zero out samples below noise floor
	for (int32 i = 0; i < NumSamples; i++)
	{
		if (FMath::Abs(AudioData[i]) < NoiseFloor)
		{
			AudioData[i] = 0.0f;
		}
	}
}

void UNajikaVoiceCapture::ApplyEchoCancellation(float* AudioData, int32 NumSamples)
{
	// Placeholder for echo cancellation
	// In production, use WebRTC AEC or similar library
	// For now, apply simple high-pass filter to reduce low-frequency echo

	if (EchoFilterState.Num() == 0)
	{
		EchoFilterState.SetNumZeroed(2);
	}

	const float Alpha = 0.9f; // High-pass filter coefficient

	for (int32 i = 0; i < NumSamples; i++)
	{
		float Output = AudioData[i] - EchoFilterState[0] + Alpha * EchoFilterState[1];
		EchoFilterState[0] = AudioData[i];
		EchoFilterState[1] = Output;
		AudioData[i] = Output;
	}
}

void UNajikaVoiceCapture::ApplyAutomaticGainControl(float* AudioData, int32 NumSamples)
{
	// Simple AGC - normalize to target level
	float MaxAmplitude = 0.0f;

	for (int32 i = 0; i < NumSamples; i++)
	{
		MaxAmplitude = FMath::Max(MaxAmplitude, FMath::Abs(AudioData[i]));
	}

	if (MaxAmplitude > 0.0f && MaxAmplitude < AGCTargetLevel)
	{
		float Gain = AGCTargetLevel / MaxAmplitude;
		Gain = FMath::Min(Gain, 2.0f); // Limit gain to prevent over-amplification

		for (int32 i = 0; i < NumSamples; i++)
		{
			AudioData[i] *= Gain;
		}
	}
}

TArray<uint8> UNajikaVoiceCapture::EncodeToOpus(const float* AudioData, int32 NumSamples)
{
	// Placeholder for Opus encoding
	// In production, use libopus library
	// For now, convert float to int16 PCM

	TArray<uint8> EncodedData;
	EncodedData.Reserve(NumSamples * sizeof(int16));

	for (int32 i = 0; i < NumSamples; i++)
	{
		int16 Sample = (int16)(FMath::Clamp(AudioData[i], -1.0f, 1.0f) * 32767.0f);
		EncodedData.Add((uint8)(Sample & 0xFF));
		EncodedData.Add((uint8)((Sample >> 8) & 0xFF));
	}

	return EncodedData;
}

float UNajikaVoiceCapture::CalculateAudioLevel(const float* AudioData, int32 NumSamples)
{
	if (NumSamples == 0)
	{
		return 0.0f;
	}

	// Calculate RMS level
	float Sum = 0.0f;

	for (int32 i = 0; i < NumSamples; i++)
	{
		Sum += AudioData[i] * AudioData[i];
	}

	return FMath::Sqrt(Sum / NumSamples);
}

void UNajikaVoiceCapture::SetCaptureState(EVoiceCaptureState NewState)
{
	if (CaptureState != NewState)
	{
		CaptureState = NewState;
		OnCaptureStateChanged.Broadcast(NewState);
	}
}

void UNajikaVoiceCapture::OnAudioCaptured(const void* AudioData, int32 NumFrames, int32 NumChannels, int32 SampleRate, double StreamTime, bool bOverflow)
{
	if (bOverflow)
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoiceCapture: Audio buffer overflow"));
	}

	// Convert to float array
	const float* FloatData = static_cast<const float*>(AudioData);
	int32 NumSamples = NumFrames * NumChannels;

	ProcessAudioBuffer(FloatData, NumSamples);
}
