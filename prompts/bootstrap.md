# Project Bootstrap Prompt Template

I'm building [PROJECT NAME], a [ONE-LINE DESCRIPTION] for [CONTEXT: client demo / take-home / internal POC / side project / production service / shared codebase]. You are going to help me design the architecture and then implement it, but you will not write any code until I explicitly approve the plan in step 4 below.

## Context

- **Purpose:** [what success looks like for this build]
- **Audience for the code:** [who will read it - me, a reviewer, a customer, teammates, future maintainers, a future me]
- **Time budget:** [hours, days, weeks - be honest, including buffer]
- **Defensibility requirement:** [will I walk through this code with someone? if yes, every line must be defensible]
- **Quality bar:** [readable + conventional > clever; or production-grade > MVP; or whatever fits]
- **Target platforms:** [iOS / Android / web / desktop / server / specific OS versions]
- **Reference materials:** [paths to any existing code, setup folders, docs, schemas to read FIRST]

## What we are building (the brief)

[Paste or paraphrase the actual requirements. List concrete deliverables. Be precise about what is in scope.]

## Scope beyond the brief - extension hooks

These are NOT to be built now, but the architecture must accommodate them cleanly without rework:

- [extension 1]
- [extension 2]
- [extension 3]

The architecture should leave seams for these (data model fields, service boundaries, state shape). Implement only the core brief in the initial build.

## Non-negotiable constraints

- **Stack / language:** [versions, frameworks]
- **State management / architecture pattern:** [be specific - e.g. "plain ChangeNotifier, NO Riverpod/BLoC/Provider/GetX"]
- **Architectural style:** [e.g. "simple layering. No Clean Architecture, no hexagonal ports-and-adapters, no repository pattern unless strictly needed"]
- **File size guidance:** [e.g. "single-purpose; ~200 lines is a soft signal to consider splitting, ~800 needs a clear reason — neither is a hard cap"]
- **Comment style:** [e.g. "explain WHY not WHAT, senior-engineer level, no boilerplate"]
- **Dependencies:** [allowed / forbidden / approval-required]
- **Performance / optimization:** [e.g. "no premature optimization until naive version works"]
- **Testing:** [required / nice-to-have / out of scope]

## What I want from you in this session - in order

**Step 1 - Read reference materials.**
View [LIST OF FILES/PATHS]. Summarize in 3-5 bullets: what versions/conventions/gotchas are established, and what minimum must be carried into the new project.

**Step 2 - Propose the file/module tree.**
Give me a complete file tree for the initial build. For each file, one sentence on what it holds. Group by concern (models / services / state / ui / etc).

**Step 3 - Explain the architecture in one paragraph.**
How data flows: from input through to output. What state lives where, what triggers what. Call out explicitly how the extension hooks fit. Maximum 200 words.

**Step 4 - List trade-offs, risks, and uncertainties.**
3-5 bullets on the main trade-offs of this design and what I should be ready to defend. Flag anything you are uncertain about regarding the framework/SDK/language version. If you need to verify an API surface, say so explicitly and propose how (e.g. "I'll read the package source in [LOCATION] before committing to signatures").

**Step 5 - Wait for my approval.**
After steps 1-4, stop and ask me to approve, request changes, or ask questions. DO NOT write any code until I say "go build."

## Style of our interaction going forward

- I will review each chunk you produce. Before generating a new file or making a non-trivial change, tell me what you are about to build and why.
- If I ask you to simplify, err on the side of over-simplifying. Readable beats clever.
- If you are about to use a pattern, library, or abstraction I haven't approved, stop and ask first.
- For any non-trivial use of an SDK, framework, or language feature you haven't verified, READ THE SOURCE FIRST and confirm exact signatures before designing against them. Flag surprises explicitly.
- Comments are written as if explaining to a colleague who will read this code in a code review with me.
- After each significant change, run the project's analyzer/linter and confirm it passes before declaring done.
- Maintain a NOTES.md at the project root. Every non-trivial decision (architectural choice, trade-off, surprise discovered, scope cut) gets one or two sentences added at the moment it happens.

Begin with Step 1.
