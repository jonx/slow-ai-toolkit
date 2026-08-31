---
name: docs-restructure
description: Apply the Slow AI docs-restructure protocol when a project's documentation has grown by accretion and needs restructuring rather than a rewrite - status stated in several places, no links between documents, no tables of contents, long files that mix design, procedure and narrative, a README status section nobody can read, tools and tests with no index. Use when the user says "clean up the docs", "restructure the documentation", "the docs are a mess", "nettoie la doc", "reorganise la doc", "I can't find where things are documented", or asks for documentation maintenance rules for agents. It is the structural sibling of docs-refresh - refresh makes the words true, restructure gives every fact one home. Run restructure first when the tree itself is the problem. The protocol measures first, moves and links by script, consolidates status into one file, converts prose to finished-state text, writes the rules for future agents and adds a checker that enforces them. Not for verifying and rewriting README content against the code (docs-refresh) or for punctuation (deaiify).
---

# Slow AI - Docs Restructure

You are applying the **Slow AI** working method to a documentation tree that
has accreted. The principle: documentation is a product, not a diary. Every
document except the journal describes the finished system, every fact has one
home, and everything is reachable by a link. Structure is fixed by scripts and
kept by a checker; prose is fixed section by section as it is touched.

Two failure modes this protocol exists to prevent:

- **Accretion.** Each session appends a paragraph to the README status, the
  milestone table, the journal, the changelog and the design doc. Six copies of
  every fact; none readable.
- **Rewrite by enthusiasm.** An agent rewrites 3,000 lines of technical prose
  it cannot verify, and the documentation now contradicts the code.

The cure is mechanical work on structure and links, a small number of hand
rewrites of the top-level documents, and a rule that converts the rest over
time.

Bundled with this skill:

- `check-docs.py` - a repository-local checker: links, anchors, generated
  tables of contents, identifier references, navigation blocks, index
  membership. Copy it into the repository's tool directory and adapt the
  `CONFIG` block.
- `move-doc.py` - move, split or extract Markdown files while rewriting the
  relative links inside them and every inbound link in the repository.
- `templates/DOCUMENTATION.md` - the rule set for future agents, to adapt.
- `../../prompts/docs-restructure.md` - a paste-anywhere version of this
  protocol for agents that do not load skills.

## Relation to docs-refresh

Two disciplines, two skills:

- **docs-refresh** makes the words true: it verifies every claim against the
  code and rewrites the README around what-is / where-going / where-now.
- **docs-restructure** (this skill) makes the tree navigable: one home per
  fact, links, tables of contents, status in one file, rules and a checker.

When both are needed, restructure first, then refresh: the refresh rewrite of
the README and the status file is Step 8 below, and it applies the
docs-refresh rules (verify every command, three questions, no journey). A
refresh on an unstructured tree produces a true README beside six stale
copies of the same status.

## Step 0 - Establish the mode and the ground

Decide the **mode** from the request:

- *"give me recommendations"*, *"what would you change"* - assess only: run
  Steps 1 and 2, report, stop.
- *"clean it up"*, *"do it"* - execute: run every step; do not ask for
  confirmation of what this protocol already specifies.

Then check the ground, before reading a single document:

1. `git status --short` and `ps` for other agent sessions. If another session
   is editing the same tree, every write must re-read the file first, you must
   never revert its edits, and you commit only the files you own. Say so in
   the report.
2. Commit conventions: `CONTRIBUTING.md`, recent `git log`. Some repositories
   forbid AI attribution in trailers; follow the repository, not your default.
3. Branch policy: what the user said. If nothing, work on a branch and say so.
4. Protected content, to move but never reword: normative specifications,
   ADRs and decision records, API headers, generated files (`FILE_INDEX`,
   checksums, changelogs produced by tools), anything under `vendor/`,
   `third_party/`, `node_modules/`, `target/`, `build/`.
5. The license header convention of the repository, for every new file.

## Step 1 - Measure, read-only

Collect these numbers; they are the before column of the report.

