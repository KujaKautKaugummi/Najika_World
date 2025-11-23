// Copyright Model 1 - Najika Digivice APK

#include "NajikaAPIClient.h"
#include "HttpModule.h"
#include "JsonUtilities.h"

// ============================================
// CHAT SYSTEM
// ============================================

void UNajikaAPIClient::SendChatMessage(const FString& Message, FOnChatResponse Callback)
{
	// Create POST request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = CreateRequest(TEXT("/api/chat"), TEXT("POST"));

	// Create JSON body
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("message"), Message);

	// Serialize JSON
	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	// Set request body
	Request->SetContentAsString(JsonString);

	// Store delegate for callback
	ChatDelegates.Add(Request, Callback);

	// Send request
	Request->OnProcessRequestComplete().BindLambda(
		[this, Callback](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
		{
			if (!bWasSuccessful || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Chat request failed!"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ChatDelegates.Remove(Request);
				return;
			}

			// Parse JSON response
			TSharedPtr<FJsonObject> JsonResponse = ParseJSON(Response->GetContentAsString());
			if (!JsonResponse.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Failed to parse chat response JSON"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ChatDelegates.Remove(Request);
				return;
			}

			// Extract response text
			FString ResponseText = JsonResponse->GetStringField(TEXT("response"));
			bool bSuccess = JsonResponse->GetBoolField(TEXT("ok"));

			UE_LOG(LogTemp, Log, TEXT("[Najika] Chat response: %s"), *ResponseText);

			// Execute callback
			Callback.ExecuteIfBound(ResponseText, bSuccess);
			ChatDelegates.Remove(Request);
		}
	);

	Request->ProcessRequest();
}

// ============================================
// NAJIKA STATUS & CARE
// ============================================

