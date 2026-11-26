# Girlshell Vault

A worldbuilding vault for girlshell-inspired lore. Separate from the Chronicler (Luminara) vault by design.

## Era scope and sibling vaults

The two vaults split LUMINARA history by era. Ruled by Cecìl on 2026-11-26.

- `~/Documents/Chronicler/Luminara/`: E1 FOUNDING ERA and E2 KINGDOM ERA, years 1 to 599.
- `~/Documents/Chronicler/Girlshell/`: E3 COUNCIL ERA, year 600 onward.
- Year numbers do not reset at era boundaries. E1 covers years 1 to 299, E2 covers 300 to 599, E3 begins at 600.
- Era and event data live in `Meta/Luminara Timeline.json` and `Meta/Luminara Timeline.md`, stored at the same relative path in both vaults. The two `.md` copies are byte-identical shared reference material, not era-scoped articles.

## Conventions
- Markdown + YAML frontmatter (`title:`, `tags:`) + `[[wikilinks]]` + leading flavor blockquote (`>`).
- No em dashes in vault files.
- Explore first, scribe later: nothing is written as canon until Cecìl says "scribe this."
- When scribing, fill in details under the headers defined in `_system/templates/` (Character, Locations, Organizations, Technology). Empty headers are fine; do not pad with invented content, but populate what the user supplies under the existing structure.

## Folders

- `Characters/`: named individuals. Artemis, The Princess, Ampersat, Metiz Sanchez, Sakuya the Artificer, Circei.
- `Technology/`: the era's machinery and its conceptual layer: devices, protocols, practices, and systems. IPv7, The Palladium, X0_anon, Shell Pilots, Driver, Communication with Animals, Pass-Through, Hands-Free, LUMINET, LITEBOW, ACE.
- `Locations/`: geography. District E, Island of Angels.
- `Events/`: things that happened or are happening: coups, customs, and eras of drift. The Coup and the Council of Angels, Romantic Duels, Language Drift of the Council Era.
- `Classes/`: groups defined by innate or biological characteristics, or by a shared culture. The members did not choose to be in them, and the group is not an institution. Harpies, Luddites, Romanticists.
- `Organizations/`: groups with institutional presence: a body, a hierarchy, a membership, a name it answers to. Gorgon Operations Koros, The Council of Angels, the Foundation.
- `Meta/`: author-side tooling, themes, and session logs.
- `images/`: image assets, referenced by filename from the vault root, never moved.

### The Classes and Organizations rule

The dividing line is involuntary composition versus institutional presence.

A **Class** is a set of people who share something innate, biological, or cultural that they did not choose. Harpies are a Class because harpyhood is a transformation of the individual, not an enrollment. The Luddites and Romanticists are Classes because they are cultures, people grouped by how they live rather than by an organization they joined. A Class can be hunted, but it cannot be summoned to a meeting.

An **Organization** is a body with institutional presence: a hierarchy, a membership roll, a chain of command, a name it answers to in a corridor. GOK is an Organization because it has a roster and a mission. The Council of Angels is an Organization because it sits, rules, and issues orders. An Organization can be infiltrated, defunded, or overthrown.

When a group could be either, the test is: does it have a door, or is it a description? A door means Organization. A description means Class.

### Link and filename rules

- Wikilinks resolve by **filename only**. Renaming a file does not break inbound links, because Chronicler matches on the name of the file itself, not its path.
- Wikilinks resolve by **filename alone**. A link never needs a path prefix: `[[IPv7]]` reaches `Technology/IPv7.md` from anywhere in the vault, and moving a file between folders breaks no inbound link.
- The filename is the canonical form. A link never carries a path prefix; the name alone is the address. The name `IPv7` reaches `Technology/IPv7.md` wherever that file sits.
- Keep basenames unique **case-insensitively** across the whole vault. `IPv7.md` and `IPV7.md` would be two files resolving to the same link, and one would shadow the other.
- Images resolve through the vault config's `imageImportDir` (`images`), not relative to the article's folder. `src="GOK-dark.png"` works from any folder.

## Source material
- `~/Documents/Misc/Girl Frame 2026_03_15.pdf`: the TTRPG (PbtA: Girls pilot Vital Frames against Gorgons from Voidspace, under the Foundation and their Handlers)
- The Vital Frontier chapter in `~/Desktop/Luminara Story Bible.pdf` (if this lore connects to Luminara's future)

## Status
- Created 2026-09-22 during a creativity session.
- Folder structure reorganized 2026-10-23 into Characters, Technology, Locations, Events, Classes, Organizations, Meta.

## Log and callout conventions

Custom log blocks are styled via `.chronicler/snippets/lilith.css` (must be enabled in Settings → CSS Snippets). Use HTML divs with the matching class:

- `<div class="log-info">` — `ℹ | ΓΟΚ Internal Database` (pastel blue)
- `<div class="log-warning">` — `WARNING| ΓΟΚ Internal Database` (amber)
- `<div class="log-hazard">` — `⚠ HAZARD| Poses a threat to Gorgon Operations` (reddish-purple)
- `<div class="log-confidential">` — `CONFIDENTIAL| ΓΟΚ Internal Database` (red/magenta)
- `<div class="log-personnel">` — `p | ΓΟΚ Personnel Directory` (green)

Each block carries its own border, gradient, and dimmed body text automatically. The prefix is inserted via CSS `::before`.
