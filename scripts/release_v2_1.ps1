$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$buildRoot = Join-Path $projectRoot 'work\zipbuild\v2.1'
$backupRoot = Join-Path $projectRoot 'work\zipbuild\backup-before-v2.1'
$approved = Join-Path $projectRoot 'work\c2012-stage\pacote-27-09e-placa-arredondada'
$releaseRoot = Join-Path $projectRoot 'release'
New-Item -ItemType Directory -Force -Path $buildRoot,$backupRoot | Out-Null

$cars = @(
    @{ Name='Fusion2012_FWD_MW2005'; Slot='COBALTSS'; Source='z12'; Approved='2012' },
    @{ Name='Fusion2018_AWD_MW2005'; Slot='MUSTANGGT'; Source='z18'; Approved='2018' }
)

foreach ($car in $cars) {
    $package = Join-Path $buildRoot $car.Name
    if (Test-Path -LiteralPath $package) {
        throw "Package staging folder already exists: $package"
    }
    Copy-Item -LiteralPath (Join-Path $projectRoot ('work\zipbuild\' + $car.Source)) -Destination $package -Recurse
    foreach ($name in @('GEOMETRY.BIN','TEXTURES.BIN')) {
        $source = Join-Path $approved ($car.Approved + '\' + $name)
        if (-not (Test-Path -LiteralPath $source)) { throw "Approved file missing: $source" }
        foreach ($route in @('CARS','ADDONS\CARS_REPLACE')) {
            $target = Join-Path $package ($route + '\' + $car.Slot + '\' + $name)
            Copy-Item -LiteralPath $source -Destination $target -Force
            if ((Get-FileHash -LiteralPath $source).Hash -ne (Get-FileHash -LiteralPath $target).Hash) {
                throw "Hash mismatch: $target"
            }
        }
    }
    Copy-Item -LiteralPath (Join-Path $releaseRoot 'instalar.bat') -Destination (Join-Path $package 'instalar.bat') -Force
    Copy-Item -LiteralPath (Join-Path $releaseRoot 'NOTAS-v2.1.md') -Destination (Join-Path $package 'NOTAS-v2.1.md') -Force
    $manifest = Get-ChildItem -LiteralPath $package -Recurse -File |
        Where-Object Name -ne 'SHA256SUMS.txt' |
        Sort-Object FullName |
        ForEach-Object {
            $relative = $_.FullName.Substring($package.Length + 1).Replace('\','/')
            ((Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant() + '  ./' + $relative)
        }
    [IO.File]::WriteAllLines((Join-Path $package 'SHA256SUMS.txt'), [string[]]$manifest,
        [Text.UTF8Encoding]::new($false))
    $candidate = Join-Path $buildRoot ($car.Name + '.zip')
    [IO.Compression.ZipFile]::CreateFromDirectory($package, $candidate,
        [IO.Compression.CompressionLevel]::Optimal, $true)
    $zip = [IO.Compression.ZipFile]::OpenRead($candidate)
    try {
        $prefix = $car.Name + '/'
        $files = Get-ChildItem -LiteralPath $package -Recurse -File
        if ($zip.Entries.Count -ne $files.Count) { throw "ZIP entry count mismatch: $candidate" }
        foreach ($file in $files) {
            $entryName = $prefix + $file.FullName.Substring($package.Length + 1).Replace('\','/')
            $entry = $zip.GetEntry($entryName)
            if ($null -eq $entry -or $entry.Length -ne $file.Length) {
                throw "ZIP entry missing or wrong length: $entryName"
            }
        }
    } finally { $zip.Dispose() }
    $published = Join-Path $releaseRoot ($car.Name + '.zip')
    if (Test-Path -LiteralPath $published) {
        Copy-Item -LiteralPath $published -Destination (Join-Path $backupRoot ($car.Name + '.zip')) -Force
    }
    Copy-Item -LiteralPath $candidate -Destination $published -Force
    if ((Get-FileHash -LiteralPath $candidate).Hash -ne (Get-FileHash -LiteralPath $published).Hash) {
        throw "Published ZIP differs from validated candidate: $published"
    }
    Write-Output ((Get-FileHash -LiteralPath $published).Hash + '  ' + $published)
}

$contentSums = foreach ($car in $cars) {
    '# ' + $car.Name + '.zip'
    Get-Content -LiteralPath (Join-Path $buildRoot ($car.Name + '\SHA256SUMS.txt'))
    ''
}
[IO.File]::WriteAllLines((Join-Path $releaseRoot 'SHA256SUMS-conteudo.txt'),
    [string[]]$contentSums,[Text.UTF8Encoding]::new($false))
