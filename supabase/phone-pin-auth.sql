-- Configure as the Send SMS Auth Hook before enabling the Phone provider.
-- Admin-created confirmed phone identities use PIN/password login, not OTP.
-- Reject all SMS flows; never pretend an undelivered verification code was sent.
CREATE FUNCTION public.d12_reject_sms_login(event jsonb)
RETURNS jsonb LANGUAGE sql IMMUTABLE SECURITY INVOKER SET search_path = ''
AS $$ SELECT '{"error":{"http_code":403,"message":"SMS sign-in is unavailable. Use your admin-issued WhatsApp number and PIN."}}'::jsonb $$;
REVOKE ALL ON FUNCTION public.d12_reject_sms_login(jsonb) FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.d12_reject_sms_login(jsonb) TO supabase_auth_admin;
GRANT USAGE ON SCHEMA public TO supabase_auth_admin;
