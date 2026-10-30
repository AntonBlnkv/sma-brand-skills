# References and Higgsfield ids · SMA Max kit v1.6 (22 Oct 2026)

**These are the original ids.** On any account other than the one that built the kit, run the bootstrap first (`bootstrap.md`) and pass every id through `python3 scripts/ids.py map` / `get`. Every file behind these ids is in `assets/` (list: `assets/manifest.json`).

How to attach: in a Higgsfield generation, pass the id as `medias: [{value: <id>, role: "image_references"}]`. A job id (from a past generation) and a media id (an uploaded file) are both accepted. If a media id stops working, upload the file from `assets/refs/` again (Higgsfield `media_upload`, PUT, `media_confirm`) and use the new id.

## 1 · Always
| What | Id | File | Attach how |
|---|---|---|---|
| Max Element `SMA-Max-v3` | `01ba1fc5-227c-439d-aa29-47ada4e45545` | — | in the prompt text: `<<<01ba1fc5-227c-439d-aa29-47ada4e45545>>>` |
| Master photo `MX3-BO-6` | job `3394863f-6981-426a-a55e-6400056a0900` | `assets/refs/MX3-BO-6-gpt25-sunburst_MASTER.jpg` | every Max frame; prompt says "look only, NOT pose" |
| Canonical face `MX3-TA-5` | job `a92d51cd-bbe8-42d3-8fdd-11dae5d3c31c` | `assets/refs/MX3-TA-5-head-front.jpg` | face reference for a front-on head; also when a model has no Elements |
| Face profile `MX3-TA-6` | job `76795864-d94c-4df8-8c65-454e783ca598` | `assets/refs/MX3-TA-6-head-profile.jpg` | face reference for a profile head |
| Reference profile `MX3-TA-1` | job `dc637319-6e29-4660-b100-7e815f154601` | `assets/refs/MX3-TA-1-side-wheel.jpg` | body proportions, standing |
| Other angles | TA-2 `b51deb9d-601f-4745-9621-c64be2ae61de` · TA-3 `16f822e8-1a39-49a5-9c77-e89be4f43d1c` (its head crop: `assets/refs/HEAD-TA3-eyes-straight.jpg`) · TA-4 `48bab5dd-f301-4ba8-91e0-8eef0f4fe7bd` | full frames in the SMA brand repo `docs/brand/photo-spec/max/`) | pose or angle reference only |

**Never use:** Element `SMA-Max-v3.1` `33a3c7d0…` (turns into a real dog), `SMA-Max-v2-inscene` `a29f73eb…`, `SMA-Max-continuity` `0cd7d22f…`.

## 2 · Cast
| Who | Element | Approved cast frame (attach) |
|---|---|---|
| Family mom / dad / toddler | `38f73cfe-d229-4034-a7f3-45c97bbe959e` / `463e9ac3-b5de-4a49-afe3-cdd8ee075f2d` / `509bd9ee-cdf0-457f-a2d4-7ec63b36ca8b` | `MX3-SC-1` job `f12d9610-9e69-445d-9292-a4e8cf0c32ac` |
| Woman driver | `b35dc1c6-598f-4ccc-9df1-e941ef01c332` | `MX3-SC-3` job `7583f0c7-5027-49dd-b5ec-eebc7b862c1d` |
Paste-ready cast lines with wardrobe anchors: `prompts.md` §1. Secondary cast notes live in the SMA brand repo (`docs/brand/photo-spec/cast.md`).

