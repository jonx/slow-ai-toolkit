---
name: add-feature
description: Apply the Slow AI add-feature protocol when the user wants to add a new feature to an existing project that is already in good shape. Use when they say "add this feature", "I want to add [X] to my app", "extend this with [Y]", or describe a scoped addition to a healthy codebase. The protocol reads the relevant existing code first, proposes a change set, identifies what could regress, and waits for explicit approval before any code is written. Not for messy or unfamiliar projects — use the rescue skill for those.
---

# Slow AI — Add Feature

You are applying the **Slow AI** working method to add a feature to an existing healthy project.

The principle: every line of generated code should be a line the user would stand by, line by line, in a code review or interview. Speed is fine; sloppiness compounded by speed is not.

Do not write or modify any code until you have walked through Steps 1–6 below and the user has explicitly said "go build."

## Step 0 — Gather context

If not already provided, ask for these as a single grouped question:

- **Project** — name + one-line description
- **Where it lives** — path / repo
- **Current state** — working / partly working / known issues
- **Audience for the code** — reviewer, customer, future self
- **Time budget** — hours, honest with buffer
- **Defensibility requirement** — will the user walk through this with someone?
- **Reference materials** — paths to project docs, NOTES.md, design docs, related code paths
- **The feature itself** — concrete behavior, edge cases, explicit non-goals
- **Why it belongs here** — one sentence, to defend against scope creep
- **Constraints inherited from the project** — stack, existing state pattern (do NOT introduce a new one for this feature), architectural style, file-size convention, comment style, dependency policy
- **Constraints specific to this feature** — scope boundaries and explicit non-goals

## Step 1 — Read the existing project

View the files most relevant to this feature. Also view `NOTES.md` and `README.md` if they exist. Summarize in 3–5 bullets:

- The relevant existing patterns this feature must fit into
- The state container(s) it will touch
- The data flow it will plug into
- Any conventions or constraints visible in the code that the user might not have remembered

If anything you find **contradicts** the constraints the user gave above, stop and flag it before continuing.

## Step 2 — Verify any unfamiliar APIs

If this feature touches an SDK, framework, library, or language feature you haven't verified recently, **read the source before designing**. Confirm exact signatures, parameter shapes, return types. Flag surprises explicitly. Pattern-matching what an API "usually looks like" is the single biggest source of debug time later.

If everything is already familiar from prior work in this project, say so and skip this step.

## Step 3 — Propose the change set

List every file that will change. For each:

- Created / modified / deleted
- One-sentence purpose of the change
- Rough line count

Then propose any new file(s) needed, with the same shape as the project's existing file conventions. Group by concern.

## Step 4 — Explain the integration (one paragraph, ≤200 words)

How this feature plugs into the existing data flow: what triggers it, where its state lives, what it reads, what it writes, how the UI sees it. Call out anywhere this touches shared state and what could go wrong if another feature were also touching it.

## Step 5 — List trade-offs, risks, and what could regress

- 3–5 bullets on trade-offs and what the user should be ready to defend
- Anything you're uncertain about (APIs, edge cases, race conditions)
- **Explicit list** of which existing behaviors could regress if this is implemented carelessly
- **Test/verification plan** — how will we know the feature works AND that nothing it touches broke?

## Step 6 — Wait for approval

Stop. Ask the user to approve, request changes, or ask questions. Do not write code until they say "go build."

## After approval

Work in small named chunks. Before generating or modifying a file, say what you're about to do and why. After each significant change:

- Run the project's analyzer/linter (and any tests). Confirm green before declaring done.
- Update `NOTES.md` with one or two sentences: the design choice and any trade-off worth remembering. Add a "With more time" bullet for anything consciously deferred.

## Match the project, not your preferences

Match the existing conventions even where you would do it differently in a green-field build. Consistency with the existing code matters more than your stylistic preferences. A codebase with one pattern done acceptably is more maintainable than a codebase with three patterns each done "better."

The exception is when an existing pattern is itself part of the problem — but that's the rescue skill, not this one. If you find yourself wanting to fix existing rot while adding a feature, **stop and surface it** rather than silently changing scope.

## Defaults to refuse

For this feature, do not introduce a new state management framework, architectural layer, or large dependency unless the user explicitly asked for it. Match what the project already does.

## Done criteria

The feature is complete when:

- [ ] All specified user-visible behavior works
- [ ] Specified edge cases / failure modes handled gracefully
- [ ] No regressions in the existing behaviors enumerated in Step 5
- [ ] Analyzer/linter passes with zero warnings
- [ ] `NOTES.md` updated
- [ ] Device/runtime tested

When all boxes are ticked, **stop**. No follow-on features in this session — defend scope.

## Full method

See [METHOD.md](../../METHOD.md) for the canonical rationale.
