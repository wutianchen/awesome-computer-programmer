# Claude

There are two categories of claude toolbox, native builtin and customize. Like there are builtin subagents which come from claude and customize subagents that customer can build for their own purpose.

## Marketplace

https://claudemarketplaces.com/


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

## Harness

#### MCP Server

[MCP Server Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) is an open-source standard for connecting AI applications to external systems. Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems

* [mcp](./mcp.md)

#### Skill

[Agent Skill](https://agentskills.io/home) are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows

* [openskills](https://www.skillsdirectory.com/)
* [skill](./skill.md) (previous feature `custom slash command` merged into `skill` ?)
* [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)

#### Language Server Protocol

[Language Server Protocol](https://microsoft.github.io/language-server-protocol/) is meant to provide the language-specific smarts and communicate with development tools over a protocol that enables inter-process communication. See the list of [implementations](https://microsoft.github.io/language-server-protocol/implementors/servers/)

LSP can be used together with mcp-lsp server like

* [serena](https://github.com/oraios/serena) top consideration

other minor ones (based on github stars):

* [mcp-language-server](https://github.com/isaacphi/mcp-language-server)
* [lsp-mcp](https://github.com/jonrad/lsp-mcp)


### Tool

tbd.

### Hook

tbd.



## Relevant source of information

- [Antropic Engineering Blog](https://www.anthropic.com/engineering)
- [Antropic Blog](https://claude.com/blog)
- [Antropic Academy](https://www.anthropic.com/learn)
* [claude plugins](https://claude.com/plugins)


## Questions

* when is the context of skill and mcp injected into claude main agent 

* [subagent](./subsgent.md)
* Agent
* claude bultin slash command (complementary of the custom slash command)
* [coworkder](https://claude.com/product/cowork)
* Agent Teams