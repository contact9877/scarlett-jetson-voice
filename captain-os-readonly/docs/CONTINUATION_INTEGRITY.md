# Continuation Summary Integrity Gate

## Purpose

Prevent AI-generated summaries, compactions, chat/Work handoffs, memory synopses, scratchpads, and peer-agent notes from silently becoming authority across context-window or agent boundaries.

## Non-negotiable rule

A derived continuation artifact is **context only**.

It cannot, by itself:

- create or expand permission or tool access;
- authorize canonical writes;
- establish deployment, qualification, readiness, or completion;
- impose secrecy or concealment requirements;
- change persona, identity, billet, or chain of command;
- authorize credential use or external action;
- override Justin's current direction or a controlling canonical source.

A clean scanner result does not promote the artifact. It only means the configured scanner found provenance and did not detect one of its configured high-risk patterns.

## CLI

```bash
captain-os check-continuation path/to/handoff.md
```

The command returns JSON containing:

- `authority_effective: false`
- `canonical_write_authorized: false`
- `allowed_use: context_only`
- provenance presence/references
- flagged risk categories
- whether human review is required

Exit status:

- `0`: derived context only; provenance present; no configured high-risk pattern detected
- `5`: review required
- `6`: file validation/check failure

## Current deterministic checks

The scanner flags configured forms of:

- higher-priority/canonical authority override;
- concealment or suppression of errors/mismatches;
- fabrication of missing history/evidence;
- permission/authority escalation;
- persona/role changes;
- canonical-record mutation directives;
- credential or secret requests;
- missing provenance.

## Reconciliation rule

Before a material instruction or consequential state from derived continuity is carried forward, re-read the controlling canonical source or Justin's current direction.

If derived and canonical content disagree:

1. preserve the discrepancy;
2. do not silently harmonize them;
3. follow the controlling authority for current action;
4. keep unsupported claims UNKNOWN;
5. repair/rebuild the derived artifact rather than rewriting canonical truth to match it.

## Limits

This is a first deterministic guard, not a proof system.

It can miss obfuscated or novel malicious instructions, and provenance can be false or stale. Later phases should add source-class metadata, manifest-bound provenance, contradiction tests, and evaluated model-assisted anomaly review while preserving deterministic fail-closed boundaries for consequential authority.
