# assets/

Media (audio clips, images used by services at runtime) — **not**
covered by this repository's MIT license (`../LICENSE`).

## Rule: no copyrighted media in version control

Per `AGENTS.md` rule 2 and v1.0 acceptance criterion #10
(`../docs/requirements.md`), no copyrighted soundtrack file, or any other
media the operator doesn't have clear rights to redistribute, may be
committed here. `../.gitignore` ignores everything under this directory
except this README and `.gitkeep` placeholders as a backstop — the
primary control is simply not adding those files to a tracked path.

## How startup audio actually gets installed

1. The operator supplies their own audio clip(s) locally on the deployed
   Pi, outside this repository (e.g. `/opt/murderbot/assets/`).
2. `murderbot-audio.service` (`../services/systemd/murderbot-audio.service`)
   reads clip filenames from `configs/profiles.yaml` (see
   `../configs/examples/profiles.example.yaml`), not from anything
   committed here.
3. If a clip is user-supplied and the operator has confirmed they hold
   the necessary rights (personal use, a license they've purchased, or
   original content), it is still kept local rather than committed,
   since repository visibility/distribution rights are a different
   question from personal playback rights.

## What can go here

- This README.
- `.gitkeep` placeholders for directory structure, if a runtime path
  needs to exist before assets are installed.
- Genuinely license-clear assets (e.g. UI icons the maintainer created
  from scratch) may be added with an explicit note of their license —
  none exist yet.
