# EAIMS Approved Implementations Registry

This registry lists products and services that the EAIMS project has reviewed for a defined implementation scope and a named EAIMS release.

Registry approval means only that the reviewed implementation satisfied the published listing criteria at the recorded review date. It is not certification, accreditation, legal or regulatory approval, security assurance, validation of a customer's assessment result, or a guarantee of continued conformance.

## Listing criteria

An approved listing MUST:

1. identify the implemented EAIMS release and conformance class;
2. preserve the applicable capability identifiers, maturity anchors, scoring bands, and critical gates, or disclose every material modification;
3. distinguish maturity scores from evidence confidence and review status where the claimed class requires it;
4. provide clear EAIMS attribution and applicable license notices;
5. avoid prohibited certification, accreditation, partnership, and regulatory-compliance claims;
6. document the product scope, material limitations, and review evidence;
7. complete maintainer review, including conflict-of-interest disclosure; and
8. accept re-review after a material product or EAIMS release change.

The registry status applies only to the version and scope shown below. Implementers remain responsible for security, privacy, availability, local law, customer communications, and the accuracy of their own software and services.

## Status definitions

| Status | Meaning |
|---|---|
| Approved | The named version and scope passed project review against the listing criteria. |
| Provisional | Initial review passed, but one or more stated follow-up items remain open. |
| Suspended | The listing is temporarily inactive pending clarification or remediation. |
| Withdrawn | The implementation is no longer listed as approved. |

## Registered implementations

### HM-0001 — Hoosh Madar

| Field | Record |
|---|---|
| Product | [Hoosh Madar](https://hooshmadar.ir/) |
| Provider | Hoosh Madar |
| Registry status | **Approved** |
| Listed first | 2026-08-12 |
| EAIMS release | EAIMS v0.2.1 Research Baseline |
| Conformance claim | EAIMS v0.2 Assessment Compatible; Persian localized and modified implementation |
| Approved scope | Self-assessment workflow, 27-capability questionnaire, six-level maturity anchors, critical-gate scoring, management report, and transformation-roadmap workflow |
| Delivery model | Independently developed PHP/MySQL web application for self-hosted deployment |
| Material modifications | Persian localization, user-facing diagnostic wording, level-specific workflows, product UX, reporting, and roadmap management |
| Limitations | Listing does not approve hosting configurations, customer data handling, assessment evidence, individual results, assessor independence, or legal and regulatory compliance |
| Re-review trigger | Material scoring change, removal of required capabilities or gates, incompatible EAIMS upgrade, or a substantive change to the approved scope |

#### Review and conflict disclosure

Hoosh Madar is the first implementation entered in this registry. Elias Naserkhaki is the founding steward of EAIMS and is also associated with Hoosh Madar. This related-party relationship creates an actual conflict of interest and is disclosed here.

The initial listing is a maintainer review against the criteria above, not an independent third-party audit. A future independent registry reviewer SHOULD re-evaluate this entry when the EAIMS reviewer program is operational. Until then, Hoosh Madar MUST describe itself as an “EAIMS approved implementation” only with a direct link to this record and MUST NOT use “EAIMS Certified,” “official EAIMS assessor,” or equivalent certification language.

## Applying for a listing

Open a repository issue or pull request containing:

- legal or public provider name and product URL;
- product version and implemented EAIMS release;
- requested conformance class and scope;
- a modification and limitations statement;
- reproducible review evidence or a private-review plan for sensitive material;
- security and privacy contact details; and
- all relevant commercial and reviewer conflicts.

Approval, suspension, and withdrawal decisions MUST be recorded through the public repository history. Payment, sponsorship, or commercial relationships cannot purchase or guarantee a listing.

## Reporting a concern

Report inaccurate claims or suspected loss of conformance through the repository issue tracker. Report security vulnerabilities using [SECURITY.md](../SECURITY.md), not a public issue.

See also [EAIMS Conformance](Conformance.md), [Governance](../GOVERNANCE.md), and the [Name and Mark Policy](../TRADEMARK.md).
