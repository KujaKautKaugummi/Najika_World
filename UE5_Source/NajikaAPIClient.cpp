// NajikaAPIClient.cpp
// HTTP Client Implementation für Najika World Backend API
// Kopiere diese Datei nach: Source/NajikaWorld/

#include "NajikaAPIClient.h"
#include "HttpModule.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

UNajikaAPIClient::UNajikaAPIClient()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UNajikaAPIClient::BeginPlay()
{
    Super::BeginPlay();

    // Prüfen ob Backend erreichbar ist
    UE_LOG(LogTemp, Log, TEXT("NajikaAPIClient: Initialisiert mit Backend %s"), *BaseURL);
}

// ============================================================================
// INTERNE HELPER
// ============================================================================

void UNajikaAPIClient::SendRequest(const FString& Endpoint, const FString& Verb, const FString& Content,
    TFunction<void(FHttpResponsePtr Response, bool bSuccess)> Callback)
{
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();

    Request->SetURL(BaseURL + Endpoint);
    Request->SetVerb(Verb);
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));

    if (!AuthToken.IsEmpty())
    {
        Request->SetHeader(TEXT("Authorization"), FString::Printf(TEXT("Bearer %s"), *AuthToken));
    }

    if (!Content.IsEmpty())
    {
        Request->SetContentAsString(Content);
    }

    Request->SetTimeout(RequestTimeout);

    Request->OnProcessRequestComplete().BindLambda(
        [Callback](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bConnectedSuccessfully)
        {
            Callback(Response, bConnectedSuccessfully && Response.IsValid() && Response->GetResponseCode() == 200);
        });

    Request->ProcessRequest();
}

FString UNajikaAPIClient::MakeJSON(const TMap<FString, FString>& Params)
{
    FString Result = TEXT("{");
    bool bFirst = true;

    for (const auto& Pair : Params)
    {
        if (!bFirst) Result += TEXT(",");
        Result += FString::Printf(TEXT("\"%s\":\"%s\""), *Pair.Key, *Pair.Value);
        bFirst = false;
    }

    Result += TEXT("}");
    return Result;
}

FString UNajikaAPIClient::HandToString(ECombatHand Hand)
{
    switch (Hand)
    {
        case ECombatHand::Left: return TEXT("left");
        case ECombatHand::Right: return TEXT("right");
        case ECombatHand::Both: return TEXT("both");
        default: return TEXT("left");
    }
}

FString UNajikaAPIClient::AttackTypeToString(EAttackType Type)
{
    return Type == EAttackType::Heavy ? TEXT("heavy") : TEXT("light");
}

FString UNajikaAPIClient::StatToString(ETrainableStat Stat)
{
    switch (Stat)
    {
        case ETrainableStat::Strength: return TEXT("strength");
        case ETrainableStat::Perception: return TEXT("perception");
        case ETrainableStat::Endurance: return TEXT("endurance");
        case ETrainableStat::Charisma: return TEXT("charisma");
        case ETrainableStat::Intelligence: return TEXT("intelligence");
        case ETrainableStat::Agility: return TEXT("agility");
        case ETrainableStat::Luck: return TEXT("luck");
        default: return TEXT("strength");
    }
}

FString UNajikaAPIClient::FormToString(EMimikForm Form)
{
    return Form == EMimikForm::Human ? TEXT("human") : TEXT("chest");
}

// ============================================================================
// PARSER
// ============================================================================

FNajikaChatResponse UNajikaAPIClient::ParseChatResponse(const FString& JSON)
{
    FNajikaChatResponse Result;

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JSON);

    if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
    {
        Result.Response = JsonObject->GetStringField(TEXT("response"));
        Result.Mode = JsonObject->GetStringField(TEXT("mode"));
        Result.Emotion = JsonObject->GetStringField(TEXT("emotion"));
        Result.ModelUsed = JsonObject->GetStringField(TEXT("model_used"));
    }

    return Result;
}

