# $deep-interview

Socratic deep interview with mathematical ambiguity gating before execution. Turns vague ideas into execution-ready specifications by asking targeted questions about why, how far, what's out of scope, and what OMX may decide without confirmation.

Source: `skills/deep-interview/SKILL.md` in [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)

## Usage

```
$deep-interview [--quick|--standard|--deep] [--autoresearch] <idea or vague description>
```

## Depth Profiles

| Profile | Flag | Ambiguity Threshold | Max Rounds |
|---|---|---|---|
| Quick | `--quick` | <= 0.30 | 5 |
| Standard (default) | `--standard` | <= 0.20 | 12 |
| Deep | `--deep` | <= 0.15 | 20 |
| Autoresearch | `--autoresearch` | same as Standard | same as Standard |

## Phases (0-5)

There are 6 phases total.

### Phase 0: Preflight Context Intake

Loads or creates a context snapshot under `.omx/context/{slug}-{YYYYMMDDTHHMMSSZ}.md` containing:

- Task statement
- Desired outcome
- Stated solution (what the user asked for)
- Probable intent hypothesis (why they likely want it)
- Known facts/evidence
- Constraints
- Unknowns/open questions
- Decision-boundary unknowns
- Likely codebase touchpoints

### Phase 1: Initialize

- Parses depth profile (`--quick/--standard/--deep`)
- Detects **brownfield** (existing codebase) vs **greenfield** via `explore`
- Initializes mode state with ambiguity score starting at 1.0
- Announces kickoff with profile, threshold, and current ambiguity

### Phase 2: Socratic Interview Loop

The main interview loop. Repeats until ambiguity <= threshold, max rounds hit, or user exits.

Each round:
1. **Generate next question** — targets the lowest-scoring clarity dimension, respecting stage priority:
   - Stage 1 (Intent-first): Intent, Outcome, Scope, Non-goals, Decision Boundaries
   - Stage 2 (Feasibility): Constraints, Success Criteria
   - Stage 3 (Brownfield grounding): Context Clarity (brownfield only)
2. **Ask the question** — one question per round, never batched
3. **Score ambiguity** — weighted dimensions scored in [0.0, 1.0]:
   - Greenfield: `ambiguity = 1 - (intent x 0.30 + outcome x 0.25 + scope x 0.20 + constraints x 0.15 + success x 0.10)`
   - Brownfield: `ambiguity = 1 - (intent x 0.25 + outcome x 0.20 + scope x 0.20 + constraints x 0.15 + success x 0.10 + context x 0.10)`
4. **Report progress** — shows weighted breakdown table and readiness-gate status
5. **Persist state** — appends round result via `state_write`

Readiness gates (must be explicit before crystallizing):
- Non-goals
- Decision Boundaries
- At least one pressure pass revisiting an earlier answer

### Phase 3: Challenge Modes

Assumption stress tests, each used once when applicable:

| Mode | Trigger | Purpose |
|---|---|---|
| Contrarian | Round 2+ or untested assumption | Challenge core assumptions |
| Simplifier | Round 4+ or scope expanding faster than outcome clarity | Probe minimal viable scope |
| Ontologist | Round 5+ and ambiguity > 0.25, or user describes symptoms | Ask for essence-level reframing |

### Phase 4: Crystallize Artifacts

When threshold is met (or user exits / hard cap):

- Writes interview transcript summary to `.omx/interviews/{slug}-{timestamp}.md`
- Writes execution-ready spec to `.omx/specs/deep-interview-{slug}.md`

The spec includes: metadata, clarity breakdown, intent, desired outcome, in-scope, out-of-scope/non-goals, decision boundaries, constraints, testable acceptance criteria, assumptions exposed + resolutions, pressure-pass findings, and transcript.

### Phase 5: Execution Bridge

Presents handoff options after artifact generation. Deep-interview is a requirements mode — no direct implementation happens here.

| Option | Invocation | Best When |
|---|---|---|
| `$ralplan` (recommended) | `$plan --consensus --direct <spec-path>` | Requirements clear, but architectural validation still desirable |
| `$autopilot` | `$autopilot <spec-path>` | Spec strong enough for direct planning + execution |
| `$ralph` | `$ralph <spec-path>` | Task benefits from persistent sequential completion pressure |
| `$team` | `$team <spec-path>` | Large, multi-lane, or blocker-sensitive parallel execution |
| Refine further | Continue the interview loop | Residual ambiguity too high |

## Recommended Pipeline

```
deep-interview -> ralplan -> autopilot
```

- Stage 1 (deep-interview): clarity gate
- Stage 2 (ralplan): feasibility + architecture gate
- Stage 3 (autopilot): execution + QA + validation gate