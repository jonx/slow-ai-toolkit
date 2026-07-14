---
name: docs-refresh
description: Apply the Slow AI docs-refresh protocol when the user wants a project's README or documentation rewritten, updated, or brought back in line with the code. Use when they say "rewrite the readme", "update the docs", "the readme is out of date", "make the readme presentable", "document this project properly", or before shipping, publishing, or handing off a repo. The protocol verifies docs against the actual code first, then rewrites around three questions — what is this, where is it going, where is it right now — with a confident project-not-journey tone: no war stories, no debugging sagas, no changelog narration.
---

# Slow AI — Docs Refresh

You are applying the **Slow AI** working method to a project's documentation. The principle: documentation that contradicts the code is rot, and a README narrates the *project*, never the *journey*.

## Step 0 — Gather context

If not already provided, ask as a single grouped question:

- **Audience** — newcomer, reviewer, customer, teammate, future self
- **Scope** — README only, or all docs (CONTRIBUTING, architecture docs, doc comments)
- **What to preserve** — badges, licensing text, credits, anything contractual
- **Tone target** — default is confident and forward-looking; note any deviation
- **Known lies** — anything the user already knows is stale

## Step 1 — Verify docs against reality

Read the current docs, then verify each factual claim against the codebase:

- **Build/run instructions** — do the commands exist and succeed? Run them if possible.
- **Feature claims** — does the code actually implement each documented feature?
- **Structure claims** — does the described architecture match the real file tree?
- **Status claims** — is anything described as working that isn't, or vice versa?

Produce a discrepancy list: stale / missing / wrong / undocumented-but-important. Also skim `NOTES.md` if present — it's the source of truth for status and deferred work.

## Step 2 — Propose the structure

The README answers three questions, in order:

1. **What is this?** — the project, the problem it solves, why it exists. A newcomer understands in one paragraph.
2. **Where is it going?** — the vision, the intended end state, the roadmap shape.
3. **Where is it right now?** — factual, specific status ("boots to shell on QEMU virt; graphics not yet implemented"), neither apologetic nor inflated.

Plus the practical sections the project needs: getting started, usage, the observation harness if one exists (see the give-eyes skill), contributing, license.

Show the proposed section outline and the discrepancy resolutions. Wait for approval.

## Step 3 — Write

Tone and content rules:

- **No journey.** No development history, war stories, failed approaches, or "we struggled with X" narratives. Decisions live in `NOTES.md`; the README describes what *is*.
- **No changelog prose.** Historical detail that matters goes in a separate HISTORY/CHANGELOG file.
- **Status is honest and dated implicitly by the repo state** — specific claims a reader can verify, not hedged vibes.
- **Every command shown must have been verified in Step 1.** A README with broken install instructions is worse than no README.
- **Concise and scannable** — a reader skimming for 60 seconds gets the three answers.

## Step 4 — Verify the result

Re-run the getting-started path exactly as the new README describes it, from the reader's point of view. Fix any gap between the words and the reality — in the words, or by flagging the code gap to the user (never by silently "fixing" code; that's out of scope for this skill).

## Ongoing discipline

After this refresh, docs re-verification joins the per-chunk loop: any chunk that changes behavior ends by checking whether the README still tells the truth, and updating it in the same chunk if not.

## Full method

See [METHOD.md](../../METHOD.md), section "Docs are part of the codebase."
