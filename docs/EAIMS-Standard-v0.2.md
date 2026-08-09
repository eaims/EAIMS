# EAIMS Standard v0.2

## 1. Purpose

The Enterprise AI Maturity Standard (EAIMS) defines a consistent, evidence-based method for evaluating an organization's capability to select, build, deploy, govern, operate, adopt, and continuously improve artificial intelligence systems and AI-enabled ways of working.

EAIMS is intended to support organizational assessment, transformation planning, capability development, and repeatable reassessment.

## 2. Scope

EAIMS applies to organizations using or planning to use:

* Predictive machine learning
* Generative AI and large language models
* Retrieval-augmented generation
* AI agents and workflow automation
* AI-enabled products and services
* Third-party AI services
* On-premises, cloud, and hybrid AI platforms

EAIMS evaluates organizational capability and maturity. It does not certify the safety, legality, regulatory compliance, performance, security, ethical acceptability, or suitability of any specific AI model, system, product, or service.

The framework is vendor-neutral and may be applied across different technology stacks, deployment models, sectors, and organizational contexts.

## 3. Normative Language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** indicate requirement strength within this standard.

* **MUST**: mandatory for conformance
* **MUST NOT**: prohibited for conformance
* **SHOULD**: recommended unless a documented and justified exception exists
* **SHOULD NOT**: generally discouraged unless a documented and justified exception exists
* **MAY**: optional

## 4. Principles

### 4.1 Business Alignment

AI initiatives MUST connect to identifiable organizational objectives and SHOULD be evaluated against measurable outcomes where practicable.

### 4.2 Evidence Over Perception

Capability scores MUST be supported by observable evidence.

Assessors MUST assign the highest maturity level that can be defensibly supported by the available evidence. A higher maturity level MUST NOT be assigned solely on the basis of intention, aspiration, informal perception, or undocumented claims.

Where the evidence does not support a higher maturity anchor, the lower defensible level MUST be used.

### 4.3 Responsible AI by Design

Security, privacy, safety, fairness, transparency, accountability, human oversight, and other applicable responsible-AI considerations SHOULD be integrated throughout the AI lifecycle in proportion to organizational context and risk.

### 4.4 Vendor Neutrality

EAIMS MUST NOT require a specific vendor, model provider, technology product, cloud provider, or implementation architecture.

### 4.5 Context Sensitivity

Assessments SHOULD account for organizational size, sector, regulatory environment, operating model, risk exposure, technology landscape, and strategic ambition.

Context MAY influence target maturity and implementation priorities, but MUST NOT be used to misrepresent the evidence supporting the current-state score.

### 4.6 Continuous Improvement

Maturity is not a one-time score.

Organizations SHOULD reassess periodically and after material changes to strategy, operating models, AI platforms, governance arrangements, risk exposure, or the AI system portfolio.

### 4.7 Transparency and Traceability

Assessment results SHOULD be traceable from reported maturity levels to capability scores and supporting evidence.

Material assumptions, exclusions, not-applicable decisions, and assessment limitations MUST be documented.

## 5. Maturity Levels

EAIMS defines six maturity levels from Level 0 through Level 5.

### Level 0 — AI Unaware

AI capabilities, risks, ownership, and operating practices are absent, unrecognized, or materially unmanaged.

### Level 1 — AI Exploring

Individuals or teams conduct experiments or isolated initiatives. Outcomes are inconsistent, organizational coordination is limited, and controls are predominantly informal.

### Level 2 — AI Enabled

Selected use cases operate repeatably within departments or defined organizational areas. Initial architecture, governance, data, delivery, and operating practices exist.

### Level 3 — AI Integrated

Enterprise standards, platforms, governance, lifecycle management, cross-functional ownership, and repeatable operating practices are established across material parts of the organization.

### Level 4 — AI Optimized

AI is managed as an organizational portfolio. Performance, risk, cost, adoption, operational effectiveness, and business value are systematically measured and continuously improved.

### Level 5 — AI Native

AI is embedded in the operating model, products, services, decision systems, workflows, and organizational learning loops. Advanced AI capability is broadly supported by mature governance, engineering, operational, data, and organizational practices.

Level 5 MUST NOT be interpreted as a requirement or universally desirable target for every organization. Appropriate target maturity depends on organizational strategy, economics, risk, regulation, and operating context.

## 6. Assessment Dimensions

EAIMS assesses enterprise AI maturity across nine dimensions:

1. Strategy and Leadership
2. Value and Portfolio Management
3. Data and Knowledge Readiness
4. AI Engineering and Architecture
5. Infrastructure and Platforms
6. MLOps, LLMOps, and Lifecycle Operations
7. Governance, Risk, Security, and Responsible AI
8. Organization, Talent, and Culture
9. Adoption, Process Transformation, and Change

The dimensions are decomposed into capabilities defined in the EAIMS Capability Matrix.

Capability maturity anchors provide the observable assessment states used to determine capability scores.

## 7. Assessment Requirements

A conforming EAIMS assessment MUST:

* Define the organizational scope and assessment boundary
* Identify accountable assessment owners
* Evaluate all in-scope capabilities
* Record evidence supporting capability judgments
* Record the maturity score assigned to each capability
* Record assessment confidence where required by the published assessment method
* Distinguish current-state maturity from target-state ambition
* Apply the published EAIMS scoring methodology
* Record material exceptions, assumptions, exclusions, and not-applicable decisions
* Apply published critical-dimension constraints
* Avoid allowing aggregate scoring to conceal material weaknesses in designated critical dimensions
* Preserve sufficient traceability between evidence, capability judgments, dimension results, and the final maturity result
* Produce or support prioritized improvement actions

Missing information MUST NOT automatically be interpreted as a zero score.

