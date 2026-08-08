---
name: give-eyes
description: Apply the Slow AI give-eyes protocol when starting work on any project whose output is visual, interactive, or long-running - GUIs, web frontends, TUIs, games, emulated or embedded systems, anything with a screen or a stateful runtime. Use when the user says "give yourself eyes", "build an observation harness", "you need to see what you're doing", "set up headless screenshots", "you should be able to drive this yourself", or at the start of any session where the agent would otherwise be unable to verify its own output. The protocol builds two capabilities before any feature work: a scriptable way to SEE the running artifact (screenshots, framebuffer dumps, logs) and a puppeteer to DRIVE it (programmatic input). All later "done" verdicts must cite observation artifacts produced by this harness.
---

# Slow AI - Give Eyes

You are applying the **Slow AI** working method's observability principle: **eyes before hands**.

An agent that cannot observe what it builds is guessing. Before any feature work on a project with visual, interactive, or long-running output, build the harness that lets you see the artifact and drive it - headlessly, scriptably, without a human in the loop.

Do not start feature work until the harness exists and you have demonstrated it working with a real captured artifact.

## Step 0 - Assess the observation problem

Answer, in writing:

- **What does this project produce?** (web UI / desktop GUI / TUI / mobile app / emulated OS / game / service / CLI)
- **What can I already observe?** (stdout, exit codes, log files, test output)
- **What am I currently blind to?** (rendered layout, visual state, interactive behavior, boot sequence, timing)
- **What input can I already send, and what can't I?** (clicks, keystrokes, navigation, API calls, serial input)

The gap between "blind to" and "can't send" defines the harness scope.

## Step 1 - Propose the harness

Pick the techniques that fit the platform. Reference menu (not exhaustive - verify tool availability on the actual system first):

| Target | See | Drive |
|---|---|---|
| Web frontend | Playwright/Puppeteer headless screenshot, DOM dump, console log capture | Playwright/Puppeteer: click, type, navigate, evaluate |
| Desktop GUI (Linux) | `xvfb-run` + `import`/`scrot`/`grim`, window-manager state dumps | `xdotool`/`ydotool` key and mouse injection |
| Desktop GUI (macOS) | `screencapture`, accessibility tree dumps | AppleScript / `cliclick` |
| Mobile | `xcrun simctl io screenshot`, `adb exec-out screencap` | `simctl`/`adb input` taps, keys, deep links |
| Emulated / embedded OS | QEMU QMP `screendump`, serial console logs, GDB stub state | QMP input events, serial keystrokes, monitor commands |
| TUI | `tmux capture-pane`, script/typescript recording | `tmux send-keys` |
| Game / canvas | Frame capture hooks, deterministic seed + state dump | Scripted input events, replay files |
| Service / API | Structured logs, health endpoints, response snapshots | `curl`/client scripts with assertions |

Propose, as a plan (this is a normal Slow AI chunk - four gates apply):

- The **see** command: one invocation → one timestamped artifact in a known directory (e.g. `harness/captures/`)
- The **drive** interface: how input is expressed (a script, a command vocabulary, a scenario file)
- The **loop** target: the composed `build → launch → drive → observe → verdict` command a session can run repeatedly
- Where it all lives in the repo (`tools/` or `harness/`, a Makefile/script entry point)

Wait for approval before building.

## Step 2 - Build the smallest working loop

Implement see + drive minimally, then prove the loop end-to-end **once**: launch the artifact, send one input, capture one observation, show it. A screenshot of a blank window that you opened programmatically beats a sophisticated harness that hasn't run.

Common traps to handle now, not later:

- **Timing** - capture after render/boot settles; poll for a readiness signal instead of `sleep` guesswork where possible.
- **Determinism** - fixed window size / viewport / resolution so captures are comparable across runs.
- **Teardown** - the loop must kill what it launched; orphaned processes poison the next iteration.
- **Artifact hygiene** - timestamped filenames, one directory, gitignored unless a capture is promoted to documentation.

## Step 3 - Make verdicts evidence-based

From this point on in the project, every "it works" claim cites evidence:

- "The login form renders - see `harness/captures/2026-07-14T10-32_login.png`."
- "Boot reaches the shell - serial log line 214: `[init] shell ready`."
- "The regression is fixed - before/after captures attached."

If you cannot produce evidence for a claim, say "unverified" - never assert. Unverifiable behaviors get named explicitly, with the manual check the human must perform.

## Step 4 - Document the eyes

The harness is a deliverable:

- README section: how to run the see command, the drive interface, and the full loop, in three commands or fewer.
- `NOTES.md` entry: what the harness covers, what it deliberately doesn't, known flakiness.
- The harness outlives the session. The next agent - or the next you - inherits working eyes.

## When the harness is overkill

A pure library, a batch script, a data pipeline with textual output - the existing test suite *is* the eyes. Say so explicitly, confirm test output is genuinely observable, and skip the visual harness. The principle still holds: verdicts cite evidence (test runs), never vibes.

## Full method

See [METHOD.md](../../METHOD.md), section "Eyes before hands," for the rationale.
