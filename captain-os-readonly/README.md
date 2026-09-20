# Captain OS Read-Only Bootstrap v0.2 Review

A deliberately limited first-stage companion for Justin C. Blanton's Captain OS mission.

## Current capability

- Reads an approved local snapshot of human-readable authority documents.
- Rejects symbolic links, unsupported file types, and oversized source files.
- Builds a deterministic SHA-256 manifest.
- Verifies whether approved sources changed, appeared, or disappeared after indexing.
- Performs local keyword retrieval with source-path paragraph citations.
- Runs deterministic, key-free retrieval evaluations.
- Checks derived summaries/handoffs before reuse and always classifies them as context-only, never authority.
- Flags suspicious continuation directives such as authority override, concealment, fabrication, permission escalation, persona changes, canonical-record mutation, or credential requests.
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

Before reusing an AI-generated summary, compaction, chat/Work handoff, memory synopsis, scratchpad, or peer-agent note, run:

```bash
captain-os check-continuation path/to/handoff.md
```

A clean result still reports `authority_effective: false`, `canonical_write_authorized: false`, and `allowed_use: context_only`. A risky or provenance-free artifact returns `REVIEW_REQUIRED` and a non-zero exit code. Passing this check never promotes the artifact into canonical authority; material instructions and consequential state still require reconciliation against Justin's current direction or the controlling canonical source.

`captain-os verify` exits non-zero if an approved source was added, removed, or changed after the manifest was built. Re-index only after reviewing and accepting the source change.

The default per-file intake limit is 2 MiB and can be reduced with `CAPTAIN_OS_MAX_FILE_BYTES`. Larger documents should be deliberately split or handled by a later reviewed ingestion path rather than silently loaded.

Without an API key, `ask` returns retrieval excerpts only. Optional OpenAI synthesis is installed with `pip install -e ".[openai]"` and reads `OPENAI_API_KEY` from the local environment. Never commit the key, paste it into Drive, or put it in an issue.

## Promotion status

Review branch only. It is not deployed, persistent, remotely reachable, write-enabled, or approved for merge.
