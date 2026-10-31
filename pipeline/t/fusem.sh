# fusem.sh VM AUDIODIR YTID BOOKFILES keys...  — assemble, fuse with the backbone, add the book, prepare judge + candidate files
set -e
cd ${SD_WORK:-.}
V=$1; A=$2; Y=${SD_REPO:-$HOME/sudhar-desk}/sync/$3.tsv; BK=$4; shift 4
for g2 in $A/*_p[0-9][0-9].gem2.txt; do
  [ -e "$g2" ] || continue
  g=${g2%.gem2.txt}.gem.txt
  if [ ! -s "$g" ] || [ $(stat -c %s "$g") -lt 300 ]; then cp "$g2" "$g"; echo "used split Gemini for $g"; fi
done
bash t/assemble3.sh $A $V "$@"
ENG="S=$V/sar.txt"; [ -s $V/gem.txt ] && ENG="$ENG G=$V/gem.txt"
echo "engines: $ENG"
python3 t/fuse2.py $V/doc.txt $V/items_all.json $ENG Y=$Y
python3 t/dropmantra.py $V/items_all.json $V/mantra_draft.json $V/doc.txt $V/items_nm.json
python3 t/bookref.py $V/items_nm.json $BK $V/items.json
rm -f $V/j_[0-9]*.txt
python3 t/prepjudge.py $V/items.json $V/j 150
python3 t/cands2.py $V/doc.txt $V/cands.json $ENG Y=$Y
python3 t/candlines.py $V/cands.json $V/cands.txt
wc -l $V/j_*.txt $V/cands.txt