A capability MAY be classified as not applicable only where the exclusion is justified and documented in accordance with the published scoring methodology.

### 7.1 Evidence Requirements

All capability scores are normatively required to be supported by evidence.

Evidence MAY include, where appropriate:

* Approved policies and standards
* Governance records
* Architecture documentation
* Technical configurations
* System or platform records
* Monitoring outputs
* Model or application documentation
* Risk assessments
* Audit records
* Portfolio records
* Financial or performance measures
* Training or workforce records
* Process documentation
* Incident and change records
* Interviews corroborated by other evidence
* Other verifiable organizational artifacts

Evidence SHOULD be sufficiently relevant, reliable, and current for the capability being assessed.

The absence of strong evidence SHOULD reduce the defensible maturity level or the confidence assigned to the assessment judgment, as applicable.

> **Evidence validation note.** All capability scores are normatively required to be evidence-supported. The reference validator's minimum machine-checkable requirement for one `evidence_id` at Levels 3–5 is an executable validation floor and does not waive the evidence requirement for Levels 0–2.

### 7.2 Assessment Confidence

Assessment confidence represents the strength of the evidentiary basis supporting a capability judgment.

Confidence MUST be reported separately from maturity and MUST NOT be used to increase a capability maturity score.

The published scoring methodology defines the applicable confidence classifications and any rules affecting provisional assessment status.

A provisional assessment status indicates limitations in the evidentiary basis of the assessment. It does not automatically change the underlying maturity scores.

### 7.3 Scoring and Aggregation

Capability, dimension, and enterprise-level results MUST be calculated using the published EAIMS scoring methodology applicable to the assessed EAIMS version.

EAIMS v0.2 uses equal weighting across in-scope capabilities and scored dimensions in the executable reference scoring model.

Alternative weighting schemes are experimental in EAIMS v0.2 and are not part of executable conformance unless explicitly defined by a future EAIMS specification.

Calculations SHOULD retain full precision until display or reporting.

### 7.4 Critical-Dimension Constraints

EAIMS supplements aggregate scoring with critical-dimension constraints intended to prevent material weaknesses in foundational capabilities from being obscured through compensatory averaging.

The applicable critical dimensions, thresholds, maturity ceilings, and related rules are defined by the published scoring methodology for the relevant EAIMS version.

These constraints MUST be applied after calculation of the indicative aggregate maturity result.

## 8. Conformance Classes

EAIMS defines three assessment conformance classes.

### 8.1 Self-Assessment

A self-assessment is conducted by the assessed organization using the published EAIMS materials.

Organizations SHOULD document assessor roles, evidence sources, assumptions, and limitations.

### 8.2 Facilitated Assessment

A facilitated assessment is conducted with support from an internal or external facilitator.

The facilitator SHOULD support consistent interpretation of capability anchors, evidence requirements, and scoring rules.

### 8.3 Independent Review

An independent review includes review of evidence and scoring by a party independent of the assessed operating unit.

Independence SHOULD be sufficient to reduce material conflicts of interest in the review process.

EAIMS v0.2 does not define accredited certification, accreditation requirements, conformity-assessment bodies, or certification authority.

Use of the terms **EAIMS assessment**, **EAIMS self-assessment**, **EAIMS facilitated assessment**, or **EAIMS independent review** MUST NOT be represented as accredited certification.

## 9. Reassessment

Organizations SHOULD reassess:

* At least annually
* After major organizational restructuring
* After significant AI platform or architecture changes
* After material AI-related incidents
* After significant changes to AI governance or regulatory obligations
* Before or after major AI investment or transformation programs
* When the organization's AI portfolio or operating model changes materially

Reassessment SHOULD consider both changes in maturity and changes in the quality, relevance, and freshness of supporting evidence.

Organizations SHOULD preserve prior assessment results where practicable to enable longitudinal comparison.

## 10. Interpretation of Results

EAIMS results are intended to support:

* Capability gap analysis
* Transformation planning
* Investment prioritization
* Governance improvement
* AI operating-model development
* Portfolio planning
* Risk-informed decision-making
* Periodic maturity reassessment

A higher maturity level does not automatically imply that an organization should increase AI adoption.

Organizations SHOULD determine appropriate target maturity based on strategic relevance, expected value, risk exposure, regulatory obligations, economics, and organizational context.

EAIMS results SHOULD be interpreted together with capability-level evidence, confidence information, critical-dimension results, and documented assessment limitations rather than as an isolated enterprise score.

## 11. Limitations

An EAIMS maturity score does not guarantee:

* AI system safety
* Regulatory or legal compliance
* Positive return on investment
* Ethical outcomes
* Security assurance
* Model quality or accuracy
* Successful organizational adoption
* Business performance
* Certification against another standard

EAIMS assesses organizational maturity and capability. It does not replace system-specific technical evaluation, legal review, regulatory assessment, cybersecurity assessment, responsible-AI evaluation, financial analysis, professional audit, or other specialized assurance activities.

EAIMS is a decision-support and organizational capability-assessment framework, not a substitute for professional legal, regulatory, security, financial, ethical, or audit advice.

## 12. Version and Validation Status

This document defines the normative organizational requirements of the EAIMS v0.2 specification family.

Patch releases within the v0.2 specification family MAY correct documentation, metadata, implementation inconsistencies, tests, or research-support materials without redefining the fundamental maturity architecture.

The EAIMS v0.2 reference implementation provides executable validation and scoring support for the published assessment structure.

At the time of this specification, EAIMS has undergone internal implementation testing and fictional-case demonstration but has not yet established independent multi-organization validation, representative benchmarking, inter-rater reliability, or accredited certification.

These limitations MUST be considered when EAIMS results are interpreted, compared, or communicated.
