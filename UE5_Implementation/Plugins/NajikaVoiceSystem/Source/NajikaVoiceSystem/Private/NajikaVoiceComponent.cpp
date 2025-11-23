// Copyright Najika Development Team. All Rights Reserved.

#include "NajikaVoiceComponent.h"
#include "Engine/World.h"
#include "TimerManager.h"

UNajikaVoiceComponent::UNajikaVoiceComponent()
	: VoiceCapture(nullptr)
	, VoicePlayback(nullptr)
	, WhisperClient(nullptr)
	, CallState(EVoiceCallState::Idle)
	, bPushToTalkActive(false)
	, bMicrophoneMuted(false)
	, bPlaybackMuted(false)
	, CallStartTime(0.0f)
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.TickInterval = 0.1f; // Update stats every 100ms
}

void UNajikaVoiceComponent::BeginPlay()
{
	Super::BeginPlay();

	if (bAutoInitialize)
	{
		Initialize(BackendURL, CaptureConfig);
	}
}

void UNajikaVoiceComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsInCall())
	{
		StopVoiceCall();
	}

	if (VoiceCapture)
	{
		VoiceCapture->Shutdown();
	}

	if (VoicePlayback)
	{
		VoicePlayback->Shutdown();
	}

	Super::EndPlay(EndPlayReason);
}

void UNajikaVoiceComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	if (IsInCall())
	{
		UpdateCallStats(DeltaTime);
	}
}

bool UNajikaVoiceComponent::Initialize(const FString& InBackendURL, const FNajikaVoiceCaptureConfig& Config)
{
	BackendURL = InBackendURL;
	CaptureConfig = Config;

	// Create voice capture
	VoiceCapture = NewObject<UNajikaVoiceCapture>(this);
	if (!VoiceCapture || !VoiceCapture->Initialize(CaptureConfig))
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceComponent: Failed to initialize voice capture"));
		return false;
	}

	// Bind delegates
	VoiceCapture->OnAudioPacketReady.AddDynamic(this, &UNajikaVoiceComponent::OnAudioPacketReady);
	VoiceCapture->OnVoiceActivityDetected.AddDynamic(this, &UNajikaVoiceComponent::OnVoiceDetected);

	// Create voice playback
	VoicePlayback = NewObject<UNajikaVoicePlayback>(this);
	if (!VoicePlayback || !VoicePlayback->Initialize(CaptureConfig.SampleRate, CaptureConfig.NumChannels))
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceComponent: Failed to initialize voice playback"));
		return false;
	}

	// Create Whisper client
	WhisperClient = NewObject<UNajikaWhisperClient>(this);
	if (!WhisperClient || !WhisperClient->Initialize(BackendURL))
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceComponent: Failed to initialize Whisper client"));
		return false;
	}

	// Bind Whisper delegate
	WhisperClient->OnTranscriptionComplete.AddDynamic(this, &UNajikaVoiceComponent::OnWhisperTranscriptionComplete);

	SetCallState(EVoiceCallState::Idle);

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Initialized successfully"));
	return true;
}

void UNajikaVoiceComponent::StartVoiceCall()
{
	if (IsInCall())
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoiceComponent: Already in call"));
		return;
	}

	if (!VoiceCapture || !VoicePlayback)
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaVoiceComponent: Not initialized"));
		return;
	}

	SetCallState(EVoiceCallState::Connecting);

	// Start playback first (for incoming audio)
	VoicePlayback->StartPlayback();

	// Start capture based on mode
	if (bUsePushToTalk)
	{
		// In push-to-talk mode, wait for user to press button
		UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Push-to-talk mode - press button to talk"));
	}
	else
	{
		// In VAD mode, start capture immediately
		VoiceCapture->StartCapture();
	}

	// Reset stats
	CallStats = FNajikaVoiceCallStats();
	CallStartTime = GetWorld()->GetTimeSeconds();

	SetCallState(EVoiceCallState::InCall);
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Voice call started"));
}

void UNajikaVoiceComponent::StopVoiceCall()
{
	if (!IsInCall())
	{
		return;
	}

	SetCallState(EVoiceCallState::Disconnecting);

	if (VoiceCapture)
	{
		VoiceCapture->StopCapture();
	}

	if (VoicePlayback)
	{
		VoicePlayback->StopPlayback();
	}

	bPushToTalkActive = false;

	SetCallState(EVoiceCallState::Idle);
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Voice call stopped"));
}

void UNajikaVoiceComponent::StartPushToTalk()
{
	if (!IsInCall() || !bUsePushToTalk)
	{
		return;
	}

	if (bMicrophoneMuted)
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoiceComponent: Microphone is muted"));
		return;
	}

	if (!bPushToTalkActive && VoiceCapture)
	{
		VoiceCapture->StartCapture();
		bPushToTalkActive = true;
		UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Push-to-talk started"));
	}
}

