// Copyright Najika Development Team. All Rights Reserved.

#include "NajikaVoicePlayback.h"
#include "Components/AudioComponent.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"

UNajikaVoicePlayback::UNajikaVoicePlayback()
	: SampleRate(48000)
	, NumChannels(1)
	, PlaybackVolume(1.0f)
	, bIsPlaying(false)
	, JitterBufferSizeMs(100)
	, ExpectedSequenceNumber(0)
	, LastPacketTimestamp(0)
	, SoundWave(nullptr)
	, AudioComponent(nullptr)
	, bSpatialAudioEnabled(false)
	, SpatialLocation(FVector::ZeroVector)
{
}

bool UNajikaVoicePlayback::Initialize(int32 InSampleRate, int32 InNumChannels)
{
	SampleRate = InSampleRate;
	NumChannels = InNumChannels;

	// Create procedural sound wave
	SoundWave = NewObject<USoundWaveProcedural>(this);
	if (!SoundWave)
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoicePlayback: Failed to create SoundWaveProcedural"));
		return false;
	}

	SoundWave->SetSampleRate(SampleRate);
	SoundWave->NumChannels = NumChannels;
	SoundWave->Duration = INDEFINITELY_LOOPING_DURATION;
	SoundWave->SoundGroup = SOUNDGROUP_Voice;
	SoundWave->bLooping = false;

	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Initialized (SampleRate: %d, Channels: %d)"),
		SampleRate, NumChannels);

	return true;
}

void UNajikaVoicePlayback::QueueAudioPacket(const FNajikaAudioPacket& Packet)
{
	FScopeLock Lock(&PacketQueueLock);

	// Add to queue sorted by sequence number
	int32 InsertIndex = PacketQueue.Num();

	for (int32 i = 0; i < PacketQueue.Num(); i++)
	{
		if (PacketQueue[i].SequenceNumber > Packet.SequenceNumber)
		{
			InsertIndex = i;
			break;
		}
	}

	PacketQueue.Insert(Packet, InsertIndex);

	// Limit queue size to prevent memory overflow
	const int32 MaxQueueSize = 100;
	if (PacketQueue.Num() > MaxQueueSize)
	{
		// Remove oldest packets
		PacketQueue.RemoveAt(0, PacketQueue.Num() - MaxQueueSize);
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoicePlayback: Queue overflow, removed old packets"));
	}

	// Auto-start playback if buffer is filled
	if (!bIsPlaying && PacketQueue.Num() >= (JitterBufferSizeMs / 20))
	{
		StartPlayback();
	}
}

void UNajikaVoicePlayback::StartPlayback()
{
	if (bIsPlaying)
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoicePlayback: Already playing"));
		return;
	}

	if (!SoundWave)
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoicePlayback: SoundWave not initialized"));
		return;
	}

	// Create audio component if needed
	if (!AudioComponent)
	{
		UWorld* World = GetWorld();
		if (!World)
		{
			UE_LOG(LogTemp, Error, TEXT("NajikaVoicePlayback: No world context"));
			return;
		}

		AudioComponent = UGameplayStatics::SpawnSound2D(World, SoundWave, PlaybackVolume, 1.0f, 0.0f, nullptr, false, false);

		if (!AudioComponent)
		{
			UE_LOG(LogTemp, Error, TEXT("NajikaVoicePlayback: Failed to create AudioComponent"));
			return;
		}

		AudioComponent->bIsUISound = true;
		AudioComponent->bAutoDestroy = false;
	}

	// Configure spatial audio
	if (bSpatialAudioEnabled)
	{
		AudioComponent->SetWorldLocation(SpatialLocation);
		AudioComponent->bAllowSpatialization = true;
	}
	else
	{
		AudioComponent->bAllowSpatialization = false;
	}

	AudioComponent->Play();

	bIsPlaying = true;
	ExpectedSequenceNumber = 0;

	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Started playback"));

	// Start feeding audio data
	if (SoundWave)
	{
		// Queue initial buffer
		FNajikaAudioPacket Packet;
		while (GetNextPacket(Packet))
		{
			TArray<float> DecodedAudio = DecodeOpusPacket(Packet.AudioData);
			ProcessAudioForPlayback(DecodedAudio);

			// Convert float to int16
			TArray<uint8> PCMData;
			PCMData.Reserve(DecodedAudio.Num() * sizeof(int16));

			for (float Sample : DecodedAudio)
			{
				int16 PCMSample = (int16)(FMath::Clamp(Sample, -1.0f, 1.0f) * 32767.0f);
				PCMData.Add((uint8)(PCMSample & 0xFF));
				PCMData.Add((uint8)((PCMSample >> 8) & 0xFF));
			}

			SoundWave->QueueAudio(PCMData.GetData(), PCMData.Num());
		}
	}
}

void UNajikaVoicePlayback::StopPlayback()
{
	if (!bIsPlaying)
	{
		return;
	}

	if (AudioComponent && AudioComponent->IsPlaying())
	{
		AudioComponent->Stop();
	}

	if (SoundWave)
	{
		SoundWave->ResetAudio();
	}

	ClearBuffer();

	bIsPlaying = false;
	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Stopped playback"));
}

