# OMX

[Website](https://yeachan-heo.github.io/oh-my-codex-website/docs.html)

others:

* https://github.com/Yeachan-Heo/oh-my-codex
* https://dev.to/benriemer/how-to-supercharge-your-ai-coding-workflow-with-oh-my-codex-1n5f
* https://github.com/scalarian/oh-my-codex

## setup omx

```bash
omx setup
```

Other commands to explore:

* omx explore
* omx sparkshellcodex


## Folder Structure

All artifacts live under the `.omx/` directory at the project root.

| Directory | Purpose | Example Files |
|---|---|---|
| `.omx/specs/` | Execution-ready specs from deep-interview, autoresearch mission bundles | `deep-interview-{slug}.md`, `autoresearch-{slug}/mission.md`, `autoresearch-{slug}/sandbox.md`, `autoresearch-{slug}/result.json` |
| `.omx/interviews/` | Interview transcript summaries (kept for ralph PRD compatibility) | `{slug}-{timestamp}.md` |
| `.omx/context/` | Preflight context snapshots reused across skills (deep-interview, ralplan) | `{slug}-{YYYYMMDDTHHMMSSZ}.md` |
| `.omx/plans/` | Planning artifacts produced by ralplan/plan consensus workflow | `prd-{slug}.md`, `test-spec-{slug}.md` |
| `.omx/logs/` | Runtime logs — turn JSONL, tmux hook logs, autoresearch run ledgers | `hooks-YYYY-MM-DD.jsonl`, `tmux-hook-YYYY-MM-DD.jsonl`, `autoresearch/{run-id}/manifest.json` |
| `.omx/state/` | Resumable mode state for skills (deep-interview, ralph, etc.) | JSON state files per active mode |
| `.omx/autoresearch/` | Session-level autoresearch instructions | `deep-interview-session-instructions.md` |
| `.omx/project-memory.json` | Project-level memory store | single JSON file |
| `.omx/notepad.md` | Scratchpad notepad | single markdown file |

Source references (from [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) repo):

| Directory | Source |
|---|---|
| `specs/` | `src/planning/artifacts.ts` (line 49: `specsDir = join(cwd, '.omx', 'specs')`), `skills/deep-interview/SKILL.md` (Phase 4 crystallize artifacts) |
| `interviews/` | `skills/deep-interview/SKILL.md` (Phase 4: `.omx/interviews/{slug}-{timestamp}.md`) |
| `context/` | `skills/deep-interview/SKILL.md` (Phase 0 preflight: `.omx/context/{slug}-{timestamp}.md`), `skills/ralplan/SKILL.md` (pre-context intake) |
| `plans/` | `src/utils/paths.ts` (line 196-197: `omxPlansDir`), `src/planning/artifacts.ts` (line 48, 54-55: PRD and test-spec patterns) |
| `logs/` | `src/utils/paths.ts` (line 200-201: `omxLogsDir`), `src/cli/autoresearch.ts` (line 54: autoresearch ledger under `.omx/logs/autoresearch/`) |
| `state/` | `src/utils/paths.ts` (line 181-182: `omxStateDir`) |
| `autoresearch/` | `src/cli/autoresearch.ts` (line 78-79: `join(repoRoot, '.omx', 'autoresearch')`) |
| `project-memory.json` | `src/utils/paths.ts` (line 185-186: `omxProjectMemoryPath`) |
| `notepad.md` | `src/utils/paths.ts` (line 190-191: `omxNotepadPath`) |


## role or workflow keywords

* $architect
* $executor
* $plan


## Skills

* deep-interview
* plan (ralplan)
* autopilot

basic workflow

```bash
deep-interview -> ralplan -> autopilot
```