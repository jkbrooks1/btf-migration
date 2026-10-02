# btf-migration

Rebuild of the btf.net Framer site, deployed to a temporary Cloudflare Pages project (`temp-btf`).

## Goal

Make a close visual and functional copy of the current Framer site first. No redesign in this pass. Keep the same pages, copy, images, navigation, and URL paths.

## Layout

- `source-framer/` : local-only copy of the Framer export, kept unmodified for comparison. It is NOT committed (it is listed in `.gitignore`) because the export contains Google Apps Script deployment IDs and this repo is public.
- `site/` : static files generated from the export (deployment IDs removed). Astro serves this folder unchanged as its static files (`publicDir` in `astro.config.mjs`). It includes `robots.txt` and `_headers`.
- `src/pages/404.astro` : the real 404 page. Cloudflare Pages returns it with HTTP 404 for unknown paths.
- `astro.config.mjs`, `package.json` : minimal Astro setup. `npm run build` writes `dist/`.
- `dist/` : build output that gets deployed. Not committed.
- `scripts/build_site.py` : rebuilds `site/` from `source-framer/` and applies the draft rules (`npm run build:site`).
- `docs/route-inventory.md` : every route found, marked included, skipped, or redirected.
- `docs/cutover.md` : the future production cutover process. Cutover is a separate, explicitly approved task.

## Workflow

- Work on a branch (for example `rebuild/initial`) and open a pull request.
- Do not push to `main` without approval. The Pages project treats `main` as production.
- Deploy only by pushing to GitHub; Cloudflare Pages builds the preview. Do not use Wrangler to deploy.
- Use only existing `wrangler login` or `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` environment variables. Never print, paste, or commit tokens.
- Before every commit and every deploy, two leak checks must return nothing: a `git grep` for the Google Apps Script macros URL, and a `grep -r` of `site/` for the Apps Script deployment ID prefix. The exact commands are in the build log.

## Draft-deploy rules

- Contact and waitlist forms (none exist in the Framer export) would be non-submitting placeholders, clearly marked "Draft - not live".
- The two embedded Apps Script resource widgets on `/resources` (broken on the live Framer page) are replaced by a link block to `https://resources.biketourfrance.net/`.
- WhatsApp and other outbound links are real only if approved; otherwise they point to `#`. The `cdm-sep2026.biketourfrance.net` link on the home page points to `#`.
- No analytics scripts. Framer editor and `api.framer.com` calls are removed or blocked.
- Staging no-index protections, all required and never removed during staging:
  - `noindex, nofollow, noarchive` robots meta tag on every page (including the 404 page)
  - `X-Robots-Tag: noindex, nofollow, noarchive` response header (`site/_headers`)
  - `robots.txt` with `User-agent: *` and `Disallow: /`

## Build and deploy

Deploys come from GitHub only. Do not deploy with Wrangler.

- Repository: `jkbrooks1/biketourfrance`. Cloudflare Pages project `temp-btf` is Git-connected to it.
- Production branch: `main`. Production auto-deploys are disabled until the owner explicitly approves them. Never push to `main` without approval.
- Pushing a branch creates a GitHub-driven preview deployment. Branch `rebuild/initial` gets the preview alias `rebuild-initial.temp-btf.pages.dev`.
- Cloudflare build settings expected: build command `npm run build`, output directory `dist`, Node 22 (`.node-version`).

```bash
npm install
npm run build:site     # optional: regenerate site/ from source-framer/ (needs the local export)
npm run build          # Astro build to dist/
git push origin rebuild/initial   # Cloudflare builds and deploys the preview
```

Local test (no deploy): `npx wrangler pages dev dist` (older Wrangler versions may need `--compatibility-date=2026-07-08`).

## Status

- [x] Route inventory
- [x] Assets and fonts copied
- [x] Pages rebuilt
- [x] Side-by-side check against live site (page text matches on `/`; `/resources` differs only where the broken embeds were replaced)
- [x] Draft deployed to temp-btf (preview: https://rebuild-initial.temp-btf.pages.dev)
- [x] Real 404 page (HTTP 404) and enforced no-index protections
- [x] Cutover process documented (`docs/cutover.md`, not started)
- [ ] Integrations approved (forms, WhatsApp, analytics)
- [ ] Owner review of staging preview
