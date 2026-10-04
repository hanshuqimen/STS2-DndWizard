# D&D Wizard for Slay the Spire 2

A Wizard-inspired character with 37 individually illustrated cards, 6 relics, manual Upcast, HP-funded Overcast and run-scoped spellbook progression. Includes English and Simplified Chinese localization.

**Release: v0.4.0. Target: Windows Slay the Spire 2 v0.107.1 with BaseLib 3.3.2. This version has passed compilation, offline rule and resource checks. On 2026-10-04, the maintainer reported manually testing the latest version with no issues found.**

## Install

1. Close the game.
2. Install [BaseLib](https://github.com/Alchyr/BaseLib-StS2/releases); the development dependency is 3.3.2.
3. Download **DndWizard-v0.4.0-sts2-0.107.1.zip** from [Releases](https://github.com/hanshuqimen/STS2-DndWizard/releases/latest).
4. Extract its DndWizard folder into your game's mods directory.
5. Enable mods and start a new run as The Wizard.

The folder must directly contain DndWizard.dll, DndWizard.pck and DndWizard.json. No Steam Workshop subscription is required. GitHub's automatically generated Source code archive is not the installable mod. Other game/dependency versions and old-save migration have not been validated.

## Mechanics

Start with 6 Spell Slots. Slots persist between combats and refill when you choose Rest at a campfire. Smith does not refill them. Choose base casting or Upcast through a synchronized selection grid. Upcast increases hits, damage, Block or control depending on the spell.

Once per combat, missing slots can be paid with HP through Overcast. The choice lists the slot and HP payment; knowingly lethal base payments are excluded. Native HP-loss modifiers still apply.

Victories grant research XP: normal 1, elite 2, boss 3. Milestones at 3/7/12 XP increase capacity to 7/8/9, reduce Overcast HP cost at level 3 and unlock tier 4 at level 4. Research belongs to the current run and is saved with the spellbook.

Concentration spells are mutually exclusive: Ward, Evocation and Meditation support defense, multi-hit burst and sustained recovery. Two Cantrips restore one slot, at most once per turn.

## Build and validation

See [Build instructions](docs/BUILD.md). Requires .NET SDK 10, a local game install, BaseLib, a standalone Godot executable and sts2-modding-mcp's Python environment.

The CI checks pure casting/progression rules and authored content without game binaries. Full local builds also check imported textures and scenes. See [validation boundaries](TESTING.md).

## License and feedback

[MIT License](LICENSE). Original AI-generated illustrations and authored SVG icons are included; see [asset provenance](ASSETS.md). Game binaries, BaseLib and extracted game media are not distributed.

Report bugs through [Issues](https://github.com/hanshuqimen/STS2-DndWizard/issues), including game, BaseLib and mod versions plus reproduction steps. This is an independent fan project. Relevant game names and trademarks remain with their respective owners.
