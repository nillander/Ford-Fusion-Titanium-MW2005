#!/bin/bash
# Recria o ambiente de build numa nuvem Linux nova (container efêmero).
# Pré-requisito: staged para /mnt/user-data/uploads os arquivos listados em CONTINUACAO-FUSION2012.md (seção "Entradas").
set -e
# 1. PowerShell 7 (traz .NET 8 + Roslyn para Add-Type): apt e dot.net são bloqueados, GitHub não
mkdir -p /opt/pwsh && cd /opt/pwsh && curl -sSL -o p.tgz https://github.com/PowerShell/PowerShell/releases/download/v7.4.6/powershell-7.4.6-linux-x64.tar.gz && tar xzf p.tgz && chmod +x pwsh
# 2. árvore de ferramentas/scripts antigos do projeto em /home/claude/v3
mkdir -p /home/claude/v3 /home/claude/c12 && cd /home/claude/v3 && tar xzf /mnt/user-data/uploads/fusion-mw2005/work/c2012-stage/scripts.tgz
S=/home/claude/v3/versions/v3-fusion-ajm3899/scripts
sed -i 's#/home/claude/v3/cs/bin#/home/claude/c12/cs/bin#' $S/mw.ps1
sed -i 's#/mnt/user-data/uploads/fusion-mw2005/scripts/validator#/home/claude/v3/scripts/validator#' $S/val.ps1
sed -i 's#/home/claude/v3/cs/bin/mwtc.dll#/home/claude/c12/cs/bin/mwtc.dll#; s#Get-ChildItem /home/claude/v3/mwtc/\*.cs#Get-ChildItem /home/claude/c12/mwtc/*.cs#' $S/mwtc.ps1
# 3. mwtc sem System.Drawing
mkdir -p /home/claude/c12/mwtc && cd /home/claude/c12/mwtc && cp /home/claude/v3/tools/mwtc/{AssemblyInfo,Compiler,ConfigFile,DDS,TpkCore}.cs . 
sed -i 's/^using System.Drawing;//; s/^using System.Windows.Forms;//; s/^using System.Drawing.Imaging;//' *.cs
python3 - <<'PY'
s=open('DDS.cs').read(); i=s.index('\t\tpublic Image Decode()'); j=s.index('{',i); d=0; k=j
while True:
    d+= s[k]=='{'; d-= s[k]=='}'
    if s[k]=='}' and d==0: break
    k+=1
open('DDS.cs','w').write(s[:i]+s[k+1:])
PY
echo "ambiente pronto; copie versions/fusion2012-fwd/scripts para /home/claude/c12 (ver CONTINUACAO)"
