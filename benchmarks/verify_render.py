"""Optional isolated headless browser QA; never imported by the CLI."""

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


def verify(path, out):
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        context = browser.new_context(offline=True, viewport={"width": 1440, "height": 1000})
        page = context.new_page()
        requests, errors = [], []
        page.on("request", lambda r: requests.append(r.url))
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(path.resolve().as_uri())
        headings = page.locator("h1,h2").all_text_contents()
        assert len(headings) == 7 and headings[0] == "What this report saw"
        assert page.locator("svg").count() > 0
        assert not errors
        assert not any(u.startswith(("http:", "https:", "ws:", "wss:")) for u in requests)
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        page.screenshot(path=str(out / "desktop.png"))
        page.locator("svg").first.screenshot(path=str(out / "distribution.png"))
        if page.locator("svg").count() > 1:
            page.locator("svg").last.screenshot(path=str(out / "loss-ratio.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("window.scrollTo(0, 0)")
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        page.screenshot(path=str(out / "mobile.png"))
        data = {
            "headings": headings,
            "svg_charts": page.locator("svg").count(),
            "external_requests": 0,
            "javascript_errors": errors,
            "offline": True,
            "desktop_width": 1440,
            "mobile_width": 390,
        }
        (out / "verification.json").write_text(json.dumps(data, indent=2))
        context.close()
        browser.close()
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.report, args.out)))
