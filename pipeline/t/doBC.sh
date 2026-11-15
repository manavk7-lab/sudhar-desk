#!/bin/bash
# doBC.sh N YT — apply book check, and post only if every check is clean
cd $(dirname $0)/..; export SD_REPO=${SD_REPO:-/home/claude/sudhar-desk}
out=$(python3 t/applybookcheck.py $1 $2 2>&1)
echo "$out" | grep "^rows\|SKIP" | cut -c1-150
echo "$out" | tail -n 4 | cut -c1-120
if echo "$out" | grep -q "Traceback" || echo "$out" | tail -n 4 | grep -q "diffs [1-9]\|problems [1-9]\|overlaps [1-9]\|^revertcheck.py new.txt |   "; then echo "HOLD $1"; else bash t/postbc.sh $1 $2 2>&1 | tail -n 2; fi
