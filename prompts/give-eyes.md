# Give-Eyes Prompt Template

Before we do any feature work on this project, you are going to build yourself eyes: a scriptable way to SEE the running artifact and a puppeteer to DRIVE it, headlessly, without me in the loop. From then on, every "it works" claim you make must cite an observation artifact (screenshot, log excerpt, captured output) — never an assertion.

## Context

- **Project:** [name + one-line description]
- **Where it lives:** [path / repo]
- **What it produces:** [web UI / desktop GUI / TUI / mobile app / emulated OS / game / service]
- **How it's launched today:** [command(s), environment, anything fiddly]
- **What you can already observe:** [stdout / logs / test output / nothing]
- **What you're blind to:** [rendered layout / boot sequence / interactive behavior / …]
- **Available tooling:** [e.g. QEMU with QMP, Playwright installed, xvfb available, simulator — or "unknown, check the system"]
- **Constraints:** [e.g. "harness lives in tools/", "no new heavy dependencies without approval", "must run in CI"]

## What I want from you in this session — in order

**Step 1 — Assess the observation gap.**
State in writing what this project produces, what you can already observe, what you're blind to, and what input you can and can't send. Verify which candidate tools are actually available on this system before proposing to use them.

**Step 2 — Propose the harness.**
- The **see** command: one invocation → one timestamped artifact in a known directory
- The **drive** interface: how programmatic input is expressed (script, command vocabulary, scenario file)
- The **loop**: the composed build → launch → drive → observe → verdict command
- Where it lives in the repo and how it's invoked (Makefile target, script)
- Trade-offs and risks: timing/readiness detection, determinism (fixed viewport/resolution), teardown, artifact hygiene

**Step 3 — Wait for my approval.** Do not build until I say "go build."

**Step 4 — Build the smallest working loop and prove it.**
Launch the artifact, send one input, capture one observation, show me the artifact. A dumb harness that ran beats a clever one that didn't.

**Step 5 — Document the eyes.**
README section (see/drive/loop in ≤3 commands), NOTES.md entry (coverage, gaps, known flakiness). The harness is a deliverable that outlives this session.

## Ground rules going forward

- Verdicts cite evidence: "renders correctly — see [capture path]" or "boots to shell — serial log line N." If you can't produce evidence, say "unverified."
- If some behavior genuinely can't be observed headlessly, name it explicitly and tell me precisely what to check manually.
- The loop must clean up after itself — no orphaned processes.

Begin with Step 1.
