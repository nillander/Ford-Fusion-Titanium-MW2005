param([switch]$Install, [switch]$RearOnly)
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
    Run $csc @('/nologo','/r:tools\mwgc\mwgc.exe','/main:AttachRearLenses','/out:tools\mwgc\AttachRearLenses.exe','scripts\AppendPartMeshes.cs','scripts\AttachRearLenses.cs')
    Run 'tools\mwgc\mwgc.exe' @('-nowait','-xname','MUSTANGGT',"$out\fusion-rear-lenses.mwr","$out\lights.bin")
    # Use a fixed pre-attachment baseline; repeated runs must not accumulate lenses.
    $baseline = "$out\baseline-before-base-attachment.bin"
    if (!(Test-Path -LiteralPath $baseline)) { throw "Missing fixed baseline: $baseline. Do not substitute an already patched release." }
    if ((Get-FileHash -LiteralPath $baseline).Hash -ne '76C1C1BBD1DA8001D6AA7C3412C1CE9042923B7ACCEB7CEB7521FD12D208296C') { throw 'Unexpected baseline hash; refusing to accumulate or replace existing geometry.' }
    Run 'tools\mwgc\AttachRearLenses.exe' @($baseline,"$out\lights.bin","$out\rear-GEOMETRY.BIN")
    if ($RearOnly) {
        Copy-Item -LiteralPath "$out\rear-GEOMETRY.BIN" -Destination "$out\GEOMETRY.BIN" -Force
    } else {
        $front = "$v2\work\fusion-front-lenses"
        Run 'tools\blender-4.5.14-windows-x64\blender.exe' @('--background','--factory-startup','--python-exit-code','1','--python','scripts\export_fusion_rear_lights.py','--','--front')
        Run 'tools\mwgc\mwgc.exe' @('-nowait','-xname','MUSTANGGT',"$front\fusion-front-lenses.mwr","$front\lights.bin")
        Run 'tools\mwgc\AttachRearLenses.exe' @("$out\rear-GEOMETRY.BIN","$front\lights.bin","$out\GEOMETRY.BIN")
    }
    Run 'tools\mwgc\InspectGeometry.exe' @("$out\GEOMETRY.BIN","$out\geometry.json")
    Run 'tools\dotnet\dotnet.exe' @('scripts\validator\bin\Release\net8.0\Validator.dll',"$out\GEOMETRY.BIN","$out\validation.json")
    Run 'work\venv\Scripts\python.exe' @('scripts\prepare_fusion_rear_tpk.py')
    Run 'tools\dotnet\dotnet.exe' @('scripts\validator\bin\Release\net8.0\Validator.dll',"$out\tpk\TEXTURES.BIN","$out\tpk-validation.json","$out\verified-textures")
    if ($Install) {
        $gameRoot = 'D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition'
        if (Get-Process speed -ErrorAction SilentlyContinue) { throw 'Close the game before installation.' }
        $backup = Join-Path $out ('backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
        New-Item -ItemType Directory -Path $backup | Out-Null
        Copy-Item -LiteralPath "$v2\release\MUSTANGGT\GEOMETRY.BIN" -Destination "$backup\release-GEOMETRY.BIN"
        Copy-Item -LiteralPath "$v2\release\MUSTANGGT\TEXTURES.BIN" -Destination "$backup\release-TEXTURES.BIN"
        Copy-Item -LiteralPath "$out\GEOMETRY.BIN" -Destination "$v2\release\MUSTANGGT\GEOMETRY.BIN" -Force
        Copy-Item -LiteralPath "$out\tpk\TEXTURES.BIN" -Destination "$v2\release\MUSTANGGT\TEXTURES.BIN" -Force
        $expected = (Get-FileHash -LiteralPath "$out\GEOMETRY.BIN").Hash
        # A later installation introduced Mod Loader. Keep both entry paths
        # current so launching the -mod shortcut cannot load a stale V1 car.
        foreach ($relative in @('CARS\MUSTANGGT','ADDONS\CARS_REPLACE\MUSTANGGT')) {
            $game = Join-Path $gameRoot $relative
            if (!(Test-Path -LiteralPath $game)) { continue }
            $label = $relative.Replace('\','-')
            foreach ($name in @('GEOMETRY.BIN','TEXTURES.BIN')) {
                Copy-Item -LiteralPath "$game\$name" -Destination "$backup\$label-$name"
                Copy-Item -LiteralPath "$v2\release\MUSTANGGT\$name" -Destination "$game\$name" -Force
                if ((Get-FileHash -LiteralPath "$game\$name").Hash -ne (Get-FileHash -LiteralPath "$v2\release\MUSTANGGT\$name").Hash) { throw "Installed hash differs: $relative/$name" }
            }
        }
        Write-Output "Installed Fusion lenses (RearOnly=$RearOnly): $expected"
    }
} finally { Pop-Location }
