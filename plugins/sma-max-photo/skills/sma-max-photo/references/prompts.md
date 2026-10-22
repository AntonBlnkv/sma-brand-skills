# Prompt blocks · SMA Max kit v1.6 (22 Oct 2026)

All prompts are English. Model: **Nano Banana Pro** (`nano_banana_pro`; Higgsfield reports it as `nano_banana_2`). Single frames 2k, scenes on a location plate 4k. Aspect 3:2 unless the format says otherwise. Ids are in `references/refs.md`. Paths are relative to the skill folder.

## 1 · Scene prompt, in this order
Camera → style line → scene → Max block (§2) → cast → light/QA tail. Camera and style go first: placed at the end of a long prompt they are ignored (brand repo `references.md` §14).

**Camera** (example): `Candid documentary photograph, handheld at eye level, 35mm lens, f/2.8.`

**Style line** (D = Daylight, A = Cinema, C = Evening; the scripts call them `day`, `cin`, `eve`). Every scene ships in all three: generate in D, then make A and C by relighting the approved D frame (5.6). Frame codes end in the same letter (P07D, P07A, P07C).
- **D · Clean Daylight:** `CLEAN DAYLIGHT: bright natural late-morning daylight from one clear direction with real shadows, neutral daylight white balance, true whites, clean blue sky, fresh greens, natural colours, crisp digital capture, no grain.`
- **A · Cinematic, softer:** `CINEMATIC FILM STILL with a restrained grade: only a gentle hint of teal in the deepest shadows, natural warm skin, medium-soft contrast, subtle halation on highlights and soft oval bokeh; filmic but natural, not stylised.`
- **C · Evening:** `EVENING, BLUE HOUR: deep blue dusk outside, warm tungsten lamps glowing inside and falling on the people and on Max, soft low light, cosy and calm.`

**On a location plate**, the plate fixes the camera and the light: write the camera line as `Camera exactly as in the first reference photo.` and use style D only with a daylight plate.

**Fill every slot.** Every `{…}` in a block (POSE, EXPRESSION, MOUTH, SCALE, and `{object}` / `{person}` inside some emotion texts) must be replaced; no braces or brackets may stay in the final prompt.

**Scene:** 2–4 sentences: the moment, one action with a consequence, two story objects, nobody looks at the lens. On a location plate, start with: `In the exact location of the first reference photo (keep the place, camera and light exactly)…`

**Cast** (paste the whole line, wardrobe included; these are the lines used in the 22 Oct tests):
- Family: `The same Black mom, dad and toddler as in the reference photo: <<<38f73cfe-d229-4034-a7f3-45c97bbe959e>>> mom, <<<463e9ac3-b5de-4a49-afe3-cdd8ee075f2d>>> dad, <<<509bd9ee-cdf0-457f-a2d4-7ec63b36ca8b>>> toddler. Wardrobe: mom light-blue denim shirt over a white tee and jeans; dad navy jacket, white tee, khaki-grey trousers; toddler light-blue tee, beige trousers.`
- Woman driver: `The same woman as in the reference photo: <<<b35dc1c6-598f-4ccc-9df1-e941ef01c332>>>, late 30s, brown hair pulled back, white shirt, sky-blue sweater over the shoulders, light jeans.`
- Only one cast per frame: the family OR the woman (Phase 1). Write "a family kitchen with white cabinets", never "a white family kitchen" (the cast gets swapped).

**Tail:** `Max is lit by exactly the same light as the people, with a contact shadow, and the scene's colours reflected in his eyes and nose. Nobody looks at the camera. No logos, no readable text.`

