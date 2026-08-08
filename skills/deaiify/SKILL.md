---
name: deaiify
description: Strip AI-tell typography (em dashes, en dashes, curly quotes, the single-character ellipsis, non-breaking and thin spaces) from files or text and replace it with plain ASCII, so published writing reads as hand-authored and contains nothing the author couldn't type on their own keyboard. Use when asked to "de-AI-ify", "remove the em dashes", "clean up the punctuation", "make it look human-written", or before publishing site copy, docs, or a README.
---

# Slow AI - De-AI-ify

You are applying the **Slow AI** working method to prose. The principle: if you
can defend every line of code, you should also be able to claim every line of
text. A handful of characters are dead giveaways that text was machine-written -
mostly because almost nobody can type them: the em dash, curly quotes, the
single-character ellipsis, invisible spacing characters. This skill removes
them.

## Step 0 - Gather context

If not already provided, establish:

- **Scope** - which files or directories (default: the project's prose surface:
  `*.html`, `*.css`, `*.md`, `*.js`)
- **Keep-list** - intentional design glyphs that must survive (arrows in UI
  chrome, list-bullet characters, box drawing). Ask if the project has any.
- **Language** - accented letters of the author's language (`é è à ç ö ñ ...`)
  are typeable and correct. They are never stripped.

## The rules

Replace every occurrence:

| Character                             | Replace with   |
| ------------------------------------- | -------------- |
| `—` em dash                           | `-` hyphen     |
| `–` en dash, `‒` figure dash, `―` bar | `-` hyphen     |
| `…` ellipsis character                | `...`          |
| `"` `"` curly double quotes           | `"` straight   |
| `'` `'` curly single / apostrophe     | `'` straight   |
| non-breaking / narrow / thin space    | ordinary space |

**Tilde `~` is flagged, not auto-replaced**, because the fix depends on
meaning: `~40 MB` should become `about 40 MB`, not `-40 MB`. Reword by hand.

**Never touch** the keep-list glyphs or accented letters. A stripped `é` is a
spelling error, not a cleanup.

## How to run

The deterministic helper lives next to this file - it does the mechanical
swaps so no judgment (and no rewriting) is involved:

```
# Report what would change, per file (no edits):
python3 deaiify.py --check

# Apply to the default file set (*.html, *.css, *.md, *.js;
# skips .git, node_modules, build outputs):
python3 deaiify.py

# Apply to specific files only:
python3 deaiify.py path/to/file.md
```

Copy `deaiify.py` into the project (or run it from the skill directory with
file arguments). After it runs, it lists any files still containing `~` so
they can be reworded by hand. Then re-read the touched prose: a spaced em dash
that became ` - ` occasionally reads better as a comma or a rewritten
sentence.

## The standing rule

This is not only a cleanup tool. When this skill is active in a project,
**generate clean text from the start**: plain hyphens, straight quotes,
three-dot ellipses, ordinary spaces - in copy, docs, comments, and commit
messages. The best de-AI-ify run is the one with nothing to do.
