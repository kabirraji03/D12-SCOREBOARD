-- Service-only PIN storage. Browser roles cannot read hashes or call this RPC.
CREATE TABLE public.d12_admin_security (
  user_id uuid PRIMARY KEY REFERENCES public.profiles(id) ON DELETE CASCADE,
  pin_hash text NOT NULL,
  failures integer NOT NULL DEFAULT 0,
  locked_until timestamptz
);
ALTER TABLE public.d12_admin_security ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.d12_admin_security FROM PUBLIC, anon, authenticated;
GRANT ALL ON public.d12_admin_security TO service_role;
CREATE FUNCTION public.d12_check_admin_pin(p_user_id uuid, p_pin text, p_new_pin text DEFAULT NULL)
RETURNS jsonb LANGUAGE plpgsql SECURITY INVOKER SET search_path = '' AS $$
DECLARE s public.d12_admin_security; n integer;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM public.profiles WHERE id=p_user_id AND role='admin') THEN
    RETURN jsonb_build_object('success',false,'error','Administrator access required.');
  END IF;
  IF p_pin IS NULL OR p_pin !~ '^[0-9]{6}$' OR (p_new_pin IS NOT NULL AND p_new_pin !~ '^[0-9]{6}$') THEN
    RETURN jsonb_build_object('success',false,'error','PIN must contain exactly 6 digits.');
  END IF;
  INSERT INTO public.d12_admin_security(user_id,pin_hash)
    VALUES(p_user_id,extensions.crypt('123456',extensions.gen_salt('bf',10))) ON CONFLICT DO NOTHING;
  SELECT * INTO s FROM public.d12_admin_security WHERE user_id=p_user_id FOR UPDATE;
  IF s.locked_until > now() THEN
    RETURN jsonb_build_object('success',false,'error','Too many attempts. Try again in 5 minutes.');
  END IF;
  IF extensions.crypt(p_pin,s.pin_hash) <> s.pin_hash THEN
    n := CASE WHEN s.locked_until IS NOT NULL THEN 1 ELSE s.failures+1 END;
    UPDATE public.d12_admin_security SET failures=n,locked_until=CASE WHEN n>=5 THEN now()+interval '5 minutes' ELSE NULL END WHERE user_id=p_user_id;
    RETURN jsonb_build_object('success',false,'error',CASE WHEN n>=5 THEN 'Too many attempts. Try again in 5 minutes.' ELSE 'Incorrect admin PIN.' END);
  END IF;
  UPDATE public.d12_admin_security SET failures=0,locked_until=NULL,
    pin_hash=CASE WHEN p_new_pin IS NULL THEN pin_hash ELSE extensions.crypt(p_new_pin,extensions.gen_salt('bf',10)) END WHERE user_id=p_user_id;
  RETURN jsonb_build_object('success',true);
END;
$$;
REVOKE ALL ON FUNCTION public.d12_check_admin_pin(uuid,text,text) FROM PUBLIC,anon,authenticated;
GRANT EXECUTE ON FUNCTION public.d12_check_admin_pin(uuid,text,text) TO service_role;
