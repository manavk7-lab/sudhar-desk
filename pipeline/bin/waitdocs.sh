cd ${SD_WORK:-.}
for pair in doc9now:v9/now9.txt doc10:v10/doc.txt doc11:v11/doc.txt doc12:v12/doc.txt doc13:v13/doc.txt; do
  k=${pair%%:*}; f=${pair#*:}
  for i in $(seq 1 60); do python3 bin/getdoc.py $k $f 2>/dev/null && break; sleep 10; done
done
echo DOCSDONE
