#!/bin/bash
# postbc.sh N YT — post bcN/new.txt over the Doc (hash = bcN/final.txt, the Doc as read) and rewrite review/YT.json.
set -e -o pipefail; N=$1; YT=$2; TAG=${3:-claude-$(date +%F)}; R=${SD_REPO:-/home/claude/sudhar-desk}
DOC=$(awk -F'\t' -v n="UPNISHAD -video $N.corrected" '$1==n{print $2}' docs.tsv)
PAR=$(awk -F'\t' -v n="UPNISHAD -video $N.corrected" '$1==n{print $3}' docs.tsv)
[ "$PAR" = "13GCS6Z1zUmUKI7noi8MA43aYLblzqB4O" ] && { echo "TOTAL FINAL — not posting"; exit 1; }
H=$(python3 -c "import hashlib;print(hashlib.sha256(open('bc$N/final.txt',encoding='utf-8').read().encode()).hexdigest()[:16])")
OUT=$(python3 bin/postdoc.py $DOC $H bc$N/new.txt 2>&1 | tail -n 1); echo "$OUT"
case "$OUT" in *' OK'*) ;; *) echo 'NOT POSTED — review JSON left as it is'; exit 1;; esac
rm -f $R/review/$YT.json
python3 t/merge_review.py $R/review/$YT.json bc$N/new.txt bc$N/items.json $TAG | tail -n 1
