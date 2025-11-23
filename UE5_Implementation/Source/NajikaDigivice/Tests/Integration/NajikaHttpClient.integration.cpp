// Copyright Claude Code. All Rights Reserved.

#include "Misc/AutomationTest.h"
#include "NajikaHttpClient.h"
#include "NajikaBackendTypes.h"
#include "JsonObjectConverter.h"

// ============================================================
// MOCK HTTP CLIENT
// ============================================================

/**
 * Mock HTTP Client for testing without backend
 * Simulates HTTP responses with predefined data
 */
class FMockHttpClient
{
public:
	static FString GetMockNajikaStatusResponse()
	{
		return TEXT(R"({
			"najika": {
				"hunger": 85.0,
				"thirst": 90.0,
				"energy": 70.0,
				"hygiene": 60.0,
				"happiness": 95.0,
				"strength": 15,
				"intelligence": 20,
				"dexterity": 18,
				"charisma": 25,
				"care_mistakes": 2,
				"fatigue": 10.0,
				"weight": 52.5,
				"discipline": 75.0,
				"level": 5,
				"xp": 250,
				"evolution_stage": "champion",
				"equipment": {
					"weapon": "iron_sword",
					"armor": "leather_vest",
					"accessory": "magic_ring"
				},
				"last_fed": 0.0,
				"last_trained": 0.0,
				"last_sleep": 0.0,
				"last_update": 0.0
			},
			"living": {
				"current_mood": "happy",
				"mood_intensity": 80,
				"living_hunger": 85.0,
				"living_energy": 70.0,
				"mood_game": 90.0,
				"anger_level": 5.0,
				"auto_care_enabled": true,
				"control_mode": "ai",
				"player_online": true,
				"autonomy_level": 60,
				"growth_stage": "developing",
				"relationship_stage": "friend",
				"emotional_bond": 50,
				"current_activity": "reading"
			}
		})");
	}

	static FString GetMockChatResponse()
	{
		return TEXT(R"({
			"response": "Hallo! Wie geht es dir heute?",
			"najika_state": {
				"hunger": 85.0,
				"thirst": 90.0,
				"energy": 70.0,
				"hygiene": 60.0,
				"happiness": 95.0
			},
			"living_state": {
				"current_mood": "happy",
				"mood_intensity": 80
			}
		})");
	}

	static FString GetMockActionResponse(bool bSuccess = true)
	{
		if (bSuccess)
		{
			return TEXT(R"({
				"status": "success",
				"message": "Action completed successfully"
			})");
		}
		else
		{
			return TEXT(R"({
				"status": "error",
				"message": "Action failed"
			})");
		}
	}
};

// ============================================================
// HTTP CLIENT INITIALIZATION TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_HttpClient_Initialize,
	"Najika.Integration.HttpClient.Initialize",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_HttpClient_Initialize::RunTest(const FString& Parameters)
{
	// Create HTTP client
	UNajikaHttpClient* Client = NewObject<UNajikaHttpClient>();
	TestNotNull(TEXT("HTTP Client should be created"), Client);

	// Initialize with default URL
	Client->Initialize();
	FString BaseURL = Client->GetBaseURL();
	TestEqual(TEXT("Default base URL should be http://127.0.0.1:8000"), BaseURL, TEXT("http://127.0.0.1:8000"));

	// Initialize with custom URL
	Client->Initialize(TEXT("http://192.168.1.100:8080"));
	BaseURL = Client->GetBaseURL();
	TestEqual(TEXT("Custom base URL should be set"), BaseURL, TEXT("http://192.168.1.100:8080"));

	return true;
}

// ============================================================
// JSON PARSING TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_HttpClient_ParseNajikaState,
	"Najika.Integration.HttpClient.ParseNajikaState",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_HttpClient_ParseNajikaState::RunTest(const FString& Parameters)
{
	// Get mock response
	FString JsonResponse = FMockHttpClient::GetMockNajikaStatusResponse();

	// Parse JSON
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonResponse);
	bool bParsed = FJsonSerializer::Deserialize(Reader, JsonObject);

	TestTrue(TEXT("JSON should parse successfully"), bParsed);
	TestTrue(TEXT("JSON object should be valid"), JsonObject.IsValid());

	// Extract najika object
	const TSharedPtr<FJsonObject>* NajikaObject;
	bool bHasNajika = JsonObject->TryGetObjectField(TEXT("najika"), NajikaObject);
	TestTrue(TEXT("JSON should have 'najika' field"), bHasNajika);

	// Test field values
	if (bHasNajika && NajikaObject->IsValid())
	{
		double Hunger = (*NajikaObject)->GetNumberField(TEXT("hunger"));
		TestEqual(TEXT("Hunger should be 85.0"), Hunger, 85.0, 0.01);

		int32 Strength = (*NajikaObject)->GetIntegerField(TEXT("strength"));
		TestEqual(TEXT("Strength should be 15"), Strength, 15);

		FString EvolutionStage = (*NajikaObject)->GetStringField(TEXT("evolution_stage"));
		TestEqual(TEXT("Evolution stage should be 'champion'"), EvolutionStage, TEXT("champion"));
	}

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_HttpClient_ParseLivingState,
	"Najika.Integration.HttpClient.ParseLivingState",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_HttpClient_ParseLivingState::RunTest(const FString& Parameters)
{
	// Get mock response
	FString JsonResponse = FMockHttpClient::GetMockNajikaStatusResponse();

	// Parse JSON
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonResponse);
	bool bParsed = FJsonSerializer::Deserialize(Reader, JsonObject);

	TestTrue(TEXT("JSON should parse successfully"), bParsed);

	// Extract living object
	const TSharedPtr<FJsonObject>* LivingObject;
	bool bHasLiving = JsonObject->TryGetObjectField(TEXT("living"), LivingObject);
	TestTrue(TEXT("JSON should have 'living' field"), bHasLiving);

	// Test field values
	if (bHasLiving && LivingObject->IsValid())
	{
		FString CurrentMood = (*LivingObject)->GetStringField(TEXT("current_mood"));
		TestEqual(TEXT("Current mood should be 'happy'"), CurrentMood, TEXT("happy"));

		int32 MoodIntensity = (*LivingObject)->GetIntegerField(TEXT("mood_intensity"));
		TestEqual(TEXT("Mood intensity should be 80"), MoodIntensity, 80);

		int32 AutonomyLevel = (*LivingObject)->GetIntegerField(TEXT("autonomy_level"));
		TestEqual(TEXT("Autonomy level should be 60"), AutonomyLevel, 60);
	}

	return true;
}

