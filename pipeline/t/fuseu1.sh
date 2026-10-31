# fuseu1.sh — Upanishad 1: assemble transcripts, fuse with the backbone, prepare judge files
set -e
cd ${SD_WORK:-.}
Y=${SD_REPO:-$HOME/sudhar-desk}/sync/sBXs4P2SE2U.tsv
# pieces Gemini refused whole: use the split transcription
for g2 in audio/u1/*_p[0-9][0-9].gem2.txt; do
  [ -e "$g2" ] || continue
  g=${g2%.gem2.txt}.gem.txt
  if [ ! -s "$g" ] || [ $(stat -c %s "$g") -lt 300 ]; then cp "$g2" "$g"; echo "used split Gemini for $g"; fi
done
for f in audio/u1/*_p[0-9][0-9].gem.txt audio/u1/*_p[0-9][0-9].sar.txt; do
  if [ $(stat -c %s "$f") -lt 300 ]; then echo "EMPTY $f"; fi
done
bash t/assemble2.sh audio/u1 vu1 u1z u1a u1b u1c u1d u1e
python3 t/fuse2.py vu1/doc.txt vu1/items.json S=vu1/sar.txt G=vu1/gem.txt Y=$Y
python3 t/prepjudge.py vu1/items.json vu1/j 150
python3 t/cands2.py vu1/doc.txt vu1/cands.json S=vu1/sar.txt G=vu1/gem.txt Y=$Y
python3 t/candlines.py vu1/cands.json vu1/cands.txt
wc -l vu1/j_*.txt vu1/cands.txt
