// Copyright Najika Development Team. All Rights Reserved.

#include "OPTIONAL_NajikaBlueprintLibrary.h"
#include "Json.h"
#include "JsonUtilities.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/PlatformFilemanager.h"
#include "GenericPlatform/GenericPlatformMisc.h"
#include "GenericPlatform/GenericPlatformHttp.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/Engine.h"

// ============================================================================
// JSON UTILITIES
// ============================================================================

bool UNajikaBlueprintLibrary::ParseJsonToMap(const FString& JsonString, TMap<FString, FString>& OutMap)
{
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

	if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
	{
		return false;
	}

	OutMap.Empty();

	for (const auto& Pair : JsonObject->Values)
	{
		if (Pair.Value->Type == EJson::String)
		{
			OutMap.Add(Pair.Key, Pair.Value->AsString());
		}
		else if (Pair.Value->Type == EJson::Number)
		{
			OutMap.Add(Pair.Key, FString::SanitizeFloat(Pair.Value->AsNumber()));
		}
		else if (Pair.Value->Type == EJson::Boolean)
		{
			OutMap.Add(Pair.Key, Pair.Value->AsBool() ? TEXT("true") : TEXT("false"));
		}
	}

	return true;
}

FString UNajikaBlueprintLibrary::MapToJson(const TMap<FString, FString>& Map)
{
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject());

	for (const auto& Pair : Map)
	{
		JsonObject->SetStringField(Pair.Key, Pair.Value);
	}

	FString OutputString;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&OutputString);
	FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);

	return OutputString;
}

FString UNajikaBlueprintLibrary::GetJsonValue(const FString& JsonString, const FString& Key, const FString& DefaultValue)
{
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

	if (!FJsonSerializer::Deserialize(Reader, JsonObject) || !JsonObject.IsValid())
	{
		return DefaultValue;
	}

	FString Value;
	if (JsonObject->TryGetStringField(Key, Value))
	{
		return Value;
	}

	return DefaultValue;
}

bool UNajikaBlueprintLibrary::IsValidJson(const FString& JsonString)
{
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);
	return FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid();
}

// ============================================================================
// STRING UTILITIES
// ============================================================================

FString UNajikaBlueprintLibrary::TruncateString(const FString& String, int32 MaxLength, const FString& Ellipsis)
{
	if (String.Len() <= MaxLength)
	{
		return String;
	}

	return String.Left(MaxLength - Ellipsis.Len()) + Ellipsis;
}

FString UNajikaBlueprintLibrary::FormatNumberWithSeparator(int32 Number, const FString& Separator)
{
	FString NumberString = FString::FromInt(Number);
	FString Result;

	int32 Count = 0;
	for (int32 i = NumberString.Len() - 1; i >= 0; i--)
	{
		if (Count > 0 && Count % 3 == 0)
		{
			Result = Separator + Result;
		}
		Result = FString::Chr(NumberString[i]) + Result;
		Count++;
	}

	return Result;
}

FString UNajikaBlueprintLibrary::SecondsToTimeString(float Seconds, bool bShowHours)
{
	int32 Hours = FMath::FloorToInt(Seconds / 3600.0f);
	int32 Minutes = FMath::FloorToInt((Seconds - Hours * 3600) / 60.0f);
	int32 Secs = FMath::FloorToInt(Seconds - Hours * 3600 - Minutes * 60);

	if (bShowHours || Hours > 0)
	{
		return FString::Printf(TEXT("%02d:%02d:%02d"), Hours, Minutes, Secs);
	}
	else
	{
		return FString::Printf(TEXT("%02d:%02d"), Minutes, Secs);
	}
}

FString UNajikaBlueprintLibrary::SanitizeString(const FString& String)
{
	FString Result;
	for (TCHAR Char : String)
	{
		if (FChar::IsAlnum(Char) || FChar::IsWhitespace(Char))
		{
			Result.AppendChar(Char);
		}
	}
	return Result;
}

// ============================================================================
// MATH UTILITIES
// ============================================================================

float UNajikaBlueprintLibrary::RemapValue(float Value, float InMin, float InMax, float OutMin, float OutMax)
{
	return OutMin + (Value - InMin) * (OutMax - OutMin) / (InMax - InMin);
}