// ============================================================
// DATA STRUCTURE TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_NajikaState_Defaults,
	"Najika.Integration.DataStructures.NajikaState_Defaults",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_NajikaState_Defaults::RunTest(const FString& Parameters)
{
	// Create default state
	FNajikaState State;

	// Test default values
	TestEqual(TEXT("Default hunger should be 100"), State.Hunger, 100.0f);
	TestEqual(TEXT("Default thirst should be 100"), State.Thirst, 100.0f);
	TestEqual(TEXT("Default energy should be 100"), State.Energy, 100.0f);
	TestEqual(TEXT("Default hygiene should be 100"), State.Hygiene, 100.0f);
	TestEqual(TEXT("Default happiness should be 100"), State.Happiness, 100.0f);

	TestEqual(TEXT("Default strength should be 10"), State.Strength, 10);
	TestEqual(TEXT("Default intelligence should be 10"), State.Intelligence, 10);
	TestEqual(TEXT("Default dexterity should be 10"), State.Dexterity, 10);
	TestEqual(TEXT("Default charisma should be 10"), State.Charisma, 10);

	TestEqual(TEXT("Default care mistakes should be 0"), State.CareMistakes, 0);
	TestEqual(TEXT("Default weight should be 50"), State.Weight, 50.0f);
	TestEqual(TEXT("Default level should be 1"), State.Level, 1);
	TestEqual(TEXT("Default XP should be 0"), State.XP, 0);

	TestEqual(TEXT("Default evolution stage should be 'base'"), State.EvolutionStage, TEXT("base"));

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_NajikaLivingState_Defaults,
	"Najika.Integration.DataStructures.NajikaLivingState_Defaults",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_NajikaLivingState_Defaults::RunTest(const FString& Parameters)
{
	// Create default living state
	FNajikaLivingState State;

	// Test default values
	TestEqual(TEXT("Default mood should be 'neutral'"), State.CurrentMood, TEXT("neutral"));
	TestEqual(TEXT("Default mood intensity should be 50"), State.MoodIntensity, 50);

	TestEqual(TEXT("Default living hunger should be 100"), State.LivingHunger, 100.0f);
	TestEqual(TEXT("Default living energy should be 100"), State.LivingEnergy, 100.0f);
	TestEqual(TEXT("Default mood game should be 100"), State.MoodGame, 100.0f);

	TestEqual(TEXT("Default anger level should be 0"), State.AngerLevel, 0.0f);
	TestEqual(TEXT("Default auto care should be true"), State.bAutoCareEnabled, true);

	TestEqual(TEXT("Default control mode should be 'ai'"), State.ControlMode, TEXT("ai"));
	TestEqual(TEXT("Default player online should be false"), State.bPlayerOnline, false);

	TestEqual(TEXT("Default autonomy level should be 50"), State.AutonomyLevel, 50);
	TestEqual(TEXT("Default growth stage should be 'developing'"), State.GrowthStage, TEXT("developing"));
	TestEqual(TEXT("Default relationship stage should be 'getting_to_know'"), State.RelationshipStage, TEXT("getting_to_know"));
	TestEqual(TEXT("Default emotional bond should be 0"), State.EmotionalBond, 0);

	return true;
}

// ============================================================
// MOCK API ENDPOINT TESTS
// ============================================================

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNajikaTest_HttpClient_MockActionResponse,
	"Najika.Integration.HttpClient.MockActionResponse",
	EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTest_HttpClient_MockActionResponse::RunTest(const FString& Parameters)
{
	// Get mock success response
	FString SuccessResponse = FMockHttpClient::GetMockActionResponse(true);

	// Parse JSON
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(SuccessResponse);
	bool bParsed = FJsonSerializer::Deserialize(Reader, JsonObject);

	TestTrue(TEXT("Success response should parse"), bParsed);

	FString Status = JsonObject->GetStringField(TEXT("status"));
	TestEqual(TEXT("Status should be 'success'"), Status, TEXT("success"));

	FString Message = JsonObject->GetStringField(TEXT("message"));
	TestTrue(TEXT("Message should not be empty"), !Message.IsEmpty());

	// Get mock error response
	FString ErrorResponse = FMockHttpClient::GetMockActionResponse(false);

	Reader = TJsonReaderFactory<>::Create(ErrorResponse);
	bParsed = FJsonSerializer::Deserialize(Reader, JsonObject);

	TestTrue(TEXT("Error response should parse"), bParsed);

	Status = JsonObject->GetStringField(TEXT("status"));
	TestEqual(TEXT("Status should be 'error'"), Status, TEXT("error"));

	return true;
}

// ============================================================
// SUMMARY
// ============================================================

// Total integration tests: 6
// Categories: Initialization (1), JSON Parsing (2), Data Structures (2), Mock API (1)
//
// NOTE: Full HTTP client integration tests with real network requests
// should be run in a separate test suite with a mock backend server.
// These tests focus on data structure validation and JSON parsing logic.
