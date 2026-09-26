import { createClient } from 'npm:@supabase/supabase-js@2.109.0';
const cors = {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type','Access-Control-Allow-Methods':'POST, OPTIONS'};
const reply=(data:unknown,status=200)=>new Response(JSON.stringify(data),{status,headers:{...cors,'Content-Type':'application/json','Cache-Control':'no-store'}});
Deno.serve(async(req)=>{
  if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
  if(req.method!=='POST')return reply({success:false,error:'POST required.'},405);
  try{
    const token=req.headers.get('Authorization')?.replace(/^Bearer\s+/i,'')||'';
    const client=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false,autoRefreshToken:false}});
    const {data:{user},error}=await client.auth.getUser(token);
    if(error||!user)return reply({success:false,error:'Sign in again to continue.'},401);
    const body=await req.json();
    if(!['verify','change'].includes(body.action)||!/^\d{6}$/.test(body.pin||'')||(body.action==='change'&&!/^\d{6}$/.test(body.new_pin||'')))return reply({success:false,error:'PIN must contain exactly 6 digits.'},400);
    const result=await client.rpc('d12_check_admin_pin',{p_user_id:user.id,p_pin:body.pin,p_new_pin:body.action==='change'?body.new_pin:null});
    if(result.error)throw result.error;
    return reply(result.data);
  }catch{return reply({success:false,error:'Unable to verify PIN. Please retry.'},500);}
});
