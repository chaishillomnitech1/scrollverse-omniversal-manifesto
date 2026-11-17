# THE OMNIVERSAL KNOWLEDGE OBSERVATORY

**Six domains. One living archive. No premature dismissal.**

The Observatory is a research, provenance, and preservation framework for investigating humanity's questions across ancient civilizations, religious developments, UAPs, unexplained phenomena, cosmic discoveries, and consciousness/intelligence.

It extends the ScrollVerse Omniversal Manifesto archive. It does not replace existing repositories, pyramids, raw transmissions, or source artifacts. It links them while preserving their original locations and provenance.

## Governing principle

**Curiosity without prejudice. Investigation without premature conclusions. Knowledge without artificial boundaries.**

The Observatory is open to unusual, unfamiliar, minority, and emerging questions. Openness is not automatic belief: every claim retains its source, context, evidence state, competing explanations, and unresolved questions.

## Six research domains

1. **Ancient civilizations and knowledge traditions** — Egyptian, Sumerian, Mesopotamian, Indus Valley, Indigenous, African, Mesoamerican, Hermetic, and other traditions. Distinguish primary texts, archaeology, oral histories, later translations, modern esoteric interpretations, and unsupported attributions.
2. **Religious developments and spiritual movements** — Christianity, Islam, Judaism, Hinduism, Buddhism, Indigenous traditions, and emerging movements. Preserve each tradition's own account respectfully; do not rank traditions or present theological claims as laboratory findings.
3. **UAP disclosure** — government records, military reports, scientific investigations, sensor data, witness accounts, and official reviews. “Unidentified” is a status, not an explanation.
4. **Unexplained phenomena** — atmospheric and astronomical anomalies, paranormal reports, cryptids, unusual natural events, and historical accounts. Record ordinary explanations considered without treating an untested explanation as settled.
5. **Cosmic discoveries** — astronomy, astrophysics, planetary science, astrobiology, exoplanets, biosignatures, and relevant mission data. Distinguish candidate signals from confirmed detections.
6. **Consciousness and intelligence** — neuroscience, cognitive science, philosophy of mind, AI research, animal cognition, first-person reports, and human experience. Preserve testimony without treating testimony alone as proof of a proposed mechanism.

Cross-domain connections are welcome, but a connection is initially a **research lead**, not proof that two phenomena share a cause.

## Required discovery record

Every accession records:

1. Original evidence and an immutable pointer or preserved copy where rights permit.
2. Historical context.
3. Geographic origin and location precision.
4. Witness, author, institution, instrument, or reporting organization.
5. Independent corroboration and its independence.
6. Competing explanations and tests performed.
7. Unresolved questions and missing evidence.
8. Cross-disciplinary connections.
9. A dated history of how interpretations and evidence states change.

The machine-readable contract is in [DISCOVERY-RECORD.schema.json](./DISCOVERY-RECORD.schema.json). The research rules are in [RESEARCH-AND-EVIDENCE-PROTOCOL.md](./RESEARCH-AND-EVIDENCE-PROTOCOL.md).

## Preserve originals separately

- Raw testimony, source documents, photographs, recordings, datasets, and original wording are never silently rewritten.
- Curated summaries, translations, annotations, and hypotheses are separate, attributed layers.
- Corrections append a dated revision; they do not erase the earlier record.
- Hashes identify captured bytes; a hash alone does not establish authenticity, date, authorship, or truth.
- Respect copyright, privacy, consent, cultural protocols, and restricted Indigenous knowledge. Do not republish protected or sacred material without permission.

## Evidence states

Use explicit labels rather than a single vague confidence score:

- `UNASSESSED` — accessioned, not yet reviewed.
- `SOURCE_LOCATED` — source identified; contents or provenance still need review.
- `REPORTED` — an account exists; truth of the event is not established.
- `CORROBORATED` — independent evidence supports one or more details.
- `SUPPORTED` — multiple relevant lines of evidence support a specific claim.
- `ESTABLISHED` — strong, convergent evidence under appropriate disciplinary standards.
- `CONTESTED` — credible sources or interpretations materially disagree.
- `UNRESOLVED` — evidence is insufficient to decide among explanations.
- `NOT_SUPPORTED` — the available evidence does not support the stated claim.
- `RETRACTED_OR_CORRECTED` — a source or prior interpretation has been withdrawn or corrected; preserve the history.

These labels apply to individual claims, not whole cultures, religions, witnesses, or fields.

## Initial operating cycle

`DISCOVER → CAPTURE → PRESERVE → CONTEXTUALIZE → CORROBORATE → COMPARE → CONNECT → REVIEW → UPDATE`

A discovery is not complete merely because it is exciting, published, or widely repeated. It becomes a durable Observatory record when its source trail and limitations can be inspected.

## Automated source discovery

See [INGEST-RUN-LOG.md](./INGEST-RUN-LOG.md) for dated workflow evidence, collection counts, feed failures, and corrective actions.

The scheduled collector and its human-review process are documented in [AUTOMATION-AND-OPERATIONS.md](./AUTOMATION-AND-OPERATIONS.md). The initial allowlisted source registry is [SOURCES.json](./SOURCES.json). Incoming feed items are source leads only and are never automatically promoted to verified findings. The machine-readable lead contract is [INGEST-LEAD.schema.json](./INGEST-LEAD.schema.json). Regression tests run on pull requests; daily feed records are published to a persistent review branch rather than silently modifying the canonical archive.

## Live source-review stream

Daily automated source-lead accessions are preserved on the separate [Observatory ingestion review branch](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/tree/automation/observatory-daily-ingest). Each lead remains unreviewed and unverified until a human curator inspects the underlying source.

## Existing ScrollVerse artifacts

See [PYRAMID-AND-ARCHIVE-CROSSWALK.md](./PYRAMID-AND-ARCHIVE-CROSSWALK.md) for a first-pass inventory of existing digital-pyramid and archive references. Existing artifacts remain in their original repositories.

## Current status

**COLLECTOR OPERATIONAL; ATLAS UNDER REVIEW.** The scheduled collector and institutional page-hash monitor are implemented in `.github/workflows/observatory-ingest.yml` and `OBSERVATORY/scripts/ingest_feeds.py`. The latest recorded successful run is 2026-11-16, GitHub Actions run [#43979168083](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/actions/runs/43979168083): 11 successful feeds, 496 source leads, zero feed failures, four feeds at the 100-item cap, two changed page hashes, and zero page-monitor failures. These are discovery leads and review flags, not verified findings. The Atlas interface is proposed in [PR #9](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/pull/9); it is not merged or deployed. The public dashboard, curated discovery library, complete global source network, and scientific review board remain future work.

**Archive doctrine:** Nothing erased. Nothing inflated. Nothing hidden. Everything contextualized.
