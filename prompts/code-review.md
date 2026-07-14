# Code Review Prompt Template

Review this project's code thoroughly. You will judge, not modify — the output is a report. Every finding must cite file and line, explain why it matters, and propose a concrete fix. Areas that are fine get one line saying so; do not pad.

## Context

- **Project:** [name + one-line description]
- **Where it lives:** [path / repo]
- **Why the review:** [shipping / handing off / interviewing / inherited / health check]
- **Hot spots:** [anywhere I already suspect trouble — this is where to dig deepest]
- **Out of scope:** [dimensions to skip, e.g. "no security review, offline hobby tool" / "no concurrency, simple script"]
- **Depth:** [quick pass / thorough audit]

## What I want from you — in order

**Step 1 — Understand before judging.**
Explore the repo structure, build system, entry points, dominant conventions. Run the linter and tests if available — their output is input to the review, not the review. Don't list findings until you can state in one paragraph what this project is and how it's shaped.

**Step 2 — Review across these dimensions** (skip what I ruled out, but say so in one line):

1. **Correctness & robustness** — swallowed errors, unchecked returns, missing null/bounds checks; edge cases (empty, zero, unicode, huge inputs); resource leaks especially on error paths; undefined behavior, platform assumptions.
2. **Performance** — O(n²) over growing data, repeated work in loops; N+1 queries, chatty I/O, sync blocking on hot paths; copies in tight loops, unbounded growth. Only flag paths that plausibly matter.
3. **Concurrency & state** — races, unsynchronized shared mutable state, lock ordering; fire-and-forget tasks, missing awaits, sync-over-async deadlocks.
4. **Security** — injection (SQL/command/path traversal), hardcoded or logged secrets, unsafe deserialization, weak crypto, overly permissive access.
5. **Maintainability & design** — duplication that will drift, god files, dead code, misleading names, comments that lie, convention inconsistencies, leaky API surface.
6. **Dependencies & build** — outdated/unmaintained deps, known vulnerabilities, floating versions, non-reproducible builds.
7. **Tests** — the 3–5 highest-risk *untested* areas; tests asserting nothing; flaky-by-design tests.

**Step 3 — Report.**
- One-paragraph overall health assessment.
- Findings grouped by severity: **Critical** (bugs, data loss, security) / **High** (likely bugs, serious perf) / **Medium** (design) / **Low** (nits). Each with file:line, problem, why it matters, suggested fix (snippet where useful).
- Clean areas: one line each. Zero findings in a dimension is a valid result.
- **Top 5 recommended actions** by impact-to-effort.

**Step 4 — Stop.** Do not fix anything. If I want fixes, we'll run the rescue protocol with your report as its rot list.

## Evidence discipline

Never report a suspicion as a confirmed finding. Mark suspicions "worth verifying" with the verification step. Only claim what you actually read.

Begin with Step 1.
