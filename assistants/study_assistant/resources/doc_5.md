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
* [Agent progress](#agent-progress)
* [LLM tokens](#llm-tokens)
* [Custom updates](#custom-updates)
* [Stream multiple modes](#stream-multiple-modes)
* [Disable streaming](#disable-streaming)

[Core components](/oss/python/langchain/agents)

# Streaming

LangChain implements a streaming system to surface real-time updates. Streaming is crucial for enhancing the responsiveness of applications built on LLMs. By displaying output progressively, even before a complete response is ready, streaming significantly improves user experience (UX), particularly when dealing with the latency of LLMs.

## [​](#overview) Overview

LangChain’s streaming system lets you surface live feedback from agent runs to your application. What’s possible with LangChain streaming:

* [**Stream agent progress**](#agent-progress) — get state updates after each agent step.
* [**Stream LLM tokens**](#llm-tokens) — stream language model tokens as they’re generated.
* [**Stream custom updates**](#custom-updates) — emit user-defined signals (e.g., `"Fetched 10/100 records"`).
* [**Stream multiple modes**](#stream-multiple-modes) — choose from `updates` (agent progress), `messages` (LLM tokens + metadata), or `custom` (arbitrary user data).

## [​](#agent-progress) Agent progress

To stream agent progress, use the [`stream`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.stream) or [`astream`](https://reference.langchain.com/python/langgraph/graphs/#langgraph.graph.state.CompiledStateGraph.astream) methods with `stream_mode="updates"`. This emits an event after every agent step. For example, if you have an agent that calls a tool once, you should see the following updates:

* **LLM node**: [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) with tool call requests
* **Tool node**: [`ToolMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage) with execution result
* **LLM node**: Final AI response

Streaming agent progress

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent def get_weather(city: str) -> str: def  get_weather(city: str) -> str: """Get weather for a given city.""" """Get weather for a given city."""  return f"It's always sunny in {city}!"  return  f "It's always sunny in {city}!" agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[get_weather],  tools =[get_weather],))for chunk in agent.stream( for  chunk in agent.stream(  {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, stream_mode="updates",  stream_mode = "updates",):): for step, data in chunk.items():  for step, data in chunk.items(): print(f"step: {step}")  print(f"step: {step} ") print(f"content: {data['messages'][-1].content_blocks}")  print(f"content: {data['messages'][- 1].content_blocks} ")
```

Output

Copy

Ask AI

```
step: modelstep:  modelcontent: [{'type': 'tool_call', 'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_OW2NYNsNSKhRZpjW0wm2Aszd'}]content: [{'type': 'tool_call', 'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_OW2NYNsNSKhRZpjW0wm2Aszd'}] step: toolsstep:  toolscontent: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}] step: modelstep:  modelcontent: [{'type': 'text', 'text': 'It's always sunny in San Francisco!'}]content: [{'type': 'text', 'text':  'It's  always  sunny  in  San Francisco!'}]
```

## [​](#llm-tokens) LLM tokens

To stream tokens as they are produced by the LLM, use `stream_mode="messages"`. Below you can see the output of the agent streaming tool calls and the final response.

Streaming LLM tokens

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent def get_weather(city: str) -> str: def  get_weather(city: str) -> str: """Get weather for a given city.""" """Get weather for a given city."""  return f"It's always sunny in {city}!"  return  f "It's always sunny in {city}!" agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[get_weather],  tools =[get_weather],))for token, metadata in agent.stream( for token, metadata in agent.stream(  {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, stream_mode="messages",  stream_mode = "messages",):): print(f"node: {metadata['langgraph_node']}")  print(f"node: {metadata['langgraph_node']} ") print(f"content: {token.content_blocks}")  print(f"content: {token.content_blocks} ") print("\n")  print(" \n ")
```

Output

Copy

Ask AI

```
node: modelnode:  modelcontent: [{'type': 'tool_call_chunk', 'id': 'call_vbCyBcP8VuneUzyYlSBZZsVa', 'name': 'get_weather', 'args': '', 'index': 0}]content: [{'type': 'tool_call_chunk', 'id': 'call_vbCyBcP8VuneUzyYlSBZZsVa', 'name': 'get_weather', 'args': '', 'index':  0}] node: modelnode:  modelcontent: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '{"', 'index': 0}]content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '{"', 'index':  0}] node: modelnode:  modelcontent: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'city', 'index': 0}]content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'city', 'index':  0}] node: modelnode:  modelcontent: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '":"', 'index': 0}]content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '":"', 'index':  0}] node: modelnode:  modelcontent: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'San', 'index': 0}]content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': 'San', 'index':  0}] node: modelnode:  modelcontent: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': ' Francisco', 'index': 0}]content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': ' Francisco', 'index':  0}] node: modelnode:  modelcontent: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '"}', 'index': 0}]content: [{'type': 'tool_call_chunk', 'id': None, 'name': None, 'args': '"}', 'index':  0}] node: modelnode:  modelcontent: []content: [] node: toolsnode:  toolscontent: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}] node: modelnode:  modelcontent: []content: [] node: modelnode:  modelcontent: [{'type': 'text', 'text': 'Here'}]content: [{'type': 'text', 'text': 'Here'}] node: modelnode:  modelcontent: [{'type': 'text', 'text': ''s'}]content: [{'type': 'text', 'text': ''s'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' what'}]content: [{'type': 'text', 'text': ' what'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' I'}]content: [{'type': 'text', 'text': ' I'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' got'}]content: [{'type': 'text', 'text': ' got'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ':'}]content: [{'type': 'text', 'text': ':'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' "'}]content: [{'type': 'text', 'text': ' "'}] node: modelnode: modelcontent: [{'type': 'text', 'text': "It's"}]content: [{'type': 'text', 'text': "It's"}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' always'}]content: [{'type': 'text', 'text': ' always'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' sunny'}]content: [{'type': 'text', 'text': ' sunny'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' in'}]content: [{'type': 'text', 'text': ' in'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' San'}]content: [{'type': 'text', 'text': ' San'}] node: modelnode: modelcontent: [{'type': 'text', 'text': ' Francisco'}]content: [{'type': 'text', 'text': ' Francisco'}] node: modelnode: modelcontent: [{'type': 'text', 'text': '!"\n\n'}]content: [{'type': 'text', 'text': '!"\n\n'}]
```

## [​](#custom-updates) Custom updates

To stream updates from tools as they are executed, you can use [`get_stream_writer`](https://reference.langchain.com/python/langgraph/config/#langgraph.config.get_stream_writer).

Streaming custom updates

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langgraph.config import get_stream_writer from langgraph.config import  get_stream_writer  def get_weather(city: str) -> str: def  get_weather(city: str) -> str: """Get weather for a given city.""" """Get weather for a given city.""" writer = get_stream_writer()  writer = get_stream_writer()  # stream any arbitrary data  # stream any arbitrary data writer(f"Looking up data for city: {city}") writer(f"Looking up data for city: {city} ") writer(f"Acquired data for city: {city}") writer(f"Acquired data for city: {city} ") return f"It's always sunny in {city}!"  return  f "It's always sunny in {city}!" agent = create_agent(agent = create_agent( model="claude-sonnet-4-5-20250929",  model ="claude-sonnet-4-5-20250929", tools=[get_weather],  tools =[get_weather],)) for chunk in agent.stream(for  chunk in agent.stream( {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, stream_mode="custom"  stream_mode = "custom"):): print(chunk)  print(chunk)
```

Output

Copy

Ask AI

```
Looking up data for city: San Francisco Looking  up  data  for city:  San  FranciscoAcquired data for city: San Francisco Acquired  data  for city:  San  Francisco
```

If you add [`get_stream_writer`](https://reference.langchain.com/python/langgraph/config/#langgraph.config.get_stream_writer) inside your tool, you won’t be able to invoke the tool outside of a LangGraph execution context.

## [​](#stream-multiple-modes) Stream multiple modes

You can specify multiple streaming modes by passing stream mode as a list: `stream_mode=["updates", "custom"]`:

Streaming multiple modes

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langgraph.config import get_stream_writer from langgraph.config import  get_stream_writer def get_weather(city: str) -> str: def  get_weather(city: str) -> str: """Get weather for a given city.""" """Get weather for a given city.""" writer = get_stream_writer()  writer = get_stream_writer() writer(f"Looking up data for city: {city}") writer(f"Looking up data for city: {city} ") writer(f"Acquired data for city: {city}") writer(f"Acquired data for city: {city} ") return f"It's always sunny in {city}!"  return  f "It's always sunny in {city}!" agent = create_agent(agent = create_agent( model="gpt-5-nano",  model ="gpt-5-nano", tools=[get_weather],  tools =[get_weather],)) for stream_mode, chunk in agent.stream( for stream_mode, chunk in agent.stream(  {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, {"messages": [{"role": "user", "content": "What is the weather in SF?"}]}, stream_mode=["updates", "custom"]  stream_mode =["updates", "custom"]):): print(f"stream_mode: {stream_mode}")  print(f"stream_mode: {stream_mode} ") print(f"content: {chunk}")  print(f"content: {chunk} ") print("\n")  print(" \n ")
```

Output

Copy

Ask AI

```
stream_mode: updatesstream_mode:  updatescontent: {'model': {'messages': [AIMessage(content='', response_metadata={'token_usage': {'completion_tokens': 280, 'prompt_tokens': 132, 'total_tokens': 412, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 256, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tlgBzGEbedGYxZ0rTCz5F7OXpL7', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--480c07cb-e405-4411-aa7f-0520fddeed66-0', tool_calls=[{'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_KTNQIftMrl9vgNwEfAJMVu7r', 'type': 'tool_call'}], usage_metadata={'input_tokens': 132, 'output_tokens': 280, 'total_tokens': 412, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 256}})]}}content: {'model': {'messages': [AIMessage(content= '', response_metadata={'token_usage': {'completion_tokens': 280, 'prompt_tokens': 132, 'total_tokens': 412, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 256, 'rejected_prediction_tokens':  0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens':  0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tlgBzGEbedGYxZ0rTCz5F7OXpL7', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--480c07cb-e405-4411-aa7f-0520fddeed66-0', tool_calls=[{'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_KTNQIftMrl9vgNwEfAJMVu7r', 'type': 'tool_call'}], usage_metadata={'input_tokens': 132, 'output_tokens': 280, 'total_tokens': 412, 'input_token_details': {'audio': 0, 'cache_read':  0}, 'output_token_details': {'audio': 0, 'reasoning':  256}})]}} stream_mode: customstream_mode:  customcontent: Looking up data for city: San Franciscocontent:  Looking  up  data  for city:  San  Francisco stream_mode: customstream_mode:  customcontent: Acquired data for city: San Franciscocontent:  Acquired  data  for city:  San  Francisco stream_mode: updatesstream_mode:  updatescontent: {'tools': {'messages': [ToolMessage(content="It's always sunny in San Francisco!", name='get_weather', tool_call_id='call_KTNQIftMrl9vgNwEfAJMVu7r')]}}content: {'tools': {'messages': [ToolMessage(content="It's always sunny in San Francisco!", name='get_weather', tool_call_id='call_KTNQIftMrl9vgNwEfAJMVu7r')]}} stream_mode: updatesstream_mode:  updatescontent: {'model': {'messages': [AIMessage(content='San Francisco weather: It's always sunny in San Francisco!\n\n', response_metadata={'token_usage': {'completion_tokens': 764, 'prompt_tokens': 168, 'total_tokens': 932, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 704, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tljDFVki1e1haCyikBptAuXuHYG', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--acbc740a-18fe-4a14-8619-da92a0d0ee90-0', usage_metadata={'input_tokens': 168, 'output_tokens': 764, 'total_tokens': 932, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 704}})]}}content: {'model': {'messages': [AIMessage(content='San Francisco weather: It' s always  sunny  in  San Francisco! \n\n', response_metadata={'token_usage': {'completion_tokens': 764, 'prompt_tokens': 168, 'total_tokens': 932, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 704, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-C9tljDFVki1e1haCyikBptAuXuHYG', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--acbc740a-18fe-4a14-8619-da92a0d0ee90-0', usage_metadata={'input_tokens': 168, 'output_tokens': 764, 'total_tokens': 932, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 704}})]}}
```

## [​](#disable-streaming) Disable streaming

In some applications you might need to disable streaming of individual tokens for a given model. This is useful in [multi-agent](/oss/python/langchain/multi-agent) systems to control which agents stream their output. See the [Models](/oss/python/langchain/models#disable-streaming) guide to learn how to disable streaming. 

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/streaming.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Short-term memory](/oss/python/langchain/short-term-memory)[Middleware](/oss/python/langchain/middleware)