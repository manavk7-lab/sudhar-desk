// recorder_fn.js — defines window.__startRec(KEY,START,END) (the recorder3.js body as a function) and window.__loadVid(id),
// so the same YouTube tab can record video after video with one short call each (inject once per tab, after the relay).
window.__startRec=async(KEY,START,END)=>{
if(!window.__sdput)return 'no relay: run browser/relay_yt.js first';
if(window.__R&&!window.__R.done&&!window.__R.err)return 'already running';
const R0=window.__R;  // an earlier recording in this tab: its audio graph is reused (createMediaElementSource works once per video element)
const R=window.__R={key:KEY,part:0,bytes:0,chunks:0,done:false,err:null,store:{},failed:[],started:Date.now()};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const post=async(part,data)=>{for(let a=0;a<4;a++){try{if(await window.__sdput(KEY,part,data)){R.failed=R.failed.filter(x=>x!==part);return true}}catch(e){R.lastErr=String(e)}await sleep(4000*(a+1))}if(!R.failed.includes(part))R.failed.push(part);return false};
let q=Promise.resolve();
const send=blob=>{q=q.then(async()=>{const buf=new Uint8Array(await blob.arrayBuffer());R.bytes+=buf.length;let bin='';for(let i=0;i<buf.length;i+=32768)bin+=String.fromCharCode.apply(null,buf.subarray(i,i+32768));const b64=btoa(bin);const P=[];for(let i=0;i<b64.length;i+=90000)P.push(b64.slice(i,i+90000));P[P.length-1]='|'+P[P.length-1];for(const p of P){const idx=R.part++;R.store[idx]=p;await post(idx,p)}R.chunks++;}).catch(e=>{R.err=String(e)})};
R.resend=async list=>{for(const i of list)if(R.store[i]!=null)await post(i,R.store[i]);return 'resent '+list.length};
try{
const mp=document.querySelector('#movie_player');
try{mp.setPlaybackQualityRange('tiny','tiny')}catch(e){}
const v=document.querySelector('video');if(!v)throw new Error('no video');
const unm=()=>{try{if(mp.isMuted&&mp.isMuted()){mp.unMute();R.unmuted=(R.unmuted||0)+1}}catch(e){}if(v.muted){v.muted=false;R.unmuted=(R.unmuted||0)+1}if(v.volume<1)v.volume=1};
unm();v.addEventListener('volumechange',unm);  // YouTube mutes background playback after ~30 s; that recorded silence (31 Oct)
const ad=()=>mp&&mp.classList.contains('ad-showing');
const skip=()=>{const sk=document.querySelector('.ytp-skip-ad-button,.ytp-ad-skip-button-modern,.ytp-ad-skip-button');if(sk)try{sk.click()}catch(e){}};
for(let i=0;i<90&&ad();i++){skip();await sleep(1000)}
try{mp.seekTo(START,true)}catch(e){v.currentTime=START}
try{await v.play()}catch(e){R.playErr=String(e)}
for(let i=0;i<60;i++){if(Math.abs(v.currentTime-START)<4&&!v.paused&&v.readyState>=3)break;await sleep(250)}
R.t0=Math.round(v.currentTime*10)/10;
let ctx,dst;if(window.__AUD){ctx=window.__AUD.ctx;dst=window.__AUD.dst}else if(R0&&R0.ctx&&R0.rec&&R0.rec.stream){ctx=R0.ctx;dst={stream:R0.rec.stream}}else{ctx=new AudioContext();const src=ctx.createMediaElementSource(v);dst=ctx.createMediaStreamDestination();src.connect(dst)}window.__AUD={ctx,dst};
try{await ctx.resume()}catch(e){}
const rec=new MediaRecorder(dst.stream,{mimeType:'audio/webm;codecs=opus',audioBitsPerSecond:24000});
R.rec=rec;R.ctx=ctx;
R.map=[];R.mapIv=setInterval(()=>{try{if(!R.done)R.map.push([Math.round(ctx.currentTime*10)/10,Math.round(v.currentTime*10)/10,ad()?1:0])}catch(e){}},5000);   // recording time vs video time (a video without captions needs it)
rec.ondataavailable=e=>{if(e.data&&e.data.size)send(e.data)};
rec.onstop=()=>{q=q.then(async()=>{await post('n',String(R.part));R.done=true;try{v.pause()}catch(e){}})};
rec.start(60000);
const stop=()=>{if(rec.state==='recording')rec.stop()};
const tick=()=>{if(R.done||rec.state!=='recording')return;skip();unm();if(!ad()){if(v.currentTime>=END)stop();else if(v.ended)stop();else if(v.paused)v.play().catch(()=>{})}R.t=Math.round(v.currentTime);R.ad=ad();R.ctxState=ctx.state};
v.addEventListener('timeupdate',tick);v.addEventListener('ended',()=>{if(!ad())stop()});R.iv=setInterval(tick,4000);
}catch(e){R.err=String(e)}
return 'started '+KEY;
};
window.__loadVid=async id=>{const mp=document.querySelector('#movie_player');mp.loadVideoById(id);await new Promise(s=>setTimeout(s,5000));try{mp.pauseVideo()}catch(e){}return mp.getVideoData().video_id+' '+mp.getDuration()};
window.__getCaps=async KEY=>{
 if(!window.__sdput) return 'no relay: run relay_yt.js first';
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 const mp=document.querySelector('#movie_player');
 const pr=(mp&&mp.getPlayerResponse&&mp.getPlayerResponse())||window.ytInitialPlayerResponse;
 const vid=pr&&pr.videoDetails&&pr.videoDetails.videoId;
 // 1) the player's own caption request (has every parameter YouTube wants); turn CC on once if there is none yet
 const fromPerf=()=>performance.getEntriesByType('resource').map(e=>e.name).filter(n=>n.includes('/api/timedtext')&&n.includes('v='+vid)).pop();
 let url=fromPerf();
 if(!url){const b=document.querySelector('.ytp-subtitles-button');if(b&&b.getAttribute('aria-pressed')!=='true'){b.click();await sleep(4000);url=fromPerf();b.click()}else if(b){b.click();await sleep(1500);b.click();await sleep(4000);url=fromPerf()}}
 // 2) otherwise the track list in the player response
 if(!url){const T=(((pr||{}).captions||{}).playerCaptionsTracklistRenderer||{}).captionTracks||[];
   const t=T.find(x=>x.languageCode==='gu'&&x.kind==='asr')||T.find(x=>x.languageCode==='gu')||T[0];url=t&&t.baseUrl}
 if(!url) return 'no caption track';
 const u=new URL(url,location.href);u.searchParams.set('fmt','json3');u.searchParams.delete('tlang');
 const j=await fetch(u.toString()).then(r=>r.json());
 const L=['# Sudhar Desk sync — YouTube auto-caption word times for '+vid+' (ms<TAB>word)'];
 for(const ev of (j.events||[])){if(!ev.segs)continue;for(const s of ev.segs){const w=(s.utf8||'').trim();if(!w)continue;
   const ms=(ev.tStartMs||0)+(s.tOffsetMs||0);for(const x of w.split(/\s+/))L.push(ms+'\t'+x)}}
 const text=L.join('\n')+'\n';
 const P=[];for(let i=0;i<text.length;i+=90000)P.push(text.slice(i,i+90000));
 const put=(part,data)=>window.__sdput(KEY,part,data);
 for(let i=0;i<P.length;i++) if(!await put(i,P[i])) return 'put failed at part '+i;
 await put('n',String(P.length));
 return JSON.stringify({video:vid,words:L.length-1,parts:P.length,first:L[1],last:L[L.length-1]});
};
'defined'
