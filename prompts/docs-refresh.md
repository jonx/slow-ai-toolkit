# Docs Refresh Prompt Template

Rewrite this project's README (and listed docs) so they tell the truth and read like a project, not a diary. Verify claims against the actual code before writing. No development war stories, no debugging sagas, no "we struggled with X" — the README describes what IS, where it's GOING, and where it stands RIGHT NOW.

## Context

- **Project:** [name + one-line description]
- **Where it lives:** [path / repo]
- **Audience:** [newcomer / reviewer / customer / teammate / future me]
- **Scope:** [README only / README + these docs: …]
- **Preserve:** [badges, license text, credits, anything contractual]
- **Known lies:** [anything I already know is stale in the current docs]

## What I want from you — in order

**Step 1 — Verify docs against reality.**
Read the current docs, then check every factual claim against the code:
- Build/run instructions — do the commands exist and succeed? Run them if possible.
- Feature claims — implemented or not?
- Structure claims — does the described architecture match the real tree?
- Status claims — anything called working that isn't, or vice versa?
Also read NOTES.md if present — it's the source of truth for status and deferred work.
Produce a discrepancy list: stale / missing / wrong / undocumented-but-important.

**Step 2 — Propose the structure and wait for approval.**
The README answers, in order: **What is this?** (problem, purpose — one paragraph a newcomer gets), **Where is it going?** (vision, roadmap shape), **Where is it right now?** (specific, factual status like "boots to shell on QEMU virt; graphics not yet implemented" — neither apologetic nor inflated). Plus the practical sections this project needs: getting started, usage, observation harness if one exists, license. Show me the outline and how each discrepancy gets resolved. Do not write until I approve.

**Step 3 — Write.**
- Confident, forward-looking tone. Project, not journey. Decisions belong in NOTES.md; history belongs in a HISTORY file or nowhere.
- Every command shown must have been verified in Step 1.
- Concise and scannable — a 60-second skim answers the three questions.

**Step 4 — Verify the result.**
Walk the getting-started path exactly as the new README describes it, as a fresh reader. Fix gaps in the words; flag (don't fix) gaps in the code.

Begin with Step 1.
