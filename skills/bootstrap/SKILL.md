---
name: bootstrap
description: Apply the Slow AI bootstrap protocol when the user is starting a new coding project from scratch. Use when they say things like "help me build", "I want to create [X]", "start a new project", "I'm building a take-home / interview project / customer demo / proof-of-concept / side project", or any other signal that they're beginning a new codebase that will be reviewed, demoed, or maintained beyond the session. Walks the user through gathering context, planning across four written gates, and waiting for explicit approval before any code is written.
---

# Slow AI — Bootstrap

You are applying the **Slow AI** working method to a new-project bootstrap.

The principle: every line of generated code should be a line the user would stand by, line by line, in a code review or interview. Speed is fine; sloppiness compounded by speed is not.

Do not write any code until you have walked through Steps 1–5 below and the user has explicitly said "go build" (or equivalent explicit approval).

## Step 0 — Gather context

If the user has not already provided these, ask for them as a single grouped question (don't drip-feed):

- **Purpose** — what success looks like for this build
- **Audience for the code** — who will read it (reviewer, customer, future maintainer, future self)
- **Time budget** — hours/days, honest with buffer
- **Defensibility requirement** — will the user walk through this with someone? If yes, every line must be defensible
- **Quality bar** — readable + conventional vs. production-grade vs. throwaway
- **Target platforms / runtime**
- **Reference materials** — any existing code, setup folders, schemas, docs to read FIRST
- **The brief itself** — concrete deliverables, what's in scope
- **Extension hooks** — things NOT to build now but architecture must accommodate cleanly later
- **Non-negotiable constraints** — stack, state management pattern, architectural style (e.g. "no Clean Architecture"), file-size guidance, comment style, allowed/forbidden dependencies

Be specific about what to **forbid** — half the value of this protocol is preventing default patterns the agent reaches for from training data (Riverpod for one piece of state, repository layers in a 200-line app, premature optimization).

## Step 1 — Read reference materials

View whatever the user pointed at. Summarize in 3–5 bullets: versions/conventions/gotchas established, what minimum must be carried into the new project. If there are no reference materials, say so explicitly and move on.

## Step 2 — Propose the file/module tree

A complete file tree for the initial build. One sentence per file describing its responsibility. Group by concern (models / services / state / ui / etc.).

This list is a **contract for scope**. Implementation must not produce files not on this list without re-planning.

## Step 3 — Explain the architecture (one paragraph, ≤200 words)

How data flows: from input through to output. What state lives where, what triggers what. Call out explicitly how the extension hooks fit. If you can't explain it in 200 words, the design is wrong, not the prose budget.

## Step 4 — List trade-offs, risks, uncertainties

3–5 bullets on the main trade-offs and what the user should be ready to defend. Flag anything you're uncertain about regarding the framework/SDK/language version. If you need to verify an API surface, **say so explicitly** and propose how (e.g., "I'll read the package source at [LOCATION] before committing to signatures").

"We could revisit this later" is **not** a trade-off — name what was given up and why.

## Step 5 — Wait for approval

Stop. Do not write code. Ask the user to approve, request changes, or ask questions. Proceed only when they say "go build" (or equivalent).

## After approval

Work in small named chunks. Before generating a new file or making a non-trivial change, say what you're about to build and why. After each significant change:

- Run the analyzer/linter and any tests. Confirm green before declaring done.
- Update `NOTES.md` at the project root with one or two sentences in the user's voice: decision made, trade-off taken, surprise discovered, scope cut.

## Defaults to refuse

Unless the user explicitly asked for them, do not introduce:

- State management frameworks for one or two state surfaces (Riverpod, BLoC, Redux, MobX, Provider, Zustand, Recoil, Pinia, Vuex, etc.) — a `ChangeNotifier` / `useState` / module-level holder is almost always enough.
- Repository / usecase / domain layers in a few-hundred-line app.
- Hexagonal / Clean / Onion / DDD architectures unless complexity warrants them.
- Premature optimization (custom isolates, streaming parsers, micro-caches) before the naive version works and is measured.
- Files growing past ~200 lines without re-evaluating, or past ~800 without a clear reason. Neither is a hard cap — the discipline is noticing the size and either justifying or splitting.
- Boilerplate comments that restate the code. Comments explain *why*, never *what*.

If the prompt didn't forbid these explicitly, propose simpler alternatives in Steps 2/3 and let the user choose.

## NOTES.md template

Create at the project root with these sections, updated live as decisions happen:

```markdown
# [Project] — Architecture and Decision Log

## Architecture at a glance
[3–5 bullets, kept current]

## Key decisions
[One subsection per decision, written when made]

## Trade-offs made under time pressure
[Bullets, added when made]

## With more time, I would
[Bullets, added when something is consciously deferred]

## Things to discuss in the walkthrough
[Questions the user wants the reviewer to ask]
```

## If the work is genuinely small

If the project is a throwaway script, one-off experiment, or learning exercise, acknowledge the skill is active, ask whether the gates apply, and respect a no. The method is for code that will outlive the session.

## Full method

See [METHOD.md](../../METHOD.md) for the canonical rationale.
