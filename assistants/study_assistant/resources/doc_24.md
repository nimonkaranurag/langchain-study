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

* [Setup](#setup)
* [Invoke a graph from a node](#invoke-a-graph-from-a-node)
* [Add a graph as a node](#add-a-graph-as-a-node)
* [Add persistence](#add-persistence)
* [View subgraph state](#view-subgraph-state)
* [Stream subgraph outputs](#stream-subgraph-outputs)

[Capabilities](/oss/python/langgraph/persistence)

# Subgraphs

This guide explains the mechanics of using subgraphs. A subgraph is a [graph](/oss/python/langgraph/graph-api#graphs) that is used as a [node](/oss/python/langgraph/graph-api#nodes) in another graph. Subgraphs are useful for:

* Building [multi-agent systems](/oss/python/langchain/multi-agent)
* Re-using a set of nodes in multiple graphs
* Distributing development: when you want different teams to work on different parts of the graph independently, you can define each part as a subgraph, and as long as the subgraph interface (the input and output schemas) is respected, the parent graph can be built without knowing any details of the subgraph

When adding subgraphs, you need to define how the parent graph and the subgraph communicate:

* [Invoke a graph from a node](#invoke-a-graph-from-a-node) — subgraphs are called from inside a node in the parent graph
* [Add a graph as a node](#add-a-graph-as-a-node) — a subgraph is added directly as a node in the parent and **shares [state keys](/oss/python/langgraph/graph-api#state)** with the parent

## [​](#setup) Setup

Copy

Ask AI

```
pip install -U langgraph pip  install -U  langgraph
```

**Set up LangSmith for LangGraph development** Sign up for [LangSmith](https://smith.langchain.com) to quickly spot issues and improve the performance of your LangGraph projects. LangSmith lets you use trace data to debug, test, and monitor your LLM apps built with LangGraph — read more about how to get started [here](https://docs.smith.langchain.com).

## [​](#invoke-a-graph-from-a-node) Invoke a graph from a node

A simple way to implement a subgraph is to invoke a graph from inside the node of another graph. In this case subgraphs can have **completely different schemas** from the parent graph (no shared keys). For example, you might want to keep a private message history for each of the agents in a [multi-agent](/oss/python/langchain/multi-agent) system. If that’s the case for your application, you need to define a node **function that invokes the subgraph**. This function needs to transform the input (parent) state to the subgraph state before invoking the subgraph, and transform the results back to the parent state before returning the state update from the node.

Copy

Ask AI

```
from typing_extensions import TypedDict from  typing_extensions import  TypedDictfrom langgraph.graph.state import StateGraph, START from langgraph.graph.state import StateGraph, START class SubgraphState(TypedDict): class  SubgraphState(TypedDict): bar: str bar: str # Subgraph # Subgraph def subgraph_node_1(state: SubgraphState): def  subgraph_node_1(state: SubgraphState): return {"bar": "hi! " + state["bar"]}  return {"bar": "hi! " + state["bar"]} subgraph_builder = StateGraph(SubgraphState) subgraph_builder = StateGraph(SubgraphState)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge(START, "subgraph_node_1")subgraph = subgraph_builder.compile() subgraph = subgraph_builder.compile() # Parent graph # Parent graph class State(TypedDict): class  State(TypedDict): foo: str foo: str def call_subgraph(state: State): def  call_subgraph(state: State):  # Transform the state to the subgraph state  # Transform the state to the subgraph state subgraph_output = subgraph.invoke({"bar": state["foo"]})  subgraph_output = subgraph.invoke({"bar": state["foo"]})  # Transform response back to the parent state  # Transform response back to the parent state return {"foo": subgraph_output["bar"]}  return {"foo": subgraph_output["bar"]} builder = StateGraph(State) builder = StateGraph(State)builder.add_node("node_1", call_subgraph)builder.add_node("node_1", call_subgraph)builder.add_edge(START, "node_1")builder.add_edge(START, "node_1")graph = builder.compile() graph = builder.compile()
```

Full example: different state schemas

Copy

Ask AI

```
from typing_extensions import TypedDict from  typing_extensions import  TypedDictfrom langgraph.graph.state import StateGraph, START from langgraph.graph.state import StateGraph, START # Define subgraph # Define subgraphclass SubgraphState(TypedDict): class  SubgraphState(TypedDict):  # note that none of these keys are shared with the parent graph state  # note that none of these keys are shared with the parent graph state bar: str bar: str baz: str baz: str def subgraph_node_1(state: SubgraphState): def  subgraph_node_1(state: SubgraphState): return {"baz": "baz"}  return {"baz": "baz"} def subgraph_node_2(state: SubgraphState): def  subgraph_node_2(state: SubgraphState): return {"bar": state["bar"] + state["baz"]}  return {"bar": state["bar"] + state["baz"]} subgraph_builder = StateGraph(SubgraphState) subgraph_builder = StateGraph(SubgraphState)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_2)subgraph_builder.add_node(subgraph_node_2)subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")subgraph = subgraph_builder.compile() subgraph = subgraph_builder.compile() # Define parent graph # Define parent graphclass ParentState(TypedDict): class  ParentState(TypedDict): foo: str foo: str def node_1(state: ParentState): def  node_1(state: ParentState): return {"foo": "hi! " + state["foo"]}  return {"foo": "hi! " + state["foo"]} def node_2(state: ParentState): def  node_2(state: ParentState):  # Transform the state to the subgraph state  # Transform the state to the subgraph state response = subgraph.invoke({"bar": state["foo"]})  response = subgraph.invoke({"bar": state["foo"]})  # Transform response back to the parent state  # Transform response back to the parent state return {"foo": response["bar"]}  return {"foo": response["bar"]} builder = StateGraph(ParentState) builder = StateGraph(ParentState)builder.add_node("node_1", node_1)builder.add_node("node_1", node_1)builder.add_node("node_2", node_2)builder.add_node("node_2", node_2)builder.add_edge(START, "node_1")builder.add_edge(START, "node_1")builder.add_edge("node_1", "node_2")builder.add_edge("node_1", "node_2")graph = builder.compile() graph = builder.compile() for chunk in graph.stream({"foo": "foo"}, subgraphs=True): for  chunk in graph.stream({"foo": "foo"}, subgraphs = True): print(chunk)  print(chunk)
```

Copy

Ask AI

```
((), {'node_1': {'foo': 'hi! foo'}})((), {'node_1': {'foo': 'hi! foo'}})(('node_2:9c36dd0f-151a-cb42-cbad-fa2f851f9ab7',), {'grandchild_1': {'my_grandchild_key': 'hi Bob, how are you'}})(('node_2:9c36dd0f-151a-cb42-cbad-fa2f851f9ab7',), {'grandchild_1': {'my_grandchild_key': 'hi Bob, how are you'}})(('node_2:9c36dd0f-151a-cb42-cbad-fa2f851f9ab7',), {'grandchild_2': {'bar': 'hi! foobaz'}})(('node_2:9c36dd0f-151a-cb42-cbad-fa2f851f9ab7',), {'grandchild_2': {'bar': 'hi! foobaz'}})((), {'node_2': {'foo': 'hi! foobaz'}})((), {'node_2': {'foo': 'hi! foobaz'}}) 
```

 

Full example: different state schemas (two levels of subgraphs)

This is an example with two levels of subgraphs: parent -> child -> grandchild.

Copy

Ask AI

```
# Grandchild graph # Grandchild graph from typing_extensions import TypedDict from  typing_extensions import  TypedDictfrom langgraph.graph.state import StateGraph, START, END from langgraph.graph.state import StateGraph, START, END class GrandChildState(TypedDict): class  GrandChildState(TypedDict): my_grandchild_key: str my_grandchild_key: str def grandchild_1(state: GrandChildState) -> GrandChildState: def  grandchild_1(state: GrandChildState) -> GrandChildState: # NOTE: child or parent keys will not be accessible here  # NOTE: child or parent keys will not be accessible here return {"my_grandchild_key": state["my_grandchild_key"] + ", how are you"}  return {"my_grandchild_key": state["my_grandchild_key"] + ", how are you"} grandchild = StateGraph(GrandChildState) grandchild = StateGraph(GrandChildState)grandchild.add_node("grandchild_1", grandchild_1)grandchild.add_node("grandchild_1", grandchild_1) grandchild.add_edge(START, "grandchild_1")grandchild.add_edge(START, "grandchild_1")grandchild.add_edge("grandchild_1", END)grandchild.add_edge("grandchild_1", END) grandchild_graph = grandchild.compile() grandchild_graph = grandchild.compile() # Child graph # Child graphclass ChildState(TypedDict): class  ChildState(TypedDict): my_child_key: str my_child_key: str def call_grandchild_graph(state: ChildState) -> ChildState: def  call_grandchild_graph(state: ChildState) -> ChildState: # NOTE: parent or grandchild keys won't be accessible here  # NOTE: parent or grandchild keys won't be accessible here grandchild_graph_input = {"my_grandchild_key": state["my_child_key"]}  grandchild_graph_input = {"my_grandchild_key": state["my_child_key"]} grandchild_graph_output = grandchild_graph.invoke(grandchild_graph_input)  grandchild_graph_output = grandchild_graph.invoke(grandchild_graph_input) return {"my_child_key": grandchild_graph_output["my_grandchild_key"] + " today?"}  return {"my_child_key": grandchild_graph_output["my_grandchild_key"] +  " today?"} child = StateGraph(ChildState) child = StateGraph(ChildState)# We're passing a function here instead of just compiled graph (`grandchild_graph`)# We're passing a function here instead of just compiled graph (`grandchild_graph`)child.add_node("child_1", call_grandchild_graph)child.add_node("child_1", call_grandchild_graph)child.add_edge(START, "child_1")child.add_edge(START, "child_1")child.add_edge("child_1", END)child.add_edge("child_1", END)child_graph = child.compile() child_graph = child.compile() # Parent graph # Parent graphclass ParentState(TypedDict): class  ParentState(TypedDict): my_key: str my_key: str def parent_1(state: ParentState) -> ParentState: def  parent_1(state: ParentState) -> ParentState: # NOTE: child or grandchild keys won't be accessible here  # NOTE: child or grandchild keys won't be accessible here return {"my_key": "hi " + state["my_key"]}  return {"my_key": "hi " + state["my_key"]} def parent_2(state: ParentState) -> ParentState: def  parent_2(state: ParentState) -> ParentState: return {"my_key": state["my_key"] + " bye!"}  return {"my_key": state["my_key"] + " bye!"} def call_child_graph(state: ParentState) -> ParentState: def  call_child_graph(state: ParentState) -> ParentState: child_graph_input = {"my_child_key": state["my_key"]}  child_graph_input = {"my_child_key": state["my_key"]} child_graph_output = child_graph.invoke(child_graph_input)  child_graph_output = child_graph.invoke(child_graph_input) return {"my_key": child_graph_output["my_child_key"]}  return {"my_key": child_graph_output["my_child_key"]} parent = StateGraph(ParentState) parent = StateGraph(ParentState)parent.add_node("parent_1", parent_1)parent.add_node("parent_1", parent_1)# We're passing a function here instead of just a compiled graph (`child_graph`)# We're passing a function here instead of just a compiled graph (`child_graph`)parent.add_node("child", call_child_graph)parent.add_node("child", call_child_graph)parent.add_node("parent_2", parent_2)parent.add_node("parent_2", parent_2) parent.add_edge(START, "parent_1")parent.add_edge(START, "parent_1")parent.add_edge("parent_1", "child")parent.add_edge("parent_1", "child")parent.add_edge("child", "parent_2")parent.add_edge("child", "parent_2")parent.add_edge("parent_2", END)parent.add_edge("parent_2", END) parent_graph = parent.compile() parent_graph = parent.compile() for chunk in parent_graph.stream({"my_key": "Bob"}, subgraphs=True): for  chunk in parent_graph.stream({"my_key": "Bob"}, subgraphs = True): print(chunk)  print(chunk)
```

Copy

Ask AI

```
((), {'parent_1': {'my_key': 'hi Bob'}})((), {'parent_1': {'my_key': 'hi Bob'}})(('child:2e26e9ce-602f-862c-aa66-1ea5a4655e3b', 'child_1:781bb3b1-3971-84ce-810b-acf819a03f9c'), {'grandchild_1': {'my_grandchild_key': 'hi Bob, how are you'}})(('child:2e26e9ce-602f-862c-aa66-1ea5a4655e3b', 'child_1:781bb3b1-3971-84ce-810b-acf819a03f9c'), {'grandchild_1': {'my_grandchild_key': 'hi Bob, how are you'}})(('child:2e26e9ce-602f-862c-aa66-1ea5a4655e3b',), {'child_1': {'my_child_key': 'hi Bob, how are you today?'}})(('child:2e26e9ce-602f-862c-aa66-1ea5a4655e3b',), {'child_1': {'my_child_key': 'hi Bob, how are you today?'}})((), {'child': {'my_key': 'hi Bob, how are you today?'}})((), {'child': {'my_key': 'hi Bob, how are you today?'}})((), {'parent_2': {'my_key': 'hi Bob, how are you today? bye!'}})((), {'parent_2': {'my_key': 'hi Bob, how are you today? bye!'}}) 
```

## [​](#add-a-graph-as-a-node) Add a graph as a node

When the parent graph and subgraph can communicate over a shared state key (channel) in the [schema](/oss/python/langgraph/graph-api#state), you can add a graph as a [node](/oss/python/langgraph/graph-api#nodes) in another graph. For example, in [multi-agent](/oss/python/langchain/multi-agent) systems, the agents often communicate over a shared [messages](/oss/python/langgraph/graph-api#why-use-messages) key.  If your subgraph shares state keys with the parent graph, you can follow these steps to add it to your graph:

1. Define the subgraph workflow (`subgraph_builder` in the example below) and compile it
2. Pass compiled subgraph to the [`add_node`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.StateGraph.add_node) method when defining the parent graph workflow

Copy

Ask AI

```
from typing_extensions import TypedDict from  typing_extensions import  TypedDictfrom langgraph.graph.state import StateGraph, START from langgraph.graph.state import StateGraph, START class State(TypedDict): class  State(TypedDict): foo: str foo: str # Subgraph # Subgraph def subgraph_node_1(state: State): def  subgraph_node_1(state: State): return {"foo": "hi! " + state["foo"]}  return {"foo": "hi! " + state["foo"]} subgraph_builder = StateGraph(State) subgraph_builder = StateGraph(State)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge(START, "subgraph_node_1")subgraph = subgraph_builder.compile() subgraph = subgraph_builder.compile() # Parent graph # Parent graph builder = StateGraph(State) builder = StateGraph(State)builder.add_node("node_1", subgraph) builder.add_node("node_1", subgraph) builder.add_edge(START, "node_1")builder.add_edge(START, "node_1")graph = builder.compile() graph = builder.compile()
```

Full example: shared state schemas

Copy

Ask AI

```
from typing_extensions import TypedDict from  typing_extensions import  TypedDictfrom langgraph.graph.state import StateGraph, START from langgraph.graph.state import StateGraph, START # Define subgraph # Define subgraphclass SubgraphState(TypedDict): class  SubgraphState(TypedDict): foo: str # shared with parent graph state foo: str  # shared with parent graph state bar: str # private to SubgraphState bar: str  # private to SubgraphState def subgraph_node_1(state: SubgraphState): def  subgraph_node_1(state: SubgraphState): return {"bar": "bar"}  return {"bar": "bar"} def subgraph_node_2(state: SubgraphState): def  subgraph_node_2(state: SubgraphState): # note that this node is using a state key ('bar') that is only available in the subgraph # note that this node is using a state key ('bar') that is only available in the subgraph # and is sending update on the shared state key ('foo') # and is sending update on the shared state key ('foo') return {"foo": state["foo"] + state["bar"]}  return {"foo": state["foo"] + state["bar"]} subgraph_builder = StateGraph(SubgraphState) subgraph_builder = StateGraph(SubgraphState)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_2)subgraph_builder.add_node(subgraph_node_2)subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")subgraph = subgraph_builder.compile() subgraph = subgraph_builder.compile() # Define parent graph # Define parent graphclass ParentState(TypedDict): class  ParentState(TypedDict): foo: str foo: str def node_1(state: ParentState): def  node_1(state: ParentState): return {"foo": "hi! " + state["foo"]}  return {"foo": "hi! " + state["foo"]} builder = StateGraph(ParentState) builder = StateGraph(ParentState)builder.add_node("node_1", node_1)builder.add_node("node_1", node_1)builder.add_node("node_2", subgraph)builder.add_node("node_2", subgraph)builder.add_edge(START, "node_1")builder.add_edge(START, "node_1")builder.add_edge("node_1", "node_2")builder.add_edge("node_1", "node_2")graph = builder.compile() graph = builder.compile() for chunk in graph.stream({"foo": "foo"}): for  chunk in graph.stream({"foo": "foo"}): print(chunk)  print(chunk)
```

Copy

Ask AI

```
{'node_1': {'foo': 'hi! foo'}}{'node_1': {'foo': 'hi! foo'}}{'node_2': {'foo': 'hi! foobar'}}{'node_2': {'foo': 'hi! foobar'}} 
```

## [​](#add-persistence) Add persistence

You only need to **provide the checkpointer when compiling the parent graph**. LangGraph will automatically propagate the checkpointer to the child subgraphs.

Copy

Ask AI

```
from langgraph.graph import START, StateGraph from langgraph.graph import  START, StateGraphfrom langgraph.checkpoint.memory import MemorySaver from langgraph.checkpoint.memory import  MemorySaver from typing_extensions import TypedDict from  typing_extensions import  TypedDict class State(TypedDict): class  State(TypedDict): foo: str foo: str # Subgraph # Subgraph def subgraph_node_1(state: State): def  subgraph_node_1(state: State): return {"foo": state["foo"] + "bar"}  return {"foo": state["foo"] +  "bar"} subgraph_builder = StateGraph(State) subgraph_builder = StateGraph(State)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge(START, "subgraph_node_1")subgraph = subgraph_builder.compile() subgraph = subgraph_builder.compile() # Parent graph # Parent graph builder = StateGraph(State) builder = StateGraph(State)builder.add_node("node_1", subgraph)builder.add_node("node_1", subgraph)builder.add_edge(START, "node_1")builder.add_edge(START, "node_1") checkpointer = MemorySaver() checkpointer = MemorySaver()graph = builder.compile(checkpointer=checkpointer) graph = builder.compile(checkpointer =checkpointer)
```

If you want the subgraph to **have its own memory**, you can compile it with the appropriate checkpointer option. This is useful in [multi-agent](/oss/python/langchain/multi-agent) systems, if you want agents to keep track of their internal message histories:

Copy

Ask AI

```
subgraph_builder = StateGraph(...) subgraph_builder = StateGraph(...)subgraph = subgraph_builder.compile(checkpointer=True) subgraph = subgraph_builder.compile(checkpointer = True)
```

## [​](#view-subgraph-state) View subgraph state

When you enable [persistence](/oss/python/langgraph/persistence), you can [inspect the graph state](/oss/python/langgraph/persistence#checkpoints) (checkpoint) via the appropriate method. To view the subgraph state, you can use the subgraphs option. You can inspect the graph state via `graph.get_state(config)`. To view the subgraph state, you can use `graph.get_state(config, subgraphs=True)`.

**Available **only** when interrupted** Subgraph state can only be viewed **when the subgraph is interrupted**. Once you resume the graph, you won’t be able to access the subgraph state.

View interrupted subgraph state

Copy

Ask AI

```
from langgraph.graph import START, StateGraph from langgraph.graph import  START, StateGraphfrom langgraph.checkpoint.memory import MemorySaver from langgraph.checkpoint.memory import  MemorySaverfrom langgraph.types import interrupt, Command from langgraph.types import interrupt, Command from typing_extensions import TypedDict from  typing_extensions import  TypedDict class State(TypedDict): class  State(TypedDict): foo: str foo: str # Subgraph # Subgraph def subgraph_node_1(state: State): def  subgraph_node_1(state: State): value = interrupt("Provide value:")  value = interrupt("Provide value:") return {"foo": state["foo"] + value}  return {"foo": state["foo"] + value} subgraph_builder = StateGraph(State) subgraph_builder = StateGraph(State)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge(START, "subgraph_node_1") subgraph = subgraph_builder.compile() subgraph = subgraph_builder.compile() # Parent graph # Parent graph builder = StateGraph(State) builder = StateGraph(State)builder.add_node("node_1", subgraph)builder.add_node("node_1", subgraph)builder.add_edge(START, "node_1")builder.add_edge(START, "node_1") checkpointer = MemorySaver() checkpointer = MemorySaver()graph = builder.compile(checkpointer=checkpointer) graph = builder.compile(checkpointer =checkpointer) config = {"configurable": {"thread_id": "1"}} config = {"configurable": {"thread_id": "1"}} graph.invoke({"foo": ""}, config)graph.invoke({"foo": ""}, config)parent_state = graph.get_state(config) parent_state = graph.get_state(config) # This will be available only when the subgraph is interrupted.# This will be available only when the subgraph is interrupted.# Once you resume the graph, you won't be able to access the subgraph state.# Once you resume the graph, you won't be able to access the subgraph state.subgraph_state = graph.get_state(config, subgraphs=True).tasks[0].state subgraph_state = graph.get_state(config, subgraphs = True).tasks[0].state # resume the subgraph # resume the subgraphgraph.invoke(Command(resume="bar"), config)graph.invoke(Command(resume = "bar"), config)
```

1. This will be available only when the subgraph is interrupted. Once you resume the graph, you won’t be able to access the subgraph state.

## [​](#stream-subgraph-outputs) Stream subgraph outputs

To include outputs from subgraphs in the streamed outputs, you can set the subgraphs option in the stream method of the parent graph. This will stream outputs from both the parent graph and any subgraphs.

Copy

Ask AI

```
for chunk in graph.stream(for  chunk in graph.stream( {"foo": "foo"}, {"foo": "foo"}, subgraphs=True,  subgraphs = True,  stream_mode="updates",  stream_mode = "updates",):): print(chunk)  print(chunk)
```

Stream from subgraphs

Copy

Ask AI

```
from typing_extensions import TypedDict from  typing_extensions import  TypedDictfrom langgraph.graph.state import StateGraph, START from langgraph.graph.state import StateGraph, START # Define subgraph # Define subgraphclass SubgraphState(TypedDict): class  SubgraphState(TypedDict): foo: str foo: str bar: str bar: str def subgraph_node_1(state: SubgraphState): def  subgraph_node_1(state: SubgraphState): return {"bar": "bar"}  return {"bar": "bar"} def subgraph_node_2(state: SubgraphState): def  subgraph_node_2(state: SubgraphState): # note that this node is using a state key ('bar') that is only available in the subgraph # note that this node is using a state key ('bar') that is only available in the subgraph # and is sending update on the shared state key ('foo') # and is sending update on the shared state key ('foo') return {"foo": state["foo"] + state["bar"]}  return {"foo": state["foo"] + state["bar"]} subgraph_builder = StateGraph(SubgraphState) subgraph_builder = StateGraph(SubgraphState)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_1)subgraph_builder.add_node(subgraph_node_2)subgraph_builder.add_node(subgraph_node_2)subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge(START, "subgraph_node_1")subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")subgraph = subgraph_builder.compile() subgraph = subgraph_builder.compile() # Define parent graph # Define parent graphclass ParentState(TypedDict): class  ParentState(TypedDict): foo: str foo: str def node_1(state: ParentState): def  node_1(state: ParentState): return {"foo": "hi! " + state["foo"]}  return {"foo": "hi! " + state["foo"]} builder = StateGraph(ParentState) builder = StateGraph(ParentState)builder.add_node("node_1", node_1)builder.add_node("node_1", node_1)builder.add_node("node_2", subgraph)builder.add_node("node_2", subgraph)builder.add_edge(START, "node_1")builder.add_edge(START, "node_1")builder.add_edge("node_1", "node_2")builder.add_edge("node_1", "node_2")graph = builder.compile() graph = builder.compile() for chunk in graph.stream(for  chunk in graph.stream( {"foo": "foo"}, {"foo": "foo"}, stream_mode="updates",  stream_mode = "updates", subgraphs=True,  subgraphs = True, ):): print(chunk)  print(chunk)
```

Copy

Ask AI

```
((), {'node_1': {'foo': 'hi! foo'}})((), {'node_1': {'foo': 'hi! foo'}})(('node_2:e58e5673-a661-ebb0-70d4-e298a7fc28b7',), {'subgraph_node_1': {'bar': 'bar'}})(('node_2:e58e5673-a661-ebb0-70d4-e298a7fc28b7',), {'subgraph_node_1': {'bar': 'bar'}})(('node_2:e58e5673-a661-ebb0-70d4-e298a7fc28b7',), {'subgraph_node_2': {'foo': 'hi! foobar'}})(('node_2:e58e5673-a661-ebb0-70d4-e298a7fc28b7',), {'subgraph_node_2': {'foo': 'hi! foobar'}})((), {'node_2': {'foo': 'hi! foobar'}})((), {'node_2': {'foo': 'hi! foobar'}}) 
```

 

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/use-subgraphs.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Memory](/oss/python/langgraph/add-memory)[Application structure](/oss/python/langgraph/application-structure)