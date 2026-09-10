from pathlib import Path

src=Path('app-v9-4.html')
s=src.read_text()

s=s.replace('D12 Cuesports Score Board V9.4 • Secure Access','D12 Cuesports Score Board V9.5 • Responsive Interface Edition')
s=s.replace('Version 9.4 • Touch-First Context Edition','Version 9.5 • Responsive Interface Edition')

css=r'''
/* VERSION 9.5 — PROFESSIONAL RESPONSIVE INTERFACE */
html{width:100%;min-height:100%;overflow-x:hidden!important;scroll-behavior:smooth}
body{width:100%;min-height:100dvh;overflow-x:hidden!important;overflow-y:auto!important;-webkit-text-size-adjust:100%}
main#app{transform:none!important;scale:1!important;zoom:1!important;transform-origin:top center!important;width:100%!important;min-width:0!important;margin:0 auto!important;overflow:visible!important}
body:not(.d12-auth-mode) main#app{min-height:calc(100dvh - 120px)!important}
body:not(.d12-auth-mode) .head{position:sticky!important;top:0!important;z-index:100!important}
body:not(.d12-auth-mode) .tabs{z-index:95!important;scrollbar-width:none;-ms-overflow-style:none;scroll-snap-type:x proximity;overscroll-behavior-x:contain}
body:not(.d12-auth-mode) .tabs::-webkit-scrollbar{display:none}
body:not(.d12-auth-mode) .tab{scroll-snap-align:start;flex:0 0 auto}
.card,.player,.d12-main-scoring,.d12-main-clock{min-width:0}
button,.btn,.tab,.clock-player-btn,.player-select{touch-action:manipulation;-webkit-tap-highlight-color:transparent}
button:focus-visible,.btn:focus-visible,.tab:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid color-mix(in srgb,var(--accent) 60%,white 40%);outline-offset:2px}

/* MOBILE — readable, full width, natural vertical scroll */
@media (max-width:700px){
  html,body{overflow-y:auto!important;height:auto!important;min-height:100dvh!important}
  body.device-mobile:not(.d12-auth-mode){display:block!important;padding:0!important}
  body.device-mobile:not(.d12-auth-mode) main#app{max-width:none!important;width:100%!important;padding:10px 10px calc(24px + env(safe-area-inset-bottom))!important;transform:none!important;zoom:1!important}
  body.device-mobile:not(.d12-auth-mode) .head{padding:8px 10px!important;min-height:62px!important}
  body.device-mobile:not(.d12-auth-mode) .brand{gap:8px!important;align-items:center!important}
  body.device-mobile:not(.d12-auth-mode) .club-logo{width:42px!important;height:42px!important;border-radius:11px!important;flex:0 0 42px!important}
  body.device-mobile:not(.d12-auth-mode) h1{font-size:18px!important;line-height:1.08!important}
  body.device-mobile:not(.d12-auth-mode) .sub{font-size:10px!important;line-height:1.25!important;margin-top:2px!important}
  body.device-mobile:not(.d12-auth-mode) .tabs{position:sticky!important;top:58px!important;padding:7px 8px!important;gap:6px!important;background:color-mix(in srgb,var(--bg) 94%,transparent)!important;backdrop-filter:blur(18px)!important}
  body.device-mobile:not(.d12-auth-mode) .tab{min-height:40px!important;padding:8px 11px!important;border-radius:12px!important;font-size:12px!important;line-height:1!important}
  body.device-mobile:not(.d12-auth-mode) .hero{height:105px!important;border-radius:18px!important;padding:14px!important;margin-bottom:8px!important}
  body.device-mobile:not(.d12-auth-mode) .hero h2{font-size:27px!important;line-height:1!important}
  body.device-mobile:not(.d12-auth-mode) .hero p{font-size:11px!important;max-width:92%!important}
  body.device-mobile:not(.d12-auth-mode) .grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:8px!important;margin-top:8px!important;grid-auto-rows:auto!important}
  body.device-mobile:not(.d12-auth-mode) .card{padding:11px!important;margin-top:9px!important;border-radius:16px!important}
  body.device-mobile:not(.d12-auth-mode) .player{padding:10px 8px!important;border-radius:16px!important}
  body.device-mobile:not(.d12-auth-mode) .player .score{font-size:58px!important;min-height:70px!important;margin-top:3px!important}
  body.device-mobile:not(.d12-auth-mode) .player .name,body.device-mobile:not(.d12-auth-mode) .name{font-size:16px!important;min-height:42px!important;margin:5px 0!important}
  body.device-mobile:not(.d12-auth-mode) .player .active-tag{height:25px!important;font-size:9px!important;margin-bottom:4px!important}
  body.device-mobile:not(.d12-auth-mode) input,body.device-mobile:not(.d12-auth-mode) select{font-size:16px!important;min-height:44px!important;padding:9px!important;border-radius:12px!important}
  body.device-mobile:not(.d12-auth-mode) .btn,body.device-mobile:not(.d12-auth-mode) button.btn{min-height:46px!important;padding:9px 10px!important;border-radius:12px!important;font-size:12px!important;line-height:1.1!important}
  body.device-mobile:not(.d12-auth-mode) .row{gap:7px!important}
  body.device-mobile:not(.d12-auth-mode) .d12-primary-actions{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important;margin-top:9px!important}
  body.device-mobile:not(.d12-auth-mode) .d12-primary-action{min-height:52px!important;border-radius:13px!important;padding:7px!important}
  body.device-mobile:not(.d12-auth-mode) .d12-primary-action .ico{font-size:18px!important}
  body.device-mobile:not(.d12-auth-mode) .d12-primary-action .lbl{font-size:10px!important}
  body.device-mobile:not(.d12-auth-mode) .time{font-size:72px!important;line-height:.95!important;margin:5px 0!important}
  body.device-mobile:not(.d12-auth-mode) .clock-player-picks{display:grid!important;grid-template-columns:1fr 1fr!important;gap:7px!important}
  body.device-mobile:not(.d12-auth-mode) .clock-player-btn{min-height:46px!important;font-size:13px!important;border-radius:12px!important}
  body.device-mobile:not(.d12-auth-mode) .d12-clock-controls{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:7px!important}
  body.device-mobile:not(.d12-auth-mode) .d12-clock-controls .btn{width:100%!important;min-width:0!important}
  body.device-mobile:not(.d12-auth-mode) .d12-clock-controls .ball-played-btn{grid-column:1/-1!important;min-height:50px!important;font-size:13px!important}
  body.device-mobile:not(.d12-auth-mode) .balls{grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:7px!important}
  body.device-mobile:not(.d12-auth-mode) .balls button{min-height:50px!important;border-radius:12px!important;font-size:11px!important;padding:6px!important}
  body.device-mobile:not(.d12-auth-mode) .snooker-compact-grid{gap:8px!important}
  body.device-mobile:not(.d12-auth-mode) .snooker-mini-card{padding:9px!important;border-radius:14px!important;min-width:0!important}
  body.device-mobile:not(.d12-auth-mode) .snooker-foul-row{grid-template-columns:minmax(0,.9fr) minmax(145px,1.1fr)!important}
  body.device-mobile:not(.d12-auth-mode) .item{padding:10px!important;border-radius:12px!important;gap:6px!important;align-items:center!important}
  body.device-mobile:not(.d12-auth-mode) h2{font-size:21px!important} body.device-mobile:not(.d12-auth-mode) h3{font-size:15px!important;margin-top:4px!important;margin-bottom:8px!important}
  body.device-mobile:not(.d12-auth-mode) .note{font-size:11px!important;line-height:1.35!important}
  body.device-mobile:not(.d12-auth-mode) .d12-context-window{width:100%!important;max-height:88dvh!important;border-radius:20px 20px 0 0!important;padding:11px!important}
}

/* very narrow phones */
@media (max-width:380px){
  body.device-mobile:not(.d12-auth-mode) main#app{padding-left:7px!important;padding-right:7px!important}
  body.device-mobile:not(.d12-auth-mode) .grid{gap:6px!important}
  body.device-mobile:not(.d12-auth-mode) .player .score{font-size:50px!important}
  body.device-mobile:not(.d12-auth-mode) .btn{font-size:11px!important;padding:8px 6px!important}
  body.device-mobile:not(.d12-auth-mode) .tab{font-size:11px!important;padding:8px 9px!important}
}

/* TABLET — comfortable two-column workspace */
@media (min-width:701px) and (max-width:1199px){
  body.device-tablet:not(.d12-auth-mode){display:block!important;overflow-y:auto!important}
  body.device-tablet:not(.d12-auth-mode) main#app{width:min(100%,1024px)!important;max-width:1024px!important;padding:16px 18px 28px!important;transform:none!important;zoom:1!important}
  body.device-tablet:not(.d12-auth-mode) .head{padding:11px 18px!important}
  body.device-tablet:not(.d12-auth-mode) .club-logo{width:50px!important;height:50px!important}
  body.device-tablet:not(.d12-auth-mode) h1{font-size:23px!important}
  body.device-tablet:not(.d12-auth-mode) .tabs{top:72px!important;padding:9px 14px!important;gap:8px!important}
  body.device-tablet:not(.d12-auth-mode) .tab{min-height:44px!important;padding:10px 14px!important;font-size:13px!important}
  body.device-tablet:not(.d12-auth-mode) .hero{height:150px!important;border-radius:22px!important;padding:20px!important}
  body.device-tablet:not(.d12-auth-mode) .hero h2{font-size:34px!important}
  body.device-tablet:not(.d12-auth-mode) .grid{grid-template-columns:1fr 1fr!important;gap:14px!important;margin-top:14px!important;grid-auto-rows:auto!important}
  body.device-tablet:not(.d12-auth-mode) .card{padding:16px!important;margin-top:14px!important;border-radius:20px!important}
  body.device-tablet:not(.d12-auth-mode) .player .score{font-size:82px!important;min-height:100px!important}
  body.device-tablet:not(.d12-auth-mode) .btn{min-height:50px!important;font-size:14px!important}
  body.device-tablet:not(.d12-auth-mode) input,body.device-tablet:not(.d12-auth-mode) select{min-height:48px!important;font-size:15px!important}
  body.device-tablet:not(.d12-auth-mode) .time{font-size:96px!important}
  body.device-tablet:not(.d12-auth-mode) .d12-clock-controls{display:grid!important;grid-template-columns:repeat(5,minmax(0,1fr))!important;gap:8px!important}
  body.device-tablet:not(.d12-auth-mode) .balls{grid-template-columns:repeat(7,minmax(0,1fr))!important}
}

/* PC / LARGE DISPLAY — centered dashboard, no forced shrink */
@media (min-width:1200px){
  body.device-pc:not(.d12-auth-mode),body.device-desktop:not(.d12-auth-mode){display:block!important;overflow-y:auto!important}
  body.device-pc:not(.d12-auth-mode) main#app,body.device-desktop:not(.d12-auth-mode) main#app{width:min(calc(100% - 40px),1320px)!important;max-width:1320px!important;padding:20px 24px 36px!important;transform:none!important;zoom:1!important}
  body.device-pc:not(.d12-auth-mode) .head,body.device-desktop:not(.d12-auth-mode) .head{padding:12px max(24px,calc((100vw - 1320px)/2 + 24px))!important}
  body.device-pc:not(.d12-auth-mode) .tabs,body.device-desktop:not(.d12-auth-mode) .tabs{top:82px!important;padding:10px max(24px,calc((100vw - 1320px)/2 + 24px))!important;justify-content:flex-start!important}
  body.device-pc:not(.d12-auth-mode) .tab,body.device-desktop:not(.d12-auth-mode) .tab{min-height:46px!important;padding:11px 17px!important;font-size:14px!important}
  body.device-pc:not(.d12-auth-mode) .hero,body.device-desktop:not(.d12-auth-mode) .hero{height:180px!important;border-radius:24px!important}
  body.device-pc:not(.d12-auth-mode) .grid,body.device-desktop:not(.d12-auth-mode) .grid{grid-template-columns:1fr 1fr!important;gap:18px!important;grid-auto-rows:auto!important}
  body.device-pc:not(.d12-auth-mode) .card,body.device-desktop:not(.d12-auth-mode) .card{padding:18px!important;border-radius:22px!important}
  body.device-pc:not(.d12-auth-mode) .player .score,body.device-desktop:not(.d12-auth-mode) .player .score{font-size:92px!important}
  body.device-pc:not(.d12-auth-mode) .d12-clock-controls,body.device-desktop:not(.d12-auth-mode) .d12-clock-controls{display:grid!important;grid-template-columns:repeat(5,minmax(0,1fr))!important;gap:10px!important}
}

/* Landscape phone/tablet: use horizontal space without shrinking */
@media (orientation:landscape) and (max-height:700px){
  body:not(.d12-auth-mode) .head{position:relative!important}
  body:not(.d12-auth-mode) .tabs{top:0!important}
  body.device-mobile:not(.d12-auth-mode) .hero{height:82px!important}
  body.device-mobile:not(.d12-auth-mode) .time{font-size:60px!important}
}
'''
s=s.replace('</style>',css+'</style>',1)

