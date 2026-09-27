param(
    [Parameter(Mandatory=$true)][string]$Source,
    [Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments
)
$ErrorActionPreference = 'Stop'
$project = 'C:\Users\nillander\NoDocuments\fusion-mw2005'
$core = Join-Path $project 'tools\mwgc\RealGeometry.cs'
$output = Join-Path $project ('work\' + [IO.Path]::GetFileNameWithoutExtension($Source) + '-local.dll')
if (Test-Path -LiteralPath $output) { Remove-Item -LiteralPath $output }
Add-Type -Path @($core, $Source) -OutputAssembly $output -OutputType Library -ReferencedAssemblies @('System.Collections','System.Console','System.Runtime','System.Linq','System.Text.Json','System.Collections.NonGeneric','System.Runtime.Extensions','System.Memory') -IgnoreWarnings -CompilerOptions @('/unsafe','/define:GAME_NFSMW')
$assembly = [Reflection.Assembly]::LoadFrom($output)
$entryType = $assembly.GetTypes() | Where-Object { $_.GetMethod('Main',[Reflection.BindingFlags]'Static,Public,NonPublic') } | Select-Object -First 1
$entryMethod = $entryType.GetMethod('Main',[Reflection.BindingFlags]'Static,Public,NonPublic')
$entryMethod.Invoke($null,@(,[string[]]$Arguments)) | Out-Null
