$PSStyle.OutputRendering='PlainText'; $ErrorActionPreference='Stop'
$dll='/home/claude/v3/cs/bin/mwtc.dll'
if(!(Test-Path $dll)){ Add-Type -Path (Get-ChildItem /home/claude/v3/mwtc/*.cs).FullName -OutputAssembly $dll -OutputType Library -ReferencedAssemblies System.Collections,System.Console,System.Runtime,System.Collections.NonGeneric,System.Runtime.InteropServices -IgnoreWarnings }
$asm=[Reflection.Assembly]::LoadFrom($dll)
$t=$asm.GetTypes() | ? { $_.GetMethod('Main',[Reflection.BindingFlags]'Static,Public,NonPublic') } | select -First 1
[string[]]$a=$args
$r=$t.GetMethod('Main',[Reflection.BindingFlags]'Static,Public,NonPublic').Invoke($null,@(,$a)); "exit=$r"
