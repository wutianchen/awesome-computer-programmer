# Context Management - Compaction

Compaction automatically summarizes older conversation context when approaching the context window limit,    
replacing stale messages with concise summaries. This keeps the active context focused — long contexts       
degrade model performance even before hitting the token cap.  


## How it triggers (in Claude Code CLI)

1. The system monitors input token count each turn                                                           
2. When tokens exceed a threshold (default: 150,000 tokens, minimum: 50,000), compaction kicks in
3. Claude generates a <summary> of the conversation so far                                                   
4. A compaction content block is inserted into the assistant's response                                      
5. On the next turn, all messages before the compaction block are dropped — the summary replaces them

## How to use compaction

You don't need to do anything — Claude Code handles compaction automatically. But you can influence it:

1. /compact — manually trigger compaction at any time (useful to free up context before a complex task)
2. /compact <instructions> — compact with custom instructions, e.g. /compact preserve all file paths and function signatures
3. CLAUDE.md files — content in CLAUDE.md is treated as the system prompt and survives compaction (it's re-injected each time). Put critical context here.


## Source of Information

* https://platform.claude.com/docs/en/build-with-claude/compaction
* https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents