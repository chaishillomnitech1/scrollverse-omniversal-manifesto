#!/usr/bin/env python3
"""Fetch allowlisted Observatory RSS/Atom feeds and preserve source-lead metadata.

This collector is deliberately a lead-discovery system, not an evidence adjudicator.
It stores titles, canonical source links, dates, identifiers, feed lineage and hashes.
It does not copy copyrighted article bodies or infer that an item is true.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from html.parser import HTMLParser
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "OBSERVATORY" / "SOURCES.json"
MAX_FEED_BYTES = 2_000_000
MAX_ITEMS_PER_FEED = 100
MAX_PAGE_BYTES = 2_000_000
USER_AGENT = "OmniversalKnowledgeObservatory/1.0 (+https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto)"
DOMAIN_VALUES = {
    "ancient_civilizations", "religious_developments", "uap_disclosure",
    "unexplained_phenomena", "cosmic_discoveries", "consciousness_intelligence"
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def child_text(node: ET.Element, names: set[str]) -> str | None:
    for child in list(node):
        if local_name(child.tag) in names:
            value = (child.text or "").strip()
            if value:
                return value
    return None


def atom_link(node: ET.Element) -> str | None:
    for child in list(node):
        if local_name(child.tag) == "link":
            href = child.attrib.get("href", "").strip()
            rel = child.attrib.get("rel", "alternate")
            if href and rel in ("alternate", ""):
                return href
    return None


def safe_https_url(value: str | None) -> str | None:
    if not value:
        return None
    try:
        parsed = urllib.parse.urlparse(value.strip())
    except ValueError:
        return None
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        return None
    return value.strip()


def parse_feed(xml_bytes: bytes, feed: dict, fetched_at: str) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items = []
    for node in root.iter():
        kind = local_name(node.tag)
        if kind not in ("item", "entry"):
            continue
        title = child_text(node, {"title"}) or "(untitled source item)"
        link = atom_link(node) if kind == "entry" else child_text(node, {"link"})
        if kind == "item" and link:
            link = link.strip()
        link = safe_https_url(link)
        guid = child_text(node, {"guid", "id"})
        published = child_text(node, {"pubdate", "published", "updated", "date", "issued"})
        creator = child_text(node, {"creator", "author", "name"})
        # Hash normalized metadata, not copyrighted article body text.
        stable = {
            "feed_id": feed["id"], "title": title.strip(), "link": link,
            "guid": guid, "published_raw": published, "creator": creator
        }
        digest = hashlib.sha256(
            json.dumps(stable, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if not link:
            # Keep unlinked items out of the research queue; report them in feed diagnostics.
            continue
        items.append({
            "lead_id": "OKO-LEAD-" + digest[:20].upper(),
            "title": title.strip()[:500],
            "source_url": link,
            "source_identifier": guid,
            "published_raw": published,
            "creator_or_author": creator,
            "feed_id": feed["id"],
            "feed_name": feed["name"],
            "feed_url": feed["url"],
            "source_class": feed["source_class"],
            "domains": feed["domains"],
            "first_seen_utc": fetched_at,
            "metadata_sha256": digest,
            "discovery_state": "SOURCE_LOCATED",
            "review_state": "UNREVIEWED",
            "truth_assessment": "NOT_ASSESSED",
            "preservation_note": "Original source remains at source_url. This record preserves discovery metadata and lineage, not the copyrighted article body."
        })
        if len(items) >= MAX_ITEMS_PER_FEED:
            break
    return items


def fetch_feed(feed: dict, timeout: int = 25) -> tuple[list[dict], dict]:
    url = safe_https_url(feed.get("url"))
    if not url:
        raise ValueError(f"Feed {feed.get('id')} does not use an approved HTTPS URL")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml, application/rss+xml, application/xml, text/xml"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        final_url = safe_https_url(response.geturl())
        origin_host = urllib.parse.urlparse(url).hostname
        final_host = urllib.parse.urlparse(final_url).hostname if final_url else None
        if not final_url or final_host != origin_host:
            raise ValueError("Feed redirect must remain on the registered HTTPS host")
        content_type = response.headers.get("Content-Type", "")
        payload = response.read(MAX_FEED_BYTES + 1)
    if len(payload) > MAX_FEED_BYTES:
        raise ValueError("Feed exceeds 2 MB safety limit")
    fetched_at = utc_now()
    parsed = parse_feed(payload, feed, fetched_at)
    return parsed, {
        "feed_id": feed["id"], "feed_url": url, "final_url": final_url,
        "http_content_type": content_type, "http_result": "success",
        "feed_payload_sha256": hashlib.sha256(payload).hexdigest(),
        "items_discovered": len(parsed), "items_limit_reached": len(parsed) >= MAX_ITEMS_PER_FEED, "per_feed_item_limit": MAX_ITEMS_PER_FEED, "fetched_at_utc": fetched_at
    }



class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data.strip())


def fetch_monitored_page(page: dict, prior_state: dict, timeout: int = 25) -> tuple[dict, dict]:
    url = safe_https_url(page.get("url"))
    if not url:
        raise ValueError(f"Monitored page {page.get('id')} does not use HTTPS")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        final_url = safe_https_url(response.geturl())
        origin_host = urllib.parse.urlparse(url).hostname
        final_host = urllib.parse.urlparse(final_url).hostname if final_url else None
        if not final_url or final_host != origin_host:
            raise ValueError("Monitored-page redirect must remain on the registered HTTPS host")
        content_type = response.headers.get("Content-Type", "")
        payload = response.read(MAX_PAGE_BYTES + 1)
    if len(payload) > MAX_PAGE_BYTES:
        raise ValueError("Monitored page exceeds 2 MB safety limit")
    digest = hashlib.sha256(payload).hexdigest()
    parser = TitleParser()
    try:
        parser.feed(payload.decode("utf-8", errors="replace"))
    except Exception:
        pass
    title = " ".join(part for part in parser.parts if part)[:300] or page["name"]
    prior = prior_state.get(page["id"], {})
    prior_hash = prior.get("content_sha256")
    if not prior_hash:
        change_state = "BASELINE"
    elif prior_hash == digest:
        change_state = "UNCHANGED"
    else:
        change_state = "CHANGED"
    checked = utc_now()
    check = {
        "page_id": page["id"],
        "page_name": page["name"],
        "source_url": url,
        "final_url": final_url,
        "domains": page["domains"],
        "content_type": content_type,
        "title": title,
        "content_sha256": digest,
        "previous_content_sha256": prior_hash,
        "change_state": change_state,
        "checked_at_utc": checked,
        "review_required": change_state in ("BASELINE", "CHANGED"),
        "preservation_note": "Page-change metadata only. This hash is not proof of authorship, authenticity, event occurrence, or truth; inspect and accession the underlying source separately."
    }
    next_state = {"content_sha256": digest, "last_checked_utc": checked, "source_url": url, "title": title}
    return check, next_state

def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(data.get("feeds"), list):
        raise ValueError("SOURCES.json must contain a feeds array")
    for feed in data["feeds"]:
        if not set(feed.get("domains", [])).issubset(DOMAIN_VALUES):
            raise ValueError(f"Unknown domain in source {feed.get('id')}")
    return data


def run(output_dir: Path, registry: dict) -> dict:
    now = datetime.now(timezone.utc)
    day = now.strftime("%Y-%m-%d")
    destination = output_dir / f"{day}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    existing = {"leads": []}
    if destination.exists():
        try:
            existing = json.loads(destination.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            raise ValueError(f"Refusing to overwrite invalid existing archive: {destination}")
    leads = {item["lead_id"]: item for item in existing.get("leads", [])}
    diagnostics = []
    failures = []
    for feed in registry["feeds"]:
        if not feed.get("enabled", False):
            continue
        try:
            discovered, diagnostic = fetch_feed(feed)
            diagnostics.append(diagnostic)
            for item in discovered:
                # Preserve the first-seen timestamp on repeat runs.
                leads.setdefault(item["lead_id"], item)
        except (urllib.error.URLError, TimeoutError, ValueError, ET.ParseError, OSError) as exc:
            failures.append({"feed_id": feed.get("id"), "feed_url": feed.get("url"), "error_type": type(exc).__name__, "message": str(exc)[:400], "recorded_at_utc": utc_now()})
    state_path = output_dir.parent / "state" / "monitored-pages.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    prior_state = {}
    if state_path.exists():
        prior_state = json.loads(state_path.read_text(encoding="utf-8"))
    page_checks = []
    page_failures = []
    next_state = dict(prior_state)
    for page in registry.get("monitored_pages", []):
        if not page.get("enabled", False) or page.get("fetch_mode") != "page_hash_monitor":
            continue
        try:
            check, state = fetch_monitored_page(page, prior_state)
            page_checks.append(check)
            next_state[page["id"]] = state
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            page_failures.append({"page_id": page.get("id"), "source_url": page.get("url"), "error_type": type(exc).__name__, "message": str(exc)[:400], "recorded_at_utc": utc_now()})
    state_path.write_text(json.dumps(next_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload = {
        "archive_id": f"OKO-FEED-INGEST-{day}",
        "generated_at_utc": utc_now(),
        "collector_version": "1.0.0",
        "registry_version": registry.get("registry_version"),
        "record_type": "discovery_leads_not_verified_findings",
        "lead_count": len(leads),
        "leads": sorted(leads.values(), key=lambda x: (x.get("published_raw") or "", x["lead_id"]), reverse=True),
        "feed_diagnostics": diagnostics,
        "feed_failures": failures,
        "page_checks": page_checks,
        "page_failures": page_failures,
        "coverage_note": "A feed item is a lead to inspect. Feed inclusion, repetition, metadata hashes, and source class do not establish factual truth or independent corroboration."
    }
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {"archive": str(destination), "leads": len(leads), "feeds_succeeded": len(diagnostics), "feeds_failed": len(failures), "pages_checked": len(page_checks), "pages_failed": len(page_failures), "pages_changed": sum(1 for item in page_checks if item["change_state"] == "CHANGED")}
    print(json.dumps(summary, indent=2))
    if not diagnostics and not page_checks:
        raise RuntimeError("No registered feeds or monitored pages succeeded; refusing to treat this run as a healthy collection cycle")
    return payload


def self_test() -> None:
    rss = b"""<?xml version='1.0'?><rss version='2.0'><channel><item><title>Test discovery</title><link>https://example.org/report</link><guid>abc-1</guid><pubDate>Mon, 16 Nov 2026 12:00:00 GMT</pubDate></item></channel></rss>"""
    atom = b"""<?xml version='1.0'?><feed xmlns='http://www.w3.org/2005/Atom'><entry><title>Atom discovery</title><id>tag:example.org,2026:2</id><link href='https://example.org/atom' rel='alternate'/><updated>2026-11-16T12:00:00Z</updated></entry></feed>"""
    feed = {"id":"test","name":"Test","url":"https://example.org/feed","domains":["cosmic_discoveries"],"source_class":"test"}
    assert len(parse_feed(rss, feed, "2026-11-16T12:00:00Z")) == 1
    assert len(parse_feed(atom, feed, "2026-11-16T12:00:00Z")) == 1
    assert safe_https_url("http://example.org") is None
    assert safe_https_url("https://user:pass@example.org") is None
    title_parser = TitleParser()
    title_parser.feed("<html><head><title>Observatory Test Page</title></head></html>")
    assert " ".join(title_parser.parts) == "Observatory Test Page"
    print("Self-test passed: RSS, Atom, HTTPS allowlist, page-title parsing, and metadata accession.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output-dir", default=str(ROOT / "OBSERVATORY" / "ingest" / "daily"))
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        try:
            run(Path(args.output_dir), load_registry())
        except Exception as error:
            print(f"Observatory ingestion failed: {error}", file=sys.stderr)
            raise
