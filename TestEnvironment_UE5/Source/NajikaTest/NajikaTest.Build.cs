// NajikaTest.Build.cs
// Unreal Build Tool configuration for Model 2 Test Environment

using UnrealBuildTool;

public class NajikaTest : ModuleRules
{
    public NajikaTest(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "HeadMountedDisplay",
            "EnhancedInput"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            // Add private dependencies here
        });

        // For Android deployment (Xiaomi 11T Pro)
        if (Target.Platform == UnrealTargetPlatform.Android)
        {
            PublicDependencyModuleNames.AddRange(new string[]
            {
                "OnlineSubsystem",
                "OnlineSubsystemUtils"
            });
        }

        // Uncomment if you are using Slate UI
        // PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

        // Uncomment if you are using online features
        // PrivateDependencyModuleNames.Add("OnlineSubsystem");
    }
}
