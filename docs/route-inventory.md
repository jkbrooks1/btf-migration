# Route inventory

Source: local Framer export `source-framer/` (published Sep 30, 2026, 1:06 AM UTC). The export search indexes list exactly two routes.

| Route | Source file | Status | Notes |
|-------|-------------|--------|-------|
| `/` | `index.html` | Included | Home page. Copy, images, and navigation unchanged. |
| `/resources` | `resources/index.html` | Included | Served by Cloudflare Pages from `resources/index.html`. `/resources/` redirects to `/resources` automatically. |

No routes are skipped. No `_redirects` file is needed.

## Files not carried into `site/`

| Item | Status | Reason |
|------|--------|--------|
| `assets/api.framer.com/` | Skipped | Framer editor auth stub (an error message, not a token). Not used by the public pages. |
| `assets/events.framer.com/` | Skipped | Framer event/analytics stub. No analytics allowed on the draft. |
| `assets/framer.com/` | Skipped | Framer editor bootstrap. Not referenced by either page. |

## Draft-deploy changes to routes

| Where | Original | Draft |
|-------|----------|-------|
| `/` outbound link | `https://cdm-sep2026.biketourfrance.net` | `#`. Point it back to the real link once outbound links are approved. |
| `/resources` "Helpful Stuff" embed | Google Apps Script iframe (broken on live: source document missing) | Link block to `https://resources.biketourfrance.net/` (no iframe). |
| `/resources` "Helpful Sites" embed | Google Apps Script iframe (broken on live: source document missing) | Same link block to `https://resources.biketourfrance.net/` (no iframe). |
| Runtime call to `api.framer.com/functions/check-iframe-url` | Live Framer API call | Blocked (`about:blank#blocked-`). |
| Every page | none | `<meta name="robots" content="noindex">`; site-wide `X-Robots-Tag: noindex, nofollow` in `_headers`; `robots.txt` with `Disallow: /`. |

## Known facts for later

- The Apps Script deployments behind the two `/resources` embeds return an error (their source Google document is missing). The live btf.net page shows that error too (checked 2026-10-02). A new site, `resources.biketourfrance.net`, is live (static page with audio, documents, and external links). Staging links to it. The Framer page itself is still unfixed; that is a live-site change for the owner.
- The export contains no forms, no WhatsApp links, and no `mailto:`/`tel:` links.
- The export contains no analytics scripts. Framer runtime code that calls `api.framer.com` was blocked.
- `source-framer/` holds the Apps Script deployment IDs and is not committed. `site/` has them removed.
