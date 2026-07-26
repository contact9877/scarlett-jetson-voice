# Threat Model

## Assets

- Justin's source-of-truth documents
- API credentials
- Personal health, legal, family, career, financial, work, and invention information
- Repository integrity and audit history

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
- Environment collector excludes credentials, usernames, hostnames, network identifiers, and file contents.

## Residual risks

- A malicious passage can still influence model synthesis.
- Local malware can steal environment variables.
- Keyword retrieval can miss relevant context.
- Incorrect snapshot selection can omit controlling authorities.
- Dependencies require ongoing review.
