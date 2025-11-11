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
* [Access](#access)
* [Inside tools](#inside-tools)
* [Inside middleware](#inside-middleware)

[Advanced usage](/oss/python/langchain/guardrails)

# Runtime

## [​](#overview) Overview

LangChain’s [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) runs on LangGraph’s runtime under the hood. LangGraph exposes a [`Runtime`](https://reference.langchain.com/python/langgraph/runtime/#langgraph.runtime.Runtime) object with the following information:

1. **Context**: static information like user id, db connections, or other dependencies for an agent invocation
2. **Store**: a [BaseStore](https://reference.langchain.com/python/langgraph/store/#langgraph.store.base.BaseStore) instance used for [long-term memory](/oss/python/langchain/long-term-memory)
3. **Stream writer**: an object used for streaming information via the `"custom"` stream mode

You can access the runtime information within [tools](#inside-tools) and [middleware](#inside-middleware).

## [​](#access) Access

When creating an agent with [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent), you can specify a `context_schema` to define the structure of the `context` stored in the agent [`Runtime`](https://reference.langchain.com/python/langgraph/runtime/#langgraph.runtime.Runtime). When invoking the agent, pass the `context` argument with the relevant configuration for the run:

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclass from langchain.agents import create_agent from langchain.agents import  create_agent  @dataclass @dataclassclass Context: class  Context: user_name: str user_name: str agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[...],  tools =[...], context_schema=Context  context_schema = Context )) agent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "What's my name?"}]}, {"messages": [{"role": "user", "content": "What's my name?"}]}, context=Context(user_name="John Smith")  context =Context(user_name = "John Smith") ))
```

### [​](#inside-tools) Inside tools

You can access the runtime information inside tools to:

* Access the context
* Read or write long-term memory
* Write to the [custom stream](/oss/python/langchain/streaming#custom-updates) (ex, tool progress / updates)

Use the `ToolRuntime` parameter to access the [`Runtime`](https://reference.langchain.com/python/langgraph/runtime/#langgraph.runtime.Runtime) object inside a tool.

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclassfrom langchain.tools import tool, ToolRuntime from langchain.tools import tool, ToolRuntime  @dataclass @dataclassclass Context: class  Context: user_id: str user_id: str @tool @tooldef fetch_user_email_preferences(runtime: ToolRuntime[Context]) -> str: def  fetch_user_email_preferences(runtime: ToolRuntime[Context]) -> str:  """Fetch the user's email preferences from the store.""" """Fetch the user's email preferences from the store.""" user_id = runtime.context.user_id  user_id = runtime.context.user_id  preferences: str = "The user prefers you to write a brief and polite email." preferences: str = "The user prefers you to write a brief and polite email." if runtime.store:  if runtime.store:  if memory := runtime.store.get(("users",), user_id):  if  memory := runtime.store.get(("users",), user_id):  preferences = memory.value["preferences"]  preferences = memory.value["preferences"]  return preferences  return  preferences
```

### [​](#inside-middleware) Inside middleware

You can access runtime information in middleware to create dynamic prompts, modify messages, or control agent behavior based on user context. Use `request.runtime` to access the [`Runtime`](https://reference.langchain.com/python/langgraph/runtime/#langgraph.runtime.Runtime) object inside middleware decorators. The runtime object is available in the [`ModelRequest`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.ModelRequest) parameter passed to middleware functions.

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclass from langchain.messages import AnyMessage from langchain.messages import  AnyMessagefrom langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langchain.agents.middleware import dynamic_prompt, ModelRequest, before_model, after_model from langchain.agents.middleware import dynamic_prompt, ModelRequest, before_model, after_modelfrom langgraph.runtime import Runtime from langgraph.runtime import  Runtime  @dataclass @dataclassclass Context: class  Context: user_name: str user_name: str # Dynamic prompts # Dynamic prompts @dynamic_prompt @dynamic_promptdef dynamic_system_prompt(request: ModelRequest) -> str: def  dynamic_system_prompt(request: ModelRequest) -> str: user_name = request.runtime.context.user_name  user_name = request.runtime.context.user_name  system_prompt = f"You are a helpful assistant. Address the user as {user_name}."  system_prompt =  f"You are a helpful assistant. Address the user as {user_name}."  return system_prompt  return  system_prompt # Before model hook # Before model hook @before_model @before_modeldef log_before_model(state: AgentState, runtime: Runtime[Context]) -> dict | None: def  log_before_model(state: AgentState, runtime: Runtime[Context]) -> dict  |  None:  print(f"Processing request for user: {runtime.context.user_name}")  print(f"Processing request for user: {runtime.context.user_name} ")  return None  return  None # After model hook # After model hook @after_model @after_modeldef log_after_model(state: AgentState, runtime: Runtime[Context]) -> dict | None: def  log_after_model(state: AgentState, runtime: Runtime[Context]) -> dict  |  None:  print(f"Completed request for user: {runtime.context.user_name}")  print(f"Completed request for user: {runtime.context.user_name} ")  return None  return  None agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[...],  tools =[...], middleware=[dynamic_system_prompt, log_before_model, log_after_model],  middleware =[dynamic_system_prompt, log_before_model, log_after_model],  context_schema=Context  context_schema = Context)) agent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "What's my name?"}]}, {"messages": [{"role": "user", "content": "What's my name?"}]}, context=Context(user_name="John Smith")  context =Context(user_name = "John Smith")))
```

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/runtime.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Guardrails](/oss/python/langchain/guardrails)[Context engineering in agents](/oss/python/langchain/context-engineering)