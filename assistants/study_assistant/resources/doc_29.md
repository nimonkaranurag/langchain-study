We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

* [Learn](/oss/python/learn)

##### Tutorials

##### Conceptual overviews

* [Memory](/oss/python/concepts/memory)
* [Context](/oss/python/concepts/context)
* [Graph API](/oss/python/langgraph/graph-api)
* [Functional API](/oss/python/langgraph/functional-api)

##### Additional resources

* [LangChain Academy](https://academy.langchain.com/)
* [Case studies](/oss/python/langgraph/case-studies)

* [Static runtime context](#static-runtime-context)
* [Dynamic runtime context](#dynamic-runtime-context)
* [Dynamic cross-conversation context](#dynamic-cross-conversation-context)
* [See also](#see-also)

[Conceptual overviews](/oss/python/concepts/memory)

# Context overview

**Context engineering** is the practice of building dynamic systems that provide the right information and tools, in the right format, so that an AI application can accomplish a task. Context can be characterized along two key dimensions:

1. By **mutability**:

* **Static context**: Immutable data that doesn’t change during execution (e.g., user metadata, database connections, tools)
* **Dynamic context**: Mutable data that evolves as the application runs (e.g., conversation history, intermediate results, tool call observations)

1. By **lifetime**:

* **Runtime context**: Data scoped to a single run or invocation
* **Cross-conversation context**: Data that persists across multiple conversations or sessions

Runtime context refers to local context: data and dependencies your code needs to run. It does **not** refer to:

* The LLM context, which is the data passed into the LLM’s prompt.
* The “context window”, which is the maximum number of tokens that can be passed to the LLM.

Runtime context is a form of dependency injection and can be used to optimize the LLM context. It lets to provide dependencies (like database connections, user IDs, or API clients) to your tools and nodes at runtime rather than hardcoding them. For example, you can use user metadata in the runtime context to fetch user preferences and feed them into the context window.

LangGraph provides three ways to manage context, which combines the mutability and lifetime dimensions:

| Context type | Description | Mutability | Lifetime | Access method |
| --- | --- | --- | --- | --- |
| [**Static runtime context**](#static-runtime-context) | User metadata, tools, db connections passed at startup | Static | Single run | `context` argument to `invoke`/`stream` |
| [**Dynamic runtime context (state)**](#dynamic-runtime-context-state) | Mutable data that evolves during a single run | Dynamic | Single run | LangGraph state object |
| [**Dynamic cross-conversation context (store)**](#dynamic-cross-conversation-context-store) | Persistent data shared across conversations | Dynamic | Cross-conversation | LangGraph store |

## [​](#static-runtime-context) Static runtime context

**Static runtime context** represents immutable data like user metadata, tools, and database connections that are passed to an application at the start of a run via the `context` argument to `invoke`/`stream`. This data does not change during execution.

Copy

Ask AI

```
@dataclass @dataclassclass ContextSchema: class  ContextSchema: user_name: str user_name: str graph.invoke(graph.invoke( {"messages": [{"role": "user", "content": "hi!"}]}, {"messages": [{"role": "user", "content": "hi!"}]}, context={"user_name": "John Smith"}  context ={"user_name": "John Smith"} ))
```

* Agent prompt
* Workflow node
* In a tool

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclassfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import dynamic_prompt, ModelRequest from langchain.agents.middleware import dynamic_prompt, ModelRequest  @dataclass @dataclassclass ContextSchema: class  ContextSchema: user_name: str user_name: str @dynamic_prompt @dynamic_promptdef personalized_prompt(request: ModelRequest) -> str: def  personalized_prompt(request: ModelRequest) -> str:  user_name = request.runtime.context.user_name  user_name = request.runtime.context.user_name return f"You are a helpful assistant. Address the user as {user_name}."  return  f"You are a helpful assistant. Address the user as {user_name}." agent = create_agent(agent = create_agent( model="claude-sonnet-4-5-20250929",  model ="claude-sonnet-4-5-20250929", tools=[get_weather],  tools =[get_weather], middleware=[personalized_prompt],  middleware =[personalized_prompt], context_schema=ContextSchema  context_schema = ContextSchema)) agent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "what is the weather in sf"}]}, {"messages": [{"role": "user", "content": "what is the weather in sf"}]}, context=ContextSchema(user_name="John Smith")  context =ContextSchema(user_name = "John Smith") ))
```

See [Agents](/oss/python/langchain/agents) for details.

The `Runtime` object can be used to access static context and other utilities like the active store and stream writer. See the @[`Runtime`][langgraph.runtime.Runtime] documentation for details.

## [​](#dynamic-runtime-context) Dynamic runtime context

**Dynamic runtime context** represents mutable data that can evolve during a single run and is managed through the LangGraph state object. This includes conversation history, intermediate results, and values derived from tools or LLM outputs. In LangGraph, the state object acts as [short-term memory](/oss/python/concepts/memory) during a run.

* In an agent
* In a workflow

Example shows how to incorporate state into an agent **prompt**.State can also be accessed by the agent’s **tools**, which can read or update the state as needed. See [tool calling guide](/oss/python/langchain/tools#short-term-memory) for details.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import dynamic_prompt, ModelRequest from langchain.agents.middleware import dynamic_prompt, ModelRequestfrom langchain.agents import AgentState from langchain.agents import  AgentState class CustomState(AgentState): class  CustomState(AgentState):  user_name: str user_name: str @dynamic_prompt @dynamic_promptdef personalized_prompt(request: ModelRequest) -> str: def  personalized_prompt(request: ModelRequest) -> str:  user_name = request.state.get("user_name", "User")  user_name = request.state.get("user_name", "User") return f"You are a helpful assistant. User's name is {user_name}"  return  f"You are a helpful assistant. User's name is {user_name} " agent = create_agent(agent = create_agent( model="claude-sonnet-4-5-20250929",  model ="claude-sonnet-4-5-20250929", tools=[...],  tools =[...], state_schema=CustomState,  state_schema =CustomState,  middleware=[personalized_prompt],  middleware =[personalized_prompt], )) agent.invoke({agent.invoke({ "messages": "hi!",  "messages": "hi!", "user_name": "John Smith"  "user_name": "John Smith"})})
```

**Turning on memory** Please see the [memory guide](/oss/python/langgraph/add-memory) for more details on how to enable memory. This is a powerful feature that allows you to persist the agent’s state across multiple invocations. Otherwise, the state is scoped only to a single run.

## [​](#dynamic-cross-conversation-context) Dynamic cross-conversation context

**Dynamic cross-conversation context** represents persistent, mutable data that spans across multiple conversations or sessions and is managed through the LangGraph store. This includes user profiles, preferences, and historical interactions. The LangGraph store acts as [long-term memory](/oss/python/concepts/memory#long-term-memory) across multiple runs. This can be used to read or update persistent facts (e.g., user profiles, preferences, prior interactions).

## [​](#see-also) See also

* [Memory conceptual overview](/oss/python/concepts/memory)
* [Short-term memory in LangChain](/oss/python/langchain/short-term-memory)
* [Long-term memory in LangChain](/oss/python/langchain/long-term-memory)
* [Memory in LangGraph](/oss/python/langgraph/add-memory)

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/concepts/context.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Memory overview

Previous](/oss/python/concepts/memory)[Graph API overview](/oss/python/langgraph/graph-api)