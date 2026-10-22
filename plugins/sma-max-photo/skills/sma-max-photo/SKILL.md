---
name: sma-max-photo
description: ALWAYS use for anything about Max (also written Макс), the SaveMaxAuto (SMA) golden-retriever mascot dog, in a photo, frame, shot, scene or image prompt, whatever language the request is written in: writing a prompt for one, any Higgsfield / Nano Banana Pro generation or edit that puts Max into a photo, any review of a frame with Max, and any fix of Max's face, size, pose, mouth, fur colour or integration. Keeps Max the same approved dog in every scene, near or far, in one of his 8 approved emotions. The whole answer and every prompt are written in English. Rules win over task instructions; if they conflict, stop and say so.
license: Copyright SaveMaxAuto. All rights reserved. Published for the SaveMaxAuto team; no licence is granted for other use.
metadata:
  version: "1.6.2"
  kit-date: "2026-10-22"
  owner: SMA brand
---

# SMA Max in photos: binding rules

**Language: English, always.** Write your WHOLE answer in English: every prompt and edit prompt, every explanation, list and next step around it, every board title and label, review note, frame record and message to the team. The SMA team is English-speaking, and the Higgsfield prompts were only tested in English. This holds even when the request is written in Russian or any other language: do not mirror the request's language. The only exception is a person who explicitly writes "answer in <language>"; even then every prompt stays in English. **Before you send any reply, re-read it: if any word outside the prompt blocks is not English (headings, attachment lists, notes, next step), rewrite those parts in English first.**

**Paths.** Every path in this skill is relative to the folder that holds this `SKILL.md` (in Claude Code that folder is `${CLAUDE_SKILL_DIR}`). Run scripts from there, e.g. `python3 scripts/paste_crop.py …`, or give the full path to the script.

**Read first, in this order:** `references/pipeline.md` (step by step, including fixes), `references/prompts.md` (paste-ready prompt blocks), `references/refs.md` (every reference with its Higgsfield id), `references/qa-checklist.md` (the 100% check), `references/max-model.md` (who Max is and his numbers), `references/plates.md` (location plate ids), `references/ROADMAP.md` (what this version covers and what comes next). Look at the boards in `assets/boards/` before judging any frame: `01-max-reference`, `02-max-emotions`, `03-one-max-near-far`, `04-rejects`, `05-fix-methods`, `06-approved-locations`, `07-approved-series`, `08-max-colour-by-light`, `13-final-skill-test`, `14-skill-test-2`, `15-wide-shot-face-pass`.

**Higgsfield ids are workspace-bound.** The Element and job ids in `references/refs.md` work only in the SMA Higgsfield workspace. If a Max reference id fails, upload the matching file from `assets/refs/` or `assets/emotions/` (Higgsfield `media_upload` → PUT → `media_confirm`) and use the new media id; never substitute another dog. The cast Elements, cast frames and location plates exist only as ids in that workspace: without access to it, stop and ask the brand owner.

**Scripts** need Python 3.9+ with Pillow and NumPy: `pip install -r scripts/requirements.txt`. Every script prints its usage with `--help`. Codes (BO-6, TA-1, EX-xx, SC-x, L-plates, P/F/G frames) and who decides what: `references/refs.md` §6–7.

## M0. Scope of this version (Phase 1, v1.6)
- People: ONLY the approved cast, with their Elements and cast frames from `references/refs.md` §2:
  - the family: mom `38f73cfe-d229-4034-a7f3-45c97bbe959e`, dad `463e9ac3-b5de-4a49-afe3-cdd8ee075f2d`, toddler `509bd9ee-cdf0-457f-a2d4-7ec63b36ca8b`; cast frame SC-1 `f12d9610-9e69-445d-9292-a4e8cf0c32ac`;
  - the woman driver `b35dc1c6-598f-4ccc-9df1-e941ef01c332`; cast frame SC-3 `7583f0c7-5027-49dd-b5ec-eebc7b862c1d`.
