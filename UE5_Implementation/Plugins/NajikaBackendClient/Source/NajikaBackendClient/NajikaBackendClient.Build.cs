// Copyright Claude Code. All Rights Reserved.

using UnrealBuildTool;

public class NajikaBackendClient : ModuleRules
{
	public NajikaBackendClient(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicIncludePaths.AddRange(
			new string[] {
				// Add public include paths required here
			}
		);

		PrivateIncludePaths.AddRange(
			new string[] {
				// Add other private include paths required here
			}
		);

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"Engine",
				"HTTP",
				"WebSockets",
				"Json",
				"JsonUtilities"
			}
		);

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"Slate",
				"SlateCore"
			}
		);

		DynamicallyLoadedModuleNames.AddRange(
			new string[]
			{
				// Add any modules that your module loads dynamically here
			}
		);
	}
}
