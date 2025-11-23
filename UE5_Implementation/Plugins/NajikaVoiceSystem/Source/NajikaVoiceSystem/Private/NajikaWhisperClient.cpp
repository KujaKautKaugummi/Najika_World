// Copyright Najika Development Team. All Rights Reserved.

#include "NajikaWhisperClient.h"
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Json.h"
#include "JsonUtilities.h"
#include "Misc/Base64.h"

UNajikaWhisperClient::UNajikaWhisperClient()
	: BackendURL(TEXT("http://localhost:8000"))
	, bIsProcessing(false)
	, RequestStartTime(0.0)
	, HttpModule(nullptr)
{
}

bool UNajikaWhisperClient::Initialize(const FString& InBackendURL)
{
	BackendURL = InBackendURL;

	HttpModule = &FHttpModule::Get();
	if (!HttpModule)
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaWhisperClient: Failed to get HTTP module"));
		return false;
	}

	UE_LOG(LogTemp, Log, TEXT("NajikaWhisperClient: Initialized with backend %s"), *BackendURL);
	return true;
}

void UNajikaWhisperClient::TranscribeAudio(const TArray<uint8>& AudioData, int32 SampleRate, const FString& LanguageCode)
{
	if (bIsProcessing)
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaWhisperClient: Already processing a request"));
		return;
	}

	if (AudioData.Num() == 0)
	{
		UE_LOG(LogTemp, Warning, TEXT("NajikaWhisperClient: Empty audio data"));
		return;
	}

	if (!HttpModule)
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaWhisperClient: Not initialized"));
		return;
	}

	// Create HTTP request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = HttpModule->CreateRequest();

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaWhisperClient::OnTranscriptionResponse);
	Request->SetURL(BackendURL + TEXT("/api/voice/transcribe"));
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

	// Create JSON payload
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject());

	// Encode audio data to Base64
	FString AudioDataBase64 = FBase64::Encode(AudioData);
	JsonObject->SetStringField(TEXT("audio_data"), AudioDataBase64);
	JsonObject->SetNumberField(TEXT("sample_rate"), SampleRate);
	JsonObject->SetStringField(TEXT("language"), LanguageCode);

	// Convert JSON to string
	FString RequestContent;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&RequestContent);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	Request->SetContentAsString(RequestContent);

	// Send request
	bIsProcessing = true;
	RequestStartTime = FPlatformTime::Seconds();

	if (Request->ProcessRequest())
	{
		UE_LOG(LogTemp, Log, TEXT("NajikaWhisperClient: Transcription request sent (%d bytes audio)"),
			AudioData.Num());
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaWhisperClient: Failed to send transcription request"));
		bIsProcessing = false;

		// Broadcast error result
		FNajikaWhisperResult Result;
		Result.bSuccess = false;
		Result.ErrorMessage = TEXT("Failed to send HTTP request");
		OnTranscriptionComplete.Broadcast(Result);
	}
}

void UNajikaWhisperClient::TranscribePacket(const FNajikaAudioPacket& Packet)
{
	TranscribeAudio(Packet.AudioData, Packet.SampleRate, TEXT("auto"));
}

void UNajikaWhisperClient::SetBackendURL(const FString& URL)
{
	BackendURL = URL;
	UE_LOG(LogTemp, Log, TEXT("NajikaWhisperClient: Backend URL set to %s"), *BackendURL);
}

void UNajikaWhisperClient::OnTranscriptionResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
{
	bIsProcessing = false;

	double ProcessingTime = FPlatformTime::Seconds() - RequestStartTime;

	FNajikaWhisperResult Result;
	Result.ProcessingTime = (float)ProcessingTime;

	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaWhisperClient: HTTP request failed"));
		Result.bSuccess = false;
		Result.ErrorMessage = TEXT("HTTP request failed");
		OnTranscriptionComplete.Broadcast(Result);
		return;
	}

	int32 ResponseCode = Response->GetResponseCode();

	if (ResponseCode != 200)
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaWhisperClient: HTTP error %d"), ResponseCode);
		Result.bSuccess = false;
		Result.ErrorMessage = FString::Printf(TEXT("HTTP error %d"), ResponseCode);
		OnTranscriptionComplete.Broadcast(Result);
		return;
	}

	// Parse response
	FString ResponseContent = Response->GetContentAsString();
	Result = ParseResponse(ResponseContent);
	Result.ProcessingTime = (float)ProcessingTime;

	if (Result.bSuccess)
	{
		UE_LOG(LogTemp, Log, TEXT("NajikaWhisperClient: Transcription complete: '%s' (confidence: %.2f, time: %.2fs)"),
			*Result.Text, Result.Confidence, Result.ProcessingTime);
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaWhisperClient: Transcription failed: %s"), *Result.ErrorMessage);
	}

	OnTranscriptionComplete.Broadcast(Result);
}

FNajikaWhisperResult UNajikaWhisperClient::ParseResponse(const FString& ResponseContent)
{
	FNajikaWhisperResult Result;

	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ResponseContent);

	if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("NajikaWhisperClient: Failed to parse JSON response"));
		Result.bSuccess = false;
		Result.ErrorMessage = TEXT("Invalid JSON response");
		return Result;
	}

	// Check for success field
	bool bSuccess = false;
	if (JsonObject->TryGetBoolField(TEXT("success"), bSuccess) && !bSuccess)
	{
		FString ErrorMsg;
		JsonObject->TryGetStringField(TEXT("error"), ErrorMsg);
		Result.bSuccess = false;
		Result.ErrorMessage = ErrorMsg.IsEmpty() ? TEXT("Unknown error") : ErrorMsg;
		return Result;
	}

	// Extract transcription result
	FString Text;
	if (JsonObject->TryGetStringField(TEXT("text"), Text))
	{
		Result.Text = Text;
		Result.bSuccess = true;
	}
	else
	{
		Result.bSuccess = false;
		Result.ErrorMessage = TEXT("No text field in response");
		return Result;
	}

	// Extract optional fields
	double Confidence = 0.0;
	if (JsonObject->TryGetNumberField(TEXT("confidence"), Confidence))
	{
		Result.Confidence = (float)Confidence;
	}

	FString Language;
	if (JsonObject->TryGetStringField(TEXT("language"), Language))
	{
		Result.LanguageCode = Language;
	}

	return Result;
}
