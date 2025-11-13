// Copyright Claude Code. All Rights Reserved.

#include "NajikaHttpClient.h"
#include "Http.h"
#include "Json.h"
#include "JsonUtilities.h"

UNajikaHttpClient::UNajikaHttpClient()
{
	BaseURL = TEXT("http://127.0.0.1:8000");
}

void UNajikaHttpClient::Initialize(const FString& InBaseURL)
{
	BaseURL = InBaseURL;
	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Initialized with BaseURL: %s"), *BaseURL);
}

// ============================================================
// CHAT & CONVERSATION
// ============================================================

void UNajikaHttpClient::SendChatMessage(const FString& Message, FOnNajikaChatResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("message"), Message);
	JsonObject->SetStringField(TEXT("user"), TEXT("User"));

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/chat");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnChatRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaHttpClient] Request Body: %s"), *JsonString);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetChatHistory(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/chat/history"), OnResponse);
}

void UNajikaHttpClient::GetBondStatus(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/bond/status"), OnResponse);
}

// ============================================================
// NAJIKA CARE SYSTEM
// ============================================================

void UNajikaHttpClient::GetNajikaStatus(FOnNajikaStatusResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/status");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnStatusRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("GET"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] GET %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::FeedNajika(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/feed");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GiveDrink(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/drink");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::WashNajika(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/wash");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::PutToSleep(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/sleep");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::TrainNajika(const FString& TrainingType, FOnNajikaActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("type"), TrainingType);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/train");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Training: %s"), *URL, *TrainingType);

	Request->ProcessRequest();
}

void UNajikaHttpClient::PraiseNajika(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/praise");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::ScoldNajika(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/scold");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

// ============================================================
// EQUIPMENT SYSTEM
// ============================================================

void UNajikaHttpClient::EquipItem(const FString& ItemID, const FString& Slot, FOnNajikaActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("item_id"), ItemID);
	JsonObject->SetStringField(TEXT("slot"), Slot);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/equip");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Item: %s, Slot: %s"), *URL, *ItemID, *Slot);

	Request->ProcessRequest();
}

void UNajikaHttpClient::UnequipItem(const FString& Slot, FOnNajikaActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("slot"), Slot);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/najika/unequip");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Slot: %s"), *URL, *Slot);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetEquipment(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/najika/equipment"), OnResponse);
}

// ============================================================
// BATTLE SYSTEM
// ============================================================

void UNajikaHttpClient::StartBattle(FOnBattleStartResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/battle/start");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnBattleStartRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetBattleStatus(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/battle/status"), OnResponse);
}

void UNajikaHttpClient::BattleAction(const FString& ActionType, int32 Target, const FString& SkillID, const FString& ItemID, FOnBattleActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("action"), ActionType);
	JsonObject->SetNumberField(TEXT("target"), Target);
	if (!SkillID.IsEmpty())
	{
		JsonObject->SetStringField(TEXT("skill_id"), SkillID);
	}
	if (!ItemID.IsEmpty())
	{
		JsonObject->SetStringField(TEXT("item_id"), ItemID);
	}

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/battle/action");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnBattleActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Action: %s, Target: %d"), *URL, *ActionType, Target);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetBattleSkills(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/battle/skills"), OnResponse);
}

void UNajikaHttpClient::ResetBattle(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/battle/reset");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

// ============================================================
// VOICE CALL SYSTEM
// ============================================================

void UNajikaHttpClient::StartVoiceCall(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/voice_call/start");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::SendVoiceCallAudio(const FString& AudioDataBase64, FOnVoiceCallAudioResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("audio_data"), AudioDataBase64);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/voice_call/audio");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnVoiceCallAudioRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Audio Data Size: %d bytes"), *URL, AudioDataBase64.Len());

	Request->ProcessRequest();
}

void UNajikaHttpClient::EndVoiceCall(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/voice_call/end");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(TEXT("{}"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetVoiceCallStats(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/voice_call/stats"), OnResponse);
}

// ============================================================
// LIVING SYSTEM (AUTONOMY)
// ============================================================

void UNajikaHttpClient::GetLivingState(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/living/state"), OnResponse);
}

void UNajikaHttpClient::CheckProactiveMessage(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/living/proactive"), OnResponse);
}

void UNajikaHttpClient::CheckActivityCompletion(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/living/activity/check"), OnResponse);
}

