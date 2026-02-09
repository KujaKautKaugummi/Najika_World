// NajikaBackendModule.h
// Main module header for Najika Backend Plugin

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class FNajikaBackendModule : public IModuleInterface
{
public:
    /** IModuleInterface implementation */
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
};
