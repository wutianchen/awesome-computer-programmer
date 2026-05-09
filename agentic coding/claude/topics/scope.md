# Scope

## Type of Scopes

* project-level
* user level
* local



## About mcp


About mcp setting

By default, claude mcp add writes to ~/.claude.json (in your home directory).

  The exact file depends on the --scope flag:
  ┌─────────────────┬─────────────────┬──────────────────────────┬───────────────────┐
  │      Scope      │      Flag       │           File           │      Shared?      │
  ├─────────────────┼─────────────────┼──────────────────────────┼───────────────────┤
  │ Local (default) │ --scope local   │ ~/.claude.json           │ No                │
  ├─────────────────┼─────────────────┼──────────────────────────┼───────────────────┤
  │ User            │ --scope user    │ ~/.claude.json           │ No                │
  ├─────────────────┼─────────────────┼──────────────────────────┼───────────────────┤
  │ Project         │ --scope project │ .mcp.json (project root) │ Yes (committable) │
  └─────────────────┴─────────────────┴──────────────────────────┴───────────────────┘
  So if you run:
  claude mcp add myserver ...
  It goes into ~/.claude.json by default.

  To make it shared with your team (checked into git), use:
  claude mcp add myserver --scope project ...
  which writes to .mcp.json in your project root.

Claude loads mcp server along the configuration hierarchy local -> user -> project and combine them (instead of overriding)

## Source of Information
Link: https://code.claude.com/docs/en/settings