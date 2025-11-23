// NajikaHUD.cpp - HUD implementation
#include "NajikaHUD.h"
#include "Engine/Canvas.h"
ANajikaHUD::ANajikaHUD() { }
void ANajikaHUD::BeginPlay() { Super::BeginPlay(); }
void ANajikaHUD::DrawHUD() {
    Super::DrawHUD();
    if (!bShowHUD) return;
    DrawHealthBar();
    DrawStaminaBar();
    DrawManaBar();
}
void ANajikaHUD::DrawHealthBar() {
    if (!Canvas) return;
    float BarWidth = 200.0f;
    float BarHeight = 20.0f;
    float X = 20.0f;
    float Y = 20.0f;
    DrawRect(FLinearColor::Red, X, Y, BarWidth * (CurrentHealth / MaxHealth), BarHeight);
}
void ANajikaHUD::DrawStaminaBar() {
    if (!Canvas) return;
    float BarWidth = 200.0f;
    float BarHeight = 15.0f;
    float X = 20.0f;
    float Y = 45.0f;
    DrawRect(FLinearColor::Green, X, Y, BarWidth * (CurrentStamina / MaxStamina), BarHeight);
}
void ANajikaHUD::DrawManaBar() {
    if (!Canvas) return;
    float BarWidth = 200.0f;
    float BarHeight = 15.0f;
    float X = 20.0f;
    float Y = 65.0f;
    DrawRect(FLinearColor::Blue, X, Y, BarWidth * (CurrentMana / MaxMana), BarHeight);
}
void ANajikaHUD::ShowNotification(const FString& Message) {
    OnNotificationShown.Broadcast(Message);
}
