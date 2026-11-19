# punctsteps.sh vN YT — apply the punctuation agents' output, carry items, merge, check (PROCESS steps 9)
V=$1; Y=$2
python3 t/applypunct.py $V/new_a.txt $V/pc.json $V/final.txt $V/rev_punct.json $V/pc_*_out.json | tail -1
python3 t/fixitems.py $V/new_a.txt $V/final.txt $V/items_f.json $V/items_all_final.json | tail -1
python3 t/addrp.py $V $Y | tail -1
python3 t/mergealign.py $V/final.txt $V/items_all_final.json $V/doc_orig.txt | tail -1
python3 t/overlapcheck.py $V/final.txt $V/items_all_final.json | tail -2
python3 t/revertcheck.py $V/final.txt $V/items_all_final.json $V/doc_orig.txt | tail -3
