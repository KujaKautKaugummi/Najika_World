// Copyright Claude Code. All Rights Reserved.

#include "NajikaBackendClientModule.h"

#define LOCTEXT_NAMESPACE "FNajikaBackendClientModule"

void FNajikaBackendClientModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	UE_LOG(LogTemp, Log, TEXT("[NajikaBackendClient] Module Started"));
}

void FNajikaBackendClientModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module. For modules that support dynamic reloading,
	// we call this function before unloading the module.
	UE_LOG(LogTemp, Log, TEXT("[NajikaBackendClient] Module Shutdown"));
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FNajikaBackendClientModule, NajikaBackendClient)
