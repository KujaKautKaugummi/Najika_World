// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "OPTIONAL_NajikaBlueprintLibrary.generated.h"

// ============================================================================
// OPTIONAL: Blueprint Function Library
// ============================================================================
//
// HINWEIS: Diese Library ist OPTIONAL und bietet Helper-Funktionen
// für häufige Aufgaben in Blueprints.
//
// Features:
// - JSON Parsing / Serialization
// - String Utilities
// - Math Utilities
// - Time/Date Formatting
// - Network Helpers
// - Save/Load Helpers
//
// Usage in Blueprint:
//   Einfach Funktionen aus dieser Library verwenden - sie erscheinen
//   automatisch im Blueprint Context Menu unter "Najika | Utils"
//
// ============================================================================

/**
 * OPTIONAL: Blueprint Function Library mit nützlichen Helper-Funktionen
 */
UCLASS()
class NAJIKABACKENDCLIENT_API UNajikaBlueprintLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	// ========================================================================
	// JSON UTILITIES
	// ========================================================================

	/**
	 * Parse JSON string to key-value map
	 * @param JsonString JSON string to parse
	 * @param OutMap Parsed key-value pairs
	 * @return True if parsing succeeded
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Utils|JSON")
	static bool ParseJsonToMap(const FString& JsonString, TMap<FString, FString>& OutMap);

	/**
	 * Create JSON string from key-value map
	 * @param Map Key-value pairs
	 * @return JSON string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|JSON")
	static FString MapToJson(const TMap<FString, FString>& Map);

	/**
	 * Get value from JSON string by key
	 * @param JsonString JSON string
	 * @param Key Key to lookup
	 * @param DefaultValue Default value if key not found
	 * @return Value for key or default value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|JSON")
	static FString GetJsonValue(const FString& JsonString, const FString& Key, const FString& DefaultValue = TEXT(""));

	/**
	 * Check if JSON string is valid
	 * @param JsonString JSON string to validate
	 * @return True if valid JSON
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|JSON")
	static bool IsValidJson(const FString& JsonString);

	// ========================================================================
	// STRING UTILITIES
	// ========================================================================

	/**
	 * Truncate string to maximum length with ellipsis
	 * @param String String to truncate
	 * @param MaxLength Maximum length
	 * @param Ellipsis Ellipsis text (default: "...")
	 * @return Truncated string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|String")
	static FString TruncateString(const FString& String, int32 MaxLength, const FString& Ellipsis = TEXT("..."));

	/**
	 * Format number with thousands separator
	 * @param Number Number to format
	 * @param Separator Separator character (default: ",")
	 * @return Formatted string (e.g., "1,234,567")
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|String")
	static FString FormatNumberWithSeparator(int32 Number, const FString& Separator = TEXT(","));

	/**
	 * Convert seconds to time string (HH:MM:SS or MM:SS)
	 * @param Seconds Total seconds
	 * @param bShowHours Show hours even if 0
	 * @return Formatted time string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|String")
	static FString SecondsToTimeString(float Seconds, bool bShowHours = false);

	/**
	 * Remove special characters from string (keep alphanumeric and spaces)
	 * @param String Input string
	 * @return Sanitized string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|String")
	static FString SanitizeString(const FString& String);

	// ========================================================================
	// MATH UTILITIES
	// ========================================================================

	/**
	 * Remap value from one range to another
	 * @param Value Input value
	 * @param InMin Input range minimum
	 * @param InMax Input range maximum
	 * @param OutMin Output range minimum
	 * @param OutMax Output range maximum
	 * @return Remapped value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Math")
	static float RemapValue(float Value, float InMin, float InMax, float OutMin, float OutMax);

	/**
	 * Clamp value to 0-1 range
	 * @param Value Input value
	 * @return Clamped value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Math")
	static float Clamp01(float Value);

	/**
	 * Calculate percentage (Value / Max * 100)
	 * @param Value Current value
	 * @param Max Maximum value
	 * @return Percentage (0-100)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Math")
	static float CalculatePercentage(float Value, float Max);

	/**
	 * Linear interpolation with custom alpha curve
	 * @param A Start value
	 * @param B End value
	 * @param Alpha Interpolation factor (0-1)
	 * @param Curve Curve exponent (1.0 = linear, 2.0 = ease in, 0.5 = ease out)
	 * @return Interpolated value
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Math")
	static float LerpCurve(float A, float B, float Alpha, float Curve = 1.0f);

	// ========================================================================
	// TIME / DATE UTILITIES
	// ========================================================================

	/**
	 * Get current timestamp (Unix timestamp in seconds)
	 * @return Current timestamp
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Time")
	static int64 GetCurrentTimestamp();

	/**
	 * Get current timestamp in milliseconds
	 * @return Current timestamp in milliseconds
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Time")
	static int64 GetCurrentTimestampMs();

	/**
	 * Format timestamp to readable date string
	 * @param Timestamp Unix timestamp in seconds
	 * @param Format Format string (e.g., "YYYY-MM-DD HH:MM:SS")
	 * @return Formatted date string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Time")
	static FString FormatTimestamp(int64 Timestamp, const FString& Format = TEXT("YYYY-MM-DD HH:MM:SS"));

	/**
	 * Get time ago string (e.g., "5 minutes ago", "2 hours ago")
	 * @param Timestamp Unix timestamp in seconds
	 * @return Time ago string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Time")
	static FString GetTimeAgoString(int64 Timestamp);

	// ========================================================================
	// NETWORK UTILITIES
	// ========================================================================

	/**
	 * Check if device has internet connection
	 * @return True if connected to internet
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Network")
	static bool HasInternetConnection();

	/**
	 * Get local IP address
	 * @return Local IP address as string
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Network")
	static FString GetLocalIPAddress();

	/**
	 * Ping server to check connectivity
	 * @param ServerURL Server URL (e.g., "http://localhost:8000")
	 * @return True if server is reachable
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Utils|Network")
	static bool PingServer(const FString& ServerURL);

	// ========================================================================
	// DEVICE INFO
	// ========================================================================

	/**
	 * Get device name
	 * @return Device name (e.g., "Xiaomi 11T Pro")
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Device")
	static FString GetDeviceName();

	/**
	 * Get device model
	 * @return Device model
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Device")
	static FString GetDeviceModel();

	/**
	 * Get operating system version
	 * @return OS version (e.g., "Android 11")
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Device")
	static FString GetOSVersion();

	/**
	 * Get available RAM in MB
	 * @return Available RAM in megabytes
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Device")
	static int32 GetAvailableRAM();

	/**
	 * Get battery level (0-100)
	 * @return Battery percentage
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Device")
	static int32 GetBatteryLevel();

	/**
	 * Check if device is charging
	 * @return True if device is plugged in
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|Device")
	static bool IsDeviceCharging();

	// ========================================================================
	// SAVE/LOAD UTILITIES
	// ========================================================================

	/**
	 * Save string to file
	 * @param Filename Filename (relative to SavedDir)
	 * @param Content String content to save
	 * @return True if saved successfully
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Utils|SaveLoad")
	static bool SaveStringToFile(const FString& Filename, const FString& Content);

	/**
	 * Load string from file
	 * @param Filename Filename (relative to SavedDir)
	 * @param OutContent Loaded string content
	 * @return True if loaded successfully
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Utils|SaveLoad")
	static bool LoadStringFromFile(const FString& Filename, FString& OutContent);

	/**
	 * Check if save file exists
	 * @param Filename Filename (relative to SavedDir)
	 * @return True if file exists
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|SaveLoad")
	static bool DoesSaveFileExist(const FString& Filename);

	/**
	 * Delete save file
	 * @param Filename Filename (relative to SavedDir)
	 * @return True if deleted successfully
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Utils|SaveLoad")
	static bool DeleteSaveFile(const FString& Filename);

	// ========================================================================
	// UI UTILITIES
	// ========================================================================

	/**
	 * Get safe zone padding for notched displays
	 * @return Safe zone padding (Top, Bottom, Left, Right)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|UI")
	static FMargin GetSafeZonePadding();

	/**
	 * Get screen resolution
	 * @param OutWidth Screen width in pixels
	 * @param OutHeight Screen height in pixels
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|UI")
	static void GetScreenResolution(int32& OutWidth, int32& OutHeight);

	/**
	 * Get DPI scale
	 * @return DPI scale factor (1.0 = 96 DPI)
	 */
	UFUNCTION(BlueprintPure, Category = "Najika|Utils|UI")
	static float GetDPIScale();

	// ========================================================================
	// DEBUG UTILITIES
	// ========================================================================

	/**
	 * Print debug message with color
	 * @param Message Message to print
	 * @param Color Color (Red, Green, Blue, Yellow, etc.)
	 * @param Duration Duration in seconds
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Utils|Debug")
	static void PrintDebug(const FString& Message, const FString& Color = TEXT("White"), float Duration = 2.0f);

	/**
	 * Log message to console
	 * @param Message Message to log
	 * @param bWarning If true, log as warning
	 * @param bError If true, log as error
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Utils|Debug")
	static void LogMessage(const FString& Message, bool bWarning = false, bool bError = false);
};
