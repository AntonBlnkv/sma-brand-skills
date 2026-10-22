# Max model: who he is and his numbers

*Excerpt from the SMA brand spec `max.md` v3.7 (§1 and §2), for the `sma-max-photo` skill. Scale lines are in `prompts.md` §3. Paths are relative to the skill folder.*

## 1 · Who he is
One adult male golden retriever, about 4 years old and about 30 kg. He is a stylised Pixar-quality 3D character composited into real photographs, and the only stylised element in the frame (the GEICO-gecko model).

Source lineage: the continuity model by the SMA animation team → the in-scene look → master frame `MX3-BO-6` (`assets/refs/MX3-BO-6-gpt25-sunburst_MASTER.jpg`).

**Canonical face = `MX3-TA-5`** (brand owner: narrower than the faces in the turnaround TA-0; "take this one"). The Max block (`prompts.md` §2) asks for it in words because the Element alone averages the faces.

## 2 · Numeric model
Measured on the Element frames `MX3-TA-2` (front, sitting) and `MX3-TA-1` (side, standing), ±10%. **W = height at the withers.** Reference images: `assets/refs/MX3-TA-1-side-wheel.jpg`, `assets/refs/MX3-TA-5-head-front.jpg`, board `assets/boards/01-max-reference.jpg`.

| Parameter | v3 target | Reject if |
|---|---|---|
| Height at withers | 58 cm (= W) | — |
| Crown, sitting | ≈80 cm = a standing adult's hip = a kitchen tabletop | above the hip |
| Next to a seated adult | head no higher than their lower chest, below the top edge of a laptop on their knees | at chest, shoulder or face level |
| Head (crown → chin), front, sitting | 0.20–0.24 of sitting height (measured 0.21) | > 0.27 (puppy) |
| Head length, profile | 0.45–0.55 W | > 0.65 W |
| Muzzle (stop → nose tip) | 0.40–0.45 of head length; fairly narrow, as in TA-5 | < 0.35 (puppy) or wide and flat |
| Foreleg, elbow → ground | 0.48–0.55 W (measured 0.49) | < 0.45 W |
| Body, chest → rump | 1.1–1.25 W (measured 1.2, fur included) | < 1.0 (square, puppy) |
| Nose | 0.40–0.44 of skull width (measured 0.42), matte dark brown ≈ `#2E261B` | glossy or small |
| Eyes | 0.13–0.16 of skull width (measured 0.15), brown iris, whites visible, gap ≈ 1.9 eye widths, set ≈ 37% down from the crown | > 0.18 (puppy) or no whites (real dog) |
| Ears | drop ears, tip at the jaw line | erect or short |
| Tail | feathered, reaches the hock | stub, curled over the back |
| Fur colour | back ≈ `#DDAE67`, shadow side ≈ `#B6893C`, cream chest and feathering | orange, red or grey cast |
| Collar | navy leather, never bright or royal blue | light blue, missing |
| Tag | round brushed brass with an embossed M, ≈ 0.27 of skull width, hanging at the chest | missing, square, gold-shiny |

**Fur material.** Dense, soft, completely matte feature-animation groom: fine strands with natural clumping, longer feathering on the chest, ears, back of the legs and tail, a soft sunlit rim. Reject any specular sheen, smooth vinyl or clay surface, or a blobby plush-toy look.

**Fluffiness.** The brand owner finds the turnaround "a bit too fluffy, but fine if that is our style". It stays as is. An attempt to tone it down ("medium-length tidy coat, not overly fluffy") coincided with Max turning into a realistic dog. That run was on the rejected v3.1 Element, so the phrase is not proven guilty, but it is not used.

**TA-2 caveat.** The brand owner reads the front-sitting TA-2 as having a slightly long neck or body. The measurements are inside the norms, so it stays in the v3 Element. Watch for a long neck in front-on sitting frames.

**What made v2 read as a puppy** : a head about 0.30 of sitting height, a short muzzle, eyes larger and set lower, short legs. Each is now a row in the table above.

