# Pipeline: a new SMA photo with Max · kit v1.6 (22 Oct 2026)

Every step below has been run on the approved sets. Prompts: `references/prompts.md`. Ids: `references/refs.md`. Check: `references/qa-checklist.md`. All paths are relative to the skill folder (the one with `SKILL.md`).

## A · Make the frame
1. **Pick the idea and its ad use** ("Max fetches…"). Copy on the image needs the marketing lead's sign-off; numbers, claims and a child "driving" need legal review (`refs.md` §7).
2. **Choose the route.**
   - *On a location plate* (the place must stay the same across frames): a location plate (SMA brand repo `docs/brand/photo-spec/locations/`, or the plate's Higgsfield job id), Nano Banana Pro **4k**. A plate freezes camera and light, so one plate per camera angle.
   - *Without a plate* (free composition, the ideas series): Nano Banana Pro **2k**, 3:2.
3. **Frame for Max.** Sitting or standing, Max fills at least a third of the frame height, and his head is at least about 1/6 of the frame width. Smaller than that, the model simplifies his face (flat face, small eyes) and has to be fixed in step 7. Lying, or in a wide room shot, the true size (`prompts.md` §3 scale lines) comes first: drop the "third of the frame height" clause and plan the face pass (step 7) on a crop.
4. **Write the prompt in the fixed order:** camera → style line (D; A and C come later by relighting, step 11b) → scene → Max block → cast → tail (`prompts.md` §1–2). Fill POSE with **"at the same distance from the camera as {person}"**, EXPRESSION with one of the 8 texts, MOUTH to match it, SCALE with an object-anchored line.
5. **Attach:** plate (if any) → BO-6 → cast frame → TA-1 side view (body proportions) → optional pose reference, always last (`prompts.md` §2). Generate 2 takes.

## B · Check
6. **QA at 100% zoom** (`qa-checklist.md`). Crop Max's head and put it next to the reference head on one board (`scripts/board.py`). Never approve from a thumbnail.

## C · Fix (only what failed; each pass smooths fur, so use as few as possible)
7. **Wrong face, flat face, realistic face → face from an approved head, on a crop.**
   1. Cut a 3:2 box around Max from the full-resolution frame (`python3 scripts/crop.py FULL.png x0,y0,x1,y1 CROP.png`). The box must hold the whole head **and** the collar with the tag (otherwise you get two collars), and as little of the people as possible.
   2. Upload the crop. Edit it with prompt 5.3, attaching an approved head from `assets/refs/` with the **same expression** and a similar angle (2nd image); TA-5 or BO-6 may be the 3rd.
   3. Run 2 takes. Discard any take that reframed the crop or made the head smaller.
   3b. In wide shots this step is normal, not an exception: a small profile head comes out realistic (S1, 22 Oct). Match the angle: profile head → TA-6 (`assets/refs/MX3-TA-6-head-profile.jpg`, job `76795864-d94c-4df8-8c65-454e783ca598`), P02A or P08D; never a side-glance head (P03A, P06C) on a profile.
   4. Paste back with exactly the box `crop.py` printed (if the edit moved or added objects around the head, use `REGION=…` instead of `FULL=1` to paste only the head): `FULL=1 python3 scripts/paste_crop.py FULL.png x0,y0,x1,y1 EDITED.png OUT.png`. Border diff under ~15 = clean; above ~30 = the model moved the image, discard; in between, look at the seam at 100% and discard if it shows.
   5. Compare the head with the reference at 100% on a board.
8. **Too small / too big / wrong pose or place → remove, then re-add.** An edit never changes Max's scale or pose (8 of 8 failed).
   1. Remove Max (prompt 5.1). Check the plate is clean.
   2. Re-add on the clean plate (prompt 5.2): object anchor for size + "same distance from the camera as {person}" + "no zoom, no crop". Attach the clean plate, BO-6, the cast frame, TA-1, and optionally, last, an approved frame where Max has the right size/pose ("pose and size only").
   3. Two takes; reject any that zoomed or moved the camera.
   4. Then step 7 if the face is off.
8b. **Cross-eyed or side-eye look** (pupils pushed into the corners, the far eye on the edge of the face): edit the crop with an eye reference whose eyes look straight ahead (`assets/refs/HEAD-TA3-eyes-straight.jpg`, media `a8f84e0e-aa01-47c7-a839-3dc904ec7f27`): "both pupils CENTRED in round eyes, both eyes looking the same way"; on a 3/4 head add "turn the head a little toward the camera so both eyes show". Words alone do not move the eyes.
9. **Mouth, gaze, ear, small expression changes → one single edit** (prompt 5.4), on a crop when the head is under ~500 px. If an open smile keeps showing teeth, switch to the closed smile. For EX-01 / EX-04 this pass is expected, not an exception (teeth in 8 of 8 joy/excited frames across the two 22 Oct tests). The crop must hold the whole head with margin: a tight crop left the tongue at its edge (22 Oct, F1).
10. **Max looks pasted in (too bright, no shadow, wrong collar colour) but size and place are right → integration edit** (prompt 5.5). If he also sits in the wrong place, use step 8 instead.
10b. **Max's fur is the wrong colour** (too orange, too yellow, grey). First build a mask of his WHOLE silhouette: crop around Max → model edit "remove the dog" (5.1) and, if parts are missed, "replace the dog with a flat green shape of the same outline" → `python3 scripts/max_mask.py CROP.png NO_DOG.png MASK.png [GREEN.png]` (GREEN.png = the model's green-shape edit; the green is keyed automatically). Check the red overlay `max_mask.py` writes next to the mask (`MASK_check.jpg`): it must cover his whole body, ears and tail. Then `python3 scripts/recolor_max.py BASE.png x x0,y0,x1,y1 day|cin|eve OUT.png --mask MASK.png` (start with the style defaults: day H 29.5 / S 0.45–0.58 · cin H 27.5 / S 0.48–0.60 · eve H 22.5 / S 0.46–0.55; adjust only if he still reads wrong next to BO-6: **too orange** usually means too saturated, so lower `--smax`, e.g. 0.50; **grey-brown** = raise `--smin`, e.g. 0.55; a touch more gold in the evening = `--hue 24`; the 22 Oct evening fixes used `--hue 24 --smax 0.58 --smin 0.50`; options may go anywhere on the command line). A partial mask leaves red patches (T3, 21 Oct). One mask serves all three styles of the same frame. No model: it moves only the hue and saturation of Max's fur in the approved frame, so his face, eyes, fur pattern, pose and light stay pixel for pixel. MASKREF is any version of the frame where his fur colour differs (it only finds where Max is); `--maskpair A,B` takes the mask from another pair of the same composition. **Never fix colour with a model edit** (21 Oct: cream bibs, white muzzles, a realistic head). Check by eye next to BO-6.
11. **The whole frame came back with a colour cast** (pink/magenta whites after a 4k re-add): `python3 scripts/colormatch.py APPROVED.jpg RESULT.png OUT.jpg`. This undoes the model's drift toward the approved frame; it is not a grade. Then, if you only need Max from the new frame, paste his region with step 7.4.

