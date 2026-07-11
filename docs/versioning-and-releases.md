# Versioning & Release Strategy

## Versioning

[Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`), applied
to this repository as a whole (docs + software + hardware design
together) rather than per-subsystem, since a hardware change often forces
a documentation and software change in lockstep:

- **MAJOR** — breaking changes to the physical interface (wiring,
  connector pinout, power topology) that make an existing built unit
  incompatible with new instructions, or a breaking change to
  `murderbot_core`'s config schema.
- **MINOR** — new capability that doesn't break existing builds/config
  (e.g. adding the RGB phase once Phase 3 is stable, adding a new event
  type).
- **PATCH** — bug fixes, documentation corrections, dependency bumps, test
  additions.

Pre-1.0 (`0.x.y`), minor version bumps may include breaking changes, per
standard SemVer pre-1.0 convention — each `ROADMAP.md` phase completing
is a reasonable trigger for a `0.x.0` tag.

`v1.0.0` is reserved for meeting every acceptance criterion in
`docs/requirements.md`.

## Release process

1. Ensure `CHANGELOG.md`'s `[Unreleased]` section accurately reflects
   everything since the last tag.
2. Move `[Unreleased]` into a new dated version section.
3. Tag the commit: `git tag -a vX.Y.Z -m "..."` and push the tag.
4. `.github/workflows/release.yml` drafts a GitHub Release from the
   `CHANGELOG.md` section for that tag.
5. For hardware-affecting releases, confirm `docs/wiring.md` and
   `hardware/bom.csv` match the as-built state referenced by the release
   (v1.0 acceptance criterion #9 and beyond).

## What this project does not yet have

- **No OTA update mechanism.** Deliberately deferred — see `ROADMAP.md`
  post-1.0 list, item 9. OTA requires this versioning/rollback story to
  be proven manually first.
- **No LTS branch policy.** Only `main` is supported pre-1.0
  (`SECURITY.md`); this will be revisited at `v1.0.0`.
- **No automated PyPI/package publishing.** `services/` is consumed by
  cloning this repository, not by installing a published package, at
  least through v1.0.
