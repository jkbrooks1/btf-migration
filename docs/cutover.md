# Production cutover (future work, not part of staging)

Nothing in this document is to be done during staging work.

## Status

- **Cutover is a separate, explicitly approved task.** It does not happen as a side effect of building, reviewing, merging, or deploying the staging site.
- Staging runs only on the `temp-btf` Cloudflare Pages project as a preview branch (`rebuild-initial`). No custom domain is attached. No DNS record has been changed.
- The live site stays on Framer until the owner approves cutover in a separate request.

## Future process (for the approved cutover task only)

1. **Add each production hostname through the Cloudflare Pages custom-domain workflow** for the project. Do this one hostname at a time. Do not edit DNS records by hand as a substitute.
2. **Inspect the DNS change Cloudflare says it requires** for each hostname. Record what it proposes before accepting it.
3. **Verify that MX records and unrelated TXT records remain unchanged.** Take a read-only DNS snapshot before and after, and compare them. Email for the domain depends on those records (mail routing, SPF, and domain verification).
4. **Remove the staging no-index protections only after the production domain resolves to the approved build.** The protections are:
   - the `noindex` robots meta tag on every page
   - the `X-Robots-Tag: noindex, nofollow, noarchive` response header (`site/_headers`)
   - `robots.txt` with `Disallow: /`
   - the robots value set in the Framer runtime page metadata (patched by `scripts/build_site.py`)

   Keep all of them in place until that check passes.

## Before cutover is requested

- Owner reviews the staging preview on phone and desktop.
- Owner decides the home page link to the CDM subdomain (currently `#` on staging).
- Owner decides on forms, WhatsApp links, and analytics (none exist in the Framer export).
- Owner confirms how the Framer page's broken `/resources` embeds are handled (staging links to `resources.biketourfrance.net` instead).
- Merging `rebuild/initial` to `main` needs separate owner approval.

## Not in scope

- Moving the primary domain from `.net` to `.com` is a separate project.
