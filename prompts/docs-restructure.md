# Docs Restructure Prompt Template

Use when a project's documentation has grown by accretion: status stated in
several places, no links, no tables of contents, long files mixing design,
procedure and narrative, tools and tests without an index. Fill the
placeholders; delete what does not apply. The skill version, with the checker
and the move tool, is `skills/docs-restructure/`. For the README content
itself, `prompts/docs-refresh.md` is the sibling: restructure the tree first,
then refresh the words.

---

Restructure the documentation of `{repository path}`. {Branch policy: work on
main / on a branch}. Do not touch code under `{code directories}`. Do not ask
for confirmation of what this brief specifies; report at the end.

## Goal

1. Every document except the journal reads as finished-state text: what the
   system is, how it is built, what a procedure does, what a milestone
   requires. Never how it got there ("now", "currently", "still", "remains",
   "no longer", "latest", "was superseded" belong in the journal or in a
   decision's status field).
2. One home per fact: status in one file, design in one, procedure in one,
   history in one. Every other mention is a link.
3. Findability: every document reachable by a clickable link from an index;
   every tool and gate with one row saying what it does and which document
   owns it; a generated table of contents in every long file.
4. A written rule set for future agents, enforced by a checker.

## What you will find

{Three to eight bullet points from a quick survey: the good series to keep,
the files that state status, the mega-files, the handover or memo documents,
the generated files and their generator, the absence of links or checker or
agent instructions, the normative content that must not be reworded.}

## Target structure

| Kind | Answers | Home |
|---|---|---|
| State | where are we? | `{status file}` - the only status authority |
| Design | how is it built and why? | `{design series / ADRs / specs}` |
| Procedure | what do I run, what does it prove? | `{procedure docs, runbooks, test plans, tool index}` |
| History | what was decided, tried, delivered? | `{decision log}`, `{journal}` (new if absent), `{changelog}` |
| Agent rules | how do agents work here? | `AGENTS.md` (+ one-line `CLAUDE.md` pointing to it) |

Concretely:

- `README.md`: product-facing; status at most five table rows linking
  `{status file}`.
- `{docs index}`: one row per document with a one-line summary.
- `{decision index}`: generated table of decisions with status.
- `{status file}`: one-line status cells; design and procedure link columns.
- `{roadmap or plan}`: the plan only; no status lines.
- `{handover or memo}`: split into agent rules, open questions, decision
  statuses and journal; then delete or date into `memos/`.
- `{tests index}` and `{tools index}`: one row per file, with the owning
  document and the command that runs it.
- `{journal}`: newest first, dated; your first entry describes this work.
- `docs/DOCUMENTATION.md`: the rules; `AGENTS.md` links it.

## Cross-references, links, tables of contents

- A navigation block after the title of every design document: milestones,
  decisions (linked), procedures, gates, runbook; `none` for empty fields;
  derived from what the document already cites.
- Convert every backticked repository path naming an existing file into a
  link, repository-wide, by script; list the ones that do not resolve.
- A generated `<!-- toc -->` block in every file over about 150 lines.

## The checker

Add `{tool dir}/check-docs.py` (Python 3, standard library). It verifies
links and anchors (ignoring fenced code), generates and verifies TOC blocks,
verifies every `{identifier pattern}` reference, requires the navigation block
in design documents, requires index rows for tools and tests, and exits
non-zero with one problem per line. Wire it into `{make / xtask / npm / CI}`
and `CONTRIBUTING.md`.

## Constraints

- Never reword normative text in `{spec / ADR / API locations}`; moving,
  linking, adding a block or a TOC is fine.
- Never renumber a series. Never delete information: what has no home goes to
  the journal with its origin noted.
- Do not rewrite technical bodies you cannot verify against the code; give
  them structure and leave the convert-as-touched rule.
- Follow the repository's commit conventions. Separate commits: tooling;
  indexes and links; status consolidation; splits; rules. Checker green at
  each.
- Move files by script that rewrites inbound and internal links; never by
  hand.

## Order

1. Measure: documents and lines, files with status lines, journey-word count,
   unreferenced documents, unresolved paths.
2. Tooling.
3. Indexes, links, blocks, TOCs.
4. Status consolidation.
5. Splits and narrative extraction.
6. Rules file and agent pointer.
7. Checker green, `git diff --check`, journal entry, commits.

## Report

Before/after numbers; files created, moved, split, deleted; where each part of
a split document went; unresolved paths; what you deliberately did not rewrite
and why; the exact checker command.
