# Building from source

Players should use the [prebuilt release](https://github.com/hanshuqimen/STS2-DndWizard/releases/latest). These instructions are for development.

## Requirements

- .NET SDK 10 (the mod targets net9.0; standalone rule checks target net10.0).
- A local Windows game v0.107.1 install containing data_sts2_windows_x86_64/ and its game assemblies.
- BaseLib 3.3.2 in your game's mods/BaseLib/ directory.
- A standalone Godot console executable; offline assets were authored using 4.7.2.
- A local sts2-modding-mcp checkout with run.py and a venv Python environment containing mcp and Pillow. Install project requirements with that environment's pip if needed.

All illustration originals are included. No paid image generation is required to rebuild.

## MCP import compatibility

This project first imports textures with Godot and then calls the local MCP build_pck tool with convert_pngs=false.

The MCP packer must retain native .import files in that mode. In sts2mcp/pck_builder.py, if its skip condition is `if ext == ".import":`, update it to `if ext == ".import" and convert_pngs:`. Back up that file first. If your MCP version already preserves them, no edit is needed. This change is required because the native texture references must accompany the .ctex files.

## Build

```powershell
powershell -ExecutionPolicy Bypass -File .\Build.ps1 -GameDir "C:\Games\Slay the Spire 2" -McpRoot "C:\Tools\sts2-modding-mcp" -GodotExe "C:\Tools\Godot\Godot_console.exe"
```

Build.ps1 generates code/text, normalizes artwork, runs content validation, compiles, runs pure rule checks, imports and packages textures through MCP, and verifies resources. It does not start the game. Output is dist/DndWizard-v0.4.0-sts2-0.107.1.zip.

Add -Install to install after building, with the target game closed. Install.ps1 backs up this mod's existing files before replacement.

## Offline checks without game files

```powershell
dotnet run --project tests/Rules/Rules.csproj -c Release
python -m pip install -r requirements-dev.txt
python tools/validate_content.py
```

Edit generate_content.py rather than Code/Cards.g.cs or cards.json. Resource/payment code lives in Code/Arcana.cs, Code/UpcastChoice.cs and Code/SpellbookRules.cs.