void UNajikaAPIClient::GetNajikaStatus(FOnNajikaStatus Callback)
{
	// Create GET request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = CreateRequest(TEXT("/api/najika/status"), TEXT("GET"));

	// Store delegate for callback
	StatusDelegates.Add(Request, Callback);

	// Send request
	Request->OnProcessRequestComplete().BindLambda(
		[this, Callback](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
		{
			if (!bWasSuccessful || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Status request failed!"));
				Callback.ExecuteIfBound(0, 0, 0, false);
				StatusDelegates.Remove(Request);
				return;
			}

			// Parse JSON response
			TSharedPtr<FJsonObject> JsonResponse = ParseJSON(Response->GetContentAsString());
			if (!JsonResponse.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Failed to parse status response JSON"));
				Callback.ExecuteIfBound(0, 0, 0, false);
				StatusDelegates.Remove(Request);
				return;
			}

			// Extract status values
			int32 Hunger = JsonResponse->GetIntegerField(TEXT("hunger"));
			int32 Energy = JsonResponse->GetIntegerField(TEXT("energy"));
			int32 Happiness = JsonResponse->GetIntegerField(TEXT("happiness"));

			UE_LOG(LogTemp, Log, TEXT("[Najika] Status - Hunger: %d, Energy: %d, Happiness: %d"), Hunger, Energy, Happiness);

			// Execute callback
			Callback.ExecuteIfBound(Hunger, Energy, Happiness, true);
			StatusDelegates.Remove(Request);
		}
	);

	Request->ProcessRequest();
}

void UNajikaAPIClient::FeedNajika(FOnActionResponse Callback)
{
	// Create POST request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = CreateRequest(TEXT("/api/najika/feed"), TEXT("POST"));

	// Store delegate for callback
	ActionDelegates.Add(Request, Callback);

	// Send request
	Request->OnProcessRequestComplete().BindLambda(
		[this, Callback](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
		{
			if (!bWasSuccessful || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Feed request failed!"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ActionDelegates.Remove(Request);
				return;
			}

			// Parse JSON response
			TSharedPtr<FJsonObject> JsonResponse = ParseJSON(Response->GetContentAsString());
			if (!JsonResponse.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Failed to parse feed response JSON"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ActionDelegates.Remove(Request);
				return;
			}

			// Extract message (optional, may not exist)
			FString Message = JsonResponse->HasField(TEXT("message")) ?
				JsonResponse->GetStringField(TEXT("message")) : TEXT("Fed successfully!");
			bool bSuccess = JsonResponse->GetBoolField(TEXT("ok"));

			UE_LOG(LogTemp, Log, TEXT("[Najika] Feed response: %s"), *Message);

			// Execute callback
			Callback.ExecuteIfBound(Message, bSuccess);
			ActionDelegates.Remove(Request);
		}
	);

	Request->ProcessRequest();
}

void UNajikaAPIClient::GiveWaterToNajika(FOnActionResponse Callback)
{
	// Create POST request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = CreateRequest(TEXT("/api/najika/drink"), TEXT("POST"));

	// Store delegate for callback
	ActionDelegates.Add(Request, Callback);

	// Send request
	Request->OnProcessRequestComplete().BindLambda(
		[this, Callback](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
		{
			if (!bWasSuccessful || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Drink request failed!"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ActionDelegates.Remove(Request);
				return;
			}

			// Parse JSON response
			TSharedPtr<FJsonObject> JsonResponse = ParseJSON(Response->GetContentAsString());
			if (!JsonResponse.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Failed to parse drink response JSON"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ActionDelegates.Remove(Request);
				return;
			}

			// Extract message
			FString Message = JsonResponse->HasField(TEXT("message")) ?
				JsonResponse->GetStringField(TEXT("message")) : TEXT("Drink given successfully!");
			bool bSuccess = JsonResponse->GetBoolField(TEXT("ok"));

			UE_LOG(LogTemp, Log, TEXT("[Najika] Drink response: %s"), *Message);

			// Execute callback
			Callback.ExecuteIfBound(Message, bSuccess);
			ActionDelegates.Remove(Request);
		}
	);

	Request->ProcessRequest();
}

void UNajikaAPIClient::WashNajika(FOnActionResponse Callback)
{
	// Create POST request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = CreateRequest(TEXT("/api/najika/wash"), TEXT("POST"));

	// Store delegate for callback
	ActionDelegates.Add(Request, Callback);

	// Send request
	Request->OnProcessRequestComplete().BindLambda(
		[this, Callback](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
		{
			if (!bWasSuccessful || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Wash request failed!"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ActionDelegates.Remove(Request);
				return;
			}

			// Parse JSON response
			TSharedPtr<FJsonObject> JsonResponse = ParseJSON(Response->GetContentAsString());
			if (!JsonResponse.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Failed to parse wash response JSON"));
				Callback.ExecuteIfBound(TEXT(""), false);
				ActionDelegates.Remove(Request);
				return;
			}

			// Extract message
			FString Message = JsonResponse->HasField(TEXT("message")) ?
				JsonResponse->GetStringField(TEXT("message")) : TEXT("Wash complete!");
			bool bSuccess = JsonResponse->GetBoolField(TEXT("ok"));

			UE_LOG(LogTemp, Log, TEXT("[Najika] Wash response: %s"), *Message);

			// Execute callback
			Callback.ExecuteIfBound(Message, bSuccess);
			ActionDelegates.Remove(Request);
		}
	);

	Request->ProcessRequest();
}

// ============================================
// TEXT-TO-SPEECH
// ============================================

void UNajikaAPIClient::GenerateTTS(const FString& Text, FOnTTSResponse Callback)
{
	// Create POST request
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = CreateRequest(TEXT("/api/tts"), TEXT("POST"));

	// Create JSON body
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("text"), Text);

	// Serialize JSON
	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	// Set request body
	Request->SetContentAsString(JsonString);

	// Store delegate for callback
	TTSDelegates.Add(Request, Callback);

	// Send request
	Request->OnProcessRequestComplete().BindLambda(
		[this, Callback](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
		{
			if (!bWasSuccessful || !Response.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] TTS request failed!"));
				Callback.ExecuteIfBound(TEXT(""), false);
				TTSDelegates.Remove(Request);
				return;
			}

			// Parse JSON response
			TSharedPtr<FJsonObject> JsonResponse = ParseJSON(Response->GetContentAsString());
			if (!JsonResponse.IsValid())
			{
				UE_LOG(LogTemp, Error, TEXT("[Najika] Failed to parse TTS response JSON"));
				Callback.ExecuteIfBound(TEXT(""), false);
				TTSDelegates.Remove(Request);
				return;
			}

			// Extract audio path or base64 data
			FString AudioData = JsonResponse->GetStringField(TEXT("audio"));
			bool bSuccess = JsonResponse->GetBoolField(TEXT("ok"));

			UE_LOG(LogTemp, Log, TEXT("[Najika] TTS audio generated: %s"), *AudioData);

			// Execute callback
			Callback.ExecuteIfBound(AudioData, bSuccess);
			TTSDelegates.Remove(Request);
		}
	);

	Request->ProcessRequest();
}

// ============================================
// HELPER FUNCTIONS (Private)
// ============================================

TSharedRef<IHttpRequest, ESPMode::ThreadSafe> UNajikaAPIClient::CreateRequest(const FString& Endpoint, const FString& Verb)
{
	// Create HTTP request
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	// Set URL
	Request->SetURL(BaseURL + Endpoint);

	// Set HTTP verb
	Request->SetVerb(Verb);

	// Set headers
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetHeader(TEXT("Accept"), TEXT("application/json"));
	Request->SetHeader(TEXT("User-Agent"), TEXT("NajikaDigivice/1.0 (UnrealEngine)"));

	// Set timeout
	Request->SetTimeout(RequestTimeout);

	return Request;
}

TSharedPtr<FJsonObject> UNajikaAPIClient::ParseJSON(const FString& ResponseString)
{
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ResponseString);

	if (FJsonSerializer::Deserialize(Reader, JsonObject))
	{
		return JsonObject;
	}

	UE_LOG(LogTemp, Error, TEXT("[Najika] JSON Parse Error: %s"), *ResponseString);
	return nullptr;
}
