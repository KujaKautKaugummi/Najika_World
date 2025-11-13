# UE5 Testing Framework for Najika Digivice

**Project:** Najika Digivice UE5 Migration
**Testing Framework:** Unreal Automation Testing
**Date:** 2025-11-13

---

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Unit Tests](#unit-tests)
3. [Integration Tests](#integration-tests)
4. [Performance Tests](#performance-tests)
5. [Test Execution](#test-execution)
6. [CI/CD Integration](#cicd-integration)

---

## Testing Overview

### Test Categories

**Unit Tests:**
- Blueprint Function Library (math, string, JSON utilities)
- Data structures (FNajikaState, FNajikaLivingState parsing)
- Utility functions (time formatting, color conversion)

**Integration Tests:**
- HTTP Client (mock backend responses)
- Character state synchronization
- UI widget updates

**Performance Tests:**
- Animation system (frame rate monitoring)
- HTTP client throughput
- UI rendering performance

---

## Unit Tests

### Test Files

**1. NajikaBlueprintLibrary.spec.cpp**
- Test all Blueprint Function Library functions
- JSON parsing/serialization
- Math utilities (lerp, clamp, map range)
- String formatting
- Platform detection

**2. NajikaBackendTypes.spec.cpp**
- Test data structure initialization
- JSON serialization/deserialization
- Default values

**3. NajikaGameState.spec.cpp**
- Test world time updates
- Day/night cycle
- Event system

**Test Structure:**
```cpp
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FNajikaTestClassName,
    "Najika.Unit.ClassName.TestName",
    EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::ProductFilter
)

bool FNajikaTestClassName::RunTest(const FString& Parameters)
{
    // Arrange
    // Act
    // Assert
    return true;
}
```

---

## Integration Tests

### Test Files

**1. NajikaHttpClient.integration.cpp**
- Mock HTTP server responses
- Test all API endpoints
- Test error handling
- Test timeout handling

**2. NajikaCharacter.integration.cpp**
- Test backend state synchronization
- Test care actions (Feed, Drink, Wash, Sleep)
- Test combat system
- Test equipment changes

**3. NajikaUIWidget.integration.cpp**
- Test UI updates from state changes
- Test button click handlers
- Test notification system

---

## Performance Tests

### Test Files

**1. NajikaPerformance.perf.cpp**
- Measure HTTP client throughput (requests/second)
- Measure animation system performance (FPS)
- Measure UI update performance
- Memory usage monitoring

**Performance Benchmarks:**
- HTTP Client: >100 requests/second
- Animation System: Stable 60 FPS
- UI Updates: <5ms per frame
- Memory Usage: <500 MB

---

## Test Execution

### Running Tests

**From Editor:**
1. Open Session Frontend (Window → Developer Tools → Session Frontend)
2. Select Automation tab
3. Select tests to run
4. Click "Start Tests"

**From Command Line:**
```batch
UE5Editor-Cmd.exe "C:/NajikaDigivice_UE5/NajikaDigivice/NajikaDigivice.uproject" ^
    -ExecCmds="Automation RunTests Najika" ^
    -unattended -nopause -testexit="Automation Test Queue Empty" ^
    -log -ReportOutputPath="C:/NajikaDigivice_UE5/TestReports"
```

**From .bat Script:**
See Phase 8: RunTests.bat

---

## CI/CD Integration

### GitHub Actions Workflow

**File:** `.github/workflows/unreal-tests.yml`

```yaml
name: Unreal Engine Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v2

    - name: Setup Unreal Engine
      uses: game-ci/unity-builder@v2
      # Configure UE5 installation path

    - name: Run Unit Tests
      run: |
        RunTests.bat

    - name: Upload Test Results
      uses: actions/upload-artifact@v2
      with:
        name: test-results
        path: TestReports/
```

---

## Test Coverage Goals

**Target Coverage:** 80%

**Priority Areas (100% coverage):**
- Blueprint Function Library (all functions)
- JSON parsing (FNajikaState, FNajikaLivingState)
- HTTP Client (all endpoints)

**Medium Priority (60% coverage):**
- Game classes (Character, GameMode, GameState)
- UI widgets (HUD, Chat, Status)

**Low Priority (40% coverage):**
- Animation Blueprint logic
- Material parameter calculations

---

## Test File Locations

```
UE5_Implementation/Source/NajikaDigivice/Tests/
├── Unit/
│   ├── NajikaBlueprintLibrary.spec.cpp
│   ├── NajikaBackendTypes.spec.cpp
│   └── NajikaGameState.spec.cpp
├── Integration/
│   ├── NajikaHttpClient.integration.cpp
│   ├── NajikaCharacter.integration.cpp
│   └── NajikaUIWidget.integration.cpp
└── Performance/
    └── NajikaPerformance.perf.cpp
```

---

## Mock Objects

### MockHttpClient

**Purpose:** Mock HTTP responses for testing without backend.

```cpp
class FMockHttpClient
{
public:
    void SetMockResponse(const FString& Endpoint, const FString& JsonResponse);
    void SimulateNetworkDelay(float DelaySeconds);
    void SimulateNetworkError(int32 ErrorCode);
};
```

### MockGameState

**Purpose:** Mock game state for UI testing.

```cpp
class FMockGameState
{
public:
    FNajikaState GetMockNajikaState();
    FNajikaLivingState GetMockLivingState();
};
```

---

## Test Data

### Sample JSON Responses

**File:** `Tests/Data/mock_responses.json`

```json
{
    "najika_status": {
        "hunger": 85.0,
        "thirst": 90.0,
        "energy": 70.0,
        "hygiene": 60.0,
        "happiness": 95.0,
        "strength": 15,
        "intelligence": 20,
        "dexterity": 18,
        "charisma": 25
    },
    "chat_response": {
        "response": "Hallo! Wie geht es dir?",
        "najika_state": { ... },
        "living_state": { ... }
    }
}
```

---

## Continuous Testing

### Pre-Commit Hook

**File:** `.git/hooks/pre-commit`

```bash
#!/bin/sh
# Run quick unit tests before commit
echo "Running unit tests..."
RunTests.bat -quick
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

### Nightly Test Run

**Scheduled Test Execution:**
- Time: 2:00 AM daily
- Run all tests (unit, integration, performance)
- Generate test report
- Email results to team

---

## Notes

- All test files use `IMPLEMENT_SIMPLE_AUTOMATION_TEST` macro
- Test names follow pattern: `Najika.[Unit|Integration|Performance].[Class].[TestName]`
- Use `TestTrue()`, `TestFalse()`, `TestEqual()` for assertions
- Mock objects must clean up resources in destructor
- Performance tests should run for at least 10 seconds for accurate results

---

**END OF TESTING_FRAMEWORK.md**