# Neutralize the legacy whole-page scale-to-fit engine. Keep its name because existing
# observers/listeners call it, but make it reset scaling instead of shrinking the UI.
neutral=r'''
<script>
function d12V95ResetLegacyScaling(){
  const app=document.getElementById('app');
  if(app){app.style.setProperty('transform','none','important');app.style.setProperty('zoom','1','important');app.style.setProperty('scale','1','important');app.style.removeProperty('height');app.style.removeProperty('max-height');app.style.removeProperty('transform-origin');}
  document.documentElement.style.setProperty('--d12-fit-scale','1');
  if(!document.body.classList.contains('d12-context-open'))document.body.style.setProperty('overflow-y','auto','important');
}
function d12FitViewport(){requestAnimationFrame(d12V95ResetLegacyScaling)}
window.addEventListener('resize',d12V95ResetLegacyScaling,{passive:true});
window.addEventListener('orientationchange',()=>setTimeout(d12V95ResetLegacyScaling,120),{passive:true});
if(window.visualViewport)window.visualViewport.addEventListener('resize',d12V95ResetLegacyScaling,{passive:true});
document.addEventListener('DOMContentLoaded',()=>{d12V95ResetLegacyScaling();setTimeout(d12V95ResetLegacyScaling,250)});
</script>
'''
s=s.replace('</body>',neutral+'</body>',1)

Path('app-v9-5.html').write_text(s)

assert 'V9.5' in s
assert 'VERSION 9.5 — PROFESSIONAL RESPONSIVE INTERFACE' in s
assert 'function d12FitViewport(){requestAnimationFrame(d12V95ResetLegacyScaling)}' in s
assert 'app-v9-4.html' not in s[:200]
print('Version 9.5 responsive build created')
