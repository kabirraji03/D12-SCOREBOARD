from pathlib import Path
import re

src=Path('app-v9-3.html')
s=src.read_text()

# Version identity
s=s.replace('D12 Cuesports Score Board V9.3 • Secure Access','D12 Cuesports Score Board V9.4 • Secure Access')
s=s.replace('Version 9.3 • Touch-First Context Edition','Version 9.4 • Touch-First Context Edition')

# 1) Remove Shot Clock primary button. 2) Rename More -> Match Tools.
s=re.sub(r'\s*<button class="d12-primary-action" onclick="d12OpenContext\(\'clock\'\)"><span class="ico">⏱</span><span class="lbl">Shot Clock</span></button>', '', s, count=1)
s=s.replace('<button class="d12-primary-action" onclick="d12OpenContext(\'more\')"><span class="ico">⋯</span><span class="lbl">More</span></button>', '<button class="d12-primary-action" onclick="d12OpenContext(\'more\')"><span class="ico">🧰</span><span class="lbl">Match Tools</span></button>', 1)

# Main-page shot clock renderer.
main_start=s.index('function d12MainScoring(){')
main_end=s.index('\nfunction snook(){', main_start)
new_main=r'''function d12MainShotClock(d){
  if(!S.set.independentClock)return '';
  const cp=Number(d.clockPlayer||d.active||1);d.clockPlayer=cp;
  return `<div class="card clock d12-main-clock"><h3>Shot Clock</h3><div class="clock-player-picks"><button class="clock-player-btn ${cp===1?'active':''}" onclick="selectClockPlayer(1)">${esc(d.p1||'Player 1')}</button><button class="clock-player-btn ${cp===2?'active':''}" onclick="selectClockPlayer(2)">${esc(d.p2||'Player 2')}</button></div><div class="score-player-label">Timer: ${esc(cp===1?(d.p1||'Player 1'):(d.p2||'Player 2'))}</div><div id="clock" class="time">${fmt(d.t)}</div><div class="row d12-clock-controls"><button class="btn" onclick="start()">Start</button><button class="btn ball-played-btn" onclick="ballPlayed()">● Balls - No Motion</button><button class="btn gray" onclick="stop()">Pause</button><button class="btn orange" onclick="extend()">+ Extension</button><button class="btn gray" onclick="resetclock()">Reset</button></div><p class="note">${d.e} extension(s) remaining • +${S.set.ext}s each. “Balls - No Motion” returns the clock to the default time and stops it. Press Start to begin again, or select the other player to reset and immediately start that player’s countdown.</p></div>`;
}
function d12MainScoring(){
  const d=S.games[cur];if(!d)return '';
  const clock=d12MainShotClock(d);
  if(cur==='Snooker')return snook()+snookerBallButtons(d)+clock;
  if(cur==='Duya Legends')return `<div class="card d12-main-scoring"><h3>Duya Legends Scoring</h3>${duya()}</div>`+clock;
  const p=Number(d.active)||1,pname=p===1?(d.p1||'Player 1'):(d.p2||'Player 2');
  return `<div class="card d12-main-scoring"><h3>${esc(cur)} Scoring</h3><div class="score-player-label">Active: ${esc(pname)}</div><div class="row"><button class="btn" onclick="chg(${p},1)">＋ Add Point</button><button class="btn gray" onclick="chg(${p},-1)">− Remove Point</button></div></div>`+clock;
}
'''
s=s[:main_start]+new_main+s[main_end:]

# Shot clock behavior: No Motion stops at default; switching player resets + starts.
old_select="function selectClockPlayer(n){let d=S.games[cur];n=Number(n);if(n!==1&&n!==2)return;stop();d.clockPlayer=n;d.t=S.set.shot;d.e=S.set.n;save();d12RefreshOpenContext('clock')}"
new_select="function selectClockPlayer(n){let d=S.games[cur];n=Number(n);if(n!==1&&n!==2)return;stop();d.clockPlayer=n;d.t=S.set.shot;d.e=S.set.n;save();render();start()}"
if old_select not in s: raise SystemExit('selectClockPlayer target not found')
s=s.replace(old_select,new_select,1)
old_ball="function ballPlayed(){let d=S.games[cur];stop();d.t=S.set.shot;save();d12RefreshOpenContext('clock');start()}"
new_ball="function ballPlayed(){let d=S.games[cur];stop();d.t=S.set.shot;save();render()}"
if old_ball not in s: raise SystemExit('ballPlayed target not found')
s=s.replace(old_ball,new_ball,1)
# Main-page controls need live rerender after reset/extension too.
s=s.replace("function resetclock(){stop();let d=S.games[cur];d.t=S.set.shot;d.e=S.set.n;save();d12RefreshOpenContext('clock')}","function resetclock(){stop();let d=S.games[cur];d.t=S.set.shot;d.e=S.set.n;save();render()}",1)
s=s.replace("function extend(){let d=S.games[cur];if(d.e<=0)return alert('No extensions remaining.');d.t+=S.set.ext;d.e--;save();d12RefreshOpenContext('clock')}","function extend(){let d=S.games[cur];if(d.e<=0)return alert('No extensions remaining.');d.t+=S.set.ext;d.e--;save();render()}",1)

