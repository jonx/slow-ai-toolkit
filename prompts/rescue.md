# Mid-Project Rescue Prompt Template

I have an existing project that needs to be brought back into a defensible state before I [add features / hand it off / ship it / interview on it / debug it productively]. You are going to help me assess it and propose a remediation plan, but you will not write or modify any code until I explicitly approve the plan in step 6 below.

## Context

- **Project:** [name + one-line description]
- **Where it lives:** [path / repo]
- **Why it needs rescuing:** [pick all that apply]
  - Vibe-coded without architectural direction, now hard to reason about
  - Inherited from someone else
  - Multiple LLM sessions accreted inconsistent patterns
  - It works but I can't defend it in a walkthrough
  - It doesn't work and I don't know why
  - I lost the thread on what's actually in it
  - [other]
- **Current state:** [does it run? does it pass linting? does it have tests? are there known broken features?]
- **Time budget for the rescue:** [hours - be realistic]
- **Required outcome:** [pick one]
  - "Working and defensible" - I need to walk through this with someone
  - "Working and shippable" - I need to ship this
  - "Working and extendable" - I need to add features without making it worse
  - "Just working" - the bar is "it runs and does what it claims"
- **Reference materials:** [paths to any README, NOTES, design docs, original brief, prior conversation logs - anything that documents intent vs. what got built]

## What I think is in this project

[Your best understanding. Be honest about what you don't remember or never knew. The LLM's job in Step 1 is partly to verify or contradict this.]

- **Stack / language:** [if you know]
- **Architecture pattern:** [if you know - or "unclear"]
- **Major features that should work:** [list]
- **Things I suspect are broken or fragile:** [list]
- **Things I want to keep no matter what:** [list - these are non-negotiable]
- **Things I'd be happy to delete:** [list - these are explicit candidates for removal]

## What I want from you in this session - in order

**Step 1 - Inventory the project.**

View the project root. Read [README, NOTES.md, package manifests, any obvious entry-point file, and the directory tree at depth 2]. Then produce:

- **File tree summary:** which directories hold what, with line counts per file. Flag any file over 300 lines as "needs scrutiny."
- **Dependencies inventory:** every runtime dep, every dev dep, with a one-line purpose for each. Flag any that look unused, deprecated, or redundant.
- **Entry points:** what runs first, what state initializes where.
- **Apparent architectural pattern:** what shape did whoever built this seem to be aiming for? Be honest if it's inconsistent.
- **Things that contradict what I described above:** explicit list. Do not gloss over discrepancies.

Do NOT propose changes yet. The output of Step 1 is just an inventory.

**Step 2 - Run the project as it stands.**

Tell me what command would run, build, or test this project. If it has a linter/analyzer, what's its current output? If you can't determine these without running them, list the commands I should run and what to look for.

For each:
- Does it pass cleanly?
- If not, list every error and warning verbatim.
- Categorize each as: (a) blocks the project from running, (b) blocks shipping but not running, (c) cosmetic.

**Step 3 - Identify the rot.**

List, in priority order, the actual problems with this codebase. Be specific. Examples of what to look for:

- Inconsistent state management (multiple patterns coexisting)
- Dead code, dead files, dead branches
- Orphaned imports, unused dependencies
- Files doing too many things
- Comments lying about the code (out of date / misleading)
- TODO/FIXME/HACK markers (list them all with context)
- Commented-out code blocks
- Magic numbers and unexplained constants
- Race conditions, missing cancellation, missing error handling
- Things that work by accident (the LLM-equivalent of "I'm not sure why this works")
- Code that doesn't match its own documentation
- Tests that don't test what they claim to test (if there are tests at all)

For each item: where it is, why it's a problem, severity (blocker / serious / cosmetic).

**Step 4 - Identify the load-bearing parts.**

The opposite of step 3. List the parts of this codebase that are working, sensible, and worth preserving. Anything we'd want to defend rather than rewrite. This list is the floor we don't go below in step 5.

**Step 5 - Propose a remediation plan.**

Given the time budget and required outcome from the Context section, propose a triage:

- **Must fix:** items from step 3 that block the required outcome. For each: estimated effort, what changes, risk of breaking step 4 items.
- **Should fix:** items that aren't blockers but materially improve defensibility. Same shape.
- **Won't fix this session:** items that are real problems but don't fit the budget. These go into NOTES.md as known issues, not silently ignored.
- **Order of operations:** what to fix first, second, third. Justify the ordering (usually: things that unblock other fixes go first; safest fixes go before riskier ones).
- **Verification gates:** between fixes, how do we confirm we haven't regressed something in step 4?

If the required outcome is genuinely not achievable in the time budget, say so explicitly. Propose what a realistic outcome would be, and let me decide whether to extend the budget or lower the bar.

**Step 6 - Wait for my approval.**

Stop. Show me the plan. I will approve, modify, or reject. DO NOT modify any code until I say "go fix."

## Style of our interaction going forward

- After approval, work through the plan one item at a time. Before each change, tell me what file you're about to touch and why. After each change, run the analyzer/linter (and any tests) and confirm green before moving to the next item.
- If you discover something during a fix that materially changes the plan, stop and tell me. Don't silently expand scope.
- If a fix turns out to be larger than estimated, stop and tell me. We re-triage rather than blow the budget.
- Match the project's existing conventions even where you'd prefer something else, UNLESS the convention itself is on the rot list and we agreed to change it.
- Update NOTES.md as you go. Every fix gets one line: what was wrong, what you changed, why. Every "won't fix" item from step 5 gets logged under "Known issues."
- For deleted files, deleted dependencies, or deleted code blocks, commit the deletion as its own commit with a clear message. Don't bundle deletions into feature commits - they should be reviewable in isolation.

## Done criteria for this rescue

The rescue is complete when:
- [ ] All "must fix" items from step 5 are resolved
- [ ] Analyzer/linter passes cleanly
- [ ] [BUILD/RUN/TEST commands] succeed
- [ ] No new regressions in items from step 4 (the load-bearing parts)
- [ ] NOTES.md reflects the current state, including known issues
- [ ] [SPECIFIC DEFENSIBILITY CHECK - e.g. "I can walk through the entry point and three core files without finding anything I can't explain"]

When all boxes are ticked, STOP. The project is ready for [whatever the required outcome was]. No new features in this session.

Begin with Step 1.
