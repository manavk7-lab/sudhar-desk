# assemble2.sh AUDIODIR OUTDIR key1 key2 ...  -> OUTDIR/sar.txt OUTDIR/gem.txt (overlaps merged)
set -e
cd ${SD_WORK:-.}
A=$1; O=$2; shift 2
for e in gem sar; do
  files=""
  for k in "$@"; do
    ls $A/${k}_p*.${e}.txt >/dev/null
    cat $(ls $A/${k}_p[0-9][0-9].${e}.txt | sort) | tr '\n' ' ' > $O/${k}.${e}.txt
    files="$files $O/${k}.${e}.txt"
  done
  python3 t/mergeov.py $O/${e}.txt $files
done