float UNajikaBlueprintLibrary::Clamp01(float Value)
{
	return FMath::Clamp(Value, 0.0f, 1.0f);
}

float UNajikaBlueprintLibrary::CalculatePercentage(float Value, float Max)
{
	if (Max == 0.0f)
	{
		return 0.0f;
	}
	return (Value / Max) * 100.0f;
}

float UNajikaBlueprintLibrary::LerpCurve(float A, float B, float Alpha, float Curve)
{
	float CurvedAlpha = FMath::Pow(FMath::Clamp(Alpha, 0.0f, 1.0f), Curve);
	return FMath::Lerp(A, B, CurvedAlpha);
}

// ============================================================================
// TIME / DATE UTILITIES
// ============================================================================

int64 UNajikaBlueprintLibrary::GetCurrentTimestamp()
{
	return FDateTime::UtcNow().ToUnixTimestamp();
}

int64 UNajikaBlueprintLibrary::GetCurrentTimestampMs()
{
	return FDateTime::UtcNow().ToUnixTimestamp() * 1000;
}

FString UNajikaBlueprintLibrary::FormatTimestamp(int64 Timestamp, const FString& Format)
{
	FDateTime DateTime = FDateTime::FromUnixTimestamp(Timestamp);

	// Simple format replacement (extend as needed)
	FString Result = Format;
	Result = Result.Replace(TEXT("YYYY"), *FString::FromInt(DateTime.GetYear()));
	Result = Result.Replace(TEXT("MM"), *FString::Printf(TEXT("%02d"), DateTime.GetMonth()));
	Result = Result.Replace(TEXT("DD"), *FString::Printf(TEXT("%02d"), DateTime.GetDay()));
	Result = Result.Replace(TEXT("HH"), *FString::Printf(TEXT("%02d"), DateTime.GetHour()));
	Result = Result.Replace(TEXT("MM"), *FString::Printf(TEXT("%02d"), DateTime.GetMinute()));
	Result = Result.Replace(TEXT("SS"), *FString::Printf(TEXT("%02d"), DateTime.GetSecond()));

	return Result;
}

FString UNajikaBlueprintLibrary::GetTimeAgoString(int64 Timestamp)
{
	int64 CurrentTimestamp = GetCurrentTimestamp();
	int64 DiffSeconds = CurrentTimestamp - Timestamp;

	if (DiffSeconds < 60)
	{
		return FString::Printf(TEXT("%lld seconds ago"), DiffSeconds);
	}
	else if (DiffSeconds < 3600)
	{
		return FString::Printf(TEXT("%lld minutes ago"), DiffSeconds / 60);
	}
	else if (DiffSeconds < 86400)
	{
		return FString::Printf(TEXT("%lld hours ago"), DiffSeconds / 3600);
	}
	else
	{
		return FString::Printf(TEXT("%lld days ago"), DiffSeconds / 86400);
	}
}

// ============================================================================
// NETWORK UTILITIES
// ============================================================================

bool UNajikaBlueprintLibrary::HasInternetConnection()
{
	return FPlatformMisc::HasActiveWiFiConnection() || FPlatformMisc::HasActiveNetworkConnection();
}

FString UNajikaBlueprintLibrary::GetLocalIPAddress()
{
	bool bCanBindAll;
	return ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->GetLocalHostAddr(*GLog, bCanBindAll)->ToString(false);
}

bool UNajikaBlueprintLibrary::PingServer(const FString& ServerURL)
{
	// Simple ping implementation (synchronous, use with caution)
	// In production, use async HTTP request
	return !ServerURL.IsEmpty();  // Placeholder
}

// ============================================================================
// DEVICE INFO
// ============================================================================

FString UNajikaBlueprintLibrary::GetDeviceName()
{
	return FPlatformMisc::GetDeviceName();
}

FString UNajikaBlueprintLibrary::GetDeviceModel()
{
	return FPlatformMisc::GetDeviceModel();
}

FString UNajikaBlueprintLibrary::GetOSVersion()
{
	return FPlatformMisc::GetOSVersion();
}

int32 UNajikaBlueprintLibrary::GetAvailableRAM()
{
	return FPlatformMemory::GetStats().AvailablePhysical / (1024 * 1024);  // Convert to MB
}

