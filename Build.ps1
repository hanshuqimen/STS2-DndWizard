param(
    [string]$GameDir = 'C:\Games\Slay the Spire 2',
    [string]$McpRoot = 'C:\Tools\sts2-modding-mcp',
    [string]$GodotExe = 'C:\Tools\Godot\Godot_console.exe',
    [switch]$Install
)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$pythonExe = Join-Path $McpRoot 'venv\Scripts\python.exe'
$env:STS2_MCP_ROOT = $McpRoot
$env:STS2_GAME_DIR = $GameDir
$env:GODOT_EXE = $GodotExe
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
foreach ($required in @($pythonExe, $GodotExe, (Join-Path $GameDir 'data_sts2_windows_x86_64\sts2.dll'), (Join-Path $GameDir 'mods\BaseLib\BaseLib.dll'))) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Required dependency missing: $required" }
}
function Assert-Exit([string]$Step) { if ($LASTEXITCODE -ne 0) { throw "$Step failed with exit code $LASTEXITCODE" } }
& $pythonExe (Join-Path $projectRoot 'generate_content.py')
Assert-Exit 'Content generation'
& $pythonExe (Join-Path $projectRoot 'tools\make_card_reference.py')
Assert-Exit 'Card reference generation'
& $pythonExe (Join-Path $projectRoot 'generate_assets.py')
Assert-Exit 'Asset generation'
& $GodotExe --headless --script (Join-Path $projectRoot 'rasterize.gd') -- (Join-Path $projectRoot 'raster-jobs.json')
Assert-Exit 'SVG rasterization'
& $GodotExe --headless --script (Join-Path $projectRoot 'tools\card_art_preview.gd') -- $projectRoot
Assert-Exit 'Card artwork dimensions and contact sheets'
& $pythonExe (Join-Path $projectRoot 'tools\validate_content.py')
Assert-Exit 'Offline content and localization validation'
& dotnet build (Join-Path $projectRoot 'DndWizard.csproj') -c Release --nologo "-p:GameDir=$GameDir"
Assert-Exit 'C# build'
& dotnet run --project (Join-Path $projectRoot 'tests\Rules\Rules.csproj') -c Release | Tee-Object -FilePath (Join-Path $projectRoot 'test-results\v0.4.0-rules.txt')
Assert-Exit 'Offline casting and progression rules'
& $pythonExe (Join-Path $projectRoot 'prepare_pack.py')
Assert-Exit 'Godot import'
$packArgs = Join-Path $projectRoot 'build\pack-arguments.json'
@{source_dir=(Join-Path $projectRoot 'build\pack'); output_path=(Join-Path $projectRoot 'DndWizard.pck'); convert_pngs=$false} | ConvertTo-Json | Set-Content -LiteralPath $packArgs -Encoding utf8
& $pythonExe (Join-Path $projectRoot 'tools\mcp_call.py') build_pck $packArgs
Assert-Exit 'MCP resource package'
& $GodotExe --headless --script (Join-Path $projectRoot 'verify_pack.gd') -- (Join-Path $projectRoot 'DndWizard.pck') (Join-Path $projectRoot 'raster-jobs.json') (Join-Path $projectRoot 'test-results\v0.4.0-resources.json')
Assert-Exit 'Resource loading verification (MCP must retain native .import files)'
$distRoot = Join-Path $projectRoot 'dist'
$modOutput = Join-Path $distRoot 'DndWizard'
New-Item -ItemType Directory -Force -Path $modOutput | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot 'bin\Release\net9.0\DndWizard.dll') -Destination $modOutput -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'DndWizard.pck') -Destination $modOutput -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'mod_manifest.json') -Destination (Join-Path $modOutput 'DndWizard.json') -Force
Compress-Archive -LiteralPath $modOutput -DestinationPath (Join-Path $distRoot 'DndWizard-v0.4.0-sts2-0.107.1.zip') -Force
Get-ChildItem -LiteralPath $modOutput -File | Get-FileHash -Algorithm SHA256 | Select-Object Hash,@{Name='File';Expression={Split-Path $_.Path -Leaf}} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $distRoot 'SHA256.json') -Encoding utf8
if ($Install) { & (Join-Path $projectRoot 'Install.ps1') -GameDir $GameDir }
Write-Host "Build and resource verification passed. Package: $distRoot"

