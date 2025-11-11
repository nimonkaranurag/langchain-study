LangGraph overview - Docs by LangChain

===============

[Skip to main content](https://docs.langchain.com/oss/python/langgraph/overview#content-area)

We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page![Image 1: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 2: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)LangChain + LangGraph

Search...

Ctrl K

*   [GitHub](https://github.com/langchain-ai)
*   [Try LangSmith](https://smith.langchain.com/)
*   [Try LangSmith](https://smith.langchain.com/)

Search...

Navigation

LangGraph overview

[LangChain](https://docs.langchain.com/oss/python/langchain/overview)[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)[Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview)[Integrations](https://docs.langchain.com/oss/python/integrations/providers/overview)[Learn](https://docs.langchain.com/oss/python/learn)[Reference](https://docs.langchain.com/oss/python/reference/overview)[Contribute](https://docs.langchain.com/oss/python/contributing/overview)

Python

*   [Overview](https://docs.langchain.com/oss/python/langgraph/overview)

##### LangGraph v1.0

*   [Release notes](https://docs.langchain.com/oss/python/releases/langgraph-v1)
*   [Migration guide](https://docs.langchain.com/oss/python/migrate/langgraph-v1)

##### Get started

*   [Install](https://docs.langchain.com/oss/python/langgraph/install)
*   [Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
*   [Local server](https://docs.langchain.com/oss/python/langgraph/local-server)
*   [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
*   [Workflows + agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

##### Capabilities

*   [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
*   [Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
*   [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
*   [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
*   [Time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
*   [Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
*   [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

##### Production

*   [Application structure](https://docs.langchain.com/oss/python/langgraph/application-structure)
*   [Studio](https://docs.langchain.com/oss/python/langgraph/studio)
*   [Test](https://docs.langchain.com/oss/python/langgraph/test)
*   [Deploy](https://docs.langchain.com/oss/python/langgraph/deploy)
*   [Agent Chat UI](https://docs.langchain.com/oss/python/langgraph/ui)
*   [Observability](https://docs.langchain.com/oss/python/langgraph/observability)

##### LangGraph APIs

*   Graph API 
*   Functional API 
*   [Runtime](https://docs.langchain.com/oss/python/langgraph/pregel)

![Image 3: US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

close

On this page
*   [Install](https://docs.langchain.com/oss/python/langgraph/overview#install)
*   [Core benefits](https://docs.langchain.com/oss/python/langgraph/overview#core-benefits)
*   [LangGraph ecosystem](https://docs.langchain.com/oss/python/langgraph/overview#langgraph-ecosystem)
*   [Acknowledgements](https://docs.langchain.com/oss/python/langgraph/overview#acknowledgements)

LangGraph overview
==================

Copy page

Copy page

**LangGraph v1.0 is now available!**For a complete list of changes and instructions on how to upgrade your code, see the [release notes](https://docs.langchain.com/oss/python/releases/langgraph-v1) and [migration guide](https://docs.langchain.com/oss/python/migrate/langgraph-v1).If you encounter any issues or have feedback, please [open an issue](https://github.com/langchain-ai/docs/issues/new?template=02-langgraph.yml&labels=langgraph,python) so we can improve. To view v0.x documentation, [go to the archived content](https://github.com/langchain-ai/langgraph/tree/main/docs/docs).

Trusted by companies shaping the future of agents— including Klarna, Replit, Elastic, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.LangGraph is very low-level, and focused entirely on agent **orchestration**. Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with [models](https://docs.langchain.com/oss/python/langchain/models) and [tools](https://docs.langchain.com/oss/python/langchain/tools).We will commonly use [LangChain](https://docs.langchain.com/oss/python/langchain/overview) components throughout the documentation to integrate models and tools, but you don’t need to use LangChain to use LangGraph. If you are just getting started with agents or want a higher-level abstraction, we recommend you use LangChain’s [agents](https://docs.langchain.com/oss/python/langchain/agents) that provide pre-built architectures for common LLM and tool-calling loops.LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.
[​](https://docs.langchain.com/oss/python/langgraph/overview#install)

 Install
-------------------------------------------------------------------------------

pip

uv

Copy

Ask AI

```
pip install -U langgraph
```

Then, create a simple hello world example:

Copy

Ask AI

```
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```

[​](https://docs.langchain.com/oss/python/langgraph/overview#core-benefits)

Core benefits
------------------------------------------------------------------------------------------

LangGraph provides low-level supporting infrastructure for _any_ long-running, stateful workflow or agent. LangGraph does not abstract prompts or architecture, and provides the following central benefits:
*   [Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution): Build agents that persist through failures and can run for extended periods, resuming from where they left off.
*   [Human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/interrupts): Incorporate human oversight by inspecting and modifying agent state at any point.
*   [Comprehensive memory](https://docs.langchain.com/oss/python/concepts/memory): Create stateful agents with both short-term working memory for ongoing reasoning and long-term memory across sessions.
*   [Debugging with LangSmith](https://docs.langchain.com/langsmith/home): Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
*   [Production-ready deployment](https://docs.langchain.com/langsmith/deployments): Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.

[​](https://docs.langchain.com/oss/python/langgraph/overview#langgraph-ecosystem)

LangGraph ecosystem
------------------------------------------------------------------------------------------------------

While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents. To improve your LLM application development, pair LangGraph with:
*   [LangSmith](http://www.langchain.com/langsmith) — Helpful for agent evals and observability. Debug poor-performing LLM app runs, evaluate agent trajectories, gain visibility in production, and improve performance over time.
*   [LangSmith](https://docs.langchain.com/langsmith/home) — Deploy and scale agents effortlessly with a purpose-built deployment platform for long running, stateful workflows. Discover, reuse, configure, and share agents across teams — and iterate quickly with visual prototyping in [Studio](https://docs.langchain.com/langsmith/studio).
*   [LangChain](https://docs.langchain.com/oss/python/langchain/overview) - Provides integrations and composable components to streamline LLM application development. Contains agent abstractions built on top of LangGraph.

[​](https://docs.langchain.com/oss/python/langgraph/overview#acknowledgements)

Acknowledgements
------------------------------------------------------------------------------------------------

LangGraph is inspired by [Pregel](https://research.google/pubs/pub37252/) and [Apache Beam](https://beam.apache.org/). The public interface draws inspiration from [NetworkX](https://networkx.org/documentation/latest/). LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.

* * *

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/overview.mdx)

[Connect these docs programmatically](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

Yes No

[What's new in v1 Next](https://docs.langchain.com/oss/python/releases/langgraph-v1)

Ctrl+I

[Docs by LangChain home page![Image 4: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 5: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

Resources

[Forum](https://forum.langchain.com/)[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Trust Center](https://trust.langchain.com/)

Company

[About](https://langchain.com/about)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

[Powered by Mintlify](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=langchain-5e9cc07a)

Assistant

Responses are generated using AI and may contain mistakes.