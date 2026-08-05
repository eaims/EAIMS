# EAIMS v0.2 Conformance

Conformance claims MUST name the EAIMS version, class, scope, assessment mode, modifications, and unresolved validation errors.

## Classes

| Class | Minimum requirements | Permitted claim |
|---|---|---|
| Data Compatible | Valid published identifiers and schemas | “EAIMS v0.2 Data Compatible” |
| Assessment Compatible | All 27 capabilities, published anchors, scoring bands, and critical gates | “EAIMS v0.2 Assessment Compatible” |
| Evidence-Based Assessment | Assessment Compatible plus evidence IDs, confidence, scope, exclusions, and limitations | “EAIMS v0.2 Evidence-Based Assessment” |
| Independently Reviewed | Evidence-Based plus reviewer independence statement, conflicts, review record, and reviewer identity | “Independently reviewed using EAIMS v0.2” |
| Modified Implementation | All modifications and scoring effects disclosed | “Based on EAIMS v0.2; modified” |

No class constitutes EAIMS certification, accreditation, ISO conformity, legal compliance, or project endorsement.

## Prohibited claims

- “EAIMS Certified” or “Official EAIMS Assessor”
- “Compliant with ISO/IEC 42001” based only on EAIMS
- “Independently reviewed” when the reviewer reports into, benefits from, or designed the assessed operating unit without disclosure
- Unmodified conformance when gates, anchors, weights, dimensions, or scoring bands changed

## Machine verification

The reference CLI validates Data and Assessment Compatible inputs. Governance and independence facts require documented human review; software cannot verify them automatically.
