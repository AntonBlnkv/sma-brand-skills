# Max photo kit · scope and roadmap

*Agreed with the brand owner on 22 Oct 2026. Paths are relative to the skill folder; full Element ids are in `references/refs.md` §2.*

## Phase 1 · current version (v1.6)
- **Max** with the **approved cast only**:
  - the family: mom, dad and toddler (Elements `38f73cfe…` / `463e9ac3…` / `509bd9ee…`, cast frame SC-1 `f12d9610…`);
  - the woman driver (Element `b35dc1c6…`, cast frame SC-3 `7583f0c7…`).
- **Locations can vary:**
  - the approved location plates (SMA brand repo `docs/brand/photo-spec/locations/`);
  - new places without a plate, as in the final tests (`assets/boards/13-final-skill-test.jpg`, `assets/boards/14-skill-test-2.jpg`).
- Every scene ships in three treatments: **Daylight, Cinema and Evening**.
- **Not covered:** other people. A frame with new people is outside the kit. Their faces change from frame to frame, and the people check below does not exist yet.

## Phase 2 · other people (planned, not started)
1. **Adding a new cast member:**
   - generate a portrait and a full-length frame without Max;
   - get it approved;
   - make a Higgsfield Element from those images;
   - write down the wardrobe anchor.
   This is the same path the current family and woman took.
2. **A general cast slot in the prompt.** It takes the Element ids, the approved cast frame and the wardrobe, and replaces the hard-coded family and woman blocks in `references/prompts.md` §1. Max is still placed "at the same distance from the camera as {person}", and his size is measured against any adult (`references/prompts.md` §3b).
3. **People QA:** the same people as the cast frame, no swaps, and the right number of people. A failed frame is regenerated. Even with the approved cast, 3 of 16 takes came back with other people in the 22 Oct tests.
4. **Test:**
   - 2 new casts, for example an older couple, and a father with a teenager;
   - 2 scenes each, in all 3 treatments;
   - results on board 15.
5. **Update** `SKILL.md`, the package `README.md` and this downloadable skill package (bump the version).