FNajikaCombatResult UNajikaAPIClient::ParseCombatResponse(const FString& JSON)
{
    FNajikaCombatResult Result;

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JSON);

    if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
    {
        Result.bSuccess = JsonObject->GetBoolField(TEXT("success"));
        Result.Damage = JsonObject->GetNumberField(TEXT("damage"));
        Result.bCritical = JsonObject->GetBoolField(TEXT("critical"));
        Result.ComboCount = JsonObject->GetIntegerField(TEXT("combo_count"));
        Result.Animation = JsonObject->GetStringField(TEXT("animation"));
        Result.Message = JsonObject->GetStringField(TEXT("message"));
    }

    return Result;
}

FNajikaCompanionStatus UNajikaAPIClient::ParseCompanionResponse(const FString& JSON)
{
    FNajikaCompanionStatus Result;

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JSON);

    if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
    {
        FString PersonalityStr = JsonObject->GetStringField(TEXT("active_personality"));
        if (PersonalityStr == TEXT("megumin")) Result.ActivePersonality = ENajikaPersonality::Megumin;
        else if (PersonalityStr == TEXT("harley")) Result.ActivePersonality = ENajikaPersonality::Harley;
        else if (PersonalityStr == TEXT("shiro")) Result.ActivePersonality = ENajikaPersonality::Shiro;
        else if (PersonalityStr == TEXT("melissa")) Result.ActivePersonality = ENajikaPersonality::Melissa;

        Result.Mood = JsonObject->GetStringField(TEXT("mood"));
        Result.RelationshipLevel = JsonObject->GetIntegerField(TEXT("relationship_level"));
        Result.RelationshipName = JsonObject->GetStringField(TEXT("relationship_name"));

        const TSharedPtr<FJsonObject>* CombatStyle;
        if (JsonObject->TryGetObjectField(TEXT("combat_style"), CombatStyle))
        {
            Result.CombatStyleName = (*CombatStyle)->GetStringField(TEXT("name"));
            Result.DamageBonus = (*CombatStyle)->GetNumberField(TEXT("damage_bonus"));
            Result.DodgeBonus = (*CombatStyle)->GetNumberField(TEXT("dodge_bonus"));
        }
    }

    return Result;
}

FMimikStatus UNajikaAPIClient::ParseMimikResponse(const FString& JSON)
{
    FMimikStatus Result;

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JSON);

    if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
    {
        FString FormStr = JsonObject->GetStringField(TEXT("current_form"));
        Result.CurrentForm = FormStr == TEXT("human") ? EMimikForm::Human : EMimikForm::Chest;

        Result.bIsHidden = JsonObject->GetBoolField(TEXT("is_hidden"));
        Result.NajikaBond = JsonObject->GetIntegerField(TEXT("najika_bond"));

        const TArray<TSharedPtr<FJsonValue>>* StomachArray;
        if (JsonObject->TryGetArrayField(TEXT("stomach_contents"), StomachArray))
        {
            for (const auto& Item : *StomachArray)
            {
                Result.StomachContents.Add(Item->AsString());
            }
        }

        const TSharedPtr<FJsonObject>* Abilities;
        if (JsonObject->TryGetObjectField(TEXT("abilities"), Abilities))
        {
            const TArray<TSharedPtr<FJsonValue>>* UnlockedArray;
            if ((*Abilities)->TryGetArrayField(TEXT("unlocked"), UnlockedArray))
            {
                for (const auto& Ability : *UnlockedArray)
                {
                    Result.UnlockedAbilities.Add(Ability->AsString());
                }
            }
        }
    }

    return Result;
}

