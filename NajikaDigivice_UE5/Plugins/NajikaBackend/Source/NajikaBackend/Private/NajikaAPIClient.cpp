// NajikaAPIClient.cpp
// Implementation of Najika Backend HTTP Client

#include "NajikaAPIClient.h"
#include "HttpModule.h"
#include "Interfaces/IHttpResponse.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

void UNajikaAPIClient::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    UE_LOG(LogTemp, Log, TEXT("[Najika] API Client initialized - Backend: %s"), *BackendURL);
}

void UNajikaAPIClient::Deinitialize()
{
    UE_LOG(LogTemp, Log, TEXT("[Najika] API Client shutting down"));
    Super::Deinitialize();
}

// ============================================
// HTTP HELPERS
// ============================================

void UNajikaAPIClient::SendGETRequest(const FString& Endpoint, TFunction<void(FHttpResponsePtr)> OnSuccess)
{
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(BackendURL + Endpoint);
    Request->SetVerb(TEXT("GET"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

    Request->OnProcessRequestComplete().BindLambda(
        [this, OnSuccess](FHttpRequestPtr Req, FHttpResponsePtr Res, bool bSuccess)
        {
            OnRequestComplete(Req, Res, bSuccess, OnSuccess);
        });

    Request->ProcessRequest();
}

void UNajikaAPIClient::SendPOSTRequest(const FString& Endpoint, const FString& JsonBody, TFunction<void(FHttpResponsePtr)> OnSuccess)
{
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(BackendURL + Endpoint);
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request->SetContentAsString(JsonBody);

    Request->OnProcessRequestComplete().BindLambda(
        [this, OnSuccess](FHttpRequestPtr Req, FHttpResponsePtr Res, bool bSuccess)
        {
            OnRequestComplete(Req, Res, bSuccess, OnSuccess);
        });

    Request->ProcessRequest();
}

void UNajikaAPIClient::OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess, TFunction<void(FHttpResponsePtr)> OnSuccess)
{
    if (!bSuccess || !Response.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("[Najika] HTTP Request failed!"));
        OnAPIError.Broadcast(TEXT("Connection failed - Is backend running on port 8000?"));
        return;
    }

    int32 ResponseCode = Response->GetResponseCode();
    if (ResponseCode != 200)
    {
        UE_LOG(LogTemp, Warning, TEXT("[Najika] HTTP Response Code: %d"), ResponseCode);
        OnAPIError.Broadcast(FString::Printf(TEXT("Server error: %d"), ResponseCode));
        return;
    }

    // Success!
    if (OnSuccess)
    {
        OnSuccess(Response);
    }
}

TSharedPtr<FJsonObject> UNajikaAPIClient::ParseJsonResponse(const FString& JsonString)
{
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

    if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("[Najika] Failed to parse JSON response"));
        return nullptr;
    }

    return JsonObject;
}

// ============================================
// CORE CHAT
// ============================================

void UNajikaAPIClient::SendChatMessage(const FString& Message)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("message"), Message);
    JsonObject->SetStringField(TEXT("player_id"), PlayerId);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendPOSTRequest(TEXT("/api/chat"), JsonBody, [this](FHttpResponsePtr Response)
    {
        FString ResponseStr = Response->GetContentAsString();
        TSharedPtr<FJsonObject> Json = ParseJsonResponse(ResponseStr);

        if (Json.IsValid())
        {
            FString ResponseText = Json->GetStringField(TEXT("response"));
            FString Mood = Json->HasField(TEXT("mood")) ? Json->GetStringField(TEXT("mood")) : TEXT("neutral");

            UE_LOG(LogTemp, Log, TEXT("[Najika] Chat response: %s (Mood: %s)"), *ResponseText, *Mood);
            OnChatResponse.Broadcast(ResponseText, Mood);
        }
    });
}

void UNajikaAPIClient::GetChatHistory()
{
    SendGETRequest(TEXT("/api/chat/history"), [this](FHttpResponsePtr Response)
    {
        // Broadcast raw JSON for now
        OnNajikaStatusReceived.Broadcast(Response->GetContentAsString());
    });
}

// ============================================
// NAJIKA STATUS
// ============================================

void UNajikaAPIClient::GetNajikaStatus()
{
    SendGETRequest(TEXT("/api/najika/status"), [this](FHttpResponsePtr Response)
    {
        OnNajikaStatusReceived.Broadcast(Response->GetContentAsString());
    });
}

void UNajikaAPIClient::FeedNajika()
{
    SendPOSTRequest(TEXT("/api/najika/feed"), TEXT("{}"), [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Fed! Response: %s"), *Response->GetContentAsString());
        GetNajikaStatus(); // Refresh status
    });
}

void UNajikaAPIClient::GiveDrink()
{
    SendPOSTRequest(TEXT("/api/najika/drink"), TEXT("{}"), [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Gave drink!"));
        GetNajikaStatus();
    });
}

void UNajikaAPIClient::WashNajika()
{
    SendPOSTRequest(TEXT("/api/najika/wash"), TEXT("{}"), [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Washed!"));
        GetNajikaStatus();
    });
}

