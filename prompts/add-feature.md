# Add-a-Feature Prompt Template

I want to add a new feature to an existing project. You are going to help me design the change and then implement it, but you will not write any code until I explicitly approve the plan in step 5 below.

## Context

- **Project:** [name + one-line description]
- **Where it lives:** [path / repo]
- **Current state:** [working / partly working / known issues]
- **Audience for the code:** [me / a reviewer / customer / future me]
- **Time budget for this feature:** [hours - be honest, including buffer]
- **Defensibility requirement:** [will I walk through this code with someone? if yes, every line must be defensible]
- **Reference materials:** [paths to project docs, NOTES.md, design docs, related code paths]

## The feature

[Describe what you want to add. Be concrete. List user-visible behavior, edge cases you care about, and any explicit non-goals.]

**Why it belongs in this project:** [one sentence on why this fits, not feature-creep]

## Constraints inherited from the project

[List anything the LLM needs to respect - the project's existing patterns. Common ones:]

- **Stack / language version:** [as established]
- **State management / architecture pattern:** [as established - do NOT introduce a new one for this feature]
- **Architectural style:** [match what's already there]
- **File size guidance:** [match the project's convention]
- **Comment style:** [match the project's convention]
- **Dependencies:** [allowed / forbidden / approval-required - default is "no new deps unless I approve"]

## Constraints specific to this feature

- [scope boundary 1]
- [scope boundary 2]
- [explicit non-goals]

## What I want from you in this session - in order

**Step 1 - Read the existing project.**
View [LIST OF FILES/PATHS most relevant to this feature]. Also view NOTES.md and README.md if they exist. Summarize in 3-5 bullets:
- The relevant existing patterns this feature must fit into
- The state container(s) it will touch
- The data flow it will plug into
- Any conventions or constraints visible in the code I might not have remembered

If anything you find contradicts the constraints I gave above, stop and flag it before continuing.

**Step 2 - Verify any unfamiliar APIs.**
If this feature touches an SDK, framework, library, or language feature you haven't verified in the last few sessions, READ THE SOURCE before designing. Confirm exact signatures, parameter shapes, and return types. Flag surprises explicitly. If everything is already familiar from prior work in this project, say so and skip this step.

**Step 3 - Propose the change set.**
List every file that will change. For each:
- Created / modified / deleted
- One-sentence purpose of the change
- Roughly how many lines

Then propose any new file(s) needed, with the same shape as the project's existing file conventions. Group by concern.

**Step 4 - Explain the integration in one paragraph.**
How this feature plugs into the existing data flow: what triggers it, where its state lives, what it reads, what it writes, how the UI sees it. Maximum 200 words. Call out anywhere this is touching shared state and what could go wrong if another feature were also touching it.

**Step 5 - List trade-offs, risks, and what gets touched.**
- 3-5 bullets on trade-offs and what I should be ready to defend
- Anything you are uncertain about (APIs, edge cases, race conditions)
- Explicit list of which existing behaviors could regress if this is implemented carelessly
- Test/verification plan: how will we know the feature works AND that nothing it touches broke

**Step 6 - Wait for my approval.**
Stop and ask me to approve, request changes, or ask questions. DO NOT write any code until I say "go build."

## Style of our interaction going forward

- I will review each chunk you produce. Before generating or modifying a file, tell me what you are about to do and why.
- If I ask you to simplify, err on the side of over-simplifying.
- If you are about to use a pattern, library, or abstraction not already in this project, stop and ask first.
- Match the existing project's conventions even if you would do it differently in a green-field build. Consistency with the existing code matters more than your stylistic preferences.
- For any non-trivial use of an SDK or framework feature you haven't verified, READ THE SOURCE FIRST and confirm exact signatures.
- After each significant change, run the project's analyzer/linter and confirm it passes before declaring done.
- After the feature is working, update NOTES.md with one or two sentences capturing the design choice and any trade-off worth remembering. Add a "With more time" bullet for anything we consciously deferred.

## Done criteria for this feature

The feature is complete when:
- [ ] [USER-VISIBLE BEHAVIOR 1] works on [PLATFORMS]
- [ ] [USER-VISIBLE BEHAVIOR 2] works
- [ ] [EDGE CASE / FAILURE MODE] handled gracefully
- [ ] No regressions in [LIST OF EXISTING BEHAVIORS THE FEATURE INTERACTS WITH]
- [ ] Analyzer/linter passes with zero warnings
- [ ] NOTES.md updated
- [ ] [DEVICE / RUNTIME] tested

When all boxes are ticked, STOP. No follow-on features in this session.

Begin with Step 1.
