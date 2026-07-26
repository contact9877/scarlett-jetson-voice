# Captain OS Read-Only Bootstrap v0.2 Review

A deliberately limited first-stage companion for Justin C. Blanton's Captain OS mission.

## Current capability

- Reads an approved local snapshot of human-readable authority documents.
- Rejects symbolic links, unsupported file types, and oversized source files.
- Builds a deterministic SHA-256 manifest.
- Verifies whether approved sources changed, appeared, or disappeared after indexing.
- Performs local keyword retrieval with source-path paragraph citations.
- Runs deterministic, key-free retrieval evaluations.
- Optionally uses the OpenAI Agents SDK to synthesize only retrieved passages.
- Refuses arbitrary command execution, source mutation, messaging, calendar actions, account changes, deployment, and autonomous permission expansion.

Google Drive remains the durable source of truth. This repository is an execution-layer component and must remain rebuildable.

## Quick start

Python 3.11 or newer is recommended.

```bash
cd captain-os-readonly
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -e .
captain-os doctor
python scripts/collect_environment.py
```

Put approved `.md` or `.txt` exports in `data/approved_snapshot/`, then run:

```bash
captain-os index
captain-os verify
captain-os ask "What is the current Captain OS implementation stage?"
python evals/run_local.py
```

`captain-os verify` exits non-zero if an approved source was added, removed, or changed after the manifest was built. Re-index only after reviewing and accepting the source change.

The default per-file intake limit is 2 MiB and can be reduced with `CAPTAIN_OS_MAX_FILE_BYTES`. Larger documents should be deliberately split or handled by a later reviewed ingestion path rather than silently loaded.

Without an API key, `ask` returns retrieval excerpts only. Optional OpenAI synthesis is installed with `pip install -e ".[openai]"` and reads `OPENAI_API_KEY` from the local environment. Never commit the key, paste it into Drive, or put it in an issue.

## Promotion status

Review branch only. It is not deployed, persistent, remotely reachable, write-enabled, or approved for merge.
