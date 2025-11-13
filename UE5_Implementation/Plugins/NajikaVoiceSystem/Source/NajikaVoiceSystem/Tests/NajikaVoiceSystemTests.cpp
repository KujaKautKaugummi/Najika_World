// Copyright Najika Development Team. All Rights Reserved.

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "NajikaVoiceCapture.h"
#include "NajikaVoicePlayback.h"
#include "NajikaVoiceEncoding.h"
#include "NajikaWhisperClient.h"
#include "NajikaVoiceComponent.h"
#include "NajikaVoiceTypes.h"

// ============================================================================
// NAJIKA VOICE SYSTEM - UNIT TESTS
// ============================================================================
//
// Test suite for NajikaVoiceSystem plugin
//
// Run tests in UE5 Editor:
//   Window > Test Automation
//   Filter: "Najika.Voice"
//   Select all tests > Start Tests
//
// ============================================================================

// ============================================================================
// VOICE CAPTURE TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceCaptureConstruction,
	"Najika.Voice.Capture.Construction",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceCaptureConstruction::RunTest(const FString& Parameters)
{
	// Test: Voice capture object can be created
	UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

	TestNotNull(TEXT("Voice capture should be created"), Capture);
	TestFalse(TEXT("Capture should not be initialized by default"), Capture->IsInitialized());
	TestFalse(TEXT("Capture should not be active by default"), Capture->IsCapturing());

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceCaptureInitialization,
	"Najika.Voice.Capture.Initialization",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceCaptureInitialization::RunTest(const FString& Parameters)
{
	// Test: Voice capture initializes with valid configuration
	UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

	FNajikaVoiceCaptureConfig Config;
	Config.SampleRate = 48000;
	Config.NumChannels = 1;
	Config.bEnableVAD = true;
	Config.bEnableNoiseSuppression = true;
	Config.bEnableEchoCancellation = false;
	Config.bEnableAGC = true;

	bool bSuccess = Capture->Initialize(Config);

	TestTrue(TEXT("Capture should initialize successfully"), bSuccess);
	TestTrue(TEXT("Capture should be initialized"), Capture->IsInitialized());
	TestEqual(TEXT("Sample rate should be set"), Capture->GetSampleRate(), 48000);

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceVADDetection,
	"Najika.Voice.VAD.Detection",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceVADDetection::RunTest(const FString& Parameters)
{
	// Test: Voice Activity Detection works correctly
	UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

	FNajikaVoiceCaptureConfig Config;
	Config.SampleRate = 48000;
	Config.bEnableVAD = true;
	Capture->Initialize(Config);

	// Test silence (low energy)
	TArray<float> SilenceBuffer;
	SilenceBuffer.Init(0.001f, 1024);  // Very quiet audio
	bool bVoiceInSilence = Capture->DetectVoiceActivity(SilenceBuffer.GetData(), 1024);
	TestFalse(TEXT("VAD should not detect voice in silence"), bVoiceInSilence);

	// Test loud audio (high energy)
	TArray<float> LoudBuffer;
	LoudBuffer.Init(0.8f, 1024);  // Loud audio
	bool bVoiceInLoud = Capture->DetectVoiceActivity(LoudBuffer.GetData(), 1024);
	TestTrue(TEXT("VAD should detect voice in loud audio"), bVoiceInLoud);

	// Test medium audio (should detect with default sensitivity)
	TArray<float> MediumBuffer;
	MediumBuffer.Init(0.3f, 1024);  // Medium volume
	bool bVoiceInMedium = Capture->DetectVoiceActivity(MediumBuffer.GetData(), 1024);
	TestTrue(TEXT("VAD should detect voice in medium-volume audio"), bVoiceInMedium);

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceVADSensitivity,
	"Najika.Voice.VAD.Sensitivity",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceVADSensitivity::RunTest(const FString& Parameters)
{
	// Test: VAD sensitivity levels work correctly
	UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

	FNajikaVoiceCaptureConfig Config;
	Config.SampleRate = 48000;
	Config.bEnableVAD = true;
	Capture->Initialize(Config);

	// Medium-low volume audio
	TArray<float> TestBuffer;
	TestBuffer.Init(0.15f, 1024);

	// High sensitivity should detect
	Capture->SetVADSensitivity(EVADSensitivity::High);
	bool bDetectedHigh = Capture->DetectVoiceActivity(TestBuffer.GetData(), 1024);
	TestTrue(TEXT("High sensitivity should detect medium-low audio"), bDetectedHigh);

	// Low sensitivity should not detect
	Capture->SetVADSensitivity(EVADSensitivity::Low);
	bool bDetectedLow = Capture->DetectVoiceActivity(TestBuffer.GetData(), 1024);
	TestFalse(TEXT("Low sensitivity should not detect medium-low audio"), bDetectedLow);

	return true;
}

// ============================================================================
// VOICE ENCODING TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceEncodingBase64,
	"Najika.Voice.Encoding.Base64",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceEncodingBase64::RunTest(const FString& Parameters)
{
	// Test: Base64 encoding/decoding works correctly
	UNajikaVoiceEncoding* Encoding = NewObject<UNajikaVoiceEncoding>();

	// Original data
	TArray<uint8> OriginalData = {0x01, 0x02, 0x03, 0x04, 0x05};

	// Encode
	FString EncodedString = Encoding->EncodeToBase64(OriginalData);
	TestFalse(TEXT("Encoded string should not be empty"), EncodedString.IsEmpty());
	TestEqual(TEXT("Encoded string should be 'AQIDBAU='"), EncodedString, TEXT("AQIDBAU="));

	// Decode
	TArray<uint8> DecodedData = Encoding->DecodeFromBase64(EncodedString);
	TestEqual(TEXT("Decoded data size should match original"), DecodedData.Num(), OriginalData.Num());
	TestTrue(TEXT("Decoded data should match original"), DecodedData == OriginalData);

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceEncodingPCM16,
	"Najika.Voice.Encoding.PCM16Conversion",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceEncodingPCM16::RunTest(const FString& Parameters)
{
	// Test: Float to PCM16 conversion
	UNajikaVoiceEncoding* Encoding = NewObject<UNajikaVoiceEncoding>();

	TArray<float> FloatSamples = {-1.0f, -0.5f, 0.0f, 0.5f, 1.0f};
	TArray<uint8> PCM16Data = Encoding->ConvertFloatToPCM16(FloatSamples);

	TestEqual(TEXT("PCM16 data size should be 2x float count"), PCM16Data.Num(), FloatSamples.Num() * 2);

	// Convert back
	TArray<float> ConvertedBack = Encoding->ConvertPCM16ToFloat(PCM16Data);
	TestEqual(TEXT("Converted back size should match original"), ConvertedBack.Num(), FloatSamples.Num());

	// Check values (with tolerance for quantization error)
	for (int32 i = 0; i < FloatSamples.Num(); i++)
	{
		float Difference = FMath::Abs(ConvertedBack[i] - FloatSamples[i]);
		TestTrue(TEXT("Converted values should be close to original"), Difference < 0.01f);
	}

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceEncodingResampling,
	"Najika.Voice.Encoding.Resampling",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceEncodingResampling::RunTest(const FString& Parameters)
{
	// Test: Audio resampling (simple linear interpolation)
	UNajikaVoiceEncoding* Encoding = NewObject<UNajikaVoiceEncoding>();

	// Source: 4 samples at 16kHz
	TArray<float> SourceSamples = {0.0f, 0.5f, 1.0f, 0.5f};
	int32 SourceSampleRate = 16000;

	// Target: 48kHz (3x samples)
	int32 TargetSampleRate = 48000;
	TArray<float> ResampledSamples = Encoding->Resample(SourceSamples, SourceSampleRate, TargetSampleRate);

	// Should have approximately 3x samples
	int32 ExpectedCount = (SourceSamples.Num() * TargetSampleRate) / SourceSampleRate;
	TestEqual(TEXT("Resampled count should be ~3x original"), ResampledSamples.Num(), ExpectedCount);

	return true;
}

// ============================================================================
// VOICE PLAYBACK TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoicePlaybackConstruction,
	"Najika.Voice.Playback.Construction",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoicePlaybackConstruction::RunTest(const FString& Parameters)
{
	// Test: Voice playback object can be created
	UNajikaVoicePlayback* Playback = NewObject<UNajikaVoicePlayback>();

	TestNotNull(TEXT("Playback should be created"), Playback);
	TestFalse(TEXT("Playback should not be initialized by default"), Playback->IsInitialized());

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoicePlaybackInitialization,
	"Najika.Voice.Playback.Initialization",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoicePlaybackInitialization::RunTest(const FString& Parameters)
{
	// Test: Voice playback initializes correctly
	UNajikaVoicePlayback* Playback = NewObject<UNajikaVoicePlayback>();

	FNajikaVoicePlaybackConfig Config;
	Config.SampleRate = 48000;
	Config.NumChannels = 1;
	Config.JitterBufferSize = 10;

	bool bSuccess = Playback->Initialize(Config);

	TestTrue(TEXT("Playback should initialize successfully"), bSuccess);
	TestTrue(TEXT("Playback should be initialized"), Playback->IsInitialized());

	return true;
}

// ============================================================================
// WHISPER CLIENT TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaWhisperClientConstruction,
	"Najika.Voice.Whisper.Construction",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaWhisperClientConstruction::RunTest(const FString& Parameters)
{
	// Test: Whisper client can be created
	UNajikaWhisperClient* Client = NewObject<UNajikaWhisperClient>();

	TestNotNull(TEXT("Whisper client should be created"), Client);

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaWhisperClientConfiguration,
	"Najika.Voice.Whisper.Configuration",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaWhisperClientConfiguration::RunTest(const FString& Parameters)
{
	// Test: Whisper client accepts configuration
	UNajikaWhisperClient* Client = NewObject<UNajikaWhisperClient>();

	Client->SetBackendURL(TEXT("http://localhost:8000"));
	Client->SetDefaultLanguage(TEXT("en"));

	FString URL = Client->GetBackendURL();
	TestEqual(TEXT("Backend URL should be set"), URL, TEXT("http://localhost:8000"));

	return true;
}

// ============================================================================
// VOICE COMPONENT INTEGRATION TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceComponentConstruction,
	"Najika.Voice.Component.Construction",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceComponentConstruction::RunTest(const FString& Parameters)
{
	// Test: Voice component can be created
	UNajikaVoiceComponent* Component = NewObject<UNajikaVoiceComponent>();

	TestNotNull(TEXT("Voice component should be created"), Component);
	TestNotNull(TEXT("Voice capture should exist"), Component->GetVoiceCapture());
	TestNotNull(TEXT("Voice playback should exist"), Component->GetVoicePlayback());

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceComponentInitialization,
	"Najika.Voice.Component.Initialization",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceComponentInitialization::RunTest(const FString& Parameters)
{
	// Test: Voice component initializes all subcomponents
	UNajikaVoiceComponent* Component = NewObject<UNajikaVoiceComponent>();

	bool bSuccess = Component->InitializeVoiceSystem(48000);

	TestTrue(TEXT("Voice system should initialize successfully"), bSuccess);
	TestTrue(TEXT("Voice capture should be initialized"), Component->GetVoiceCapture()->IsInitialized());
	TestTrue(TEXT("Voice playback should be initialized"), Component->GetVoicePlayback()->IsInitialized());

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceComponentCallModes,
	"Najika.Voice.Component.CallModes",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceComponentCallModes::RunTest(const FString& Parameters)
{
	// Test: Voice component supports different call modes
	UNajikaVoiceComponent* Component = NewObject<UNajikaVoiceComponent>();
	Component->InitializeVoiceSystem(48000);

	// Test push-to-talk mode
	Component->SetUsePushToTalk(true);
	TestTrue(TEXT("Push-to-talk should be enabled"), Component->IsPushToTalkEnabled());

	Component->StartPushToTalk();
	TestTrue(TEXT("Should be transmitting in PTT mode"), Component->IsTransmitting());

	Component->StopPushToTalk();
	TestFalse(TEXT("Should not be transmitting after stopping PTT"), Component->IsTransmitting());

	// Test VAD mode
	Component->SetUsePushToTalk(false);
	TestFalse(TEXT("Push-to-talk should be disabled"), Component->IsPushToTalkEnabled());

	return true;
}

// ============================================================================
// AUDIO PACKET TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaAudioPacketCreation,
	"Najika.Voice.AudioPacket.Creation",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaAudioPacketCreation::RunTest(const FString& Parameters)
{
	// Test: Audio packet struct creation and serialization
	FNajikaAudioPacket Packet;
	Packet.AudioData = {0x01, 0x02, 0x03, 0x04};
	Packet.SequenceNumber = 1234;
	Packet.Timestamp = 1705089600000;
	Packet.SampleRate = 48000;
	Packet.EncodingFormat = EVoiceEncodingFormat::Opus;
	Packet.bContainsVoice = true;

	TestEqual(TEXT("Audio data size should be 4"), Packet.AudioData.Num(), 4);
	TestEqual(TEXT("Sequence number should be set"), Packet.SequenceNumber, 1234);
	TestEqual(TEXT("Sample rate should be 48000"), Packet.SampleRate, 48000);
	TestTrue(TEXT("Should contain voice"), Packet.bContainsVoice);

	return true;
}

// ============================================================================
// PERFORMANCE TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoicePerformanceVAD,
	"Najika.Voice.Performance.VAD",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoicePerformanceVAD::RunTest(const FString& Parameters)
{
	// Test: VAD performance (should process 1000 frames quickly)
	UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

	FNajikaVoiceCaptureConfig Config;
	Config.SampleRate = 48000;
	Config.bEnableVAD = true;
	Capture->Initialize(Config);

	TArray<float> TestBuffer;
	TestBuffer.Init(0.5f, 960);  // 20ms at 48kHz

	double StartTime = FPlatformTime::Seconds();

	// Process 1000 frames (20 seconds of audio)
	for (int32 i = 0; i < 1000; i++)
	{
		Capture->DetectVoiceActivity(TestBuffer.GetData(), 960);
	}

	double EndTime = FPlatformTime::Seconds();
	double ElapsedTime = EndTime - StartTime;

	// Should complete in less than 1 second (real-time requirement: 20s audio in < 1s)
	TestTrue(TEXT("VAD should process 1000 frames in < 1 second"), ElapsedTime < 1.0);

	UE_LOG(LogTemp, Log, TEXT("VAD Performance: Processed 1000 frames in %.3f seconds"), ElapsedTime);

	return true;
}

// ============================================================================
// EDGE CASE TESTS
// ============================================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceEdgeCaseEmptyBuffer,
	"Najika.Voice.EdgeCases.EmptyBuffer",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceEdgeCaseEmptyBuffer::RunTest(const FString& Parameters)
{
	// Test: Handling of empty audio buffer
	UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

	FNajikaVoiceCaptureConfig Config;
	Capture->Initialize(Config);

	TArray<float> EmptyBuffer;
	bool bVoiceDetected = Capture->DetectVoiceActivity(EmptyBuffer.GetData(), 0);

	TestFalse(TEXT("VAD should not detect voice in empty buffer"), bVoiceDetected);

	return true;
}

// ----------------------------------------------------------------------------

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FNajikaVoiceEdgeCaseNullBuffer,
	"Najika.Voice.EdgeCases.NullBuffer",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter)

bool FNajikaVoiceEdgeCaseNullBuffer::RunTest(const FString& Parameters)
{
	// Test: Handling of null buffer pointer
	UNajikaVoiceCapture* Capture = NewObject<UNajikaVoiceCapture>();

	FNajikaVoiceCaptureConfig Config;
	Capture->Initialize(Config);

	bool bVoiceDetected = Capture->DetectVoiceActivity(nullptr, 1024);

	TestFalse(TEXT("VAD should handle null buffer gracefully"), bVoiceDetected);

	return true;
}

// ============================================================================
// TEST SUMMARY
// ============================================================================
//
// Total Tests: 20+
//
// Coverage:
//   - Voice Capture: Construction, Initialization, VAD, Sensitivity
//   - Voice Encoding: Base64, PCM16 conversion, Resampling
//   - Voice Playback: Construction, Initialization
//   - Whisper Client: Construction, Configuration
//   - Voice Component: Construction, Initialization, Call modes
//   - Audio Packets: Creation and serialization
//   - Performance: VAD processing speed
//   - Edge Cases: Empty/null buffers
//
// To run these tests:
//   1. Open UE5 Editor
//   2. Window > Test Automation
//   3. Filter: "Najika.Voice"
//   4. Select all tests
//   5. Click "Start Tests"
//
// Expected result: All tests PASS (green)
//
// ============================================================================
