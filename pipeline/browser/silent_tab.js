// silent_tab.js — run FIRST in a YouTube tab opened on a placeholder address (watch?v=xxxxxxxxxx0: no video, nothing plays).
// Every <video> the player creates is wired into a hidden audio graph before it can play, so the tab never sounds on
// the speakers (Manav, 17 Nov: "mute all audio"; 18 Nov: loadVideoById makes a NEW <video> element, which played aloud
// for a few seconds before this hook existed). Then the yellow 'open relay' button (as relay_yt.js), then recorder_fn.js,
// then __loadVid(ID) and __startRec(...). A tab still shows 'This video isn't available' — that is the placeholder page.
await new Promise(r=>setTimeout(r,2500));
if(!window.__AUD){const ctx=new AudioContext();const dst=ctx.createMediaStreamDestination();window.__AUD={ctx,dst}}
const A=window.__AUD; const hook=v=>{if(v.__g)return;try{const s=A.ctx.createMediaElementSource(v);s.connect(A.dst);v.__g=1}catch(e){window.__hookErr=String(e)}}; window.__hook=hook;
document.querySelectorAll('video').forEach(hook);
if(!window.__playHooked){const op=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){hook(this);return op.apply(this,arguments)};new MutationObserver(ms=>{for(const m of ms)for(const n of m.addedNodes){if(n.tagName==='VIDEO')hook(n);else if(n.querySelectorAll)n.querySelectorAll('video').forEach(hook)}}).observe(document.documentElement,{childList:true,subtree:true});window.__playHooked=1}
(()=>{const SD='https://manavk7-lab.github.io';let b=document.getElementById('__relaybtn');
if(!b){b=document.createElement('button');b.id='__relaybtn';b.textContent='open relay';b.style.cssText='position:fixed;left:8px;bottom:8px;z-index:999999;padding:14px 22px;font-size:18px;background:#fc0';document.body.appendChild(b);b.onclick=()=>{window.__rw=window.open(SD+'/sudhar-desk/version.txt','sdrelay_'+Math.random().toString(36).slice(2,6))}}
if(!window.__pend){window.__pend={};window.addEventListener('message',ev=>{if(ev.origin===SD&&ev.data&&ev.data.__sd===1&&ev.data.ack){const f=window.__pend[ev.data.ack];if(f){f(ev.data.ok);delete window.__pend[ev.data.ack]}}})}
window.__sdput=(key,part,data)=>new Promise(res=>{const id=Math.random().toString(36).slice(2);window.__pend[id]=res;window.__rw.postMessage({__sd:1,id,key,part,data},SD);setTimeout(()=>{if(window.__pend[id]){delete window.__pend[id];res(false)}},120000)});})();
JSON.stringify({videos:document.querySelectorAll('video').length,hooked:[...document.querySelectorAll('video')].map(v=>!!v.__g),err:window.__hookErr||null,btn:!!document.getElementById('__relaybtn')})
