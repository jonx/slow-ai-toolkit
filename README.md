# Slow AI Toolkit

A working method and a small set of prompt templates for using AI coding agents on serious work — code that gets reviewed, shipped, maintained, or walked through. The shape: verify, plan, approve, implement, test, note, move on. Defend scope at every gate.

Tested on take-homes, client demos, side projects, and production codebases. The discipline that works for a 200-line interview project also works for a feature added to a codebase a team will touch six months from now.

## Why "Slow AI"

The name borrows loosely from **Slow Food**. Slow Food isn't anti-cooking; it's against industrial shortcuts that produce something edible but not worth eating. Slow AI isn't anti-AI; it's against the part of vibe-coding where speed compounds into code nobody can stand by. Speed is fine. Sloppiness compounded by speed is not.

Full rationale in [`METHOD.md`](METHOD.md).

## Agent-agnostic

The method is agent-agnostic. The plugin packaging targets [Claude Code](https://claude.com/claude-code), but the prompts and method paste cleanly into Cursor, Aider, Continue, Cline, plain ChatGPT, Claude.ai web — anything that takes natural-language input. See [Using this with any agent](#using-this-with-any-agent) below.

## Install (Claude Code)

This repo ships as a Claude Code plugin that bundles three skills (`bootstrap`, `add-feature`, `rescue`) and includes its own marketplace manifest.

```sh
# Add the marketplace, then install the plugin
/plugin marketplace add github:jonx/slow-ai-toolkit
/plugin install slow-ai-toolkit@slow-ai
```

Once installed, the right skill auto-activates when you describe what you're doing — "help me build a CLI", "add a feature to this app", "rescue this codebase" — and walks you through the protocol before any code is written.

You can also invoke a skill explicitly:

```
/slow-ai-toolkit:bootstrap
/slow-ai-toolkit:add-feature
/slow-ai-toolkit:rescue
```

To update later: `/plugin update`. To uninstall: `/plugin uninstall slow-ai-toolkit@slow-ai`.

## When to use which

Three templates, three situations:

- **[`prompts/bootstrap.md`](prompts/bootstrap.md)** - starting a new project from scratch
- **[`prompts/add-feature.md`](prompts/add-feature.md)** - adding to an existing project that's already in good shape
- **[`prompts/rescue.md`](prompts/rescue.md)** - bringing a messy or unfamiliar project back to a defensible state

They share a method but differ in where they start. The bootstrap assumes nothing exists. The add-feature assumes the existing code is healthy and consistent. The rescue assumes neither.

## The method, in one paragraph

Before any code is written, the agent produces a written plan: file tree, data flow, trade-offs, risks, and explicit uncertainties. You review and approve before implementation begins. Each phase has a hard boundary - no scope creep mid-phase. After every significant change, the analyzer/linter runs and the project gets device-tested or runtime-tested. A `NOTES.md` at the project root captures decisions as they happen, not reconstructed at the end. The agent matches existing project conventions even when it would prefer something else. Patterns and libraries you haven't approved are off-limits without an explicit ask.

The point isn't to slow down. It's to make every line of generated code something you can defend in a code review or a walkthrough.

The full method, with rationale, is in [`METHOD.md`](METHOD.md).

## How to use a template

1. Copy the template to a fresh document.
2. Fill in the bracketed sections honestly. Be specific about constraints, especially the things you want to *forbid* - half the value is preventing the agent from reaching for patterns it would default to.
3. Paste the filled-in template as the first message in a new agent session. Make sure any reference materials it asks to read are accessible (in the working directory, in the repo, etc.).
4. Wait for the planning steps. Read them properly.
5. Push back. Approval is not a formality. Common things to push on:
   - Over-engineered architecture (repository layers, usecase layers, "clean architecture" applied to a 200-line app)
   - Sneaky imports of state-management or DI frameworks you forbade
   - Vague trade-off statements ("we could revisit this later")
   - Confident claims about an SDK the agent hasn't actually verified
   - Files that are going to grow past the size limit you set
6. Once approved, let the agent implement, then run the verification gates. Don't skip them.
7. Update `NOTES.md` as you go.

## What's in each template

### Bootstrap

Starts from a blank slate. The agent reads any setup reference materials you point at, proposes a file tree and architecture, lists trade-offs and uncertainties, and waits for approval before code is written. Best used when:

- You have a clear brief or set of requirements
- You're choosing the stack and patterns yourself
- You're going to walk through this code with someone (interview, code review, customer)

### Add-feature

Plugs into an existing project. The agent reads the relevant existing code first, then proposes a change set - which files change, which are new, which are deleted, with line estimates. Lists what could regress and how to verify. Best used when:

- The host project is in good shape and has consistent conventions
- The feature is well-defined and scoped
- You care about not breaking what's already working

### Rescue

For projects you don't fully trust. The agent inventories what's actually there, runs the linter and any tests, identifies the rot, identifies what's load-bearing, and proposes a triaged remediation plan with explicit "won't fix" items. Best used when:

- You inherited the project, or it accreted across multiple sessions
- You can't predict whether the linter passes
- You suspect more than three things are broken or wrong
- Someone else is going to look at this code soon

## Cross-cutting principles

Things every template enforces, worth understanding regardless of which one you're using.

**Verification before design.** If the agent is going to use an SDK, framework, or library feature it hasn't recently verified, it reads the source first and confirms exact signatures. Generated code that pattern-matches "what an API like this usually looks like" is the single biggest source of debug time later.

**Approval gates.** No code is written until you've approved a written plan. This forces the agent to think before generating, and it forces you to think before approving. Both halves matter.

**Forbidden patterns lists.** Each template encourages explicit "do not use" rules. Without them, agents reach for whatever was popular in their training data, which is usually overengineered for what you actually need. Forbidding patterns is more useful than recommending them.

**File size discipline.** ~200 lines is the indicative point where a file is probably doing more than one thing — worth pausing to ask whether to split. ~800 lines is the point where the size needs an explicit defense. Neither is a hard rule: generated parsers, state machines, and config tables sometimes legitimately exceed both. The discipline is *noticing* the size and either justifying it or splitting, not hitting a number.

**Match the project, not your preferences.** When working in an existing codebase, consistency with what's there beats consistency with the agent's defaults. A codebase with one pattern done acceptably is more maintainable than a codebase with three patterns each done well.

**Live decision log.** Every project gets a `NOTES.md` updated as decisions are made. Sections: architecture at a glance, key decisions, trade-offs made under time pressure, with-more-time, things to discuss in the walkthrough. By the time you're done building, most of your write-up is already drafted in your own voice.

**Defend scope.** "Just one more feature" is the failure mode every project drifts into. Every template has explicit done criteria and a "no follow-on features in this session" clause. Use them.

## Suggested project layout

Whatever the agent generates, the project ends up with:

```
project-root/
|- README.md          # what it does, how to run, written for the audience
|- NOTES.md           # decisions, trade-offs, with-more-time, walkthrough hints
|- [source files]
```

For projects you'll hand off or ship, the README and NOTES are deliverables. Treat them as such from day one, not as end-of-day reconstruction.

## When the templates don't fit

The templates are scaffolding, not law. If a project is small enough that a 200-word architecture paragraph feels excessive, skip it. If you genuinely don't care whether the code is defensible (throwaway script, exploration, learning a new API), skip the gates.

The signal that you actually want the templates: any future-you, teammate, or reviewer is going to read this code, and you'd rather they be impressed than confused.

## A note on AI disclosure

These templates assume you'll be transparent about AI use when relevant. The method itself is a defensibility argument: you can show that every architectural decision was yours, every line was reviewed, and the project shipped is genuinely yours regardless of who held the keyboard. That's a stronger position than pretending no AI was involved.

For interviews, take-homes, and client work, default to disclosure. Most reviewers in 2026 expect it; the surprise is when candidates don't disclose. The method is the signal that you're using AI as a force multiplier, not a substitute for thinking.

## Adjusting over time

Keep a personal forbidden-patterns list across projects. Mine grows by one or two items per project. Common entries:

- State-management frameworks for projects that don't need them (Riverpod, BLoC, Redux for a single-state-container app)
- Repository / usecase / domain layers in apps that fit in a few hundred lines
- Premature optimization (custom isolates, streaming parsers, micro-caches)
- Boilerplate comments that restate the code

Yours will be different. The discipline is naming them out loud, not having a specific list.

If you find yourself reaching for the rescue template often, that's a signal something upstream is misbehaving - either bootstrap discipline is loose, add-feature is being skipped, or you're starting projects with too much ambition relative to time. Worth a periodic look at which template you needed last, and why.

## Using this with any agent

The toolkit has three layers, designed to peel apart cleanly:

1. **The prompts** ([`prompts/*.md`](prompts/)) are plain text with bracketed fields. Copy, fill in, paste as the first message in any agent session. No setup, no integration.
2. **The skills** ([`skills/*/SKILL.md`](skills/)) auto-load the matching protocol into Claude Code when trigger phrases fire. They're plain markdown with a YAML header; tools that consume similar formats can adapt them.
3. **The method** ([`METHOD.md`](METHOD.md)) is the canonical reference. Read once, internalize, apply with or without the prompts. The layer that survives switching tools.

Concrete per-tool notes:

- **Claude Code:** install the plugin (see [Install (Claude Code)](#install-claude-code) above). The three skills auto-activate on trigger phrases. Or paste a prompt manually if you prefer.
- **Cursor:** paste a prompt into chat. For project-wide enforcement, drop the body of one of the `skills/*/SKILL.md` files into `.cursor/rules/slow-ai.mdc`.
- **Aider:** paste a prompt as the first message. For repeated use, point `--read` at a file containing a skill body.
- **Continue / Cline:** paste a prompt at the top of a session, or place a skill body in the tool's custom-instructions / rules file.
- **Plain ChatGPT, Claude.ai web, Gemini:** paste a prompt at the top of the conversation. If the tool supports custom instructions or system prompts, drop a skill body there.
- **Anything else:** the prompts are plain text. They work wherever natural language goes in.

The discipline travels. The packaging is a convenience.

## Files

- [`prompts/bootstrap.md`](prompts/bootstrap.md) - new project, blank slate (paste-anywhere template)
- [`prompts/add-feature.md`](prompts/add-feature.md) - new feature, healthy host project (paste-anywhere template)
- [`prompts/rescue.md`](prompts/rescue.md) - existing project, unknown or messy state (paste-anywhere template)
- [`skills/bootstrap/SKILL.md`](skills/bootstrap/SKILL.md) - Claude Code skill that auto-applies the bootstrap protocol
- [`skills/add-feature/SKILL.md`](skills/add-feature/SKILL.md) - Claude Code skill that auto-applies the add-feature protocol
- [`skills/rescue/SKILL.md`](skills/rescue/SKILL.md) - Claude Code skill that auto-applies the rescue protocol
- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) - plugin manifest
- [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) - marketplace manifest (this repo is its own marketplace)
- [`METHOD.md`](METHOD.md) - the method explained, canonical reference
- [`examples/`](examples/) - case studies (in progress)
- [`NOTES.md`](NOTES.md) - the toolkit's own decision log (dogfooded)

Each prompt is a self-contained template with bracketed fields to fill in. Copy, adapt, paste into a fresh agent session.
