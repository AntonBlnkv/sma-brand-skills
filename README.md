# sma-max-photo · SMA Max photo skill · v1.6.2 (22 Oct 2026)

*© SaveMaxAuto. All rights reserved. Published for the SaveMaxAuto team so it can install and update the skill; no licence is granted for other use. Owner: SMA brand.*

A skill for AI coding agents (**Claude Code** and **OpenAI Codex**) that puts Max, the SaveMaxAuto golden-retriever mascot, into brand photos the approved way: the same dog in every scene, one of his 8 approved emotions, correct size and colour in Daylight / Cinema / Evening, and a fixed method for every kind of fix. Generation runs in Higgsfield (Nano Banana Pro); the skill holds the rules, prompts, reference ids, reference images and the Python fix scripts.

> **Quick start.** Unzip, run `./install.sh`, run `pip install -r ~/.claude/skills/sma-max-photo/scripts/requirements.txt`, restart your agent. In Claude Code the skill loads by itself when a task is about Max in a photo, or call `/sma-max-photo`; in Codex use `$sma-max-photo`. Higgsfield ids work only in the SMA workspace.
>
> **Language.** Everything in the skill is in English: rules, prompts, board labels, and the agent's reviews and messages.

## What this version covers (Phase 1)
- **Max with the approved cast only:** the family (mom, dad, toddler; cast frame SC-1) and the woman driver (cast frame SC-3). Their Element ids are in `references/refs.md` §2.
- **Any location:** an approved location plate or a new place without a plate.
- **Three treatments** for every scene: Daylight, Cinema, Evening.
- **Not covered: other people.** If a task needs a new person, the skill says it is outside this version and asks; it does not improvise a cast. Adding new people is Phase 2 (planned, not started): a new cast member gets a portrait and a frame without Max, approval, then an Element; a general cast slot in the prompt; a people check in QA; a test on 2 new casts. Details: `references/ROADMAP.md`.

## What is inside
```
sma-max-photo-skill/
├── README.md, AGENTS.md, install.sh
├── .claude-plugin/marketplace.json        # makes this folder/repo a Claude Code marketplace "sma-brand"
├── tests/smoke_test.py                    # runs every script on test images
└── plugins/sma-max-photo/
    ├── .claude-plugin/plugin.json         # Claude Code plugin manifest
    ├── plugin.json                        # Codex plugin manifest
    └── skills/sma-max-photo/              # THE SKILL (this folder alone is enough to install)
        ├── SKILL.md                       # binding rules M1–M6 (frontmatter: name, description)
        ├── agents/openai.yaml             # Codex display name
        ├── references/                    # pipeline, prompts, refs (Higgsfield ids), plates, qa-checklist, max-model, ROADMAP
        ├── scripts/                       # crop, paste_crop, max_mask, recolor_max, colormatch, board + requirements.txt
        └── assets/                        # refs/ (master + approved heads), emotions/ (8), boards/ (11 overview JPGs)
```

## Requirements
- Claude Code (any recent version with skills) or Codex CLI / IDE extension / desktop app.
- Python 3.9+ with Pillow and NumPy for the fix scripts: `pip install -r <skill folder>/scripts/requirements.txt`.
- Access to the SMA Higgsfield workspace. The Element `SMA-Max-v3` and every job id in `references/refs.md` exist only there. Without it, upload the images from `assets/` to your Higgsfield account and use the new media ids; the Element has to be recreated from `assets/refs/` (ask the brand owner).

**Get it:** repo https://github.com/AntonBlnkv/sma-brand-skills · zip of the latest version: https://github.com/AntonBlnkv/sma-brand-skills/releases/latest

## Install: the simple way (both tools, no plugin system)
```bash
./install.sh            # Claude Code + Codex, for all your projects
./install.sh claude     # only ~/.claude/skills/sma-max-photo
./install.sh codex      # only ~/.agents/skills/sma-max-photo
./install.sh project ~/path/to/project   # into that project's .claude/skills and .agents/skills
```
The script copies `plugins/sma-max-photo/skills/sma-max-photo/` into place; an old copy is moved to `*.bak-<date>`, never deleted. By hand it is the same copy:

| Tool | Personal (all projects) | One project (commit it for the team) |
|---|---|---|
| Claude Code | `~/.claude/skills/sma-max-photo/` | `<project>/.claude/skills/sma-max-photo/` |
| Codex | `~/.agents/skills/sma-max-photo/` | `<project>/.agents/skills/sma-max-photo/` |

Restart the agent afterwards. To update, download the new version and run `./install.sh` again.

