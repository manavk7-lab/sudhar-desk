// Post a new full text to a Doc via the app's Apps Script bridge, only if the Doc is still exactly what we based it on.
// Placeholders: __KEY__ (putcap key holding the new text), __DOC__, __OLD__ (sha16 of the Doc we started from), __NEW__ (sha16 of the new text)
window.__jobPost={st:'run'};
(async()=>{
 const J=window.__jobPost, KEY='__KEY__', CK='__CK__', docId='__DOC__', OLD='__OLD__', NEW='__NEW__';
 const sleep=ms=>new Promise(s=>setTimeout(s,ms));
 const sha=async t=>{const h=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(t));return [...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16)};
 const get=async part=>{for(let a=0;a<6;a++){try{const u=gas.url+'?'+new URLSearchParams({action:'getcap',ck:CK,key:KEY,part:String(part)});const x=await fetch(u,{redirect:'follow'}).then(r=>r.json());if(x&&x.data!=null)return x.data}catch(e){J.err=String(e)}await sleep(3000*(a+1))}return null};
 const getText=async()=>{for(let a=0;a<5;a++){try{const x=await gasGetText(docId);if(x&&typeof x.text==='string')return x.text}catch(e){J.err=String(e)}await sleep(4000)}return null};
 try{
  const n=parseInt(await get('n')); if(!n) throw new Error('no parts');
  let b64=''; for(let i=0;i<n;i++){const d=await get(i); if(d==null) throw new Error('part '+i); b64+=d}
  const bin=atob(b64); const bytes=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) bytes[i]=bin.charCodeAt(i);
  const text=new TextDecoder().decode(bytes); J.newLen=text.length; J.newSha=await sha(text);
  if(J.newSha!==NEW) throw new Error('new text sha mismatch '+J.newSha);
  const cur=await getText(); if(cur==null) throw new Error('could not read Doc');
  J.curSha=await sha(cur);
  if(J.curSha!==OLD){J.st='changed';return}
  let r=null; for(let a=0;a<3&&!r;a++){try{r=await gasPost({docId,fullText:text,dev:'claude',name:'Claude'})}catch(e){J.err=String(e);await sleep(5000)}}
  J.post=JSON.stringify(r).slice(0,200);
  await sleep(2000);
  const after=await getText(); J.afterSha=after==null?null:await sha(after);
  J.st=(J.afterSha===NEW)?'done':'verify-mismatch';
 }catch(e){J.st='err';J.err=String(e)}
})();
'started'
