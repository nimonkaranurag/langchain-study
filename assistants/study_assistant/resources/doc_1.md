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

* [Prerequisites](#prerequisites)
* [Deploy your agent](#deploy-your-agent)
* [1. Create a repository on GitHub](#1-create-a-repository-on-github)

[Use in production](/oss/python/langchain/studio)

# Deploy

LangSmith is the fastest way to turn agents into production systems. Traditional hosting platforms are built for stateless, short-lived web apps, while LangGraph is **purpose-built for stateful, long-running agents**, so you can go from repo to reliable cloud deployment in minutes.

## [​](#prerequisites) Prerequisites

Before you begin, ensure you have the following:

* A [GitHub account](https://github.com/)
* A [LangSmith account](https://smith.langchain.com/) (free to sign up)

## [​](#deploy-your-agent) Deploy your agent

### [​](#1-create-a-repository-on-github) 1. Create a repository on GitHub

Your application’s code must reside in a GitHub repository to be deployed on LangSmith. Both public and private repositories are supported. For this quickstart, first make sure your app is LangGraph-compatible by following the [local server setup guide](/oss/python/langchain/studio#setup-local-agent-server). Then, push your code to the repository. 

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/deploy.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Test

Previous](/oss/python/langchain/test)[Agent Chat UI](/oss/python/langchain/ui)