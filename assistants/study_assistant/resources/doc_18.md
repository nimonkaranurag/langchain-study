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
* [Usage](#usage)
* [In production](#in-production)
* [Customizing agent memory](#customizing-agent-memory)
* [Common patterns](#common-patterns)
* [Trim messages](#trim-messages)
* [Delete messages](#delete-messages)
* [Summarize messages](#summarize-messages)
* [Access memory](#access-memory)
* [Tools](#tools)
* [Read short-term memory in a tool](#read-short-term-memory-in-a-tool)
* [Write short-term memory from tools](#write-short-term-memory-from-tools)
* [Prompt](#prompt)
* [Before model](#before-model)
* [After model](#after-model)

[Core components](/oss/python/langchain/agents)

# Short-term memory

## [​](#overview) Overview

Memory is a system that remembers information about previous interactions. For AI agents, memory is crucial because it lets them remember previous interactions, learn from feedback, and adapt to user preferences. As agents tackle more complex tasks with numerous user interactions, this capability becomes essential for both efficiency and user satisfaction. Short term memory lets your application remember previous interactions within a single thread or conversation.

A thread organizes multiple interactions in a session, similar to the way email groups messages in a single conversation.

Conversation history is the most common form of short-term memory. Long conversations pose a challenge to today’s LLMs; a full history may not fit inside an LLM’s context window, resulting in an context loss or errors. Even if your model supports the full context length, most LLMs still perform poorly over long contexts. They get “distracted” by stale or off-topic content, all while suffering from slower response times and higher costs. Chat models accept context using [messages](/oss/python/langchain/messages), which include instructions (a system message) and inputs (human messages). In chat applications, messages alternate between human inputs and model responses, resulting in a list of messages that grows longer over time. Because context windows are limited, many applications can benefit from using techniques to remove or “forget” stale information.

## [​](#usage) Usage

To add short-term memory (thread-level persistence) to an agent, you need to specify a `checkpointer` when creating an agent.

LangChain’s agent manages short-term memory as a part of your agent’s state.By storing these in the graph’s state, the agent can access the full context for a given conversation while maintaining separation between different threads.State is persisted to a database (or memory) using a checkpointer so the thread can be resumed at any time.Short-term memory updates when the agent is invoked or a step (like a tool call) is completed, and the state is read at the start of each step.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaver  agent = create_agent(agent = create_agent( "gpt-5", "gpt-5", [get_user_info], [get_user_info], checkpointer=InMemorySaver(),  checkpointer =InMemorySaver(), )) agent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]}, {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]}, {"configurable": {"thread_id": "1"}},  {"configurable": {"thread_id": "1"}}, ))
```

### [​](#in-production) In production

In production, use a checkpointer backed by a database:

Copy

Ask AI

```
pip install langgraph-checkpoint-postgres pip  install langgraph-checkpoint-postgres
```

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent from langgraph.checkpoint.postgres import PostgresSaver from langgraph.checkpoint.postgres import  PostgresSaver  DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable" DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"with PostgresSaver.from_conn_string(DB_URI) as checkpointer: with PostgresSaver.from_conn_string(DB_URI) as checkpointer: checkpointer.setup() # auto create tables in PostgresSql checkpointer.setup() # auto create tables in PostgresSql agent = create_agent( agent = create_agent( "gpt-5", "gpt-5", [get_user_info], [get_user_info], checkpointer=checkpointer,  checkpointer =checkpointer,  ) )
```

## [​](#customizing-agent-memory) Customizing agent memory

By default, agents use [`AgentState`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.AgentState) to manage short term memory, specifically the conversation history via a `messages` key. You can extend [`AgentState`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.AgentState) to add additional fields. Custom state schemas are passed to [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) using the [`state_schema`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state_schema) parameter.

Copy

Ask AI

```
from langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaver class CustomAgentState(AgentState): class  CustomAgentState(AgentState):  user_id: str user_id: str preferences: dict preferences: dict agent = create_agent(agent = create_agent( "gpt-5", "gpt-5", [get_user_info], [get_user_info], state_schema=CustomAgentState,  state_schema =CustomAgentState,  checkpointer=InMemorySaver(),  checkpointer =InMemorySaver(),)) # Custom state can be passed in invoke # Custom state can be passed in invokeresult = agent.invoke(result = agent.invoke( { { "messages": [{"role": "user", "content": "Hello"}],  "messages": [{"role": "user", "content": "Hello"}], "user_id": "user_123",  "user_id": "user_123",  "preferences": {"theme": "dark"}  "preferences": {"theme": "dark"}  }, }, {"configurable": {"thread_id": "1"}}) {"configurable": {"thread_id": "1"}})
```

## [​](#common-patterns) Common patterns

With [short-term memory](#add-short-term-memory) enabled, long conversations can exceed the LLM’s context window. Common solutions are:

[## Trim messages

Remove first or last N messages (before calling LLM)](#trim-messages)[## Delete messages

Delete messages from LangGraph state permanently](#delete-messages)[## Summarize messages

Summarize earlier messages in the history and replace them with a summary](#summarize-messages)

## Custom strategies

Custom strategies (e.g., message filtering, etc.)

This allows the agent to keep track of the conversation without exceeding the LLM’s context window.

### [​](#trim-messages) Trim messages

Most LLMs have a maximum supported context window (denominated in tokens). One way to decide when to truncate messages is to count the tokens in the message history and truncate whenever it approaches that limit. If you’re using LangChain, you can use the trim messages utility and specify the number of tokens to keep from the list, as well as the `strategy` (e.g., keep the last `max_tokens`) to use for handling the boundary. To trim message history in an agent, use the [`@before_model`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.before_model) middleware decorator:

Copy

Ask AI

```
from langchain.messages import RemoveMessage from langchain.messages import  RemoveMessagefrom langgraph.graph.message import REMOVE_ALL_MESSAGES from langgraph.graph.message import  REMOVE_ALL_MESSAGESfrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaverfrom langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langchain.agents.middleware import before_model from langchain.agents.middleware import  before_modelfrom langgraph.runtime import Runtime from langgraph.runtime import  Runtimefrom langchain_core.runnables import RunnableConfig from langchain_core.runnables import  RunnableConfig from typing import Any from  typing import  Any  @before_model @before_modeldef trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None: def  trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] |  None: """Keep only the last few messages to fit context window.""" """Keep only the last few messages to fit context window.""" messages = state["messages"]  messages = state["messages"]  if len(messages) <= 3:  if  len(messages) <=  3:  return None # No changes needed  return  None  # No changes needed  first_msg = messages[0]  first_msg = messages[0] recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]  recent_messages = messages[- 3:] if  len(messages) %  2 ==  0  else messages[- 4:] new_messages = [first_msg] + recent_messages  new_messages = [first_msg] +  recent_messages  return { return { "messages": [ "messages": [ RemoveMessage(id=REMOVE_ALL_MESSAGES), RemoveMessage(id = REMOVE_ALL_MESSAGES), *new_messages * new_messages ] ] } } agent = create_agent(agent = create_agent( model, model, tools=tools,  tools =tools, middleware=[trim_messages],  middleware =[trim_messages], checkpointer=InMemorySaver(),  checkpointer =InMemorySaver(),)) config: RunnableConfig = {"configurable": {"thread_id": "1"}}config: RunnableConfig = {"configurable": {"thread_id": "1"}} agent.invoke({"messages": "hi, my name is bob"}, config)agent.invoke({"messages": "hi, my name is bob"}, config)agent.invoke({"messages": "write a short poem about cats"}, config)agent.invoke({"messages": "write a short poem about cats"}, config)agent.invoke({"messages": "now do the same but for dogs"}, config)agent.invoke({"messages": "now do the same but for dogs"}, config)final_response = agent.invoke({"messages": "what's my name?"}, config) final_response = agent.invoke({"messages": "what's my name?"}, config) final_response["messages"][-1].pretty_print()final_response["messages"][- 1].pretty_print() """ """ ================================== Ai Message ================================== ================================== Ai Message ================================== Your name is Bob. You told me that earlier.Your name is Bob. You told me that earlier.If you'd like me to call you a nickname or use a different name, just say the word.If you'd like me to call you a nickname or use a different name, just say the word. """ """
```

### [​](#delete-messages) Delete messages

You can delete messages from the graph state to manage the message history. This is useful when you want to remove specific messages or clear the entire message history. To delete messages from the graph state, you can use the `RemoveMessage`. For `RemoveMessage` to work, you need to use a state key with [`add_messages`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.message.add_messages) [reducer](/oss/python/langgraph/graph-api#reducers). The default [`AgentState`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.AgentState) provides this. To remove specific messages:

Copy

Ask AI

```
from langchain.messages import RemoveMessage from langchain.messages import  RemoveMessage def delete_messages(state): def  delete_messages(state): messages = state["messages"]  messages = state["messages"] if len(messages) > 2:  if  len(messages) >  2:  # remove the earliest two messages  # remove the earliest two messages return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}  return {"messages": [RemoveMessage(id =m.id) for  m in messages[: 2]]} 
```

To remove **all** messages:

Copy

Ask AI

```
from langgraph.graph.message import REMOVE_ALL_MESSAGES from langgraph.graph.message import  REMOVE_ALL_MESSAGES def delete_messages(state): def  delete_messages(state): return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]}  return {"messages": [RemoveMessage(id = REMOVE_ALL_MESSAGES)]} 
```

When deleting messages, **make sure** that the resulting message history is valid. Check the limitations of the LLM provider you’re using. For example:

* Some providers expect message history to start with a `user` message
* Most providers require `assistant` messages with tool calls to be followed by corresponding `tool` result messages.

Copy

Ask AI

```
from langchain.messages import RemoveMessage from langchain.messages import  RemoveMessagefrom langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langchain.agents.middleware import after_model from langchain.agents.middleware import  after_modelfrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaverfrom langgraph.runtime import Runtime from langgraph.runtime import  Runtimefrom langchain_core.runnables import RunnableConfig from langchain_core.runnables import  RunnableConfig  @after_model @after_modeldef delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None: def  delete_old_messages(state: AgentState, runtime: Runtime) -> dict  |  None: """Remove old messages to keep conversation manageable.""" """Remove old messages to keep conversation manageable.""" messages = state["messages"]  messages = state["messages"] if len(messages) > 2:  if  len(messages) >  2:  # remove the earliest two messages  # remove the earliest two messages return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}  return {"messages": [RemoveMessage(id =m.id) for  m in messages[: 2]]}  return None  return  None agent = create_agent(agent = create_agent( "gpt-5-nano", "gpt-5-nano", tools=[],  tools =[], system_prompt="Please be concise and to the point.",  system_prompt ="Please be concise and to the point.", middleware=[delete_old_messages],  middleware =[delete_old_messages], checkpointer=InMemorySaver(),  checkpointer =InMemorySaver(),)) config: RunnableConfig = {"configurable": {"thread_id": "1"}}config: RunnableConfig = {"configurable": {"thread_id": "1"}} for event in agent.stream(for  event in agent.stream( {"messages": [{"role": "user", "content": "hi! I'm bob"}]}, {"messages": [{"role": "user", "content": "hi! I'm bob"}]}, config, config, stream_mode="values",  stream_mode = "values",):): print([(message.type, message.content) for message in event["messages"]])  print([(message.type, message.content) for  message in event["messages"]]) for event in agent.stream(for  event in agent.stream( {"messages": [{"role": "user", "content": "what's my name?"}]}, {"messages": [{"role": "user", "content": "what's my name?"}]}, config, config, stream_mode="values",  stream_mode = "values",):): print([(message.type, message.content) for message in event["messages"]])  print([(message.type, message.content) for  message in event["messages"]])
```

Copy

Ask AI

```
[('human', "hi! I'm bob")][('human', "hi! I'm bob")][('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.')][('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.')][('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.'), ('human', "what's my name?")][('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.'), ('human', "what's my name?")][('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.'), ('human', "what's my name?"), ('ai', 'Your name is Bob. How can I help you today, Bob?')][('human', "hi! I'm bob"), ('ai', 'Hi Bob! Nice to meet you. How can I help you today? I can answer questions, brainstorm ideas, draft text, explain things, or help with code.'), ('human', "what's my name?"), ('ai', 'Your name is Bob. How can I help you today, Bob?')][('human', "what's my name?"), ('ai', 'Your name is Bob. How can I help you today, Bob?')][('human', "what's my name?"), ('ai', 'Your name is Bob. How can I help you today, Bob?')] 
```

### [​](#summarize-messages) Summarize messages

The problem with trimming or removing messages, as shown above, is that you may lose information from culling of the message queue. Because of this, some applications benefit from a more sophisticated approach of summarizing the message history using a chat model.  To summarize message history in an agent, use the built-in [`SummarizationMiddleware`](/oss/python/langchain/middleware#summarization):

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import SummarizationMiddleware from langchain.agents.middleware import  SummarizationMiddlewarefrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaverfrom langchain_core.runnables import RunnableConfig from langchain_core.runnables import  RunnableConfig checkpointer = InMemorySaver() checkpointer = InMemorySaver() agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[],  tools =[], middleware=[ middleware =[ SummarizationMiddleware( SummarizationMiddleware( model="gpt-4o-mini",  model ="gpt-4o-mini", max_tokens_before_summary=4000, # Trigger summarization at 4000 tokens  max_tokens_before_summary = 4000, # Trigger summarization at 4000 tokens messages_to_keep=20, # Keep last 20 messages after summary  messages_to_keep = 20, # Keep last 20 messages after summary ) ) ], ], checkpointer=checkpointer,  checkpointer =checkpointer,)) config: RunnableConfig = {"configurable": {"thread_id": "1"}}config: RunnableConfig = {"configurable": {"thread_id": "1"}}agent.invoke({"messages": "hi, my name is bob"}, config)agent.invoke({"messages": "hi, my name is bob"}, config)agent.invoke({"messages": "write a short poem about cats"}, config)agent.invoke({"messages": "write a short poem about cats"}, config)agent.invoke({"messages": "now do the same but for dogs"}, config)agent.invoke({"messages": "now do the same but for dogs"}, config)final_response = agent.invoke({"messages": "what's my name?"}, config) final_response = agent.invoke({"messages": "what's my name?"}, config) final_response["messages"][-1].pretty_print()final_response["messages"][- 1].pretty_print() """ """ ================================== Ai Message ================================== ================================== Ai Message ================================== Your name is Bob!Your name is Bob! """ """
```

See [`SummarizationMiddleware`](/oss/python/langchain/middleware#summarization) for more configuration options.

## [​](#access-memory) Access memory

You can access and modify the short-term memory (state) of an agent in several ways:

### [​](#tools) Tools

#### [​](#read-short-term-memory-in-a-tool) Read short-term memory in a tool

Access short term memory (state) in a tool using the `ToolRuntime` parameter. The `tool_runtime` parameter is hidden from the tool signature (so the model doesn’t see it), but the tool can access the state through it.

Copy

Ask AI

```
from langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langchain.tools import tool, ToolRuntime from langchain.tools import tool, ToolRuntime class CustomState(AgentState): class  CustomState(AgentState): user_id: str user_id: str @tool @tooldef get_user_info(def  get_user_info( runtime: ToolRuntime  runtime: ToolRuntime) -> str:) -> str: """Look up user info.""" """Look up user info.""" user_id = runtime.state["user_id"]  user_id = runtime.state["user_id"] return "User is John Smith" if user_id == "user_123" else "Unknown user"  return  "User is John Smith"  if  user_id ==  "user_123"  else  "Unknown user" agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[get_user_info],  tools =[get_user_info], state_schema=CustomState,  state_schema =CustomState,)) result = agent.invoke({result = agent.invoke({ "messages": "look up user information",  "messages": "look up user information", "user_id": "user_123"  "user_id": "user_123"})})print(result["messages"][-1].content) print(result["messages"][- 1].content)# > User is John Smith.# > User is John Smith.
```

#### [​](#write-short-term-memory-from-tools) Write short-term memory from tools

To modify the agent’s short-term memory (state) during execution, you can return state updates directly from the tools. This is useful for persisting intermediate results or making information accessible to subsequent tools or prompts.

Copy

Ask AI

```
from langchain.tools import tool, ToolRuntime from langchain.tools import tool, ToolRuntimefrom langchain_core.runnables import RunnableConfig from langchain_core.runnables import  RunnableConfigfrom langchain.messages import ToolMessage from langchain.messages import  ToolMessagefrom langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langgraph.types import Command from langgraph.types import  Command from pydantic import BaseModel from  pydantic import  BaseModel class CustomState(AgentState): class  CustomState(AgentState):  user_name: str user_name: str class CustomContext(BaseModel): class  CustomContext(BaseModel): user_id: str user_id: str @tool @tooldef update_user_info(def  update_user_info( runtime: ToolRuntime[CustomContext, CustomState],  runtime: ToolRuntime[CustomContext, CustomState],) -> Command:) -> Command: """Look up and update user info.""" """Look up and update user info.""" user_id = runtime.context.user_id  user_id = runtime.context.user_id  name = "John Smith" if user_id == "user_123" else "Unknown user"  name =  "John Smith"  if  user_id ==  "user_123"  else  "Unknown user" return Command(update={  return Command(update ={  "user_name": name,  "user_name": name,  # update the message history  # update the message history "messages": [ "messages": [ ToolMessage( ToolMessage( "Successfully looked up user information",  "Successfully looked up user information", tool_call_id=runtime.tool_call_id  tool_call_id =runtime.tool_call_id ) ) ] ] }) }) @tool @tooldef greet(def  greet( runtime: ToolRuntime[CustomContext, CustomState]  runtime: ToolRuntime[CustomContext, CustomState]) -> str:) -> str: """Use this to greet the user once you found their info.""" """Use this to greet the user once you found their info.""" user_name = runtime.state["user_name"]  user_name = runtime.state["user_name"] return f"Hello {user_name}!"  return  f "Hello {user_name}!"agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[update_user_info, greet],  tools =[update_user_info, greet], state_schema=CustomState,  state_schema =CustomState,  context_schema=CustomContext,  context_schema =CustomContext, )) agent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "greet the user"}]}, {"messages": [{"role": "user", "content": "greet the user"}]}, context=CustomContext(user_id="user_123"),  context =CustomContext(user_id = "user_123"),))
```

### [​](#prompt) Prompt

Access short term memory (state) in middleware to create dynamic prompts based on conversation history or custom state fields.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent from typing import TypedDict from  typing import  TypedDictfrom langchain.agents.middleware import dynamic_prompt, ModelRequest from langchain.agents.middleware import dynamic_prompt, ModelRequest class CustomContext(TypedDict): class  CustomContext(TypedDict): user_name: str user_name: str def get_weather(city: str) -> str: def  get_weather(city: str) -> str: """Get the weather in a city.""" """Get the weather in a city.""" return f"The weather in {city} is always sunny!"  return  f "The weather in {city} is always sunny!"  @dynamic_prompt @dynamic_promptdef dynamic_system_prompt(request: ModelRequest) -> str: def  dynamic_system_prompt(request: ModelRequest) -> str: user_name = request.runtime.context["user_name"]  user_name = request.runtime.context["user_name"] system_prompt = f"You are a helpful assistant. Address the user as {user_name}."  system_prompt =  f"You are a helpful assistant. Address the user as {user_name}."  return system_prompt  return  system_prompt agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[get_weather],  tools =[get_weather], middleware=[dynamic_system_prompt],  middleware =[dynamic_system_prompt], context_schema=CustomContext,  context_schema =CustomContext,)) result = agent.invoke(result = agent.invoke( {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, context=CustomContext(user_name="John Smith"),  context =CustomContext(user_name = "John Smith"),))for msg in result["messages"]: for  msg in result["messages"]: msg.pretty_print() msg.pretty_print() 
```

Output

Copy

Ask AI

```
================================ Human Message ================================= ================================  Human  Message ================================= What is the weather in SF? What  is  the  weather  in  SF? ================================== Ai Message ================================== ==================================  Ai  Message ==================================Tool Calls: Tool Calls: get_weather (call_WFQlOGn4b2yoJrv7cih342FG)  get_weather (call_WFQlOGn4b2yoJrv7cih342FG) Call ID: call_WFQlOGn4b2yoJrv7cih342FG  Call ID:  call_WFQlOGn4b2yoJrv7cih342FG Args: Args: city: San Francisco city:  San  Francisco ================================= Tool Message ================================= =================================  Tool  Message =================================Name: get_weatherName:  get_weather The weather in San Francisco is always sunny! The  weather  in  San  Francisco  is  always sunny! ================================== Ai Message ================================== ==================================  Ai  Message ================================== Hi John Smith, the weather in San Francisco is always sunny! Hi  John Smith,  the  weather  in  San  Francisco  is  always sunny!
```

### [​](#before-model) Before model

Access short term memory (state) in [`@before_model`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.before_model) middleware to process messages before model calls.

Copy

Ask AI

```
from langchain.messages import RemoveMessage from langchain.messages import  RemoveMessagefrom langgraph.graph.message import REMOVE_ALL_MESSAGES from langgraph.graph.message import  REMOVE_ALL_MESSAGESfrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaverfrom langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langchain.agents.middleware import before_model from langchain.agents.middleware import  before_modelfrom langgraph.runtime import Runtime from langgraph.runtime import  Runtime from typing import Any from  typing import  Any  @before_model @before_modeldef trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None: def  trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] |  None: """Keep only the last few messages to fit context window.""" """Keep only the last few messages to fit context window.""" messages = state["messages"]  messages = state["messages"]  if len(messages) <= 3:  if  len(messages) <=  3:  return None # No changes needed  return  None  # No changes needed  first_msg = messages[0]  first_msg = messages[0] recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]  recent_messages = messages[- 3:] if  len(messages) %  2 ==  0  else messages[- 4:] new_messages = [first_msg] + recent_messages  new_messages = [first_msg] +  recent_messages  return { return { "messages": [ "messages": [ RemoveMessage(id=REMOVE_ALL_MESSAGES), RemoveMessage(id = REMOVE_ALL_MESSAGES), *new_messages * new_messages ] ] } } agent = create_agent(agent = create_agent( model, model, tools=tools,  tools =tools, middleware=[trim_messages]  middleware =[trim_messages])) config: RunnableConfig = {"configurable": {"thread_id": "1"}}config: RunnableConfig = {"configurable": {"thread_id": "1"}} agent.invoke({"messages": "hi, my name is bob"}, config)agent.invoke({"messages": "hi, my name is bob"}, config)agent.invoke({"messages": "write a short poem about cats"}, config)agent.invoke({"messages": "write a short poem about cats"}, config)agent.invoke({"messages": "now do the same but for dogs"}, config)agent.invoke({"messages": "now do the same but for dogs"}, config)final_response = agent.invoke({"messages": "what's my name?"}, config) final_response = agent.invoke({"messages": "what's my name?"}, config) final_response["messages"][-1].pretty_print()final_response["messages"][- 1].pretty_print() """ """ ================================== Ai Message ================================== ================================== Ai Message ================================== Your name is Bob. You told me that earlier.Your name is Bob. You told me that earlier.If you'd like me to call you a nickname or use a different name, just say the word.If you'd like me to call you a nickname or use a different name, just say the word. """ """
```

### [​](#after-model) After model

Access short term memory (state) in [`@after_model`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.after_model) middleware to process messages after model calls.

Copy

Ask AI

```
from langchain.messages import RemoveMessage from langchain.messages import  RemoveMessagefrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaverfrom langchain.agents import create_agent, AgentState from langchain.agents import create_agent, AgentStatefrom langchain.agents.middleware import after_model from langchain.agents.middleware import  after_modelfrom langgraph.runtime import Runtime from langgraph.runtime import  Runtime  @after_model @after_modeldef validate_response(state: AgentState, runtime: Runtime) -> dict | None: def  validate_response(state: AgentState, runtime: Runtime) -> dict  |  None: """Remove messages containing sensitive words.""" """Remove messages containing sensitive words.""" STOP_WORDS = ["password", "secret"]  STOP_WORDS = ["password", "secret"] last_message = state["messages"][-1]  last_message = state["messages"][- 1] if any(word in last_message.content for word in STOP_WORDS):  if  any(word in last_message.content for  word in  STOP_WORDS): return {"messages": [RemoveMessage(id=last_message.id)]}  return {"messages": [RemoveMessage(id =last_message.id)]}  return None  return  None agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[],  tools =[], middleware=[validate_response],  middleware =[validate_response], checkpointer=InMemorySaver(),  checkpointer =InMemorySaver(),))
```

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/short-term-memory.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Tools](/oss/python/langchain/tools)[Streaming](/oss/python/langchain/streaming)