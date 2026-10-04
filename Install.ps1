param([string]$GameDir = 'C:\Games\Slay the Spire 2')
$ErrorActionPreference = 'Stop'
$gameRoot = (Resolve-Path -LiteralPath $GameDir).Path
if (-not (Test-Path -LiteralPath (Join-Path $gameRoot 'SlayTheSpire2.exe'))) { throw 'Not a Slay the Spire 2 installation.' }
if (-not (Test-Path -LiteralPath (Join-Path $gameRoot 'mods\BaseLib\BaseLib.dll'))) { throw 'BaseLib 3.3.2 is required.' }
$active = Get-Process -Name SlayTheSpire2 -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq (Join-Path $gameRoot 'SlayTheSpire2.exe') }
if ($active) { throw 'Close the target game before installing.' }
$source = Join-Path $PSScriptRoot 'dist\DndWizard'
$target = Join-Path $gameRoot 'mods\DndWizard'
$files = @('DndWizard.dll', 'DndWizard.pck', 'DndWizard.json')
foreach ($file in $files) { if (-not (Test-Path -LiteralPath (Join-Path $source $file))) { throw "Build first: missing $file" } }
New-Item -ItemType Directory -Path $target -Force | Out-Null
$backup = Join-Path $PSScriptRoot ('install-backups\' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $backup -Force | Out-Null
# Back up only this mod's known files; never recurse through the game's mods or saves.
foreach ($file in @('DndWizard.dll','DndWizard.pck','DndWizard.json','mod_manifest.json','DndWizard.deps.json','DndWizard.runtimeconfig.json')) {
    $oldFile = Join-Path $target $file
    if (Test-Path -LiteralPath $oldFile) { Move-Item -LiteralPath $oldFile -Destination (Join-Path $backup $file) }
}
foreach ($file in $files) { Copy-Item -LiteralPath (Join-Path $source $file) -Destination (Join-Path $target $file) }
Write-Host "Installed: $target"
Write-Host "Previous files: $backup"
