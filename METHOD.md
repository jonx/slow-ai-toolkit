# The Slow AI Method

This is the canonical reference. The skills in [`skills/`](skills/) are the agent-facing condensed versions (one per scenario); the prompt templates in [`prompts/`](prompts/) are the paste-ready operationalization for non-Claude tools. This file is the *why*.

## What it is

A working method for using AI coding agents on real projects. Slow Food in spirit: not anti-AI, but anti the part of vibe-coding where speed compounds into code nobody can stand by.

## The principle

Every line of generated code should be a line you would stand by, line by line, in a code review or interview. Speed is fine. Sloppiness compounded by speed is not.

That single sentence is the lever. Most other rules in this method are mechanical consequences of taking it seriously.

## Why this exists

Default agent behavior is "produce something runnable, fast." That is not the same as "produce something defensible." The first is rewarded by chat-style interactions; the second is what survives a code review, an interview walkthrough, a customer hand-off, or you re-reading it in three months.

The gap between the two shows up in concrete ways:

- An SDK call that pattern-matches "what this API usually looks like" but isn't quite right. Hours of debugging later.
- A repository / usecase / domain layer for a 200-line app, because the agent saw similar shapes during training.
- A state-management framework wired in for one piece of state.
- A 600-line file holding three loosely related concerns.
- Comments that restate the code instead of explaining it.

These aren't AI failures. They're failures of direction. The method below directs the agent away from each one explicitly.

## The seven-step loop

For any non-trivial coding chunk, work the loop:

1. **Verify** the SDK, framework, or library *before* designing against it. Read the source, confirm exact signatures, flag surprises. Pattern-matching what an API "usually looks like" is the single biggest source of debug time later.
2. **Plan** the next chunk in writing. Files that change, data flow, trade-offs, risks, uncertainties. No code yet.
3. **Approve** explicitly. The user reads the plan, pushes back if anything is wrong, then says go. Approval is not a formality.
4. **Implement** in small named layers. One concern at a time.
5. **Test** the result. Run the analyzer or linter. Run the project. Confirm the change behaves as intended and nothing visible regressed — and confirm it by *observation*, not assertion: cite the screenshot, log excerpt, or test output that proves it (see "Eyes before hands" below).
6. **Note** the decision in `NOTES.md` at the project root, in the user's voice, as it happens. Architecture, key decisions, trade-offs, with-more-time, things to discuss in a walkthrough.
7. **Move on.** Resist mid-phase scope creep. Defend boundaries.

The loop runs per *chunk*, not per *project*. A project is many chunks; a chunk is one thing you can plan, approve, build, and verify in a sitting.

## Eyes before hands

An agent that cannot observe what it builds is guessing. Linters and compilers catch syntax; they say nothing about whether the window actually opened, the layout actually holds, the boot actually reaches the shell, or the button actually does anything. For any project whose output is visual, interactive, or long-running, step 5 (Test) is theater unless the agent has *eyes*.

So the first chunk of such a project — before any feature work — is the **observation harness**: the tooling that lets the agent see the running artifact and drive it, headlessly and on demand.

Two capabilities, always both:

1. **See** — a repeatable, scriptable way to capture what the artifact looks like or outputs right now. Headless screenshots, framebuffer dumps, serial/console logs, structured state dumps. One command, one artifact, no human in the loop.
2. **Drive** — a puppeteer: a way to send input to the artifact programmatically. Click, type, navigate, invoke, send keystrokes down a serial line. Observation without control only proves the happy path you happened to land on.

Together they close the loop: build → launch → drive → observe → verdict. The agent stops reporting "this should work" and starts reporting "here is the screenshot / log line that shows it working."

Consequences the method takes seriously:

- **The harness is a deliverable, not scaffolding.** It lives in the repo (`tools/`, `harness/`, a Makefile target), it's documented in the README, and it outlives the session. Future sessions — and future agents — inherit the eyes.
- **Verdicts require evidence.** "Done" claims in step 5 must cite an observation artifact: a screenshot path, a log excerpt, a test run. An agent asserting success without evidence is the same failure mode as an agent pattern-matching an SDK signature — confident, unverified, expensive later.
- **Blindness is a named risk.** If some behavior genuinely can't be observed headlessly (hardware quirk, third-party service), the plan says so in Gate 4 and names the fallback: what the human must manually check, precisely.

The techniques are platform-specific — Playwright for web, `xvfb` + capture for desktop GUI, simulator screenshot commands for mobile, QMP screendump and serial consoles for emulated systems, `tmux capture-pane` for TUIs — but the principle is uniform: **give the agent eyes first, then let it build.** The `give-eyes` skill operationalizes this.

## The four gates

Step 2 is concrete: before any code is written for a non-trivial chunk, produce these four artifacts.

### Gate 1 — Reference summary

What the existing code, brief, or setup materials establish. Three to five bullets. The point is to surface what's *already true* before designing what should be added. If the agent skips this gate it will silently invent a parallel reality.

### Gate 2 — File or change-set list

One line per file. For new projects: every file in the initial build. For features: created / modified / deleted, with rough line count. The list is a contract for scope. If implementation produces a file not on the list, the loop is broken — re-plan, don't accrete.

### Gate 3 — Data-flow paragraph

200 words max. How state moves: from input through to output, what triggers what, where it lives, where it's read. If you can't explain it in 200 words, the design is wrong, not the prose budget.

### Gate 4 — Trade-offs and uncertainties

Explicit. With mitigation or verification plan for each uncertainty. "We could revisit this later" is not a trade-off — it is decoration. Real trade-offs name what was given up and why.

After the four gates: stop. Wait for approval.

## Defaults to refuse