- Locations may vary: an approved location plate (job ids in `references/plates.md`; the image files live in the SMA brand repo, `docs/brand/photo-spec/locations/`), or a new place without a plate, built from the scene prompt alone (boards `13-final-skill-test`, `14-skill-test-2`).
- Every scene ships in three treatments: Daylight, Cinema, Evening (M5b).
- **If a task needs other people** (a new person, another family, a crowd with faces): say that it is outside the current version (Phase 2, `references/ROADMAP.md`) and ask the brand owner before doing anything. Never improvise a new cast.

## M1. The reference is fixed. Do not redesign Max.
- The approved Max = master `MX3-BO-6` (`assets/refs/MX3-BO-6-gpt25-sunburst_MASTER.jpg`), face `MX3-TA-5`, side view `MX3-TA-1`, profile `MX3-TA-6`, the 8 emotions in `assets/emotions/`, **plus** Max in the approved scenes (boards `06-approved-locations`, `07-approved-series`). Match to these; never "improve" them. BO-6 shows a hint of lower teeth: copy his look from it, never his mouth.
- Rejected on 20 Oct 2026 and never to be repeated: matching every frame to one **neutral series face** (NREF-1) or to P09A's raised-brow face. Max lost his emotion and quality dropped.

## M2. Inputs for every Max frame
- Model **Nano Banana Pro** (`nano_banana_pro`), 2k single frames / 4k on a location plate; 3:2 unless a format is given.
- Element `<<<01ba1fc5-227c-439d-aa29-47ada4e45545>>>` (SMA-Max-v3) in the prompt. Never v3.1 `33a3c7d0…`, v2 `a29f73eb…`, continuity `0cd7d22f…`.
- `image_references`: plate (if any) → **BO-6** `3394863f-6981-426a-a55e-6400056a0900` with "look ONLY, NOT his pose" → approved cast frame (family `f12d9610-9e69-445d-9292-a4e8cf0c32ac`, woman `7583f0c7-5027-49dd-b5ec-eebc7b862c1d`) → **TA-1 `dc637319-6e29-4660-b100-7e815f154601` for body proportions** ("the attached SIDE-VIEW photo", always the last body reference) → optional pose reference ("pose only").
- Prompt order: camera → style line → scene → Max block → cast → tail. Max block verbatim from `references/prompts.md` §2, with the four slots filled (POSE, EXPRESSION, MOUTH, SCALE).

## Prompt skeleton (copy exactly; details in `references/prompts.md`)
Every new Max frame is written in this order and in English. The texts below are copied from `references/prompts.md`; paste them **character for character**. Never paraphrase the Max block, never drop the Element tag, never leave a `{slot}` or a bracketed placeholder in the final prompt. If a part does not fit the scene, read `references/prompts.md` before changing anything.

1. **Camera:** `Candid documentary photograph, handheld at eye level, 35mm lens, f/2.8.` On a location plate use `Camera exactly as in the first reference photo.` instead.
2. **Style line (Daylight; Cinema and Evening are relights, prompt 5.6):** `CLEAN DAYLIGHT: bright natural late-morning daylight from one clear direction with real shadows, neutral daylight white balance, true whites, clean blue sky, fresh greens, natural colours, crisp digital capture, no grain.`
3. **Scene:** 2–4 sentences: the moment, one action with a consequence, two story objects, nobody looks at the lens. On a plate (`references/plates.md`), begin with `In the exact location of the first reference photo (keep the place, camera and light exactly)…`.
4. **Max block** (fill POSE, EXPRESSION, MOUTH and SCALE; keep everything else word for word):