FStatTrainingResult UNajikaAPIClient::ParseTrainingResponse(const FString& JSON)
{
    FStatTrainingResult Result;

    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JSON);

    if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
    {
        Result.bSuccess = JsonObject->GetBoolField(TEXT("success"));
        Result.StatName = JsonObject->GetStringField(TEXT("stat"));
        Result.OldValue = JsonObject->GetNumberField(TEXT("old_value"));
        Result.NewValue = JsonObject->GetNumberField(TEXT("new_value"));
        Result.XPGained = JsonObject->GetNumberField(TEXT("xp_gained"));
        Result.Message = JsonObject->GetStringField(TEXT("message"));
        Result.TrainingsToday = JsonObject->GetIntegerField(TEXT("trainings_today"));
        Result.MaxTrainingsPerDay = JsonObject->GetIntegerField(TEXT("max_trainings"));
    }

    return Result;
}

// ============================================================================
// CHAT API
// ============================================================================

void UNajikaAPIClient::SendChat(const FString& Message, bool bPrivateMode, FOnChatResponse OnSuccess, FOnAPIError OnError)
{
    FString Mode = bPrivateMode ? TEXT("private") : TEXT("public");
    FString Content = FString::Printf(TEXT("{\"message\":\"%s\",\"mode\":\"%s\"}"), *Message, *Mode);

    SendRequest(TEXT("/api/chat"), TEXT("POST"), Content,
        [this, OnSuccess, OnError](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                FNajikaChatResponse ChatResponse = ParseChatResponse(Response->GetContentAsString());
                OnSuccess.ExecuteIfBound(ChatResponse);
            }
            else
            {
                OnError.ExecuteIfBound(TEXT("Chat request failed"));
            }
        });
}

void UNajikaAPIClient::CheckHealth(FOnAPIError OnResult)
{
    SendRequest(TEXT("/api/chat/health"), TEXT("GET"), TEXT(""),
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                OnResult.ExecuteIfBound(TEXT("Backend is running!"));
            }
            else
            {
                OnResult.ExecuteIfBound(TEXT("ERROR: Backend not reachable on port 8000!"));
            }
        });
}

// ============================================================================
// COMBAT API
// ============================================================================

void UNajikaAPIClient::Attack(ECombatHand Hand, EAttackType AttackType, const FString& TargetId,
    FOnCombatResult OnSuccess, FOnAPIError OnError)
{
    FString Content = FString::Printf(
        TEXT("{\"hand\":\"%s\",\"attack_type\":\"%s\",\"target_id\":\"%s\"}"),
        *HandToString(Hand),
        *AttackTypeToString(AttackType),
        *TargetId
    );

    SendRequest(TEXT("/api/combat-hands/attack"), TEXT("POST"), Content,
        [this, OnSuccess, OnError](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                FNajikaCombatResult Result = ParseCombatResponse(Response->GetContentAsString());
                OnSuccess.ExecuteIfBound(Result);
            }
            else
            {
                OnError.ExecuteIfBound(TEXT("Attack request failed"));
            }
        });
}

void UNajikaAPIClient::EquipWeapon(const FString& WeaponId, ECombatHand Hand, FOnAPIError OnResult)
{
    FString Content = FString::Printf(
        TEXT("{\"weapon_id\":\"%s\",\"hand\":\"%s\"}"),
        *WeaponId,
        *HandToString(Hand)
    );

    SendRequest(TEXT("/api/combat-hands/equip"), TEXT("POST"), Content,
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            OnResult.ExecuteIfBound(bSuccess ? TEXT("Weapon equipped!") : TEXT("ERROR: Could not equip weapon"));
        });
}

void UNajikaAPIClient::DualAttack(EAttackType AttackType, const FString& TargetId,
    FOnCombatResult OnSuccess, FOnAPIError OnError)
{
    Attack(ECombatHand::Both, AttackType, TargetId, OnSuccess, OnError);
}

// ============================================================================
// COMPANION API
// ============================================================================

