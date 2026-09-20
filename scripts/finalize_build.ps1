param([switch]$SkipRender)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    function Run([string]$Program, [string[]]$Arguments) {
        & $Program @Arguments
        if ($LASTEXITCODE -ne 0) { throw "Falha ($LASTEXITCODE): $Program $Arguments" }
    }
    $py = Join-Path $projectRoot 'work\venv\Scripts\python.exe'
    $blender = Join-Path $projectRoot 'tools\blender-4.5.14-windows-x64\blender.exe'
    $dotnet = Join-Path $projectRoot 'tools\dotnet\dotnet.exe'
    Run $py @('scripts\remove_mwr_spikes.py')
    New-Item -ItemType Directory -Force -Path 'release\FORDGT' | Out-Null
    $csc = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
    Run $csc @('/nologo','/r:tools\mwgc\mwgc.exe','/out:tools\mwgc\MergeGeometry.exe','scripts\MergeGeometry.cs')
    Run $csc @('/nologo','/r:tools\mwgc\mwgc.exe','/out:tools\mwgc\RemapCompatibilityTextures.exe','scripts\RemapCompatibilityTextures.cs')
    Run 'tools\mwgc\mwgc.exe' @('-nowait','-xname','FORDGT','work\fusion.mwr','work\fordgt-from-mwr.bin')
    Run 'tools\mwgc\MergeGeometry.exe' @('donor\fordgt\ADDONS\CARS_REPLACE\FORDGT\GEOMETRY.BIN','work\fordgt-from-mwr.bin','work\fordgt-merged.bin')
    Run 'tools\mwgc\RemapCompatibilityTextures.exe' @('work\fordgt-merged.bin','release\FORDGT\GEOMETRY.BIN')
    Run $dotnet @('scripts\validator\bin\Release\net8.0\Validator.dll','release\FORDGT\GEOMETRY.BIN','reference\geometry-validation.json')
    Run $dotnet @('scripts\validator\bin\Release\net8.0\Validator.dll','release\FORDGT\TEXTURES.BIN','reference\texture-independent-validation.json','work\compiled-textures')
    Run 'tools\mwgc\InspectGeometry.exe' @('release\FORDGT\GEOMETRY.BIN','work\compiled-geometry.json')
    Run $py @('scripts\validate_release.py')
    if (!$SkipRender) {
        Run $blender @('--background','--threads','1','--factory-startup','--python-exit-code','1','--python','scripts\render_compiled.py')
    }
    Run $py @('scripts\package_release.py')
} finally {
    Pop-Location
}