void UNajikaHttpClient::StartActivity(const FString& Activity, FOnNajikaActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("activity"), Activity);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/living/activity/start");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Activity: %s"), *URL, *Activity);

	Request->ProcessRequest();
}

// ============================================================
// SYSTEM STATUS
// ============================================================

void UNajikaHttpClient::GetSystemStatus(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/status"), OnResponse);
}

void UNajikaHttpClient::GetRooms(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/rooms"), OnResponse);
}

void UNajikaHttpClient::SaveState(FOnNajikaActionResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/save");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("GET"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] GET %s"), *URL);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetCompleteState(FOnNajikaHTTPResponse OnResponse)
{
	GetRequest(TEXT("/api/state"), OnResponse);
}

// ============================================================
// MINI-GAMES
// ============================================================

void UNajikaHttpClient::SubmitRhythmScore(int32 Score, float Accuracy, FOnNajikaActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetNumberField(TEXT("score"), Score);
	JsonObject->SetNumberField(TEXT("accuracy"), Accuracy);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/minigame/rhythm");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Score: %d, Accuracy: %.2f"), *URL, Score, Accuracy);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GardenAction(const FString& Action, const FString& ItemID, FOnNajikaActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetStringField(TEXT("action"), Action);
	JsonObject->SetStringField(TEXT("item"), ItemID);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/minigame/garden");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Action: %s, Item: %s"), *URL, *Action, *ItemID);

	Request->ProcessRequest();
}

void UNajikaHttpClient::SubmitReflexScore(int32 ReactionTimeMS, FOnNajikaActionResponse OnResponse)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
	JsonObject->SetNumberField(TEXT("reaction_time_ms"), ReactionTimeMS);

	FString JsonString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + TEXT("/api/minigame/reflex");

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnActionRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonString);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s - Reaction Time: %dms"), *URL, ReactionTimeMS);

	Request->ProcessRequest();
}

// ============================================================
// GENERIC HTTP METHODS
// ============================================================

void UNajikaHttpClient::PostRequest(const FString& Endpoint, const FString& JsonData, FOnNajikaHTTPResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + Endpoint;

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("POST"));
	Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
	Request->SetContentAsString(JsonData);

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] POST %s"), *URL);
	UE_LOG(LogTemp, Verbose, TEXT("[NajikaHttpClient] Request Body: %s"), *JsonData);

	Request->ProcessRequest();
}

void UNajikaHttpClient::GetRequest(const FString& Endpoint, FOnNajikaHTTPResponse OnResponse)
{
	FHttpModule* Http = &FHttpModule::Get();
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = Http->CreateRequest();

	FString URL = BaseURL + Endpoint;

	Request->OnProcessRequestComplete().BindUObject(this, &UNajikaHttpClient::OnRequestComplete, OnResponse);
	Request->SetURL(URL);
	Request->SetVerb(TEXT("GET"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] GET %s"), *URL);

	Request->ProcessRequest();
}

// ============================================================
// INTERNAL CALLBACK HANDLERS
// ============================================================

void UNajikaHttpClient::OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaHTTPResponse Callback)
{
	FNajikaAPIResponse APIResponse;

	if (bWasSuccessful && Response.IsValid())
	{
		APIResponse.bSuccess = true;
		APIResponse.StatusCode = Response->GetResponseCode();
		APIResponse.Data = Response->GetContentAsString();
		APIResponse.Message = TEXT("Request successful");

		UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Response Code: %d"), APIResponse.StatusCode);
		UE_LOG(LogTemp, Verbose, TEXT("[NajikaHttpClient] Response Body: %s"), *APIResponse.Data);
	}
	else
	{
		APIResponse.bSuccess = false;
		APIResponse.StatusCode = Response.IsValid() ? Response->GetResponseCode() : 0;
		APIResponse.Message = TEXT("Request failed");
		APIResponse.ErrorMessage = Response.IsValid() ? Response->GetContentAsString() : TEXT("No response");

		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Request failed! Status: %d"), APIResponse.StatusCode);
	}

	Callback.ExecuteIfBound(APIResponse);
}

