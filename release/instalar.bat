@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"

set "CANDIDATOS=%TEMP%\fusion-mw2005-pastas.txt"
set "PERGUNTADAS=%TEMP%\fusion-mw2005-perguntadas.txt"
if exist "%CANDIDATOS%" del /f /q "%CANDIDATOS%"
if exist "%PERGUNTADAS%" del /f /q "%PERGUNTADAS%"

if exist "%~dp0CARS\COBALTSS\" (
    set "MENSAGEM=O Fusion 2012 substitui o Chevrolet Cobalt SS."
) else if exist "%~dp0CARS\MUSTANGGT\" (
    set "MENSAGEM=O Fusion 2018 substitui o Ford Mustang GT."
) else (
    echo Nao encontrei CARS\COBALTSS nem CARS\MUSTANGGT nesta pasta:
    echo %~dp0
    pause
    exit /b 1
)
if not exist "%~dp0ADDONS\" (
    echo Nao encontrei a pasta ADDONS ao lado deste script.
    pause
    exit /b 1
)

echo Procurando Need for Speed: Most Wanted 2005...
echo.

call :DoRegistro "HKLM\SOFTWARE\WOW6432Node\EA GAMES\Need for Speed Most Wanted"
call :DoRegistro "HKLM\SOFTWARE\EA GAMES\Need for Speed Most Wanted"
call :DoRegistro "HKLM\SOFTWARE\WOW6432Node\Electronic Arts\Need for Speed Most Wanted"
call :DoRegistro "HKLM\SOFTWARE\Electronic Arts\Need for Speed Most Wanted"

call :Testar "C:\Program Files (x86)\EA GAMES\Need for Speed Most Wanted"
call :Testar "C:\Program Files\EA GAMES\Need for Speed Most Wanted"
call :Testar "C:\Program Files (x86)\Electronic Arts\Need for Speed Most Wanted"
call :Testar "C:\Program Files\Electronic Arts\Need for Speed Most Wanted"
call :Testar "C:\Jogos\Need for Speed Most Wanted"
call :Testar "D:\Jogos\Need for Speed Most Wanted"
call :Testar "D:\Games\Need for Speed Most Wanted"

call :Steam

if exist "%CANDIDATOS%" call :PerguntarLista
if not errorlevel 1 exit /b 0

echo Procurando speed.exe nos discos fixos. Isso pode demorar.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$seen = @{}; Get-Content -LiteralPath $env:TEMP'\fusion-mw2005-pastas.txt' -ErrorAction SilentlyContinue | ForEach-Object { $seen[$_.TrimEnd('\').ToLower()] = $true }; Get-CimInstance Win32_LogicalDisk -Filter \"DriveType=3\" | ForEach-Object { Get-ChildItem -LiteralPath ($_.DeviceID + '\') -Filter speed.exe -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object { $dir = $_.DirectoryName; $key = $dir.TrimEnd('\').ToLower(); if (-not $seen.ContainsKey($key) -and (Test-Path -LiteralPath (Join-Path $dir 'CARS'))) { $seen[$key] = $true; Add-Content -LiteralPath $env:TEMP'\fusion-mw2005-pastas.txt' -Value $dir -Encoding ascii } } }"

if not exist "%CANDIDATOS%" goto Manual
call :PerguntarLista
if not errorlevel 1 exit /b 0

:Manual
echo.
set "DIGITADA="
set /p DIGITADA=Digite a pasta do jogo, ou Enter para cancelar: 
if not defined DIGITADA exit /b 1
call :Confirmar "%DIGITADA%"
if errorlevel 1 (
    echo Instalacao cancelada.
    pause
    exit /b 1
)
exit /b 0

:DoRegistro
set "CHAVE=%~1"
for /f "tokens=3,*" %%A in ('reg query "%CHAVE%" /v "Install Dir" 2^>nul') do (
    if /i "%%A"=="REG_SZ" call :Testar "%%B"
)
exit /b 0

:Steam
set "STEAM="
for /f "tokens=2,*" %%A in ('reg query "HKCU\Software\Valve\Steam" /v SteamPath 2^>nul') do (
    if /i "%%A"=="REG_SZ" set "STEAM=%%B"
)
if not defined STEAM exit /b 0
set "STEAM=!STEAM:/=\!"
call :Testar "!STEAM!\steamapps\common\Need for Speed Most Wanted"
if not exist "!STEAM!\steamapps\libraryfolders.vdf" exit /b 0
for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "$p='%STEAM%\steamapps\libraryfolders.vdf'; if (Test-Path -LiteralPath $p) { Select-String -LiteralPath $p -Pattern '\"path\"\s+\"([^\"]+)\"' -AllMatches | ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value.Replace('\\\\','\') } }"`) do (
    call :Testar "%%P\steamapps\common\Need for Speed Most Wanted"
)
exit /b 0

:Testar
set "PASTA=%~1"
if not defined PASTA exit /b 0
if "!PASTA:~-1!"=="\" set "PASTA=!PASTA:~0,-1!"
if not exist "!PASTA!\speed.exe" if not exist "!PASTA!\SPEED.EXE" exit /b 0
if not exist "!PASTA!\CARS" exit /b 0
if not exist "%CANDIDATOS%" (
    >>"%CANDIDATOS%" echo !PASTA!
    exit /b 0
)
findstr /L /I /X /C:"!PASTA!" "%CANDIDATOS%" >nul
if errorlevel 1 >>"%CANDIDATOS%" echo !PASTA!
exit /b 0

:PerguntarLista
for /f "usebackq delims=" %%G in ("%CANDIDATOS%") do (
    findstr /L /I /X /C:"%%G" "%PERGUNTADAS%" >nul 2>&1
    if errorlevel 1 (
        call :Confirmar "%%G"
        if not errorlevel 1 exit /b 0
    )
)
exit /b 1

:Confirmar
set "JOGO=%~1"
if not exist "!JOGO!\speed.exe" if not exist "!JOGO!\SPEED.EXE" (
    echo.
    echo Essa pasta nao tem speed.exe:
    echo !JOGO!
    exit /b 1
)
>>"%PERGUNTADAS%" echo !JOGO!
echo.
echo Pasta encontrada:
echo !JOGO!
set "RESP="
set /p RESP=Esta pasta esta correta? (S/N) 
if /i "!RESP!"=="S" goto Instalar
if /i "!RESP!"=="SIM" goto Instalar
exit /b 1

:Instalar
echo.
echo Feche o jogo se ele estiver aberto.
echo Copiando CARS e ADDONS para:
echo !JOGO!
robocopy "%~dp0CARS" "!JOGO!\CARS" /E /R:1 /W:1
if errorlevel 8 goto Falhou
robocopy "%~dp0ADDONS" "!JOGO!\ADDONS" /E /R:1 /W:1
if errorlevel 8 goto Falhou
echo.
echo Instalacao concluida. Abra o jogo pelo Mod Loader.
echo !MENSAGEM!
pause
exit /b 0

:Falhou
echo.
echo A copia falhou. Feche o jogo e execute o script de novo.
pause
exit /b 1