# 3) Widen right-side Award Foul button.
s=s.replace('<h3 style="margin-top:14px">Foul Count System</h3><div class="row"><select id="fp"', '<h3 style="margin-top:14px">Foul Count System</h3><div class="row snooker-foul-row"><select id="fp"',1)
s=s.replace('<button class="btn red" onclick="sf()">Award Foul</button>', '<button class="btn red snooker-foul-award" onclick="sf()">Award Foul</button>',1)

# 4) Distinct Century / Maximum-147 audio feedback, hooked into the central break recorder.
reward_hook=r'''
/* VERSION 9.4 — DISTINCT SNOOKER ACHIEVEMENT AUDIO */
function d12V94PlayAchievementSound(kind){
  if(S?.set?.vibe&&navigator.vibrate){try{navigator.vibrate(kind==='maximum'?[160,60,160,60,320]:[110,55,110])}catch(_){}}
  if(!S?.set?.sound)return;
  try{
    const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;
    const c=new AC();
    const notes=kind==='maximum'?[523.25,659.25,783.99,1046.5,1318.5,1568]:[523.25,659.25,783.99,1046.5];
    const gap=kind==='maximum'?0.115:0.14;
    notes.forEach((freq,i)=>{
      const o=c.createOscillator(),g=c.createGain();o.type=kind==='maximum'?'triangle':'sine';o.frequency.value=freq;
      const t=c.currentTime+i*gap;g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(kind==='maximum'?0.12:0.085,t+0.018);g.gain.exponentialRampToValueAtTime(0.0001,t+0.22);
      o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+0.24);
    });
    if(kind==='maximum'){
      const o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.value=104.65;const t=c.currentTime;g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(0.055,t+0.03);g.gain.exponentialRampToValueAtTime(0.0001,t+0.78);o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+0.8);
    }
    setTimeout(()=>{try{c.close()}catch(_){}},1800);
  }catch(err){console.warn('Achievement sound unavailable',err)}
}
const d12V94SnookerRecordPotBase=snookerRecordPot;
snookerRecordPot=function(g,p,value){
  const key='snookerMaxBreak'+Number(p),before=Math.max(0,Number(g?.[key])||0);
  const result=d12V94SnookerRecordPotBase(g,p,value);
  const after=Math.max(0,Number(g?.[key])||0);
  if(before<147&&after>=147)d12V94PlayAchievementSound('maximum');
  else if(before<100&&after>=100)d12V94PlayAchievementSound('century');
  return result;
};
'''
boot_marker="document.addEventListener('DOMContentLoaded',()=>{d12BootAuth()});"
if boot_marker not in s: raise SystemExit('boot marker not found')
s=s.replace(boot_marker,reward_hook+'\n'+boot_marker,1)

# V9.4 layout overrides.
css=r'''
/* VERSION 9.4 — MAIN SHOT CLOCK + FOUL WIDTH */
.d12-primary-actions{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.d12-main-clock{margin-top:12px}
.d12-main-clock .clock-player-picks{margin-bottom:8px}
.d12-main-clock .d12-clock-controls{align-items:stretch}
.d12-main-clock .ball-played-btn{min-width:180px}
.snooker-foul-row{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(190px,1.35fr)!important;gap:10px!important;align-items:stretch!important}
.snooker-foul-row select{width:100%!important;min-width:0!important}
.snooker-foul-row .snooker-foul-award{width:100%!important;min-width:190px!important}
@media(max-width:700px){.d12-primary-actions{grid-template-columns:repeat(2,minmax(0,1fr))!important}.d12-main-clock .ball-played-btn{min-width:0}.snooker-foul-row{grid-template-columns:minmax(0,.8fr) minmax(150px,1.2fr)!important}.snooker-foul-row .snooker-foul-award{min-width:150px!important}}
'''
s=s.replace('</style>',css+'</style>',1)

Path('app-v9-4.html').write_text(s)

# Structural safety checks
assert 'V9.4' in s
assert "d12OpenContext('clock')" not in s[s.index('function d12PrimaryActions()'):s.index('function d12ContextTitle')]
assert '>Match Tools</span>' in s
assert 'Balls - No Motion' in s
assert "function ballPlayed(){let d=S.games[cur];stop();d.t=S.set.shot;save();render()}" in s
assert "render();start()}function ballPlayed" in s
assert 'snooker-foul-award' in s
assert 'd12V94PlayAchievementSound' in s
assert "d12V94PlayAchievementSound('century')" in s
assert "d12V94PlayAchievementSound('maximum')" in s
print('Version 9.4 build created successfully')
