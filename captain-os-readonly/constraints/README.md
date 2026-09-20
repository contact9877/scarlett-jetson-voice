# CI dependency constraints

These files pin the Python toolchain used by the Captain OS read-only GitHub Actions test job.

They are **CI reproducibility controls**, not a universal application lockfile or a software-supply-chain guarantee.

## Files

- `ci-runtime.txt` constrains the dev/test packages installed into the Python 3.11 CI environment.
- `ci-build.txt` constrains packages used in pip's isolated PEP 517 build environment.

The two channels are intentionally separate. With pip 26.2+, ordinary constraints no longer apply to isolated build environments, so the workflow supplies both `PIP_CONSTRAINT` and `PIP_BUILD_CONSTRAINT`.

## Current snapshot provenance

The runtime snapshot was derived from successful Captain OS Read-Only CI #83 on 2026-09-20 (Python 3.11 / Ubuntu 24.04) and then verified by a clean GitHub Actions run using the committed constraints.

The isolated-build snapshot was reviewed against the build backend declared by `pyproject.toml`. Hatchling 1.32.3 was the current non-yanked PyPI release on 2026-09-20; its build-side supporting packages are constrained here where they are part of the reviewed build path.

## Update procedure

Do not edit constraints merely because a newer release exists.

For an intentional update:

1. Review the candidate package release/provenance and compatibility.
2. Change only the needed constraint entries.
3. Let CI perform a clean constrained install.
4. Confirm the "Verify constrained CI toolchain" step reports the intended versions.
5. Confirm the incompatible-constraint negative test still fails closed.
6. Require existing Ruff, pytest, key-free retrieval evaluations, compileall, and CodeQL to remain green.
7. Review the constraints diff and retain the prior commit as rollback.
8. Record material toolchain changes in the relevant Captain OS continuity/security record.

## Failure behavior

The CI job includes a negative resolver check using an impossible temporary pytest constraint. The job must observe dependency resolution failure. A resolver that silently ignores the constraint or falls back to unconstrained packages causes CI failure.

## Residual limitations

- This snapshot targets the current GitHub-hosted Python 3.11 / Ubuntu CI lane, not every OS or Python version.
- It does not hash-pin every wheel/sdist.
- It does not make PyPI or the network immutable.
- It does not lock optional OpenAI runtime extras because baseline read-only CI does not install them.
- It does not prove package maintainers, build infrastructure, or transitive artifacts are trustworthy.
- The project metadata keeps flexible dependency ranges for normal development; CI reproducibility is enforced by these separate reviewed constraint files.

If stronger guarantees become necessary, evaluate hash-locked artifacts, attestations/provenance verification, or a reviewed lock format as a separate change rather than silently expanding this mechanism.
