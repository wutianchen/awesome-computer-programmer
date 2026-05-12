# Harness Engineering vs Context Engineering

## Context Engineering

The practice of crafting and managing **what information the model sees** — system prompts, examples, retrieved documents, conversation history, tool descriptions. It operates at the **input level**.

```
Context Engineering controls:
  ┌─────────────────────────────────┐
  │  System prompt                  │
  │  Few-shot examples              │
  │  RAG-retrieved documents        │
  │  Conversation history/memory    │
  │  Tool descriptions              │
  └─────────────────────────────────┘
          │
          ▼
      ┌────────┐
      │  LLM   │
      └────────┘
```

Goal: give the model the right information at the right time so it produces the right output.

Techniques:
- Prompt engineering (system prompts, instruction tuning)
- Retrieval-Augmented Generation (RAG)
- Dynamic context selection (what to include, what to omit)
- Conversation/memory management (what to remember across turns)
- Few-shot example curation

## Harness Engineering

The practice of engineering the **entire execution environment** around the model — tools, permissions, hooks, agents, skills, workflows. It operates at the **system level**.

```
Harness Engineering controls:
  ┌───────────────────────────────────────────────┐
  │  Tools (what the model can DO)                │
  │  Permissions (what the model is ALLOWED to do)│
  │  Hooks (automated reactions to events)        │
  │  Skills (reusable workflows)                  │
  │  Agent orchestration (sub-agents, delegation) │
  │  Settings (model, mode, environment)          │
  │  CLAUDE.md / project instructions             │
  │  Memory system                                │
  └───────────────────────────────────────────────┘
          │
          ▼
      ┌────────┐
      │  LLM   │ ──► tool calls ──► external systems
      └────────┘
```

Goal: give the model the right capabilities, constraints, and automation so it executes tasks correctly and safely.

Techniques:
- Tool design (what APIs/commands are exposed)
- Permission configuration (allow/deny rules, approval workflows)
- Hook scripting (pre/post actions on tool calls)
- Skill/slash-command definitions (reusable task templates)
- Agent orchestration (sub-agents, parallelism, isolation)
- Project conventions (CLAUDE.md, settings.json)

## The Difference

| | Context Engineering | Harness Engineering |
|---|---|---|
| Focus | What the model **reads** | What the model **can do** and how it's controlled |
| Operates on | The context window (input) | The execution environment (system) |
| Controls | Information | Capabilities + constraints + automation |
| Analogy | Giving an employee the right briefing document | Giving an employee the right tools, permissions, and SOPs |
| Output | Better reasoning and responses | Correct, safe, automated execution |

## Relationship

Context engineering is a **component** of harness engineering, not a separate concern. The harness determines what context gets loaded:

```
Harness layer:
  CLAUDE.md → automatically loaded into context
  Memory system → recalled and injected into context
  Skill prompt → expanded and injected into context
  Tool descriptions → always present in context

These are harness decisions that manifest as context.
```

But harness engineering goes beyond context — it also governs:
- **Execution**: what happens when the model calls a tool (sandbox, permissions, hooks)
- **Safety**: what the model is prevented from doing regardless of what it "wants"
- **Workflow**: automated sequences triggered by events, not by the model's reasoning
- **Orchestration**: spawning sub-agents, parallel work, isolated worktrees


## Summary

**Context engineering** = the art of what the model knows.
**Harness engineering** = the art of what the model can do, and how safely/automatically it does it.

A great context with a bad harness produces smart suggestions that execute dangerously. A great harness with bad context produces safe execution of the wrong thing. You need both.
