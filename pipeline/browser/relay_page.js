// relay_page.js — run in the manavk7-lab.github.io tab that relay_yt.js opened. Fill __CK__ (python3 t/mkjs.py).
// Reads the Apps Script URL from Sudhar Desk's own saved settings (localStorage 'desk-gas'), so nobody types it.
(()=>{
 if(window.__relay)return 'already';
 const CK='__CK__'; const G=JSON.parse(localStorage.getItem('desk-gas')||'{}');
 window.__relay={n:0,fail:0,last:null,hasUrl:!!G.url}; document.title='relay';
 window.addEventListener('message',async ev=>{
  if(ev.origin!=='https://www.youtube.com')return; const m=ev.data; if(!m||typeof m!=='object'||m.__sd!==1||m.ack)return;
  let ok=false;
  for(let a=0;a<6&&!ok;a++){try{const r=await fetch(G.url,{method:'POST',redirect:'follow',headers:{'Content-Type':'text/plain;charset=utf-8'},
    body:JSON.stringify({action:'putcap',ck:CK,key:m.key,part:m.part,data:m.data})}).then(r=>r.json());ok=!!(r&&r.ok)}
   catch(e){await new Promise(s=>setTimeout(s,3000*(a+1)))}}
  window.__relay.n++; if(!ok)window.__relay.fail++; window.__relay.last=m.key+':'+m.part;
  try{ev.source.postMessage({__sd:1,ack:m.id,ok},ev.origin)}catch(e){window.__relay.ackErr=String(e)}
 });
 return JSON.stringify({opener:!!window.opener,hasUrl:window.__relay.hasUrl});
})()
