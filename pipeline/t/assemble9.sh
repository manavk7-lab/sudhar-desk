set -e
cd ${SD_WORK:-.}
for e in gem sar; do
  for k in a9a a9b a9c; do cat audio/a9/${k}_p*.${e}.txt | tr '\n' ' ' > v9/${k}.${e}.txt; done
  python3 t/mergeov.py v9/${e}.txt v9/a9a.${e}.txt v9/a9b.${e}.txt v9/a9c.${e}.txt
done
