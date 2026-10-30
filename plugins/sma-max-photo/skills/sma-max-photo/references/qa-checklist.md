# QA checklist: every frame with Max · kit v1.6 (22 Oct 2026)

**New frames (twin method): first drop the clear rejects listed in `references/pipeline.md` §A0 step 6, then let the brand owner pick from a `scripts/twin_board.py` board. Do not issue an "is this our Max" verdict yourself: on 29 Oct an agent's verdicts matched the owner's on 11 of 20 frames.** The full table below is for approved frames and their relights.

Open the full-resolution file. For check 4, draw the ruler first: `python3 scripts/ruler.py FRAME.png RULER.jpg [x0,y0,x1,y1]` and read the y of the adult's crown and shoes and of Max's crown and paws. Zoom on Max to 100%. Put his head next to the reference head (`assets/refs/`) on one board. Check in this order; the first failure decides the fix (`references/pipeline.md` §C).

| # | Check | Pass | Fix if it fails |
|---|---|---|---|
| 1 | **Animated, not a real dog** | Cartoon eyes with visible whites, oversized matte nose | Regenerate; keep the "clearly an animated character" anchor |
| 2 | **Same face as the reference** | Skull, muzzle length/width, eye size and set, brow, nose match TA-5 / the approved head at that angle | Step 7: face from an approved head on a crop |
| 3 | **Adult, not a puppy** | Head (crown to chin) 0.20–0.24 of sitting height, about 1/5; muzzle almost half the head; long legs (`max-model.md` §2) | Step 8: remove + re-add, describe the body |
| 4 | **Size and place against a person** | Measure with `scripts/ruler.py`. **Place:** his paws on the ground line of the named adult's shoes (within about 2% of the frame height), never lower in the frame (= nearer the camera). **Size, sitting:** crown to paws 0.50–0.60 of that standing adult's height (approved SC-1: 0.55–0.57; his crown at the adult's hip); next to a seated or crouching adult, crown below their shoulders. **Standing:** crown 0.42–0.52 of the adult's height. **Lying:** skull (without ears) about as wide as the adult's head. Do NOT judge by head height: in SC-1 his head with ears is about as tall as an adult's head | New frame: discard the take and generate again (twin method, pipeline §A0); never resize or paste Max (step 8a withdrawn 29 Oct) |
| 5 | **Mouth** | Matches the emotion asked for: closed smile, or open with tongue (teeth are fine in joy / excited / trot) | Step 9 single edit |
| 6 | **Emotion** | One of the 8 (EX-01, 02, 03, 04, 06, 07, 08, 10) and the one the scene asked for; never sad, scared, guilty, aggressive; no folds on the face | Step 9 single edit; or step 7 with a head that has the emotion |
| 7 | **Collar and tag** | Navy leather collar (not bright blue), ONE ROUND dull-brass MEDAL tag (coin-shaped disc, raised rim, small embossed M), NOT a letter-shaped M charm (may hide only when lying) | Single edit: "make the collar navy blue leather" |
| 8 | **Fur** | Matte, strands visible, not glossy, not plush, neck/chest no fluffier than BO-6 | Regenerate; fewer edit passes |
| 8b | **Fur colour** | Next to BO-6 by eye, and `scripts/measure_fur.py … --style day\|cin\|eve` inside the band (Daylight 28–33°, Cinema 26.5–30.5°, Evening 19–28° on the lit side) | `scripts/recolor_max.py` with a whole-silhouette mask (pipeline step 10b); never a model edit |
| 9 | **Light and contact** | Same light direction and softness as the people, contact shadow, not brighter or more saturated than the scene | Step 10 integration edit |
| 10 | **The rest of the frame** | Cast not swapped, hands and fingers right, cars unbranded with correct anatomy, no readable text, glass/fog layers intact | Single edit or regenerate |
| 11 | **Edit seams** (after a crop paste) | No visible box edge, no second collar, no ghosted outline | Redo the crop with a larger box; paste with `FULL=1` |
| 12 | **Series** | At least 4 different emotions, at most 2 frames with the same head angle | Re-plan the next frames |

Never say a frame is clean before checking it at 100%. A wrong "clean" is worse than "not checked yet".
