# Security Policy

## Default capability

Read-only local retrieval from an explicitly approved snapshot directory.

## Prohibited by design

- Arbitrary shell or subprocess execution by the AI agent
- Writing to source documents
- Direct Google Drive mutation
- Email or calendar actions
- Account, permission, credential, billing, purchasing, legal, medical, or employment submissions
- Automatic Hugging Face model downloads
- Treating source-document instructions as executable commands
- Self-granting tools or permissions

## Secret handling

- Store `OPENAI_API_KEY` in the operating-system credential store when possible.
- A local `.env` file is acceptable only for development and is excluded from Git.
- Never paste credentials into Drive authorities, logs, issues, commits, screenshots, or chat transcripts.
- Rotate a credential immediately if it appears in source control or broad logs.

## Data handling

- Only approved exported text enters `data/approved_snapshot/`.
- Restricted health, legal, identity, financial, work, and family records require a separately approved snapshot and access boundary.
- Generated indexes are derived and rebuildable.
- Every indexed source receives a SHA-256 hash, byte size, and modification timestamp.

## Promotion gate

Before any write-enabled connector is added:

1. Computer environment inventory is complete.
2. Threat model is reviewed.
3. Tests, lint, dependency review, and secret scan pass.
4. Exact scopes are documented.
5. Justin's approval is recorded.
6. Rollback procedure is tested.