## 3 · Approved heads for "face by reference" (pick the same expression and a similar angle)
| Head | Expression · angle | Id | File |
|---|---|---|---|
| P03A | soft closed smile · 3/4, eyes to the side (⚠️ the side glance copies over and reads cross-eyed; fix eyes after with TA-3) | media `09237d8e-7ab6-4691-8fab-76d3f64193af` (crop) · full frame job `951fe868-e5fd-44b6-bc31-145032bc3ca3` | `assets/refs/HEAD-P03A-3q-soft-smile.jpg` |
| P08D | content, looking up · profile | media `5ad38080-6e80-498f-aba0-77a7c6ebc526` (crop) · full frame job `f0a9f9db-b41c-40fb-86dc-297414217e0a` | `assets/refs/HEAD-P08D-profile-up-content.jpg` |
| P02A | content smile · profile, head level | full frame job `7513ef2d-00ec-4d5e-9d21-a83723a2d634` | `assets/refs/HEAD-P02A-profile-content.jpg` |
| P06C (fixed) | open smile, tongue · 3/4 (⚠️ eyes glance to the side: on a small or profile head it copies over as side-eye and a smooth head; use it for the MOUTH, not the whole head) | job `9151d439-06bd-48a5-8b2a-82a1f7c0e4e4` (crop) | `assets/refs/HEAD-P06C-open-smile-tongue.jpg` |
| P03C (fixed, accepted) | happy open smile, tongue · 3/4, evening, behind fogged glass | job `3e017010-f656-4dad-a009-52a446aec982` (crop) | `assets/refs/HEAD-P03C-evening-3q.jpg` |
| P06A (fixed, accepted) | happy open smile, tongue · 3/4 toward the camera, eyes centred | job `7e1830e4-01cc-4e2e-bfe7-47a94ed27c40` (crop); mirrored copy media `4ffcb026-c380-4238-9c57-11812e77515d` | `assets/refs/HEAD-P06A-open-smile-to-camera.jpg` |
| TA-3 (eyes) | happy, eyes straight ahead · 3/4 — use it for the EYES | media `a8f84e0e-aa01-47c7-a839-3dc904ec7f27` · full job `16f822e8-1a39-49a5-9c77-e89be4f43d1c` | `assets/refs/HEAD-TA3-eyes-straight.jpg` |
| TA-5 | neutral, friendly · front | job `a92d51cd-bbe8-42d3-8fdd-11dae5d3c31c` | `assets/refs/MX3-TA-5-head-front.jpg` |
| TA-6 | neutral smile · profile | job `76795864-d94c-4df8-8c65-454e783ca598` | `assets/refs/MX3-TA-6-head-profile.jpg` |

**Do not use as a face reference:** P09A or NREF-1 (raised brow / neutral face that the brand owner rejected on 20 Oct), any frame with folds on the face.

## 4 · The 8 emotions (pose/expression reference only, attached last; whole Max frames; never use EX-01 for a face fix)
EX-01 `5045f62c-a5b3-4074-938a-1a2c5a6dac9d` · EX-02 `0cdffd24-cf38-44a4-a8e2-7cecff505b2b` · EX-03 `3e25890e-18ca-4296-9e03-33b0595d713f` · EX-04 `9dd8e852-213f-4095-85e5-c86ece4afea6` · EX-06 `78c0534b-eb96-4279-bb99-52bfc4dc86a8` · EX-07 `453e916d-82ad-4960-9724-054784647d45` · EX-08 `6da0bc91-ca11-49d8-91af-c4d811f283f3` · EX-10 `0beeebaf-4ab9-4ae6-b173-eb3da783caa5`. Files: `assets/emotions/MX3-EX-*.jpg`, board `assets/boards/02-max-emotions.jpg`.

## 5 · Approved scene sets (the target look)
Full-resolution files of these sets live in the SMA brand repo (`docs/brand/photo-spec/`); this package carries only the overview boards.
- **Locations set** (8 scenes on location plates): board `assets/boards/06-approved-locations.jpg`; scene test T2 job `8b6bc9ef-8413-4c61-b0a7-6d8d6d4d011c`.
- **Ideas series** (11 scenes × D/A/C, 27 frames): board `assets/boards/07-approved-series.jpg`. Job ids are in the brand repo's `references.md` §15.
- **Location plates** (empty, to place people and Max into): job ids in `plates.md`; image files in the brand repo (`docs/brand/photo-spec/locations/`). Family kitchen L2a plate with the 06 cast and no Max: job `5a69a802-abf9-4c9d-90b3-61b511017f3e`.

## 6 · Codes used in this kit
| Code | Means |
|---|---|
| BO-6 | The master photo of Max (`MX3-BO-6`), attached to every Max frame for his look |
| TA-1 … TA-6 | Turnaround angles of Max (TA-1 side view, TA-5 front face, TA-6 profile face) |
| EX-01 … EX-10 | The 8 approved emotions (EX-05, EX-09, EX-11 were dropped) |
| SC-1, SC-3 | Approved cast frames: the family (SC-1), the woman driver (SC-3) |
| HEAD-… | Approved head crops used to fix a face (`assets/refs/`) |
| L1a … L7b | Location plates (`plates.md`) |
| P01 … P11 + D/A/C | The ideas series (board 07); the last letter is the treatment: D Daylight, A Cinema, C Evening |
| F1 … F4, G1 … G4 | Frames of the two final skill tests of 22 Oct (boards 13 and 14) |
| T1 … T6 | Frames of the first kit test (20 Oct) |
| NREF-1, P09A | Rejected face references: never use them |

## 7 · Who decides
- **Brand owner (the SMA brand team):** approves frames, the kit and anything outside Phase 1 (new people, new uses).
- **Copy on an image:** the SMA marketing lead. **Numbers, claims or legal wording on an image, and a child "driving":** legal review. Ask the brand owner who that is today.
