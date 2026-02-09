// NajikaVoiceClient.cpp
// Voice Call implementation with WebSocket

#include "NajikaVoiceClient.h"
#include "HttpModule.h"
#include "Interfaces/IHttpResponse.h"
#include "WebSocketsModule.h"
#include "Misc/Base64.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

void UNajikaVoiceClient::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Client initialized"));
}

void UNajikaVoiceClient::Deinitialize()
{
    if (bIsCallActive)
    {
        EndVoiceCall();
    }
    DisconnectWebSocket();
    Super::Deinitialize();
}

// ============================================
// VOICE CALL MANAGEMENT
// ============================================

void UNajikaVoiceClient::StartVoiceCall()
{
    if (bIsCallActive)
    {
        UE_LOG(LogTemp, Warning, TEXT("[Najika Voice] Call already active!"));
        return;
    }

    // Start call via HTTP
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("player_id"), TEXT("player_1"));

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendHTTPRequest(TEXT("/api/voice_call/start"), TEXT("POST"), JsonBody,
        [this](FHttpResponsePtr Response)
        {
            FString ResponseStr = Response->GetContentAsString();

            TSharedPtr<FJsonObject> Json;
            TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ResponseStr);

            if (FJsonSerializer::Deserialize(Reader, Json) && Json.IsValid())
            {
                CurrentSessionId = Json->GetStringField(TEXT("session_id"));
                bIsCallActive = true;

                UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Call started! Session: %s"), *CurrentSessionId);
                OnVoiceCallStarted.Broadcast(CurrentSessionId);

                // Connect WebSocket for real-time audio
                ConnectWebSocket();

                // Play greeting audio if provided
                if (Json->HasField(TEXT("greeting_audio")))
                {
                    FString GreetingBase64 = Json->GetStringField(TEXT("greeting_audio"));
                    TArray<uint8> GreetingAudio = DecodeBase64Audio(GreetingBase64);
                    FString GreetingText = Json->HasField(TEXT("greeting_text")) ?
                        Json->GetStringField(TEXT("greeting_text")) : TEXT("Hallo Mr. K!");

                    OnVoiceResponse.Broadcast(GreetingText, GreetingAudio);
                }
            }
        });
}

void UNajikaVoiceClient::EndVoiceCall()
{
    if (!bIsCallActive)
    {
        return;
    }

    // Disconnect WebSocket
    DisconnectWebSocket();

    // End call via HTTP
    SendHTTPRequest(TEXT("/api/voice_call/end"), TEXT("POST"), TEXT("{}"),
        [this](FHttpResponsePtr Response)
        {
            UE_LOG(LogTemp, Log, TEXT("[Najika Voice] Call ended"));
        });

    bIsCallActive = false;
    CurrentSessionId.Empty();
    OnVoiceCallEnded.Broadcast();
}

void UNajikaVoiceClient::SendAudio(const TArray<uint8>& AudioData)
{
    if (!bIsCallActive)
    {
        UE_LOG(LogTemp, Warning, TEXT("[Najika Voice] No active call!"));
        return;
    }

    // Encode audio to Base64
    FString AudioBase64 = EncodeAudioBase64(AudioData);

    // Send via HTTP (or WebSocket for lower latency)
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("audio"), AudioBase64);
    JsonObject->SetStringField(TEXT("format"), TEXT("wav"));
    JsonObject->SetStringField(TEXT("session_id"), CurrentSessionId);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendHTTPRequest(TEXT("/api/voice_call/audio"), TEXT("POST"), JsonBody,
        [this](FHttpResponsePtr Response)
        {
            FString ResponseStr = Response->GetContentAsString();

            TSharedPtr<FJsonObject> Json;
            TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ResponseStr);

            if (FJsonSerializer::Deserialize(Reader, Json) && Json.IsValid())
            {
                // Get transcription
                if (Json->HasField(TEXT("transcription")))
                {
                    FString Transcription = Json->GetStringField(TEXT("transcription"));
                    OnTranscription.Broadcast(Transcription);
                }

                // Get response
                FString ResponseText = Json->HasField(TEXT("response_text")) ?
                    Json->GetStringField(TEXT("response_text")) : TEXT("");

                // Get response audio
                TArray<uint8> ResponseAudio;
                if (Json->HasField(TEXT("response_audio")))
                {
                    FString AudioBase64 = Json->GetStringField(TEXT("response_audio"));
                    ResponseAudio = DecodeBase64Audio(AudioBase64);
                }

                if (!ResponseText.IsEmpty())
                {
                    OnVoiceResponse.Broadcast(ResponseText, ResponseAudio);
                }
            }
        });
}