void UNajikaAPIClient::GetCompanionStatus(FOnCompanionStatus OnSuccess, FOnAPIError OnError)
{
    SendRequest(TEXT("/api/companion/najika"), TEXT("GET"), TEXT(""),
        [this, OnSuccess, OnError](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                FNajikaCompanionStatus Status = ParseCompanionResponse(Response->GetContentAsString());
                OnSuccess.ExecuteIfBound(Status);
            }
            else
            {
                OnError.ExecuteIfBound(TEXT("Could not get companion status"));
            }
        });
}

void UNajikaAPIClient::DoActivity(const FString& Activity, int32 DurationMinutes, FOnAPIError OnResult)
{
    FString Content = FString::Printf(
        TEXT("{\"activity\":\"%s\",\"duration_minutes\":%d}"),
        *Activity,
        DurationMinutes
    );

    SendRequest(TEXT("/api/companion/activity"), TEXT("POST"), Content,
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                OnResult.ExecuteIfBound(Response->GetContentAsString());
            }
            else
            {
                OnResult.ExecuteIfBound(TEXT("ERROR: Activity failed"));
            }
        });
}

void UNajikaAPIClient::GiveGift(const FString& ItemId, FOnAPIError OnResult)
{
    FString Content = FString::Printf(TEXT("{\"item_id\":\"%s\"}"), *ItemId);

    SendRequest(TEXT("/api/companion/gift"), TEXT("POST"), Content,
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            OnResult.ExecuteIfBound(bSuccess ? TEXT("Gift given!") : TEXT("ERROR: Could not give gift"));
        });
}

void UNajikaAPIClient::CompanionAttack(const FString& TargetId, FOnCombatResult OnSuccess, FOnAPIError OnError)
{
    FString Content = FString::Printf(TEXT("{\"target_id\":\"%s\"}"), *TargetId);

    SendRequest(TEXT("/api/companion/attack"), TEXT("POST"), Content,
        [this, OnSuccess, OnError](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                FNajikaCombatResult Result = ParseCombatResponse(Response->GetContentAsString());
                OnSuccess.ExecuteIfBound(Result);
            }
            else
            {
                OnError.ExecuteIfBound(TEXT("Companion attack failed"));
            }
        });
}

// ============================================================================
// MIMIK API
// ============================================================================

void UNajikaAPIClient::GetMimikStatus(FOnMimikStatus OnSuccess, FOnAPIError OnError)
{
    SendRequest(TEXT("/api/mimik/status"), TEXT("GET"), TEXT(""),
        [this, OnSuccess, OnError](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                FMimikStatus Status = ParseMimikResponse(Response->GetContentAsString());
                OnSuccess.ExecuteIfBound(Status);
            }
            else
            {
                OnError.ExecuteIfBound(TEXT("Could not get Mimik status"));
            }
        });
}

void UNajikaAPIClient::TransformMimik(EMimikForm TargetForm, FOnAPIError OnResult)
{
    FString Content = FString::Printf(TEXT("{\"target_form\":\"%s\"}"), *FormToString(TargetForm));

    SendRequest(TEXT("/api/mimik/transform"), TEXT("POST"), Content,
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            OnResult.ExecuteIfBound(bSuccess ? TEXT("Transformation complete!") : TEXT("ERROR: Could not transform"));
        });
}

void UNajikaAPIClient::HideMimik(FOnAPIError OnResult)
{
    SendRequest(TEXT("/api/mimik/hide"), TEXT("POST"), TEXT("{}"),
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            OnResult.ExecuteIfBound(bSuccess ? TEXT("Now hidden!") : TEXT("ERROR: Could not hide"));
        });
}

void UNajikaAPIClient::UseMimikAbility(const FString& AbilityId, const FString& TargetId,
    FOnCombatResult OnSuccess, FOnAPIError OnError)
{
    FString Content = FString::Printf(
        TEXT("{\"ability_id\":\"%s\",\"target_id\":\"%s\"}"),
        *AbilityId,
        *TargetId
    );

    SendRequest(TEXT("/api/mimik/ability"), TEXT("POST"), Content,
        [this, OnSuccess, OnError](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                FNajikaCombatResult Result = ParseCombatResponse(Response->GetContentAsString());
                OnSuccess.ExecuteIfBound(Result);
            }
            else
            {
                OnError.ExecuteIfBound(TEXT("Mimik ability failed"));
            }
        });
}

