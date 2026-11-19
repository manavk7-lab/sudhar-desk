# midsteps.sh vN YT — manual rows, mantras, આગળે, items, times, folds, checks (PROCESS steps 6–7)
set -e
V=$1; Y=$2
python3 t/manualgen.py $V/new.txt $V/manual_spec.json $V/manual.json
python3 t/mantra_apply.py $V/new.txt $V/manual.json $V/new_o.txt $V/rev_manual.json | tail -1
python3 t/mantra_apply.py $V/new_o.txt $V/mantra_draft.json $V/new_m.txt $V/rev_mantra.json | tail -1
cp v59/agale_spec.json $V/
python3 t/manualgen.py $V/new_m.txt $V/agale_spec.json $V/agale.json
python3 t/mantra_apply.py $V/new_m.txt $V/agale.json $V/new_a.txt $V/rev_agale.json | tail -1
python3 t/collect_items.py $V | tail -1
python3 t/addtimes.py $V/new_a.txt $SD_REPO/sync/$Y.tsv $V/items_pre.json | tail -1
python3 t/autofold.py $V $V/new_a.txt $V/items_pre.json $V/fold_groups.json | grep -i "lost" || true
python3 t/foldfix.py $V $V/new_a.txt $V/items_pre.json $V/fold_groups.json $V/items_f.json | tail -1
python3 t/overlapcheck.py $V/new_a.txt $V/items_f.json | tail -4
python3 t/revertcheck.py $V/new_a.txt $V/items_f.json $V/doc_orig.txt | tail -3
