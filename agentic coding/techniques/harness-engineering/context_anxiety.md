# Context Anxiety

## What It Is

Context anxiety is a behavioral pattern where an LLM agent begins **prematurely concluding its work** as it approaches its perceived context limit, rather than completing tasks thoroughly. The agent starts wrapping up, summarizing, or cutting corners — not because the task is done, but because it "feels" the context window filling up.

## How It Manifests

- Agent starts wrapping up work before reaching actual context limits
- Cuts short productive development cycles
- Produces rushed, incomplete outputs in later turns
- Begins summarizing instead of continuing to execute
- Declares tasks "done" prematurely

## Why It Happens

The model is aware (from training) that context windows are finite. As conversations grow long, the model begins to behave as if it's running out of space — even when it isn't at the hard limit yet. It's a learned behavior, not a hard constraint.

## Solutions

### Context Resets (Preferred)

Clear the context window entirely and start a fresh agent with a structured handoff. The new agent picks up from a clean slate using a handoff artifact (summary of state, remaining tasks, relevant file paths).

```
Agent 1 (context filling up)
  → produces handoff artifact (state summary + remaining work)
  → terminates

Agent 2 (fresh context)
  → reads handoff artifact
  → continues work with full context budget
```

Cost: the handoff artifact must contain enough state for the next agent to pick up cleanly.
Benefit: eliminates context anxiety entirely — the new agent doesn't "feel" any pressure.

### Compaction (Alternative)

Summarize earlier conversation parts in place — compress old turns into a shorter representation while keeping the conversation going. Preserves continuity but **doesn't eliminate context anxiety** since the agent retains awareness that the conversation has been long/compressed.

### Model Capability

Context anxiety varies by model. It was notably strong in earlier models (e.g., Claude Sonnet 4.5) but largely resolved in newer ones (e.g., Claude Opus 4.5/4.6) with better long-context retrieval capabilities.

## Relationship to Harness Engineering

Context anxiety is a problem the **harness** solves, not the prompt. You can't reliably prompt away the behavior — instead you architect the harness to:
- Monitor context usage
- Trigger resets at appropriate thresholds
- Automate handoff artifact generation
- Spawn fresh agents to continue work

This is why harness engineering matters for long-running tasks — the harness manages the model's lifecycle so the model can focus on the work.

## Reference

* [Harness design for long-running apps — Anthropic Engineering](https://www.anthropic.com/engineering/harness-design-long-running-apps)