void UNajikaAPIClient::SleepNajika()
{
    SendPOSTRequest(TEXT("/api/najika/sleep"), TEXT("{}"), [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Sleeping!"));
        GetNajikaStatus();
    });
}

void UNajikaAPIClient::PraiseNajika()
{
    SendPOSTRequest(TEXT("/api/najika/praise"), TEXT("{}"), [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Praised! Bond increased!"));
        GetNajikaStatus();
    });
}

// ============================================
// BATTLE SYSTEM
// ============================================

void UNajikaAPIClient::StartBattle(const FString& EnemyId)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("enemy_id"), EnemyId);
    JsonObject->SetStringField(TEXT("player_id"), PlayerId);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendPOSTRequest(TEXT("/api/battle/start"), JsonBody, [this](FHttpResponsePtr Response)
    {
        FString ResponseStr = Response->GetContentAsString();
        UE_LOG(LogTemp, Log, TEXT("[Najika] Battle started!"));
        OnBattleUpdate.Broadcast(ResponseStr, true);
    });
}

void UNajikaAPIClient::GetBattleStatus()
{
    SendGETRequest(TEXT("/api/battle/status"), [this](FHttpResponsePtr Response)
    {
        FString ResponseStr = Response->GetContentAsString();
        TSharedPtr<FJsonObject> Json = ParseJsonResponse(ResponseStr);

        if (Json.IsValid())
        {
            bool bIsPlayerTurn = Json->HasField(TEXT("turn")) && Json->GetStringField(TEXT("turn")) == TEXT("player");
            OnBattleUpdate.Broadcast(ResponseStr, bIsPlayerTurn);
        }
    });
}

void UNajikaAPIClient::BattleAction(const FString& ActionType, const FString& TargetId)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("action"), ActionType);
    if (!TargetId.IsEmpty())
    {
        JsonObject->SetStringField(TEXT("target"), TargetId);
    }

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendPOSTRequest(TEXT("/api/battle/action"), JsonBody, [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Battle action executed!"));
        GetBattleStatus();
    });
}

void UNajikaAPIClient::UseSkill(const FString& SkillId)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("skill_id"), SkillId);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendPOSTRequest(TEXT("/api/skill/use"), JsonBody, [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Skill used!"));
        GetBattleStatus();
    });
}

// ============================================
// QUEST SYSTEM
// ============================================

void UNajikaAPIClient::GetActiveQuests()
{
    SendGETRequest(TEXT("/api/quests/active"), [this](FHttpResponsePtr Response)
    {
        OnQuestUpdate.Broadcast(Response->GetContentAsString());
    });
}

void UNajikaAPIClient::GetAvailableQuests()
{
    SendGETRequest(TEXT("/api/quests/available"), [this](FHttpResponsePtr Response)
    {
        OnQuestUpdate.Broadcast(Response->GetContentAsString());
    });
}

void UNajikaAPIClient::StartQuest(const FString& QuestId)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("quest_id"), QuestId);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendPOSTRequest(TEXT("/api/quests/start"), JsonBody, [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Quest started!"));
        GetActiveQuests();
    });
}

void UNajikaAPIClient::CompleteQuest(const FString& QuestId)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("quest_id"), QuestId);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendPOSTRequest(TEXT("/api/quests/complete"), JsonBody, [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Quest completed!"));
        GetActiveQuests();
    });
}

// ============================================
// SHOP & ECONOMY
// ============================================

void UNajikaAPIClient::GetPlayerGold()
{
    SendGETRequest(TEXT("/api/player/gold"), [this](FHttpResponsePtr Response)
    {
        OnNajikaStatusReceived.Broadcast(Response->GetContentAsString());
    });
}

void UNajikaAPIClient::BuyItem(const FString& ItemId, int32 Quantity)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("item_id"), ItemId);
    JsonObject->SetNumberField(TEXT("quantity"), Quantity);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendPOSTRequest(TEXT("/api/shop/buy"), JsonBody, [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Item purchased!"));
    });
}

// ============================================
// CONFIGURATION
// ============================================

void UNajikaAPIClient::SetBackendURL(const FString& URL)
{
    // SECURITY: Only allow localhost!
    if (!URL.Contains(TEXT("127.0.0.1")) && !URL.Contains(TEXT("localhost")))
    {
        UE_LOG(LogTemp, Error, TEXT("[Najika] SECURITY: Only localhost URLs allowed!"));
        OnAPIError.Broadcast(TEXT("SECURITY: Only localhost URLs allowed!"));
        return;
    }

    BackendURL = URL;
    UE_LOG(LogTemp, Log, TEXT("[Najika] Backend URL set to: %s"), *BackendURL);
}

void UNajikaAPIClient::CheckBackendConnection()
{
    SendGETRequest(TEXT("/api/status"), [this](FHttpResponsePtr Response)
    {
        UE_LOG(LogTemp, Log, TEXT("[Najika] Backend connection OK!"));
        OnNajikaStatusReceived.Broadcast(TEXT("{\"connected\": true}"));
    });
}
