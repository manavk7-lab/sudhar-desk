// docget.js — run in the Sudhar Desk tab: reads a Doc exactly as the Apps Script sees it (the text the hash-checked
// post compares with), keeps its sha16, and puts the text into the cache so bin/getdoc.py KEY out.txt can fetch it.
// Placeholders: __KEY__ (cache key), __DOC__ (Doc id); __CK__ is filled by t/mkjs.py. Poll window.__jobGet.
window.__jobGet={st:'run'};
(async()=>{
 const J=window.__jobGet, KEY='__KEY__', CK='__CK__', docId='__DOC__';
 const sleep=ms=>new Promise(s=>setTimeout(s,ms));
 const sha=async t=>{const h=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(t));return [...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16)};
 const put=async(part,data)=>{for(let a=0;a<5;a++){try{const r=await fetch(gas.url,{method:'POST',redirect:'follow',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({action:'putcap',ck:CK,key:KEY,part:String(part),data})}).then(r=>r.json());if(r&&r.ok)return true}catch(e){J.err=String(e)}await sleep(3000*(a+1))}return false};
 try{
  let x=null; for(let a=0;a<5&&!x;a++){try{x=await gasGetText(docId)}catch(e){J.err=String(e);await sleep(4000)}}
  if(!x||typeof x.text!=='string') throw new Error('could not read Doc');
  const t=x.text; J.len=t.length; J.sha=await sha(t);
  const bytes=new TextEncoder().encode(t); let bin=''; for(let i=0;i<bytes.length;i+=32768) bin+=String.fromCharCode.apply(null,bytes.subarray(i,i+32768));
  const b64=btoa(bin); const P=[]; for(let i=0;i<b64.length;i+=90000) P.push(b64.slice(i,i+90000));
  for(let i=0;i<P.length;i++){if(!await put(i,P[i])) throw new Error('put part '+i)}
  if(!await put('n',String(P.length))) throw new Error('put n');
  J.parts=P.length; J.st='done';
 }catch(e){J.st='err';J.err=String(e)}
})();
'started'
