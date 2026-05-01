# Installing the Slow AI skill

The file [`SKILL.md`](SKILL.md) in this directory is a Claude Code skill. When installed, it loads automatically into agent sessions whose first user message matches its trigger keywords ("help me build", "add this feature", "rescue this codebase", etc.) and prompts the agent to apply the method.

## Install (Claude Code)

Claude Code looks for skills under `~/.claude/skills/<name>/SKILL.md`. Either copy or symlink:

### Symlink (recommended — keeps the skill in sync with this repo)

```sh
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skill" ~/.claude/skills/slow-ai
```

That's it. Next time you start Claude Code, the skill loads.

### Copy (use if you'd rather snapshot a version)

```sh
mkdir -p ~/.claude/skills/slow-ai
cp SKILL.md ~/.claude/skills/slow-ai/
```

You'll need to copy again whenever the skill changes.

## Verify

Open a new Claude Code session in any project and say something like *"help me build a small CLI"* or *"add a feature to this app"*. The skill should fire and the agent should respond with the four-gate protocol instead of jumping into code.

If it doesn't:

- Check `~/.claude/skills/slow-ai/SKILL.md` is readable.
- Check the YAML frontmatter at the top of `SKILL.md` is intact.
- Check that no other skill is overriding it (skills with overlapping triggers will queue; usually fine).

## Other agent runtimes

The skill is plain markdown with a YAML header. The body (everything below the frontmatter) is what describes the method to the agent — that part is fully portable. Concrete adaptations:

- **Cursor:** copy the body of [`SKILL.md`](SKILL.md) into `.cursor/rules/slow-ai.mdc` in your project, or into Cursor's user-level rules. Cursor will surface it on every relevant session.
- **Aider:** save the body as `slow-ai.md` somewhere convenient, then `aider --read slow-ai.md` (or add `read: [slow-ai.md]` to `.aider.conf.yml`).
- **Continue:** add the body to your `~/.continue/config.json` system message, or to a project-level rules file.
- **Cline / Roo Code:** paste the body into the tool's "Custom Instructions" field.
- **Plain ChatGPT, Claude.ai web, Gemini:** paste the body as the first message of a conversation, or into the tool's custom-instructions setting if it has one.
- **API-level integrations:** prepend the body to the system prompt of any agent loop you control.

In tools without auto-loading, you can also skip the skill entirely and paste a [prompt](../prompts/) directly — the prompts are self-contained protocols that already encode the method.

## Uninstall

```sh
rm ~/.claude/skills/slow-ai
```

(Or `rm -rf` if you copied instead of symlinked.)
