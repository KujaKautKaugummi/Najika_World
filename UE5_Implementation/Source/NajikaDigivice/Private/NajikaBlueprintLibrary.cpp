// Copyright Claude Code. All Rights Reserved.

#include "NajikaBlueprintLibrary.h"
#include "JsonObjectConverter.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/PlatformFileManager.h"
#include "Engine/Engine.h"

// ============================================================
// JSON UTILITIES
// ============================================================

bool UNajikaBlueprintLibrary::ParseNajikaStateFromJSON(const FString& JsonString, FNajikaState& OutState)
{
	return FJsonObjectConverter::JsonObjectStringToUStruct<FNajikaState>(JsonString, &OutState, 0, 0);
}

FString UNajikaBlueprintLibrary::NajikaStateToJSON(const FNajikaState& State)
{
	FString JsonString;
	FJsonObjectConverter::UStructToJsonObjectString(State, JsonString);
	return JsonString;
}

bool UNajikaBlueprintLibrary::ParseJSONToMap(const FString& JsonString, TMap<FString, FString>& OutMap)
{
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

	if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
	{
		for (auto& Pair : JsonObject->Values)
		{
			OutMap.Add(Pair.Key, Pair.Value->AsString());
		}
		return true;
	}

	return false;
}

FString UNajikaBlueprintLibrary::GetJSONValue(const FString& JsonString, const FString& Key, const FString& DefaultValue)
{
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

	if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
	{
		if (JsonObject->HasField(Key))
		{
			return JsonObject->GetStringField(Key);
		}
	}

	return DefaultValue;
}

// ============================================================
// MATH UTILITIES
// ============================================================

float UNajikaBlueprintLibrary::LerpFloat(float A, float B, float Alpha)
{
	return FMath::Lerp(A, B, Alpha);
}

float UNajikaBlueprintLibrary::ClampFloat(float Value, float Min, float Max)
{
	return FMath::Clamp(Value, Min, Max);
}

float UNajikaBlueprintLibrary::MapRangeFloat(float Value, float InMin, float InMax, float OutMin, float OutMax)
{
	float Normalized = (Value - InMin) / (InMax - InMin);
	return FMath::Lerp(OutMin, OutMax, Normalized);
}

float UNajikaBlueprintLibrary::GetPercentage(float Value, float Max)
{
	if (Max <= 0.0f) return 0.0f;
	return (Value / Max) * 100.0f;
}

float UNajikaBlueprintLibrary::EaseIn(float Alpha)
{
	return Alpha * Alpha * Alpha; // Cubic ease in
}

float UNajikaBlueprintLibrary::EaseOut(float Alpha)
{
	float OneMinusAlpha = 1.0f - Alpha;
	return 1.0f - (OneMinusAlpha * OneMinusAlpha * OneMinusAlpha); // Cubic ease out
}

float UNajikaBlueprintLibrary::EaseInOut(float Alpha)
{
	if (Alpha < 0.5f)
	{
		return 4.0f * Alpha * Alpha * Alpha; // Ease in
	}
	else
	{
		float F = ((2.0f * Alpha) - 2.0f);
		return 0.5f * F * F * F + 1.0f; // Ease out
	}
}

// ============================================================
// STRING UTILITIES
// ============================================================

FString UNajikaBlueprintLibrary::FormatTime(float Seconds)
{
	int32 TotalSeconds = FMath::RoundToInt(Seconds);
	int32 Minutes = TotalSeconds / 60;
	int32 Secs = TotalSeconds % 60;

	return FString::Printf(TEXT("%02d:%02d"), Minutes, Secs);
}

FString UNajikaBlueprintLibrary::FormatTimeDetailed(float Seconds)
{
	int32 TotalSeconds = FMath::RoundToInt(Seconds);
	int32 Hours = TotalSeconds / 3600;
	int32 Minutes = (TotalSeconds % 3600) / 60;
	int32 Secs = TotalSeconds % 60;

	return FString::Printf(TEXT("%02d:%02d:%02d"), Hours, Minutes, Secs);
}

FString UNajikaBlueprintLibrary::FormatNumber(int32 Number)
{
	FString NumberString = FString::Printf(TEXT("%d"), Number);
	FString Result;

	int32 Count = 0;
	for (int32 i = NumberString.Len() - 1; i >= 0; i--)
	{
		if (Count == 3)
		{
			Result = TEXT(",") + Result;
			Count = 0;
		}
		Result = NumberString[i] + Result;
		Count++;
	}

	return Result;
}

