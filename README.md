# EAIMS — Enterprise AI Maturity Standard

> An open, vendor-neutral, evidence-based, and executable specification for enterprise AI maturity.

**Version:** 0.2.1 Research Baseline  
**Status:** Public Review and Pilot Preparation  
**Documentation and assessment content:** CC BY 4.0  
**Code, workflows, and schemas:** Apache-2.0

## What EAIMS adds

EAIMS combines an enterprise operating model with reproducible assessment infrastructure:

- 9 dimensions, 27 capabilities, and 162 observable maturity anchors
- Capability-specific evidence examples, counter-evidence, and freshness guidance
- Confidence reporting and critical gates that prevent unsafe averaging
- Deterministic Python scoring engine, CLI, schemas, automated tests, and reports
- Three complete fictional assessment fixtures
- Independent conceptual crosswalk to major public AI-governance themes
- Conformance classes, assessor handbook, pilot protocol, and benchmark protocol
- Dependency-free browser reference interface and local Docker deployment

EAIMS supports predictive ML, generative AI, RAG, agents, third-party services, and cloud, hybrid, sovereign, or on-premises architectures. It does not prescribe a vendor, model, platform, or consulting provider.

## Project status and stewardship

EAIMS was founded and initially authored by **Elias Naserkhaki**, registrant and founding steward of **eaims.org**. Founder attribution records project origin and stewardship; it does not create accredited standards authority or override published governance.

EAIMS is not an ISO, IEC, ANSI, governmental, or accredited standard. It does not provide certification, legal compliance, safety assurance, or endorsement. See [Disclaimer](DISCLAIMER.md), [IP Policy](IP_POLICY.md), [Origin](ORIGIN.md), and [Trademark Policy](TRADEMARK.md).

## Quick start

Run the reference engine without third-party runtime dependencies:

```bash
python -m pip install -e .
eaims validate examples/fictional-manufacturer.assessment.json
eaims score examples/fictional-manufacturer.assessment.json
eaims report examples/fictional-manufacturer.assessment.json --format html --output report.html
```

Run the browser interface:

```bash
python -m http.server 8080
# open http://localhost:8080/site/
```

Or use Docker:

```bash
docker build -t eaims .
docker run --rm -p 8080:80 eaims
```

## Assessment flow

1. Define scope and evidence handling with the [Assessor Handbook](docs/Assessor-Handbook.md).
2. Complete the [questionnaire](assessment/questionnaire.md) using the [evidence catalog](assessment/evidence-catalog.json).
3. Validate and score the assessment with the CLI.
4. Apply the [Conformance](docs/Conformance.md) claim appropriate to the evidence and review process.
5. Produce findings and a roadmap; never present the result as certification.

## Key documentation

| Need | Resource |
|---|---|
| Normative foundation | [EAIMS Standard](docs/EAIMS-Standard-v0.2.md) and [Capability Matrix](docs/Capability-Matrix-v0.2.md) |
| Scoring | [Scoring Methodology](assessment/scoring-methodology.md) |
| Evidence | [Evidence Catalog](assessment/evidence-catalog.json) |
| Facilitation | [Assessor Handbook](docs/Assessor-Handbook.md) |
| Implementation claims | [Conformance](docs/Conformance.md) |
| Research pilots | [Pilot Protocol](docs/Pilot-Protocol.md) |
| Future benchmarking | [Benchmark Protocol](docs/Benchmark-Protocol.md) |
| External frameworks | [Independent Conceptual Crosswalk](docs/Standards-Crosswalk.md) |
| Change process | [RFCs](rfcs/README.md) and [Decisions](decisions/0001-six-level-scale.md) |

## Validation status

v0.2 is executable and internally tested. It has **not yet** completed independent multi-organization validation, inter-rater reliability research, academic peer review, or representative benchmarking. The repository publishes protocols for generating that evidence honestly.

## Contributing and support

Contributions require DCO sign-off and rights disclosure. See [Contributing](CONTRIBUTING.md), [Reviewer Program](REVIEWERS.md), [Sponsorship Policy](SPONSORSHIP.md), and [Financial Transparency](FINANCIAL_TRANSPARENCY.md). Funding cannot buy changes, favorable scores, certification, endorsement, or governance control.

## Publications

Books and research outputs: [EAIMS Publications](publications/README.md)

## Project website

https://eaims.org
