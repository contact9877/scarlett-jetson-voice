# Threat Model

## Assets

- Justin's source-of-truth documents
- API credentials
- Personal health, legal, family, career, financial, work, and invention information
- Repository integrity and audit history
- Continuation integrity across chat/context-window boundaries

## Primary threats

1. Prompt injection in files, emails, webpages, calendar descriptions, or repositories.
2. Credential leakage through logs, commits, screenshots, or errors.
3. Over-broad connector scopes.
4. Exfiltration by untrusted dependencies or model code.
5. Destructive or misleading tool calls.
6. Authority drift where generated output overrides official records.
7. Silent source changes or stale indexes.
8. Supply-chain compromise.
9. Public-repository exposure of private material.
10. Derived-continuation drift where a summary, compaction, handoff, memory synopsis, scratchpad, or peer-agent note inserts or preserves unauthorized instructions, concealment requirements, fabricated history, permission escalation, persona changes, or false deployment/readiness state.

## Controls in v0.2

- Approved local snapshot only.
- Source text is data, never policy.
- No command runner or write connector is attached to the agent.
- SHA-256 manifest and source-path citations.
- Retrieval-only fallback.
- OpenAI receives only retrieved excerpts, never the unrestricted filesystem.
- No automatic Hugging Face model download.
- No secret values in configuration files.
- Derived indexes can be deleted and rebuilt.
- Model outputs are synthesis, not authority.
- Derived continuity artifacts are always context-only and cannot confer canonical-write authority.
- Deterministic continuation preflight flags authority override, concealment, fabrication, permission escalation, persona changes, canonical-record mutation directives, credential requests, and missing provenance.
- Synthesis instructions require reconciliation of material derived-continuity claims against Justin's current direction or the controlling canonical source.
- Environment collector excludes credentials, usernames, hostnames, network identifiers, and file contents.

## Residual risks

- A malicious passage can still influence model synthesis.
- The continuation scanner is heuristic and can miss obfuscated or novel instruction patterns.
- A continuation can contain plausible but false facts without matching a flagged directive pattern.
- Provenance presence does not prove provenance correctness.
- Local malware can steal environment variables.
- Keyword retrieval can miss relevant context.
- Incorrect snapshot selection can omit controlling authorities.
- Dependencies require ongoing review.

## Required regression direction

Future qualification must include synthetic continuations containing:
- unauthorized higher-priority override attempts;
- concealment of failures or source mismatches;
- fabricated missing history;
- permission or deployment escalation;
- unexpected persona/role changes;
- canonical-write directives;
- credential/secret requests;
- stale but plausible facts with valid-looking provenance;
- clean derived context that remains non-authoritative even when it passes the scanner.

A passing continuation check means only that no configured high-risk pattern was found and provenance was present. It never means the artifact is canonical truth.
