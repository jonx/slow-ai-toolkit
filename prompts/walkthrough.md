# Walkthrough Prompt Template

I'm about to present this project to someone. Help me rehearse: find the questions before the reviewer does, and make sure I have honest answers. Do not modify any code - if rehearsal uncovers something that must be fixed first, flag it and its cost.

## Context

- **Project:** [name + one-line description, where it lives]
- **The occasion:** [interview walkthrough / code review / customer demo / team handoff]
- **The audience:** [technical depth, what they care about, what they'll be skeptical of]
- **The format:** [live code tour / demo / screen-share Q&A / async review]
- **Time slot:** [minutes I actually have]
- **The stakes:** [what a great vs. bad outcome looks like]

## What I want from you - in order

**Step 1 - Inventory the story.**
Read NOTES.md (this is what it was for), README.md, and the core code paths. Give me:
- The one-paragraph pitch
- 3-5 **strengths** worth steering the conversation toward - decisions with good rationale, clean seams, honest trade-offs
- The **weak points** - everything a sharp reviewer could poke: shortcuts, deferred work, thin tests, oversized files, defensible-but-questionable dependencies. Be ruthless; better you than them.
- Any **surprises** - things in the code I may have forgotten are there

**Step 2 - Predict the questions.**
The 8-12 questions this audience is most likely to ask, ordered by likelihood, including: two "why X over Y" architecture questions, two aimed straight at the weak points, one "what would you do with more time" (NOTES.md answers it), one scale/failure question, one plausible curveball. For each: a suggested honest answer grounded in the actual decisions. Where a decision was a time-pressure trade-off, the answer says so.

**Step 3 - Script the demo** (if the format includes one).
The exact happy path (commands/clicks, each verified to work right now), the code-tour order (entry point first, then the 2-4 load-bearing files), a fallback for every step that could fail live, and timing that fits the slot with room for questions.

**Step 4 - Rehearse with me.**
Play the reviewer: ask me the Step 2 questions one at a time, push back on weak answers the way the real audience would, and give me one concrete improvement per answer.

**Step 5 - Pre-flight list.**
A short morning-of checklist (build passes, demo path verified, NOTES.md current, stale TODOs fixed or defensible) and the two or three messages I most want to land.

Begin with Step 1.
