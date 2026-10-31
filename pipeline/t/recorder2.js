(async()=>{
const KEY='__KEY__',START=__START__,END=__END__,U='__URL__',CK='__CK__';
if(window.__R&&!window.__R.done&&!window.__R.err)return 'already running';
const R=window.__R={key:KEY,part:0,bytes:0,chunks:0,done:false,err:null,store:{},failed:[],started:Date.now()};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const post=async(part,data)=>{for(let a=0;a<6;a++){try{const r=await fetch(U,{method:'POST',redirect:'follow',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({action:'putcap',ck:CK,key:KEY,part,data})}).then(r=>r.json());if(r&&r.ok){R.failed=R.failed.filter(x=>x!==part);return true}}catch(e){R.lastErr=String(e)}await sleep(4000*(a+1))}if(!R.failed.includes(part))R.failed.push(part);return false};
let q=Promise.resolve();
const send=blob=>{q=q.then(async()=>{const buf=new Uint8Array(await blob.arrayBuffer());R.bytes+=buf.length;let bin='';for(let i=0;i<buf.length;i+=32768)bin+=String.fromCharCode.apply(null,buf.subarray(i,i+32768));const b64=btoa(bin);const P=[];for(let i=0;i<b64.length;i+=90000)P.push(b64.slice(i,i+90000));P[P.length-1]='|'+P[P.length-1];for(const p of P){const idx=R.part++;R.store[idx]=p;await post(idx,p)}R.chunks++;}).catch(e=>{R.err=String(e)})};
R.resend=async list=>{for(const i of list)if(R.store[i]!=null)await post(i,R.store[i]);return 'resent '+list.length};
try{
const mp=document.querySelector('#movie_player');
try{mp.setPlaybackQualityRange('tiny','tiny')}catch(e){}
const v=document.querySelector('video');if(!v)throw new Error('no video');
v.muted=false;v.volume=1;
const ad=()=>mp&&mp.classList.contains('ad-showing');
const skip=()=>{const sk=document.querySelector('.ytp-skip-ad-button,.ytp-ad-skip-button-modern,.ytp-ad-skip-button');if(sk)try{sk.click()}catch(e){}};
for(let i=0;i<90&&ad();i++){skip();await sleep(1000)}
try{mp.seekTo(START,true)}catch(e){v.currentTime=START}
try{await v.play()}catch(e){R.playErr=String(e)}
for(let i=0;i<60;i++){if(Math.abs(v.currentTime-START)<4&&!v.paused&&v.readyState>=3)break;await sleep(250)}
R.t0=Math.round(v.currentTime*10)/10;
const ctx=new AudioContext();const src=ctx.createMediaElementSource(v);const dst=ctx.createMediaStreamDestination();src.connect(dst);
try{await ctx.resume()}catch(e){}
const rec=new MediaRecorder(dst.stream,{mimeType:'audio/webm;codecs=opus',audioBitsPerSecond:24000});
R.rec=rec;R.ctx=ctx;
rec.ondataavailable=e=>{if(e.data&&e.data.size)send(e.data)};
rec.onstop=()=>{q=q.then(async()=>{await post('n',String(R.part));R.done=true;try{v.pause()}catch(e){}})};
rec.start(60000);
const stop=()=>{if(rec.state==='recording')rec.stop()};
const tick=()=>{if(R.done||rec.state!=='recording')return;skip();if(!ad()){if(v.currentTime>=END)stop();else if(v.ended)stop();else if(v.paused)v.play().catch(()=>{})}R.t=Math.round(v.currentTime);R.ad=ad();R.ctxState=ctx.state};
v.addEventListener('timeupdate',tick);v.addEventListener('ended',()=>{if(!ad())stop()});R.iv=setInterval(tick,4000);
}catch(e){R.err=String(e)}
return 'started '+KEY;
})()
