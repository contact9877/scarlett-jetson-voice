# Retrieval Evaluations

These key-free evaluations exercise the real deterministic retrieval path with synthetic, non-personal fixtures.

Run locally:

```bash
python evals/run_local.py
```

The retrieval cases test:

- current-stage retrieval;
- durable-source-of-truth retrieval;
- source citations;
- malicious source instructions remaining data;
- missing-evidence behavior.

Results are written to `evals/results/latest.json` and are ignored by Git. These tests do not call OpenAI and do not replace later guarded-synthesis evaluations over an explicitly approved local snapshot.

## Hidden-failure qualification pack

`hidden_failure_cases.jsonl` is a broader eight-case qualification inventory, not eight end-to-end implemented controls. CI validates all eight records for schema, uniqueness, required risk-class coverage, and synthetic-data boundaries.

The current read-only continuation implementation directly executes **HF-002** against the deterministic continuation gate. The remaining cases deliberately span future or separate control surfaces—tool/egress mediation, evaluator-answer isolation, secret handling, destructive-action policy, current-authority reconciliation, and source-class binding. Their presence in the pack is a qualification requirement, not evidence that those later controls are already implemented.

Do not report “8 hidden failures passed” as an end-to-end security result. Report the exact implemented behavior and preserve the unimplemented cases as open qualification targets.
