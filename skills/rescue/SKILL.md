---
name: rescue
description: Apply the Slow AI rescue protocol when the user has an existing project in unknown, messy, or untrusted state and wants to bring it back to a defensible state before adding features, shipping, handing off, or interviewing on it. Use when they say "rescue this codebase", "clean up this project", "this got vibe-coded and I can't reason about it", "I inherited this", "this works but I can't defend it", "multiple LLM sessions accreted inconsistent patterns", or similar. The protocol inventories, runs the linter, identifies the rot AND the load-bearing parts, then proposes a triaged remediation plan with explicit "won't fix" items.
---

# Slow AI — Rescue

You are applying the **Slow AI** working method to rescue a project that's in unknown or messy state.

The principle: every line of generated code should be a line the user would stand by, line by line, in a code review or interview. For a rescue, that means an honest inventory before any change — and explicit "won't fix" items rather than silent acceptance.

Do not write or modify any code until you have walked through Steps 1–6 below and the user has explicitly said "go fix."

## Step 0 — Gather context

If not already provided, ask for these as a single grouped question:

- **Project** — name + one-line description
- **Where it lives** — path / repo
- **Why it needs rescuing** — pick all that apply:
  - Vibe-coded without architectural direction, now hard to reason about
  - Inherited from someone else
  - Multiple LLM sessions accreted inconsistent patterns
  - Works but the user can't defend it in a walkthrough
  - Doesn't work and the user doesn't know why
  - User lost the thread on what's actually in it
- **Current state** — does it run? does it pass linting? does it have tests? known broken features?
- **Time budget** — hours, realistic
- **Required outcome** — pick one:
  - "Working and defensible" — walk through with someone
  - "Working and shippable" — ship it
  - "Working and extendable" — add features without making it worse
  - "Just working" — runs and does what it claims
- **Reference materials** — any README, NOTES, design docs, original brief, prior conversation logs
- **What the user thinks is in the project** — best guess at stack, architecture, working features, suspected breakages, things to keep no matter what, things they'd happily delete

The user's last bullet is honest guesswork; your Step 1 will verify or contradict it.

## Step 1 — Inventory the project

View the project root. Read README, NOTES.md, package manifests, any obvious entry-point file, and the directory tree at depth 2. Produce:

- **File tree summary** — which directories hold what, with line counts per file. Flag any file over 300 lines as "needs scrutiny."
- **Dependencies inventory** — every runtime dep, every dev dep, with a one-line purpose for each. Flag any that look unused, deprecated, or redundant.
- **Entry points** — what runs first, what state initializes where.
- **Apparent architectural pattern** — what shape did whoever built this seem to be aiming for? Be honest if it's inconsistent.
- **Things that contradict the user's Step 0 description** — explicit list. Do not gloss over discrepancies.

Do NOT propose changes yet. Step 1 is just inventory.

## Step 2 — Run the project as it stands

Identify the build/run/test/lint commands. Run them if possible; otherwise list them and tell the user what to look for. For each:

- Does it pass cleanly?
- If not, list every error and warning verbatim.
- Categorize each as: (a) blocks the project from running, (b) blocks shipping but not running, (c) cosmetic.

## Step 3 — Identify the rot

List, in priority order, the actual problems. Be specific. Look for:

- Inconsistent state management (multiple patterns coexisting)
- Dead code, dead files, dead branches
- Orphaned imports, unused dependencies
- Files doing too many things
- Comments lying about the code (out of date / misleading)
- TODO/FIXME/HACK markers (list them all with context)
- Commented-out code blocks
- Magic numbers and unexplained constants
- Race conditions, missing cancellation, missing error handling
- Things that work by accident
- Code that doesn't match its own documentation
- Tests that don't test what they claim to test (if there are tests at all)

For each item: where it is, why it's a problem, severity (blocker / serious / cosmetic).

## Step 4 — Identify the load-bearing parts

The opposite of Step 3. List the parts of this codebase that are working, sensible, and worth preserving — anything to defend rather than rewrite. This list is the floor we don't go below in Step 5.

## Step 5 — Propose a triaged remediation plan

Given the time budget and required outcome:

- **Must fix** — items from Step 3 that block the required outcome. For each: estimated effort, what changes, risk of breaking Step 4 items.
- **Should fix** — non-blockers that materially improve defensibility. Same shape.
- **Won't fix this session** — real problems that don't fit the budget. These go into `NOTES.md` as known issues, not silently ignored.
- **Order of operations** — what to fix first, second, third. Justify the ordering (usually: unblockers first, safest fixes before riskier ones).
- **Verification gates** — between fixes, how do we confirm we haven't regressed Step 4 items?

If the required outcome is genuinely not achievable in the time budget, **say so explicitly**. Propose a realistic outcome and let the user decide whether to extend the budget or lower the bar.

## Step 6 — Wait for approval

Stop. Show the plan. The user approves, modifies, or rejects. Do not modify any code until they say "go fix."

## After approval

Work through the plan one item at a time. Before each change, say what file you're about to touch and why. After each change, run the analyzer/linter (and any tests) and confirm green before moving to the next item.

- If you discover something during a fix that materially changes the plan, **stop and tell the user**. Don't silently expand scope.
- If a fix turns out to be larger than estimated, **stop and tell the user**. Re-triage rather than blow the budget.
- Match the project's existing conventions even where you'd prefer something else, **unless** the convention itself is on the rot list and you agreed to change it.
- Update `NOTES.md` as you go. Every fix gets one line: what was wrong, what you changed, why. Every "won't fix" item from Step 5 gets logged under "Known issues."
- For deleted files, deleted dependencies, or deleted code blocks, commit the deletion as its own commit with a clear message. Don't bundle deletions into feature commits.

## Done criteria

The rescue is complete when:

- [ ] All "must fix" items from Step 5 are resolved
- [ ] Analyzer/linter passes cleanly
- [ ] Build/run/test commands succeed
- [ ] No new regressions in Step 4 (load-bearing parts)
- [ ] `NOTES.md` reflects the current state, including known issues
- [ ] The specific defensibility check from the required outcome is met (e.g., "I can walk through the entry point and three core files without finding anything I can't explain")

When all boxes are ticked, **stop**. The project is ready for the required outcome. No new features in this session.

## Full method

See [METHOD.md](../../METHOD.md) for the canonical rationale.
