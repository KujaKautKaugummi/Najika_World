// Copyright Najika Development Team. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

/**
 * Najika Voice System Module
 * Provides complete voice chat functionality with Whisper AI integration
 */
class FNajikaVoiceSystemModule : public IModuleInterface
{
public:
	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

private:
	/** Has module started up successfully */
	bool bModuleStarted;
};