| Measure | How |
|---|---|
| Documents and lines, excluding vendored trees | `find . -name '*.md' \| xargs wc -l`, sorted |
| Link graph | count outbound links per file, inbound per target; list documents nobody links to |
| Backticked paths that should be links | grep for `` `[a-z0-9_./-]+\.md` `` |
| Tables of contents | files over 150 lines without a `<!-- toc -->` block |
| Status duplication | files containing `Status:` or a "current position" paragraph; count the places where the same milestone is described |
| Journey wording | count of *now, new, still, remains, no longer, latest, currently, today* in non-journal documents |
| Revisions and dates in prose | commit hashes and dates in design documents |
| Mega-files | any document over 500 lines; its `##` sections and their sizes |
| Indexes | is every tool, script, test plan, `make` target, ADR listed somewhere with one line of purpose |
| Agent instructions | `CLAUDE.md`, `AGENTS.md`, an existing rule set, an existing checker |
| Generated files | who generates them; whether they are committed |

Sample three documents of each kind and read them in full. The numbers say
where; the samples say what the text actually does wrong.

## Step 2 - Diagnose and name the target map

Write the diagnosis as a table of symptom and measure. Then assign every
existing document to one of four kinds and name its home:

| Kind | Answers | Typical home |
|---|---|---|
| State | where are we | one milestones or status file |
| Design | how is it built and why is it bounded that way | one document per area, numbered series, ADRs, specs |
| Procedure | what do I run and what does it prove | development procedure, runbooks per area, test plans, hardware or experiment cards |
| History | what was decided, tried, delivered | decision log or ADRs, journal, changelog, TODO |

Rules for the map:

- Keep existing numbering (`docs/12-*.md`, `ADR-034`) and existing good
  series. Restructuring is not renumbering.
- A file that mixes kinds gets split; a file that duplicates a home gets
  replaced by a link.
- A point-in-time document (a handover, a review memo, a proposal) goes to a
  `memos/` folder with a date, or is split into the homes it was standing in
  for.
- Name what you will **not** rewrite: the technical bodies of design documents
  you cannot verify against the code. They get structure (block, TOC, links)
  and the convert-as-touched rule, not a rewrite.

In assess mode, stop here. Present the diagnosis, the target map, and the
recommendations in the order they should be executed, each with the measure it
fixes.

## Step 3 - Tooling first

Nothing after this step is done without a check that would fail if it were
undone.

1. Copy `check-docs.py` into the repository's tool directory. Adapt `CONFIG`:
   excluded trees, identifier contracts (decision IDs, card IDs, milestone
   IDs - each a regex plus where it must resolve), navigation-block contracts
   (which files must carry which block), index contracts (which directory
   must be listed in which index).
2. Wire it into the repository's usual entry point: a `make` target, a
   `cargo xtask`, an npm script, CI. One line in `CONTRIBUTING.md`.
3. Run it once and keep the baseline output. It will fail; that is the work
   list.

The checker ignores fenced code, so examples in the rules document do not
trigger it. Do not put placeholder identifiers such as `HT-XX` in prose;
use `HT-*`.

## Step 4 - Move and split by script, never by hand

Use `move-doc.py` for every move, split and extraction. It rewrites the
relative links inside the moved text and every inbound link in the
repository, and maps old heading anchors to the new files when a document is
split. Hand-moving text loses links every time.

- Splitting a card file, a test plan or a runbook collection: one file per
  `##` section, named after the identifier in the heading, plus an index that
  keeps the preamble. Keep the old path as the index if other sessions edit
  it, so their next edit fails visibly instead of silently.
- Extracting procedures from a procedure document into per-area runbooks:
  extract sections to `RUNBOOK.md` beside the area's design document, with a
  two-line header linking the design document and the procedure index.
- A flat 600-line section with no headings: split at paragraph boundaries you
  name explicitly by their first words; route each piece; give each a heading.

Run the checker after every batch.

## Step 5 - Indexes, links, blocks, tables of contents

