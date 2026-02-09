// NajikaBackendModule.cpp
// Module implementation

#include "NajikaBackendModule.h"

#define LOCTEXT_NAMESPACE "FNajikaBackendModule"

void FNajikaBackendModule::StartupModule()
{
    UE_LOG(LogTemp, Log, TEXT("[Najika] Backend Module loaded!"));
}

void FNajikaBackendModule::ShutdownModule()
{
    UE_LOG(LogTemp, Log, TEXT("[Najika] Backend Module unloaded!"));
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FNajikaBackendModule, NajikaBackend)