```text
{POSE: where he is, how he is placed, **at the same distance from the camera as {named person}** (NOT in the foreground), filling at least a third of the frame height}: <<<01ba1fc5-227c-439d-aa29-47ada4e45545>>> — Max, the SMA mascot, looking EXACTLY like the attached master photo (same face, same fur length and texture, same colours, same proportions); use the master photo for his LOOK ONLY, NOT for his pose, head angle or camera angle: a stylised Pixar-quality 3D animated golden retriever composited into this real photograph, clearly an animated character, NOT a real dog. Fully grown ADULT male of about 30 kg, NOT a puppy, with the body proportions of the attached SIDE-VIEW photo of Max (his whole body in profile): long legs (front leg from elbow to ground about half his shoulder height), deep chest, body clearly longer than it is tall, long tapered muzzle (almost half the length of his head), a SMALL head: sitting, his head from crown to chin is only about one fifth of his sitting height; NOT a big round puppy head, NOT short stubby legs, NOT chubby. Face as in his front close-up reference: refined, fairly narrow muzzle. Cartoon brown eyes with visible whites (medium-small, not puppy eyes), both pupils centred and looking the same way, oversized matte dark-brown nose, soft drop ears. Navy blue leather collar with ONE ROUND brushed-brass MEDAL tag hanging from a small ring at the front: a flat coin-shaped disc with a raised rim and a small embossed letter M in its centre, about as wide as his nose; NOT a letter-shaped M charm, NOT a cut-out letter, NOT square, NOT shiny gold. Fur: dense, soft, MATTE feature-animation groom with fine strands and natural clumping, honey-gold back fading to cream chest; NOT glossy, NOT plastic, NOT a plush toy. Expression: {EXPRESSION, §4}. {MOUTH: for an open-mouth emotion write `Mouth softly open, pink tongue just showing, NO teeth visible.`; for a closed-mouth emotion write `His mouth stays CLOSED: lips together, no teeth, no tongue.`} SCALE: {SCALE line, §3} His whole body is clearly smaller than an adult's. Soft contact shadow, lit by the same light as the scene. He is the only stylised element and the only warm-coloured object in the frame.
```

   - **EXPRESSION** (one of the 8, word for word): **EX-01 joy**: `pure joy: mouth open in a big happy cartoon grin, pink tongue out and slightly to one side, NO teeth visible, eyes OPEN and bright with clearly visible whites (NOT squinting), brows lifted happily, ears relaxed back` · **EX-02 head tilt**: `curious head tilt: head tilted about 25 degrees to one side, one ear lifted slightly higher than the other, a small calm closed-mouth smile, eyes bright and interested (not startled, not worried); a grown-up dog's curiosity, NOT puppyish` · **EX-03 chin on paws**: `lying flat on his belly with his chin resting on his crossed front paws, eyes open and looking calmly, CONTENT: relaxed brows, a small closed-mouth smile, ears soft; calm and happy, NOT sad, NOT pleading` · **EX-04 excited**: `excited: mouth open in a big grin with the tongue showing and NO teeth, ears perked forward, tail held high and wagging (slight motion blur on the tail tip)` · **EX-06 trot**: `happy trot on all four long legs: mouth slightly open, ears bouncing, one front paw and the opposite hind paw lifted, tail streaming behind, a little motion blur on his paws` · **EX-07 dozing**: `peacefully dozing and CONTENT: eyes gently closed in two happy curves, a small relaxed smile, head resting on his front paws; a cosy happy nap, NOT sad, NOT sick` · **EX-08 listening**: `listening attentively: ears raised and pushed forward, head turned slightly toward the person, eyes focused on them, mouth closed` · **EX-10 suspicious**: `playfully suspicious: ONE eyebrow raised high, the other lowered, eyes in a sideways glance at {object}, a small knowing smirk with the mouth closed; comic and friendly, NOT angry`
   - **MOUTH**: open-mouth emotions (EX-01, EX-04, EX-06) `Mouth softly open, pink tongue just showing, NO teeth visible.`; all others `His mouth stays CLOSED: lips together, no teeth, no tongue.` For EX-01 / EX-04 plan the mouth pass (prompt 5.4) anyway.
   - **SCALE** (pick the one that fits, anchor it to an object in the frame): **sit**: `real golden-retriever size; sitting, the top of his head is at a standing adult's hip, about 80 cm from the ground; next to a seated adult his head is no higher than their lower chest.` · **sit-kitchen**: `a FULL-SIZE ADULT golden retriever of about 30 kg, NOT a puppy: sitting, the top of his head is level with the kitchen counter / tabletop (about 78 cm) and with the standing adult's hip.` · **stand**: `standing, his shoulders are just above a standing adult's knee (about 58 cm) and his head reaches mid-thigh.` · **lie**: `lying, nose to tail-base he is about 1 metre long, roughly an adult's leg from hip to heel. Stretched out, NOT curled into a ball, long front legs forward.` · **car**: `standing beside a car wheel, his back is just below the top of the tyre.` More keys in `references/prompts.md` §3.
   - **POSE**: where he is and how he is placed, always `at the same distance from the camera as {the named person} (NOT in the foreground)`, beside or behind that person, never between the people and the camera. Lying or in a wide room shot, drop "filling at least a third of the frame height".
   - Right after the Max block (before the cast line), add the fur line for Daylight: `his fur is a warm honey-gold (yellow-gold, cream chest) like the master photo, NOT orange, NOT red-brown`.
