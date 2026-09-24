# usage: pwsh mw.ps1 Script.cs args...
$PSStyle.OutputRendering='PlainText'
$ErrorActionPreference='Stop'
$script=$args[0]; $rest=@($args | Select-Object -Skip 1)
$name=[IO.Path]::GetFileNameWithoutExtension($script)
$dll="/home/claude/v3/cs/bin/$name.dll"
New-Item -ItemType Directory -Force /home/claude/v3/cs/bin | Out-Null
$srcs=@('/home/claude/v3/tools/mwgc/RealGeometry.cs',$script)
$code=($srcs | ForEach-Object { Get-Content -Raw $_ }) -join "`n"
# hoist usings: simple approach—compile files separately joined is problematic; use -Path
if(!(Test-Path $dll) -or (Get-Item $script).LastWriteTime -gt (Get-Item $dll).LastWriteTime){ if(Test-Path $dll){Remove-Item $dll}; Add-Type -Path $srcs -OutputAssembly $dll -OutputType Library -ReferencedAssemblies System.Collections,System.Console,System.Runtime,System.Linq,System.Text.Json,System.Collections.NonGeneric,System.Runtime.Extensions,System.Memory -IgnoreWarnings -CompilerOptions '/unsafe','/define:GAME_NFSMW' }
$asm=[Reflection.Assembly]::LoadFrom($dll)
$t=$asm.GetTypes() | Where-Object { $_.GetMethod('Main',[Reflection.BindingFlags]'Static,Public,NonPublic') } | Select-Object -First 1
$m=$t.GetMethod('Main',[Reflection.BindingFlags]'Static,Public,NonPublic')
[string[]]$a=$rest
$m.Invoke($null,@(,$a)) | Out-Null
