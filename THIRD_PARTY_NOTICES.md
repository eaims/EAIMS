# EAIMS Third-Party Notices and Provenance Boundaries

Copyright © 2026 Elias Naserkhaki. All rights reserved except as expressly licensed.

This file identifies third-party rights boundaries for the EAIMS v1.0 candidate. It is not a claim that third-party dependencies or referenced standards are part of EAIMS copyright.

## 1. Included license texts

The repository includes unmodified copies of the following public-license texts for convenience and legal clarity:

- Apache License 2.0 — `LICENSES/Apache-2.0.txt`.
- Creative Commons Attribution 4.0 International — `LICENSES/CC-BY-4.0.txt`.

Those license texts remain the legal instruments of their respective licensors and are not authored by EAIMS.

## 2. Runtime and test dependencies

The Python package declares dependencies such as `PyYAML` and `jsonschema`, and test/CI workflows may install tools such as `pytest`, `setuptools`, `wheel`, `build`, dependency-audit tooling, and SBOM tooling. These packages are **not vendored into this repository** by the v1.0 candidate and remain subject to their own licenses and notices when installed.

## 3. Container and CI references

Dockerfiles and CI configuration may reference third-party container images, package registries, and GitHub Actions. A reference, version pin, or installation command is not an incorporation of the referenced third-party source code into EAIMS. Any downloaded image, action, or package remains governed by its own terms.

## 4. External standards, frameworks, laws, products, and publications

EAIMS may identify or discuss external standards, frameworks, laws, products, or publications for factual citation, comparison, interoperability, research, or context. Such references do not imply ownership, affiliation, endorsement, equivalence, or incorporation of protected source material.

EAIMS v1.0 SHALL NOT reproduce protected third-party wording, tables, graphics, paid-standard text, proprietary taxonomies, customer documents, or confidential materials without a documented legal basis compatible with the intended release.

## 5. External reviews and findings

External findings, observations, facts, ideas, requirements, and recommendations may inform independently drafted EAIMS material. Such input is not treated as incorporated copyrightable expression unless the third-party expression itself is copied into the repository.

If third-party substantive copyrightable text, code, schema, test, translation, graphic, or other artifact is directly incorporated into an official EAIMS release, the rights-instrument requirements in `IP_POLICY.md`, `CONTRIBUTOR-RIGHTS.md`, `CLA.md`, and `COPYRIGHT-ASSIGNMENT.md` apply before incorporation.

## 6. Current v1.0 candidate provenance conclusion

The release audit for this candidate did not identify any known directly incorporated substantive third-party text, code, or artifact requiring an unrecorded rights instrument. Third-party software dependencies are referenced rather than vendored; external-review/design inputs are represented as generalized findings or independently drafted requirements; synthetic reference implementations are labeled synthetic.

If a later audit identifies contrary evidence, the affected material SHALL be quarantined from official release until provenance and rights are resolved.
