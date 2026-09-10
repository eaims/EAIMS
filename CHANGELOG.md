# Changelog

## Unreleased — v1 input and review hardening

- Reject empty evidence collection times, ambiguous input types, non-finite numbers and duplicate YAML mapping keys before assessment.
- Add v1 fixture and result schemas while preserving legacy contracts and existing valid reference results.
- Reject duplicate review/finding identities; preserve the original ledger when applying resolutions.
- Resolve review schemas through the shared installed-package data root.
- Add optional `review summarize --fail-on-unmet` for automation with explicit exit semantics.
- Add a v1 quickstart and clearly label legacy questionnaire, scoring and browser resources.
- Extend regression coverage and installed-wheel review checks.

These changes do not alter the frozen normative specification or retroactively change the published 1.0.0 release evidence.

## 0.2.1 - Research Baseline

- Established the immutable baseline for the first peer-reviewed EAIMS paper
- Corrected v0.2 document-version headings and citation metadata
- Clarified normative evidence requirements versus executable validation
- Aligned scoring documentation with the equal-weight v0.2 reference implementation
- Added reproducible computational sensitivity-analysis materials for Paper 01
- Added a central publications index for the English and Persian EAIMS books and research outputs

## 0.2.0 — Executable Community Draft

- Added deterministic Python scoring, validation, CLI, Markdown/HTML reports, and nine automated tests
- Added input, result, and evidence-catalog schemas
- Added capability-specific evidence examples, counter-evidence, and freshness guidance
- Added three complete fictional machine-readable assessments
- Added assessor handbook, conformance classes, pilot and benchmark protocols, and independent conceptual crosswalk
- Added RFCs, decision records, reviewer program, sponsorship safeguards, and financial-transparency policy
- Added dependency-free browser interface and Docker deployment
- Renamed normative documents for v0.2 and strengthened explicit limitations

## 0.1.2 — Legal and IP Hardening

- Added license boundaries and complete license texts
- Added DCO, contributor rights, provenance, IP, trademark, disclaimer, authorship, and third-party notices
- Defined Elias Naserkhaki as founder, initial author, and founding steward of eaims.org

## 0.1.0 — Initial Community Draft

- Defined six levels, nine dimensions, 27 capabilities, scoring, questionnaires, governance, and examples
