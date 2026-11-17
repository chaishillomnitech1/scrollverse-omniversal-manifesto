# Observatory Atlas — v1

A static, dependency-free research interface for the Omniversal Knowledge Observatory.

## Data source

The Atlas discovers the newest dated JSON accession in the public automation/observatory-daily-ingest branch using the GitHub Contents API, then loads that accession's raw JSON. It does not copy daily data into this repository or silently substitute an older snapshot when the live source cannot be reached.

## Current capabilities

- Six-domain filtering and per-domain lead counts.
- Full-text search over title, author, feed, source URL, source class, and lead ID.
- Source-class and publication-year filters.
- Publication-date sorting and paginated results.
- Source lineage, first-seen date, lead ID, and metadata SHA-256 display.
- Feed and institutional page-monitor diagnostics.
- Explicit SOURCE_LOCATED, UNREVIEWED, and NOT_ASSESSED status labels.

## Evidence and scope boundaries

The Atlas displays source leads, not verified discoveries. It does not infer truth, corroboration, geographic origin, or causal relationships. The current feed-lead schema does not contain verified geographic coordinates or claim-level competing explanations. Those belong in separately curated DISCOVERY-RECORD.schema.json accessions after human review.

The UI does not download copyrighted article bodies or media. Original sources open at their canonical HTTPS URLs. No source lead is promoted automatically.

## Preview and hosting

Open index.html in a browser with network access. The GitHub Contents API and raw GitHub URLs must be reachable from the browser. This commit does not deploy a public website or configure GitHub Pages; hosting is a separate verified step.

## Next engineering milestones

1. Add curated discovery-record indexing and claim-level evidence review.
2. Add a map only when records contain sourced geographic coordinates and precision.
3. Add a historical timeline based on normalized, source-backed dates.
4. Add a permissions-aware original-source preservation workflow.
5. Integrate the Atlas into an approved ScrollVerse route after a deployment target and origin policy are selected.
