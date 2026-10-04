# v0.4.0 validation

On 2026-10-04, the maintainer confirmed that the latest version had been manually tested with no issues found. The tested scenarios were not individually documented. This is a maintainer-reported result; no new in-game testing was performed during publication.

No game bridge or game process is used by the public CI.

- Release compilation against local game v0.107.1 and BaseLib 3.3.2: 0 warnings, 0 errors.
- 5,339 offline assertions against the same pure SpellbookRules.cs used by gameplay: payment conservation, nonnegative resources, discounts, lethal-payment exclusion, once-per-combat eligibility and progression milestones.
- Content check: 37 unique original illustrations and runtime textures, 11 powers, 6 relics and matching Chinese/English localization keys.
- Standalone Godot resource checks: 58 textures and 3 scenes loaded without failures.

Reports: [rules](test-results/v0.4.0-rules.txt), [content](test-results/v0.4.0-static.json), [resources](test-results/v0.4.0-resources.json).

Not individually documented in the maintainer report: character/choice UI, actual combat resolution, HP-loss relic interactions, progression/save loading, old-save migration, multiplayer, full runs or balance. Godot 4.7.2 was used for offline asset authoring; the target game's runtime is 4.5.1.

CI runs only the pure rules and content checks. It cannot compile the full mod without locally supplied game and BaseLib assemblies.
