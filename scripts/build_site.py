#!/usr/bin/env python3
"""Build site/ from the local Framer export in source-framer/.

Draft-deploy transformations (nothing else is changed):
  - noindex meta tag on every HTML page
  - outbound link to the CDM subdomain points to "#"
  - Apps Script <iframe> resource widgets (broken on the live Framer page: missing
    Google document) replaced by a plain link block to resources.biketourfrance.net
    (HTML pages and the Framer embed component). No iframe, no script.
  - embed url values pointing at Apps Script blanked
  - Framer api.framer.com calls in the runtime pointed at an inert URL
  - Framer runtime page metadata robots value set to noindex, nofollow (the runtime
    rewrites the robots meta tag after load)
  - robots.txt (Disallow: /) and _headers (X-Robots-Tag: noindex, nofollow, noarchive)
  - Framer editor-only folders (api.framer.com, events.framer.com, framer.com) left out

source-framer/ is gitignored because the export contains Apps Script deployment IDs.
The output in site/ has those IDs removed, and the script fails if any remain.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source-framer")
OUT = os.path.join(ROOT, "site")
SKIP_DIRS = {
    os.path.join("assets", "api.framer.com"),
    os.path.join("assets", "events.framer.com"),
    os.path.join("assets", "framer.com"),
}

# Also consumes the stray ``` (markdown fence typo) that follows the first Framer embed.
IFRAME = re.compile(r"<iframe\b.*?</iframe>(?:\s*\\?`\\?`\\?`)?", re.S | re.I)
APPS_SCRIPT = re.compile(r"https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec")
FRAMER_API = "https://api.framer.com/"
CDM_LINK = 'href="https://cdm-sep2026.biketourfrance.net"'
NOINDEX = '<meta name="robots" content="noindex, nofollow, noarchive">'

RESOURCES_URL = "https://resources.biketourfrance.net/"
PLACEHOLDER = (
    '<div style="width:100%;box-sizing:border-box;padding:24px;text-align:center;font-family:inherit">'
    "<p style=\"font-size:18px;line-height:1.5;margin:0 0 16px\">Templates, audio guides, and trusted sites now live in the BikeTourFrance resource library.</p>"
    '<p><a href="' + RESOURCES_URL + '" target="_blank" rel="noopener" '
    'style="display:inline-block;font-size:16px;padding:12px 24px;background:#2f5d1f;color:#fff;'
    'text-decoration:none;border-radius:4px">Open the resource library</a></p>'
    "</div>"
)

ROBOTS = "User-agent: *\nDisallow: /\n"
HEADERS = "/*\n  X-Robots-Tag: noindex, nofollow, noarchive\n"


def transform(text, is_html, counts):
    text, n = IFRAME.subn(PLACEHOLDER, text)
    counts["iframes_replaced"] += n
    text, n = APPS_SCRIPT.subn("", text)
    counts["apps_script_urls_removed"] += n
    if FRAMER_API in text:
        counts["framer_api_calls_blocked"] += text.count(FRAMER_API)
        text = text.replace(FRAMER_API, "about:blank#blocked-")
    text, n = re.subn(r"robots:`max-image-preview:large`", "robots:`noindex, nofollow, noarchive`", text)
    counts["runtime_robots_patched"] += n
    if is_html:
        text, n = re.subn(re.escape(CDM_LINK), 'href="#"', text)
        counts["cdm_links"] += n
        text = re.sub(r'<meta name="robots"[^>]*>', "", text)
        text = text.replace("<head>", "<head>" + NOINDEX, 1)
        counts["noindex"] += 1
    return text


def main():
    if not os.path.isdir(SRC):
        sys.exit("source-framer/ not found")
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    counts = {
        "files": 0,
        "iframes_replaced": 0,
        "apps_script_urls_removed": 0,
        "framer_api_calls_blocked": 0,
        "runtime_robots_patched": 0,
        "cdm_links": 0,
        "noindex": 0,
    }
    for dirpath, dirnames, filenames in os.walk(SRC):
        rel_dir = os.path.relpath(dirpath, SRC)
        dirnames[:] = [d for d in dirnames if os.path.normpath(os.path.join(rel_dir, d)) not in SKIP_DIRS]
        os.makedirs(os.path.join(OUT, rel_dir), exist_ok=True)
        for name in filenames:
            src = os.path.join(dirpath, name)
            dst = os.path.join(OUT, rel_dir, name)
            if name.endswith((".html", ".mjs", ".js")):
                text = open(src, encoding="utf-8").read()
                text = transform(text, name.endswith(".html"), counts)
                open(dst, "w", encoding="utf-8").write(text)
            else:
                shutil.copyfile(src, dst)
            counts["files"] += 1
    open(os.path.join(OUT, "robots.txt"), "w").write(ROBOTS)
    open(os.path.join(OUT, "_headers"), "w").write(HEADERS)
    print(counts)


if __name__ == "__main__":
    main()
