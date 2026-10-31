function fix7(text){
  const rep={};
  const strip=s=>s.replace(/[“”‘’"]/g,'').replace(/(^|[^઀-૿A-Za-z0-9])'|'(?![઀-૿A-Za-z0-9])/g,'$1');
  const ns=s=>strip(s).replace(/\s+/g,' ').trim();
  // 1. duplicated paragraph near 68 min: drop the first copy if it equals the second
  const P='આમ દેહથી તો આટલું પત્યું';
  const a=text.indexOf(P), b=a<0?-1:text.indexOf(P,a+10);
  if(a>=0&&b>0){
    const first=text.slice(a,b), end='ખોટું જ કહેવાય ને!';
    const e2=text.indexOf(end,b); const second=e2>0?text.slice(b,e2+end.length):'';
    if(ns(first)===ns(second)){text=text.slice(0,a)+text.slice(b);rep.dup='removed '+first.length+' chars'}
    else rep.dup='NOT equal — left alone';
  } else rep.dup='not found';
  // 2. missing passage 8:29–9:45
  const PASS='કેમ? તો કે, તે ઝેર પીધું છે. કે હા, તને એવું દેખાય છે, એ એ તારી દ્રષ્ટિમાં ઝેર છે, એના પ્રત્યે ચડેલું તને. આ ઝેર તારું કયા જન્મેવું ઉતરશે, હું તો એ વિચારું છું. અને જે દાડે આ સમાચાર, એટલે આ ઘટના, આ વાર્તાલાપની માહિતી, પેલા મદિરા મહાશયને જેવી મળી, એનું એક નામ છે, ચોપડીઓમાં લખેલું છે, તે દિવસથી એકદમ પ્યોર! આ તે પછી એને ક્યારેય એને સ્પર્શ ના આ, કે જિંદગી એના સાથે રહે. બહુ ઉચ્ચ કક્ષાના સાધક બન્યા. થાય તો રામકૃષ્ણના માટે આ પણ નહીં અને તે પણ નહીં, સમાન! પેલો રોજ આવે છે એટલા માટે જ એની ઉપર ભાવ છે, એવું પણ નહીં, અને તું એની ટીકાને ';
  if(text.includes('ઝેર પીધું')) rep.passage='already there';
  else { const re=/(તને હું એ વિચાર કરું છું\.)\s*(નિંદા કરે છે)/; if(re.test(text)){text=text.replace(re,'$1 '+PASS+'$2');rep.passage='inserted'} else rep.passage='anchor NOT found'; }
  // 3. quotation marks
  const before=text.length; text=strip(text); rep.quotes=(before-text.length)+' removed';
  return {text,rep};
}
if(typeof module!=='undefined') module.exports=fix7;
