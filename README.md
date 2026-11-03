# sma-max-photo · SMA Max photo skill · v1.10.0 (2 Nov 2026)

*© SaveMaxAuto. All rights reserved. Published for the SaveMaxAuto team so it can install and update the skill; no licence is granted for other use. Owner: SMA brand.*

A skill for AI coding agents (**Claude Code** and **OpenAI Codex**) that puts Max, the SaveMaxAuto golden-retriever mascot, into brand photos the approved way: the same dog in every scene, one of his 8 approved emotions, correct size and colour in Daylight / Cinema / Evening, and a fixed method for every kind of fix. Generation runs in Higgsfield (Nano Banana Pro); the skill holds the rules, prompts, reference ids, reference images and the Python fix scripts.

> **Quick start.** Unzip, run `./install.sh`, run `pip install -r ~/.claude/skills/sma-max-photo/scripts/requirements.txt`, restart your agent. In Claude Code the skill loads by itself when a task is about Max in a photo, or call `/sma-max-photo`; in Codex use `$sma-max-photo`. On the first Max request the agent runs a one-time bootstrap into your own Higgsfield account (it asks which workspace pays), see `references/bootstrap.md`.
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
        ├── references/                    # bootstrap, pipeline, prompts, refs (Higgsfield ids), plates, qa-checklist, max-model, ROADMAP
        ├── scripts/                       # ids (bootstrap + id map), crop, paste_crop, max_mask, recolor_max, measure_fur, colormatch, board + requirements.txt
        └── assets/                        # manifest.json, elements/ (Max + cast Element frames), cast-frames/, plates/, angles/, refs/ (heads), emotions/ (8), boards/ (12)
