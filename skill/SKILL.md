---
name: slow-ai
description: Apply the Slow AI working method to non-trivial coding work. Use this skill whenever the user is starting a new coding project, adding a feature to an existing project, fixing or rescuing a messy or unfamiliar codebase, working on a take-home, interview project, customer demo, or proof-of-concept, or vibe-coding anything they will need to walk someone through later. Activate on phrases like "help me build", "add this feature", "clean up this project", "rescue this codebase", "I need to walk through this", or any signal that the resulting code will be reviewed, demoed, or maintained beyond the current session.
---

# Slow AI

A working method for using AI coding agents on real projects. The Slow Food version of vibe-coding: not against AI, against the part of vibe-coding where speed compounds into code nobody stands by.

## The principle

Every line of generated code should be a line the user would stand by, line by line, in a code review or interview. Speed is fine. Sloppiness compounded by speed is not.

## The seven-step loop

For any non-trivial coding task, work the user through this loop:

1. **Verify** the SDK, framework, or library before designing against it. Read the source, confirm exact signatures, flag surprises. Pattern-matching what an API "usually looks like" is the single biggest source of debug time later.
2. **Plan** the next chunk in writing. Files that change, data flow, trade-offs, risks, uncertainties. No code yet.
3. **Approve** explicitly. The user reads the plan, pushes back if anything is wrong, then says go. Approval is not a formality.
4. **Implement** in small named layers. One concern at a time.
5. **Test** the result. Run the analyzer or linter. Run the project. Confirm the change behaves as intended and nothing visible regressed.
6. **Note** the decisions in a `NOTES.md` at the project root, as they happen, in the user's voice. Architecture, key decisions, trade-offs, with-more-time, things to discuss in a walkthrough.
7. **Move on.** Resist mid-phase scope creep. Defend boundaries.

## The four gates

Before any code is written for a non-trivial chunk of work, produce:

- **Reference summary** - what the existing code or setup materials establish
- **File or change-set list** - what touches what, one line per file
- **Data-flow paragraph** - 200 words max, how state moves through the system
- **Trade-offs and uncertainties** - explicit, with mitigation or verification plan

Then wait for approval. Do not write code until the user says go.

## Defaults to refuse

Unless the user explicitly asks for them, do not introduce:

- State management frameworks for projects that fit in one or two state surfaces (Riverpod, BLoC, Redux, MobX, Provider, etc.)
- Repository, usecase, or domain layers in projects that fit in a few hundred lines
- Hexagonal, clean, or onion architectures unless the project's complexity warrants them
- Premature optimization (custom isolates, streaming parsers, complex caching) before the naive version works
- Files growing past ~200 lines without re-evaluating, or past ~800 without a clear reason — both are flags to think, not hard ceilings
- Boilerplate comments that restate the code

If the user's prompt didn't forbid these explicitly, propose simpler alternatives in the plan and let the user choose.

## Match the project, not your preferences

When working in an existing codebase, match the conventions already there even if you would do it differently in a green-field build. Consistency with the existing code matters more than stylistic preferences. The exception is when an existing pattern is itself part of the problem the user is fixing.

## The three prompt templates

For substantial work, point the user toward the right paste-ready template:

- **Bootstrap** - new project from scratch. Reads any reference materials, proposes architecture, lists trade-offs, waits for approval.
- **Add-feature** - new feature in a healthy existing project. Reads the relevant existing code, proposes the change set, lists what could regress.
- **Rescue** - existing project in unknown or messy state. Inventories what is there, runs the linter, identifies the rot and the load-bearing parts, proposes triaged remediation with explicit "won't fix" items.

The templates are bundled with this skill. If the user's task fits one of the three patterns and they have not already used a template, suggest copying the relevant one as the first message in a fresh agent session.

## When the skill loads but the work is small

If the user's task is genuinely small (a one-line fix, a quick experiment, a script they will throw away), do not impose the full method. Acknowledge the skill is active, ask whether they want the gates applied, and respect a no. The method is for code that will outlive the session. Throwaway work is exempt.

## NOTES.md template

Whenever a project starts under this method, create or update a `NOTES.md` at the project root with these sections:

```markdown
# [Project] - Architecture and Decision Log

## Architecture at a glance
[3-5 bullets, kept current]

## Key decisions
[One subsection per decision, written when the decision is made]

## Trade-offs made under time pressure
[Bullets, added when made]

## With more time, I would
[Bullets, added when something is consciously deferred]

## Things to discuss in the walkthrough
[The questions the user wants the reviewer to ask]
```

Update it as decisions happen. Do not reconstruct it at the end.
