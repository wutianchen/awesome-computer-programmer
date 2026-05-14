# Configuration

```bash
/config
```

it controls

* extended thinking
* auto-compact

# Effort

* adjust the effort level by

```bash
effort
```

* ultrathink — include this word in your prompt for maximum reasoning on a single turn

What it does:
- Sets effort to high for that one turn only — doesn't change your default setting
- Claude gets significantly more internal reasoning space to work through the problem
- Better at catching edge cases, self-correcting, and handling multi-step logic

# `settings.json`

`settings.json` is Claude Code's configuration file — a plain JSON file where you tell Claude Code how to behave: which tools are auto-approved, which model to use, what hooks to fire, where to find MCP servers, environment variables, and so on.

## Where it lives — three layers, in precedence order

Claude Code merges settings from up to four locations, with later layers overriding earlier ones:

| Path | Scope | Checked into git? |
|---|---|---|
| `~/.claude/settings.json` | User-global (all projects) | No |
| `<project>/.claude/settings.json` | Project, shared with team | **Yes** (commit it) |
| `<project>/.claude/settings.local.json` | Project, your machine only | No (auto-`.gitignore`d) |
| Enterprise-managed policy file | Org-wide overrides | Set by IT |

Project settings let your team standardize hooks and permissions; `settings.local.json` is for personal overrides you don't want to commit.

## What's in it

A typical project `settings.json` has a few of these top-level keys:

```json
{
  "model": "claude-opus-4-7",
  "permissions": {
    "allow": ["Bash(git status)", "Bash(npm test)", "Read", "Edit"],
    "deny": ["Bash(rm -rf *)"],
    "ask": ["Bash(git push:*)"]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "./scripts/audit.sh" }]
      }
    ]
  },
  "env": {
    "DATABASE_URL": "postgres://localhost/dev"
  },
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgres://..."]
    }
  }
}
```

## The common keys

### `permissions`

Controls which tool calls auto-approve, prompt, or get blocked. Three lists:

- `allow` — auto-approved (no prompt).
- `deny` — always blocked.
- `ask` — always prompts even if otherwise allow-listed.

The matcher syntax is `<Tool>(<pattern>)`:

- `"Bash(npm test)"` — exact match.
- `"Bash(git status:*)"` — prefix match (anything starting with `git status`).
- `"Edit(src/**)"` — glob match on file paths.
- `"Read"` — every call to that tool, no pattern.

This is where you tune the "should Claude ask before running X?" friction.

### `hooks`

Event-driven shell commands. Lifecycle events: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `Notification`, `SessionStart`, `SessionEnd`. Each entry has a `matcher` (which tool/event it fires on) and a list of commands. Useful for audit logging, auto-formatting, blocking dangerous paths, or piping context into prompts.

### `model`

The model ID to use, e.g. `"claude-opus-4-7"`, `"claude-sonnet-4-6"`. Override per project if some repos benefit from a faster/cheaper model.

### `env`

Environment variables injected into Claude Code's tool-execution shell. Handy for setting `DATABASE_URL` per project so Bash calls pick it up.

### `mcpServers`

External MCP (Model Context Protocol) servers to connect to. Each entry defines a server name → how to launch it (`command`, `args`, `env`). Once connected, the server's tools appear as `mcp__<server>__<tool>` and Claude can call them like any other tool.

### `enableAllProjectMcpServers` / `enabledMcpjsonServers`

Whether to trust MCP servers defined in `.mcp.json` files in the project. By default Claude Code asks before enabling them; you can pre-approve specific ones here.

### `apiKeyHelper`

A shell command that prints an API key to stdout. Useful when your key rotates (e.g., AWS STS, short-lived tokens) — Claude Code calls the helper instead of reading a static key.

### `outputStyle`

Pre-tuned response styles (e.g., `"default"`, `"explanatory"`, `"learning"`). Affects verbosity and format of Claude's text output.

### `statusLine`

Custom status-line command. Output appears at the bottom of the Claude Code UI. Use the `/statusline` slash command to set this up interactively.

### `includeCoAuthoredBy`

Boolean — whether to add `Co-Authored-By: Claude` to commits Claude makes. Defaults to true.

## How to view / edit it

- `/config` — opens an interactive settings editor.
- `claude config get <key>` / `claude config set <key> <value>` — CLI commands for scripted changes.
- Or just open the file directly. It's plain JSON.

## Things to know

1. **Validation is permissive.** Unknown keys are ignored, not errored. So a typo in `mcpServerss` will silently do nothing. `claude --debug` and `/doctor` help spot misconfigurations.

2. **`settings.local.json` is the right place for secrets.** It's not checked in. `settings.json` is for team-shared policy.

3. **Hooks run as your shell user.** Same blast radius as anything else you'd run. Treat hooks from a freshly cloned repo's `.claude/settings.json` with the same caution as a `Makefile` from that repo.

4. **`CLAUDE.md` is *not* settings.** `CLAUDE.md` is project context (what Claude reads to understand your codebase). `settings.json` is configuration (how Claude Code behaves). Different files, different purposes.

5. **Precedence is shallow merge per top-level key.** `permissions.allow` from `settings.local.json` *replaces* `permissions.allow` from `settings.json`, not merges into it. Same for `hooks`. Keep this in mind when overriding.

## Minimal useful starter

For a project where you want Claude Code to be productive without endless permission prompts, but still safe:

