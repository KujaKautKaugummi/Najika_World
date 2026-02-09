// NajikaAPIClient.h
// HTTP Client für Najika World Backend API
// Kopiere diese Datei nach: Source/NajikaWorld/
//
// WICHTIG: Port 8000! (8 Gebote!)

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "NajikaAPITypes.h"
#include "NajikaAPIClient.generated.h"

UCLASS(ClassGroup=(Najika), meta=(BlueprintSpawnableComponent))
class NAJIKAWORLD_API UNajikaAPIClient : public UActorComponent
{
    GENERATED_BODY()

public:
    UNajikaAPIClient();

    // ========================================================================
    // KONFIGURATION
    // ========================================================================

    /** Backend URL - IMMER 127.0.0.1:8000! (8 Gebote!) */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Config")
    FString BaseURL = TEXT("http://127.0.0.1:8000");

    /** Timeout in Sekunden */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Config")
    float RequestTimeout = 10.0f;

    /** Auth Token (für Owner-Features) */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Config")
    FString AuthToken;

    // ========================================================================
    // CHAT API
    // ========================================================================

    /** Chat mit Najika senden */
    UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
    void SendChat(const FString& Message, bool bPrivateMode, FOnChatResponse OnSuccess, FOnAPIError OnError);

    /** Prüfen ob Backend läuft */
    UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
    void CheckHealth(FOnAPIError OnResult);

    // ========================================================================
    // COMBAT API (Two-Hand System)
    // ========================================================================

    /** Angriff ausführen (Q/E System) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Combat")
    void Attack(ECombatHand Hand, EAttackType AttackType, const FString& TargetId, FOnCombatResult OnSuccess, FOnAPIError OnError);

    /** Waffe ausrüsten */
    UFUNCTION(BlueprintCallable, Category = "Najika|Combat")
    void EquipWeapon(const FString& WeaponId, ECombatHand Hand, FOnAPIError OnResult);

    /** Combo ausführen (Dual Attack) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Combat")
    void DualAttack(EAttackType AttackType, const FString& TargetId, FOnCombatResult OnSuccess, FOnAPIError OnError);

    // ========================================================================
    // COMPANION API (Najika)
    // ========================================================================

    /** Najika's Status abrufen */
    UFUNCTION(BlueprintCallable, Category = "Najika|Companion")
    void GetCompanionStatus(FOnCompanionStatus OnSuccess, FOnAPIError OnError);

    /** Aktivität mit Najika */
    UFUNCTION(BlueprintCallable, Category = "Najika|Companion")
    void DoActivity(const FString& Activity, int32 DurationMinutes, FOnAPIError OnResult);

    /** Geschenk geben */
    UFUNCTION(BlueprintCallable, Category = "Najika|Companion")
    void GiveGift(const FString& ItemId, FOnAPIError OnResult);

    /** Najika angreifen lassen */
    UFUNCTION(BlueprintCallable, Category = "Najika|Companion")
    void CompanionAttack(const FString& TargetId, FOnCombatResult OnSuccess, FOnAPIError OnError);

    // ========================================================================
    // MIMIK API (Kuja's Character)
    // ========================================================================

    /** Mimik-Status abrufen */
    UFUNCTION(BlueprintCallable, Category = "Najika|Mimik")
    void GetMimikStatus(FOnMimikStatus OnSuccess, FOnAPIError OnError);

    /** Form wechseln (Truhe/Mensch) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Mimik")
    void TransformMimik(EMimikForm TargetForm, FOnAPIError OnResult);

    /** Verstecken (nur als Truhe) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Mimik")
    void HideMimik(FOnAPIError OnResult);

    /** Mimik-Fähigkeit nutzen */
    UFUNCTION(BlueprintCallable, Category = "Najika|Mimik")
    void UseMimikAbility(const FString& AbilityId, const FString& TargetId, FOnCombatResult OnSuccess, FOnAPIError OnError);

    /** Ziel fressen (Mimik-Truhe exklusiv!) */
    UFUNCTION(BlueprintCallable, Category = "Najika|Mimik")
    void EatTarget(const FString& TargetId, FOnAPIError OnResult);

    // ========================================================================
    // STAT TRAINING API (Learning by Doing!)
    // ========================================================================

    /** Stat trainieren durch Aktivität */
    UFUNCTION(BlueprintCallable, Category = "Najika|Training")
    void TrainStat(ETrainableStat Stat, const FString& Activity, FOnTrainingResult OnSuccess, FOnAPIError OnError);

    /** Training-Status abrufen */
    UFUNCTION(BlueprintCallable, Category = "Najika|Training")
    void GetTrainingStatus(FOnAPIError OnResult);

    // ========================================================================
    // GAME STATE API
    // ========================================================================

    /** Spielstand speichern */
    UFUNCTION(BlueprintCallable, Category = "Najika|Game")
    void SaveGame(FOnAPIError OnResult);

    /** Spielstand laden */
    UFUNCTION(BlueprintCallable, Category = "Najika|Game")
    void LoadGame(FOnAPIError OnResult);

    // ========================================================================
    // INVENTORY API
    // ========================================================================

    /** Inventar abrufen */
    UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
    void GetInventory(FOnAPIError OnResult);

    /** Item benutzen */
    UFUNCTION(BlueprintCallable, Category = "Najika|Inventory")
    void UseItem(const FString& ItemId, FOnAPIError OnResult);

protected:
    virtual void BeginPlay() override;

private:
    // ========================================================================
    // INTERNE HELPER
    // ========================================================================

    /** HTTP Request erstellen und senden */
    void SendRequest(const FString& Endpoint, const FString& Verb, const FString& Content,
        TFunction<void(FHttpResponsePtr Response, bool bSuccess)> Callback);

    /** JSON String erstellen */
    FString MakeJSON(const TMap<FString, FString>& Params);

    /** Response zu Chat parsen */
    FNajikaChatResponse ParseChatResponse(const FString& JSON);

    /** Response zu Combat parsen */
    FNajikaCombatResult ParseCombatResponse(const FString& JSON);

    /** Response zu Companion parsen */
    FNajikaCompanionStatus ParseCompanionResponse(const FString& JSON);

    /** Response zu Mimik parsen */
    FMimikStatus ParseMimikResponse(const FString& JSON);

    /** Response zu Training parsen */
    FStatTrainingResult ParseTrainingResponse(const FString& JSON);

    /** Hand Enum zu String */
    FString HandToString(ECombatHand Hand);

    /** Attack Type Enum zu String */
    FString AttackTypeToString(EAttackType Type);

    /** Stat Enum zu String */
    FString StatToString(ETrainableStat Stat);

    /** Form Enum zu String */
    FString FormToString(EMimikForm Form);
};
