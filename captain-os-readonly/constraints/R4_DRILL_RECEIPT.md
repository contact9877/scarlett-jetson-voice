# R4 CI Constraint Update / Rollback Drill Receipt

Date: 2026-09-20

Purpose: force an in-scope CI run after the runtime constraint file was restored byte-for-byte to the reviewed base snapshot.

Drill sequence:
1. Start from review/captain-os-readonly-v0.2 head 064eb903c91bbfcc12ba92473244431051a01bac.
2. Change only Ruff constraint 0.16.8 -> 0.16.7.
3. CI #93 passed with the constrained toolchain verifying Ruff 0.16.7, 29 pytest tests, 4/4 key-free retrieval evals, Ruff static checks and the incompatible-constraint fail-closed negative.
4. Restore Ruff 0.16.7 -> 0.16.8. The constraint file content SHA returned to its original reviewed blob SHA 3ab096b77b8709e9a421b38eaabf50a643380e05.
5. Because the PR then had no net path diff, GitHub path-filtered workflows did not emit a rollback run. This receipt is intentionally the only remaining diff so CI can verify the restored constraints without changing runtime behavior.

This file is drill evidence only and must not be merged into the production/review branch as a required runtime artifact.
