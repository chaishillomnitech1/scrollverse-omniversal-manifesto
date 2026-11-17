# Observatory Ingestion Run Log

This is an append-only operational history. A successful collector run means the software completed its registered fetch and archive steps; it does not mean the discoveries are verified.

## 2026-11-16 — initial RSS/Atom collection

- Workflow run: [#43978377195](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/actions/runs/43978377195)
- Outcome: FAILED at publication handoff, after collection completed.
- Collection: 396 feed-lead records; 10 feeds succeeded; NASA Science feed failed XML parsing.
- Cause: repository Actions token was not permitted to create pull requests. The collector had already committed a review branch, but the job ended failed at PR creation.
- Correction: replaced PR creation with a persistent review branch; no default-branch protection was bypassed.

## 2026-11-16 — persistent branch publication correction

- Workflow run: [#43978635893](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/actions/runs/43978635893)
- Outcome: FAILED during review-branch preparation.
- Cause: Git author identity was configured after the branch merge, not before it.
- Correction: configure the bot identity before branch checkout/merge; add .gitignore and remove generated Python bytecode.

## 2026-11-16 — first successful persistent daily archive

- Workflow run: [#43978752883](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/actions/runs/43978752883)
- Outcome: SUCCESS.
- Collection: 396 feed-lead records; 10 feeds succeeded; zero feed failures.
- Three feeds reached the 100-item per-feed limit. This is a minimum observed count, not an exhaustive total.
- Persistent review branch: [automation/observatory-daily-ingest](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/tree/automation/observatory-daily-ingest).

## 2026-11-16 — institutional page-monitor baseline

- Workflow run: [#43979032570](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/actions/runs/43979032570)
- Outcome: SUCCESS.
- Feed collection: 396 leads; 10 feeds succeeded; zero feed failures.
- Page checks: NASA UAP and Archaeology Magazine baseline hashes recorded.
- AARO and Smithsonian NMAI returned HTTP 403 from the GitHub Actions runner; those references were moved to human-review-only mode rather than repeatedly retried.

## 2026-11-16 — current expanded collection

- Workflow run: [#43979168083](https://github.com/chaishillomnitech1/scrollverse-omniversal-manifesto/actions/runs/43979168083)
- Outcome: SUCCESS.
- Feed collection: 496 feed-lead records; 11 feeds succeeded; zero feed failures.
- Four feeds reached the 100-item per-feed limit: Pew Religion, arXiv AI, arXiv Quantum Physics, and USGS earthquakes.
- Page checks: NASA UAP and Archaeology Magazine both returned CHANGED hash states, which creates a human-review flag. A changed page hash can reflect dynamic page content; it is not proof that a specific report or finding changed.
- Page failures: zero.
- Review-branch commit: 609f1d5.

## Scope boundary

The automation now covers all six Observatory domain labels through registered research feeds and official page monitoring, but coverage is uneven. UAP monitoring currently includes NASA's official UAP page; AARO is human-review-only due runner-side HTTP 403. Indigenous community knowledge and oral histories are not automatically harvested. Paranormal and cryptid reports are not yet covered by a curated, rights-aware source network. Those gaps remain explicit work items.

No feed lead or page hash is automatically promoted to corroborated, supported, or established evidence.