## 2 · Max block (paste verbatim, fill the four slots: POSE, EXPRESSION, MOUTH, SCALE)
> {POSE: where he is, how he is placed, **at the same distance from the camera as {named person}** (NOT in the foreground), filling at least a third of the frame height}: <<<01ba1fc5-227c-439d-aa29-47ada4e45545>>> — Max, the SMA mascot, looking EXACTLY like the attached master photo (same face, same fur length and texture, same colours, same proportions); use the master photo for his LOOK ONLY, NOT for his pose, head angle or camera angle: a stylised Pixar-quality 3D animated golden retriever composited into this real photograph, clearly an animated character, NOT a real dog. Fully grown ADULT male of about 30 kg, NOT a puppy, with the body proportions of the attached SIDE-VIEW photo of Max (his whole body in profile): long legs (front leg from elbow to ground about half his shoulder height), deep chest, body clearly longer than it is tall, long tapered muzzle (almost half the length of his head), a SMALL head: sitting, his head from crown to chin is only about one fifth of his sitting height; NOT a big round puppy head, NOT short stubby legs, NOT chubby. Face as in his front close-up reference: refined, fairly narrow muzzle. Cartoon brown eyes with visible whites (medium-small, not puppy eyes), both pupils centred and looking the same way, oversized matte dark-brown nose, soft drop ears. Navy blue leather collar with ONE ROUND brushed-brass MEDAL tag hanging from a small ring at the front: a flat coin-shaped disc with a raised rim and a small embossed letter M in its centre, about as wide as his nose; NOT a letter-shaped M charm, NOT a cut-out letter, NOT square, NOT shiny gold. Fur: dense, soft, MATTE feature-animation groom with fine strands and natural clumping, honey-gold back fading to cream chest; NOT glossy, NOT plastic, NOT a plush toy. Expression: {EXPRESSION, §4}. {MOUTH: for an open-mouth emotion write `Mouth softly open, pink tongue just showing, NO teeth visible.`; for a closed-mouth emotion write `His mouth stays CLOSED: lips together, no teeth, no tongue.`} SCALE: {SCALE line, §3} His whole body is clearly smaller than an adult's. Soft contact shadow, lit by the same light as the scene. He is the only stylised element and the only warm-coloured object in the frame.

**The Max block is for Daylight generation and for re-adding Max (5.2).** Cinema and Evening are never generated from scratch: they are relights of the approved Daylight frame with prompt 5.6, which does not repeat the Max block, so "the only warm-coloured object" never meets warm evening lamps. In a lying pose or a wide room shot, drop "filling at least a third of the frame height" from POSE: the true size comes first (`pipeline.md` step 3).

**Tag and proportions (brand owner, final test 22 Oct):** "round brass M tag" was drawn as a letter-shaped M charm (F2, all three styles), and "adult, small head" in words still gave a puppy (F4: big round head, short muzzle). The block now describes the tag as a round medal with an embossed M and gives the head/leg/muzzle ratios from `references/max-model.md`, with TA-1 attached for proportions. Avoid "playful" in the head-tilt expression: it pulls toward a puppy.

**Joy and excitement open the mouth anyway (final test 2, 22 Oct):** with the MOUTH slot set to CLOSED, EX-01 (joy) and EX-04 (excited) still came back with an open mouth and teeth in 4 of 4 frames; listening (EX-08) and head tilt (EX-02) stayed closed there, but in the English skill test (22 Oct, S2) head tilt still came back with teeth in 1 of 2 takes. For EX-01 / EX-04 keep the open-mouth EXPRESSION text and the open MOUTH line, and plan the mouth pass (5.4, on a wide crop that holds the whole head and collar) as a normal step, or choose a calmer emotion.

**Mouth slot (final test, 22 Oct):** the old fixed line "If he smiles: mouth softly open, pink tongue just showing" overrode every closed-mouth expression: 4 of 8 frames came back with teeth although the expression said CLOSED. Fill the MOUTH slot to match the expression; never leave the open-mouth sentence in a closed-mouth prompt.

**Placement rule from the skill test:** never place Max on the camera side of the people or the furniture ("on the rug in front of the sofa" put him in the foreground and he came out too big in 2 of 2). Put him **beside or behind** a named person, at that person's distance. Prefer plates that already show room for people; a tight close-up plate (L6c) was redrawn wider in 2 of 2.