void UNajikaHttpClient::OnChatRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaChatResponse Callback)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Chat request failed!"));
		Callback.ExecuteIfBound(TEXT(""), FNajikaState(), FNajikaLivingState());
		return;
	}

	FString ResponseString = Response->GetContentAsString();
	TSharedPtr<FJsonObject> JsonObject = ParseJsonResponse(ResponseString);

	if (!JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Failed to parse chat response JSON"));
		Callback.ExecuteIfBound(TEXT(""), FNajikaState(), FNajikaLivingState());
		return;
	}

	FString NajikaResponse = JsonObject->GetStringField(TEXT("response"));

	// Parse Najika state
	FNajikaState NajikaState;
	if (JsonObject->HasField(TEXT("najika_state")))
	{
		TSharedPtr<FJsonObject> StateObject = JsonObject->GetObjectField(TEXT("najika_state"));
		NajikaState = ParseNajikaState(StateObject);
	}

	// Parse Living state
	FNajikaLivingState LivingState;
	if (JsonObject->HasField(TEXT("living_state")))
	{
		TSharedPtr<FJsonObject> LivingObject = JsonObject->GetObjectField(TEXT("living_state"));
		LivingState = ParseLivingState(LivingObject);
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Chat Response: %s"), *NajikaResponse);

	Callback.ExecuteIfBound(NajikaResponse, NajikaState, LivingState);
}

void UNajikaHttpClient::OnStatusRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaStatusResponse Callback)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Status request failed!"));
		Callback.ExecuteIfBound(FNajikaState(), FNajikaLivingState());
		return;
	}

	FString ResponseString = Response->GetContentAsString();
	TSharedPtr<FJsonObject> JsonObject = ParseJsonResponse(ResponseString);

	if (!JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Failed to parse status response JSON"));
		Callback.ExecuteIfBound(FNajikaState(), FNajikaLivingState());
		return;
	}

	// Parse Najika state
	FNajikaState NajikaState;
	if (JsonObject->HasField(TEXT("najika")))
	{
		TSharedPtr<FJsonObject> StateObject = JsonObject->GetObjectField(TEXT("najika"));
		NajikaState = ParseNajikaState(StateObject);
	}

	// Parse Living state
	FNajikaLivingState LivingState;
	if (JsonObject->HasField(TEXT("living_state")))
	{
		TSharedPtr<FJsonObject> LivingObject = JsonObject->GetObjectField(TEXT("living_state"));
		LivingState = ParseLivingState(LivingObject);
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Status Retrieved - HP: %.1f, Hunger: %.1f"), NajikaState.Happiness, NajikaState.Hunger);

	Callback.ExecuteIfBound(NajikaState, LivingState);
}

void UNajikaHttpClient::OnActionRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnNajikaActionResponse Callback)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Action request failed!"));
		Callback.ExecuteIfBound(false, TEXT("Request failed"));
		return;
	}

	FString ResponseString = Response->GetContentAsString();
	TSharedPtr<FJsonObject> JsonObject = ParseJsonResponse(ResponseString);

	if (!JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Failed to parse action response JSON"));
		Callback.ExecuteIfBound(false, TEXT("Invalid JSON response"));
		return;
	}

	bool bSuccess = JsonObject->GetBoolField(TEXT("ok"));
	FString Message = JsonObject->GetStringField(TEXT("msg"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Action Result: %s - %s"), bSuccess ? TEXT("SUCCESS") : TEXT("FAIL"), *Message);

	Callback.ExecuteIfBound(bSuccess, Message);
}

void UNajikaHttpClient::OnBattleStartRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnBattleStartResponse Callback)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Battle start request failed!"));
		Callback.ExecuteIfBound(FNajikaBattleState(), TArray<FNajikaEnemy>());
		return;
	}

	FString ResponseString = Response->GetContentAsString();
	TSharedPtr<FJsonObject> JsonObject = ParseJsonResponse(ResponseString);

	if (!JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Failed to parse battle start response JSON"));
		Callback.ExecuteIfBound(FNajikaBattleState(), TArray<FNajikaEnemy>());
		return;
	}

	// Parse battle state
	FNajikaBattleState BattleState;
	BattleState.bActive = true;
	BattleState.Wave = JsonObject->GetIntegerField(TEXT("wave"));
	BattleState.HP = JsonObject->GetIntegerField(TEXT("player_hp"));
	BattleState.MaxHP = JsonObject->GetIntegerField(TEXT("player_max_hp"));

	// Parse enemies
	TArray<FNajikaEnemy> Enemies = ParseEnemies(JsonObject->GetField<EJson::Array>(TEXT("enemies")));
	BattleState.EnemyCount = Enemies.Num();

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Battle Started - Wave: %d, Enemies: %d"), BattleState.Wave, BattleState.EnemyCount);

	Callback.ExecuteIfBound(BattleState, Enemies);
}

