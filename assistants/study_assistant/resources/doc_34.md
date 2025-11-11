We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

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

* [Overview](#overview)
* [Actors](#actors)
* [Channels](#channels)
* [Examples](#examples)
* [High-level API](#high-level-api)

[LangGraph APIs](/oss/python/langgraph/graph-api)

# LangGraph runtime

[`Pregel`](https://reference.langchain.com/python/langgraph/pregel/) implements LangGraph’s runtime, managing the execution of LangGraph applications. Compiling a [StateGraph](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.StateGraph) or creating an [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/#langgraph.func.entrypoint) produces a [`Pregel`](https://reference.langchain.com/python/langgraph/pregel/) instance that can be invoked with input. This guide explains the runtime at a high level and provides instructions for directly implementing applications with Pregel.
> **Note:** The [`Pregel`](https://reference.langchain.com/python/langgraph/pregel/) runtime is named after [Google’s Pregel algorithm](https://research.google/pubs/pub37252/), which describes an efficient method for large-scale parallel computation using graphs.

## [​](#overview) Overview

In LangGraph, Pregel combines [**actors**](https://en.wikipedia.org/wiki/Actor_model) and **channels** into a single application. **Actors** read data from channels and write data to channels. Pregel organizes the execution of the application into multiple steps, following the **Pregel Algorithm**/**Bulk Synchronous Parallel** model. Each step consists of three phases:

* **Plan**: Determine which **actors** to execute in this step. For example, in the first step, select the **actors** that subscribe to the special **input** channels; in subsequent steps, select the **actors** that subscribe to channels updated in the previous step.
* **Execution**: Execute all selected **actors** in parallel, until all complete, or one fails, or a timeout is reached. During this phase, channel updates are invisible to actors until the next step.
* **Update**: Update the channels with the values written by the **actors** in this step.

Repeat until no **actors** are selected for execution, or a maximum number of steps is reached.

## [​](#actors) Actors

An **actor** is a `PregelNode`. It subscribes to channels, reads data from them, and writes data to them. It can be thought of as an **actor** in the Pregel algorithm. `PregelNodes` implement LangChain’s Runnable interface.

## [​](#channels) Channels

Channels are used to communicate between actors (PregelNodes). Each channel has a value type, an update type, and an update function – which takes a sequence of updates and modifies the stored value. Channels can be used to send data from one chain to another, or to send data from a chain to itself in a future step. LangGraph provides a number of built-in channels:

* [`LastValue`](https://reference.langchain.com/python/langgraph/channels/#langgraph.channels.LastValue): The default channel, stores the last value sent to the channel, useful for input and output values, or for sending data from one step to the next.
* [`Topic`](https://reference.langchain.com/python/langgraph/channels/#langgraph.channels.Topic): A configurable PubSub Topic, useful for sending multiple values between **actors**, or for accumulating output. Can be configured to deduplicate values or to accumulate values over the course of multiple steps.
* [`BinaryOperatorAggregate`](https://reference.langchain.com/python/langgraph/pregel/#langgraph.pregel.Pregel--advanced-channels-context-and-binaryoperatoraggregate): stores a persistent value, updated by applying a binary operator to the current value and each update sent to the channel, useful for computing aggregates over multiple steps; e.g.,`total = BinaryOperatorAggregate(int, operator.add)`

## [​](#examples) Examples

While most users will interact with Pregel through the [StateGraph](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.StateGraph) API or the [`@entrypoint`](https://reference.langchain.com/python/langgraph/func/#langgraph.func.entrypoint) decorator, it is possible to interact with Pregel directly. Below are a few different examples to give you a sense of the Pregel API.

* Single node
* Multiple nodes
* Topic
* BinaryOperatorAggregate
* Cycle

Copy

Ask AI

```
from langgraph.channels import EphemeralValue from langgraph.channels import  EphemeralValuefrom langgraph.pregel import Pregel, NodeBuilder from langgraph.pregel import Pregel, NodeBuilder node1 = (node1 = ( NodeBuilder().subscribe_only("a") NodeBuilder().subscribe_only("a") .do(lambda x: x + x) .do(lambda  x: x + x) .write_to("b") .write_to("b"))) app = Pregel(app = Pregel( nodes={"node1": node1},  nodes ={"node1": node1}, channels={ channels ={ "a": EphemeralValue(str),  "a": EphemeralValue(str), "b": EphemeralValue(str),  "b": EphemeralValue(str), }, }, input_channels=["a"],  input_channels =["a"], output_channels=["b"],  output_channels =["b"],)) app.invoke({"a": "foo"})app.invoke({"a": "foo"})
```

Copy

Ask AI

```
{'b': 'foofoo'}{'b': 'foofoo'} 
```

## [​](#high-level-api) High-level API

LangGraph provides two high-level APIs for creating a Pregel application: the [StateGraph (Graph API)](/oss/python/langgraph/graph-api) and the [Functional API](/oss/python/langgraph/functional-api).

* StateGraph (Graph API)
* Functional API

The [StateGraph (Graph API)](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.StateGraph) is a higher-level abstraction that simplifies the creation of Pregel applications. It allows you to define a graph of nodes and edges. When you compile the graph, the StateGraph API automatically creates the Pregel application for you.

Copy

Ask AI

```
from typing import TypedDict from  typing import  TypedDict from langgraph.constants import START from langgraph.constants import  STARTfrom langgraph.graph import StateGraph from langgraph.graph import  StateGraph class Essay(TypedDict): class  Essay(TypedDict): topic: str topic: str content: str | None content: str  |  None score: float | None score: float  |  None def write_essay(essay: Essay): def  write_essay(essay: Essay): return { return { "content": f"Essay about {essay['topic']}",  "content": f "Essay about {essay['topic']} ", } } def score_essay(essay: Essay): def  score_essay(essay: Essay): return { return { "score": 10  "score": 10 } } builder = StateGraph(Essay) builder = StateGraph(Essay)builder.add_node(write_essay)builder.add_node(write_essay)builder.add_node(score_essay)builder.add_node(score_essay)builder.add_edge(START, "write_essay")builder.add_edge(START, "write_essay")builder.add_edge("write_essay", "score_essay")builder.add_edge("write_essay", "score_essay") # Compile the graph.# Compile the graph.# This will return a Pregel instance.# This will return a Pregel instance.graph = builder.compile() graph = builder.compile()
```

The compiled Pregel instance will be associated with a list of nodes and channels. You can inspect the nodes and channels by printing them.

Copy

Ask AI

```
print(graph.nodes) print(graph.nodes)
```

You will see something like this:

Copy

Ask AI

```
{'__start__': ,{'__start__': , 'write_essay': , 'write_essay': , 'score_essay': } 'score_essay': } 
```

Copy

Ask AI

```
print(graph.channels) print(graph.channels)
```

You should see something like this

Copy

Ask AI

```
{'topic': ,{'topic': , 'content': , 'content': , 'score': , 'score': , '__start__': , '__start__': , 'write_essay': , 'write_essay': , 'score_essay': , 'score_essay': , 'branch:__start__:__self__:write_essay': , 'branch:__start__:__self__:write_essay': , 'branch:__start__:__self__:score_essay': , 'branch:__start__:__self__:score_essay': , 'branch:write_essay:__self__:write_essay': , 'branch:write_essay:__self__:write_essay': , 'branch:write_essay:__self__:score_essay': , 'branch:write_essay:__self__:score_essay': , 'branch:score_essay:__self__:write_essay': , 'branch:score_essay:__self__:write_essay': , 'branch:score_essay:__self__:score_essay': , 'branch:score_essay:__self__:score_essay': , 'start:write_essay': } 'start:write_essay': } 
```

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/pregel.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Use the functional API](/oss/python/langgraph/use-functional-api)