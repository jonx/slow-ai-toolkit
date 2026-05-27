# slow-ai-toolkit — Architecture and Decision Log

This is the toolkit's own NOTES.md, dogfooding the method the toolkit advocates. If a future change to the toolkit doesn't end up in here, the method isn't being applied.

## Architecture at a glance

- Three top-level deliverables: the **method** (`METHOD.md`), the **prompts** (`prompts/`), the **skills** (`skills/`, bundled as a Claude Code plugin). The README is the entry point that sends readers to the right one.
- `METHOD.md` is the canonical reference; each `skills/<name>/SKILL.md` is a tighter agent-facing version of the same content scoped to one scenario (bootstrap / add-feature / rescue); the prompt templates operationalize the method into paste-ready protocols for non-Claude tools.
- `examples/` is reserved for case studies; currently empty (see "With more time" below).
- The skills are consumed by Claude Code via the plugin in `.claude-plugin/` (this repo is its own marketplace).

## Key decisions

### Three artefacts (skills + method + prompts), not one

There's overlap between `METHOD.md`, the `SKILL.md` files, and the prompt headers. That overlap is intentional. Each artefact has a different consumer:

- **`SKILL.md` files** are read by an agent at activation time. They must be self-contained because each one is the only thing the agent sees when its trigger fires.
- **`METHOD.md`** is read by a human deciding whether to adopt the method. It has room for *why*, examples, and acknowledgement of edge cases.
- **Prompt headers** are read by a human filling in a template. They're optimised for fillable fields, not for explanation.

A single document optimised for all three audiences would serve none well.

### Three skills, not one method-loader

The first version of this toolkit shipped a single `skill/SKILL.md` whose body was the method itself; the agent then suggested the right prompt template at runtime. That worked but had a seam: the user described their task, the skill loaded the method, and only then was a template proposed.

Splitting into three trigger-specific skills (`bootstrap`, `add-feature`, `rescue`) collapses that into one step — the scenario-specific protocol fires directly. Each skill is heavier than the old single skill, but that's the right trade because there's now no "loaded but waiting" intermediate state.

### Packaged as a Claude Code plugin, with a self-marketplace

Previously the install instructions told users to `ln -s skill/ ~/.claude/skills/slow-ai`. That worked but didn't survive `/plugin update`, didn't version, and didn't compose with the marketplace ecosystem. Repackaged as a plugin with its own `.claude-plugin/marketplace.json` so the install path is `/plugin marketplace add github:jonx/slow-ai-toolkit` followed by `/plugin install slow-ai-toolkit@slow-ai`. The marketplace lives in the same repo as the plugin (one-plugin marketplace) — if/when there are more plugins, they go under `./plugins/<name>/` with the marketplace pointing to them.

### Templates are intentionally verbose

A short template makes the agent's job easier and the human's harder — they have to fill in unstated constraints from memory, and they will forget. The templates list constraint categories *exhaustively* (state management, architectural style, file-size guidance, comment style, deps) precisely so the human is prompted to make the call rather than leaving it implicit.

### Bootstrap prompt has no "exit criteria" section

Other two templates do. Bootstrap doesn't, because at project-start time you genuinely don't know enough to write done-criteria. Adding a placeholder section produces lies. Better to require done-criteria when scope is concrete (i.e., from `add-feature` onward).

This is a known asymmetry — see "With more time."

### Repo named `slow-ai-toolkit` and README leads with the Slow Food origin

The project's working name was "AI-Assisted Build Prompts," accurate but flat. Renaming to `slow-ai-toolkit` and surfacing the Slow Food connection on the front page does two things: gives the method a memorable handle, and signals up front that this is a stance, not a productivity hack. The Slow Food parallel was already in `METHOD.md`; promoting it to the README makes the framing visible to readers who only skim the entry page.

### Multi-agent story moved to the README

Previously the "this works in non-Claude tools too" framing was one paragraph in `skill/README.md` (now deleted as part of the plugin restructure). The method is genuinely tool-portable — burying that on a sub-page understated it. Front-page section "Using this with any agent" now lists concrete adoption notes per tool (Cursor, Aider, Continue, Cline, plain web chats). The plugin packaging targets Claude Code; the prompts and method don't depend on it.

### File-size guidance softened: indicative, not hard

Earlier drafts had ~200 lines as a "hard ceiling unless defensible." In practice some files genuinely belong oversized — generated parsers, state machines, config tables — and a hard rule produces either contortions to dodge it or quiet rule-breaking. Reframed across `README.md`, `METHOD.md`, the skill files, and `prompts/bootstrap.md`: ~200 lines is the prompt to *notice* (probably doing more than one thing), ~800 is where the size needs explicit defense, neither is a hard cap. The discipline is the noticing, not the number.

### AI-disclosure form is per-user — verify, don't default

The toolkit advocates AI disclosure (see README "A note on AI disclosure"). The *form* of disclosure (commit `Co-Authored-By:` trailers, README notes, PR descriptions, in-line comments) is a personal preference that varies by individual, team, audience, and even repo. Future agent sessions working on this repo, or on any repo where the user is using this method, should ASK the human before adding such trailers — never default them in. The initial commit on this repo deliberately omits the trailer for that reason.

## Trade-offs made under time pressure

- `examples/` is empty at first publish. Decided to ship the toolkit without a case study rather than block on writing one. Risk: readers without prior context for the method may find it abstract. Placeholder `examples/README.md` notes the gap publicly.
- The four-gate "200-word data-flow paragraph" rule in `METHOD.md` doesn't scale to large multi-file features. Left unchanged for now — the rule is more useful as friction than as a literal limit. Worth revisiting with a "how this scales" note once the case study lands.

## With more time, I would

- Write a worked case-study example under `examples/` — bootstrap → ship → walkthrough — as the strongest argument for the method.
- Add an "exit criteria" section to `prompts/bootstrap.md` even at project-start time, framed as "you'll fill this in when scope solidifies; here's the slot."
- Add a `prompts/walkthrough.md` template — a fourth prompt for the moment when you're about to demo a finished project to a reviewer. Asks the agent to enumerate weak points, surprises, and likely questions. Makes the walkthrough rehearsal mechanical instead of vibey.
- Expand the forbidden-patterns list in `METHOD.md` with language- or framework-specific entries (Flutter, React, Rust, etc.). Currently the list is generic.
- Add a short rationale to each "default to refuse" entry. The current list says *what* to refuse but not always *why* it tends to be wrong. A reviewer encountering "no Riverpod" will want to know.
- Address the team-codebase cases the method understates: how `NOTES.md` interacts with PR descriptions and commit messages on a team (probably: NOTES.md is for cross-cutting context, commits/PRs for change-specific rationale), and how the four gates scale on a 50-file feature.

## Things to discuss in the walkthrough

If presenting this toolkit to someone:

- "Why three templates instead of one configurable one?" — because the agent's behavior diverges meaningfully based on whether a codebase exists yet and whether you trust it. A single template with mode flags would be longer to fill in and harder to use under time pressure.
- "Why not put the method in CLAUDE.md or system prompt?" — both work, neither activates conditionally on the *task* (vs. the project). The skill activates on intent keywords; system prompts apply uniformly. Different tools.
- "How is this different from a code-style guide?" — code-style guides describe the artifact. This describes the *process* that produces the artifact. Without process, style alone slips when the agent is tired or the user is hurrying.
- "Does this make me slower?" — yes, by 10–20% on the first session. Then not, because rework drops to near zero. The break-even is somewhere around session 3.
