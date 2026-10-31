// captions.js — run in a YouTube watch tab (Manav's own Chrome). Reads the Gujarati auto-caption track of the video
// that is open, turns it into word lines "ms<TAB>word" and hands it to the cloud session through the Apps Script cache.
// Needs the relay first (relay_yt.js + relay_page.js). Fill KEY: python3 t/mkjs.py browser/captions.js KEY=cap39
// Then in the cloud: python3 bin/fetchcap.py cap39 $SD_REPO/sync/<YT>.tsv
// Returns only counts (never a URL).
(async()=>{
 const KEY='__KEY__'; if(!window.__sdput) return 'no relay: run relay_yt.js first';
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 const mp=document.querySelector('#movie_player');
 const pr=(mp&&mp.getPlayerResponse&&mp.getPlayerResponse())||window.ytInitialPlayerResponse;
 const vid=pr&&pr.videoDetails&&pr.videoDetails.videoId;
 // 1) the player's own caption request (has every parameter YouTube wants); turn CC on once if there is none yet
 const fromPerf=()=>performance.getEntriesByType('resource').map(e=>e.name).filter(n=>n.includes('/api/timedtext')&&n.includes('v='+vid)).pop();
 let url=fromPerf();
 if(!url){const b=document.querySelector('.ytp-subtitles-button');if(b&&b.getAttribute('aria-pressed')!=='true'){b.click();await sleep(4000);url=fromPerf();b.click()}}
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
})()
