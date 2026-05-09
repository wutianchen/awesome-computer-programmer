# CLAUDE.md

CLAUDE.md is: A markdown file that gives Claude Code persistent instructions across sessions. Claude reads it at the start of `every conversation`.

## Where to Place It

| Scope | Location |
|---|---|
| Project (shared with team) | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| User (personal, all projects) | `~/.claude/CLAUDE.md` |

`CLAUDE.local.md`

## What to Include

Keep it **concise (under 200 lines)** and specific:

```markdown
# Project Name

## Build & Test
- `go build ./...` to build
- `go test ./...` to run tests

## Code Style
- Use 2-space indentation
- Prefer short variable names in Go
- Error messages start lowercase

## Project Structure
- API handlers in `src/api/`
- Database models in `src/models/`

## Workflow
- Run tests before committing
- Never push directly to main without review
```

## Quick Start

Run `/init` inside Claude Code — it analyzes your codebase and generates a starting CLAUDE.md automatically.

## Advanced

You can reference other files with `@path` syntax:

```markdown
See @README for project overview
```

You can also split rules into `.claude/rules/` for larger projects:

```
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md
    └── testing.md
```

## Compared to memory.md