void UNajikaHttpClient::OnBattleActionRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnBattleActionResponse Callback)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Battle action request failed!"));
		Callback.ExecuteIfBound(FNajikaBattleState(), 0, false);
		return;
	}

	FString ResponseString = Response->GetContentAsString();
	TSharedPtr<FJsonObject> JsonObject = ParseJsonResponse(ResponseString);

	if (!JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Failed to parse battle action response JSON"));
		Callback.ExecuteIfBound(FNajikaBattleState(), 0, false);
		return;
	}

	int32 DamageDealt = JsonObject->GetIntegerField(TEXT("damage_dealt"));
	bool bEnemyDefeated = JsonObject->GetBoolField(TEXT("enemy_defeated"));

	// Parse updated battle state
	FNajikaBattleState BattleState;
	if (JsonObject->HasField(TEXT("battle_state")))
	{
		TSharedPtr<FJsonObject> StateObject = JsonObject->GetObjectField(TEXT("battle_state"));
		BattleState = ParseBattleState(StateObject);
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Battle Action - Damage: %d, Enemy Defeated: %s"), DamageDealt, bEnemyDefeated ? TEXT("YES") : TEXT("NO"));

	Callback.ExecuteIfBound(BattleState, DamageDealt, bEnemyDefeated);
}

void UNajikaHttpClient::OnVoiceCallAudioRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FOnVoiceCallAudioResponse Callback)
{
	if (!bWasSuccessful || !Response.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Voice call audio request failed!"));
		Callback.ExecuteIfBound(TEXT(""), TEXT(""), TEXT(""));
		return;
	}

	FString ResponseString = Response->GetContentAsString();
	TSharedPtr<FJsonObject> JsonObject = ParseJsonResponse(ResponseString);

	if (!JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Failed to parse voice call audio response JSON"));
		Callback.ExecuteIfBound(TEXT(""), TEXT(""), TEXT(""));
		return;
	}

	FString TranscribedText = JsonObject->GetStringField(TEXT("text"));
	FString NajikaResponse = JsonObject->GetStringField(TEXT("response_text"));
	FString ResponseAudioBase64 = JsonObject->GetStringField(TEXT("response_audio"));

	UE_LOG(LogTemp, Log, TEXT("[NajikaHttpClient] Voice Call - STT: %s, Response: %s"), *TranscribedText, *NajikaResponse);

	Callback.ExecuteIfBound(TranscribedText, NajikaResponse, ResponseAudioBase64);
}

// ============================================================
// HELPER FUNCTIONS (JSON Parsing)
// ============================================================

TSharedPtr<FJsonObject> UNajikaHttpClient::ParseJsonResponse(const FString& JsonString)
{
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

	if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaHttpClient] Failed to parse JSON: %s"), *JsonString);
		return nullptr;
	}

	return JsonObject;
}

FNajikaState UNajikaHttpClient::ParseNajikaState(TSharedPtr<FJsonObject> JsonObject)
{
	FNajikaState State;

	if (!JsonObject.IsValid())
	{
		return State;
	}

	// Needs
	State.Hunger = JsonObject->GetNumberField(TEXT("hunger"));
	State.Thirst = JsonObject->GetNumberField(TEXT("thirst"));
	State.Energy = JsonObject->GetNumberField(TEXT("energy"));
	State.Hygiene = JsonObject->GetNumberField(TEXT("hygiene"));
	State.Happiness = JsonObject->GetNumberField(TEXT("happiness"));

	// Stats
	State.Strength = JsonObject->GetIntegerField(TEXT("strength"));
	State.Intelligence = JsonObject->GetIntegerField(TEXT("intelligence"));
	State.Dexterity = JsonObject->GetIntegerField(TEXT("dexterity"));
	State.Charisma = JsonObject->GetIntegerField(TEXT("charisma"));

	// Care
	State.CareMistakes = JsonObject->GetIntegerField(TEXT("care_mistakes"));
	State.Fatigue = JsonObject->GetNumberField(TEXT("fatigue"));
	State.Weight = JsonObject->GetNumberField(TEXT("weight"));
	State.Discipline = JsonObject->GetNumberField(TEXT("discipline"));

	// Growth
	State.Level = JsonObject->GetIntegerField(TEXT("level"));
	State.XP = JsonObject->GetIntegerField(TEXT("xp"));
	State.EvolutionStage = JsonObject->GetStringField(TEXT("evolution_stage"));

	// Equipment
	if (JsonObject->HasField(TEXT("equipment")))
	{
		TSharedPtr<FJsonObject> EquipObject = JsonObject->GetObjectField(TEXT("equipment"));
		State.Equipment.Weapon = EquipObject->GetStringField(TEXT("weapon"));
		State.Equipment.Armor = EquipObject->GetStringField(TEXT("armor"));
		State.Equipment.Accessory = EquipObject->GetStringField(TEXT("accessory"));
	}

	// Timestamps
	State.LastFed = JsonObject->GetNumberField(TEXT("last_fed"));
	State.LastTrained = JsonObject->GetNumberField(TEXT("last_trained"));
	State.LastSleep = JsonObject->GetNumberField(TEXT("last_sleep"));
	State.LastUpdate = JsonObject->GetNumberField(TEXT("last_update"));

	return State;
}

