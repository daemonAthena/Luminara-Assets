# Chronicler Workflow — How to Scribe Lore

A copy-paste reference for transcribing Luminara (and any) lore into the vault
**fully locally** (W6600 / qwen2.5-7b). No cloud model touches the lore prose.

All commands assume you are in the vault root:
```bash
cd ~/Documents/Chronicler
```

> **Server check first.** Every scribing step needs the local model. If it's
> down, start it, then proceed:
> ```bash
> curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/health   # 200 = up
> systemctl --user start llama-server.service                              # if down
> ```

---

## Method 1 — Interactive TUI (recommended for live sessions)

```bash
cd ~/Documents/Chronicler && python3 harness.py
```

Key bindings (shown permanently on the bottom row):

| Key | Action |
|---|---|
| **Enter** | Run the full cycle: Route → gather context → grounding question → (pause for answer) → scribe → drift → write |
| **Tab** | Switch between LORE and ANSWER boxes |
| **Ctrl-O** | Newline inside a box (plain Enter runs the cycle) |
| **Ctrl-L** | Load a lore file (prefilled `~/Documents/`, Tab = filesystem completion, Esc = cancel) |
| **Ctrl-R** | Route only |
| **Ctrl-G** | Ground only |
| **Ctrl-E** | Scribe (dry) only |
| **Ctrl-D** | Drift check only |
| **Ctrl-N** | Next (dedupe + stubgen) |

**Typical flow:**
1. Paste lore into the LORE box, then press **Enter**.
2. A context-aware grounding question fires (if the lore is thin). The cursor
   moves to the ANSWER box.
3. Type your answer, press **Enter** → it scribes, drift-checks, writes, commits.
4. Repeat with new lore (clear the LORE box first).

> If scribing targets an **existing** article, it auto-merges (amend) instead of
> overwriting. A loss-aware drift gate warns if existing facts were dropped.

---

## Method 2 — Command line (exact copy-paste)

### Step 0 (optional) — Route: see which article(s) the lore belongs to
```bash
./.venv/bin/python route.py --lore "The Hermit Prince is a femboy reporter who travels through Luminara."
```
Prints a ROUTING PLAN: each sentence → its PRIMARY target, and `NEW:` for
entities not yet in the vault.

### Step 1 (optional) — Ground: get a clarifying question for thin lore
```bash
python3 ground.py --title "Hermit Prince" --lore "The Hermit Prince is a femboy reporter."
```
- Prints 1–2 open-ended questions, or `LORE SUFFICIENT` if rich enough.
- Add `--context-file ctx.txt` to feed existing vault context so it won't
  re-ask what's already known.

### Step 2 — Scribe (DRY RUN first — always review before writing)
```bash
python3 scribe.py --lore "The Hermit Prince is a femboy reporter who travels through Luminara, documenting the people." --temperature 0.25
```
- Auto-brackets known entities into `[[links]]`, picks folder/title, transforms
  to wiki prose. **Dry-run by default** — prints the plan + article, writes nothing.
- Override placement (skips the AI classifier):
  ```bash
  python3 scribe.py --title "Hermit Prince" --folder People --tags "people,character" --lore "..."

  ```

### Step 3 — Write (with drift gate)
```bash
python3 scribe.py --lore "..." --temperature 0.25 --write --drift-check
```
- `--write` commits to git (reversible via `git revert`).
- `--drift-check` runs the no-invention gate; warns (does not block) if the
  model added facts beyond your lore.

### Step 4 (optional) — Drift check an existing article
```bash
python3 drift.py --lore "original lore" --article People/Hermit\ Prince.md
# exit 0 = clean, exit 1 = invented
```

### Step 5 — Dedupe: fix link-form mismatches to one-click alias links
```bash
python3 dedupe.py          # dry-run: shows [[link]] -> [[canonical|link]]
python3 dedupe.py --write  # rewrites source files
```

### Step 6 — Stubs: see what's missing
```bash
python3 stubgen.py --redlinks-only --top 5
```

### Commit manually (if you edited files by hand)
```bash
python3 commit.py "describe the edit"
# undo last: git -C ~/Documents/Chronicler revert --no-edit HEAD
```

---

## Method 3 — Drop-folder (headless / autonomous)

Drop a lore file into `_inbox/` and run the headless operator:
```bash
mkdir -p _inbox
cat > _inbox/My Lore.md <<'EOF'
The Saltmarsh Pact was a treaty between the Fidelans and the riverfolk,
signed after the Blooming War along the Columbine River.
EOF

python3 cron_harness.py
```
- Processes every `_inbox/*.md` / `*.txt` through the full local loop, commits
  each, and moves the file to `_inbox/done/`.
- If the local server is **down**, it prints a clean note and exits (no crash).
- On idle ticks (empty inbox) it runs `stubgen` and reports red-link count.

---

## Amend an existing article (without overwriting)

Just scribe with the same title — it auto-merges. Or be explicit:
```bash
python3 scribe.py --title "Hermit Prince" --lore "He also keeps a journal of lantern festivals." --write --drift-check
```
The existing `People/Hermit Prince.md` body is preserved and the new lore woven
in; a loss-aware gate warns if old facts were dropped.

---

## Placement rules

| Content | Folder |
|---|---|
| Provinces / cities / regions | `Places/` |
| Individuals | `People/` |
| Events / eras / wars / coalitions / houses / institutions | `History/` |
| Peoples / ethnographies / fashion / pantheon / currency | `Culture/` |
| Author frameworks | `Meta/` |

---

## Red-link check
```bash
python3 ~/linkcheck.py        # from the vault root; lists broken [[links]]
```

---

## Cron jobs (currently paused)

Three jobs exist but are **disabled** as of 2026-08-05:
- `2737d4ee6f23` "Luminara lore questions" (9am/9pm Q&A)
- `778feeb00397` "Chronicler Harness" (headless `cron_harness.py`, every 6h)
- `d06ccd9304fb` "Luminara interactive tick" (Q&A + processes posted lore, every 2h)

Resume any with: `cronjob resume <job_id>` (or ask the agent).
