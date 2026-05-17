# Model


## Modes

```
┌──────────────────┬────────────────────┬──────────────────┬─────────────────────────────────────────────────────────┐
│       Mode       │      Category      │      Toggle      │                       Description                       │
├──────────────────┼────────────────────┼──────────────────┼─────────────────────────────────────────────────────────┤
│ Normal Mode      │ Permission mode    │ Shift+Tab cycle  │ Default — asks for approval before each edit            │
├──────────────────┼────────────────────┼──────────────────┼─────────────────────────────────────────────────────────┤
│ Plan Mode        │ Permission mode    │ Shift+Tab cycle  │ Read-only analysis; creates a plan before changes       │
├──────────────────┼────────────────────┼──────────────────┼─────────────────────────────────────────────────────────┤
│ Auto-Accept Mode │ Permission mode    │ Shift+Tab cycle  │ Automatically approves edits without asking             │
├──────────────────┼────────────────────┼──────────────────┼─────────────────────────────────────────────────────────┤
│ Fast Mode        │ Independent toggle │ /fast            │ 2.5x faster responses, same Opus 4.6 model              │
├──────────────────┼────────────────────┼──────────────────┼─────────────────────────────────────────────────────────┤
│ Memory Mode      │ Independent toggle │ /memory          │ Persistent file-based memory (on by default)            │
├──────────────────┼────────────────────┼──────────────────┼─────────────────────────────────────────────────────────┤
│ Extended         │ Independent toggle │ Option+T / Alt+T │ Deep reasoning; /effort low|medium|high|max             │
│ Thinking         │                    │                  │                                                         │
└──────────────────┴────────────────────┴──────────────────┴─────────────────────────────────────────────────────────┘
```

The first three (Plan, Auto-Accept, Normal) are permission modes you cycle through with Shift+Tab. Fast mode, memory, and thinking mode are independent toggles you can combine with any permission mode.

## Reference

* [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)