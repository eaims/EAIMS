# EAIMS 1.0 — Independent Reviewer Executive Brief

## Purpose

EAIMS is an evidence-grounded and executable enterprise AI maturity framework intended to assess and improve organizational AI capability while explicitly addressing value realization, evidence, autonomy, human accountability, and operational risk.

## Canonical architecture

- 8 dimensions
- 30 capabilities
- 5 capability-specific maturity levels
- 150 maturity anchors
- 206 normative/cross-cutting requirements
- evidence classes E1–E4 and confidence C0–C4
- impact I0–I4, autonomy A0–A5, and Human Accountability Boundary states
- G0–G3 gate families
- Full, Partial, and Targeted assessment modes
- explainable capability eligibility rather than questionnaire averaging

## Major v1 redesign themes

EAIMS 1.0 adds or materially strengthens:

- model/system sourcing and external provider-change exposure;
- capability-specific advanced maturity anchors;
- preservation of higher-order evidence when prerequisites are missing;
- evidence provenance, cutoff, invalidation, conflict, and retention semantics;
- explicit partial-scope and applicability rules;
- Human Accountability Boundaries and Human Reserved decisions;
- agentic autonomy, permission envelopes, action/delegation limits, and suspension;
- federated-enterprise concepts and pilot-to-scale/value governance;
- deterministic schemas, executable rules, test coverage, and synthetic reference implementations.

## Executable state of this freeze candidate

The package includes machine-verification rules for critical MV1/MV2 requirements, assessor protocols for critical MV3/MV4 requirements, capability-specific anchor eligibility for all 150 anchors, risk/gate logic, selected HAB/agent controls, Assessment Quality, multi-assessor workflow, three synthetic end-to-end reference implementations, packaging contracts, and hosted-CI definitions.

## Validation boundary

Synthetic tests demonstrate internal consistency and designed behavior. They do not prove that EAIMS measurements correspond to real-world organizational performance, that independent assessors agree in practice, or that thresholds are empirically calibrated.

## Enterprise design inputs

The redesign is informed by feasibility testing, synthetic reference implementation work, and anonymized pilot-readiness discussions spanning large regional e-commerce, diversified enterprise-group, and corporate innovation/venture contexts. These are design inputs, not claimed deployments or validations.

## Requested reviewer posture

Please review adversarially. The preferred output is not praise; it is a list of specific claims, requirements, anchors, rules, gates, or implementation behaviors that should change before RC.
