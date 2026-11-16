# Observatory Automation and Operations

## What is automated now

The GitHub Actions workflow `.github/workflows/observatory-ingest.yml` runs daily at 11:17 UTC and can also be started manually with `workflow_dispatch`.

It:
1. Checks out the archive.
2. Runs collector self-tests and regression tests.
3. Loads only the explicitly registered HTTPS sources in `SOURCES.json`.
4. Fetches RSS 2.0 and Atom feeds with a 2 MB response limit and 25-second timeout.
5. Records titles, canonical HTTPS links, publication metadata, author when available, source/feed lineage, first-seen time, and a deterministic metadata SHA-256.
6. Deduplicates repeated feed entries and preserves their first-seen timestamp within each daily accession.
7. Records feed failures rather than silently omitting them.
8. Opens or updates a pull request for human review; it does not push unreviewed source records directly to main.

## What the collector does not do

- It does not scrape arbitrary websites or search engines.
- It does not download or republish full copyrighted articles, images, video, or PDFs.
- It does not infer the truth of a claim from feed presence, popularity, source class, or a hash.
- It does not treat repeated articles derived from one press release as independent corroboration.
- It does not automatically create a completed discovery record or change an evidence state to corroborated, supported, or established.
- It does not currently fetch monitored pages listed with `manual_review_only`.
- It does not claim full six-domain coverage. UAP official pages, Indigenous/community knowledge, cryptid/paranormal reports, and local oral histories require careful source onboarding, consent, and human review.

## Daily archive layout

`OBSERVATORY/ingest/daily/YYYY-MM-DD.json`

Each file contains:
- `leads`: source metadata records with `SOURCE_LOCATED`, `UNREVIEWED`, and `NOT_ASSESSED` states;
- `feed_diagnostics`: successful feed fetch metadata and payload hashes;
- `feed_failures`: errors, timestamps, and source IDs;
- explicit scope notes.

The original report remains at its canonical source URL. The Observatory accession preserves its bibliographic trail and metadata. Where a primary source permits lawful preservation of original bytes, a human curator may add a separately hashed immutable source artifact with rights and custody details.

## Human review gate

Every incoming item must be reviewed before promotion into a full `DISCOVERY-RECORD.schema.json` accession. Reviewers should:
- confirm the canonical source and original publication date;
- identify the original witness, author, instrument, institution, or community custodian;
- distinguish primary evidence from secondary reporting;
- locate genuinely independent corroboration;
- record plausible competing explanations;
- protect personal, sacred, Indigenous, and sensitive-location information;
- preserve prior assessments in a dated revision history.

## Extending the source network

Add a feed only after checking that:
- the endpoint is HTTPS and controlled by the named publisher/institution;
- its format is RSS 2.0 or Atom;
- its terms and rate limits permit automated feed access;
- the feed's domain mapping is justified;
- the feed is a discovery channel, not an endorsement of every item.

Use `enabled: false` for untested feeds. Do not register scraped mirrors as official sources. Respect arXiv's feed/API terms and each publisher's terms.

## Operational status

The workflow and collector are committed by pull request in this engineering phase. Runtime success is not claimed until the first scheduled or manually dispatched Actions run completes successfully. Source feeds can fail independently; inspect the daily diagnostics and Actions logs.