void UNajikaVoiceComponent::StopPushToTalk()
{
	if (!IsInCall() || !bUsePushToTalk)
	{
		return;
	}

	if (bPushToTalkActive && VoiceCapture)
	{
		VoiceCapture->StopCapture();
		bPushToTalkActive = false;
		UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Push-to-talk stopped"));
	}
}

void UNajikaVoiceComponent::SetVADMode(bool bEnabled)
{
	bUsePushToTalk = !bEnabled;

	if (VoiceCapture)
	{
		VoiceCapture->SetVADEnabled(bEnabled);
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: VAD mode %s"), bEnabled ? TEXT("enabled") : TEXT("disabled"));
}

void UNajikaVoiceComponent::SetMicrophoneGain(float Gain)
{
	if (VoiceCapture)
	{
		VoiceCapture->SetInputGain(Gain);
	}
}

void UNajikaVoiceComponent::SetPlaybackVolume(float Volume)
{
	if (VoicePlayback)
	{
		VoicePlayback->SetVolume(Volume);
	}
}

float UNajikaVoiceComponent::GetInputLevel() const
{
	if (VoiceCapture)
	{
		return VoiceCapture->GetCurrentAudioLevel();
	}
	return 0.0f;
}

void UNajikaVoiceComponent::SetAutoTranscribeEnabled(bool bEnabled)
{
	bAutoTranscribe = bEnabled;
	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Auto-transcribe %s"), bEnabled ? TEXT("enabled") : TEXT("disabled"));
}

void UNajikaVoiceComponent::TranscribeLastAudio()
{
	if (WhisperClient && LastAudioPacket.AudioData.Num() > 0)
	{
		WhisperClient->TranscribePacket(LastAudioPacket);
		UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Transcribing last audio packet"));
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaVoiceComponent: No audio to transcribe"));
	}
}

void UNajikaVoiceComponent::SetMicrophoneMuted(bool bMuted)
{
	bMicrophoneMuted = bMuted;

	if (bMuted && VoiceCapture && VoiceCapture->IsCapturing())
	{
		VoiceCapture->PauseCapture();
	}
	else if (!bMuted && VoiceCapture && IsInCall())
	{
		VoiceCapture->ResumeCapture();
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Microphone %s"), bMuted ? TEXT("muted") : TEXT("unmuted"));
}

void UNajikaVoiceComponent::SetPlaybackMuted(bool bMuted)
{
	bPlaybackMuted = bMuted;

	if (VoicePlayback)
	{
		VoicePlayback->SetVolume(bMuted ? 0.0f : 1.0f);
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Playback %s"), bMuted ? TEXT("muted") : TEXT("unmuted"));
}

void UNajikaVoiceComponent::OnAudioPacketReady(const FNajikaAudioPacket& Packet)
{
	// Store for potential transcription
	LastAudioPacket = Packet;

	// Update stats
	CallStats.PacketsSent++;

	// Auto-transcribe if enabled
	if (bAutoTranscribe && WhisperClient)
	{
		WhisperClient->TranscribePacket(Packet);
	}

	// Here you would send the packet to the network
	// For now, just log
	UE_LOG(LogTemp, VeryVerbose, TEXT("NajikaVoiceComponent: Audio packet ready (seq: %d, size: %d bytes)"),
		Packet.SequenceNumber, Packet.AudioData.Num());
}

void UNajikaVoiceComponent::OnWhisperTranscriptionComplete(const FNajikaWhisperResult& Result)
{
	// Broadcast to Blueprint
	OnTranscriptionComplete.Broadcast(Result);

	if (Result.bSuccess)
	{
		UE_LOG(LogTemp, Log, TEXT("NajikaVoiceComponent: Transcription: '%s'"), *Result.Text);
	}
}

void UNajikaVoiceComponent::OnVoiceDetected(bool bDetected)
{
	// Broadcast to Blueprint
	OnVoiceActivityDetected.Broadcast(bDetected);
}

void UNajikaVoiceComponent::UpdateCallStats(float DeltaTime)
{
	if (GetWorld())
	{
		CallStats.CallDuration = GetWorld()->GetTimeSeconds() - CallStartTime;
	}

	// Calculate packet loss rate
	if (CallStats.PacketsSent > 0)
	{
		float LossRate = (float)CallStats.PacketsLost / (float)CallStats.PacketsSent;
		// Update other stats as needed
	}
}

void UNajikaVoiceComponent::SetCallState(EVoiceCallState NewState)
{
	if (CallState != NewState)
	{
		CallState = NewState;
		OnVoiceCallStateChanged.Broadcast(NewState);
	}
}
