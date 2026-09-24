$PSStyle.OutputRendering='PlainText'
$asm=[Reflection.Assembly]::LoadFrom('/mnt/user-data/uploads/fusion-mw2005/scripts/validator/bin/Release/net8.0/Validator.dll')
$m=$asm.EntryPoint
[string[]]$a=$args
$m.Invoke($null,@(,$a)) | Out-Null
