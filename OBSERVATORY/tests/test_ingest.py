import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ingest_feeds.py"
SPEC = importlib.util.spec_from_file_location("ingest_feeds", SCRIPT)
ingest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ingest)


class FeedIngestionTests(unittest.TestCase):
    def setUp(self):
        self.feed = {
            "id": "test-feed", "name": "Test Feed",
            "url": "https://example.org/feed",
            "domains": ["cosmic_discoveries"], "source_class": "test"
        }

    def test_rss_item_becomes_source_lead(self):
        xml = b"<rss><channel><item><title>Signal report</title><link>https://example.org/item/1</link><guid>one</guid></item></channel></rss>"
        items = ingest.parse_feed(xml, self.feed, "2026-11-16T00:00:00Z")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["discovery_state"], "SOURCE_LOCATED")
        self.assertEqual(items[0]["truth_assessment"], "NOT_ASSESSED")

    def test_atom_item_becomes_source_lead(self):
        xml = b"<feed xmlns='http://www.w3.org/2005/Atom'><entry><title>Paper</title><id>paper-1</id><link href='https://example.org/paper'/></entry></feed>"
        self.assertEqual(len(ingest.parse_feed(xml, self.feed, "2026-11-16T00:00:00Z")), 1)

    def test_rejects_non_https_source(self):
        xml = b"<rss><channel><item><title>Bad</title><link>http://example.org/item</link></item></channel></rss>"
        self.assertEqual(ingest.parse_feed(xml, self.feed, "2026-11-16T00:00:00Z"), [])

    def test_deterministic_metadata_hash(self):
        xml = b"<rss><channel><item><title>Same</title><link>https://example.org/item</link><guid>x</guid></item></channel></rss>"
        a = ingest.parse_feed(xml, self.feed, "2026-11-16T00:00:00Z")[0]
        b = ingest.parse_feed(xml, self.feed, "2026-11-16T00:01:00Z")[0]
        self.assertEqual(a["metadata_sha256"], b["metadata_sha256"])

    def test_self_test(self):
        ingest.self_test()


if __name__ == "__main__":
    unittest.main()
