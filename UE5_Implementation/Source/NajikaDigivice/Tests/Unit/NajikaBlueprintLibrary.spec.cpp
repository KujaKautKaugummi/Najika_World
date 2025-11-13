// Copyright Claude Code. All Rights Reserved.

#include "Misc/AutomationTest.h"
#include "NajikaBlueprintLibrary.h"
#include "NajikaBackendTypes.h"

// ============================================================
// MATH UTILITIES TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_LerpFloat,
	"Najika.Unit.BlueprintLibrary.LerpFloat",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_LerpFloat::RunTest(const FString& Parameters)
{
	// Test basic lerp
	float Result = UNajikaBlueprintLibrary::LerpFloat(0.0f, 100.0f, 0.5f);
	TestEqual(TEXT("Lerp(0, 100, 0.5) should be 50"), Result, 50.0f);

	// Test edge cases
	Result = UNajikaBlueprintLibrary::LerpFloat(0.0f, 100.0f, 0.0f);
	TestEqual(TEXT("Lerp(0, 100, 0) should be 0"), Result, 0.0f);

	Result = UNajikaBlueprintLibrary::LerpFloat(0.0f, 100.0f, 1.0f);
	TestEqual(TEXT("Lerp(0, 100, 1) should be 100"), Result, 100.0f);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_ClampFloat,
	"Najika.Unit.BlueprintLibrary.ClampFloat",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_ClampFloat::RunTest(const FString& Parameters)
{
	// Test clamping within range
	float Result = UNajikaBlueprintLibrary::ClampFloat(50.0f, 0.0f, 100.0f);
	TestEqual(TEXT("Clamp(50, 0, 100) should be 50"), Result, 50.0f);

	// Test clamping below min
	Result = UNajikaBlueprintLibrary::ClampFloat(-10.0f, 0.0f, 100.0f);
	TestEqual(TEXT("Clamp(-10, 0, 100) should be 0"), Result, 0.0f);

	// Test clamping above max
	Result = UNajikaBlueprintLibrary::ClampFloat(150.0f, 0.0f, 100.0f);
	TestEqual(TEXT("Clamp(150, 0, 100) should be 100"), Result, 100.0f);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_MapRangeFloat,
	"Najika.Unit.BlueprintLibrary.MapRangeFloat",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_MapRangeFloat::RunTest(const FString& Parameters)
{
	// Map 50 from range (0-100) to range (0-10)
	float Result = UNajikaBlueprintLibrary::MapRangeFloat(50.0f, 0.0f, 100.0f, 0.0f, 10.0f);
	TestEqual(TEXT("MapRange(50, 0-100, 0-10) should be 5"), Result, 5.0f);

	// Map 0 from range (0-100) to range (0-10)
	Result = UNajikaBlueprintLibrary::MapRangeFloat(0.0f, 0.0f, 100.0f, 0.0f, 10.0f);
	TestEqual(TEXT("MapRange(0, 0-100, 0-10) should be 0"), Result, 0.0f);

	// Map 100 from range (0-100) to range (0-10)
	Result = UNajikaBlueprintLibrary::MapRangeFloat(100.0f, 0.0f, 100.0f, 0.0f, 10.0f);
	TestEqual(TEXT("MapRange(100, 0-100, 0-10) should be 10"), Result, 10.0f);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_GetPercentage,
	"Najika.Unit.BlueprintLibrary.GetPercentage",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_GetPercentage::RunTest(const FString& Parameters)
{
	// Test basic percentage
	float Result = UNajikaBlueprintLibrary::GetPercentage(50.0f, 100.0f);
	TestEqual(TEXT("GetPercentage(50, 100) should be 50%"), Result, 50.0f);

	// Test 0%
	Result = UNajikaBlueprintLibrary::GetPercentage(0.0f, 100.0f);
	TestEqual(TEXT("GetPercentage(0, 100) should be 0%"), Result, 0.0f);

	// Test 100%
	Result = UNajikaBlueprintLibrary::GetPercentage(100.0f, 100.0f);
	TestEqual(TEXT("GetPercentage(100, 100) should be 100%"), Result, 100.0f);

	// Test divide by zero protection
	Result = UNajikaBlueprintLibrary::GetPercentage(50.0f, 0.0f);
	TestEqual(TEXT("GetPercentage(50, 0) should be 0% (divide by zero)"), Result, 0.0f);

	return true;
}

// ============================================================
// STRING UTILITIES TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_FormatTime,
	"Najika.Unit.BlueprintLibrary.FormatTime",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_FormatTime::RunTest(const FString& Parameters)
{
	// Test 0 seconds
	FString Result = UNajikaBlueprintLibrary::FormatTime(0.0f);
	TestEqual(TEXT("FormatTime(0) should be '00:00'"), Result, TEXT("00:00"));

	// Test 90 seconds (1:30)
	Result = UNajikaBlueprintLibrary::FormatTime(90.0f);
	TestEqual(TEXT("FormatTime(90) should be '01:30'"), Result, TEXT("01:30"));

	// Test 3661 seconds (61:01)
	Result = UNajikaBlueprintLibrary::FormatTime(3661.0f);
	TestEqual(TEXT("FormatTime(3661) should be '61:01'"), Result, TEXT("61:01"));

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_FormatTimeDetailed,
	"Najika.Unit.BlueprintLibrary.FormatTimeDetailed",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_FormatTimeDetailed::RunTest(const FString& Parameters)
{
	// Test 0 seconds
	FString Result = UNajikaBlueprintLibrary::FormatTimeDetailed(0.0f);
	TestEqual(TEXT("FormatTimeDetailed(0) should be '00:00:00'"), Result, TEXT("00:00:00"));

	// Test 3661 seconds (1:01:01)
	Result = UNajikaBlueprintLibrary::FormatTimeDetailed(3661.0f);
	TestEqual(TEXT("FormatTimeDetailed(3661) should be '01:01:01'"), Result, TEXT("01:01:01"));

	// Test 86400 seconds (24:00:00)
	Result = UNajikaBlueprintLibrary::FormatTimeDetailed(86400.0f);
	TestEqual(TEXT("FormatTimeDetailed(86400) should be '24:00:00'"), Result, TEXT("24:00:00"));

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_FormatNumber,
	"Najika.Unit.BlueprintLibrary.FormatNumber",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_FormatNumber::RunTest(const FString& Parameters)
{
	// Test small number
	FString Result = UNajikaBlueprintLibrary::FormatNumber(123);
	TestEqual(TEXT("FormatNumber(123) should be '123'"), Result, TEXT("123"));

	// Test thousands separator
	Result = UNajikaBlueprintLibrary::FormatNumber(1234567);
	TestEqual(TEXT("FormatNumber(1234567) should be '1,234,567'"), Result, TEXT("1,234,567"));

	// Test negative number
	Result = UNajikaBlueprintLibrary::FormatNumber(-1234);
	TestEqual(TEXT("FormatNumber(-1234) should be '-1,234'"), Result, TEXT("-1,234"));

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_TruncateString,
	"Najika.Unit.BlueprintLibrary.TruncateString",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_TruncateString::RunTest(const FString& Parameters)
{
	// Test truncation
	FString Result = UNajikaBlueprintLibrary::TruncateString(TEXT("Hello World!"), 8);
	TestEqual(TEXT("TruncateString('Hello World!', 8) should be 'Hello...'"), Result, TEXT("Hello..."));

	// Test no truncation needed
	Result = UNajikaBlueprintLibrary::TruncateString(TEXT("Hello"), 10);
	TestEqual(TEXT("TruncateString('Hello', 10) should be 'Hello'"), Result, TEXT("Hello"));

	return true;
}

// ============================================================
// COLOR UTILITIES TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_HexToColor,
	"Najika.Unit.BlueprintLibrary.HexToColor",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_HexToColor::RunTest(const FString& Parameters)
{
	// Test with # prefix
	FLinearColor Result = UNajikaBlueprintLibrary::HexToColor(TEXT("#FF0000"));
	TestEqual(TEXT("HexToColor('#FF0000') R should be 1.0"), Result.R, 1.0f, 0.01f);
	TestEqual(TEXT("HexToColor('#FF0000') G should be 0.0"), Result.G, 0.0f, 0.01f);
	TestEqual(TEXT("HexToColor('#FF0000') B should be 0.0"), Result.B, 0.0f, 0.01f);

	// Test without # prefix
	Result = UNajikaBlueprintLibrary::HexToColor(TEXT("00FF00"));
	TestEqual(TEXT("HexToColor('00FF00') R should be 0.0"), Result.R, 0.0f, 0.01f);
	TestEqual(TEXT("HexToColor('00FF00') G should be 1.0"), Result.G, 1.0f, 0.01f);
	TestEqual(TEXT("HexToColor('00FF00') B should be 0.0"), Result.B, 0.0f, 0.01f);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_ColorToHex,
	"Najika.Unit.BlueprintLibrary.ColorToHex",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_ColorToHex::RunTest(const FString& Parameters)
{
	// Test red
	FString Result = UNajikaBlueprintLibrary::ColorToHex(FLinearColor::Red);
	TestEqual(TEXT("ColorToHex(Red) should be '#FF0000'"), Result, TEXT("#FF0000"));

	// Test green
	Result = UNajikaBlueprintLibrary::ColorToHex(FLinearColor::Green);
	TestEqual(TEXT("ColorToHex(Green) should be '#00FF00'"), Result, TEXT("#00FF00"));

	// Test blue
	Result = UNajikaBlueprintLibrary::ColorToHex(FLinearColor::Blue);
	TestEqual(TEXT("ColorToHex(Blue) should be '#0000FF'"), Result, TEXT("#0000FF"));

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_GetStatusColor,
	"Najika.Unit.BlueprintLibrary.GetStatusColor",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_GetStatusColor::RunTest(const FString& Parameters)
{
	// Test green (>75%)
	FLinearColor Result = UNajikaBlueprintLibrary::GetStatusColor(80.0f);
	TestEqual(TEXT("GetStatusColor(80) should be Green"), Result, FLinearColor::Green);

	// Test yellow (50-75%)
	Result = UNajikaBlueprintLibrary::GetStatusColor(60.0f);
	TestEqual(TEXT("GetStatusColor(60) should be Yellow"), Result, FLinearColor::Yellow);

	// Test red (<25%)
	Result = UNajikaBlueprintLibrary::GetStatusColor(20.0f);
	TestEqual(TEXT("GetStatusColor(20) should be Red"), Result, FLinearColor::Red);

	return true;
}

// ============================================================
// PLATFORM DETECTION TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_PlatformDetection,
	"Najika.Unit.BlueprintLibrary.PlatformDetection",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_PlatformDetection::RunTest(const FString& Parameters)
{
	// Test platform name is not empty
	FString PlatformName = UNajikaBlueprintLibrary::GetPlatformName();
	TestTrue(TEXT("Platform name should not be empty"), !PlatformName.IsEmpty());

	// Test that we're on exactly one platform
	bool bIsWindows = UNajikaBlueprintLibrary::IsWindows();
	bool bIsAndroid = UNajikaBlueprintLibrary::IsAndroid();
	bool bIsIOS = UNajikaBlueprintLibrary::IsIOS();

	int32 PlatformCount = (bIsWindows ? 1 : 0) + (bIsAndroid ? 1 : 0) + (bIsIOS ? 1 : 0);
	TestEqual(TEXT("Should be on exactly one platform"), PlatformCount, 1);

	// Test mobile platform check
	bool bIsMobile = UNajikaBlueprintLibrary::IsMobilePlatform();
	TestEqual(TEXT("IsMobile should match (Android || iOS)"), bIsMobile, (bIsAndroid || bIsIOS));

	return true;
}

// ============================================================
// ARRAY UTILITIES TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_ShuffleStringArray,
	"Najika.Unit.BlueprintLibrary.ShuffleStringArray",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_ShuffleStringArray::RunTest(const FString& Parameters)
{
	TArray<FString> Original = {TEXT("A"), TEXT("B"), TEXT("C"), TEXT("D"), TEXT("E")};
	TArray<FString> Shuffled = UNajikaBlueprintLibrary::ShuffleStringArray(Original);

	// Test that array size is the same
	TestEqual(TEXT("Shuffled array should have same size"), Shuffled.Num(), Original.Num());

	// Test that all elements are present (order may differ)
	for (const FString& Element : Original)
	{
		TestTrue(TEXT("Shuffled array should contain all original elements"), Shuffled.Contains(Element));
	}

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_RemoveDuplicates,
	"Najika.Unit.BlueprintLibrary.RemoveDuplicates",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_RemoveDuplicates::RunTest(const FString& Parameters)
{
	TArray<FString> Input = {TEXT("A"), TEXT("B"), TEXT("A"), TEXT("C"), TEXT("B"), TEXT("D")};
	TArray<FString> Result = UNajikaBlueprintLibrary::RemoveDuplicates(Input);

	// Test that duplicates are removed
	TestEqual(TEXT("Result should have 4 unique elements"), Result.Num(), 4);

	// Test that all unique elements are present
	TestTrue(TEXT("Result should contain 'A'"), Result.Contains(TEXT("A")));
	TestTrue(TEXT("Result should contain 'B'"), Result.Contains(TEXT("B")));
	TestTrue(TEXT("Result should contain 'C'"), Result.Contains(TEXT("C")));
	TestTrue(TEXT("Result should contain 'D'"), Result.Contains(TEXT("D")));

	return true;
}

// ============================================================
// SUMMARY
// ============================================================

// Total tests: 15
// Categories: Math (4), String (4), Color (3), Platform (1), Array (2), JSON (future)