**Attach (`image_references`, role `image_references`), in this order:** 1) the location plate (if any), 2) BO-6 master `3394863f-6981-426a-a55e-6400056a0900`, 3) the approved cast frame (family `f12d9610-9e69-445d-9292-a4e8cf0c32ac`, woman `7583f0c7-5027-49dd-b5ec-eebc7b862c1d`). 4) **TA-1 side view `dc637319-6e29-4660-b100-7e815f154601` for his BODY PROPORTIONS** (the Max block refers to it as "the attached SIDE-VIEW photo of Max", not by number, because with a plate it is the 4th image and without one the 3rd; added 22 Oct after a puppy-proportioned Max in the final test F4). If you also need a pose reference (e.g. an emotion frame from `refs.md` §4), attach it LAST and add to the prompt: `Use the last attached image for his POSE only, not its light, setting or camera angle.`

## 3 · Scale lines (anchor to an object in the frame)
| Key | SCALE text |
|---|---|
| `sit` | real golden-retriever size; sitting, the top of his head is at a standing adult's hip, about 80 cm from the ground; next to a seated adult his head is no higher than their lower chest. |
| `sit-kitchen` | a FULL-SIZE ADULT golden retriever of about 30 kg, NOT a puppy: sitting, the top of his head is level with the kitchen counter / tabletop (about 78 cm) and with the standing adult's hip. |
| `sit-by-sofa` | the top of his head is clearly BELOW the top edge of her open laptop screen; his head is far below her shoulders. |
| `sit-highchair` | sitting, the top of his head is level with the high-chair tray; his whole body is clearly smaller than the dad. |
| `stand` | standing, his shoulders are just above a standing adult's knee (about 58 cm) and his head reaches mid-thigh. |
| `lie` | lying, nose to tail-base he is about 1 metre long, roughly an adult's leg from hip to heel. Stretched out, NOT curled into a ball, long front legs forward. |
| `car` | standing beside a car wheel, his back is just below the top of the tyre. |
| `car-seat` | lying along the rear seat, his body fills the seat from the mom's thigh to the child seat; his head is as big as the mom's head. |

## 3b · Size check against a person (measured on the kit test, 20 Oct)
The brand owner's check of T1a vs T1b: T1a is right, T1b is too big. Use these ratios when Max is at the **same distance from the camera** as an adult:
- his skull (without the ears) is about as wide as the adult's head; with the ears about 1.4–1.6× the adult's head width;
- lying, nose to tail-base about 0.9–1.0 m: about the adult's leg from hip to heel, about 40–45% of a 3-seat sofa;
- sitting, the top of his head is at the standing adult's hip (about 80 cm); standing, his back is just above the adult's knee.
T1b failed all three: head about 2× the woman's, body about 1.3 m, because he was placed between the sofa and the camera.