5. **Cast** (exactly one, Phase 1): family `The same Black mom, dad and toddler as in the reference photo: <<<38f73cfe-d229-4034-a7f3-45c97bbe959e>>> mom, <<<463e9ac3-b5de-4a49-afe3-cdd8ee075f2d>>> dad, <<<509bd9ee-cdf0-457f-a2d4-7ec63b36ca8b>>> toddler. Wardrobe: mom light-blue denim shirt over a white tee and jeans; dad navy jacket, white tee, khaki-grey trousers; toddler light-blue tee, beige trousers.` OR woman driver `The same woman as in the reference photo: <<<b35dc1c6-598f-4ccc-9df1-e941ef01c332>>>, late 30s, brown hair pulled back, white shirt, sky-blue sweater over the shoulders, light jeans.`
6. **Tail:** `Max is lit by exactly the same light as the people, with a contact shadow, and the scene's colours reflected in his eyes and nose. Nobody looks at the camera. No logos, no readable text.`
7. **Attach as `image_references`, in this order, always listing each reference with its id:** location plate (if any, `references/plates.md`) → BO-6 `3394863f-6981-426a-a55e-6400056a0900` (look only) → cast frame (family SC-1 `f12d9610-9e69-445d-9292-a4e8cf0c32ac` OR woman SC-3 `7583f0c7-5027-49dd-b5ec-eebc7b862c1d`) → TA-1 side view `dc637319-6e29-4660-b100-7e815f154601` (body proportions) → optional pose reference LAST, with `Use the last attached image for his POSE only, not its light, setting or camera angle.` in the prompt.
8. **Model:** Nano Banana Pro (`nano_banana_pro`), 3:2, 2k without a plate / 4k on a plate, 2 takes. Then QA (`references/qa-checklist.md`), then relight to Cinema and Evening (prompt 5.6).


## M3. Size and body
- Size = an **object anchor** in the frame ("top of his head level with the counter / high-chair tray", "head as big as the mom's head") **and** "at the same distance from the camera as {person} (NOT in the foreground)".
- Against the puppy look, describe the **body** as ratios: head about 1/5 of sitting height, muzzle almost half the head, long legs, stretched out not curled. "Adult" and "30 kg" alone gave a puppy (22 Oct, F4).
- Size check at the same depth as an adult: Max's skull without ears ≈ the adult's head width (with ears 1.4–1.6×); lying, nose to tail-base ≈ 0.9–1 m (40–45% of a 3-seat sofa); sitting, his crown at a standing adult's hip. Never place him on the camera side of the people (`references/prompts.md` §3b).
- An edit never changes scale or pose. For those: remove Max, then re-add on the clean plate (`references/pipeline.md` step 8), with "same framing, no zoom, no crop".
- The tag is ONE ROUND brass MEDAL with a small embossed M (`references/max-model.md` §2); write it out in full. "M tag" alone gave a letter-shaped M charm (22 Oct).

