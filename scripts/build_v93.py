from pathlib import Path

src=Path('app-v9-2-9204.html')
s=src.read_text()

s=s.replace('D12 Cuesports Score Board V9.2 • Secure Access','D12 Cuesports Score Board V9.3 • Secure Access')
s=s.replace('Version 9.2 • Touch-First Context Edition','Version 9.3 • Touch-First Context Edition')

scoring_button='    <button class="d12-primary-action" onclick="d12OpenContext(\'scoring\')"><span class="ico">🎯</span><span class="lbl">Scoring</span></button>\n'
s=s.replace(scoring_button,'')

old="if(cur==='Snooker')return snookerBallButtons(d);"
new="if(cur==='Snooker')return snook()+snookerBallButtons(d);"
if old not in s:
    raise SystemExit('Snooker main scoring hook not found')
s=s.replace(old,new,1)

s=s.replace('return `<div class="card"><h3>Snooker Frame Setup</h3>','return `<div class="card snooker-setup-main"><h3>Snooker Frame Setup</h3>',1)
s=s.replace('What To Pot Next','What to Pot Next').replace('What To Pot NexT','What to Pot Next')

css='''
/* VERSION 9.3 — MAIN SNOOKER SETUP + COMPACT WHAT TO POT NEXT */
.snooker-setup-main{margin-top:12px}
.snooker-setup-main .snooker-target-card,.snooker-setup-main .snooker-info-card{max-width:190px!important;padding:10px 12px!important;border-radius:16px!important;min-height:118px!important}
.snooker-setup-main .snooker-target-red,.snooker-setup-main .snooker-any-color-image{width:72px!important;height:72px!important;min-width:72px!important;min-height:72px!important;max-width:72px!important;max-height:72px!important;object-fit:contain!important;border-radius:50%!important}
@media(max-width:700px){.snooker-setup-main .snooker-target-card,.snooker-setup-main .snooker-info-card{max-width:160px!important;min-height:104px!important;padding:8px!important}.snooker-setup-main .snooker-target-red,.snooker-setup-main .snooker-any-color-image{width:62px!important;height:62px!important;min-width:62px!important;min-height:62px!important;max-width:62px!important;max-height:62px!important}}
'''
s=s.replace('</style>',css+'</style>',1)

Path('app-v9-3.html').write_text(s)

assert 'V9.3' in s
assert "if(cur==='Snooker')return snook()+snookerBallButtons(d);" in s
assert "d12OpenContext('scoring')" not in s
assert 'Snooker Frame Setup' in s
assert 'What to Pot Next' in s
print('Version 9.3 build created successfully')
