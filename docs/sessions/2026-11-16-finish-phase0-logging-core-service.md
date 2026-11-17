# Session: Finish the Phase 0 logging-config and core_service work

- **Date:** 2026-11-16
- **Agent:** Claude Code (Claude Fable 5.2)
- **Branch / PR:** `wip/phase0-logging-core-service`, pull request #33
- **Topics:** logging_setup.py, load_logging_config, configure_logging, LoggingConfigError, logging.example.yaml, core_service.py, murderbot-core.service, systemd entrypoint, consumed_event_types, hardware isolation test, secrets-scan CI job, check_traceability.sh, REQUIREMENTS_TRACEABILITY.md, tests/conftest.py, bom_report.py, GAP-005
- **Related:** `docs/TEST_PLAN.md` GAP-005; NFR-02; `docs/backlog.md` P2/P3 software rows; `AGENTS.md` rules 5, 8, 9. No earlier session summaries exist.

## Request

Finish an in-progress branch and open a pull request for it. The branch
held one untested, unreviewed WIP commit from an interrupted session that
had followed a session plan with two tasks: make `logging_setup.py` read
the schema in `configs/examples/logging.example.yaml` (with tests), and
add the `murderbot_core.core_service` entrypoint that
`services/systemd/murderbot-core.service` references (with tests). The
instructions were to review the diff, run the suite and the CI checks,
fix what the branch broke, complete what the plan started without
starting new features, bring the constitution-required documents in line,
and leave merging to the maintainer.

## Context

- The WIP commit's own notes declared the work complete and verified.
  That was treated as a claim to check, not as a result.
- The commit also contained three things the session plan did not list:
  the host PC's GPU model reworded to `TBD` across the docs, a
  `secrets-scan` job in `.github/workflows/ci.yml`, and a change to the
  phase ordering in `tools/bom_report.py`. They were already pushed and
  the instruction was not to rewrite that commit, so they were kept,
  checked, and flagged in the pull request for the maintainer to accept
  or reject.
- The local venv runs Python 3.14 with a newer `ruff` than the
  pre-commit pin; CI runs Python 3.11. CI is the authority for 3.11.

## Decisions

- **Convert every logging-config failure to `LoggingConfigError`**
  (agent). `core_service` promises that a bad `logging.yaml` never blocks
  startup, but a YAML syntax error or an unreadable file raised a
  different exception and crashed it. Rejected: catching broad
  `Exception` in `build_core`, which would hide real bugs.
- **Validate the level inside `configure_logging()` and before touching
  the root logger** (agent). `level="..."` and a hand-built
  `LoggingConfig` bypassed the parser's validation, and a failed call
  should not leave logging half torn down.
- **Fallback applies `configure_logging()` defaults, not
  `logging.basicConfig(WARNING)`** (agent). The code comment and docs say
  "defaults" (INFO, stdout); `basicConfig` is also a no-op when the root
  logger already has handlers.
- **Prove hardware isolation in a subprocess** (agent). The existing test
  said it checked hardware mocks but asserted nothing about them, and its
  scan of module globals could not see `from murderbot_core import
  hardware`. Running the entrypoint in a fresh interpreter and asserting
  that no hardware-facing package is in `sys.modules` is order
  independent and covers transitive imports. `murderbot_core.telemetry`
  was added to the forbidden list. Rejected: instrumenting the mocks,
  since the core never constructs one there is nothing to instrument.
- **Do not add an event loop to `main()`** (agent). It exits 0 after
  setup. A blocking loop needs a real event source, which is Phase 2+;
  adding one would be a new feature. Documented in `docs/software.md`
  and `TODO.md` instead, and the systemd unit stays an example.
- **Unreleased changelog entries describe the result, not the WIP
  session's intermediate fixes** (agent). Two "Changed" bullets described
  corrections to code that had never been released; they were folded into
  the "Added" entries.
- **`docs/SESSION_PLAN.md` reset to the constitution template** (agent),
  as `AI_WORKFLOW.md` step 27 requires once outcomes are recorded.
- **`docs/AGENT_HANDOFF.md` keeps this repository's log format** (agent),
  with the Next Steps procedure moved under the newest entry; the WIP
  commit had inserted it as a top-level section in the middle of the log.

## Discoveries

- Both delimiter rows in `docs/REQUIREMENTS_TRACEABILITY.md` had been
  changed to `| | --- |`. The tables stop rendering and
  `check_traceability.sh` reports every requirement as missing, which
  fails the Constitution Compliance workflow. The WIP notes did not
  mention running that checker.
- CI's lint job runs `ruff`/`mypy` from `services/` only, so `tests/` and
  `tools/` are never linted or type-checked. That is how a
  `tuple[int, ...]` annotation on a function returning `float("inf")`
  went unnoticed in `tools/bom_report.py`. Recorded in `TODO.md`.
- `hardware.yaml`'s `*_enabled` flags are parsed but nothing consumes
  them yet; the first real backend has to gate on them.
- `pre-commit run --all-files` rewrites `CLAUDE.md` (missing final
  newline on `main`). Left alone here as unrelated to this branch.
- The WIP documents disagreed on how many tests `test_core_service.py`
  had (6, 7; the file had 8). Counts are now kept only in
  `docs/TEST_PLAN.md`'s dated coverage row.

## Outcome

Pull request #33 from `wip/phase0-logging-core-service`: the original
WIP commit plus follow-up commits for the logging fixes, the core-service
fallback and isolation tests, the traceability/BOM-tool repairs, and the
documentation. Locally: 74 tests pass with 99% coverage (338 statements,
4 missed), `ruff check`, `ruff format --check`, and `mypy src` are clean,
and the constitution checkers CI runs all pass. Deliberately left out: a
transport event loop for `core_service`, the audio/RGB/telemetry/health
entrypoints, extending CI linting to `tests/` and `tools/`, and any
`docs/MEMORY.md` entry (approval-gated).

## Open Questions

- Does the maintainer want the three out-of-plan changes (GPU wording,
  `secrets-scan` job, BOM report ordering) in this pull request, or split
  out?
- Should `murderbot-core.service` carry `Restart=on-failure` once the
  entrypoint blocks, and what is the event source? Both belong to the
  Phase 2 design.
- No release was cut: the project is pre-`v0.1.0` and nothing here is
  deployable yet.