Unless the user explicitly asks for them, do not introduce:

- **State management frameworks** for projects that fit in one or two state surfaces (Riverpod, BLoC, Redux, MobX, Provider, Zustand, Recoil, Pinia, Vuex, etc.). A `ChangeNotifier` / `useState` / module-level holder is almost always enough.
- **Repository, usecase, or domain layers** in projects that fit in a few hundred lines. The indirection costs more than it pays back at that scale.
- **Hexagonal, Clean, Onion, or DDD architectures** unless the project's complexity warrants them. They warrant them less often than they appear in tutorials.
- **Premature optimization** — custom isolates, streaming parsers, micro-caches — before the naive version works and is measured.
- **Files growing without a re-evaluation.** ~200 lines is the indicative point to pause and ask whether the file is doing more than one thing; ~800 is where the size needs an explicit defense. Neither is a hard rule — generated code, state machines, and config tables sometimes legitimately exceed both. The discipline is noticing the size and either justifying or splitting, not hitting a number.
- **Boilerplate comments that restate the code.** Comments explain *why*, never *what*.

If the user's prompt didn't forbid these explicitly, propose simpler alternatives in the plan and let the user choose. The forbidden list grows with experience; track yours.

## Match the project, not your preferences

In an existing codebase, match its conventions even if you would do it differently in a green-field build. Consistency with the existing code matters more than stylistic preferences. A codebase with one pattern done acceptably is more maintainable than a codebase with three patterns each done "better."

The exception is when an existing pattern is itself part of the problem the user is fixing. That's what the rescue template is for, and it makes the change explicit.

## When the work is small

If the task is genuinely small — a one-line fix, a quick experiment, a script you'll throw away — do not impose the full method. Acknowledge the skill is active, ask whether the gates apply, and respect a no.

The method is for code that will outlive the session. Throwaway work is exempt.

The signal that you actually *do* want the gates: someone (future you, a reviewer, a customer) is going to read this code, and you'd rather they be impressed than confused.

## NOTES.md discipline

Every project under the method gets a `NOTES.md` at the root. Sections:

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

The point is *live* logging. Add to it when the decision is made, in the user's voice, in one or two sentences. By the time you ship, your write-up is already drafted.

The reverse — reconstructing decisions at the end — is how walkthroughs go badly. You forget which trade-offs were deliberate and which were accidents. The agent will pattern-match a plausible explanation and you'll repeat it without believing it. Don't.

## When scope creeps mid-session

It will. The method's response: stop, name what's drifting, decide explicitly whether to extend the chunk's plan or close the chunk and start a new one.

The wrong response is silent expansion. The wrong response is also rigid refusal — sometimes a discovery in step 4 (implement) genuinely changes step 2 (plan). The right response is to *re-plan deliberately*, not to slide.

## Docs are part of the codebase

The method already treats `README.md` and `NOTES.md` as deliverables. The stronger claim: **documentation that contradicts the code is rot**, exactly like a comment that lies. A rescue that fixes the code and leaves the README describing the previous architecture has not finished the rescue.

Two disciplines follow:

- **Docs describe the project, not the journey.** A README answers three questions: what is this, where is it going, where is it right now. Development war stories, failed approaches, and debugging sagas do not belong in it — they belong in `NOTES.md` (decisions) or nowhere. A reader of the README is a newcomer or a reviewer; neither is served by the struggle narrative.
- **Docs get re-verified when code changes.** Any chunk that changes behavior ends with a check: does the README still tell the truth? Build instructions, feature lists, status sections — each is either still accurate or updated in the same chunk. The `docs-refresh` skill operationalizes the full-pass version of this.

## Review is a first-class scenario

The original three scenarios (bootstrap, add-feature, rescue) all *produce* code. The method applies equally to *judging* code — and "review it for speed and robustness" is too vague a brief for an agent to do it well. A serious review names its dimensions (correctness, performance, concurrency, security, maintainability, dependencies, tests), grades findings by severity, cites file and line, proposes concrete fixes, and explicitly says which areas are *fine* rather than padding. The `code-review` skill encodes that protocol. Rescue and review are siblings: review diagnoses and reports; rescue diagnoses and repairs.

## What the templates add

The skill describes the method. The templates make it operational:

- **[`prompts/bootstrap.md`](prompts/bootstrap.md)** — paste at session start for a new project. Includes context fields, constraint declarations, the four gates as a numbered protocol.
- **[`prompts/add-feature.md`](prompts/add-feature.md)** — same shape, scoped to an existing healthy project. Adds a "constraints inherited from the project" section.
- **[`prompts/rescue.md`](prompts/rescue.md)** — same shape, for projects you don't fully trust. Adds a six-step inventory before any plan.
- **[`prompts/give-eyes.md`](prompts/give-eyes.md)** — build the observation harness before feature work. See "Eyes before hands."
- **[`prompts/code-review.md`](prompts/code-review.md)** — structured multi-dimension review with severity-graded, evidence-cited findings.
- **[`prompts/docs-refresh.md`](prompts/docs-refresh.md)** — bring README and docs back in line with the code; project-not-journey framing.
- **[`prompts/walkthrough.md`](prompts/walkthrough.md)** — pre-demo rehearsal: weak points, likely reviewer questions, and the answers.

Each is a self-contained protocol. Filling in the bracketed fields is half the value — being specific about what to *forbid* is at least as useful as being specific about what to build.

## Reading order

If you're new to the method:

1. This file.
2. [`README.md`](README.md) — toolkit overview, narrative.
3. The template that fits your current task.
4. [`skills/`](skills/) only if you're installing the plugin into Claude Code or adapting a skill body for another agent runtime.
