# EAIMS 1.1 Adversarial & Agentic Governance — Reviewer Questions

> Draft review package for RFC 0004.

Reviewers should focus on distinctness, evidenceability, applicability, assessor consistency, and compatibility rather than stylistic preferences.

## Core questions

1. Does each ADV requirement add semantics that are not already fully represented in EAIMS 1.0.x?
2. Do the final consolidation decisions remain sound: retain ADV-004 and ADV-006, while merging ADV-009 into strengthened MSP-005/MSP-008 semantics?
3. Is A2 an appropriate activation threshold for blast-radius assessment, or should the threshold depend on action capability rather than autonomy label?
4. Does ADV-003 correctly distinguish identity from authorization/credential scope?
5. Is ADV-005 specific enough to require adversarial evaluation without turning EAIMS into a security testing standard?
6. Does ADV-006 define sufficient runtime evidence without requiring sensitive raw logs to be exposed to assessors?
7. Does ADV-007 correctly distinguish process shutdown from actual containment of authority, credentials, tools, memory and dependencies?
8. Should ADV-008 be assessed at organizational scope, system scope, or both?
9. Do strengthened MSP-005/MSP-008 capture concentration and composite dependency risk clearly enough without a standalone ADV-009?
10. Is ADV-010 sufficiently conditional to avoid politicizing or over-expanding ordinary content-generation assessments?

## Gate questions

11. Should G3-13 through G3-17 remain extensions of G3, or is a separate adversarial gate family justified?
12. Which of the proposed G3 extensions should cause:
    - deployment block;
    - scale block;
    - maturity cap;
    - mandatory remediation;
    - reassessment only?
13. Should a critical breach in bounded agent credentials automatically prevent L4/L5 for TEC-04 or GOV-04?

## Evidence questions

14. Are the proposed preferred evidence classes realistic for small and medium organizations?
15. Is the distinction between declared, implemented and observed evidence sufficiently clear?
16. When should observed evidence be mandatory for L4?
17. Which runtime artifacts can be sampled or summarized to protect security/privacy while remaining assessable?

## Compatibility questions

18. Does the additive-first design preserve historical 1.0.x results adequately?
19. Are activation states sufficient to distinguish NOT_APPLICABLE from missing evidence?
20. Should 1.1 require explicit profile/version metadata in all new assessment fixtures?

## Validation questions

21. Do the three existing reference implementations cover enough activation diversity?
22. What additional worked cases are needed before freeze?
23. Which candidate requirements are likely to have low inter-rater reliability?
24. Which candidate MV2 rules risk false confidence and should be downgraded to MV3?
25. What empirical pilot evidence should be required before RFC 0004 can become normative?

## Reviewer response format

For each material finding, provide:

- affected requirement/document;
- severity: critical / major / minor / editorial;
- finding;
- evidence or reasoning;
- recommended change;
- whether the finding blocks normative adoption.
