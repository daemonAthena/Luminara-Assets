# Future Front-End Features (ideas, not yet built)

These are captured ideas. **Precedence (Cecìl, 2026-08-09):** do NOT build any of
these until the current multi-target / analytics work is *extensively tested*
and *committed*. They are deliberately deferred so we don't pile unfinished
UX on top of unverified UX.

---

## 1. Clickable red-links → spawn a new grounding question (NEW, 2026-08-09)

**Idea:** After a scribe write, the pipeline reports a list of RED-LINKS (wiki
`[[targets]]` that have no article yet). Today that list is inert text. Make
each red-link a clickable item that, when clicked, opens a *new* grounding
question (via ground.py, the same flow used for the main lore) to draft a
*separate* entry for that linked entity — i.e. chain from one article's
dangling references into creating the next article.

**Why:** turns the red-link report from a passive "you have orphans" notice
into an active authoring loop — click an orphan, get asked a grounding
question, scribe the new article, repeat. Natural fit for building out the
vault from a seed.

**Open design questions (for later):**
- Does clicking a red-link start a *fresh* lore session (empty lore box, just
  the entity name as the seed) or prefill the lore box with the source
  article's sentence that referenced it? Prefilling gives context.
- Should the grounding question for the linked entity draw on the *source*
  article as context (like the main cycle does via `--context-file`)?
- How does it interact with the multi-target target list? A red-link spawned
  from a multi-target article is just another entity — same flow.
- UI affordance: render the RED-LINKS block in the Live panel as `<button>`
  or `<a>` rows; clicking POSTs to `/api/ground` (or a new
  `/api/ground-from-redlink` that takes the entity + source article) and
  surfaces the question in the existing answer box / a small popover.

**Depends on:** the red-link list is already emitted by scribe.py
(`=== RED-LINKS: N ===` in stdout, parsed in web.py's write paths). The
grounding flow already exists (`/api/ground`, `/api/cycle` stage 0). So this
is mostly a front-end affordance + a small endpoint to seed ground from an
entity name + source context.

---

## 2. Grounding-question TEMPLATES the AI can pull from (NEW, 2026-08-09)

**Idea (Cecìl, mid-test):** Maintain a library of grounding-question
*templates* the AI can draw from when it needs to ask a clarifying question
(ground.py's ASK flow). Instead of the model inventing a question from
scratch each time, it selects/populates from a curated set of templates
(e.g. "When did X happen?", "Where is X located?", "Who is X's patron?",
"What caused X?"). This makes grounding questions more consistent,
on-tone, and reviewable — and lets you tune the *kinds* of gaps the pipeline
actively probes.

**Why:** the current ground.py asks whatever the model decides. Templates
give you editorial control over what facts the pipeline prioritizes filling
in, and make the questions feel like a deliberate interview rather than
ad-hoc.

**Open design questions (for later):**
- Where do templates live? A `Meta/analytics/ground_templates.md` (or
  `.json`) the pipeline loads, so you can edit them without touching code.
- Does the model *pick* a template and fill slots, or does it rank templates
  against the lore and ask the best-fitting one? Probably: model picks the
  most relevant template + fills entities from the lore.
- Should templates be per-entity-type (person vs place vs event) so a
  "setting" gets geography questions and a "person" gets relationship
  questions?
- How does this interact with #1 (clickable red-links spawning grounding
  questions)? The red-link spawn could pull a template appropriate to the
  linked entity's inferred type.

**Depends on:** ground.py's existing ASK mechanism (it already returns
questions). This is a prompt/selection layer in front of it.

---

## (Reserved)
Add new ideas below as they come up. Keep each numbered, with the date and a
short "open questions" section so the eventual build has context.
