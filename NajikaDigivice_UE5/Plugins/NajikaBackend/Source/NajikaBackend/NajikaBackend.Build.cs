// NajikaBackend.Build.cs
// Build configuration for Najika Backend Plugin

using UnrealBuildTool;

public class NajikaBackend : ModuleRules
{
    public NajikaBackend(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        // Public dependencies - available to other modules
        PublicDependencyModuleNames.AddRange(new string[] {
            "Core",
            "CoreUObject",
            "Engine",
            "HTTP",
            "Json",
            "JsonUtilities"
        });

        // Private dependencies - only used internally
        PrivateDependencyModuleNames.AddRange(new string[] {
            "WebSockets",
            "AudioCapture",
            "AudioMixer",
            "InputCore",
            "Slate",
            "SlateCore"
        });

        // Android specific
        if (Target.Platform == UnrealTargetPlatform.Android)
        {
            PrivateDependencyModuleNames.Add("AndroidPermission");
        }
    }
}