## M4. Face and emotion
- Only the 8 emotions. Eye whites visible except in sleep. **No row of teeth, ever.** Calm states in positive words ("CONTENT, relaxed brows, small smile, NOT sad"). No strong emotion words that fold the face.
- A wrong face is fixed **with a picture**: a crop around Max (whole head + collar), an approved head from `assets/refs/` with the **same expression** and a similar angle as the 2nd image, "REPLACE the dog's head … KEEP THE HEAD EXACTLY AS LARGE AS NOW", then `FULL=1 python3 scripts/paste_crop.py …`. Never blend two faces pixel by pixel.
- **Wide shots: plan a face pass.** In a wide family frame Max's head is small (under ~400 px) and often in profile, and the model then draws a realistic dog face: small eye without a white, long plain muzzle, small nose. The brand owner rejected all three treatments of S1 for this (22 Oct). Check the face at 100% against TA-5 / TA-6 before anything else, and fix it on a crop with an approved head at the SAME angle: profile → `MX3-TA-6-head-profile.jpg` (or P02A, P08D), three-quarter → P06A, front → TA-5. A reference with a side glance (P03A, P06C) on a small head gave a smooth "clay" head with squinting side-eyes: do not use those for a profile head. If the edit also repaints the background inside the crop, paste back only the head: `REGION=x0,y0,x1,y1 python3 scripts/paste_crop.py …` (box in crop pixels). Make the relights only from the fixed Daylight frame. Worked example, approved by the brand owner on 22 Oct: board `assets/boards/15-wide-shot-face-pass.jpg`.
- Eyes: both pupils centred, both eyes looking the same way. A side glance in the reference copies over and reads cross-eyed; fix it with the eye reference `assets/refs/HEAD-TA3-eyes-straight.jpg`, not with words.
- Never use EX-01 as a face reference (teeth return). When the head is small (< ~500 px), prefer a closed-mouth smile, and do every face or mouth edit on a crop around Max (whole head + collar, with margin), never on the full frame; then paste back with `scripts/paste_crop.py`.

## M4b. What the prompt alone does not hold (kit test, 20 Oct: 12 frames)
- The right Max came out 12 of 12; a frame with no notes on Max only 6 of 12. Always make 2 takes and plan a fix pass.
- Fill the MOUTH slot of the Max block to match the expression (`references/prompts.md` §2). The old fixed "If he smiles: mouth softly open…" line put teeth into 4 of 8 closed-smile frames (22 Oct).
- Joy (EX-01) and excited (EX-04) open the mouth anyway: plan the mouth pass (prompt 5.4) on a wide crop as a normal step.
- Open smiles gave teeth in 3 of 6: use the closed-mouth version in medium/wide shots, or a mouth pass on a crop.
- Max placed on the camera side of people or furniture comes out too big: place him beside or behind a named person.
- Poses like "chin on paws" or "not curled" are often ignored: describe the head position physically, or attach a "pose only" image. EX-03 chin on paws failed 4 of 4 in the English test (22 Oct): when head-down matters, use EX-07 or EX-08 instead.
- Fix passes: at most 2 per frame (each pass smooths fur). If it still fails, remove + re-add or regenerate.
- Relights: 2 takes each; see the relight notes in `references/prompts.md` §5.6 (name the ground outdoors, mount lamps on real objects).

## M5. Integration
- Max is lit by the scene's light, has a contact shadow, is no brighter or more saturated than the real objects, wears a NAVY collar with a dull-brass round medal tag. He stays stylised; never make him realistic to "fit".
- Name every glass, fog or water layer as "keep" in an edit.
- A 4k full-frame edit can come back with a colour cast: run `scripts/colormatch.py` against the approved frame (undo, not a grade). No grain, no grade otherwise.

