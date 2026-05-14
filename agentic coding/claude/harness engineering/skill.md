# Skill

There are two main reasons for the skill feature

1. modularize and DRY the prompt and context
2. context management ([progressive disclosure](https://www.youtube.com/watch?v=DQHFow2NoQc))


Skill gives us access to 1) tools 2) resources (like mcp)

## Skill Priority

There's a clear priority order:

1. Enterprise (managed-setting.json) — managed settings, highest priority
2. Personal (~/.claude/skills) — your home directory
3. Project (project/.claude/skills) — the .claude/skills directory inside a repository
4. Plugins (project/.claude-plugin/.claude/skills) — installed plugins, lowest priority

## Best Practices

* `name`
* `description`
* `allowed-tools`: restricts which tools Claude can use when the skill is active — useful for read-only or security-sensitive workflows
* keep SKILL.md under 500 lines and link to supporting files (references, scripts, assets) that Claude reads only when needed
* Scripts execute without loading their contents into context — only the output consumes tokens, keeping context efficient

The open standard suggests organizing your skill directory with:

- scripts/ — Executable code
- references/ — Additional documentation
- assets/ — Images, templates, or other data files

## Compare to slash command

* CLAUDE.md loads into every conversation and is best for always-on project standards. Skills load on demand and are best for task-specific expertise
* Subagents run in isolated execution contexts — use them for delegated work. Skills add knowledge to your current conversation
* Hooks are event-driven (fire on file saves, tool calls). Skills are request-driven (activate based on what you're asking)
* MCP servers provide external tools and integrations — a different category entirely from skills

P.S. slash commands (which require explicit invocation) is merged into skill

## References

* [Claude Skills Explained in 23 Minutes](https://www.youtube.com/watch?v=vEvytl7wrGM)
* [Debug Skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434530) and [skill validator](https://github.com/agentskills/agentskills/tree/main/skills-ref)