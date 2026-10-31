// node gaps.js text.txt yt.tsv out.tsv [maxChar]  -> per word boundary: i, gap_ms, wordLen, sep(label), word, nextword
const A=require((process.env.SD_REPO||require('os').homedir()+'/sudhar-desk')+'/align.js'),fs=require('fs');
const [,,tf,cf,of,mx]=process.argv; const t=fs.readFileSync(tf,'utf8'); const R=A.align(t,A.parseTsv(fs.readFileSync(cf,'utf8')));
const W=R.words, lim=mx?+mx:t.length; const out=[];
for(let i=0;i+1<W.length;i++){ const a=W[i],b=W[i+1]; if(b.s>lim)break;
  const sep=t.slice(a.e,b.s); const lab=/[.?!।]/.test(sep)?'DOT':(/,/.test(sep)?'COMMA':(/\n/.test(sep)?'PARA':'NONE'));
  out.push([i,a.m&&b.m?b.t-a.t:'',a.e-a.s,lab,t.slice(a.s,a.e),t.slice(b.s,b.e),a.s].join('\t')); }
fs.writeFileSync(of,out.join('\n')); console.log('boundaries',out.length,'matched words',R.matched,'/',R.total);