## 3c · Max's fur colour follows the light (measured on all approved frames, 20 Oct)
Measured as hue (H, degrees) of the fur's mid-tone; master BO-6 = H 30–31°. Paste the matching line right after the Max block (the block itself stays verbatim), and check the frame with `scripts/measure_fur.py`.
| Light / style | Fur looks | Target H (mid-tone) | Prompt line |
|---|---|---|---|
| **Daylight** (sun or bright window) | honey-gold, yellow-gold, cream chest; bright outdoor sun = paler and yellower | **28–33°**, never below 28 | `his fur is a warm honey-gold (yellow-gold, cream chest) like the master photo, NOT orange, NOT red-brown` |
| **Cinema** (low golden sun) | the daylight honey-gold, warmed only slightly: soft golden highlights where the sun hits | **26.5–30.5°** | `his fur stays the honey-gold of the master photo, warmed only slightly by the low golden light, soft golden highlights where the sun hits; NOT orange, NOT more saturated` |
| **Evening** (warm lamps + blue dusk) | honey-gold with soft warm amber highlights where the lamp falls, a slightly darker gold in shadow; never orange all over, never grey-brown | **19–28°** on the lit side | `he is lit by the same light as the people: gentle warm highlights where the lamp light falls, slightly darker in shadow; his fur stays the honey-gold of a golden retriever, NOT orange, NOT red-brown` |
**Evening is checked on the lit side** (the brightest quarter of the fur pixels): a dusk frame is mostly shadow, and shadow always measures lower. 06 Evening measures 18° overall but 21° on the lit side (fine); 04 and 05 stay at 17–18° even on the lit side (red-brown, fix).
**Hue alone misses it (brand owner's review, 21 Oct).** Several frames inside the bands still read too orange to the eye, because the fur was too saturated, not too red. Judge Max next to BO-6 on one board; the numbers are a rough screen only.
**Words that backfired (21 Oct):** "his fur glows orange-amber" in an evening prompt made Max orange in most evening frames; "a cream muzzle" in a colour fix painted a white muzzle (05); asking to fix a "too yellow" Max overshot into orange (09), so ask for "a SMALL change" and "keep his fur markings exactly as they are".
A frame whose Max is off-colour is fixed with `scripts/recolor_max.py` (`pipeline.md` step 10b), never with a model edit. Board: `assets/boards/08-max-colour-by-light.jpg`.

## 3d · Three styles per scene
Every scene exists in **Daylight, Cinema and Evening**. The reliable way (tested on 9 location scenes, 20 Oct): approve the Daylight frame first, then make Cinema and Evening by **relighting that frame** with prompt 5.6. The composition, people and Max stay; only light, time of day and colour change. A fresh generation with the Daylight frame as reference drifts more (Max came out redder: H 18° in evening): do not use it.

## 4 · The 8 emotions (EXPRESSION slot; tested text)
| Code | Text |
|---|---|
| EX-01 joy | pure joy: mouth open in a big happy cartoon grin, pink tongue out and slightly to one side, NO teeth visible, eyes OPEN and bright with clearly visible whites (NOT squinting), brows lifted happily, ears relaxed back |
| EX-02 head tilt | curious head tilt: head tilted about 25 degrees to one side, one ear lifted slightly higher than the other, a small calm closed-mouth smile, eyes bright and interested (not startled, not worried); a grown-up dog's curiosity, NOT puppyish |
| EX-03 chin on paws | lying flat on his belly with his chin resting on his crossed front paws, eyes open and looking calmly, CONTENT: relaxed brows, a small closed-mouth smile, ears soft; calm and happy, NOT sad, NOT pleading |
| EX-04 excited | excited: mouth open in a big grin with the tongue showing and NO teeth, ears perked forward, tail held high and wagging (slight motion blur on the tail tip) |
| EX-06 trot | happy trot on all four long legs: mouth slightly open, ears bouncing, one front paw and the opposite hind paw lifted, tail streaming behind, a little motion blur on his paws |
| EX-07 dozing | peacefully dozing and CONTENT: eyes gently closed in two happy curves, a small relaxed smile, head resting on his front paws; a cosy happy nap, NOT sad, NOT sick |
| EX-08 listening | listening attentively: ears raised and pushed forward, head turned slightly toward the person, eyes focused on them, mouth closed |
| EX-10 suspicious | playfully suspicious: ONE eyebrow raised high, the other lowered, eyes in a sideways glance at {object}, a small knowing smirk with the mouth closed; comic and friendly, NOT angry |

**Skill test, 20 Oct (12 frames, brand repo `max-kit/skill-test/`):** with these texts the model gave the right Max in 12 of 12, but teeth in 3 of the 6 open-mouth frames (EX-04, EX-06), and it ignored "chin on paws" (head stayed up) and "not curled" once each. So:
- for EX-01 / EX-04 / EX-06 in a medium or wide shot, prefer the **closed-mouth version**: `…a big happy CLOSED-mouth smile with lifted cheeks, no teeth, no tongue…`; if you keep the open mouth, plan a mouth pass (prompt 5.4) on a crop;
- for EX-03 write the head position physically: `his head is DOWN: his chin rests on the floor on top of his crossed front paws, his eyes look up at {person}`.

**Chin on paws (EX-03) is unreliable:** in the English skill test (22 Oct, S3) the head stayed up in 4 of 4 takes, even with the physical head line and EX-03 attached as a pose reference. When the head-down pose matters, choose EX-07 (dozing, head on paws) or EX-08 (listening) instead, or accept the head up.

**Warm props:** the Max block says he is "the only warm-coloured object in the frame". In the scene text, give props cool or neutral colours (a green watering can, not a red one).

**The master BO-6 shows a hint of lower teeth.** Copy his look from it, never his mouth: every frame still follows "no row of teeth".

Rules: a series uses at least 4 different emotions and at most 2 frames with the same head angle. Avoid strong emotion words ("worried", "amused", "excited" alone): they put folds on his face. When his head will be small in the frame (wide shot), prefer a closed-mouth smile: open smiles at small size come back with teeth.

## 5 · Fix prompts (one change per pass)
**5.1 Remove Max** (clean in 10/10):
`Edit the attached photo: remove the golden dog completely and fill the area naturally with what would be behind him: {what is behind}. Keep everything else exactly the same: {people, props}, the light, the colours, the camera angle and the framing.`

**5.2 Re-add Max** (size, pose, position; on the clean plate). Attach: the clean plate → BO-6 → the cast frame → TA-1 side view → optionally, LAST, an approved frame where Max has the right size/pose:
`Edit the first attached photo. Output EXACTLY the same framing as the first photo: no zoom, no crop, same camera position. Keep everything the same: {people, props, light}. ADD {place}, at the same distance from the camera as {person} (NOT in the foreground): <Max block §2 with POSE / EXPRESSION / SCALE>. {Optional: copied in look and in SIZE relative to {person} from the last attached photo.}`

**5.3 Face from an approved head** (wrong face, flat face, realistic face; run on a crop, see `pipeline.md` step 7; attach the crop, then the reference head from `assets/refs/`):
`Edit the first attached photo. REPLACE the dog's head with the head of the animated dog in the second attached photo: it is the same cartoon character (Max), so copy his head design exactly: {rounded skull with a soft brow ridge, big round cartoon brown eyes with clearly visible whites, the muzzle length and width, the oversized matte dark-brown nose, the ears, the smooth golden face fur}. KEEP THE HEAD EXACTLY AS LARGE AS IT IS NOW, at the same position and angle, looking {where}. Keep his body, his single navy collar and his round brass medal tag where they are. Expression: {keep the frame's expression, e.g. a gentle happy closed-mouth smile, no teeth, no wrinkles}. Keep everything else exactly the same: {people, light, glass/fog layers named explicitly}.`
Pick the reference head with the **same expression and a similar angle** (`refs.md` §3). An expression in the reference copies onto the frame.

**5.4 Mouth / gaze / ear** (single edit; on a crop when the head is under ~500 px; for the open-mouth option attach `assets/refs/HEAD-P06C-open-smile-tongue-no-teeth.jpg` as the second image):
`Edit the attached photo. Change ONLY the dog's mouth: {a happy CLOSED-mouth smile, lips together, no teeth, no tongue | give him exactly the mouth of the dog in the second attached photo: open smile, pink tongue showing, lips covering the teeth, NO teeth visible}. Keep his eyes, brows, nose, head shape, head angle, ears, fur, collar and everything around him exactly the same, same light and colours.`

**5.5 Integration in place** (keeps pose and size; lighting only):
`Edit the first attached photo. Keep the people, the scene, the camera, the framing and the dog's pose, position, size and face exactly as they are. Change only how the dog sits in the light of this room: light him like the people ({light direction}), no bright frontal fill, his brightness and saturation no higher than {a real object in the frame}; a soft dark contact shadow under him; a faint bounce from {floor/lawn} under his chin; his collar dark NAVY (not bright blue); fur matte and edges as soft as the photo at his distance.`

**5.6 Relight to another style** (attach only the approved Daylight frame):
`Edit the attached photo. Keep EVERYTHING exactly the same: the composition, camera and framing, every person, their poses, faces and clothes, the dog's pose, size, face and expression, and every object. Change ONLY the light, the time of day and the colour of the photograph: {style line A or C from §1} {the scene's light sources: e.g. "late-afternoon low golden sun from the side, long soft shadows" / "blue hour: deep blue sky, the porch light and the garage light glowing warm on the family and Max"}. Max (the golden dog) is lit by the same light as the people: {the fur line for this style from §3c}. No text, no logos.`
Name the real light sources of the place (porch light, garage light, table lamp, dome light); evening needs at least one warm source falling on Max. Outdoors with no building in the frame, replace "lamps glowing inside" with the real outdoor sources (a street lamp, a car's interior light, string lights). The §3c fur lines say "the master photo"; in a relight only the Daylight frame is attached, so write "the attached photo" instead.
For Evening also say **"the SAME light over the WHOLE frame from the left edge to the right edge: the sun has set, NO sunlight anywhere, no sunlit patches, no hard sun shadows"**: without it the relight left the right half of 02 and 09 in daylight (a sunlit pole). Put each lamp where it is in the room and say which way its light falls ("a pendant ABOVE her, a floor lamp BEHIND her: no bright light on the front of her face"); otherwise faces get a frontal orange glow (03). Street scenes: a warm street lamp HIGH ABOVE the sidewalk casting a soft pool of light on the person and Max (09, 02); kitchens: ceiling + under-cabinet lights lighting the room evenly, "both faces lit equally well" (06). Car dome lights: "a small soft warm-white dome light (about 3000K), not an orange floodlight" (07).
After an evening relight Max can come out grey-brown (02, 09 on 21 Oct): fix with `scripts/recolor_max.py ... eve --smin 0.55`.
**Relights, from the English skill test (22 Oct):** make 2 takes per relight (Evening came out right first time in only 1 of 3). Outdoors, "the same light over the whole frame" alone left sunlit grass: also name the ground (`the whole lawn, the fence, the people and Max are in the same soft, dim blue-hour light, the grass a dim blue-green, NOT sunlit`). Put lamps on something real (`a small warm lamp mounted on the stand's wall under the awning`), never "high above" in open air (it drew a lamp floating in the sky), and expect lamps described as "out of frame" to be drawn into the frame. The 5.6 template and the §3c Evening line both say "lit by the same light as the people": write it once. "No lighter chest, belly or muzzle" means the relight must not CHANGE his fur pattern; his cream chest stays exactly as in the Daylight frame.

Every relight must also say: `The golden dog stays EXACTLY the same animated cartoon character: the same big round cartoon eyes with whites, the same face, pose and size, the same fur pattern (no lighter chest, belly or muzzle); do NOT make him look like a real dog.` Without it the 07 Cinema relight turned Max realistic.

**5.7 Fur colour fix: ⛔ do NOT use (21 Oct).** A model colour edit redraws Max: it painted cream bibs and bellies (03, 05, 07, 08, T3), white muzzles (05) and a realistic head (07 Cinema). Fix fur colour with `scripts/recolor_max.py` instead (no model; only hue and saturation of his fur move). Kept below only for history:
`Edit the first attached photo. Change ONLY the colour of the golden dog's fur: make it the warm honey-gold of the dog in the second photo, a yellow-gold with a cream chest, as he looks in bright daylight; less orange, less red. Keep his shape, face, eyes, fur texture, pose, the direction of the light and his shadows, his collar and tag and everything else exactly the same.`

**Always name glass, fog or water layers as something to keep** ("the fogged glass covers the WHOLE window in front of the dog"): edits remove them silently.
