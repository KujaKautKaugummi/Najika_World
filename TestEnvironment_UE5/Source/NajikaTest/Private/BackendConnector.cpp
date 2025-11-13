// BackendConnector.cpp - Backend integration (Hard Rule #1 - 127.0.0.1 only!)
#include "BackendConnector.h"
#include "Http.h"
UBackendConnector::UBackendConnector() { PrimaryComponentTick.bCanEverTick = false; }
void UBackendConnector::BeginPlay() { Super::BeginPlay(); }
void UBackendConnector::ConnectToHub() {
    FString URL = HubURL + "/health";
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(URL);
    Request->SetVerb("GET");
    Request->OnProcessRequestComplete().BindUObject(this, &UBackendConnector::OnHealthCheckComplete);
    Request->ProcessRequest();
}
void UBackendConnector::OnHealthCheckComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful) {
    if (bWasSuccessful && Response.IsValid()) {
        OnConnectionSuccess.Broadcast();
    } else {
        OnConnectionFailed.Broadcast("Connection failed");
    }
}
void UBackendConnector::FetchAsset(const FString& AssetID) {
    FString URL = GameCoreURL + "/api/assets/" + AssetID;
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(URL);
    Request->SetVerb("GET");
    Request->ProcessRequest();
}
