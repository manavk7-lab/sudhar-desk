// node timepos.js text.txt yt.tsv sec1 sec2 ... -> char positions of the first word at/after each time
const A=require((process.env.SD_REPO||require('os').homedir()+'/sudhar-desk')+'/align.js'),fs=require('fs');
const [,,tf,cf,...secs]=process.argv;
const t=fs.readFileSync(tf,'utf8'); const R=A.align(t,A.parseTsv(fs.readFileSync(cf,'utf8')));
const out=secs.map(s=>{const ms=+s*1000; const w=R.words.find(w=>w.t>=ms); return w?w.s:t.length});
console.log(JSON.stringify({pos:out,total:t.length,matched:R.matched,words:R.total}));
