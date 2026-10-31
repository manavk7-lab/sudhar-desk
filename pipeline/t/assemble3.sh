# assemble3.sh AUDIODIR OUTDIR key1 key2 ... -> OUTDIR/sar.txt and, if every piece has Gemini, OUTDIR/gem.txt (overlaps merged)
set -e
cd ${SD_WORK:-.}
A=$1; O=$2; shift 2
for e in sar gem; do
  files=""; ok=1
  for k in "$@"; do
    for p in $(ls $A/${k}_p[0-9][0-9].wav | sort); do
      f=${p%.wav}.${e}.txt
      if [ ! -s "$f" ] || [ $(stat -c %s "$f") -lt 300 ]; then ok=0; echo "missing $e: $f"; fi
    done
    [ $ok = 1 ] || break
    cat $(ls $A/${k}_p[0-9][0-9].${e}.txt | sort) | tr '\n' ' ' > $O/${k}.${e}.txt
    files="$files $O/${k}.${e}.txt"
  done
  if [ $ok = 1 ]; then python3 t/mergeov.py $O/${e}.txt $files; else echo "no complete $e"; rm -f $O/${e}.txt; fi
done