## M5b. Colour by light and the three treatments
- Every scene ships in **Daylight, Cinema and Evening**. When someone asks for a Cinema or Evening frame of a NEW scene, give both steps: first the Daylight generation prompt (skeleton above), then the relight prompt 5.6 to run on the approved Daylight frame. Approve Daylight first; make Cinema and Evening by **relighting that same frame** (prompt 5.6). A new generation with the Daylight frame as reference drifts redder: do not use it.
- Max's fur (median hue of the mid-tone fur, `references/prompts.md` §3c, board `assets/boards/08-max-colour-by-light.jpg`): Daylight **28–33°** honey-gold (BO-6 ≈ 30–31°) · Cinema **26.5–30.5°** golden-amber · Evening **19–28°** on the lit side: honey-gold with warm amber highlights where the lamp falls, darker in shadow, never orange all over (board 08's swatch label "orange-amber" means those highlights). **Below 19° reads red-brown: reject.**
- Judge colour by eye next to BO-6, not by the number alone: too saturated reads orange even inside the band.
- Evening relight: say "the same light over the whole frame, no sunlight anywhere" and where each lamp is; never write "his fur glows orange-amber" (it makes him orange). Write "gentle warm highlights; his fur stays honey-gold, NOT orange, NOT red-brown".
- Off-colour Max: `scripts/recolor_max.py --mask` with a whole-silhouette mask from `scripts/max_mask.py` (hue/saturation of his fur only, no model). A partial mask leaves red patches. **Never fix colour with a model edit**: on 21 Oct it painted cream bibs, white muzzles and a realistic head.
- Evening: light the people from real lamps above them (a street lamp over the sidewalk, ceiling lights over a kitchen) and ask for both faces lit equally; otherwise one face goes dark or the frame goes too dark.
- Every relight prompt says Max stays EXACTLY the same cartoon character (eyes with whites, face, fur pattern: no lighter chest/belly/muzzle, not a real dog).
- Before choosing any take: Max's head and fur pattern next to the approved frame at 100%. Never choose from thumbnails.

## M6. Review and reporting
- Check every frame at **100%** with `references/qa-checklist.md`. Put Max's head next to the reference head on one JPG board (`scripts/board.py`). Never call a frame clean before that.
- Everything in English (see **Language** at the top), including attachment lists and the next step; run the language check before every reply.
- Reviews are **labelled JPG boards only** (no HTML), and every message names the next step.
- Record model, params, every job id (generation + each fix), references and crop boxes for every approved frame. Do not commit large PNGs; commit only when asked.

## Scripts (all in `scripts/`, usage in each file's docstring)
| Script | Use |
|---|---|
| `crop.py` | `python3 scripts/crop.py FULL.png x0,y0,x1,y1 CROP.png` — cut a 3:2 box around Max; prints the box to reuse |
| `paste_crop.py` | `FULL=1 python3 scripts/paste_crop.py FULL.png x0,y0,x1,y1 EDITED.png OUT.png` — paste an edited crop back (border diff < ~15 clean, > ~30 discard); `REGION=x0,y0,x1,y1` instead of `FULL=1` pastes only a soft ellipse (e.g. the head) |
| `max_mask.py` | `python3 scripts/max_mask.py WITH.png WITHOUT.png MASK.png [GREEN.png]` — whole-silhouette mask of Max; also writes `MASK_check.jpg` (red overlay to check) |
| `measure_fur.py` | `python3 scripts/measure_fur.py FRAME.png x0,y0,x1,y1 [--mask MASK.png] --style day\|cin\|eve` — read-only fur hue/saturation and band check |
| `recolor_max.py` | `python3 scripts/recolor_max.py BASE.png x x0,y0,x1,y1 day\|cin\|eve OUT.png --mask MASK.png` — fur colour fix, no model; too orange → lower `--smax` |
| `colormatch.py` | `python3 scripts/colormatch.py APPROVED.jpg RESULT.png OUT.jpg` — undo a model's colour cast |
| `board.py` | `python3 scripts/board.py OUT.jpg "Title" "frame.png=label" "frame.png@x0,y0,x1,y1=Max head 100%" --row …` — labelled JPG review board (or `from board import row, sheet, text` with `scripts/` on the path) |