FString UNajikaBlueprintLibrary::TruncateString(const FString& Text, int32 MaxLength)
{
	if (Text.Len() <= MaxLength)
	{
		return Text;
	}

	return Text.Left(MaxLength - 3) + TEXT("...");
}

bool UNajikaBlueprintLibrary::IsValidEmail(const FString& Email)
{
	// Simple email validation (contains @ and .)
	return Email.Contains(TEXT("@")) && Email.Contains(TEXT("."));
}

FString UNajikaBlueprintLibrary::SanitizeString(const FString& Text)
{
	FString Result = Text;

	// Remove special characters
	Result = Result.Replace(TEXT("<"), TEXT(""));
	Result = Result.Replace(TEXT(">"), TEXT(""));
	Result = Result.Replace(TEXT("&"), TEXT(""));
	Result = Result.Replace(TEXT("\""), TEXT(""));
	Result = Result.Replace(TEXT("'"), TEXT(""));

	return Result;
}

// ============================================================
// DATE/TIME UTILITIES
// ============================================================

FString UNajikaBlueprintLibrary::GetCurrentDateTime()
{
	FDateTime Now = FDateTime::Now();
	return Now.ToString(TEXT("%Y-%m-%d %H:%M:%S"));
}

int64 UNajikaBlueprintLibrary::GetUnixTimestamp()
{
	return FDateTime::UtcNow().ToUnixTimestamp();
}

FString UNajikaBlueprintLibrary::FormatUnixTimestamp(int64 Timestamp)
{
	FDateTime DateTime = FDateTime::FromUnixTimestamp(Timestamp);
	return DateTime.ToString(TEXT("%Y-%m-%d %H:%M:%S"));
}

float UNajikaBlueprintLibrary::GetTimeDifference(int64 StartTimestamp, int64 EndTimestamp)
{
	return static_cast<float>(EndTimestamp - StartTimestamp);
}

// ============================================================
// SAVE/LOAD UTILITIES
// ============================================================

FString GetSaveDirectory()
{
	return FPaths::ProjectSavedDir() + TEXT("SaveGames/");
}

bool UNajikaBlueprintLibrary::SaveStringToFile(const FString& Filename, const FString& Data)
{
	FString FilePath = GetSaveDirectory() + Filename;

	// Ensure directory exists
	FString Directory = FPaths::GetPath(FilePath);
	IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
	if (!PlatformFile.DirectoryExists(*Directory))
	{
		PlatformFile.CreateDirectoryTree(*Directory);
	}

	// Save to file
	bool bSuccess = FFileHelper::SaveStringToFile(Data, *FilePath);

	if (bSuccess)
	{
		UE_LOG(LogTemp, Log, TEXT("[NajikaBlueprintLibrary] Saved to file: %s"), *FilePath);
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaBlueprintLibrary] Failed to save file: %s"), *FilePath);
	}

	return bSuccess;
}

bool UNajikaBlueprintLibrary::LoadStringFromFile(const FString& Filename, FString& OutData)
{
	FString FilePath = GetSaveDirectory() + Filename;

	bool bSuccess = FFileHelper::LoadFileToString(OutData, *FilePath);

	if (bSuccess)
	{
		UE_LOG(LogTemp, Log, TEXT("[NajikaBlueprintLibrary] Loaded from file: %s"), *FilePath);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaBlueprintLibrary] Failed to load file: %s"), *FilePath);
	}

	return bSuccess;
}

bool UNajikaBlueprintLibrary::DoesSaveFileExist(const FString& Filename)
{
	FString FilePath = GetSaveDirectory() + Filename;
	return FPaths::FileExists(FilePath);
}

bool UNajikaBlueprintLibrary::DeleteSaveFile(const FString& Filename)
{
	FString FilePath = GetSaveDirectory() + Filename;

	IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
	bool bSuccess = PlatformFile.DeleteFile(*FilePath);

	if (bSuccess)
	{
		UE_LOG(LogTemp, Log, TEXT("[NajikaBlueprintLibrary] Deleted file: %s"), *FilePath);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaBlueprintLibrary] Failed to delete file: %s"), *FilePath);
	}

	return bSuccess;
}

// ============================================================
// PLATFORM DETECTION
// ============================================================

bool UNajikaBlueprintLibrary::IsMobilePlatform()
{
	#if PLATFORM_ANDROID || PLATFORM_IOS
		return true;
	#else
		return false;
	#endif
}

bool UNajikaBlueprintLibrary::IsAndroid()
{
	#if PLATFORM_ANDROID
		return true;
	#else
		return false;
	#endif
}

bool UNajikaBlueprintLibrary::IsIOS()
{
	#if PLATFORM_IOS
		return true;
	#else
		return false;
	#endif
}