void UNajikaAPIClient::EatTarget(const FString& TargetId, FOnAPIError OnResult)
{
    FString Content = FString::Printf(TEXT("{\"target_id\":\"%s\",\"target_type\":\"enemy\"}"), *TargetId);

    SendRequest(TEXT("/api/mimik/eat"), TEXT("POST"), Content,
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            OnResult.ExecuteIfBound(bSuccess ? TEXT("*CHOMP* Target eaten!") : TEXT("ERROR: Could not eat target"));
        });
}

// ============================================================================
// STAT TRAINING API
// ============================================================================

void UNajikaAPIClient::TrainStat(ETrainableStat Stat, const FString& Activity,
    FOnTrainingResult OnSuccess, FOnAPIError OnError)
{
    FString Content = FString::Printf(
        TEXT("{\"stat\":\"%s\",\"activity\":\"%s\"}"),
        *StatToString(Stat),
        *Activity
    );

    SendRequest(TEXT("/api/stat-training/train"), TEXT("POST"), Content,
        [this, OnSuccess, OnError](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                FStatTrainingResult Result = ParseTrainingResponse(Response->GetContentAsString());
                OnSuccess.ExecuteIfBound(Result);
            }
            else
            {
                OnError.ExecuteIfBound(TEXT("Training failed"));
            }
        });
}

void UNajikaAPIClient::GetTrainingStatus(FOnAPIError OnResult)
{
    SendRequest(TEXT("/api/stat-training/status"), TEXT("GET"), TEXT(""),
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                OnResult.ExecuteIfBound(Response->GetContentAsString());
            }
            else
            {
                OnResult.ExecuteIfBound(TEXT("ERROR: Could not get training status"));
            }
        });
}

// ============================================================================
// GAME STATE API
// ============================================================================

void UNajikaAPIClient::SaveGame(FOnAPIError OnResult)
{
    SendRequest(TEXT("/game/save"), TEXT("POST"), TEXT("{}"),
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            OnResult.ExecuteIfBound(bSuccess ? TEXT("Game saved!") : TEXT("ERROR: Could not save game"));
        });
}

void UNajikaAPIClient::LoadGame(FOnAPIError OnResult)
{
    SendRequest(TEXT("/game/load"), TEXT("POST"), TEXT("{}"),
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                OnResult.ExecuteIfBound(TEXT("Game loaded!"));
            }
            else
            {
                OnResult.ExecuteIfBound(TEXT("ERROR: Could not load game"));
            }
        });
}

// ============================================================================
// INVENTORY API
// ============================================================================

void UNajikaAPIClient::GetInventory(FOnAPIError OnResult)
{
    SendRequest(TEXT("/game/inventory"), TEXT("GET"), TEXT(""),
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            if (bSuccess)
            {
                OnResult.ExecuteIfBound(Response->GetContentAsString());
            }
            else
            {
                OnResult.ExecuteIfBound(TEXT("ERROR: Could not get inventory"));
            }
        });
}

void UNajikaAPIClient::UseItem(const FString& ItemId, FOnAPIError OnResult)
{
    FString Content = FString::Printf(TEXT("{\"action\":\"use\",\"item_id\":\"%s\"}"), *ItemId);

    SendRequest(TEXT("/game/inventory/action"), TEXT("POST"), Content,
        [OnResult](FHttpResponsePtr Response, bool bSuccess)
        {
            OnResult.ExecuteIfBound(bSuccess ? TEXT("Item used!") : TEXT("ERROR: Could not use item"));
        });
}
