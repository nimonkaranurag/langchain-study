We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

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

* [Threads](#threads)
* [Checkpoints](#checkpoints)
* [Get state](#get-state)
* [Get state history](#get-state-history)
* [Replay](#replay)
* [Update state](#update-state)
* [config](#config)
* [values](#values)
* [as\_node](#as-node)
* [Memory Store](#memory-store)
* [Basic Usage](#basic-usage)
* [Semantic Search](#semantic-search)
* [Using in LangGraph](#using-in-langgraph)
* [Checkpointer libraries](#checkpointer-libraries)
* [Checkpointer interface](#checkpointer-interface)
* [Serializer](#serializer)
* [Serialization with pickle](#serialization-with-pickle)
* [Encryption](#encryption)
* [Capabilities](#capabilities)
* [Human-in-the-loop](#human-in-the-loop)
* [Memory](#memory)
* [Time Travel](#time-travel)
* [Fault-tolerance](#fault-tolerance)
* [Pending writes](#pending-writes)

[Capabilities](/oss/python/langgraph/persistence)

# Persistence

LangGraph has a built-in persistence layer, implemented through checkpointers. When you compile a graph with a checkpointer, the checkpointer saves a `checkpoint` of the graph state at every super-step. Those checkpoints are saved to a `thread`, which can be accessed after graph execution. Because `threads` allow access to graph’s state after execution, several powerful capabilities including human-in-the-loop, memory, time travel, and fault-tolerance are all possible. Below, we’ll discuss each of these concepts in more detail. 

**LangGraph API handles checkpointing automatically** When using the LangGraph API, you don’t need to implement or configure checkpointers manually. The API handles all persistence infrastructure for you behind the scenes.

## [​](#threads) Threads

A thread is a unique ID or thread identifier assigned to each checkpoint saved by a checkpointer. It contains the accumulated state of a sequence of [runs](/langsmith/assistants#execution). When a run is executed, the [state](/oss/python/langgraph/graph-api#state) of the underlying graph of the assistant will be persisted to the thread. When invoking a graph with a checkpointer, you **must** specify a `thread_id` as part of the `configurable` portion of the config.

Copy

Ask AI

```
{"configurable": {"thread_id": "1"}}{"configurable": {"thread_id": "1"}}
```

A thread’s current and historical state can be retrieved. To persist state, a thread must be created prior to executing a run. The LangSmith API provides several endpoints for creating and managing threads and thread state. See the [API reference](https://langchain-ai.github.io/langgraph/cloud/reference/api/) for more details.

## [​](#checkpoints) Checkpoints

The state of a thread at a particular point in time is called a checkpoint. Checkpoint is a snapshot of the graph state saved at each super-step and is represented by `StateSnapshot` object with the following key properties:

* `config`: Config associated with this checkpoint.
* `metadata`: Metadata associated with this checkpoint.
* `values`: Values of the state channels at this point in time.
* `next` A tuple of the node names to execute next in the graph.
* `tasks`: A tuple of `PregelTask` objects that contain information about next tasks to be executed. If the step was previously attempted, it will include error information. If a graph was interrupted [dynamically](/oss/python/langgraph/interrupts#pause-using-interrupt) from within a node, tasks will contain additional data associated with interrupts.

Checkpoints are persisted and can be used to restore the state of a thread at a later time. Let’s see what checkpoints are saved when a simple graph is invoked as follows:

Copy

Ask AI

```
from langgraph.graph import StateGraph, START, END from langgraph.graph import StateGraph, START, ENDfrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaverfrom langchain_core.runnables import RunnableConfig from langchain_core.runnables import  RunnableConfig from typing import Annotated from  typing import  Annotated from typing_extensions import TypedDict from  typing_extensions import  TypedDict from operator import add from  operator import  add class State(TypedDict): class  State(TypedDict): foo: str foo: str bar: Annotated[list[str], add] bar: Annotated[list[str], add] def node_a(state: State): def  node_a(state: State): return {"foo": "a", "bar": ["a"]}  return {"foo": "a", "bar": ["a"]} def node_b(state: State): def  node_b(state: State): return {"foo": "b", "bar": ["b"]}  return {"foo": "b", "bar": ["b"]} workflow = StateGraph(State) workflow = StateGraph(State)workflow.add_node(node_a)workflow.add_node(node_a)workflow.add_node(node_b)workflow.add_node(node_b)workflow.add_edge(START, "node_a")workflow.add_edge(START, "node_a")workflow.add_edge("node_a", "node_b")workflow.add_edge("node_a", "node_b")workflow.add_edge("node_b", END)workflow.add_edge("node_b", END) checkpointer = InMemorySaver() checkpointer = InMemorySaver()graph = workflow.compile(checkpointer=checkpointer) graph = workflow.compile(checkpointer =checkpointer) config: RunnableConfig = {"configurable": {"thread_id": "1"}}config: RunnableConfig = {"configurable": {"thread_id": "1"}}graph.invoke({"foo": ""}, config)graph.invoke({"foo": ""}, config)
```

After we run the graph, we expect to see exactly 4 checkpoints:

* Empty checkpoint with [`START`](https://reference.langchain.com/python/langgraph/constants/#langgraph.constants.START) as the next node to be executed
* Checkpoint with the user input `{'foo': '', 'bar': []}` and `node_a` as the next node to be executed
* Checkpoint with the outputs of `node_a` `{'foo': 'a', 'bar': ['a']}` and `node_b` as the next node to be executed
* Checkpoint with the outputs of `node_b` `{'foo': 'b', 'bar': ['a', 'b']}` and no next nodes to be executed

Note that we `bar` channel values contain outputs from both nodes as we have a reducer for `bar` channel.

### [​](#get-state) Get state

When interacting with the saved graph state, you **must** specify a [thread identifier](#threads). You can view the *latest* state of the graph by calling `graph.get_state(config)`. This will return a `StateSnapshot` object that corresponds to the latest checkpoint associated with the thread ID provided in the config or a checkpoint associated with a checkpoint ID for the thread, if provided.

Copy

Ask AI

```
# get the latest state snapshot # get the latest state snapshotconfig = {"configurable": {"thread_id": "1"}} config = {"configurable": {"thread_id": "1"}}graph.get_state(config)graph.get_state(config) # get a state snapshot for a specific checkpoint_id # get a state snapshot for a specific checkpoint_idconfig = {"configurable": {"thread_id": "1", "checkpoint_id": "1ef663ba-28fe-6528-8002-5a559208592c"}} config = {"configurable": {"thread_id": "1", "checkpoint_id": "1ef663ba-28fe-6528-8002-5a559208592c"}}graph.get_state(config)graph.get_state(config)
```

In our example, the output of `get_state` will look like this:

Copy

Ask AI

```
StateSnapshot(StateSnapshot( values={'foo': 'b', 'bar': ['a', 'b']}, values={'foo': 'b', 'bar': ['a', 'b']}, next=(), next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28fe-6528-8002-5a559208592c'}}, config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28fe-6528-8002-5a559208592c'}}, metadata={'source': 'loop', 'writes': {'node_b': {'foo': 'b', 'bar': ['b']}}, 'step': 2}, metadata={'source': 'loop', 'writes': {'node_b': {'foo': 'b', 'bar': ['b']}}, 'step': 2}, created_at='2024-08-29T19:19:38.821749+00:00', created_at='2024-08-29T19:19:38.821749+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, tasks=() parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, tasks=())) 
```

### [​](#get-state-history) Get state history

You can get the full history of the graph execution for a given thread by calling [`graph.get_state_history(config)`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.get_state_history). This will return a list of `StateSnapshot` objects associated with the thread ID provided in the config. Importantly, the checkpoints will be ordered chronologically with the most recent checkpoint / `StateSnapshot` being the first in the list.

Copy

Ask AI

```
config = {"configurable": {"thread_id": "1"}} config = {"configurable": {"thread_id": "1"}}list(graph.get_state_history(config)) list(graph.get_state_history(config))
```

In our example, the output of [`get_state_history`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.get_state_history) will look like this:

Copy

Ask AI

```
[[ StateSnapshot( StateSnapshot( values={'foo': 'b', 'bar': ['a', 'b']}, values={'foo': 'b', 'bar': ['a', 'b']}, next=(), next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28fe-6528-8002-5a559208592c'}}, config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28fe-6528-8002-5a559208592c'}}, metadata={'source': 'loop', 'writes': {'node_b': {'foo': 'b', 'bar': ['b']}}, 'step': 2}, metadata={'source': 'loop', 'writes': {'node_b': {'foo': 'b', 'bar': ['b']}}, 'step': 2}, created_at='2024-08-29T19:19:38.821749+00:00', created_at='2024-08-29T19:19:38.821749+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, tasks=(), tasks=(), ), ), StateSnapshot( StateSnapshot( values={'foo': 'a', 'bar': ['a']}, values={'foo': 'a', 'bar': ['a']}, next=('node_b',), next=('node_b',), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, metadata={'source': 'loop', 'writes': {'node_a': {'foo': 'a', 'bar': ['a']}}, 'step': 1}, metadata={'source': 'loop', 'writes': {'node_a': {'foo': 'a', 'bar': ['a']}}, 'step': 1}, created_at='2024-08-29T19:19:38.819946+00:00', created_at='2024-08-29T19:19:38.819946+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f4-6b4a-8000-ca575a13d36a'}}, parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f4-6b4a-8000-ca575a13d36a'}}, tasks=(PregelTask(id='6fb7314f-f114-5413-a1f3-d37dfe98ff44', name='node_b', error=None, interrupts=()),), tasks=(PregelTask(id='6fb7314f-f114-5413-a1f3-d37dfe98ff44', name='node_b', error=None, interrupts=()),), ), ), StateSnapshot( StateSnapshot( values={'foo': '', 'bar': []}, values={'foo': '', 'bar': []}, next=('node_a',), next=('node_a',), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f4-6b4a-8000-ca575a13d36a'}}, config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f4-6b4a-8000-ca575a13d36a'}}, metadata={'source': 'loop', 'writes': None, 'step': 0}, metadata={'source': 'loop', 'writes': None, 'step': 0}, created_at='2024-08-29T19:19:38.817813+00:00', created_at='2024-08-29T19:19:38.817813+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f0-6c66-bfff-6723431e8481'}}, parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f0-6c66-bfff-6723431e8481'}}, tasks=(PregelTask(id='f1b14528-5ee5-579c-949b-23ef9bfbed58', name='node_a', error=None, interrupts=()),), tasks=(PregelTask(id='f1b14528-5ee5-579c-949b-23ef9bfbed58', name='node_a', error=None, interrupts=()),), ), ), StateSnapshot( StateSnapshot( values={'bar': []}, values={'bar': []}, next=('__start__',), next=('__start__',), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f0-6c66-bfff-6723431e8481'}}, config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f0-6c66-bfff-6723431e8481'}}, metadata={'source': 'input', 'writes': {'foo': ''}, 'step': -1}, metadata={'source': 'input', 'writes': {'foo': ''}, 'step': -1}, created_at='2024-08-29T19:19:38.816205+00:00', created_at='2024-08-29T19:19:38.816205+00:00', parent_config=None, parent_config=None, tasks=(PregelTask(id='6d27aa2e-d72b-5504-a36f-8620e54a76dd', name='__start__', error=None, interrupts=()),), tasks=(PregelTask(id='6d27aa2e-d72b-5504-a36f-8620e54a76dd', name='__start__', error=None, interrupts=()),), ) )]] 
```

### [​](#replay) Replay

It’s also possible to play-back a prior graph execution. If we `invoke` a graph with a `thread_id` and a `checkpoint_id`, then we will *re-play* the previously executed steps *before* a checkpoint that corresponds to the `checkpoint_id`, and only execute the steps *after* the checkpoint.

* `thread_id` is the ID of a thread.
* `checkpoint_id` is an identifier that refers to a specific checkpoint within a thread.

You must pass these when invoking the graph as part of the `configurable` portion of the config:

Copy

Ask AI

```
config = {"configurable": {"thread_id": "1", "checkpoint_id": "0c62ca34-ac19-445d-bbb0-5b4984975b2a"}} config = {"configurable": {"thread_id": "1", "checkpoint_id": "0c62ca34-ac19-445d-bbb0-5b4984975b2a"}}graph.invoke(None, config=config)graph.invoke(None, config =config)
```

Importantly, LangGraph knows whether a particular step has been executed previously. If it has, LangGraph simply *re-plays* that particular step in the graph and does not re-execute the step, but only for the steps *before* the provided `checkpoint_id`. All of the steps *after* `checkpoint_id` will be executed (i.e., a new fork), even if they have been executed previously. See this [how to guide on time-travel to learn more about replaying](/oss/python/langgraph/use-time-travel). 

### [​](#update-state) Update state

In addition to re-playing the graph from specific `checkpoints`, we can also *edit* the graph state. We do this using [`update_state`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.update_state). This method accepts three different arguments:

#### [​](#config) `config`

The config should contain `thread_id` specifying which thread to update. When only the `thread_id` is passed, we update (or fork) the current state. Optionally, if we include `checkpoint_id` field, then we fork that selected checkpoint.

#### [​](#values) `values`

These are the values that will be used to update the state. Note that this update is treated exactly as any update from a node is treated. This means that these values will be passed to the [reducer](/oss/python/langgraph/graph-api#reducers) functions, if they are defined for some of the channels in the graph state. This means that [`update_state`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.update_state) does NOT automatically overwrite the channel values for every channel, but only for the channels without reducers. Let’s walk through an example. Let’s assume you have defined the state of your graph with the following schema (see full example above):

Copy

Ask AI

```
from typing import Annotated from  typing import  Annotated from typing_extensions import TypedDict from  typing_extensions import  TypedDict from operator import add from  operator import  add class State(TypedDict): class  State(TypedDict): foo: int foo: int bar: Annotated[list[str], add] bar: Annotated[list[str], add]
```

Let’s now assume the current state of the graph is

Copy

Ask AI

```
{"foo": 1, "bar": ["a"]}{"foo": 1, "bar": ["a"]} 
```

If you update the state as below:

Copy

Ask AI

```
graph.update_state(config, {"foo": 2, "bar": ["b"]})graph.update_state(config, {"foo": 2, "bar": ["b"]})
```

Then the new state of the graph will be:

Copy

Ask AI

```
{"foo": 2, "bar": ["a", "b"]}{"foo": 2, "bar": ["a", "b"]} 
```

The `foo` key (channel) is completely changed (because there is no reducer specified for that channel, so [`update_state`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.update_state) overwrites it). However, there is a reducer specified for the `bar` key, and so it appends `"b"` to the state of `bar`.

#### [​](#as-node) `as_node`

The final thing you can optionally specify when calling [`update_state`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.update_state) is `as_node`. If you provided it, the update will be applied as if it came from node `as_node`. If `as_node` is not provided, it will be set to the last node that updated the state, if not ambiguous. The reason this matters is that the next steps to execute depend on the last node to have given an update, so this can be used to control which node executes next. See this [how to guide on time-travel to learn more about forking state](/oss/python/langgraph/use-time-travel). 

## [​](#memory-store) Memory Store

 A [state schema](/oss/python/langgraph/graph-api#schema) specifies a set of keys that are populated as a graph is executed. As discussed above, state can be written by a checkpointer to a thread at each graph step, enabling state persistence. But, what if we want to retain some information *across threads*? Consider the case of a chatbot where we want to retain specific information about the user across *all* chat conversations (e.g., threads) with that user! With checkpointers alone, we cannot share information across threads. This motivates the need for the [`Store`](https://python.langchain.com/api_reference/langgraph/index.html#module-langgraph.store) interface. As an illustration, we can define an `InMemoryStore` to store information about a user across threads. We simply compile our graph with a checkpointer, as before, and with our new `in_memory_store` variable.

**LangGraph API handles stores automatically** When using the LangGraph API, you don’t need to implement or configure stores manually. The API handles all storage infrastructure for you behind the scenes.

### [​](#basic-usage) Basic Usage

First, let’s showcase this in isolation without using LangGraph.

Copy

Ask AI

```
from langgraph.store.memory import InMemoryStore from langgraph.store.memory import  InMemoryStorein_memory_store = InMemoryStore() in_memory_store = InMemoryStore()
```

Memories are namespaced by a `tuple`, which in this specific example will be `(, "memories")`. The namespace can be any length and represent anything, does not have to be user specific.

Copy

Ask AI

```
user_id = "1" user_id =  "1"namespace_for_memory = (user_id, "memories") namespace_for_memory = (user_id, "memories")
```

We use the `store.put` method to save memories to our namespace in the store. When we do this, we specify the namespace, as defined above, and a key-value pair for the memory: the key is simply a unique identifier for the memory (`memory_id`) and the value (a dictionary) is the memory itself.

Copy

Ask AI

```
memory_id = str(uuid.uuid4()) memory_id =  str(uuid.uuid4())memory = {"food_preference" : "I like pizza"} memory = {"food_preference" : "I like pizza"}in_memory_store.put(namespace_for_memory, memory_id, memory)in_memory_store.put(namespace_for_memory, memory_id, memory)
```

We can read out memories in our namespace using the `store.search` method, which will return all memories for a given user as a list. The most recent memory is the last in the list.

Copy

Ask AI

```
memories = in_memory_store.search(namespace_for_memory) memories = in_memory_store.search(namespace_for_memory)memories[-1].dict()memories[- 1].dict(){'value': {'food_preference': 'I like pizza'},{'value': {'food_preference': 'I like pizza'}, 'key': '07e0caf4-1631-47b7-b15f-65515d4c1843',  'key': '07e0caf4-1631-47b7-b15f-65515d4c1843', 'namespace': ['1', 'memories'],  'namespace': ['1', 'memories'], 'created_at': '2024-10-02T17:22:31.590602+00:00',  'created_at': '2024-10-02T17:22:31.590602+00:00', 'updated_at': '2024-10-02T17:22:31.590605+00:00'}  'updated_at': '2024-10-02T17:22:31.590605+00:00'}
```

Each memory type is a Python class ([`Item`](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.base.Item)) with certain attributes. We can access it as a dictionary by converting via `.dict` as above. The attributes it has are:

* `value`: The value (itself a dictionary) of this memory
* `key`: A unique key for this memory in this namespace
* `namespace`: A list of strings, the namespace of this memory type
* `created_at`: Timestamp for when this memory was created
* `updated_at`: Timestamp for when this memory was updated

### [​](#semantic-search) Semantic Search

Beyond simple retrieval, the store also supports semantic search, allowing you to find memories based on meaning rather than exact matches. To enable this, configure the store with an embedding model:

Copy

Ask AI

```
from langchain.embeddings import init_embeddings from langchain.embeddings import  init_embeddings store = InMemoryStore(store = InMemoryStore( index={ index ={ "embed": init_embeddings("openai:text-embedding-3-small"), # Embedding provider  "embed": init_embeddings("openai:text-embedding-3-small"), # Embedding provider "dims": 1536, # Embedding dimensions  "dims": 1536, # Embedding dimensions "fields": ["food_preference", "$"] # Fields to embed  "fields": ["food_preference", "$"] # Fields to embed } }))
```

Now when searching, you can use natural language queries to find relevant memories:

Copy

Ask AI

```
# Find memories about food preferences # Find memories about food preferences# (This can be done after putting memories into the store)# (This can be done after putting memories into the store)memories = store.search(memories = store.search( namespace_for_memory, namespace_for_memory, query="What does the user like to eat?",  query = "What does the user like to eat?", limit=3 # Return top 3 matches  limit = 3  # Return top 3 matches))
```

You can control which parts of your memories get embedded by configuring the `fields` parameter or by specifying the `index` parameter when storing memories:

Copy

Ask AI

```
# Store with specific fields to embed # Store with specific fields to embedstore.put(store.put( namespace_for_memory, namespace_for_memory, str(uuid.uuid4()),  str(uuid.uuid4()), { { "food_preference": "I love Italian cuisine",  "food_preference": "I love Italian cuisine", "context": "Discussing dinner plans"  "context": "Discussing dinner plans" }, }, index=["food_preference"] # Only embed "food_preferences" field  index =["food_preference"] # Only embed "food_preferences" field)) # Store without embedding (still retrievable, but not searchable)# Store without embedding (still retrievable, but not searchable)store.put(store.put( namespace_for_memory, namespace_for_memory, str(uuid.uuid4()),  str(uuid.uuid4()), {"system_info": "Last updated: 2024-01-01"}, {"system_info": "Last updated: 2024-01-01"}, index=False  index = False))
```

### [​](#using-in-langgraph) Using in LangGraph

With this all in place, we use the `in_memory_store` in LangGraph. The `in_memory_store` works hand-in-hand with the checkpointer: the checkpointer saves state to threads, as discussed above, and the `in_memory_store` allows us to store arbitrary information for access *across* threads. We compile the graph with both the checkpointer and the `in_memory_store` as follows.

Copy

Ask AI

```
from langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaver # We need this because we want to enable threads (conversations)# We need this because we want to enable threads (conversations)checkpointer = InMemorySaver() checkpointer = InMemorySaver() # ... Define the graph ...# ... Define the graph ... # Compile the graph with the checkpointer and store # Compile the graph with the checkpointer and storegraph = graph.compile(checkpointer=checkpointer, store=in_memory_store) graph = graph.compile(checkpointer =checkpointer, store =in_memory_store)
```

We invoke the graph with a `thread_id`, as before, and also with a `user_id`, which we’ll use to namespace our memories to this particular user as we showed above.

Copy

Ask AI

```
# Invoke the graph # Invoke the graphuser_id = "1" user_id =  "1"config = {"configurable": {"thread_id": "1", "user_id": user_id}} config = {"configurable": {"thread_id": "1", "user_id": user_id}} # First let's just say hi to the AI # First let's just say hi to the AIfor update in graph.stream(for  update in graph.stream( {"messages": [{"role": "user", "content": "hi"}]}, config, stream_mode="updates" {"messages": [{"role": "user", "content": "hi"}]}, config, stream_mode = "updates"):): print(update)  print(update)
```

We can access the `in_memory_store` and the `user_id` in *any node* by passing `store: BaseStore` and `config: RunnableConfig` as node arguments. Here’s how we might use semantic search in a node to find relevant memories:

Copy

Ask AI

```
def update_memory(state: MessagesState, config: RunnableConfig, *, store: BaseStore): def  update_memory(state: MessagesState, config: RunnableConfig, *, store: BaseStore):  # Get the user id from the config  # Get the user id from the config user_id = config["configurable"]["user_id"]  user_id = config["configurable"]["user_id"]  # Namespace the memory  # Namespace the memory namespace = (user_id, "memories")  namespace = (user_id, "memories")  # ... Analyze conversation and create a new memory # ... Analyze conversation and create a new memory  # Create a new memory ID  # Create a new memory ID memory_id = str(uuid.uuid4())  memory_id =  str(uuid.uuid4())  # We create a new memory  # We create a new memory store.put(namespace, memory_id, {"memory": memory}) store.put(namespace, memory_id, {"memory": memory}) 
```

As we showed above, we can also access the store in any node and use the `store.search` method to get memories. Recall the memories are returned as a list of objects that can be converted to a dictionary.

Copy

Ask AI

```
memories[-1].dict()memories[- 1].dict(){'value': {'food_preference': 'I like pizza'},{'value': {'food_preference': 'I like pizza'}, 'key': '07e0caf4-1631-47b7-b15f-65515d4c1843',  'key': '07e0caf4-1631-47b7-b15f-65515d4c1843', 'namespace': ['1', 'memories'],  'namespace': ['1', 'memories'], 'created_at': '2024-10-02T17:22:31.590602+00:00',  'created_at': '2024-10-02T17:22:31.590602+00:00', 'updated_at': '2024-10-02T17:22:31.590605+00:00'}  'updated_at': '2024-10-02T17:22:31.590605+00:00'}
```

We can access the memories and use them in our model call.

Copy

Ask AI

```
def call_model(state: MessagesState, config: RunnableConfig, *, store: BaseStore): def  call_model(state: MessagesState, config: RunnableConfig, *, store: BaseStore):  # Get the user id from the config  # Get the user id from the config user_id = config["configurable"]["user_id"]  user_id = config["configurable"]["user_id"]  # Namespace the memory  # Namespace the memory namespace = (user_id, "memories")  namespace = (user_id, "memories")  # Search based on the most recent message  # Search based on the most recent message memories = store.search( memories = store.search( namespace, namespace, query=state["messages"][-1].content,  query =state["messages"][- 1].content, limit=3  limit = 3 ) ) info = "\n".join([d.value["memory"] for d in memories])  info =  " \n ".join([d.value["memory"] for  d in memories])  # ... Use memories in the model call # ... Use memories in the model call
```

If we create a new thread, we can still access the same memories so long as the `user_id` is the same.

Copy

Ask AI

```
# Invoke the graph # Invoke the graphconfig = {"configurable": {"thread_id": "2", "user_id": "1"}} config = {"configurable": {"thread_id": "2", "user_id": "1"}} # Let's say hi again # Let's say hi againfor update in graph.stream(for  update in graph.stream( {"messages": [{"role": "user", "content": "hi, tell me about my memories"}]}, config, stream_mode="updates" {"messages": [{"role": "user", "content": "hi, tell me about my memories"}]}, config, stream_mode = "updates"):): print(update)  print(update)
```

When we use the LangSmith, either locally (e.g., in [Studio](/langsmith/studio)) or [hosted with LangSmith](/langsmith/platform-setup), the base store is available to use by default and does not need to be specified during graph compilation. To enable semantic search, however, you **do** need to configure the indexing settings in your `langgraph.json` file. For example:

Copy

Ask AI

```
{{ ... ... "store": { "store": { "index": { "index": { "embed": "openai:text-embeddings-3-small",  "embed": "openai:text-embeddings-3-small", "dims": 1536,  "dims": 1536, "fields": ["$"]  "fields": ["$"] } } } }}}
```

See the [deployment guide](/langsmith/semantic-search) for more details and configuration options.

## [​](#checkpointer-libraries) Checkpointer libraries

Under the hood, checkpointing is powered by checkpointer objects that conform to [`BaseCheckpointSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.base.BaseCheckpointSaver) interface. LangGraph provides several checkpointer implementations, all implemented via standalone, installable libraries:

* `langgraph-checkpoint`: The base interface for checkpointer savers ([`BaseCheckpointSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.base.BaseCheckpointSaver)) and serialization/deserialization interface ([`SerializerProtocol`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.base.SerializerProtocol)). Includes in-memory checkpointer implementation ([`InMemorySaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.memory.InMemorySaver)) for experimentation. LangGraph comes with `langgraph-checkpoint` included.
* `langgraph-checkpoint-sqlite`: An implementation of LangGraph checkpointer that uses SQLite database ([`SqliteSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.sqlite.SqliteSaver) / [`AsyncSqliteSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.sqlite.aio.AsyncSqliteSaver)). Ideal for experimentation and local workflows. Needs to be installed separately.
* `langgraph-checkpoint-postgres`: An advanced checkpointer that uses Postgres database ([`PostgresSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.postgres.PostgresSaver) / [`AsyncPostgresSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.postgres.aio.AsyncPostgresSaver)), used in LangSmith. Ideal for using in production. Needs to be installed separately.

### [​](#checkpointer-interface) Checkpointer interface

Each checkpointer conforms to [`BaseCheckpointSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.base.BaseCheckpointSaver) interface and implements the following methods:

* `.put` - Store a checkpoint with its configuration and metadata.
* `.put_writes` - Store intermediate writes linked to a checkpoint (i.e. [pending writes](#pending-writes)).
* `.get_tuple` - Fetch a checkpoint tuple using for a given configuration (`thread_id` and `checkpoint_id`). This is used to populate `StateSnapshot` in `graph.get_state()`.
* `.list` - List checkpoints that match a given configuration and filter criteria. This is used to populate state history in `graph.get_state_history()`

If the checkpointer is used with asynchronous graph execution (i.e. executing the graph via `.ainvoke`, `.astream`, `.abatch`), asynchronous versions of the above methods will be used (`.aput`, `.aput_writes`, `.aget_tuple`, `.alist`).

For running your graph asynchronously, you can use [`InMemorySaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.memory.InMemorySaver), or async versions of Sqlite/Postgres checkpointers — [`AsyncSqliteSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.sqlite.aio.AsyncSqliteSaver) / [`AsyncPostgresSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.postgres.aio.AsyncPostgresSaver) checkpointers.

### [​](#serializer) Serializer

When checkpointers save the graph state, they need to serialize the channel values in the state. This is done using serializer objects. `langgraph_checkpoint` defines [protocol](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.base.SerializerProtocol) for implementing serializers provides a default implementation ([`JsonPlusSerializer`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.jsonplus.JsonPlusSerializer)) that handles a wide variety of types, including LangChain and LangGraph primitives, datetimes, enums and more.

#### [​](#serialization-with-pickle) Serialization with `pickle`

The default serializer, [`JsonPlusSerializer`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.jsonplus.JsonPlusSerializer), uses ormsgpack and JSON under the hood, which is not suitable for all types of objects. If you want to fallback to pickle for objects not currently supported by our msgpack encoder (such as Pandas dataframes), you can use the `pickle_fallback` argument of the [`JsonPlusSerializer`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.jsonplus.JsonPlusSerializer):

Copy

Ask AI

```
from langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaverfrom langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer from langgraph.checkpoint.serde.jsonplus import  JsonPlusSerializer # ... Define the graph ...# ... Define the graph ...graph.compile(graph.compile( checkpointer=InMemorySaver(serde=JsonPlusSerializer(pickle_fallback=True))  checkpointer =InMemorySaver(serde =JsonPlusSerializer(pickle_fallback = True))))
```

#### [​](#encryption) Encryption

Checkpointers can optionally encrypt all persisted state. To enable this, pass an instance of [`EncryptedSerializer`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.encrypted.EncryptedSerializer) to the `serde` argument of any [`BaseCheckpointSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.base.BaseCheckpointSaver) implementation. The easiest way to create an encrypted serializer is via [`from_pycryptodome_aes`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.encrypted.EncryptedSerializer.from_pycryptodome_aes), which reads the AES key from the `LANGGRAPH_AES_KEY` environment variable (or accepts a `key` argument):

Copy

Ask AI

```
import sqlite3 import  sqlite3 from langgraph.checkpoint.serde.encrypted import EncryptedSerializer from langgraph.checkpoint.serde.encrypted import  EncryptedSerializerfrom langgraph.checkpoint.sqlite import SqliteSaver from langgraph.checkpoint.sqlite import  SqliteSaver serde = EncryptedSerializer.from_pycryptodome_aes() # reads LANGGRAPH_AES_KEY serde = EncryptedSerializer.from_pycryptodome_aes() # reads LANGGRAPH_AES_KEYcheckpointer = SqliteSaver(sqlite3.connect("checkpoint.db"), serde=serde) checkpointer = SqliteSaver(sqlite3.connect("checkpoint.db"), serde =serde)
```

Copy

Ask AI

```
from langgraph.checkpoint.serde.encrypted import EncryptedSerializer from langgraph.checkpoint.serde.encrypted import  EncryptedSerializerfrom langgraph.checkpoint.postgres import PostgresSaver from langgraph.checkpoint.postgres import  PostgresSaver serde = EncryptedSerializer.from_pycryptodome_aes() serde = EncryptedSerializer.from_pycryptodome_aes()checkpointer = PostgresSaver.from_conn_string("postgresql://...", serde=serde) checkpointer = PostgresSaver.from_conn_string("postgresql://...", serde =serde)checkpointer.setup()checkpointer.setup()
```

When running on LangSmith, encryption is automatically enabled whenever `LANGGRAPH_AES_KEY` is present, so you only need to provide the environment variable. Other encryption schemes can be used by implementing [`CipherProtocol`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.base.CipherProtocol) and supplying it to [`EncryptedSerializer`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.serde.encrypted.EncryptedSerializer).

## [​](#capabilities) Capabilities

### [​](#human-in-the-loop) Human-in-the-loop

First, checkpointers facilitate [human-in-the-loop workflows](/oss/python/langgraph/interrupts) workflows by allowing humans to inspect, interrupt, and approve graph steps. Checkpointers are needed for these workflows as the human has to be able to view the state of a graph at any point in time, and the graph has to be to resume execution after the human has made any updates to the state. See [the how-to guides](/oss/python/langgraph/interrupts) for examples.

### [​](#memory) Memory

Second, checkpointers allow for [“memory”](/oss/python/concepts/memory) between interactions. In the case of repeated human interactions (like conversations) any follow up messages can be sent to that thread, which will retain its memory of previous ones. See [Add memory](/oss/python/langgraph/add-memory) for information on how to add and manage conversation memory using checkpointers.

### [​](#time-travel) Time Travel

Third, checkpointers allow for [“time travel”](/oss/python/langgraph/use-time-travel), allowing users to replay prior graph executions to review and / or debug specific graph steps. In addition, checkpointers make it possible to fork the graph state at arbitrary checkpoints to explore alternative trajectories.

### [​](#fault-tolerance) Fault-tolerance

Lastly, checkpointing also provides fault-tolerance and error recovery: if one or more nodes fail at a given superstep, you can restart your graph from the last successful step. Additionally, when a graph node fails mid-execution at a given superstep, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that superstep, so that whenever we resume graph execution from that superstep we don’t re-run the successful nodes.

#### [​](#pending-writes) Pending writes

Additionally, when a graph node fails mid-execution at a given superstep, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that superstep, so that whenever we resume graph execution from that superstep we don’t re-run the successful nodes. 

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/persistence.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Workflows and agents](/oss/python/langgraph/workflows-agents)[Durable execution](/oss/python/langgraph/durable-execution)