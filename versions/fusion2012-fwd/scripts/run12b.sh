#!/bin/bash
set -e
cd /home/claude/c12
export PATH=/opt/pwsh:$PATH
S=/home/claude/v3/versions/v3-fusion-ajm3899/scripts
python3 build12.py > build/build12.log 2>&1
grep -E "!!" build/build12.log && exit 1 || true
pwsh $S/mw.ps1 cs/AddParts2.cs z10/CARS/MUSTANGGT/GEOMETRY.BIN spec12.bin build/geom_m.bin > build/addparts.log
M=build/geom_m.bin
for a in "9DB90133 1.99 -0.692 0.567" "D09091C6 1.99 0.692 0.567" "7A5B2F25 -2.13 0.67 0.72" "7ADF7EF8 -2.13 -0.67 0.72" "BF700A79 -2.245 0.49 0.714" "31A66786 -2.245 -0.49 0.714"; do set -- $a; pwsh $S/mw.ps1 cs/SetMount.cs $M $1 $2 $3 $4 build/geom_t.bin >/dev/null; mv build/geom_t.bin $M; done
pwsh $S/mw.ps1 $S/Dump.cs $M build/geom_m.dump
pwsh $S/val.ps1 $M build/geom_m_val.json
python3 rmw.py build/geom_m.dump build/prev_m.png
