# memory management

context management


## Memory Command

```bash
/memory
```


## Memory Types

### overview

| Type | About | Stored in | Changes |
|------|-------|-----------|---------|
| **user** | The person — role, expertise, preferences | `~/.claude/projects/<path>/memory/` | Slowly |
| **project** | The work — goals, decisions, deadlines | `<project-root>/.claude/settings.json`, `CLAUDE.md` | Quickly |
| **feedback** | How to approach work — avoid/repeat | `~/.claude/projects/<path>/memory/` | Moderately |
| **reference** | Pointers to external systems | `~/.claude/projects/<path>/memory/` | Rarely |

### user memory

Stores information about the user — role, expertise, preferences, and how they like to work. Helps tailor responses to the user's specific context. Changes slowly over time.

- stored in: `~/.claude/projects/<project-path>/memory/`
- example: "user is a data scientist, new to React" — Claude would explain frontend concepts differently than for a React expert

### project memory

Stores information about the work being done — goals, decisions, deadlines, incidents, and context not obvious from code or git history. Helps Claude understand the *why* behind tasks. Changes quickly as priorities shift.

- stored in: `<project-root>/.claude/settings.json` and project-level `CLAUDE.md` files
- example: "auth rewrite is driven by legal compliance, not tech debt" — Claude would prioritize compliance over ergonomics

### other memory types

- **feedback memory**: guidance on how to approach work (what to avoid, what to keep doing)
- **reference memory**: pointers to external systems (Linear projects, Grafana dashboards, Slack channels)

All memory files live under `~/.claude/projects/<project-path>/memory/` with an index in `MEMORY.md`.

> **Note:** currently all memory types are project based.


## Features

### auto-memory

Claude automatically saves notes about you and your project as you work — without you explicitly asking. As it learns things during conversations (your role, preferences, project context, feedback), it writes markdown files on its own.

- enabled by default since Claude Code v2.1.59+
- can be toggled on/off via `/memory`
- saves all 4 memory types (user, project, feedback, reference) automatically
- memories persist across conversations so future sessions have context
- stored in: `~/.claude/projects/<project-path>/memory/`
  - `<project-path>` is your project's full path with `/` replaced by `-`
  - e.g. `~/.claude/projects/-Users-tianchenwu-Projects-personal-data-cloud-engineering-toolkit/memory/`

### Conversation Logs vs Memory

**Conversation logs** (`.jsonl` files) — the raw transcript of every conversation in the project. Used for resuming sessions (`--continue`, `--resume`). Claude does NOT read past conversation logs when starting a new conversation.

**Memory** (`memory/` folder) — curated notes read **at the start of every new conversation** in that project. The only thing that persists across conversations.

```
Conversation 1: you tell Claude your preferences → saved to memory
Conversation 1 ends

Conversation 2 starts:
  ├── reads memory/ folder ✓ (knows your preferences)
  └── does NOT read conversation 1 logs ✗ (no access to prior chats)
```

| | Conversation Logs | Memory |
|---|---|---|
| What it is | Full transcript (every message, tool call, result) | Short curated notes |
| Persists across conversations | No — only accessible via `--continue`/`--resume` | Yes — loaded into every new conversation |
| Size | Large (entire chat history) | Small (concise entries, <200 lines index) |
| Who writes it | System (automatic) | Claude (when something worth remembering comes up) |
| Purpose | Resume a specific session | Carry knowledge forward to all future sessions |

> The memory folder only gets created when Claude writes a memory for the first time in a project. If no memories have been saved yet, the folder won't exist even though conversation logs are present.

### auto-dream

memory consolidation

```bash
/dream
```

## Reference

* [How Claude remembers your project](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)