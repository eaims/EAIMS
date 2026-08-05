# RFC 0001 — Executable Conformance

**Status:** Accepted for v0.2 Community Draft

## Problem
Narrative scoring rules can be implemented inconsistently.

## Decision
Publish a dependency-free reference engine, schemas, CLI, fixtures, and tests. The normative method remains readable; executable behavior resolves only cases explicitly covered by v0.2 rules.

## Alternatives
Spreadsheet-only and vendor-hosted tools were rejected as the sole reference because they reduce inspectability and portability.

## Compatibility
v0.1 inputs require explicit migration to v0.2.
