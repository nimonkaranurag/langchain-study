[Skip to main content](#content-area)

* [Overview](/oss/python/langgraph/overview)

##### LangGraph v1.0

* [Release notes](/oss/python/releases/langgraph-v1)
* [Migration guide](/oss/python/migrate/langgraph-v1)

##### Get started

* [Install](/oss/python/langgraph/install)
* [Quickstart](/oss/python/langgraph/quickstart)
* [Local server](/oss/python/langgraph/local-server)
* [Thinking in LangGraph](/oss/python/langgraph/thinking-in-langgraph)
* [Workflows + agents](/oss/python/langgraph/workflows-agents)

##### Capabilities

* [Persistence](/oss/python/langgraph/persistence)
* [Durable execution](/oss/python/langgraph/durable-execution)
* [Streaming](/oss/python/langgraph/streaming)
* [Interrupts](/oss/python/langgraph/interrupts)
* [Time travel](/oss/python/langgraph/use-time-travel)
* [Memory](/oss/python/langgraph/add-memory)
* [Subgraphs](/oss/python/langgraph/use-subgraphs)

##### Production

* [Application structure](/oss/python/langgraph/application-structure)
* [Studio](/oss/python/langgraph/studio)
* [Test](/oss/python/langgraph/test)
* [Deploy](/oss/python/langgraph/deploy)
* [Agent Chat UI](/oss/python/langgraph/ui)
* [Observability](/oss/python/langgraph/observability)

##### LangGraph APIs

* [Runtime](/oss/python/langgraph/pregel)

* [Install](#install)
* [Core benefits](#core-benefits)
* [LangGraph ecosystem](#langgraph-ecosystem)
* [Acknowledgements](#acknowledgements)

# LangGraph overview

**LangGraph v1.0 is now available!**For a complete list of changes and instructions on how to upgrade your code, see the [release notes](/oss/python/releases/langgraph-v1) and [migration guide](/oss/python/migrate/langgraph-v1).If you encounter any issues or have feedback, please [open an issue](https://github.com/langchain-ai/docs/issues/new?template=02-langgraph.yml&labels=langgraph,python) so we can improve. To view v0.x documentation, [go to the archived content](https://github.com/langchain-ai/langgraph/tree/main/docs/docs).

Trusted by companies shaping the future of agents— including Klarna, Replit, Elastic, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.
LangGraph is very low-level, and focused entirely on agent **orchestration**. Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with [models](/oss/python/langchain/models) and [tools](/oss/python/langchain/tools).
We will commonly use [LangChain](/oss/python/langchain/overview) components throughout the documentation to integrate models and tools, but you don’t need to use LangChain to use LangGraph. If you are just getting started with agents or want a higher-level abstraction, we recommend you use LangChain’s [agents](/oss/python/langchain/agents) that provide pre-built architectures for common LLM and tool-calling loops.
LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.

## [​](#install) Install

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

## [​](#core-benefits) Core benefits

LangGraph provides low-level supporting infrastructure for *any* long-running, stateful workflow or agent. LangGraph does not abstract prompts or architecture, and provides the following central benefits:

* [Durable execution](/oss/python/langgraph/durable-execution): Build agents that persist through failures and can run for extended periods, resuming from where they left off.
* [Human-in-the-loop](/oss/python/langgraph/interrupts): Incorporate human oversight by inspecting and modifying agent state at any point.
* [Comprehensive memory](/oss/python/concepts/memory): Create stateful agents with both short-term working memory for ongoing reasoning and long-term memory across sessions.
* [Debugging with LangSmith](/langsmith/home): Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
* [Production-ready deployment](/langsmith/deployments): Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.

## [​](#langgraph-ecosystem) LangGraph ecosystem

While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents. To improve your LLM application development, pair LangGraph with:

* [LangSmith](http://www.langchain.com/langsmith) — Helpful for agent evals and observability. Debug poor-performing LLM app runs, evaluate agent trajectories, gain visibility in production, and improve performance over time.
* [LangSmith](/langsmith/home) — Deploy and scale agents effortlessly with a purpose-built deployment platform for long running, stateful workflows. Discover, reuse, configure, and share agents across teams — and iterate quickly with visual prototyping in [Studio](/langsmith/studio).
* [LangChain](/oss/python/langchain/overview) - Provides integrations and composable components to streamline LLM application development. Contains agent abstractions built on top of LangGraph.

## [​](#acknowledgements) Acknowledgements

LangGraph is inspired by [Pregel](https://research.google/pubs/pub37252/) and [Apache Beam](https://beam.apache.org/). The public interface draws inspiration from [NetworkX](https://networkx.org/documentation/latest/). LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.


---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/overview.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[What's new in v1

Next](/oss/python/releases/langgraph-v1)