1. **Indexes.** One row per document in the documentation map; one row per
   area in the feature index (design link, runbook link); one row per tool in
   the tools index with the design document that owns it; one row per gate in
   the tests index with the command that runs it; a generated index of
   decisions or ADRs (`--write-toc` on the decision log, or the ADR index
   generator).
2. **Links.** Convert backticked paths that name an existing file into links,
   repository-wide, by script. List the ones that do not resolve.
3. **Navigation block** at the top of every design document, right after the
   title and license comment. It names the milestones, the decisions (linked
   to their anchors), the experiment cards, the gates, the runbook. `none` for
   an empty field. Derive it from what the document already cites; never
   invent a relation. Generate it from a mapping you author once; do not type
   twenty-five blocks by hand.
4. **Tables of contents** in every file over about 150 lines, generated by
   `check-docs.py --write-toc`, never hand-written. Not in short files.

## Step 6 - Consolidate status

- The status file gets one table per ladder, one line per milestone: state in
  backticks, what passes, what is open, links to the design document and the
  card. Acceptance text is the finished-state requirement and does not change
  with status.
- A "where we are" block of at most six rows at the top.
- Revisions, commit hashes and build stamps live in one table in the status
  file and nowhere else in the documentation.
- The README status section becomes at most five table rows plus a link.
- Every other place that stated status (roadmap, handover, design documents,
  per-file `Status:` lines) loses it and links instead.

## Step 7 - Extract narrative

Journey text is not deleted; it is moved. Paragraphs that narrate attempts,
fixes, "the first run exposed", "was corrected", superseded ideas:

- into the journal (`NOTES.md`, newest first, dated entries, links to what
  they touched) - create it if the repository has none;
- superseded decisions into the status field of the decision they belong to;
- open questions into one `open-questions.md` table: question, options, what
  would decide it.

A point-in-time handover document is split this way and then deleted or dated
into `memos/`.

## Step 8 - Rewrite the top, write the rules, point the agents

Hand-rewrite only these, as finished-state text, applying the docs-refresh
rules (verify every command you show; what is this, where is it going, where
is it now): the root README (what it is, what it is not, architecture, how to
build and verify, repository map, documentation map, license), the documentation map, the status file, the
development procedure (gate table plus rules), and the index files. Everything
else keeps its body.

Then write the rule set from `templates/DOCUMENTATION.md`: the one rule, the
four kinds and their homes, per-document rules, the navigation-block format,
the TOC rule, the checklist before commit, and the convert-as-touched rule.
Make `CLAUDE.md` or `AGENTS.md` point to it and repeat its four hardest rules
in five lines. If the repository has neither, create `AGENTS.md` and a
one-line `CLAUDE.md` that points to it.

## Step 9 - Verify, journal, commit

- The checker passes. `git diff --check` is clean.
- Sample five converted documents and read them top to bottom.
- Journal entry describing the restructuring, with links.
- Commit in logical units (tooling; moves; indexes and links; status; rules),
  each with the checker green, following the repository's conventions. If
  another session is active, stage your files explicitly; never `git add -A`.

## What not to do

- Do not rewrite technical bodies you cannot verify against the code. Give
  them structure; leave the rule to convert them as they are touched.
- Do not reword normative text, ADRs or specifications. Moving, linking and
  adding a block or a TOC change no meaning; rewording does.
- Do not renumber a series.
- Do not delete information. Anything without a home goes to the journal with
  its origin noted.
- Do not add a TOC to a short file, a block to a non-design file, or a
  checker rule the repository does not need.
- Do not write the checker to read links inside code fences; examples will
  break it.
- Do not remove a block or a section by pattern without re-inserting what the
  pattern also matched; a block-replacement script once deleted the one
  hand-written block it was meant to keep.
- Do not commit another session's uncommitted code because it sits in the
  same tree.
- Do not scatter "no claim", "unverified", "target-inert" through every
  sentence. One evidence banner per document.

## Report

End with: the before and after numbers from Step 1; files created, moved,
split, deleted; where each part of any split document went; unresolved paths;
what you deliberately did not rewrite and why; the exact command that runs the
checker; and, if another session was active, which of its files you left
untouched.
