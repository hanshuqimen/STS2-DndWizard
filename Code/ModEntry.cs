using HarmonyLib;
using MegaCrit.Sts2.Core.Logging;
using MegaCrit.Sts2.Core.Modding;

namespace DndWizard;

[ModInitializer("Init")]
public static class ModEntry
{
    private static Harmony? _harmony;

    public static void Init()
    {
        Log.Warn("[DndWizard] Initializing...");

        _harmony = new Harmony("com.localmodproject.dndwizard");
        _harmony.PatchAll();

        Log.Warn("[DndWizard] Loaded successfully!");
    }
}
