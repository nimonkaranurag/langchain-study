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

* [Overview](#overview)
* [Memory storage](#memory-storage)
* [Read long-term memory in tools](#read-long-term-memory-in-tools)
* [Write long-term memory from tools](#write-long-term-memory-from-tools)

[Advanced usage](/oss/python/langchain/guardrails)

# Long-term memory

## [​](#overview) Overview

LangChain agents use [LangGraph persistence](/oss/python/langgraph/persistence#memory-store) to enable long-term memory. This is a more advanced topic and requires knowledge of LangGraph to use.

## [​](#memory-storage) Memory storage

LangGraph stores long-term memories as JSON documents in a [store](/oss/python/langgraph/persistence#memory-store). Each memory is organized under a custom `namespace` (similar to a folder) and a distinct `key` (like a file name). Namespaces often include user or org IDs or other labels that makes it easier to organize information. This structure enables hierarchical organization of memories. Cross-namespace searching is then supported through content filters.

Copy

Ask AI

```
from langgraph.store.memory import InMemoryStore from langgraph.store.memory import  InMemoryStore def embed(texts: list[str]) -> list[list[float]]: def  embed(texts: list[str]) -> list[list[float]]:  # Replace with an actual embedding function or LangChain embeddings object  # Replace with an actual embedding function or LangChain embeddings object return [[1.0, 2.0] * len(texts)]  return [[1.0, 2.0] *  len(texts)] # InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use.# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production use.store = InMemoryStore(index={"embed": embed, "dims": 2}) store = InMemoryStore(index ={"embed": embed, "dims": 2}) user_id = "my-user" user_id = "my-user"application_context = "chitchat" application_context =  "chitchat"namespace = (user_id, application_context) namespace = (user_id, application_context) store.put( store.put(  namespace, namespace, "a-memory", "a-memory", { { "rules": [ "rules": [ "User likes short, direct language", "User likes short, direct language", "User only speaks English & python",  "User only speaks English & python", ], ], "my-key": "my-value", "my-key": "my-value", }, },)) # get the "memory" by ID # get the "memory" by IDitem = store.get(namespace, "a-memory") item = store.get(namespace, "a-memory") # search for "memories" within this namespace, filtering on content equivalence, sorted by vector similarity# search for "memories" within this namespace, filtering on content equivalence, sorted by vector similarityitems = store.search( items = store.search(  namespace, filter={"my-key": "my-value"}, query="language preferences" namespace, filter ={"my-key": "my-value"}, query = "language preferences"))
```

For more information about the memory store, see the [Persistence](/oss/python/langgraph/persistence#memory-store) guide.

## [​](#read-long-term-memory-in-tools) Read long-term memory in tools

A tool the agent can use to look up user information

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclass from langchain_core.runnables import RunnableConfig from langchain_core.runnables import  RunnableConfigfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.tools import tool, ToolRuntime from langchain.tools import tool, ToolRuntimefrom langgraph.store.memory import InMemoryStore from langgraph.store.memory import  InMemoryStore  @dataclass @dataclassclass Context: class  Context: user_id: str user_id: str # InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.store = InMemoryStore() store = InMemoryStore()  # Write sample data to the store using the put method # Write sample data to the store using the put methodstore.put( store.put(  ("users",), # Namespace to group related data together (users namespace for user data) ("users",), # Namespace to group related data together (users namespace for user data) "user_123", # Key within the namespace (user ID as key)  "user_123", # Key within the namespace (user ID as key) { { "name": "John Smith",  "name": "John Smith", "language": "English",  "language": "English", } # Data to store for the given user } # Data to store for the given user)) @tool @tooldef get_user_info(runtime: ToolRuntime[Context]) -> str: def  get_user_info(runtime: ToolRuntime[Context]) -> str: """Look up user info.""" """Look up user info.""" # Access the store - same as that provided to `create_agent` # Access the store - same as that provided to `create_agent` store = runtime.store  store = runtime.store  user_id = runtime.context.user_id  user_id = runtime.context.user_id # Retrieve data from store - returns StoreValue object with value and metadata # Retrieve data from store - returns StoreValue object with value and metadata user_info = store.get(("users",), user_id)  user_info = store.get(("users",), user_id)  return str(user_info.value) if user_info else "Unknown user"  return  str(user_info.value) if  user_info else  "Unknown user" agent = create_agent(agent = create_agent( model="claude-sonnet-4-5-20250929",  model ="claude-sonnet-4-5-20250929", tools=[get_user_info],  tools =[get_user_info], # Pass store to agent - enables agent to access store when running tools # Pass store to agent - enables agent to access store when running tools store=store,  store =store,  context_schema=Context  context_schema = Context)) # Run the agent # Run the agentagent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "look up user information"}]}, {"messages": [{"role": "user", "content": "look up user information"}]}, context=Context(user_id="user_123")  context =Context(user_id = "user_123") ))
```

## [​](#write-long-term-memory-from-tools) Write long-term memory from tools

Example of a tool that updates user information

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclass from typing_extensions import TypedDict from  typing_extensions import  TypedDict from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.tools import tool, ToolRuntime from langchain.tools import tool, ToolRuntimefrom langgraph.store.memory import InMemoryStore from langgraph.store.memory import  InMemoryStore # InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.# InMemoryStore saves data to an in-memory dictionary. Use a DB-backed store in production.store = InMemoryStore() store = InMemoryStore()  @dataclass @dataclassclass Context: class  Context: user_id: str user_id: str # TypedDict defines the structure of user information for the LLM # TypedDict defines the structure of user information for the LLMclass UserInfo(TypedDict): class  UserInfo(TypedDict): name: str name: str # Tool that allows agent to update user information (useful for chat applications)# Tool that allows agent to update user information (useful for chat applications) @tool @tooldef save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str: def  save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str: """Save user info.""" """Save user info.""" # Access the store - same as that provided to `create_agent` # Access the store - same as that provided to `create_agent` store = runtime.store  store = runtime.store  user_id = runtime.context.user_id  user_id = runtime.context.user_id  # Store data in the store (namespace, key, data) # Store data in the store (namespace, key, data) store.put(("users",), user_id, user_info)  store.put(("users",), user_id, user_info)  return "Successfully saved user info."  return "Successfully saved user info." agent = create_agent(agent = create_agent( model="claude-sonnet-4-5-20250929",  model ="claude-sonnet-4-5-20250929", tools=[save_user_info],  tools =[save_user_info], store=store,  store =store,  context_schema=Context  context_schema = Context)) # Run the agent # Run the agentagent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "My name is John Smith"}]}, {"messages": [{"role": "user", "content": "My name is John Smith"}]},  # user_id passed in context to identify whose information is being updated  # user_id passed in context to identify whose information is being updated context=Context(user_id="user_123")  context =Context(user_id = "user_123") )) # You can access the store directly to get the value # You can access the store directly to get the valuestore.get(("users",), "user_123").valuestore.get(("users",), "user_123").value
```

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/long-term-memory.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Retrieval](/oss/python/langchain/retrieval)[Studio](/oss/python/langchain/studio)