void UNajikaVoicePlayback::PausePlayback()
{
	if (!bIsPlaying)
	{
		return;
	}

	if (AudioComponent && AudioComponent->IsPlaying())
	{
		AudioComponent->SetPaused(true);
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Paused"));
}

void UNajikaVoicePlayback::ResumePlayback()
{
	if (!bIsPlaying)
	{
		return;
	}

	if (AudioComponent)
	{
		AudioComponent->SetPaused(false);
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Resumed"));
}

void UNajikaVoicePlayback::SetVolume(float Volume)
{
	PlaybackVolume = FMath::Clamp(Volume, 0.0f, 1.0f);

	if (AudioComponent)
	{
		AudioComponent->SetVolumeMultiplier(PlaybackVolume);
	}
}

void UNajikaVoicePlayback::SetJitterBufferSize(int32 BufferSizeMs)
{
	JitterBufferSizeMs = FMath::Clamp(BufferSizeMs, 20, 500);
	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Jitter buffer set to %d ms"), JitterBufferSizeMs);
}

void UNajikaVoicePlayback::ClearBuffer()
{
	FScopeLock Lock(&PacketQueueLock);
	PacketQueue.Empty();
	ExpectedSequenceNumber = 0;
}

void UNajikaVoicePlayback::SetSpatialAudio(bool bEnable, FVector Location)
{
	bSpatialAudioEnabled = bEnable;
	SpatialLocation = Location;

	if (AudioComponent)
	{
		if (bSpatialAudioEnabled)
		{
			AudioComponent->SetWorldLocation(SpatialLocation);
			AudioComponent->bAllowSpatialization = true;
		}
		else
		{
			AudioComponent->bAllowSpatialization = false;
		}
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Spatial audio %s"), bEnable ? TEXT("enabled") : TEXT("disabled"));
}

void UNajikaVoicePlayback::UpdateSpatialLocation(FVector Location)
{
	SpatialLocation = Location;

	if (AudioComponent && bSpatialAudioEnabled)
	{
		AudioComponent->SetWorldLocation(SpatialLocation);
	}
}

void UNajikaVoicePlayback::Shutdown()
{
	StopPlayback();

	if (AudioComponent)
	{
		AudioComponent->DestroyComponent();
		AudioComponent = nullptr;
	}

	SoundWave = nullptr;

	UE_LOG(LogTemp, Log, TEXT("NajikaVoicePlayback: Shutdown"));
}

TArray<float> UNajikaVoicePlayback::DecodeOpusPacket(const TArray<uint8>& EncodedData)
{
	// Placeholder for Opus decoding
	// In production, use libopus library
	// For now, convert int16 PCM back to float

	TArray<float> DecodedAudio;
	int32 NumSamples = EncodedData.Num() / sizeof(int16);
	DecodedAudio.Reserve(NumSamples);

	for (int32 i = 0; i < NumSamples; i++)
	{
		int32 ByteIndex = i * 2;
		int16 Sample = (int16)(EncodedData[ByteIndex] | (EncodedData[ByteIndex + 1] << 8));
		float FloatSample = (float)Sample / 32767.0f;
		DecodedAudio.Add(FloatSample);
	}

	return DecodedAudio;
}

void UNajikaVoicePlayback::ConcealPacketLoss(TArray<float>& AudioData)
{
	// Simple packet loss concealment - repeat last packet
	// In production, use more sophisticated PLC algorithms

	if (AudioData.Num() == 0)
	{
		// Generate silence
		AudioData.SetNumZeroed(SampleRate / 50); // 20ms of silence
	}
}

void UNajikaVoicePlayback::ProcessAudioForPlayback(TArray<float>& AudioData)
{
	// Apply volume
	if (PlaybackVolume != 1.0f)
	{
		for (float& Sample : AudioData)
		{
			Sample *= PlaybackVolume;
		}
	}

	// Clamp samples
	for (float& Sample : AudioData)
	{
		Sample = FMath::Clamp(Sample, -1.0f, 1.0f);
	}
}

bool UNajikaVoicePlayback::GetNextPacket(FNajikaAudioPacket& OutPacket)
{
	FScopeLock Lock(&PacketQueueLock);

	if (PacketQueue.Num() == 0)
	{
		return false;
	}

	// Find packet with expected sequence number
	for (int32 i = 0; i < PacketQueue.Num(); i++)
	{
		if (PacketQueue[i].SequenceNumber == ExpectedSequenceNumber)
		{
			OutPacket = PacketQueue[i];
			PacketQueue.RemoveAt(i);
			ExpectedSequenceNumber++;
			return true;
		}
	}

	// If expected packet not found, check for packet loss
	if (PacketQueue[0].SequenceNumber > ExpectedSequenceNumber)
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoicePlayback: Packet loss detected (expected %d, got %d)"),
			ExpectedSequenceNumber, PacketQueue[0].SequenceNumber);

		// Skip to next available packet
		OutPacket = PacketQueue[0];
		ExpectedSequenceNumber = OutPacket.SequenceNumber + 1;
		PacketQueue.RemoveAt(0);

		// Apply packet loss concealment
		TArray<float> DecodedAudio = DecodeOpusPacket(OutPacket.AudioData);
		ConcealPacketLoss(DecodedAudio);

		return true;
	}

	return false;
}
