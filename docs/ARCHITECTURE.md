# Architecture

This project's architecture doc lives at
[`architecture.md`](architecture.md) (lowercase — written before this
constitution-mandated uppercase path existed) and includes the Mermaid
component diagram and state-machine diagram Principle 6 calls for. This
file is kept as a short pointer so `docs/ARCHITECTURE.md`-relative links
from constitution tooling/templates still resolve to something; see
`decisions/0002-repository-structure-and-license.md` for the general
reconciliation approach to this kind of path collision.

See [`architecture.md`](architecture.md) for:

- Power topology (standby vs. host-on branches)
- Component diagram (Mermaid)
- Failure-domain table (why a crashed RGB/audio service can't take
  PiKVM/ATX down with it)
- State model diagram and invariants

Key technologies: Python 3.11+ (`services/`), Raspberry Pi 4 + PiKVM,
no frontend/database/cloud infrastructure exists in this project.
