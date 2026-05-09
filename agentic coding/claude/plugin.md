# Plugins (/plugins)

A plugin is a **package / distribution unit** — a container that bundles together commands, agents, hooks, MCP servers, skills, and output styles for distribution.

## Hierarchy

```
plugin              ← package / distribution unit
  ├── commands      ← /foo invocations
  ├── agents        ← subagents you can spawn
  ├── hooks         ← lifecycle middleware
  ├── mcp servers   ← external tool integrations
  ├── skills        ← user-invocable capabilities
  └── output styles
```

A plugin is a container. Agents are one of the things that can live inside it (alongside commands, hooks, MCP servers, etc.). Plugin is the broader concept; agent is one specific kind of component.

## Plugin vs. Agent — two orthogonal axes

They're different *kinds* of concepts, not just different sizes:

|                  | Plugin                                    | Agent / subagent                          |
| ---------------- | ----------------------------------------- | ----------------------------------------- |
| What kind of thing | A bundle / package                      | A runtime entity (a callable)             |
| Lives where      | Filesystem (`.claude/plugins/...`)        | Spawned in memory during a session        |
| Lifetime         | Installed once, persists across sessions  | Created on demand, returns one message, exits |
| Analogy          | npm package                               | A running function                        |

A plugin is **static** — files on disk. An agent is **dynamic** — a thing the model invokes mid-conversation. They're not even the same category of object.

## You can mix freely

The two axes are independent — every combination is valid:

- **Plugin without agents** — just slash commands and hooks. Plenty of plugins ship zero agents.
- **Agents without a plugin** — drop a markdown file into `~/.claude/agents/` directly; it works without ever being part of a plugin.
- **Plugin with agents** — most "domain expertise" plugins (security, data eng, frontend) bundle 1–3 specialized agents.
- **Plugin with only agents** — e.g., a "team of code reviewers" plugin that ships nothing but a roster of subagent definitions.

## A useful analogy

Think of Claude Code's components as the things in a programming language, and a plugin as a package on a registry:

- **Commands** are like CLI entry points.
- **Hooks** are like middleware.
- **MCP servers** are like service clients.
- **Agents** are like specialized worker functions you can call.
- **Skills** are like documented procedures.
- **A plugin** is like an npm package that bundles any combination of those for distribution.

You can write a worker function without publishing a package. You can publish a package that contains no worker functions. The two concepts solve different problems — **plugins solve distribution, agents solve delegation**.

---

## How to create Claude plugins

https://code.claude.com/docs/en/plugins

The plugin metadata directory is `.claude-plugin`.

## How to install Claude plugins

For example, the official Anthropic marketplace:

https://code.claude.com/docs/en/discover-plugins

```bash
/plugin marketplace add anthropics/claude-code
```

Install plugins (for example):

```bash
/plugin install commit-commands@anthropics-claude-code
```

--

## Claude Code Official Plugins

#### Summary

| Plugin | Key Command | What It Does |
|---|---|---|
| **Agent SDK Dev** | `/new-sdk-app [name]` | Scaffolds new Claude Agent SDK projects in Python/TypeScript with proper setup, SDK installation, and verification |
| **Claude Opus 4.5 Migration** | `claude-opus-4-5-migration` skill | Migrates existing code from Sonnet 4.x / Opus 4.1 to newer Opus 4.5 patterns and prompts |
| **Code Review** | `/code-review` | Runs 5 parallel Sonnet agents for confidence-scored PR reviews — bug detection, guideline compliance, git blame context. Use `--comment` to post as PR comment |
| **Commit Commands** | `/commit`, `/commit-push-pr`, `/clean_gone` | Automates git workflow: AI-generated commit messages matching repo style, branch creation, PR descriptions. Avoids committing secrets |
| **Explanatory Output Style** | SessionStart hook (auto) | Adds educational context about implementation choices — runs automatically when Claude Code starts |
| **Feature Dev** | `/feature-dev [description]` | Structured 7-phase feature development: discovery, codebase exploration, clarifying questions, architecture design, implementation, quality review, summary |
| **Frontend Design** | Auto-invoked skill | Creates distinctive, production-grade frontend interfaces with bold aesthetics, typography, animations. Just describe what you want naturally |
| **Hookify** | `/hookify`, `/hookify:list`, `/hookify:configure` | Creates custom hooks to block or warn on unwanted behaviors (e.g., dangerous `rm -rf`, hardcoded credentials) using simple markdown + regex |
| **Learning Output Style** | SessionStart hook (auto) | Interactive learning mode — asks you meaningful questions instead of giving complete solutions |
| **Plugin Dev** | `/plugin-dev:create-plugin [description]` | Toolkit for building Claude Code plugins — 8-phase workflow with 7 core skills (hooks, MCP, commands, agents, etc.) and 12+ working examples |
| **PR Review Toolkit** | Skill-based (auto) | 6 specialized review agents: comment-analyzer, test-analyzer, silent-failure-hunter, type-design-analyzer, code-reviewer, code-simplifier |
| **Ralph Wiggum** | `/ralph-loop`, `/cancel-ralph` | Iterative self-referential development loops — Claude keeps iterating on solutions autonomously until stopped |
| **Security Guidance** | PreToolUse hook (auto) | Passive security monitoring — detects 9 patterns including hardcoded secrets, dangerous commands, unsafe file operations |


#### By Use Case

| Use Case | Plugin(s) |
|---|---|
| Start a new Agent SDK project | Agent SDK Dev |
| Commit and push code | Commit Commands |
| Review a PR before merge | Code Review or PR Review Toolkit |
| Build a new multi-file feature | Feature Dev |
| Create frontend UI | Frontend Design |
| Prevent bad behaviors / enforce rules | Hookify, Security Guidance |
| Build a custom Claude Code plugin | Plugin Dev |
| Learning-focused sessions | Learning Output Style, Explanatory Output Style |
| Iterative autonomous development | Ralph Wiggum |
| Migrate to newer Claude models | Claude Opus 4.5 Migration |

--

## Plugin library

* [plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
* [plugin marketplace](https://claudemarketplaces.com/)
