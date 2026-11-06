// posttext.js — run in the Sudhar Desk tab (needs no key: it uses the app's own gasGetText/gasPost and its saved
// settings). Defines:
//   __putChunk(key, i, text, sha16)  — keep one piece of the new text; refused unless its sha16 matches
//   __postText(key, n, docId, OLD, NEW) — join pieces 0..n-1, check the whole text's sha16 = NEW, read the Doc and stop
//                                        if it is no longer OLD (st 'changed'), write it, read it back, check = NEW.
// Pieces come from `python3 t/chunks.py VM/final.txt 3000` (line ranges + sha16 per piece); pass each piece as a JS
// template literal. The app reloads itself after a push that bumps APP_VERSION — define these again then.
(()=>{
const sleep=ms=>new Promise(s=>setTimeout(s,ms));
const sha=async t=>{const h=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(t));return [...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16)};
const getText=async(docId,J)=>{for(let a=0;a<5;a++){try{const x=await gasGetText(docId);if(x&&typeof x.text==='string')return x.text}catch(e){J.err=String(e)}await sleep(4000)}return null};
window.__TC={};
window.__putChunk=async(key,i,s,h)=>{const g=await sha(s);if(g!==h)return 'MISMATCH '+i+' '+g;(window.__TC[key]=window.__TC[key]||{})[i]=s;return 'ok '+i};
window.__postText=async(key,n,docId,OLD,NEW)=>{const J={st:'run'};try{
 const C=window.__TC[key]||{};let text='';for(let i=0;i<n;i++){if(C[i]==null)throw new Error('missing chunk '+i);text+=C[i]}
 J.newLen=text.length;J.newSha=await sha(text);if(J.newSha!==NEW)throw new Error('new text sha mismatch '+J.newSha);
 const cur=await getText(docId,J);if(cur==null)throw new Error('could not read Doc');J.curSha=await sha(cur);
 if(J.curSha!==OLD){J.st='changed';return J}
 let r=null;for(let a=0;a<3&&!r;a++){try{r=await gasPost({docId,fullText:text,dev:'claude',name:'Claude'})}catch(e){J.err=String(e);await sleep(5000)}}
 J.post=JSON.stringify(r).slice(0,200);await sleep(2000);
 const after=await getText(docId,J);J.afterSha=after==null?null:await sha(after);J.st=(J.afterSha===NEW)?'done':'verify-mismatch';
}catch(e){J.st='err';J.err=String(e)}return J};
return 'defined '+typeof gasGetText+' '+typeof gasPost;
})()
