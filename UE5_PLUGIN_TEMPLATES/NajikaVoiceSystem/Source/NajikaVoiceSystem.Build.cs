// Copyright Model 1 - Najika Digivice APK

using UnrealBuildTool;

public class NajikaVoiceSystem : ModuleRules
{
	public NajikaVoiceSystem(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"HTTP",              // HTTP requests
				"Json",              // JSON parsing
				"JsonUtilities",     // JSON utilities
				"AudioCapture",      // Microphone capture
				"AudioMixer",        // Audio playback
				"Voice"              // Voice processing
			}
		);

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"WebSockets"         // WebSocket support for streaming
			}
		);

		// Android-specific settings
		if (Target.Platform == UnrealTargetPlatform.Android)
		{
			PublicDependencyModuleNames.Add("AndroidPermission");
		}
	}
}
