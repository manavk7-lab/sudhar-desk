# assemble.sh VID key1 key2 ...  -> vVID/sar.txt vVID/gem.txt (overlaps merged)
set -e
cd ${SD_WORK:-.}
V=$1; shift
for e in gem sar; do
  files=""
  for k in "$@"; do
    ls audio/b/${k}_p*.${e}.txt >/dev/null
    cat $(ls audio/b/${k}_p[0-9][0-9].${e}.txt | sort) | tr '\n' ' ' > v$V/${k}.${e}.txt
    files="$files v$V/${k}.${e}.txt"
  done
  python3 t/mergeov.py v$V/${e}.txt $files
done