bool UNajikaBlueprintLibrary::IsWindows()
{
	#if PLATFORM_WINDOWS
		return true;
	#else
		return false;
	#endif
}

FString UNajikaBlueprintLibrary::GetPlatformName()
{
	#if PLATFORM_WINDOWS
		return TEXT("Windows");
	#elif PLATFORM_ANDROID
		return TEXT("Android");
	#elif PLATFORM_IOS
		return TEXT("iOS");
	#elif PLATFORM_MAC
		return TEXT("Mac");
	#elif PLATFORM_LINUX
		return TEXT("Linux");
	#else
		return TEXT("Unknown");
	#endif
}

// ============================================================
// COLOR UTILITIES
// ============================================================

FLinearColor UNajikaBlueprintLibrary::HexToColor(const FString& HexString)
{
	FString Hex = HexString;

	// Remove # if present
	if (Hex.StartsWith(TEXT("#")))
	{
		Hex = Hex.RightChop(1);
	}

	// Parse hex to RGB
	if (Hex.Len() == 6)
	{
		int32 R = FParse::HexNumber(*Hex.Mid(0, 2));
		int32 G = FParse::HexNumber(*Hex.Mid(2, 2));
		int32 B = FParse::HexNumber(*Hex.Mid(4, 2));

		return FLinearColor(R / 255.0f, G / 255.0f, B / 255.0f);
	}

	// Invalid hex, return white
	return FLinearColor::White;
}

FString UNajikaBlueprintLibrary::ColorToHex(const FLinearColor& Color)
{
	int32 R = FMath::RoundToInt(Color.R * 255.0f);
	int32 G = FMath::RoundToInt(Color.G * 255.0f);
	int32 B = FMath::RoundToInt(Color.B * 255.0f);

	return FString::Printf(TEXT("#%02X%02X%02X"), R, G, B);
}

FLinearColor UNajikaBlueprintLibrary::LerpColor(const FLinearColor& A, const FLinearColor& B, float Alpha)
{
	return FLinearColor::LerpUsingHSV(A, B, Alpha);
}

FLinearColor UNajikaBlueprintLibrary::GetStatusColor(float Value)
{
	// Green (>75%), Yellow (50-75%), Orange (25-50%), Red (<25%)
	if (Value >= 75.0f)
	{
		return FLinearColor::Green;
	}
	else if (Value >= 50.0f)
	{
		return FLinearColor::Yellow;
	}
	else if (Value >= 25.0f)
	{
		return FLinearColor(1.0f, 0.5f, 0.0f); // Orange
	}
	else
	{
		return FLinearColor::Red;
	}
}

// ============================================================
// ARRAY UTILITIES
// ============================================================

TArray<FString> UNajikaBlueprintLibrary::ShuffleStringArray(const TArray<FString>& Array)
{
	TArray<FString> Result = Array;

	// Fisher-Yates shuffle
	for (int32 i = Result.Num() - 1; i > 0; i--)
	{
		int32 j = FMath::RandRange(0, i);
		Result.Swap(i, j);
	}

	return Result;
}

FString UNajikaBlueprintLibrary::GetRandomStringFromArray(const TArray<FString>& Array)
{
	if (Array.Num() == 0)
	{
		return TEXT("");
	}

	int32 RandomIndex = FMath::RandRange(0, Array.Num() - 1);
	return Array[RandomIndex];
}

TArray<FString> UNajikaBlueprintLibrary::RemoveDuplicates(const TArray<FString>& Array)
{
	TArray<FString> Result;
	TSet<FString> Seen;

	for (const FString& Element : Array)
	{
		if (!Seen.Contains(Element))
		{
			Result.Add(Element);
			Seen.Add(Element);
		}
	}

	return Result;
}

// ============================================================
// MISC UTILITIES
// ============================================================

void UNajikaBlueprintLibrary::LogMessage(const FString& Message, bool bWarning)
{
	if (bWarning)
	{
		UE_LOG(LogTemp, Warning, TEXT("[Blueprint] %s"), *Message);
	}
	else
	{
		UE_LOG(LogTemp, Log, TEXT("[Blueprint] %s"), *Message);
	}
}

void UNajikaBlueprintLibrary::LogError(const FString& Message)
{
	UE_LOG(LogTemp, Error, TEXT("[Blueprint] %s"), *Message);
}

void UNajikaBlueprintLibrary::PrintToScreen(const FString& Message, float Duration, FLinearColor Color)
{
	if (GEngine)
	{
		GEngine->AddOnScreenDebugMessage(-1, Duration, Color.ToFColor(true), Message);
	}
}
