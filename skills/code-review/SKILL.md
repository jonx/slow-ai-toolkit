---
name: code-review
description: Apply the Slow AI code-review protocol when the user wants an existing project's code reviewed and judged, without modifying it. Use when they say "review this code", "review for speed and robustness", "audit this project", "how healthy is this codebase", "what's wrong with this code", or "give me a code review before I ship / hand off / interview". The protocol explores the architecture first, then reviews across seven named dimensions (correctness, performance, concurrency, security, maintainability, dependencies, tests), grades every finding by severity with file/line evidence and a concrete fix, and ends with a top-5 action list. Review reports; it does not repair — use the rescue skill to fix what the review finds.
---

# Slow AI — Code Review

You are applying the **Slow AI** working method to review a codebase. You will judge, not modify. The output is a report the user can act on — every finding cites evidence and proposes a fix, and areas that are fine are declared fine in one line, not padded.

Do not modify any code. If the user wants fixes applied, that's the rescue skill (or add-feature), run after this report is approved.

## Step 0 — Gather context

If not already provided, ask as a single grouped question:

- **Project** — name, one-line description, where it lives
- **Why the review** — shipping / handing off / interviewing / inheriting / just health-checking
- **Hot spots** — anywhere the user already suspects trouble (this dramatically improves review depth)
- **Out of scope** — dimensions to skip (e.g. no security review for an offline hobby tool, no concurrency for a simple script)
- **Depth budget** — quick pass vs. thorough audit

## Step 1 — Understand before judging

Explore the repository structure, build system, entry points, and dominant conventions. Run the linter and tests if available — their output is review input, not the review itself. Do not start listing findings until you can state, in one paragraph, what the project is and how it's shaped.

## Step 2 — Review across the seven dimensions

Skip any dimension ruled out in Step 0 — but say so in one line rather than silently omitting it.

**1. Correctness & robustness** — swallowed or inconsistent error handling, unchecked returns, missing null/bounds checks; unhandled edge cases (empty, zero, unicode, huge inputs); resource leaks, especially on error paths; undefined behavior and platform assumptions.

**2. Performance** — algorithmic issues (O(n²) over growing data, repeated work in loops), I/O patterns (N+1 queries, chatty calls, sync-blocking on hot paths), memory (copies in tight loops, unbounded growth). Only flag paths that plausibly matter; do not micro-optimize cold code.

**3. Concurrency & state** — races, unsynchronized shared mutable state, lock ordering; async correctness (fire-and-forget, missing awaits, sync-over-async deadlock patterns).

**4. Security** — injection risks (SQL, command, path traversal), hardcoded or logged secrets, unsafe deserialization, weak crypto, overly permissive access.

**5. Maintainability & design** — duplication that will drift, god files/functions, dead code, misleading names, comments contradicting code, inconsistent conventions (identify the dominant one, flag deviations), confusing or leaky public API surface.

**6. Dependencies & build** — outdated or unmaintained deps, known vulnerabilities, floating versions, non-reproducible builds.

**7. Tests** — what's covered; the 3–5 highest-risk *uncovered* areas; tests that assert nothing; tests flaky by design (timing- or order-dependent).

## Step 3 — Write the report

- **Opening**: one-paragraph overall health assessment.
- **Findings** grouped by severity — **Critical** (bugs, data loss, security) / **High** (likely bugs, serious perf) / **Medium** (design, maintainability) / **Low** (style, nits). Each finding: file and line, what's wrong, why it matters, concrete suggested fix (snippet where useful).
- **Clean areas**: one line each. Zero findings in a dimension is a valid, reportable result.
- **Top 5 recommended actions**, ordered by impact-to-effort.

Do not pad. A short honest report beats a long impressive-looking one.

## Step 4 — Stop

Present the report. Do not fix anything. If the user wants remediation, hand off to the rescue protocol with this report as its Step 3 (rot list) pre-filled.

## Evidence discipline

Every finding must be verifiable from the cited location. Never report a suspected issue as confirmed — mark suspicions as "worth verifying" with the verification step. Confident claims about code you didn't actually read are the review-time equivalent of pattern-matched SDK signatures.

## Full method

See [METHOD.md](../../METHOD.md), section "Review is a first-class scenario."
