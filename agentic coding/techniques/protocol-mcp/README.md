# MCP

## MCP Marketplace

* https://mcp.so/
* https://glama.ai/mcp
* https://smithery.ai/
* https://mcpmarket.com/


## MCP Tools

* [mcp-memory-libsql](https://github.com/joleyline/mcp-memory-libsql)
* [brave-search-mcp](https://github.com/mikechao/brave-search-mcp)
* [mcp polygon](https://github.com/polygon-io/mcp_polygon)

## What is MCP

There are three components under MCP

* client
* server
* host

and

* server normally runs locally with client and host, there are also `remote server` or `managed server`
* for each mcp server, there is one mcp client

There are two ways for mcp client to connect to mcp server

* stdio (for local mcp server)
* SSE (for remote/managed mcp server)

So, there are three kinds of setting of MCP

1. local MCP server without access to the outside world (for example, internet)
2. local MCP server with access to the outside world (for example, downloading from the internet)
3. remote MCP server

what is a mcp client ? what is a mcp server ? why we need this client-server pair structure ?



## Articles

* [What Is MCP, and Why Is Everyone – Suddenly!– Talking About It?](https://huggingface.co/blog/Kseniase/mcp)
* [Top 11 essential mcp libraries](https://huggingface.co/blog/LLMhacker/top-11-essential-mcp-libraries)