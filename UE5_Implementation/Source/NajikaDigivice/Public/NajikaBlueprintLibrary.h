// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "NajikaBackendTypes.h"
#include "NajikaBlueprintLibrary.generated.h"

/**
 * Blueprint Function Library for Najika Digivice
 *
 * Provides utility functions for Blueprints:
 * - JSON parsing and serialization
 * - Math helpers (lerp, clamp, map range)
 * - String utilities (format, parse, validate)
 * - Date/Time helpers
 * - Save/Load helpers
 * - Platform detection
 * - Color utilities
 * - Array utilities
 * - File I/O
 *
 * Usage:
 * - Call functions from Blueprint graphs
 * - All functions are static (no object instance required)
 */
UCLASS()
class NAJIKADIGIVICE_API UNajikaBlueprintLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	// ============================================================
	// JSON UTILITIES
	// ============================================================

	/**
	 * Parse JSON string to FNajikaState
	 * @param JsonString JSON string
	 * @param OutState Parsed state
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|JSON")
	static bool ParseNajikaStateFromJSON(const FString& JsonString, FNajikaState& OutState);

	/**
	 * Convert FNajikaState to JSON string
	 * @param State Najika state
	 * @return JSON string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|JSON")
	static FString NajikaStateToJSON(const FNajikaState& State);

	/**
	 * Parse JSON string to key-value map
	 * @param JsonString JSON string
	 * @param OutMap Key-value map
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|JSON")
	static bool ParseJSONToMap(const FString& JsonString, TMap<FString, FString>& OutMap);

	/**
	 * Get JSON value by key
	 * @param JsonString JSON string
	 * @param Key Key name
	 * @param DefaultValue Default value if key not found
	 * @return Value as string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|JSON")
	static FString GetJSONValue(const FString& JsonString, const FString& Key, const FString& DefaultValue = TEXT(""));

	// ============================================================
	// MATH UTILITIES
	// ============================================================

	/**
	 * Lerp between two values (linear interpolation)
	 * @param A Start value
	 * @param B End value
	 * @param Alpha Interpolation factor (0-1)
	 * @return Interpolated value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Math")
	static float LerpFloat(float A, float B, float Alpha);

	/**
	 * Clamp value between min and max
	 * @param Value Value to clamp
	 * @param Min Minimum value
	 * @param Max Maximum value
	 * @return Clamped value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Math")
	static float ClampFloat(float Value, float Min, float Max);

	/**
	 * Map value from one range to another
	 * @param Value Input value
	 * @param InMin Input range minimum
	 * @param InMax Input range maximum
	 * @param OutMin Output range minimum
	 * @param OutMax Output range maximum
	 * @return Mapped value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Math")
	static float MapRangeFloat(float Value, float InMin, float InMax, float OutMin, float OutMax);

	/**
	 * Get percentage (0-100) from value and max
	 * @param Value Current value
	 * @param Max Maximum value
	 * @return Percentage (0-100)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Math")
	static float GetPercentage(float Value, float Max);

	/**
	 * Ease In (cubic)
	 * @param Alpha Input (0-1)
	 * @return Eased value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Math")
	static float EaseIn(float Alpha);

	/**
	 * Ease Out (cubic)
	 * @param Alpha Input (0-1)
	 * @return Eased value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Math")
	static float EaseOut(float Alpha);

	/**
	 * Ease In-Out (cubic)
	 * @param Alpha Input (0-1)
	 * @return Eased value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Math")
	static float EaseInOut(float Alpha);

	// ============================================================
	// STRING UTILITIES
	// ============================================================

	/**
	 * Format time in seconds to MM:SS
	 * @param Seconds Time in seconds
	 * @return Formatted string (MM:SS)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|String")
	static FString FormatTime(float Seconds);

	/**
	 * Format time in seconds to HH:MM:SS
	 * @param Seconds Time in seconds
	 * @return Formatted string (HH:MM:SS)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|String")
	static FString FormatTimeDetailed(float Seconds);

	/**
	 * Format number with thousands separator
	 * @param Number Number to format
	 * @return Formatted string (e.g., "1,234,567")
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|String")
	static FString FormatNumber(int32 Number);

	/**
	 * Truncate string to max length with ellipsis
	 * @param Text Input text
	 * @param MaxLength Maximum length
	 * @return Truncated text
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|String")
	static FString TruncateString(const FString& Text, int32 MaxLength);

	/**
	 * Check if string is valid email
	 * @param Email Email string
	 * @return True if valid
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|String")
	static bool IsValidEmail(const FString& Email);

	/**
	 * Remove special characters from string
	 * @param Text Input text
	 * @return Sanitized text
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|String")
	static FString SanitizeString(const FString& Text);

	// ============================================================
	// DATE/TIME UTILITIES
	// ============================================================

	/**
	 * Get current date/time as string
	 * @return Current date/time (YYYY-MM-DD HH:MM:SS)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|DateTime")
	static FString GetCurrentDateTime();

	/**
	 * Get current Unix timestamp
	 * @return Unix timestamp (seconds since epoch)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|DateTime")
	static int64 GetUnixTimestamp();

	/**
	 * Format Unix timestamp to readable date
	 * @param Timestamp Unix timestamp
	 * @return Formatted date (YYYY-MM-DD HH:MM:SS)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|DateTime")
	static FString FormatUnixTimestamp(int64 Timestamp);

	/**
	 * Get time difference in seconds
	 * @param StartTimestamp Start timestamp
	 * @param EndTimestamp End timestamp
	 * @return Difference in seconds
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|DateTime")
	static float GetTimeDifference(int64 StartTimestamp, int64 EndTimestamp);

	// ============================================================
	// SAVE/LOAD UTILITIES
	// ============================================================

	/**
	 * Save string to file
	 * @param Filename File name (relative to SavedDir)
	 * @param Data String data to save
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|SaveLoad")
	static bool SaveStringToFile(const FString& Filename, const FString& Data);

	/**
	 * Load string from file
	 * @param Filename File name (relative to SavedDir)
	 * @param OutData Loaded string data
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|SaveLoad")
	static bool LoadStringFromFile(const FString& Filename, FString& OutData);

	/**
	 * Check if save file exists
	 * @param Filename File name (relative to SavedDir)
	 * @return True if exists
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|SaveLoad")
	static bool DoesSaveFileExist(const FString& Filename);

	/**
	 * Delete save file
	 * @param Filename File name (relative to SavedDir)
	 * @return True if successful
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|SaveLoad")
	static bool DeleteSaveFile(const FString& Filename);

	// ============================================================
	// PLATFORM DETECTION
	// ============================================================

	/**
	 * Is running on mobile platform (Android or iOS)
	 * @return True if mobile
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Platform")
	static bool IsMobilePlatform();

	/**
	 * Is running on Android
	 * @return True if Android
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Platform")
	static bool IsAndroid();

	/**
	 * Is running on iOS
	 * @return True if iOS
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Platform")
	static bool IsIOS();

	/**
	 * Is running on Windows
	 * @return True if Windows
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Platform")
	static bool IsWindows();

	/**
	 * Get platform name
	 * @return Platform name (Windows, Android, iOS, etc.)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Platform")
	static FString GetPlatformName();

	// ============================================================
	// COLOR UTILITIES
	// ============================================================

	/**
	 * Get color from hex string
	 * @param HexString Hex color string (e.g., "#FF5733" or "FF5733")
	 * @return Linear color
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Color")
	static FLinearColor HexToColor(const FString& HexString);

	/**
	 * Convert color to hex string
	 * @param Color Linear color
	 * @return Hex string (e.g., "#FF5733")
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Color")
	static FString ColorToHex(const FLinearColor& Color);

	/**
	 * Lerp between two colors
	 * @param A Start color
	 * @param B End color
	 * @param Alpha Interpolation factor (0-1)
	 * @return Interpolated color
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Color")
	static FLinearColor LerpColor(const FLinearColor& A, const FLinearColor& B, float Alpha);

	/**
	 * Get status color (Green→Yellow→Orange→Red based on value)
	 * @param Value Value (0-100)
	 * @return Status color
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Color")
	static FLinearColor GetStatusColor(float Value);

	// ============================================================
	// ARRAY UTILITIES
	// ============================================================

	/**
	 * Shuffle string array (random order)
	 * @param Array Input array
	 * @return Shuffled array
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Array")
	static TArray<FString> ShuffleStringArray(const TArray<FString>& Array);

	/**
	 * Get random element from string array
	 * @param Array Input array
	 * @return Random element
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Array")
	static FString GetRandomStringFromArray(const TArray<FString>& Array);

	/**
	 * Remove duplicates from string array
	 * @param Array Input array
	 * @return Array without duplicates
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Array")
	static TArray<FString> RemoveDuplicates(const TArray<FString>& Array);

	// ============================================================
	// MISC UTILITIES
	// ============================================================

	/**
	 * Log message to console
	 * @param Message Message to log
	 * @param bWarning Log as warning (yellow) instead of log (white)
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Debug")
	static void LogMessage(const FString& Message, bool bWarning = false);

	/**
	 * Log error message to console
	 * @param Message Error message
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Debug")
	static void LogError(const FString& Message);

	/**
	 * Print string to screen (debug)
	 * @param Message Message to print
	 * @param Duration Display duration (seconds)
	 * @param Color Text color
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Debug")
	static void PrintToScreen(const FString& Message, float Duration = 5.0f, FLinearColor Color = FLinearColor::White);
};
