#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Move, split or extract Markdown files while keeping every link valid.

    move-doc.py move OLD.md NEW.md
        Move a file. Relative links inside it are rewritten for the new
        location; every inbound link in the repository is rewritten to the new
        path (fragments preserved).

    move-doc.py split FILE.md --into DIR [--level 2] [--name-regex REGEX]
                              [--keep-index]
        Split FILE.md into one file per heading of the given level under DIR.
        The file name is the heading's first regex group (default: the text
        before " - ", " — " or ":"), with "/" mapped to "-", plus ".md". The
        text before the first split heading becomes DIR/README.md (index with
        a table of the parts). Inbound links to FILE.md#anchor are rewritten to
        the part that owned that heading; inbound links to FILE.md are rewritten
        to the index. FILE.md is deleted unless --keep-index, in which case it
        is replaced by the index.

    move-doc.py extract FILE.md "Heading text" TARGET.md [--heading-level 2]
        Cut the section under the given heading (up to the next heading of the
        same or higher level) out of FILE.md and append it to TARGET.md
        (created with a title if missing), relocating its links. Inbound links
        to FILE.md#that-anchor are rewritten to TARGET.md#that-anchor.

Run from anywhere; paths are resolved against --root (default: the git root of
the current directory). Vendored trees are never rewritten.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

EXCLUDED = {".git", "node_modules", "vendor", "third_party", "target", "build", "dist"}
LINK = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = "".join(c for c in text if c.isalnum() or c in " -_")
    return re.sub(r"\s", "-", text)


def md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md")
                  if not any(part in EXCLUDED for part in p.relative_to(root).parts))


def relocate(text: str, old_dir: Path, new_dir: Path) -> str:
    """Rewrite relative links so text authored in old_dir resolves from new_dir."""
    def fix(m: re.Match) -> str:
        target = m.group(2)
        if SCHEME.match(target) or target.startswith(("#", "//")):
            return m.group(0)
        path, sep, frag = target.partition("#")
        absolute = os.path.normpath(old_dir / path)
        return f"{m.group(1)}{os.path.relpath(absolute, new_dir)}{sep}{frag}{m.group(3)}"
    return LINK.sub(fix, text)


def rewrite_inbound(root: Path, old: Path, resolve) -> int:
    """For every link that resolves to `old`, call resolve(fragment) -> (new_path, new_fragment)."""
    count = 0
    old_abs = old.resolve() if old.exists() else Path(os.path.normpath(old))
    for path in md_files(root):
        text = path.read_text(encoding="utf-8")

        def fix(m: re.Match) -> str:
            nonlocal count
            target = m.group(2)
            if SCHEME.match(target) or target.startswith(("#", "//")):
                return m.group(0)
            rel, sep, frag = target.partition("#")
            if Path(os.path.normpath(path.parent / rel)) != Path(os.path.normpath(old_abs)):
                return m.group(0)
            new_path, new_frag = resolve(frag)
            count += 1
            new_rel = os.path.relpath(new_path, path.parent)
            return f"{m.group(1)}{new_rel}{'#' + new_frag if new_frag else ''}{m.group(3)}"

        new_text = LINK.sub(fix, text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
    return count


def sections(lines: list[str], level: int) -> list[tuple[int, int, str]]:
    """(start, end, heading text) for every heading of exactly `level`, outside fences."""
    starts, in_fence = [], False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        m = HEADING.match(line)
        if not in_fence and m and len(m.group(1)) == level:
            starts.append((i, m.group(2)))
    out = []
    for n, (start, text) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        out.append((start, end, text))
    return out


def git_mv(root: Path, old: Path, new: Path) -> None:
    new.parent.mkdir(parents=True, exist_ok=True)
    tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", str(old)],
                             capture_output=True).returncode == 0
    if tracked:
        subprocess.run(["git", "-C", str(root), "mv", str(old), str(new)], check=True)
    else:
        old.rename(new)


def cmd_move(root: Path, args) -> None:
    old, new = (root / args.old).resolve(), (root / args.new)
    text = relocate(old.read_text(encoding="utf-8"), old.parent, new.parent)
    git_mv(root, old, new)
    new.write_text(text, encoding="utf-8")
    n = rewrite_inbound(root, old, lambda frag: (new.resolve(), frag))
    print(f"moved {args.old} -> {args.new}; inbound links rewritten: {n}")