## Install: as a Claude Code plugin (updates with one command)
The package is hosted on GitHub as `AntonBlnkv/sma-brand-skills`; no GitHub account is needed to install it:
```bash
claude plugin marketplace add AntonBlnkv/sma-brand-skills
```
```bash
claude plugin install sma-max-photo@sma-brand
```
Or inside a session: `/plugin marketplace add AntonBlnkv/sma-brand-skills`, then `/plugin install sma-max-photo@sma-brand`. Updates: `claude plugin update sma-max-photo@sma-brand`, or turn on auto-update for the marketplace in `/plugin` → Marketplaces. Without a GitHub SSH key, set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` before adding the marketplace. As a plugin the skill is named `/sma-max-photo:sma-max-photo`.

From a local copy (zip unpacked): `claude plugin marketplace add ./sma-max-photo-skill`, then the same install command.

## Install: as a Codex plugin
Codex reads `.claude-plugin/marketplace.json` as a legacy-compatible marketplace, and `plugins/sma-max-photo/plugin.json` is its plugin manifest:
```bash
codex plugin marketplace add AntonBlnkv/sma-brand-skills
```
```bash
codex plugin add sma-max-photo@sma-brand
```
or install it from the Plugins directory of the Codex app. Use an up-to-date Codex: an old CLI (0.142) fails with "model is not supported when using Codex with a ChatGPT account"; 0.163 works.

## What was tested (22 Oct 2026)
- **Claude Code:** `claude plugin validate` passes for the plugin and the marketplace; marketplace add + install works; the skill registers (`Skills (1) sma-max-photo`). Three fresh agents used the installed skill on 9 requests (English and Russian): every prompt in English, the exact Max block, the right attachments and ids, Phase 1 scope respected (new people refused with a question), fixes routed to the scripts.
- **Codex (0.163):** plugin install from the marketplace works; as a project skill (`.agents/skills`) it was run on more than 30 requests in six rounds. Final round: 9 of 9 loaded the skill (4 of them written in Russian), 0 non-English words in the answers, the exact Max block, round medal tag, BO-6, TA-1 and the cast with wardrobe in every generation prompt.
- **Scripts:** `python3 tests/smoke_test.py` runs all 7 scripts on test images, checks `--help`, checks that the prompt skeleton in `SKILL.md` matches `references/prompts.md` word for word, and that no non-English text is in the skill.
- **Real generation:** a separate session made 3 new scenes × Daylight / Cinema / Evening in Higgsfield from the package alone, in English (24 jobs). Right Max, adult proportions, round medal tag and navy collar in 9 of 9 chosen frames; teeth fixed with the mouth pass, colour fixed with `recolor_max.py`, a size error fixed with remove + re-add; EX-03 chin on paws never held. The brand owner then rejected S1 (realistic face in a wide shot); it was redone with a face pass using the approved TA-6 profile head and approved in all three treatments (board `assets/boards/15-wide-shot-face-pass.jpg`). Results: SMA brand repo, `docs/brand/photo-spec/skill-en-test-2026-10-22/`.

## Use
- **Claude Code:** the skill loads by itself when a task is about Max in a photo; or call `/sma-max-photo` (as a plugin: `/sma-max-photo:sma-max-photo`).
- **Codex:** `$sma-max-photo`, or pick it from `/skills`; it also loads implicitly by its description.
- Start with `SKILL.md`, then `references/pipeline.md`. Every path in the skill is relative to the skill folder.

## Check that it works
```bash
python3 tests/smoke_test.py
python3 tests/smoke_test.py ~/.claude/skills/sma-max-photo
```
The second line tests an installed copy. Each script prints `ok`; the last line is `ALL OK`.

## Versions
Bump `version` in both `plugin.json` files and `metadata.version` in `SKILL.md` together; plugin installs update only when the version changes. Changelog: v1.6.2 (22 Oct 2026): public-safe text (roles instead of names, licence line), install without a GitHub account. v1.6.1 (22 Oct 2026): English-only, checked in Claude Code and Codex; prompt skeleton inside SKILL.md; plates, codes and roles; crop.py and measure_fur.py; lessons from the English generation test (EX-03 unreliable, relight wording, 2 takes per relight, max 2 fix passes). v1.6.0 (22 Oct 2026) was the first standalone package of kit v1.6 (round medal tag, proportion ratios, mouth slot, three treatments, recolour without a model).

## Not in this package
Full-resolution approved frames, location plates, the cast spec, the history of every fix round and job id: they stay in the SMA brand repo (`docs/brand/photo-spec/`). The boards in `assets/boards/` show them at review size.
