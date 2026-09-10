# D12 Cuesports Score Board — GitHub Pages Ready

This folder is the hosted-web build of D12 Cuesports Score Board Version 9.0.

## Why this build fixes the mobile login problem
The mobile error occurred while the app was opened as a local `file://` HTML document. Some mobile browsers/file viewers block or fail external JavaScript from that context. GitHub Pages serves the same app over HTTPS, so the Supabase browser library and authentication can load normally.

## Publish with GitHub Pages
1. Sign in to GitHub and create a new repository, e.g. `d12-scoreboard`. Public is simplest for GitHub Pages.
2. Upload **everything in this folder** to the repository root: `index.html`, `.nojekyll`, the `assets` folder, and this README.
3. Open the repository **Settings** → **Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select branch **main** and folder **/(root)**, then Save.
6. Wait for GitHub to publish the site. Your address will normally be:
   `https://YOUR-GITHUB-USERNAME.github.io/d12-scoreboard/`
7. Open that HTTPS address on mobile, tablet, or PC and sign in with the normal D12 Supabase account.

## Important
- Do not open `index.html` directly from the phone Files/Downloads app for normal use. Use the GitHub Pages HTTPS address.
- The Supabase publishable key in the browser is intentionally a browser-safe key. Keep authorization enforced with Supabase RLS and the existing admin/operator checks.
- Do not place a Supabase service-role/secret key in `index.html` or any public GitHub file.
- Existing Edge Functions (`create-d12-operator`, `delete-d12-operator`, `manage-d12-tables`) remain in Supabase and are not moved into GitHub Pages.

## iPhone / iPad shortcut
Open the GitHub Pages address in Safari → Share → **Add to Home Screen**. The scoreboard will then launch like an app shortcut.
