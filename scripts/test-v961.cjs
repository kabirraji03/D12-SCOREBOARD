const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),assert=require('assert'),vm=require('vm');
const html=fs.readFileSync('app-v9-6-1.html','utf8');
for(const m of html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/gi))new vm.Script(m[1]);
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('**/*',r=>r.request().url()==='http://d12.test/'?r.fulfill({body:html,contentType:'text/html'}):(/\/assets\/[^/]+\.png$/.test(r.request().url())&&fs.existsSync('assets/'+r.request().url().split('/').pop()))?r.fulfill({body:fs.readFileSync('assets/'+r.request().url().split('/').pop()),contentType:'image/png'}):r.fulfill({body:'',contentType:'text/javascript'}));
 await page.goto('http://d12.test/');
 await page.evaluate(()=>{
  window.testCalls=[];window.testPin='123456';window.testRows={profiles:[{id:'op1',full_name:'O\'Brien "Test" < >',role:'operator'}],cue_tables:[{id:'table1',table_name:'Table 1',status:'available'},{id:'table2',table_name:'Table 2',status:'available'}],table_assignments:[],matches:[]};
  window.testError=false;
  function from(table){let action='select',payload,filters=[];const q={select(){return q},order(){return q},eq(k,v){filters.push([k,v]);return q},in(){return q},update(p){action='update';payload=p;return q},insert(p){action='insert';payload=p;return q},single(){return q.then(x=>({...x,data:Array.isArray(x.data)?x.data[0]:x.data}))},maybeSingle(){return q.single()},then(resolve,reject){testCalls.push({table,action,payload,filters});if(window.testError)return Promise.resolve({data:null,error:{message:'Simulated cloud failure'}}).then(resolve,reject);let rows=(testRows[table]||[]).filter(r=>filters.every(([k,v])=>r[k]===v));if(action==='insert'){rows=[{id:'new-match',...payload}];(testRows[table]||=[]).push(...rows);}if(action==='update')rows.forEach(r=>Object.assign(r,payload));return Promise.resolve({data:rows,error:null}).then(resolve,reject)}};return q;}
  d12Supabase={from,functions:{async invoke(name,{body}){testCalls.push({name,body});if(name==='d12-admin-pin'){if(body.pin!==testPin)return {data:{success:false,error:'Incorrect admin PIN.'}};if(body.action==='change')testPin=body.new_pin;return {data:{success:true}};}if(name==='delete-d12-operator')testRows.profiles=[];return {data:{success:true}};}},auth:{async signOut(){}}};
  d12StartRealtime=async()=>{};d12RealtimeStop=()=>{};d12RefreshCloudAggregate=async()=>{};d12RecordCloudEvent=async()=>{};
  D12_AUTH.user={id:'admin1',email:'admin@example.test'};D12_AUTH.profile={role:'admin',full_name:'Admin'};D12_DEVICE_SELECTED_SESSION=true;cur='Admin';render();
 });
 await page.locator('#d12AdminPin').fill('000000');await page.locator('#d12UnlockPinBtn').click();await page.getByText('Incorrect admin PIN.',{exact:true}).waitFor();
 await page.locator('#d12AdminPin').fill('123456');await page.locator('#d12UnlockPinBtn').click();await page.locator('#d12NewOperatorName').waitFor();
 async function handlers(){const bad=await page.evaluate(()=>[...document.querySelectorAll('*')].flatMap(el=>[...el.attributes].filter(a=>/^on/.test(a.name)).flatMap(a=>{try{new Function(a.value);return []}catch(e){return [a.value+':'+e.message]}})));assert.deepEqual(bad,[]);}
 await handlers();
 await page.locator('#d12NewOperatorName').fill('New Operator');assert.equal(await page.locator('#d12NewOperatorEmail').count(),0);await page.locator('#d12NewOperatorWhatsApp').fill('+234 801 234 5678');await page.getByRole('button',{name:'Generate PIN',exact:true}).click();assert.match(await page.locator('#d12NewOperatorPassword').inputValue(),/^\d{6}$/);
 await page.locator('#d12CreateOperatorBtn').click();await page.getByRole('button',{name:'Open WhatsApp Message'}).waitFor();
 assert.equal(await page.evaluate(()=>testCalls.find(c=>c.name==='create-d12-operator-v961').body.whatsapp_number),'2348012345678');assert.equal(await page.evaluate(()=>Object.hasOwn(testCalls.find(c=>c.name==='create-d12-operator-v961').body,'email')),false);
 await page.evaluate(()=>{window.confirm=()=>true;window.alert=()=>{}});await page.getByRole('button',{name:'Delete Operator',exact:true}).click();
 // Dismiss success alert if already open by using a global handler for subsequent actions.
 await page.evaluate(()=>{window.alert=message=>testCalls.push({alert:message})});
 await page.evaluate(()=>go('Settings'));await page.locator('#d12AdminPin').waitFor();await page.locator('#d12AdminPin').fill('123456');await page.locator('#d12UnlockPinBtn').click();await page.locator('#d12OldPin').fill('123456');await page.locator('#d12NewPin').fill('654321');await page.locator('#d12ConfirmPin').fill('654321');await page.locator('#d12ChangePinBtn').click();await page.locator('#d12AdminPin').waitFor();
 await page.locator('#d12AdminPin').fill('123456');await page.locator('#d12UnlockPinBtn').click();await page.getByText('Incorrect admin PIN.',{exact:true}).waitFor();await page.locator('#d12AdminPin').fill('654321');await page.locator('#d12UnlockPinBtn').click();await page.locator('#d12OldPin').waitFor();
 await page.evaluate(()=>go('8-Ball'));await page.locator('#d12ScoringTable').selectOption('table1');await page.getByRole('button',{name:'Open Table',exact:true}).click();await page.locator('.player').first().waitFor();
 await page.evaluate(()=>{D12_PLAYER_CACHE=[{id:'p1',full_name:'Alpha'},{id:'p2',full_name:'Beta'}];S.players=['Alpha','Beta'];Object.assign(S.games[cur],{p1:'Alpha',p2:'Beta',s1:0,s2:0});render()});
 await page.evaluate(()=>d12ScoreDelta(1,1));assert.equal(await page.evaluate(()=>testRows.matches[0].player1_score),1);
 await page.evaluate(()=>{testError=true});await page.evaluate(()=>d12ScoreDelta(1,1));assert.equal(await page.evaluate(()=>S.games[cur].s1),1);await page.evaluate(()=>{testError=false});
 await page.evaluate(()=>d12AdminOpenTable('table2'));assert.equal(await page.evaluate(()=>S.games['8-Ball'].cloudMatchId),'');assert.equal(await page.evaluate(()=>S.games['8-Ball'].s1),0);
 await page.evaluate(()=>{D12_AUTH.profile={role:'operator'};D12_AUTH.assignment=null;D12_AUTH.selectedTableId='table1';render()});assert.equal(await page.evaluate(()=>d12CurrentTableId()),null);await page.getByText('Waiting for Table Assignment',{exact:true}).waitFor();
 await page.evaluate(()=>{D12_AUTH.profile={role:'admin'};D12_AUTH.selectedTableId='table1';D12_AUTH.assignment={table_id:'table1'};});
 for(const tab of ['8-Ball','9-Ball','10-Ball','Heyball','Blackball','Duya Legends','Snooker','Players']){await page.evaluate(t=>go(t),tab);await handlers();}
 for(const [mode,width,height] of [['mobile',390,844],['tablet',768,1024],['pc',1440,900]]){await page.setViewportSize({width,height});await page.evaluate(m=>{S.set.deviceMode=m;go('Snooker')},mode);await page.screenshot({path:'test-'+mode+'.png',fullPage:true});}
 await page.evaluate(()=>{D12_AUTH.profile={role:'admin'};D12_AUTH.selectedTableId=null});
 for(const [mode,width,height] of [['mobile',320,740],['mobile',390,844],['tablet',768,1024],['pc',1440,900],['mobile',844,390]]){
  await page.setViewportSize({width,height});
  await page.evaluate(m=>{S.set.deviceMode=m;D12_DEVICE_SELECTED_SESSION=true},mode);
  for(const tab of ['8-Ball','9-Ball','10-Ball','Heyball','Blackball','Duya Legends','Snooker','Players','Admin','Settings']){
   await page.evaluate(t=>go(t),tab);
   if(['Admin','Settings'].includes(tab)){await page.locator('#d12AdminPin').fill('654321');await page.locator('#d12UnlockPinBtn').click();await page.locator('#d12ChangePinBtn').waitFor();}
   await handlers();
   const state=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,tabCount:document.querySelectorAll('#tabs .tab').length,icons:document.querySelectorAll('#tabs .tab-icon').length,bad:[...document.querySelectorAll('#app button,#app input:not([type=range]),#app select,#app h2,.cue-table-label')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.left< -1||r.right>innerWidth+1||r.width<35)}).map(e=>({id:e.id,text:e.textContent.slice(0,40),w:e.getBoundingClientRect().width}))}));
   assert.ok(state.scroll<=width+1,JSON.stringify({mode,width,tab,state}));assert.equal(state.icons,state.tabCount);assert.deepEqual(state.bad,[],JSON.stringify({mode,width,tab,state}));
   if(tab==='Settings'){
    await page.locator('#d12LiquidGlass').click();assert.equal(await page.evaluate(()=>document.body.classList.contains('liquid-glass')),false);assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem(K)).set.liquidGlass),false);
    await page.locator('#d12LiquidGlass').click();assert.equal(await page.evaluate(()=>document.body.classList.contains('liquid-glass')),true);
   }
   if(['Admin','Players','8-Ball','Settings'].includes(tab))await page.screenshot({path:`v961-${mode}-${width}-${tab}.png`,fullPage:true});
  }
  await page.locator('#tabs').evaluate(e=>{e.scrollLeft=e.scrollWidth});
  const last=await page.locator('#tabs .tab').last().boundingBox();assert.ok(last.x+last.width<=width+1);
  await page.evaluate(()=>d12ChangeDevice());
  assert.equal(await page.locator('.device-home-tab span').count(),0);assert.ok(!(await page.locator('.device-home').innerText()).includes('HOSTED'));
  await page.screenshot({path:`v961-device-${width}.png`,fullPage:true});
 }
 assert.equal(await page.locator('.d12-credits p').innerText(),'©2026 D12 Cue Club. All rights reserved. Scoreboard Manager. App designed by CUE STROKES by FERAS');
 assert.equal(await page.locator('#workspaceBar').innerText(),'Logout');
 await page.evaluate(()=>{D12_AUTH.user=null;render();window.loginPayloads=[];d12EnsureSupabase=async()=>({auth:{signInWithPassword:async payload=>{loginPayloads.push(payload);return {data:{user:{id:'test'},session:{}},error:null}}}});d12ApplySession=async()=>{};});
 await page.locator('#d12Email').fill('+234 801 234 5678');await page.locator('#d12Password').fill('001234');await page.locator('#d12LoginBtn').click();
 assert.deepEqual(await page.evaluate(()=>loginPayloads[0]),{phone:'+2348012345678',password:'001234'});
 await page.locator('#d12Email').fill('admin@example.test');await page.locator('#d12Password').fill('existing-password');await page.locator('#d12LoginBtn').click();
 assert.deepEqual(await page.evaluate(()=>loginPayloads[1]),{email:'admin@example.test',password:'existing-password'});
 await page.evaluate(()=>{S.set.liquidGlass=false;save()});await page.reload();assert.equal(await page.evaluate(()=>S.set.liquidGlass),false);assert.equal(await page.evaluate(()=>document.body.classList.contains('liquid-glass')),false);

 assert.deepEqual(errors,[]);console.log('PASS: scripts, rendered handlers, PIN gate/change, operator create/delete, table selection, cloud score save/rollback, table switching, operator assignment guard, all game tabs, 3 device layouts');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