def cmd_split(root: Path, args) -> None:
    source = (root / args.file).resolve()
    into = (root / args.into)
    into.mkdir(parents=True, exist_ok=True)
    lines = source.read_text(encoding="utf-8").splitlines()
    parts = sections(lines, args.level)
    if not parts:
        sys.exit(f"no level-{args.level} headings in {args.file}")
    name_re = re.compile(args.name_regex)
    anchor_map: dict[str, Path] = {}
    rows = []
    for start, end, heading in parts:
        m = name_re.search(heading)
        name = (m.group(1) if m else heading).strip().replace("/", "-")
        part = into / f"{slug(name).upper() if name.isupper() else slug(name)}.md"
        if name == name.upper() or re.match(r"^[A-Z0-9/-]+$", name):
            part = into / f"{name}.md"
        body = "\n".join(lines[start + 1:end]).strip("\n")
        body = relocate(body, source.parent, into)
        part.write_text(f"# {heading}\n\n{body}\n", encoding="utf-8")
        # every heading inside the part maps to the part; the part heading maps to its top
        anchor_map[slug(heading)] = part
        for _, lvl, txt in [(i, len(HEADING.match(l).group(1)), HEADING.match(l).group(2))
                            for i, l in enumerate(lines[start + 1:end]) if HEADING.match(l)]:
            anchor_map[slug(txt)] = part
        title = heading.split(" - ", 1)[-1].split(" — ", 1)[-1].split(": ", 1)[-1]
        rows.append(f"| [{name}]({part.name}) | {title} |")
    preamble = "\n".join(lines[:parts[0][0]]).strip("\n")
    preamble = relocate(preamble, source.parent, into)
    index = into / "README.md"
    index.write_text(preamble + "\n\n| Part | What |\n|---|---|\n" + "\n".join(rows) + "\n",
                     encoding="utf-8")

    def resolve(frag):
        if frag and frag in anchor_map:
            part = anchor_map[frag]
            return part.resolve(), ("" if slug(part.read_text().splitlines()[0][2:]) == frag else frag)
        return index.resolve(), ""

    n = rewrite_inbound(root, source, resolve)
    if args.keep_index:
        source.write_text(relocate(index.read_text(encoding="utf-8"), into, source.parent),
                          encoding="utf-8")
    else:
        subprocess.run(["git", "-C", str(root), "rm", "-q", "--cached", str(source)], capture_output=True)
        source.unlink()
    print(f"split {args.file} into {len(parts)} parts under {args.into}; inbound links rewritten: {n}")


def cmd_extract(root: Path, args) -> None:
    source = (root / args.file).resolve()
    target = (root / args.target)
    lines = source.read_text(encoding="utf-8").splitlines()
    parts = sections(lines, args.heading_level)
    match = [p for p in parts if p[2].strip() == args.heading.strip()]
    if not match:
        sys.exit(f"heading {args.heading!r} (level {args.heading_level}) not found in {args.file}")
    start, end, heading = match[0]
    body = "\n".join(lines[start:end]).strip("\n")
    body = relocate(body, source.parent, target.parent)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        existing = target.read_text(encoding="utf-8").rstrip("\n")
        target.write_text(existing + "\n\n" + body + "\n", encoding="utf-8")
    else:
        target.write_text(f"# {target.stem}\n\n{body}\n", encoding="utf-8")
    del lines[start:end]
    source.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
    anchor = slug(heading)
    n = rewrite_inbound(root, source,
                        lambda frag: (target.resolve(), frag) if frag == anchor else (source, frag))
    print(f"extracted {heading!r} from {args.file} to {args.target}; inbound links rewritten: {n}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=__doc__)
    parser.add_argument("--root", type=Path, default=None)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("move"); p.add_argument("old"); p.add_argument("new")
    p = sub.add_parser("split"); p.add_argument("file"); p.add_argument("--into", required=True)
    p.add_argument("--level", type=int, default=2)
    p.add_argument("--name-regex", default=r"^(.+?)(?:\s+-\s+|\s+—\s+|:\s+)")
    p.add_argument("--keep-index", action="store_true")
    p = sub.add_parser("extract"); p.add_argument("file"); p.add_argument("heading")
    p.add_argument("target"); p.add_argument("--heading-level", type=int, default=2)
    args = parser.parse_args()
    root = args.root
    if root is None:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        root = Path(out.stdout.strip() or ".")
    root = root.resolve()
    {"move": cmd_move, "split": cmd_split, "extract": cmd_extract}[args.command](root, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
