We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

* [Overview](/oss/python/langchain/overview)

##### LangChain v1.0

* [Release notes](/oss/python/releases/langchain-v1)
* [Migration guide](/oss/python/migrate/langchain-v1)

##### Get started

* [Install](/oss/python/langchain/install)
* [Quickstart](/oss/python/langchain/quickstart)
* [Philosophy](/oss/python/langchain/philosophy)

##### Core components

* [Agents](/oss/python/langchain/agents)
* [Models](/oss/python/langchain/models)
* [Messages](/oss/python/langchain/messages)
* [Tools](/oss/python/langchain/tools)
* [Short-term memory](/oss/python/langchain/short-term-memory)
* [Streaming](/oss/python/langchain/streaming)
* [Middleware](/oss/python/langchain/middleware)
* [Structured output](/oss/python/langchain/structured-output)

##### Advanced usage

* [Guardrails](/oss/python/langchain/guardrails)
* [Runtime](/oss/python/langchain/runtime)
* [Context engineering](/oss/python/langchain/context-engineering)
* [Model Context Protocol (MCP)](/oss/python/langchain/mcp)
* [Human-in-the-loop](/oss/python/langchain/human-in-the-loop)
* [Multi-agent](/oss/python/langchain/multi-agent)
* [Retrieval](/oss/python/langchain/retrieval)
* [Long-term memory](/oss/python/langchain/long-term-memory)

##### Use in production

* [Studio](/oss/python/langchain/studio)
* [Test](/oss/python/langchain/test)
* [Deploy](/oss/python/langchain/deploy)
* [Agent Chat UI](/oss/python/langchain/ui)
* [Observability](/oss/python/langchain/observability)

* [Install](#install)
* [Transport types](#transport-types)
* [Use MCP tools](#use-mcp-tools)
* [Custom MCP servers](#custom-mcp-servers)
* [Stateful tool usage](#stateful-tool-usage)
* [Additional resources](#additional-resources)

[Advanced usage](/oss/python/langchain/guardrails)

# Model Context Protocol (MCP)

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open protocol that standardizes how applications provide tools and context to LLMs. LangChain agents can use tools defined on MCP servers using the [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters) library.

## [​](#install) Install

Install the `langchain-mcp-adapters` library to use MCP tools in LangGraph:

Copy

Ask AI

```
pip install langchain-mcp-adapters pip  install langchain-mcp-adapters
```

## [​](#transport-types) Transport types

MCP supports different transport mechanisms for client-server communication:

* **stdio** – Client launches server as a subprocess and communicates via standard input/output. Best for local tools and simple setups.
* **Streamable HTTP** – Server runs as an independent process handling HTTP requests. Supports remote connections and multiple clients.
* **Server-Sent Events (SSE)** – a variant of streamable HTTP optimized for real-time streaming communication.

## [​](#use-mcp-tools) Use MCP tools

`langchain-mcp-adapters` enables agents to use tools defined across one or more MCP server.

Accessing multiple MCP servers

Copy

Ask AI

```
from langchain_mcp_adapters.client import MultiServerMCPClient from langchain_mcp_adapters.client import  MultiServerMCPClient from langchain.agents import create_agent from langchain.agents import  create_agent client = MultiServerMCPClient( client = MultiServerMCPClient(  { { "math": { "math": { "transport": "stdio", # Local subprocess communication  "transport": "stdio", # Local subprocess communication "command": "python",  "command": "python", # Absolute path to your math_server.py file # Absolute path to your math_server.py file "args": ["/path/to/math_server.py"],  "args": ["/path/to/math_server.py"], }, }, "weather": { "weather": { "transport": "streamable_http", # HTTP-based remote server  "transport": "streamable_http", # HTTP-based remote server  # Ensure you start your weather server on port 8000  # Ensure you start your weather server on port 8000 "url": "http://localhost:8000/mcp",  "url": "http://localhost:8000/mcp", } } } })) tools = await client.get_tools() tools =  await client.get_tools() agent = create_agent(agent = create_agent( "claude-sonnet-4-5-20250929", "claude-sonnet-4-5-20250929",  tools  tools ))math_response = await agent.ainvoke(math_response =  await agent.ainvoke( {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]} {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}))weather_response = await agent.ainvoke(weather_response =  await agent.ainvoke( {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]} {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}))
```

`MultiServerMCPClient` is **stateless by default**. Each tool invocation creates a fresh MCP `ClientSession`, executes the tool, and then cleans up.

## [​](#custom-mcp-servers) Custom MCP servers

To create your own MCP servers, you can use the `mcp` library. This library provides a simple way to define [tools](https://modelcontextprotocol.io/docs/learn/server-concepts#tools-ai-actions) and run them as servers.

Copy

Ask AI

```
pip install mcp pip  install  mcp
```

Use the following reference implementations to test your agent with MCP tool servers.

Math server (stdio transport)

Copy

Ask AI

```
from mcp.server.fastmcp import FastMCP from mcp.server.fastmcp import  FastMCP mcp = FastMCP("Math") mcp = FastMCP("Math") @mcp.tool()@mcp.tool()def add(a: int, b: int) -> int: def  add(a: int, b: int) -> int:  """Add two numbers"""  """Add two numbers""" return a + b  return  a +  b @mcp.tool()@mcp.tool()def multiply(a: int, b: int) -> int: def  multiply(a: int, b: int) -> int:  """Multiply two numbers"""  """Multiply two numbers""" return a * b  return  a *  b if __name__ == "__main__": if  __name__ ==  "__main__": mcp.run(transport="stdio") mcp.run(transport = "stdio")
```

Weather server (streamable HTTP transport)

Copy

Ask AI

```
from mcp.server.fastmcp import FastMCP from mcp.server.fastmcp import  FastMCP mcp = FastMCP("Weather") mcp = FastMCP("Weather") @mcp.tool()@mcp.tool()async def get_weather(location: str) -> str: async  def  get_weather(location: str) -> str: """Get weather for location.""" """Get weather for location."""  return "It's always sunny in New York"  return  "It's always sunny in New York" if __name__ == "__main__": if  __name__ ==  "__main__": mcp.run(transport="streamable-http") mcp.run(transport ="streamable-http")
```

## [​](#stateful-tool-usage) Stateful tool usage

For stateful servers that maintain context between tool calls, use `client.session()` to create a persistent `ClientSession`.

Using MCP ClientSession for stateful tool usage

Copy

Ask AI

```
from langchain_mcp_adapters.tools import load_mcp_tools from langchain_mcp_adapters.tools import  load_mcp_tools client = MultiServerMCPClient({...}) client = MultiServerMCPClient({...})async with client.session("math") as session: async  with client.session("math") as session: tools = await load_mcp_tools(session)  tools =  await load_mcp_tools(session)
```

## [​](#additional-resources) Additional resources

* [MCP documentation](https://modelcontextprotocol.io/introduction)
* [MCP Transport documentation](https://modelcontextprotocol.io/docs/concepts/transports)
* [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters)

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/mcp.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Context engineering in agents](/oss/python/langchain/context-engineering)[Human-in-the-loop](/oss/python/langchain/human-in-the-loop)