```json
{
  "permissions": {
    "allow": [
      "Read", "Edit", "Write", "Grep", "Glob",
      "Bash(git status)", "Bash(git diff:*)", "Bash(git log:*)",
      "Bash(npm test)", "Bash(npm run build)"
    ],
    "ask": ["Bash(git push:*)", "Bash(rm:*)"],
    "deny": ["Bash(rm -rf /*)"]
  }
}
```

This gives Claude full read/edit access plus common dev commands automatically, prompts on anything destructive or remote-affecting, and hard-blocks the obvious footgun.

# `.claude.json` vs `settings.json`

Different beasts entirely — one is **configuration** you write, the other is **state** Claude Code maintains.

## `settings.json` — declarative configuration

- **You** write it.
- Contains *policy*: which tools are allowed, what model to use, hooks, env vars, MCP server declarations.
- Lives in multiple places (`~/.claude/settings.json`, `<project>/.claude/settings.json`, `<project>/.claude/settings.local.json`) with precedence/merge rules.
- Designed to be readable and diff-able. Project-level `settings.json` is meant to be checked into git.
- Static — Claude Code reads it but doesn't write back to it.

## `~/.claude.json` — auto-managed state

- **Claude Code** writes and maintains it.
- Single file, only at `~/.claude.json` (no project-level equivalent).
- Contains *state*: who you are, what you've used, per-project history, OAuth credentials, onboarding flags, MCP server runtime info.
- Mutated constantly as you use Claude Code.
- Not meant to be hand-edited (though you can in a pinch).
- Definitely not checked into git — it has credentials.

## What's actually inside `.claude.json`

A rough map of the top-level keys:

| Key | Purpose |
|---|---|
| `userId` | Internal user identifier |
| `numStartups` | Counter — how many times you've launched Claude Code |
| `installMethod` | How Claude Code got installed (npm, brew, etc.) |
| `autoUpdates` | Auto-update toggle |
| `firstStartTime`, `lastOnboardingVersion` | Onboarding state |
| `oauthAccount` | OAuth tokens / account info if you logged in via Anthropic account |
| `tipsHistory` | Which in-app tips have been shown |
| `feedbackSurveyState` | Whether/when survey was shown |
| `cachedChangelog`, `changelogLastFetched` | Cached release notes |
| `mcpServers` | Globally configured MCP servers |
| **`projects`** | **Map of per-project state, keyed by absolute path** |

The `projects` map is the bulk of the file. Each entry looks something like:

```json
"/Users/me/Projects/myrepo": {
  "allowedTools": ["Read", "Edit", "Bash(npm test)"],
  "history": [
    { "display": "fix the auth bug", "pastedContents": {} },
    { "display": "add a test for X", "pastedContents": {} }
  ],
  "mcpServers": { "postgres": { } },
  "enabledMcpjsonServers": ["filesystem"],
  "disabledMcpjsonServers": [],
  "hasTrustDialogAccepted": true,
  "projectOnboardingSeenCount": 3,
  "hasClaudeMdExternalIncludesApproved": false,
  "exampleFiles": [],
  "lastTotalWebSearchRequests": 12
}
```

This is how your prompt history persists, why Claude Code remembers which projects you've already approved, and how per-project MCP server choices stick.

## Side-by-side

| | `settings.json` | `~/.claude.json` |
|---|---|---|
| Purpose | Configuration / policy | Runtime state |
| Author | You | Claude Code itself |
| Locations | User + project + local + enterprise | One file in `$HOME` only |
| Project-aware | Via separate per-project files | Via `projects` map keyed by path |
| Hand-editable | Yes, primary use case | Possible but discouraged |
| Check into git | Project file: yes | **Never** — has credentials |
| Stable across sessions | Yes — only changes when you edit | No — mutates constantly |
| Contains secrets | Shouldn't (use Secret managers / `settings.local.json`) | Yes (OAuth tokens) |
| Format guarantees | Public, documented | Internal, may change between versions |

## A confusing overlap — MCP servers

Both files can contain `mcpServers`, which is the source of "which one wins?" confusion. The rule:

- `settings.json` `mcpServers` — declarative, project- or user-scoped, intended to be the *source of truth* for what should be available.
- `.claude.json` `mcpServers` — runtime mirror, plus `enabledMcpjsonServers` / `disabledMcpjsonServers` lists tracking which `.mcp.json` servers you've trust-approved.

When you run `claude mcp add ...`, it writes into `.claude.json`. When you write to `settings.json`'s `mcpServers` directly, it's read by Claude Code on startup. Recent versions have been pushing toward `settings.json` as the authoritative location, with `.claude.json` holding the trust state. If they disagree, prefer `settings.json` and check `claude mcp list` to see what's actually loaded.

## Practical guidance

- Want to **change behavior** (which tools auto-approve, which model, which hooks)? Edit `settings.json`.
- Want to **clear chat history for a project**? Edit `.claude.json` and remove that project's `history` array.
- Want to **revoke trust for a project** so the dialog re-appears? Set `hasTrustDialogAccepted: false` on that project's entry in `.claude.json`.
- **Never commit `.claude.json`** to a repo. Most installs put it outside the project, but if you have it as `<project>/.claude.json` make sure it's gitignored.
- If `.claude.json` gets corrupted (it can happen — it's frequently rewritten), Claude Code may fail to start. Backing it up before manual edits is wise; Claude Code will recreate it on next launch if you delete it, but you'll lose history and approvals.

## TL;DR

**`settings.json` is what you tell Claude Code to do. `.claude.json` is what Claude Code remembers about your usage.** Configuration vs. state. Edit the first; let Claude Code manage the second.
