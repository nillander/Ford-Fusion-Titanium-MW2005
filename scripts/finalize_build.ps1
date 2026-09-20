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
    Run 'tools\mwgc\mwgc.exe' @('-nowait','-xname','FORDGT','work\fusion.mwr','work\new-geometry.bin')
    Run 'tools\mwgc\MergeGeometry.exe' @('work\fordgt-vanilla\GEOMETRY.BIN','work\new-geometry.bin','release\FORDGT\GEOMETRY.BIN')
    Run 'tools\mwgc\RemapCompatibilityTextures.exe' @('release\FORDGT\GEOMETRY.BIN','work\remapped-geometry.bin')
    Move-Item -LiteralPath 'work\remapped-geometry.bin' -Destination 'release\FORDGT\GEOMETRY.BIN' -Force
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
