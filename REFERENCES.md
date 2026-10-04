# Reference study

Reviewed locally on 2026-09-28/29. The repositories were read for architectural patterns. Their source and media are not included in the distributable.

| Project | Reviewed revision | Files / lesson used |
|---|---|---|
| [TheImmortal-StS2](https://github.com/Autmn7/TheImmortal-StS2) | `f2838c004556e4f6f61ab21ad7764dced2780128` | `MokouModCode/Character/MokouMod.cs`: separate character pools, starting deck, explicit visual paths. README warns of beta-only support, so its signatures were not assumed compatible. |
| [STS2_MarisaMod](https://github.com/lf201014/STS2_MarisaMod) | `89454443032c8debebfd365bf1e2cd5db32b95d1` | `Scripts/Cards/AbstractMarisaCard.cs`, `Scripts/Powers/ChargeUpPower.cs`, `Scripts/Characters/MarisaCharacter.cs`: pool attribute on an abstract card family, owner-scoped resource powers, localized character and scene overrides. |
| [sts2-wuwa-denia](https://github.com/Sirius882/sts2-wuwa-denia) | `5822fb2433a9fceaa0e7e9b72dc91e07fb880d4e` | `src/Core/Denia.cs`, `src/Core/DeniaSyncStatePowers.cs`: represent battle counters as model powers instead of unsynchronized global fields; distinguish baseline placeholder scenes from custom visuals. |
| [Sts2-FlagellantMod](https://github.com/JerryCatJim/Sts2-FlagellantMod) | `8c7bc8da4751c9b4be43dcabd7537d9e29be2b6b` | `Code/Character/Flagellant.cs`: independent character/relic/potion pools and explicit separation of combat, camp, shop, portrait and transition resources. |

Local authority: `sts2.dll` v0.107.1 (commit `59260271`), installed BaseLib 3.3.2, and MCP's locally decompiled game source. BaseLib was inspected locally to confirm custom-model and scene-conversion interfaces. No game DLLs, BaseLib binaries or extracted game assets are redistributed.

## Build compatibility

The current build uses local game and BaseLib assemblies, native Godot texture imports, and MCP packaging. See [BUILD.md](docs/BUILD.md) for the required .import retention fix. No local backup paths or live-game bridge records are distributed. The installer copies only the DLL, PCK and one manifest.

## Art provenance

v0.2 replaces all 32 card portraits with independently generated paintings using built-in `image_gen.imagegen`. Full prompt and source records are in `art-source/illustrations/generation-record.json`; authoring direction and QA are documented in `ART-v0.2.md`. Original generated files are kept alongside runtime 512×384 imports. The SVG card sigils below describe v0.1; SVG geometry remains in use for UI, powers and relics only.

`art-source/wizard-original.png` was created using the built-in ImageGen tool for this project, then resized with alpha preserved to `DndWizard/images/wizard.png`. The generated image has transparent corners and approximately 46.8% fully transparent pixels. It is an original wizard concept, not a copied reference-mod character.

Generation prompt: One original full-body fantasy wizard sprite, transparent background, three-quarter view facing right, silver beard, midnight-blue robes and pointed hat, parchment-gold trim, open spellbook, wooden staff with cyan crystal; chunky readable silhouette, stylized ink-and-gouache game art, no text, scenery, borders or existing-character imitation.

Card, relic, power and energy symbols are authored SVG geometry in `generate_assets.py` and `art-source/`, rasterized through Godot. Palette: midnight blue, muted gold, cyan; fire/ice/acid motifs use distinct accent colors. Original sprite uses 640×960 RGBA; cards 512×384; most icons 320×320; energy 128×128 and inline energy 24×24. Existing game audio, trail, rest/shop and energy-counter scenes are referenced at runtime and not copied into the package.
