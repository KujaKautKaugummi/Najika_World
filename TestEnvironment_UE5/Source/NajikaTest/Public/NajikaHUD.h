// NajikaHUD.h
// UI System for Test Environment
// Displays: Health, Exhaustion, Charge, Talents, Signature Moves, etc.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "ExplosionClass.h"
#include "FortniteMovementComponent.h"
#include "SignaturePathsSystem.h"
#include "NajikaHUD.generated.h"

UCLASS()
class NAJIKATEST_API ANajikaHUD : public AHUD
{
    GENERATED_BODY()

public:
    ANajikaHUD();

    virtual void DrawHUD() override;

protected:
    virtual void BeginPlay() override;

public:
    // ========== HUD DRAWING ==========

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawHealthBar();

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawExhaustionBar();

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawChargeBar();

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawMovementState();

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawSignatureMoveCooldown();

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawIFrameIndicator();

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawTalentBonuses();

    UFUNCTION(BlueprintCallable, Category = "HUD")
    void DrawAbilityCooldowns();

    // ========== CROSSHAIR ==========

    UFUNCTION(BlueprintCallable, Category = "HUD|Crosshair")
    void DrawCrosshair();

    // ========== DAMAGE NUMBERS ==========

    UFUNCTION(BlueprintCallable, Category = "HUD|Damage")
    void ShowDamageNumber(FVector WorldLocation, float Damage, bool bIsCritical);

    // ========== NOTIFICATIONS ==========

    UFUNCTION(BlueprintCallable, Category = "HUD|Notifications")
    void ShowNotification(const FString& Message, float Duration, FLinearColor Color);

    // ========== DEBUG INFO ==========

    UFUNCTION(BlueprintCallable, Category = "HUD|Debug")
    void ToggleDebugInfo();

    UFUNCTION(BlueprintCallable, Category = "HUD|Debug")
    void DrawDebugInfo();

protected:
    // ========== CONFIGURATION ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Config")
    bool bShowHealthBar = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Config")
    bool bShowExhaustionBar = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Config")
    bool bShowChargeBar = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Config")
    bool bShowMovementState = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Config")
    bool bShowDebugInfo = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Config")
    bool bShowCrosshair = true;

    // ========== COLORS ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Colors")
    FLinearColor HealthColor = FLinearColor::Green;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Colors")
    FLinearColor ExhaustionColor = FLinearColor::Red;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Colors")
    FLinearColor ChargeColor = FLinearColor::Yellow;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Colors")
    FLinearColor IFrameColor = FLinearColor(0.0f, 1.0f, 1.0f, 1.0f);  // Cyan

    // ========== FONTS ==========

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Fonts")
    UFont* HUDFont;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HUD|Fonts")
    UFont* DamageFont;

    // ========== NOTIFICATIONS ==========

    USTRUCT()
    struct FHUDNotification
    {
        GENERATED_BODY()

        FString Message;
        float TimeRemaining;
        FLinearColor Color;
    };

    TArray<FHUDNotification> ActiveNotifications;

    // ========== DAMAGE NUMBERS ==========

    USTRUCT()
    struct FDamageNumber
    {
        GENERATED_BODY()

        FVector WorldLocation;
        FVector ScreenLocation;
        float Damage;
        bool bIsCritical;
        float TimeRemaining;
        float Offset;
    };

    TArray<FDamageNumber> ActiveDamageNumbers;

private:
    // ========== HELPER FUNCTIONS ==========

    void DrawProgressBar(float X, float Y, float Width, float Height, float Progress, FLinearColor Color, const FString& Label);
    void DrawText(const FString& Text, float X, float Y, FLinearColor Color, float Scale = 1.0f);
    void UpdateNotifications(float DeltaTime);
    void UpdateDamageNumbers(float DeltaTime);

    // ========== CACHED REFERENCES ==========

    UPROPERTY()
    AExplosionClass* CachedExplosionCharacter;

    UPROPERTY()
    UFortniteMovementComponent* CachedMovementComponent;

    UPROPERTY()
    ASignaturePathsSystem* CachedSignatureSystem;
};
