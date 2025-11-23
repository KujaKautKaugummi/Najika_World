// SlimeArena.h
// Section 2.7: HANDYSPIEL (Prototyping Section - CRITICAL!)
// Assist-/Auto-Modus + Slime-Arena (Digimon-style "Anfeuern")

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SlimeArena.generated.h"

// Battle Mode
UENUM(BlueprintType)
enum class EBattleMode : uint8
{
    BM_Manual UMETA(DisplayName = "Manual (Full Control)"),
    BM_Assist UMETA(DisplayName = "Assist (Player + AI Support)"),
    BM_Auto UMETA(DisplayName = "Auto (AI Control)")
};

// Anfeuern (Cheering) Types
UENUM(BlueprintType)
enum class EAnfeuernType : uint8
{
    AT_Attack UMETA(DisplayName = "Angriff!"),
    AT_Defend UMETA(DisplayName = "Verteidigung!"),
    AT_Heal UMETA(DisplayName = "Heilen!"),
    AT_Special UMETA(DisplayName = "Spezial-Move!"),
    AT_Retreat UMETA(DisplayName = "Zurückziehen!"),
    AT_AllOut UMETA(DisplayName = "Volles Risiko!")
};

// Slime Stats
USTRUCT(BlueprintType)
struct FSlimeStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FString SlimeName = "Slime";

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Level = 1;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float MaxHealth = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float CurrentHealth = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Attack = 10.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Defense = 10.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Speed = 10.0f;

    // Move Set
    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FString> Moves;

    // AI Behavior (learned from battles)
    UPROPERTY(BlueprintReadWrite)
    TMap<FString, float> MovePreferences;

    // Win/Loss Record
    UPROPERTY(BlueprintReadOnly)
    int32 Wins = 0;

    UPROPERTY(BlueprintReadOnly)
    int32 Losses = 0;
};

// Battle State
USTRUCT(BlueprintType)
struct FBattleState
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FSlimeStats PlayerSlime;

    UPROPERTY(BlueprintReadWrite)
    FSlimeStats OpponentSlime;

    UPROPERTY(BlueprintReadWrite)
    EBattleMode BattleMode = EBattleMode::BM_Manual;

    UPROPERTY(BlueprintReadWrite)
    int32 TurnNumber = 0;

    UPROPERTY(BlueprintReadWrite)
    bool bBattleActive = false;

    UPROPERTY(BlueprintReadWrite)
    FString LastPlayerAction;

    UPROPERTY(BlueprintReadWrite)
    FString LastOpponentAction;
};

// Anfeuern Buff
USTRUCT(BlueprintType)
struct FAnfeuernBuff
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    EAnfeuernType Type;

    UPROPERTY(BlueprintReadWrite)
    float AttackBonus = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    float DefenseBonus = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    float SpeedBonus = 0.0f;

    UPROPERTY(BlueprintReadWrite)
    float Duration = 3.0f;

    UPROPERTY(BlueprintReadWrite)
    float TimeRemaining = 0.0f;
};

// Meta-Learning Data (Anonymized)
USTRUCT(BlueprintType)
struct FSlimeMetaData
{
    GENERATED_BODY()

    // Aggregate statistics WITHOUT identifiable info
    UPROPERTY(BlueprintReadOnly)
    TMap<FString, int32> MoveUsageCount;

    UPROPERTY(BlueprintReadOnly)
    TMap<FString, float> MoveSuccessRate;

    UPROPERTY(BlueprintReadOnly)
    TMap<FString, float> MoveAverageDamage;

    // NO player IDs, NO identifying data
    // Only aggregate patterns for AI learning
};

UCLASS()
class NAJIKATEST_API ASlimeArena : public AActor
{
    GENERATED_BODY()

public:
    ASlimeArena();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;

    // ========== BATTLE MANAGEMENT ==========

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Battle")
    void StartBattle(const FSlimeStats& PlayerSlime, const FSlimeStats& OpponentSlime, EBattleMode Mode);

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Battle")
    void EndBattle(bool bPlayerWon);

    UFUNCTION(BlueprintPure, Category = "SlimeArena|Battle")
    bool IsBattleActive() const { return CurrentBattle.bBattleActive; }

    UFUNCTION(BlueprintPure, Category = "SlimeArena|Battle")
    FBattleState GetCurrentBattle() const { return CurrentBattle; }

    // ========== ASSIST MODE (Anfeuern) ==========

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Assist")
    void Anfeuern(EAnfeuernType Type);

    UFUNCTION(BlueprintPure, Category = "SlimeArena|Assist")
    TArray<FAnfeuernBuff> GetActiveBuffs() const { return ActiveBuffs; }

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Assist")
    void ExecutePlayerMove(const FString& MoveName);

    // ========== AUTO MODE ==========

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Auto")
    void EnableAutoMode();

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Auto")
    void DisableAutoMode();

    UFUNCTION(BlueprintPure, Category = "SlimeArena|Auto")
    bool IsAutoModeEnabled() const { return CurrentBattle.BattleMode == EBattleMode::BM_Auto; }

    // ========== AI DECISION MAKING ==========

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|AI")
    FString DecideAIMove(const FSlimeStats& Slime, const FSlimeStats& Opponent);

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|AI")
    void ExecuteAITurn();

    // ========== META-LEARNING ==========

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Learning")
    void RecordBattleData(const FString& MoveName, bool bWasSuccessful, float Damage);

    UFUNCTION(BlueprintPure, Category = "SlimeArena|Learning")
    FSlimeMetaData GetMetaLearningData() const { return MetaData; }

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|Learning")
    void UpdateAIFromMetaData();

    // ========== REGISTRATION (API) ==========

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|API")
    void RegisterSlime(const FSlimeStats& Slime);

    UFUNCTION(BlueprintCallable, Category = "SlimeArena|API")
    void RequestDuel(const FString& OpponentSlimeName);

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SlimeArena|Config")
    float AnfeuernCooldown = 5.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SlimeArena|Config")
    float TurnDuration = 3.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SlimeArena|Config")
    bool bEnableMetaLearning = true;

    // PvE/PvP Brackets (Hard Rule #4)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SlimeArena|Config")
    bool bUseSeparatePvPScaling = true;

    // ========== STATE ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SlimeArena|State")
    FBattleState CurrentBattle;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SlimeArena|State")
    TArray<FAnfeuernBuff> ActiveBuffs;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SlimeArena|State")
    float LastAnfeuernTime = 0.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SlimeArena|State")
    float TurnTimer = 0.0f;

    // ========== META-LEARNING DATA ==========

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SlimeArena|Learning")
    FSlimeMetaData MetaData;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "SlimeArena|Learning")
    TMap<FString, FSlimeStats> RegisteredSlimes;

private:
    // ========== HELPER FUNCTIONS ==========

    void UpdateBuffs(float DeltaTime);
    void ApplyAnfeuernBuff(EAnfeuernType Type);
    void ExecuteMove(FSlimeStats& Attacker, FSlimeStats& Defender, const FString& MoveName);
    float CalculateDamage(const FSlimeStats& Attacker, const FSlimeStats& Defender, const FString& MoveName);

    // ========== AI HELPERS ==========

    FString SelectBestMove(const FSlimeStats& Slime, const FSlimeStats& Opponent);
    float EvaluateMoveEffectiveness(const FString& MoveName, const FSlimeStats& Opponent) const;
};
