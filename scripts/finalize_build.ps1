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
    Run 'tools\mwgc\mwgc.exe' @('-nowait','-xname','MUSTANGGT','work\fusion.mwr','work\new-geometry.bin')
    Run 'tools\mwgc\MergeGeometry.exe' @('donor\fusion-ajm3899\MUSTANGGT\GEOMETRY.BIN','work\new-geometry.bin','release\MUSTANGGT\GEOMETRY.BIN')
    Run 'tools\mwgc\RemapCompatibilityTextures.exe' @('release\MUSTANGGT\GEOMETRY.BIN','work\remapped-geometry.bin')
    Move-Item -LiteralPath 'work\remapped-geometry.bin' -Destination 'release\MUSTANGGT\GEOMETRY.BIN' -Force
    Run $dotnet @('scripts\validator\bin\Release\net8.0\Validator.dll','release\MUSTANGGT\GEOMETRY.BIN','reference\geometry-validation.json')
    Run $dotnet @('scripts\validator\bin\Release\net8.0\Validator.dll','release\MUSTANGGT\TEXTURES.BIN','reference\texture-independent-validation.json','work\compiled-textures')
    Run 'tools\mwgc\InspectGeometry.exe' @('release\MUSTANGGT\GEOMETRY.BIN','work\compiled-geometry.json')
    Run $py @('scripts\validate_release.py')
    if (!$SkipRender) {
        Run $blender @('--background','--threads','1','--factory-startup','--python-exit-code','1','--python','scripts\render_compiled.py')
    }
    Run $py @('scripts\package_release.py')
} finally {
    Pop-Location
}
