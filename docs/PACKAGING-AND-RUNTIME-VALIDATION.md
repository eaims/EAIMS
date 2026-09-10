# EAIMS 1.0 FC16 — Packaging and Runtime Validation

FC16 separates three distinct claims:

1. **Local Python execution validated** — the canonical validator, test suite and CLI smoke path execute in the build environment.
2. **Container definitions statically validated** — Dockerfile/Compose security and service contracts are parsed and executable-tested without claiming a container was started.
3. **Container runtime validation pending** — an actual Docker daemon is unavailable in the FC16 build environment. Hosted CI includes explicit image, minimal Compose and reference Compose runtime steps and captures runtime evidence when those jobs run.

## Container security baseline

The reference validator container is configured to run as a non-root user. Compose requests a read-only root filesystem, `no-new-privileges`, and drops Linux capabilities for validator/reference-runner services.

These settings are reference controls, not a claim of universal production-hardening suitability.

## Runtime evidence required before RC

A successful release-environment run should retain at least:

- Docker engine/version information;
- Compose version;
- successful image execution result;
- successful minimal Compose exit status;
- successful RI-01/RI-02/RI-03 reference-runner execution;
- built container image ID/digest;
- CI run identifier and UTC timestamp.

Container runtime evidence must be distinguished from static configuration validation.

## FC16 installed-package hardening

FC16 adds an explicit data-root resolver and wheel data-file mapping for `spec/`, schemas, and the test catalog. Hosted CI now builds a wheel, installs it into a fresh virtual environment, changes working directory outside the repository, and runs `eaims-validate`. This closes a packaging ambiguity where source-checkout execution could succeed while an installed wheel lacked discoverable canonical specification data.

The reference Compose file no longer starts an unused PostgreSQL service. An evidence database should only be added to the reference topology when a collector/store integration actually consumes it; otherwise the extra service creates complexity without demonstrated behavior.
