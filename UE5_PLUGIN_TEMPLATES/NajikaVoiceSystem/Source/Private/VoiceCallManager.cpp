// Copyright Model 1 - Najika Digivice APK

#include "VoiceCallManager.h"
#include "HttpModule.h"
#include "JsonUtilities.h"
#include "Misc/Base64.h"
#include "AudioDevice.h"

// ============================================
// INITIALIZATION
// ============================================

void UVoiceCallManager::Initialize()
{
	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Initializing Voice Call System..."));

	// Initialize audio capture
	AudioCapture = MakeShared<Audio::FAudioCapture>();

	// Check if audio capture is available
	if (!AudioCapture.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[Najika Voice] Failed to create audio capture device!"));
		OnVoiceCallError.Broadcast(TEXT("Failed to initialize audio capture"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Voice Call System initialized successfully!"));
}

void UVoiceCallManager::Shutdown()
{
	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Shutting down Voice Call System..."));

	if (bIsCallActive)
	{
		EndVoiceCall();
	}

	// Cleanup audio capture
	if (AudioCapture.IsValid())
	{
		AudioCapture->StopCapturing();
		AudioCapture.Reset();
	}
}

// ============================================
// VOICE CALL CONTROL
// ============================================

bool UVoiceCallManager::StartVoiceCall()
{
	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Starting voice call..."));

	// Check if already active
	if (bIsCallActive)
	{
		UE_LOG(LogTemp, Warning, TEXT("[Najika Voice] Call already active!"));
		return false;
	}

	// Check microphone permission
	if (!HasMicrophonePermission())
	{
		UE_LOG(LogTemp, Warning, TEXT("[Najika Voice] No microphone permission!"));
		RequestMicrophonePermission();
		return false;
	}

	// Initialize audio capture if needed
	if (!AudioCapture.IsValid())
	{
		Initialize();
	}

	if (!AudioCapture.IsValid())
	{
		OnVoiceCallError.Broadcast(TEXT("Audio capture not available"));
		return false;
	}

	// Configure audio capture
	Audio::FAudioCaptureDeviceParams Params;
	Params.SampleRate = SampleRate;
	Params.NumInputChannels = 1; // Mono

	// Start capturing
	AudioCapture->OpenCaptureStream(
		Params,
		[this](const float* InAudio, int32 NumSamples, int32 NumChannels)
		{
			OnAudioCapture(InAudio, NumSamples, NumChannels);
		},
		BufferSize
	);

	if (!AudioCapture->StartCapturing())
	{
		UE_LOG(LogTemp, Error, TEXT("[Najika Voice] Failed to start audio capture!"));
		OnVoiceCallError.Broadcast(TEXT("Failed to start microphone"));
		return false;
	}

	// Send start request to backend
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
	Request->SetURL(BaseURL + TEXT("/api/voice_call/start"));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	Request->OnProcessRequestComplete().BindLambda(
		[this](FHttpRequestPtr Req, FHttpResponsePtr Response, bool bSuccess)
		{
			if (!bSuccess || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika Voice] Failed to start call on backend!"));
				OnVoiceCallError.Broadcast(TEXT("Backend connection failed"));
				EndVoiceCall();
				return;
			}

			UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Backend call started successfully!"));
		}
	);

	Request->ProcessRequest();

	// Set state
	bIsCallActive = true;
	CallStartTime = FPlatformTime::Seconds();
	SilenceTimer = 0.0f;

	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Voice call started!"));
	OnVoiceCallStarted.Broadcast();

	return true;
}

void UVoiceCallManager::EndVoiceCall()
{
	if (!bIsCallActive)
	{
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Ending voice call..."));

	// Stop audio capture
	if (AudioCapture.IsValid())
	{
		AudioCapture->StopCapturing();
	}

	// Calculate duration
	float Duration = GetCallDuration();

	// Send end request to backend
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
	Request->SetURL(BaseURL + TEXT("/api/voice_call/end"));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	Request->OnProcessRequestComplete().BindLambda(
		[Duration](FHttpRequestPtr Req, FHttpResponsePtr Response, bool bSuccess)
		{
			if (bSuccess && Response.IsValid())
			{
				UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Backend call ended. Duration: %.1fs"), Duration);
			}
		}
	);

	Request->ProcessRequest();

	// Reset state
	bIsCallActive = false;
	AudioBuffer.Empty();
	CurrentAudioLevel = 0.0f;

	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Voice call ended. Duration: %.1fs"), Duration);
	OnVoiceCallEnded.Broadcast(Duration);
}

float UVoiceCallManager::GetCallDuration() const
{
	if (!bIsCallActive)
	{
		return 0.0f;
	}

	return static_cast<float>(FPlatformTime::Seconds() - CallStartTime);
}

void UVoiceCallManager::SendAudioChunk(const TArray<uint8>& AudioData)
{
	if (!bIsCallActive)
	{
		UE_LOG(LogTemp, Warning, TEXT("[Najika Voice] Cannot send audio - call not active!"));
		return;
	}

	SendAudioToBackend(AudioData);
}

// ============================================
// MICROPHONE CONTROL
// ============================================

bool UVoiceCallManager::HasMicrophonePermission() const
{
#if PLATFORM_ANDROID
	// On Android, check permission
	// TODO: Implement Android permission check
	return true; // Placeholder
#else
	// On other platforms, assume permission granted
	return true;
#endif
}

void UVoiceCallManager::RequestMicrophonePermission()
{
#if PLATFORM_ANDROID
	// TODO: Request Android microphone permission
	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Requesting microphone permission..."));
#endif
}

// ============================================
// AUDIO CAPTURE CALLBACKS
// ============================================

void UVoiceCallManager::OnAudioCapture(const float* InAudio, int32 NumSamples, int32 NumChannels)
{
	if (!bIsCallActive)
	{
		return;
	}

	// Copy audio to buffer (mono only)
	TArray<float> CapturedAudio;
	CapturedAudio.Reserve(NumSamples);

	for (int32 i = 0; i < NumSamples; i += NumChannels)
	{
		// Take first channel (mono)
		CapturedAudio.Add(InAudio[i]);
	}

	// Calculate audio level
	CurrentAudioLevel = CalculateAudioLevel(CapturedAudio);

	// Detect voice activity
	bool bVoiceDetected = DetectVoiceActivity(CurrentAudioLevel);

	if (bVoiceDetected)
	{
		// Reset silence timer
		SilenceTimer = 0.0f;

		// Add to buffer
		AudioBuffer.Append(CapturedAudio);

		// If buffer is large enough, process it
		if (AudioBuffer.Num() >= SampleRate * 2) // 2 seconds of audio
		{
			ProcessAudioBuffer(AudioBuffer);
			AudioBuffer.Empty();
		}
	}
	else
	{
		// Increment silence timer
		SilenceTimer += static_cast<float>(NumSamples) / SampleRate;

		// If silence duration exceeded, process remaining buffer
		if (SilenceTimer >= SilenceDuration && AudioBuffer.Num() > 0)
		{
			ProcessAudioBuffer(AudioBuffer);
			AudioBuffer.Empty();
			SilenceTimer = 0.0f;
		}
	}
}

void UVoiceCallManager::ProcessAudioBuffer(const TArray<float>& Buffer)
{
	if (Buffer.Num() == 0)
	{
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Processing audio buffer (%d samples)"), Buffer.Num());

	// Convert float samples (-1.0 to 1.0) to int16 PCM
	TArray<uint8> PCMData;
	PCMData.Reserve(Buffer.Num() * 2); // 16-bit = 2 bytes per sample

	for (float Sample : Buffer)
	{
		// Clamp to [-1.0, 1.0]
		float ClampedSample = FMath::Clamp(Sample, -1.0f, 1.0f);

		// Convert to int16 (-32768 to 32767)
		int16 PCMSample = static_cast<int16>(ClampedSample * 32767.0f);

		// Add bytes (little-endian)
		PCMData.Add(static_cast<uint8>(PCMSample & 0xFF));
		PCMData.Add(static_cast<uint8>((PCMSample >> 8) & 0xFF));
	}

	// Send to backend
	SendAudioToBackend(PCMData);
}

float UVoiceCallManager::CalculateAudioLevel(const TArray<float>& Buffer)
{
	if (Buffer.Num() == 0)
	{
		return 0.0f;
	}

	// Calculate RMS (Root Mean Square)
	float Sum = 0.0f;
	for (float Sample : Buffer)
	{
		Sum += Sample * Sample;
	}

	float RMS = FMath::Sqrt(Sum / Buffer.Num());
	return RMS;
}

bool UVoiceCallManager::DetectVoiceActivity(float AudioLevel)
{
	return AudioLevel > VADThreshold;
}

// ============================================
// BACKEND COMMUNICATION
// ============================================

void UVoiceCallManager::SendAudioToBackend(const TArray<uint8>& AudioData)
{
	// Convert to Base64
	FString AudioBase64 = FBase64::Encode(AudioData);

	// Create JSON
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("audio"), AudioBase64);
	JsonObject->SetNumberField(TEXT("sample_rate"), SampleRate);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	// Create HTTP request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
	Request->SetURL(BaseURL + TEXT("/api/voice_call/audio"));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	Request->OnProcessRequestComplete().BindUObject(this, &UVoiceCallManager::HandleSTTResponse);
	Request->ProcessRequest();
}

void UVoiceCallManager::HandleSTTResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[Najika Voice] STT request failed!"));
		return;
	}

	// Parse JSON response
	TSharedPtr<FJsonObject> JsonResponse;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());

	if (!FJsonSerializer::Deserialize(Reader, JsonResponse) || !JsonResponse.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[Najika Voice] Failed to parse STT response!"));
		return;
	}

	// Extract recognized text
	FString RecognizedText = JsonResponse->GetStringField(TEXT("text"));

	if (RecognizedText.IsEmpty())
	{
		// No speech detected
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Recognized: %s"), *RecognizedText);
	OnSpeechRecognized.Broadcast(RecognizedText);

	// Check for TTS audio in response
	if (JsonResponse->HasField(TEXT("audio")))
	{
		FString AudioPath = JsonResponse->GetStringField(TEXT("audio"));
		HandleTTSAudio(AudioPath);
	}
}

void UVoiceCallManager::HandleTTSAudio(const FString& AudioPath)
{
	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Receiving TTS audio: %s"), *AudioPath);

	// Construct full URL
	FString AudioURL = BaseURL + AudioPath;

	// Download and play audio
	DownloadAndPlayAudio(AudioURL);
}

void UVoiceCallManager::DownloadAndPlayAudio(const FString& AudioURL)
{
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
	Request->SetURL(AudioURL);
	Request->SetVerb(TEXT("GET"));

	Request->OnProcessRequestComplete().BindLambda(
		[this](FHttpRequestPtr Req, FHttpResponsePtr Response, bool bSuccess)
		{
			if (!bSuccess || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika Voice] Failed to download TTS audio!"));
				return;
			}

			// Get audio data
			TArray<uint8> AudioData = Response->GetContent();

			UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Downloaded TTS audio (%d bytes)"), AudioData.Num());

			// Play audio
			PlayAudioResponse(AudioData);
		}
	);

	Request->ProcessRequest();
}

// ============================================
// AUDIO PLAYBACK
// ============================================

void UVoiceCallManager::PlayAudioResponse(const TArray<uint8>& AudioData)
{
	// Create sound wave from audio data
	USoundWaveProcedural* SoundWave = CreateSoundWaveFromData(AudioData);

	if (!SoundWave)
	{
		UE_LOG(LogTemp, Error, TEXT("[Najika Voice] Failed to create sound wave!"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Playing Najika's response..."));
	OnNajikaResponse.Broadcast(SoundWave);

	// Note: Actual playback should be done by caller
	// They can use UGameplayStatics::PlaySound2D(SoundWave) or AudioComponent
}

USoundWaveProcedural* UVoiceCallManager::CreateSoundWaveFromData(const TArray<uint8>& AudioData)
{
	// TODO: Implement WAV parsing and sound wave creation
	// This is a complex task that requires:
	// 1. Parse WAV header
	// 2. Extract PCM data
	// 3. Create USoundWaveProcedural
	// 4. Queue audio data

	// For now, return nullptr (to be implemented)
	UE_LOG(LogTemp, Warning, TEXT("[Najika Voice] CreateSoundWaveFromData not yet implemented!"));
	return nullptr;
}
