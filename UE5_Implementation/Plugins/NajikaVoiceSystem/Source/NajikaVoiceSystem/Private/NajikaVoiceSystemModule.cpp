// Copyright Najika Development Team. All Rights Reserved.

#include "NajikaVoiceSystemModule.h"

#define LOCTEXT_NAMESPACE "FNajikaVoiceSystemModule"

void FNajikaVoiceSystemModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceSystem: Module started"));

	bModuleStarted = true;
}

void FNajikaVoiceSystemModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UE_LOG(LogTemp, Log, TEXT("NajikaVoiceSystem: Module shutdown"));

	bModuleStarted = false;
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FNajikaVoiceSystemModule, NajikaVoiceSystem)
