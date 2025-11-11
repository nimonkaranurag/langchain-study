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

* [Agent Chat UI](#agent-chat-ui)
* [Features](#features)
* [Quick start](#quick-start)
* [Local development](#local-development)
* [Connect to your agent](#connect-to-your-agent)

[Use in production](/oss/python/langchain/studio)

# Agent Chat UI

LangChain provides a powerful prebuilt user interface that work seamlessly with agents created using [`create_agent`](/oss/python/langchain/agents). This UI is designed to provide rich, interactive experiences for your agents with minimal setup, whether you’re running locally or in a deployed context (such as [LangSmith](/langsmith)).

## [​](#agent-chat-ui) Agent Chat UI

[Agent Chat UI](https://github.com/langchain-ai/agent-chat-ui) is a Next.js application that provides a conversational interface for interacting with any LangChain agent. It supports real-time chat, tool visualization, and advanced features like time-travel debugging and state forking. Agent Chat UI is open source and can be adapted to your application needs.

### [​](#features) Features

Tool visualization

Studio automatically renders tool calls and results in an intuitive interface.

 

Time-travel debugging

Navigate through conversation history and fork from any point

 

State inspection

View and modify agent state at any point during execution

 

Human-in-the-loop

Built-in support for reviewing and responding to agent requests

You can use generative UI in the Agent Chat UI. For more information, see [Implement generative user interfaces with LangGraph](/langsmith/generative-ui-react).

### [​](#quick-start) Quick start

The fastest way to get started is using the hosted version:

1. **Visit [Agent Chat UI](https://agentchat.vercel.app)**
2. **Connect your agent** by entering your deployment URL or local server address
3. **Start chatting** - the UI will automatically detect and render tool calls and interrupts

### [​](#local-development) Local development

For customization or local development, you can run Agent Chat UI locally:

Copy

Ask AI

```
# Create a new Agent Chat UI project # Create a new Agent Chat UI projectnpx create-agent-chat-app --project-name my-chat-ui npx create-agent-chat-app --project-name my-chat-uicd my-chat-ui cd my-chat-ui # Install dependencies and start # Install dependencies and start pnpm install pnpm  install pnpm dev pnpm  dev
```

### [​](#connect-to-your-agent) Connect to your agent

Agent Chat UI can connect to both [local](/oss/python/langchain/studio#setup-local-langgraph-server) and [deployed agents](/oss/python/langchain/deploy). After starting Agent Chat UI, you’ll need to configure it to connect to your agent:

1. **Graph ID**: Enter your graph name (find this under `graphs` in your `langgraph.json` file)
2. **Deployment URL**: Your LangGraph server’s endpoint (e.g., `http://localhost:2024` for local development, or your deployed agent’s URL)
3. **LangSmith API key (optional)**: Add your LangSmith API key (not required if you’re using a local LangGraph server)

Once configured, Agent Chat UI will automatically fetch and display any interrupted threads from your agent.

Agent Chat UI has out-of-the-box support for rendering tool calls and tool result messages. To customize what messages are shown, see [Hiding Messages in the Chat](https://github.com/langchain-ai/agent-chat-ui?tab=readme-ov-file#hiding-messages-in-the-chat).

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/ui.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Deploy](/oss/python/langchain/deploy)[Observability](/oss/python/langchain/observability)