// fwddoc.js — read a Doc into the work folder without the cache key ever being in Claude's context (6 Nov).
// Path: Sudhar Desk tab → BroadcastChannel 'sd-fwd' → relay tab → its opener (a YouTube tab) → __sdput → relay → cache.
// Then in the work folder: python3 bin/getdoc.py KEY VM/doc_orig.txt   (same format as docget.js: base64 UTF-8 parts + 'n')
// Three small injections, none with a key:

// 1) In the YouTube tab whose relay you use (relay_yt.js / recorder_fn.js already there):
if(!window.__fwdOn){window.__fwdOn=1;window.addEventListener('message',async ev=>{if(ev.origin!=='https://manavk7-lab.github.io')return;
 const m=ev.data;if(!m||m.__fwd!==1)return;let ok=false;try{ok=!!(await window.__sdput(m.key,m.part,m.data))}catch(e){}
 try{ev.source.postMessage({__fwdack:m.id,ok},ev.origin)}catch(e){}})}

// 2) In that YouTube tab's relay tab (manavk7-lab.github.io/sudhar-desk/version.txt; its window.opener is the YouTube tab):
if(!window.__bcOn){window.__bcOn=1;const bc=new BroadcastChannel('sd-fwd');bc.onmessage=ev=>{const m=ev.data;if(!m||m.__fwd!==1)return;
 window.opener.postMessage(m,'https://www.youtube.com')};window.addEventListener('message',ev=>{if(ev.origin!=='https://www.youtube.com')return;
 const m=ev.data;if(m&&m.__fwdack!=null)bc.postMessage(m)})}

// 3) In the Sudhar Desk tab (again after every app reload): await __fwdDoc(KEY, DOC) → {st:'done', len, sha, parts}
window.__fwdDoc=async(KEY,docId)=>{const J={st:'run'};const sleep=ms=>new Promise(s=>setTimeout(s,ms));try{
 const bc=new BroadcastChannel('sd-fwd');const waits={};bc.onmessage=ev=>{const m=ev.data;if(m&&m.__fwdack!=null&&waits[m.__fwdack])waits[m.__fwdack](m.ok)};
 const send=(part,data)=>new Promise(res=>{const id=KEY+':'+part+':'+Math.random();const to=setTimeout(()=>{delete waits[id];res(false)},60000);waits[id]=ok=>{clearTimeout(to);delete waits[id];res(ok)};bc.postMessage({__fwd:1,id,key:KEY,part:String(part),data})});
 let x=null;for(let a=0;a<5&&!x;a++){try{x=await gasGetText(docId)}catch(e){J.err=String(e);await sleep(4000)}}
 const t=x.text;J.len=t.length;const h=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(t));J.sha=[...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16);
 const bytes=new TextEncoder().encode(t);let bin='';for(let i=0;i<bytes.length;i+=32768)bin+=String.fromCharCode.apply(null,bytes.subarray(i,i+32768));
 const b64=btoa(bin);const P=[];for(let i=0;i<b64.length;i+=90000)P.push(b64.slice(i,i+90000));
 for(let i=0;i<P.length;i++){let ok=false;for(let a=0;a<3&&!ok;a++)ok=await send(i,P[i]);if(!ok)throw new Error('part '+i)}
 if(!await send('n',String(P.length)))throw new Error('n');J.parts=P.length;J.st='done';bc.close();
}catch(e){J.st='err';J.err=String(e)}return J};
