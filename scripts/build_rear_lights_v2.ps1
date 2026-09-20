param([switch]$Install)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    function Run([string]$Program, [string[]]$Arguments) {
        & $Program @Arguments
        if ($LASTEXITCODE -ne 0) { throw "Failed: $Program ($LASTEXITCODE)" }
    }
    $v2 = 'versions\v2-mustang-shelby'
    $out = "$v2\work\fusion-rear-lenses"
    New-Item -ItemType Directory -Force $out | Out-Null
    $csc = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
    Run 'tools\blender-4.5.14-windows-x64\blender.exe' @('--background','--factory-startup','--python-exit-code','1','--python','scripts\export_fusion_rear_lights.py')
    Run $csc @('/nologo','/r:tools\mwgc\mwgc.exe','/out:tools\mwgc\ReplaceRearLights.exe','scripts\ReplaceRearLights.cs')
    Run 'tools\mwgc\mwgc.exe' @('-nowait','-xname','MUSTANGGT',"$out\fusion-rear-lenses.mwr","$out\lights.bin")
    Run 'tools\mwgc\ReplaceRearLights.exe' @("$v2\release\MUSTANGGT\GEOMETRY.BIN","$out\lights.bin","$out\GEOMETRY.BIN")
    Run 'tools\mwgc\InspectGeometry.exe' @("$out\GEOMETRY.BIN","$out\geometry.json")
    Run 'tools\dotnet\dotnet.exe' @('scripts\validator\bin\Release\net8.0\Validator.dll',"$out\GEOMETRY.BIN","$out\validation.json")
    if ($Install) {
        $game = 'D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition\CARS\MUSTANGGT'
        if (Get-Process speed -ErrorAction SilentlyContinue) { throw 'Close the game before installation.' }
        $backup = Join-Path $out ('backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
        New-Item -ItemType Directory -Path $backup | Out-Null
        Copy-Item -LiteralPath "$game\GEOMETRY.BIN" -Destination "$backup\game-GEOMETRY.BIN"
        Copy-Item -LiteralPath "$v2\release\MUSTANGGT\GEOMETRY.BIN" -Destination "$backup\release-GEOMETRY.BIN"
        Copy-Item -LiteralPath "$out\GEOMETRY.BIN" -Destination "$v2\release\MUSTANGGT\GEOMETRY.BIN" -Force
        Copy-Item -LiteralPath "$out\GEOMETRY.BIN" -Destination "$game\GEOMETRY.BIN" -Force
        $expected = (Get-FileHash -LiteralPath "$out\GEOMETRY.BIN").Hash
        if ((Get-FileHash -LiteralPath "$game\GEOMETRY.BIN").Hash -ne $expected) { throw 'Installed hash differs' }
        Write-Output "Installed Fusion rear lenses: $expected"
    }
} finally { Pop-Location }
