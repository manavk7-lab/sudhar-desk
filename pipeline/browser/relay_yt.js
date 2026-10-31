// relay_yt.js — run in a YouTube watch tab. Adds a yellow button; a real click on it opens a small page on
// manavk7-lab.github.io (same site as Sudhar Desk, so it can read the Apps Script settings Manav saved there).
// YouTube's opener policy lets a page it opens talk back to it. window.__sdput(key, part, data) then hands data
// to that page, which stores it in the Apps Script cache (putcap) and answers ok / not ok.
(()=>{
 const SD='https://manavk7-lab.github.io';
 let b=document.getElementById('__relaybtn');
 if(!b){b=document.createElement('button');b.id='__relaybtn';b.textContent='open relay';
  b.style.cssText='position:fixed;left:8px;bottom:8px;z-index:999999;padding:14px 22px;font-size:18px;background:#fc0';
  document.body.appendChild(b);
  b.onclick=()=>{window.__rw=window.open(SD+'/sudhar-desk/version.txt','sdrelay_'+Math.random().toString(36).slice(2,6))}}
 if(!window.__pend){window.__pend={};window.addEventListener('message',ev=>{if(ev.origin===SD&&ev.data&&ev.data.__sd===1&&ev.data.ack){const f=window.__pend[ev.data.ack];if(f){f(ev.data.ok);delete window.__pend[ev.data.ack]}}})}
 window.__sdput=(key,part,data)=>new Promise(res=>{const id=Math.random().toString(36).slice(2);window.__pend[id]=res;
  window.__rw.postMessage({__sd:1,id,key,part,data},SD);setTimeout(()=>{if(window.__pend[id]){delete window.__pend[id];res(false)}},120000)});
 return 'button added';
})()