## C2 · Three styles
11b. When the Daylight frame is approved, make **Cinema** and **Evening** by relighting it (prompt 5.6), then check: (a) the light is the same over the whole frame (no daylight left on one side, shadows match the named lamps, faces lit from where the lamps are); (b) Max's fur next to BO-6 on one board, by eye, and measured with `python3 scripts/measure_fur.py FRAME.png BOX --mask MASK.png --style cin|eve`; (c) his face at 100%. If Max's colour is off in Cinema/Evening, fix it with `scripts/recolor_max.py` on that frame. **Compare Max's head and fur pattern with the approved Daylight frame at 100% for every relight and every fix before showing anything** (21 Oct: 07 Cinema came back with a realistic head and was missed on thumbnails).

## D · Hand over
12. **Review board as JPG** (never HTML): full frame before → after, plus Max's head next to the reference head, labelled. `scripts/board.py`.
13. **Record** for every approved frame: model, params, every job id (generation and each fix pass), references attached, the crop box used, and the reviewer's verdict. Keep it in the spec next to the images (the brand repo's `references.md` §15 is the model). Do not commit large PNGs.

## What not to do (each one cost a round)
- Do not blend two versions of a face pixel by pixel (ghost edges). Replace the whole crop.
- Do not trust strength words ("subtle", "medium"): order takes by the measured change instead.
- Do not run a face match against a neutral or "series" face: the brand owner rejected the neutral-face round on 20 Oct (Max lost his emotion). Match to an approved head that already has the frame's emotion.
- Do not use EX-01 as a face reference (teeth come back).
- Do not let an edit touch glass, fog or water without naming the layer as "keep".
- Do not add grain or a grade. Frames are used as generated (the only colour tool on Max is `recolor_max.py`).
- Do not pick takes from thumbnails. Max's head and fur pattern are checked at 100% against the approved frame, every time.
