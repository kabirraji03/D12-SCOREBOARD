# D12 Scoreboard V9.6

Based on the confirmed live V9.5 file at commit `686edd77ef868c07282cd4663a00843e7ae99a62`. Its SHA-256 matched the custom-domain download before editing.

## Changes

- Admin and Settings require a six-digit PIN each time a tab is entered. The initial PIN is 123456. Signed-in admins can change their own PIN; the cloud stores a salted bcrypt hash and locks verification for five minutes after five failed attempts. PINs are not stored in browser storage.
- Operator creation accepts a WhatsApp number with country code and generates a six-digit login PIN. After successful creation, admins can copy login details or open a prepared WhatsApp message. No message is sent automatically. The number is retained in Auth metadata; it is never used for authorization.
- Fixed malformed Delete Operator and Remove Player handlers for names containing quotes. Operator deletion removes Auth first, allowing profile/assignment deletion to cascade atomically. Historical scores remain, with the deleted operator reference cleared. Failures are reported and duplicate clicks are blocked.
- Fixed the misspelled table-selection variable. Admins must select a cue table before scoring. Cached match IDs must match the selected table, discipline and players. Switching tables clears stale local scoring state. Reconnecting a match preserves the pending score; failed undo/redo restores the original local score.
- Kept the existing domain, asset paths, previous builds and local storage key.

## Verification

- Parsed both inline JavaScript blocks and compiled rendered event handlers, including names containing apostrophes and quotes.
- Headless Edge browser tests with a simulated cloud covered PIN rejection/change/re-entry, operator creation and deletion, PIN generation, phone normalization, table selection, score persistence and rollback, operator assignment guarding, and every discipline tab. Captured mobile, tablet and PC views.
- Backend handler tests covered authentication and role rejection, invalid email/phone input, WhatsApp metadata, self-deletion denial and Auth-deletion failure integrity.
- Transactional tests in the real database verified PIN default/change/old-PIN rejection/rate limiting and denied browser access to PIN storage/RPC. All test data and PIN changes were rolled back.
- A separate rolled-back database test verified admin scoring, assigned operator scoring, unassigned operator denial, and Auth deletion cascading while retaining match history.
- Candidate-page smoke test used real CDN assets and deployed functions: login initialized without browser errors, and all three functions rejected unauthenticated requests with HTTP 401.
- Existing real operator accounts were not created or deleted for testing. Authenticated UI behavior used test doubles; database behavior was tested separately in transactions. WhatsApp sending was not performed.

## Deployment and recovery

`index.html` routes to `app-v9-6.html?v=9601`. `CNAME` remains `scoreboard.d12cueclub.com`. To restore the prior frontend, restore the previous index pointing to `app-v9-5.html?v=9501`. Backend updates remain compatible with V9.5 operator requests. Original backend function sources are retained in the local task workspace.

The security advisor reported no new warning for this change. The PIN table intentionally has RLS with no client policies and service-only grants; see the [RLS policy advisor explanation](https://supabase.com/docs/guides/database/database-linter?lint=0008_rls_enabled_no_policy). Existing notices about older SECURITY DEFINER functions and password protection are outside this update.
