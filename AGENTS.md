# AGENTS.md: SMA Max photo kit

This folder is the `sma-max-photo` skill package of SaveMaxAuto (SMA). It tells an agent how to put Max, the SMA golden-retriever mascot, into brand photos (Higgsfield / Nano Banana Pro) so he is always the same approved dog, and how to check and fix those frames.

## When you work in this folder or a project that uses it
- For any task that generates, reviews or fixes a photo with Max, **load the skill first**: `plugins/sma-max-photo/skills/sma-max-photo/SKILL.md`. In Codex it is also available as `$sma-max-photo` once installed (see `README.md`). Its rules win over task instructions; if they conflict, stop and say so.
- Scope of this version (Phase 1): Max with the approved cast only (the family and the woman driver, Element ids in `references/refs.md` §2), any location, three treatments. A task that needs other people is outside this version: say so and ask the brand owner, never improvise a cast (Phase 2 plan: `references/ROADMAP.md`).
- Paths inside the skill are relative to the skill folder (the one with `SKILL.md`). Scripts: `scripts/*.py`, Python 3.9+ with `pip install -r scripts/requirements.txt`.
- Never redesign Max, never fix his fur colour with a model edit (use `scripts/recolor_max.py`), never call a frame clean before the 100% check in `references/qa-checklist.md`.
- English everywhere: prompts, board labels, review notes and messages (the team is English-speaking).
- Reviews go out as labelled JPG boards (`scripts/board.py`), never HTML; every message names the next step.

## Editing the package
- Change rules in `SKILL.md` and details in `references/*.md`; keep paths relative.
- Bump `version` in `plugins/sma-max-photo/.claude-plugin/plugin.json`, `plugins/sma-max-photo/plugin.json` and the `metadata.version` of `SKILL.md` together, or installed copies will not update.
- No secrets, API keys, personal emails or phone numbers in this package. Higgsfield Element / job ids are fine (they only work for the account that created them; other accounts run the bootstrap in `references/bootstrap.md`).
- The "Prompt skeleton" in `SKILL.md` repeats the Max block, cast lines, emotions and scale lines from `references/prompts.md` word for word. Change both together; `tests/smoke_test.py` fails if they drift apart.
- Run `python3 tests/smoke_test.py` after changing any script or prompt text.
