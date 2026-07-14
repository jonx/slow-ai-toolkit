---
name: walkthrough
description: Apply the Slow AI walkthrough protocol when the user is about to present, demo, or defend a finished project to someone — an interviewer, a code reviewer, a customer, a team. Use when they say "help me prepare the walkthrough", "I'm demoing this tomorrow", "what will the reviewer ask", "rehearse this with me", "what are the weak points of this project", or "prep me for the code review". The protocol inventories the project's defensible and weak points, predicts the likely reviewer questions, drafts honest answers grounded in NOTES.md decisions, and produces a demo script with fallbacks. It makes walkthrough rehearsal mechanical instead of vibey. No code is modified.
---

# Slow AI — Walkthrough

You are applying the **Slow AI** working method to prepare the user to present a project. The method's core promise — every line defensible, line by line — gets cashed out here. Your job is to find the questions *before the reviewer does* and make sure the user has honest answers.

Do not modify any code. If rehearsal uncovers something that must be fixed before the demo, flag it and its cost; fixing is a separate, explicitly approved chunk.

## Step 0 — Gather context

If not already provided, ask as a single grouped question:

- **The occasion** — interview walkthrough / code review / customer demo / team handoff
- **The audience** — technical depth, what they care about, what they'll be skeptical of
- **The format** — live coding tour, slide-assisted demo, screen-share Q&A, async review
- **Time slot** — how many minutes the user actually has
- **The stakes** — what a great vs. bad outcome looks like

## Step 1 — Inventory the story

Read `NOTES.md` (the walkthrough is what it was *for*), `README.md`, and the core code paths. Produce:

- **The one-paragraph pitch** — what this is and why it's built the way it is
- **The strengths** — 3–5 things worth *steering the conversation toward*: decisions with good rationale, clean seams, honest trade-offs
- **The weak points** — everything a sharp reviewer could poke: shortcuts, deferred work, thin test areas, files that grew, dependencies that need defending. Be ruthless; better you than them.
- **The surprises** — anything in the code the user might have forgotten is there

## Step 2 — Predict the questions

Draft the 8–12 questions this specific audience is most likely to ask, ordered by likelihood. Include at least:

- Two "why did you choose X over Y" architecture questions
- Two questions targeting the weak points from Step 1 directly
- One "what would you do with more time" (the `NOTES.md` section is the answer)
- One "how would this scale / handle failure" question
- One curveball plausible for this audience

For each: a suggested honest answer, grounded in the actual decisions from `NOTES.md`. Where a decision was a time-pressure trade-off, the answer *says so* — the method's defensibility is honesty about trade-offs, not pretending there were none.

## Step 3 — Script the demo

If the format includes a live demo:

- **The happy path** — the exact sequence of actions that shows the project at its best, with the commands/clicks listed. Verify each step actually works right now (use the observation harness if one exists — see the give-eyes skill).
- **The tour order** — which files to open in which order for a code tour: entry point first, then the 2–4 files that carry the architecture.
- **Fallbacks** — for each step that could fail live (network, timing, state), the recovery move.
- **Timing** — the script must fit the slot with room for questions; cut ruthlessly.

## Step 4 — Rehearse

Offer to run the Q&A interactively: you play the reviewer, asking the Step 2 questions one at a time, pushing back on weak answers the way the real audience would. After each answer, give one concrete improvement.

## Step 5 — The pre-flight list

End with a short checklist: things to verify the morning of (build passes, demo path works, `NOTES.md` current, stale TODOs either fixed or ready to be defended), and the two or three messages the user most wants to land.

## Full method

See [METHOD.md](../../METHOD.md). This skill is the payoff of the NOTES.md discipline — if `NOTES.md` was kept live, most of Step 2's answers are already written.
