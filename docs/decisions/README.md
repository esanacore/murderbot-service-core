# Architecture Decision Records

This directory records significant architectural decisions using a
lightweight ADR format. An ADR is added or amended whenever the
architecture changes (`AGENTS.md` rule 6, `CONTRIBUTING.md`).

## When to write one

- A choice between two or more real alternatives, where the reasoning
  matters more than the choice itself (future contributors need to know
  *why*, not just *what*).
- Any change to `docs/architecture.md`'s component/failure-domain
  structure.
- Any decision that a future contributor might reasonably want to
  revisit or reverse — the ADR is what lets them do that safely, by
  showing what was already considered and rejected.

## Format

```
# ADR NNNN: Title

Status: Proposed | Accepted | Superseded by ADR NNNN

## Context
What problem/question forced this decision.

## Decision
What was decided.

## Alternatives considered
What else was on the table, and why it lost.

## Consequences
What this makes easier, harder, or forecloses.
```

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-service-core-architecture.md) | Single Raspberry Pi 4 for PiKVM and personality services | Accepted |
| [0002](0002-repository-structure-and-license.md) | Repository structure and licensing approach | Accepted |
