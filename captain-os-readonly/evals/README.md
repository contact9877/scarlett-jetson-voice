# Retrieval Evaluations

These key-free evaluations exercise the real deterministic retrieval path with synthetic, non-personal fixtures.

Run locally:

```bash
python evals/run_local.py
```

The cases test:

- current-stage retrieval;
- durable-source-of-truth retrieval;
- source citations;
- malicious source instructions remaining data;
- missing-evidence behavior.

Results are written to `evals/results/latest.json` and are ignored by Git. These tests do not call OpenAI and do not replace later guarded-synthesis evaluations over an explicitly approved local snapshot.