int32 UNajikaBlueprintLibrary::GetBatteryLevel()
{
	return FPlatformMisc::GetBatteryLevel();
}

bool UNajikaBlueprintLibrary::IsDeviceCharging()
{
	return FPlatformMisc::IsRunningOnBattery() == false;
}

// ============================================================================
// SAVE/LOAD UTILITIES
// ============================================================================

bool UNajikaBlueprintLibrary::SaveStringToFile(const FString& Filename, const FString& Content)
{
	FString FilePath = FPaths::ProjectSavedDir() + Filename;
	return FFileHelper::SaveStringToFile(Content, *FilePath);
}

bool UNajikaBlueprintLibrary::LoadStringFromFile(const FString& Filename, FString& OutContent)
{
	FString FilePath = FPaths::ProjectSavedDir() + Filename;
	return FFileHelper::LoadFileToString(OutContent, *FilePath);
}

bool UNajikaBlueprintLibrary::DoesSaveFileExist(const FString& Filename)
{
	FString FilePath = FPaths::ProjectSavedDir() + Filename;
	return FPlatformFileManager::Get().GetPlatformFile().FileExists(*FilePath);
}

bool UNajikaBlueprintLibrary::DeleteSaveFile(const FString& Filename)
{
	FString FilePath = FPaths::ProjectSavedDir() + Filename;
	return FPlatformFileManager::Get().GetPlatformFile().DeleteFile(*FilePath);
}

// ============================================================================
// UI UTILITIES
// ============================================================================

FMargin UNajikaBlueprintLibrary::GetSafeZonePadding()
{
	// Get safe zone from platform (handles notches, status bars, etc.)
	FMargin SafeZone;
	FDisplayMetrics DisplayMetrics;
	FDisplayMetrics::RebuildDisplayMetrics(DisplayMetrics);

	#if PLATFORM_ANDROID || PLATFORM_IOS
		// Mobile devices may have safe zones
		SafeZone.Top = 40.0f;     // Status bar
		SafeZone.Bottom = 20.0f;  // Navigation bar
		SafeZone.Left = 0.0f;
		SafeZone.Right = 0.0f;
	#else
		SafeZone = FMargin(0.0f);
	#endif

	return SafeZone;
}

void UNajikaBlueprintLibrary::GetScreenResolution(int32& OutWidth, int32& OutHeight)
{
	FDisplayMetrics DisplayMetrics;
	FDisplayMetrics::RebuildDisplayMetrics(DisplayMetrics);

	OutWidth = DisplayMetrics.PrimaryDisplayWidth;
	OutHeight = DisplayMetrics.PrimaryDisplayHeight;
}

float UNajikaBlueprintLibrary::GetDPIScale()
{
	FDisplayMetrics DisplayMetrics;
	FDisplayMetrics::RebuildDisplayMetrics(DisplayMetrics);
	return DisplayMetrics.DPIScaleFactor;
}

// ============================================================================
// DEBUG UTILITIES
// ============================================================================

void UNajikaBlueprintLibrary::PrintDebug(const FString& Message, const FString& Color, float Duration)
{
	FColor DisplayColor = FColor::White;

	if (Color == TEXT("Red"))
		DisplayColor = FColor::Red;
	else if (Color == TEXT("Green"))
		DisplayColor = FColor::Green;
	else if (Color == TEXT("Blue"))
		DisplayColor = FColor::Blue;
	else if (Color == TEXT("Yellow"))
		DisplayColor = FColor::Yellow;
	else if (Color == TEXT("Cyan"))
		DisplayColor = FColor::Cyan;
	else if (Color == TEXT("Magenta"))
		DisplayColor = FColor::Magenta;

	if (GEngine)
	{
		GEngine->AddOnScreenDebugMessage(-1, Duration, DisplayColor, Message);
	}
}

void UNajikaBlueprintLibrary::LogMessage(const FString& Message, bool bWarning, bool bError)
{
	if (bError)
	{
		UE_LOG(LogTemp, Error, TEXT("%s"), *Message);
	}
	else if (bWarning)
	{
		UE_LOG(LogTemp, Warning, TEXT("%s"), *Message);
	}
	else
	{
		UE_LOG(LogTemp, Log, TEXT("%s"), *Message);
	}
}
