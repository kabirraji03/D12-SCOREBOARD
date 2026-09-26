# D12 Scoreboard V9.6.1

Based on the confirmed live V9.6 build at commit `9d944c2`. The live HTML SHA-256 matched the local baseline before changes.

## Changes

- Operator creation now collects only full name, WhatsApp number and a six-digit PIN. The server creates a confirmed **phone** Auth identity, without an email or synthetic email. Operators use the WhatsApp number and PIN to sign in. Administrator email/password sign-in remains available.
- The database was inspected: scoreboard `players` and `profiles` have no email columns, and there were zero operator accounts. No existing scoreboard email data needed deletion. The administrator's Auth email and the separate membership application's data are preserved.
- Main navigation scrolls horizontally, keeps readable touch targets, and includes an icon on every tab. Admin PIN, player registration and cue-table selection controls wrap without clipping.
- Liquid Glass lighting, transparency and blur can be switched off in Settings; the preference survives reloads in existing local settings storage.
- Header contains the title, version and Logout. The D12 logo is larger and retains its aspect ratio. Security prose was removed. Device choice cards no longer contain the removed descriptions or Hosted Device Setup label.
- Footer contains the supplied original CUE STROKES by FERAS PNG, without cropping or stretching, and the exact requested credits.
- Existing scoring, Supabase database policies, realtime subscriptions, table assignment, export behavior, and custom-domain configuration are preserved.

## Validation completed

- Parsed all inline JavaScript and compiled rendered event handlers.
- Tested PIN rejection, change and re-entry; operator creation payload without email; phone normalization and PIN generation; quoted-name deletion; score save, failure rollback, table switching and assignment guarding.
- Tested all ten tabs at 320×740, 390×844, 768×1024, 1440×900 and 844×390. Checked horizontal overflow and interactive-control bounds, navigation scrolling, settings persistence, and device cards. Reviewed rendered screenshots with local image assets.
- Tested email-based administrator login and phone-based operator login request routing with an Auth test double, including leading-zero PINs.
- Backend tests verify authentication/role denial, required phone and exactly-six-digit PIN validation, no email in Auth creation or response, and existing delete safety behavior.
- Real-network candidate smoke test loaded the Supabase client and assets without runtime errors; all three existing management endpoints reject unauthenticated requests.

## Deployment gate — not yet cleared

The real Supabase project currently reports `external.phone: false`. Enable phone/password authentication in the project's Auth settings, then test actual operator creation, sign-in, assigned-table scoring and cleanup before merging/publishing. Do not publish the frontend or replace the live creation function until this gate passes.

`index.html` will route to `app-v9-6-1.html?v=96101`. `CNAME` remains `scoreboard.d12cueclub.com`. Existing builds are retained. No database schema migration is needed.

The Supabase security advisor reported existing warnings for older SECURITY DEFINER functions and password protection; this change adds no database grants, policies or functions. See the [advisor documentation](https://supabase.com/docs/guides/database/database-linter?lint=0028_anon_security_definer_function_executable).
