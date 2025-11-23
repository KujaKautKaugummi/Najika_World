// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "NajikaVoiceTypes.generated.h"

/**
 * Voice call state enum
 */
UENUM(BlueprintType)
enum class EVoiceCallState : uint8
{
	Idle UMETA(DisplayName = "Idle"),
	Connecting UMETA(DisplayName = "Connecting"),
	Connected UMETA(DisplayName = "Connected"),
	Ringing UMETA(DisplayName = "Ringing"),
	InCall UMETA(DisplayName = "In Call"),
	Disconnecting UMETA(DisplayName = "Disconnecting"),
	Error UMETA(DisplayName = "Error")
};

/**
 * Voice quality settings
 */
UENUM(BlueprintType)
enum class EVoiceQuality : uint8
{
	Low UMETA(DisplayName = "Low (8kHz, 16kbps)"),
	Medium UMETA(DisplayName = "Medium (16kHz, 24kbps)"),
	High UMETA(DisplayName = "High (48kHz, 64kbps)")
};

/**
 * Voice encoding format
 */
UENUM(BlueprintType)
enum class EVoiceEncodingFormat : uint8
{
	Opus UMETA(DisplayName = "Opus"),
	PCM UMETA(DisplayName = "PCM (Raw)"),
	Speex UMETA(DisplayName = "Speex")
};

/**
 * Voice capture state
 */
UENUM(BlueprintType)
enum class EVoiceCaptureState : uint8
{
	Stopped UMETA(DisplayName = "Stopped"),
	Starting UMETA(DisplayName = "Starting"),
	Capturing UMETA(DisplayName = "Capturing"),
	Paused UMETA(DisplayName = "Paused"),
	Error UMETA(DisplayName = "Error")
};

/**
 * Voice activity detection (VAD) sensitivity
 */
UENUM(BlueprintType)
enum class EVADSensitivity : uint8
{
	Low UMETA(DisplayName = "Low (Less sensitive)"),
	Medium UMETA(DisplayName = "Medium"),
	High UMETA(DisplayName = "High (More sensitive)")
};

/**
 * Audio packet structure for network transmission
 */
USTRUCT(BlueprintType)
struct FNajikaAudioPacket
{
	GENERATED_BODY()

	/** Encoded audio data */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	TArray<uint8> AudioData;

	/** Packet sequence number */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	int32 SequenceNumber = 0;

	/** Timestamp (milliseconds) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	int64 Timestamp = 0;

	/** Sample rate (Hz) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	int32 SampleRate = 48000;

	/** Number of channels (1 = Mono, 2 = Stereo) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	int32 NumChannels = 1;

	/** Encoding format */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	EVoiceEncodingFormat EncodingFormat = EVoiceEncodingFormat::Opus;

	/** Is this packet containing voice activity */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	bool bContainsVoice = false;

	FNajikaAudioPacket()
		: SequenceNumber(0)
		, Timestamp(0)
		, SampleRate(48000)
		, NumChannels(1)
		, EncodingFormat(EVoiceEncodingFormat::Opus)
		, bContainsVoice(false)
	{}
};

/**
 * Voice call statistics
 */
USTRUCT(BlueprintType)
struct FNajikaVoiceCallStats
{
	GENERATED_BODY()

	/** Total packets sent */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	int32 PacketsSent = 0;

	/** Total packets received */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	int32 PacketsReceived = 0;

	/** Packets lost */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	int32 PacketsLost = 0;

	/** Average latency (ms) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	float AverageLatency = 0.0f;

	/** Current jitter (ms) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	float Jitter = 0.0f;

	/** Call duration (seconds) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	float CallDuration = 0.0f;

	/** Average bandwidth used (kbps) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	float AverageBandwidth = 0.0f;

	FNajikaVoiceCallStats()
		: PacketsSent(0)
		, PacketsReceived(0)
		, PacketsLost(0)
		, AverageLatency(0.0f)
		, Jitter(0.0f)
		, CallDuration(0.0f)
		, AverageBandwidth(0.0f)
	{}
};

/**
 * Whisper AI transcription result
 */
USTRUCT(BlueprintType)
struct FNajikaWhisperResult
{
	GENERATED_BODY()

	/** Transcribed text */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	FString Text;

	/** Confidence score (0.0 - 1.0) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	float Confidence = 0.0f;

	/** Detected language code (e.g., "en", "ja", "de") */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	FString LanguageCode;

	/** Processing time (seconds) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	float ProcessingTime = 0.0f;

	/** Was transcription successful */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	bool bSuccess = false;

	/** Error message (if any) */
	UPROPERTY(BlueprintReadOnly, Category = "Najika|Voice")
	FString ErrorMessage;

	FNajikaWhisperResult()
		: Confidence(0.0f)
		, ProcessingTime(0.0f)
		, bSuccess(false)
	{}
};

/**
 * Voice capture configuration
 */
USTRUCT(BlueprintType)
struct FNajikaVoiceCaptureConfig
{
	GENERATED_BODY()

	/** Sample rate (Hz) - Higher = better quality, more bandwidth */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	int32 SampleRate = 48000;

	/** Buffer size (samples) - Smaller = less latency, more CPU */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	int32 BufferSize = 1024;

	/** Number of channels (1 = Mono, 2 = Stereo) */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	int32 NumChannels = 1;

	/** Enable voice activity detection */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	bool bEnableVAD = true;

	/** VAD sensitivity */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	EVADSensitivity VADSensitivity = EVADSensitivity::Medium;

	/** Enable noise suppression */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	bool bEnableNoiseSuppression = true;

	/** Enable echo cancellation */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	bool bEnableEchoCancellation = true;

	/** Enable automatic gain control */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	bool bEnableAGC = true;

	/** Microphone input gain (0.0 - 2.0) */
	UPROPERTY(BlueprintReadWrite, Category = "Najika|Voice")
	float InputGain = 1.0f;

	FNajikaVoiceCaptureConfig()
		: SampleRate(48000)
		, BufferSize(1024)
		, NumChannels(1)
		, bEnableVAD(true)
		, VADSensitivity(EVADSensitivity::Medium)
		, bEnableNoiseSuppression(true)
		, bEnableEchoCancellation(true)
		, bEnableAGC(true)
		, InputGain(1.0f)
	{}
};

// Delegate declarations

/** Called when voice capture state changes */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnVoiceCaptureStateChanged, EVoiceCaptureState, NewState);

/** Called when audio packet is ready to send */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAudioPacketReady, const FNajikaAudioPacket&, Packet);

/** Called when voice call state changes */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnVoiceCallStateChanged, EVoiceCallState, NewState);

/** Called when Whisper transcription is complete */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWhisperTranscriptionComplete, const FNajikaWhisperResult&, Result);

/** Called when voice activity is detected */
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnVoiceActivityDetected, bool, bVoiceDetected);