FNajikaLivingState UNajikaHttpClient::ParseLivingState(TSharedPtr<FJsonObject> JsonObject)
{
	FNajikaLivingState State;

	if (!JsonObject.IsValid())
	{
		return State;
	}

	State.CurrentMood = JsonObject->GetStringField(TEXT("current_mood"));
	State.MoodIntensity = JsonObject->GetIntegerField(TEXT("mood_intensity"));
	State.LivingHunger = JsonObject->GetNumberField(TEXT("hunger"));
	State.LivingEnergy = JsonObject->GetNumberField(TEXT("energy"));
	State.MoodGame = JsonObject->GetNumberField(TEXT("mood_game"));
	State.AngerLevel = JsonObject->GetNumberField(TEXT("anger_level"));
	State.bAutoCareEnabled = JsonObject->GetBoolField(TEXT("auto_care_enabled"));
	State.ControlMode = JsonObject->GetStringField(TEXT("control_mode"));
	State.bPlayerOnline = JsonObject->GetBoolField(TEXT("player_online"));
	State.AutonomyLevel = JsonObject->GetIntegerField(TEXT("autonomy_level"));
	State.GrowthStage = JsonObject->GetStringField(TEXT("growth_stage"));
	State.RelationshipStage = JsonObject->GetStringField(TEXT("relationship_stage"));
	State.EmotionalBond = JsonObject->GetIntegerField(TEXT("emotional_bond"));
	State.CurrentActivity = JsonObject->GetStringField(TEXT("current_activity"));

	return State;
}

FNajikaBattleState UNajikaHttpClient::ParseBattleState(TSharedPtr<FJsonObject> JsonObject)
{
	FNajikaBattleState State;

	if (!JsonObject.IsValid())
	{
		return State;
	}

	State.bActive = JsonObject->GetBoolField(TEXT("active"));
	State.HP = JsonObject->GetIntegerField(TEXT("hp"));
	State.MaxHP = JsonObject->GetIntegerField(TEXT("max_hp"));
	State.Wave = JsonObject->GetIntegerField(TEXT("wave"));
	State.EnemyCount = JsonObject->GetIntegerField(TEXT("enemies"));

	return State;
}

TArray<FNajikaEnemy> UNajikaHttpClient::ParseEnemies(TSharedPtr<FJsonValue> JsonValue)
{
	TArray<FNajikaEnemy> Enemies;

	if (!JsonValue.IsValid() || JsonValue->Type != EJson::Array)
	{
		return Enemies;
	}

	TArray<TSharedPtr<FJsonValue>> EnemyArray = JsonValue->AsArray();

	for (const TSharedPtr<FJsonValue>& EnemyValue : EnemyArray)
	{
		if (EnemyValue->Type != EJson::Object)
		{
			continue;
		}

		TSharedPtr<FJsonObject> EnemyObject = EnemyValue->AsObject();

		FNajikaEnemy Enemy;
		Enemy.EnemyID = EnemyObject->GetStringField(TEXT("enemy_id"));
		Enemy.Name = EnemyObject->GetStringField(TEXT("name"));
		Enemy.HP = EnemyObject->GetIntegerField(TEXT("hp"));
		Enemy.MaxHP = EnemyObject->GetIntegerField(TEXT("max_hp"));
		Enemy.Attack = EnemyObject->GetIntegerField(TEXT("atk"));
		Enemy.Defense = EnemyObject->GetIntegerField(TEXT("def"));
		Enemy.bIsBoss = EnemyObject->HasField(TEXT("boss")) ? EnemyObject->GetBoolField(TEXT("boss")) : false;

		Enemies.Add(Enemy);
	}

	return Enemies;
}