void UNajikaVoiceClient::RequestTTS(const FString& Text)
{
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetStringField(TEXT("text"), Text);

    FString JsonBody;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

    SendHTTPRequest(TEXT("/api/tts"), TEXT("POST"), JsonBody,
        [this, Text](FHttpResponsePtr Response)
        {
            FString ResponseStr = Response->GetContentAsString();

            TSharedPtr<FJsonObject> Json;
            TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(ResponseStr);

            if (FJsonSerializer::Deserialize(Reader, Json) && Json.IsValid())
            {
                if (Json->HasField(TEXT("audio")))
                {
                    FString AudioBase64 = Json->GetStringField(TEXT("audio"));
                    TArray<uint8> AudioData = DecodeBase64Audio(AudioBase64);
                    OnVoiceResponse.Broadcast(Text, AudioData);
                }
            }
        });
}

// ============================================
// HTTP HELPERS
// ============================================

void UNajikaVoiceClient::SendHTTPRequest(const FString& Endpoint, const FString& Verb, const FString& Content,
                                          TFunction<void(FHttpResponsePtr)> OnSuccess)
{
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(BackendURL + Endpoint);
    Request->SetVerb(Verb);
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request->SetContentAsString(Content);

    Request->OnProcessRequestComplete().BindLambda(
        [OnSuccess](FHttpRequestPtr Req, FHttpResponsePtr Res, bool bSuccess)
        {
            if (bSuccess && Res.IsValid() && Res->GetResponseCode() == 200)
            {
                if (OnSuccess)
                {
                    OnSuccess(Res);
                }
            }
            else
            {
                UE_LOG(LogTemp, Error, TEXT("[Najika Voice] HTTP Request failed"));
            }
        });

    Request->ProcessRequest();
}

// ============================================
// WEBSOCKET
// ============================================

void UNajikaVoiceClient::ConnectWebSocket()
{
    FString WebSocketURL = TEXT("ws://127.0.0.1:8000/voice/ws/") + CurrentSessionId;

    WebSocket = FWebSocketsModule::Get().CreateWebSocket(WebSocketURL, TEXT("ws"));

    WebSocket->OnConnected().AddUObject(this, &UNajikaVoiceClient::OnWebSocketConnected);
    WebSocket->OnMessage().AddUObject(this, &UNajikaVoiceClient::OnWebSocketMessage);
    WebSocket->OnClosed().AddUObject(this, &UNajikaVoiceClient::OnWebSocketClosed);
    WebSocket->OnConnectionError().AddUObject(this, &UNajikaVoiceClient::OnWebSocketError);

    WebSocket->Connect();
}

void UNajikaVoiceClient::DisconnectWebSocket()
{
    if (WebSocket.IsValid())
    {
        if (WebSocket->IsConnected())
        {
            WebSocket->Close();
        }
        WebSocket.Reset();
    }
    bIsConnected = false;
}

void UNajikaVoiceClient::OnWebSocketConnected()
{
    bIsConnected = true;
    UE_LOG(LogTemp, Log, TEXT("[Najika Voice] WebSocket connected!"));
}

void UNajikaVoiceClient::OnWebSocketMessage(const FString& Message)
{
    TSharedPtr<FJsonObject> Json;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Message);

    if (FJsonSerializer::Deserialize(Reader, Json) && Json.IsValid())
    {
        FString Type = Json->HasField(TEXT("type")) ? Json->GetStringField(TEXT("type")) : TEXT("");

        if (Type == TEXT("audio"))
        {
            FString AudioBase64 = Json->GetStringField(TEXT("audio"));
            TArray<uint8> AudioData = DecodeBase64Audio(AudioBase64);
            FString Text = Json->HasField(TEXT("text")) ? Json->GetStringField(TEXT("text")) : TEXT("");
            OnVoiceResponse.Broadcast(Text, AudioData);
        }
        else if (Type == TEXT("transcription"))
        {
            FString Transcription = Json->GetStringField(TEXT("text"));
            OnTranscription.Broadcast(Transcription);
        }
    }
}

void UNajikaVoiceClient::OnWebSocketClosed(int32 StatusCode, const FString& Reason, bool bWasClean)
{
    bIsConnected = false;
    UE_LOG(LogTemp, Log, TEXT("[Najika Voice] WebSocket closed: %s"), *Reason);
}

void UNajikaVoiceClient::OnWebSocketError(const FString& Error)
{
    UE_LOG(LogTemp, Error, TEXT("[Najika Voice] WebSocket error: %s"), *Error);
}

// ============================================
// AUDIO HELPERS
// ============================================

TArray<uint8> UNajikaVoiceClient::DecodeBase64Audio(const FString& Base64String)
{
    TArray<uint8> DecodedData;
    FBase64::Decode(Base64String, DecodedData);
    return DecodedData;
}

FString UNajikaVoiceClient::EncodeAudioBase64(const TArray<uint8>& AudioData)
{
    return FBase64::Encode(AudioData);
}
