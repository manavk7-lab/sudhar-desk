// node wordtimes.js text.txt yt.tsv out.json -> [[s,e,t,m],...]
const A=require((process.env.SD_REPO||require('os').homedir()+'/sudhar-desk')+'/align.js'),fs=require('fs');
const [,,tf,cf,of]=process.argv; const t=fs.readFileSync(tf,'utf8'); const R=A.align(t,A.parseTsv(fs.readFileSync(cf,'utf8')));
fs.writeFileSync(of,JSON.stringify(R.words.map(w=>[w.s,w.e,Math.round(w.t),w.m?1:0])));
console.log('words',R.words.length,'matched',R.matched);
