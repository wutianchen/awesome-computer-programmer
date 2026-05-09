# Claude

There are two categories of claude toolbox, native builtin and customize. Like there are builtin subagents which come from claude and customize subagents that customer can build for their own purpose.

## Marketplace

https://claudemarketplaces.com/


## Modes

```
┌──────────────────┬─────────────────┬─────────────────────────────────────────────────────────────────────────────┐
│       Mode       │     Toggle      │                                 Description                                │
├──────────────────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ Plan Mode        │ Shift+Tab       │ Read-only analysis; creates a plan before making changes                   │
├──────────────────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ Fast Mode        │ /fast           │ 2.5x faster responses, same Opus 4.6 model                                │
├──────────────────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ Memory Mode      │ /memory         │ Persistent file-based memory across sessions (on by default)               │
├──────────────────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ Extended         │ Option+T /      │ Deep reasoning for complex problems; adjust depth with /effort             │
│ Thinking         │ Alt+T           │ low|medium|high|max                                                        │
├──────────────────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────┤
│ Auto-Accept Mode │ Shift+Tab       │ Automatically approves edits without asking                                │
└──────────────────┴─────────────────┴─────────────────────────────────────────────────────────────────────────────┘
```

The first three (Plan, Auto-Accept, Normal) are permission modes you cycle through with Shift+Tab. Fast mode, memory, and thinking mode are independent toggles you can combine with any permission mode.

## Session vs Project

A **session** is a conversation with Claude Code. Each time you run `claude`, you start a new session. It includes all messages, tool calls, and results within that conversation.

- Resume a session: `claude --continue`
- Fork a session: `claude --continue --fork-session`

A **project** is your codebase/directory where you run Claude Code. It includes your files, git state, `CLAUDE.md`, and memory.

**How they relate:**

- Sessions are scoped to a project (directory) — resuming only shows sessions from that directory
- Multiple sessions can exist for one project (different conversations about different tasks)
- Persistent knowledge (`CLAUDE.md`, memory) carries across sessions — this is how Claude remembers context between conversations

In short: **a project is where your code lives; a session is a conversation about that code.**

---

## Toolbox

* Tool
* [mcp](./mcp.md)
* [skill](./skill.md) (previous feature `custom slash command` merged into `skill` ?)
* [subagent](./subsgent.md)
* Agent
* hook
* plugin
* claude bultin slash command (complementary of the custom slash command)
* [coworkder](https://claude.com/product/cowork)
* Agent Teams



Questions:
* when is the context of skill and mcp injected into claude main agent 


## Relevant source of information

- [Antropic Engineering Blog](https://www.anthropic.com/engineering)
- [Antropic Blog](https://claude.com/blog)
- [Antropic Academy](https://www.anthropic.com/learn)


## Resources

* [claude plugins](https://claude.com/plugins)
* [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)