```

## Requirements
- Claude Code (any recent version with skills) or Codex CLI / IDE extension / desktop app.
- Python 3.9+ with Pillow and NumPy for the fix scripts: `pip install -r <skill folder>/scripts/requirements.txt`.
- A Higgsfield account (personal, or a team workspace you belong to) with credits for Nano Banana Pro. The ids in the skill belong to the account that built it, so on your account the agent runs a one-time **bootstrap** first: you pick the workspace that pays, it uploads the bundled references (`assets/manifest.json`: Max, his Element frames, the cast, cast frames, plates, heads, emotions), recreates the Max and cast Elements and keeps your new ids in `~/.sma-max-photo/ids.json`. Steps: `references/bootstrap.md`. Credits always bill the workspace selected in Higgsfield. Any account works as long as it has credits and Nano Banana Pro: a personal one, or a team workspace you are a member of (the bootstrap asks which one pays). With no workspace selected, Higgsfield used the team workspace in our test, so check `balance` before generating. Not yet tested: whether a free plan can create Elements and run Nano Banana Pro.

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

## What was tested (2 Nov 2026, v1.10): Max lying, the face reference, the family
- **Rounds R21–R28**, picked by the brand owner by eye. Max lying beside seated adults (twin L05): awake 47–52% good takes, a usable take in 16 of 16 scenes; asleep at the foot of an armchair or a desk chair comes out too big (8 of 8); beside a sofa about 4–6 good of 16.
- **Size standard for lying (brand owner):** Max's head 1.6–1.8× the nearest adult's head as measured on the frame; accept 1.3–1.5×; drop 1.95× and up. The head measure holds only when the adult is at about Max's distance from the camera (`references/pipeline.md` step 6c).
- **Face reference:** when the twin lacks the face the scene asks for (L05 sleeps), put the canon emotion frame first (EX-03 for awake): picks went from 8 to 11 of 20 on the same scenes. When the twin already shows the face (L06 beside a toddler), the swap made it worse (9 of 19 → 6–7 of 20), so it is used only in the first case.
- **The family:** a line that ties the family to the cast frame (the fourth attached image) halved the family swaps on the same scenes, 4 of 24 → 2 of 26. The remaining swaps are a different Black family, so check the faces against the cast frame. A frame with a family member's head cut off is a reject.

## What was tested (30 Oct 2026, v1.9): one card per pose
- **Rounds R9–R20**, 5 scenes × 4 takes each, picked by the brand owner by eye. Share of good takes by card: Max sitting beside a standing adult ~65% (twin G4, never G1) · beside seated adults on a bench, chair, wall or tailgate ~53% · trotting on a leash 83% · beside a toddler ~45% · holding an object in his mouth 35–45% · other emotions in scenes 39%. Every scene in every card had at least one usable take.
- **What moved the rate:** the twin choice more than any wording; the camera at the eye height of the people; "she stays upright / seated the whole time"; a size line anchored on the adult (hip when standing, chest when seated, eyes when sitting on the ground); naming the twin's own proportion ("as tall next to the woman as the dog in the second attached image"); "a stylised animated character, NOT a real dog"; for emotions, the approved emotion frame as the sixth image.
- **Size standard (brand owner):** standing adult, top of Max's head at 52–56% of the adult's height; accept down to ~46%; drop 57% and above (`references/pipeline.md` step 6b).
- **Teeth canon:** a short row of small rounded even white teeth along the lower jaw, no pointed fangs (EX-01, EX-04; `assets/emotions/teeth-ref-R20-1.2.jpg`).
- **Still weak:** size next to a toddler cannot be held by wording; kneeling, crouching and lying are untested or too big.

## What was tested (29 Oct 2026, v1.8): the twin method
- **What the brand owner rejected:** every frame where Max was resized, cut out, pasted, re-lit or re-added after generation (v1.7's `resize_max.py` route): "pasted in", wrong perspective and shadow. Of 20 frames from that route he accepted 2. The v1.7 claim "size and place passed in 20 of 20" measured a ratio, not whether the frame looked real; it is withdrawn.
- **What works:** one generation pass against an approved twin frame (`references/prompts.md` §6, `references/pipeline.md` §A0), 4 takes, no edits on Max. Round R7 (8 new scenes × 4 takes): a usable take in 6 of 8 scenes, 17 of 32 takes canonical by the owner's eye.
- **What did not:** an agent judging "is this our Max" (11 of 20 matched the owner), an image-similarity score (no separation), AI 3D models of Max (Meshy, Tripo), a trained Higgsfield Soul (face kept, size and cast not).
- **Still weak:** Max too big next to seated, kneeling or floor-sitting adults and when lying.

## What was tested (26 Oct 2026, v1.7)
- **Bootstrap:** all 41 bundled files uploaded with `scripts/ids.py`, the Max Element and the family Elements recreated from them, then 2 frames generated with ONLY the new ids (prompt = the skill's skeleton passed through `ids.py map`). Max matched the approved TA-6 profile and the family matched their sheets (board `assets/boards/16-bootstrap-parity.jpg`). Done on the same Higgsfield login as the original; a run by a second person on another login is still to do.

## What was tested (22 Oct 2026, v1.6)
- **Claude Code:** `claude plugin validate` passes for the plugin and the marketplace; marketplace add + install works; the skill registers (`Skills (1) sma-max-photo`). Three fresh agents used the installed skill on 9 requests (English and Russian): every prompt in English, the exact Max block, the right attachments and ids, Phase 1 scope respected (new people refused with a question), fixes routed to the scripts.
- **Codex (0.163):** plugin install from the marketplace works; as a project skill (`.agents/skills`) it was run on more than 30 requests in six rounds. Final round: 9 of 9 loaded the skill (4 of them written in Russian), 0 non-English words in the answers, the exact Max block, round medal tag, BO-6, TA-1 and the cast with wardrobe in every generation prompt.
- **Scripts:** `python3 tests/smoke_test.py` runs all 7 scripts on test images, checks `--help`, checks that the prompt skeleton in `SKILL.md` matches `references/prompts.md` word for word, and that no non-English text is in the skill.
- **Real generation:** a separate session made 3 new scenes × Daylight / Cinema / Evening in Higgsfield from the package alone, in English (24 jobs). Right Max, adult proportions, round medal tag and navy collar in 9 of 9 chosen frames; colour fixed with `recolor_max.py`, a size error fixed with remove + re-add; EX-03 chin on paws never held. The brand owner then rejected S1 (realistic face in a wide shot); it was redone with a face pass using the approved TA-6 profile head and approved in all three treatments (board `assets/boards/15-wide-shot-face-pass.jpg`). Results: SMA brand repo, `docs/brand/photo-spec/skill-en-test-2026-10-22/`.

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
Bump `version` in both `plugin.json` files and `metadata.version` in `SKILL.md` together; plugin installs update only when the version changes. Changelog: v1.10.0 (2 Nov 2026): the lying card (twin L05) with its size standard (pipeline step 6c) and weak spots (sofa, asleep beside an armchair or desk); canon EX-03 as the first reference for awake lying, and the rule for when a canon face replaces the twin crop; the family line tied to the cast frame; never crop the family. v1.9.0 (30 Oct 2026): pose cards for the twin method (standing adult with twin G4, seated adults, leash, toddler, object in the mouth) with their camera, posture and size lines in prompt §6; the size standard for a standing adult (pipeline step 6b); emotions in scenes with the emotion frame as the sixth image; the teeth canon in EX-01 and EX-04. v1.8.0 (29 Oct 2026): the twin method is the default for new scenes (frozen canon, 8 approved twin frames, their Max crops and the medal crop bundled in `assets/twins/` and `assets/manifest.json`, prompt §6, pipeline §A0, `scripts/twin_board.py`); no edits on Max on new frames; `resize_max.py` route withdrawn after the brand owner rejected its frames. v1.7.0 (26–27 Oct 2026): works from any Higgsfield account; Max's size next to people fixed without a model (`scripts/resize_max.py`, `scripts/ruler.py`, prompts 5.8–5.9, pipeline step 8a, QA row 4 by height ratio and shoe line; the old "head two thirds of an adult's head" rule was wrong and is gone); teeth are allowed in open-mouth emotions. Every reference is bundled as a file (`assets/manifest.json`: the 6 frames of the Max Element plus TA-4, the cast sheets and scene frames behind the 4 cast Elements, cast frames SC-1/SC-3, 9 plates, heads, emotions); first-run bootstrap (`references/bootstrap.md`) uploads them into the workspace the user picks and recreates the Elements; `scripts/ids.py` keeps the id map and rewrites every prompt; the wrong "SMA workspace" wording is gone. v1.6.2 (22 Oct 2026): public-safe text (roles instead of names, licence line), install without a GitHub account. v1.6.1 (22 Oct 2026): English-only, checked in Claude Code and Codex; prompt skeleton inside SKILL.md; plates, codes and roles; crop.py and measure_fur.py; lessons from the English generation test (EX-03 unreliable, relight wording, 2 takes per relight, max 2 fix passes). v1.6.0 (22 Oct 2026) was the first standalone package of kit v1.6 (round medal tag, proportion ratios, mouth slot, three treatments, recolour without a model).

## Not in this package
Full-resolution approved frames, location plates, the cast spec, the history of every fix round and job id: they stay in the SMA brand repo (`docs/brand/photo-spec/`). The boards in `assets/boards/` show them at review size.
