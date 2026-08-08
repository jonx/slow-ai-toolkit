# De-AI-ify Prompt Template

Strip the typography that marks text as machine-written from this project's prose, and from now on write as if you couldn't type those characters at all. The test: nothing in the published text that the author couldn't produce on their own keyboard.

## Context

- **Project:** [name + one-line description]
- **Scope:** [files or directories to clean; default: *.html, *.css, *.md, *.js]
- **Keep-list:** [intentional design glyphs that must survive — arrows in UI chrome, bullet characters, box drawing; "none" if none]
- **Language:** [author's language(s) — accented letters of that language are correct and must never be stripped]

## The rules — apply in order

**Replace every occurrence:**

| Character | Replace with |
|---|---|
| em dash — , en dash – , figure dash, horizontal bar | `-` hyphen |
| ellipsis character … | `...` three dots |
| curly double quotes | `"` straight |
| curly single quotes / apostrophe | `'` straight |
| non-breaking / narrow / thin spaces | ordinary space |

**Flag, don't auto-replace:** the tilde `~`. The fix depends on meaning (`~40 MB` becomes `about 40 MB`, never `-40 MB`). List every remaining tilde with its file and line so I can reword.

**Never touch:** the keep-list glyphs, and accented letters of my language — a stripped accent is a spelling error, not a cleanup.

## What I want from you — in order

**Step 1 — Report.** Scan the scope and show me, per file, how many offending characters of each kind you found. No edits yet.

**Step 2 — Apply after my go-ahead.** Make the mechanical swaps exactly — no rewriting, no "improvements" — so the diff is reviewable character by character.

**Step 3 — Reword the flagged cases.** Propose a one-line rewrite for each tilde (and for any spaced em dash that would read better as a comma or a rewritten sentence). Wait for approval before applying these.

**Standing rule from here on:** in everything you write for this project — copy, docs, comments, commit messages — use plain hyphens, straight quotes, three-dot ellipses, and ordinary spaces from the start. The best cleanup pass is the one with nothing to do.
