We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

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

* [Core components](#core-components)
* [Model](#model)
* [Static model](#static-model)
* [Dynamic model](#dynamic-model)
* [Tools](#tools)
* [Defining tools](#defining-tools)
* [Tool error handling](#tool-error-handling)
* [Tool use in the ReAct loop](#tool-use-in-the-react-loop)
* [System prompt](#system-prompt)
* [Dynamic system prompt](#dynamic-system-prompt)
* [Invocation](#invocation)
* [Advanced concepts](#advanced-concepts)
* [Structured output](#structured-output)
* [ToolStrategy](#toolstrategy)
* [ProviderStrategy](#providerstrategy)
* [Memory](#memory)
* [Defining state via middleware](#defining-state-via-middleware)
* [Defining state via state\_schema](#defining-state-via-state-schema)
* [Streaming](#streaming)
* [Middleware](#middleware)

[Core components](/oss/python/langchain/agents)

# Agents

Agents combine language models with [tools](/oss/python/langchain/tools) to create systems that can reason about tasks, decide which tools to use, and iteratively work towards solutions. [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) provides a production-ready agent implementation. [An LLM Agent runs tools in a loop to achieve a goal](https://simonwillison.net/2025/Sep/18/agents/). An agent runs until a stop condition is met - i.e., when the model emits a final output or an iteration limit is reached.

[`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) builds a **graph**-based agent runtime using [LangGraph](/oss/python/langgraph/overview). A graph consists of nodes (steps) and edges (connections) that define how your agent processes information. The agent moves through this graph, executing nodes like the model node (which calls the model), the tools node (which executes tools), or middleware.Learn more about the [Graph API](/oss/python/langgraph/graph-api).

## [​](#core-components) Core components

### [​](#model) Model

The [model](/oss/python/langchain/models) is the reasoning engine of your agent. It can be specified in multiple ways, supporting both static and dynamic model selection.

#### [​](#static-model) Static model

Static models are configured once when creating the agent and remain unchanged throughout execution. This is the most common and straightforward approach. To initialize a static model from a :

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent agent = create_agent(agent = create_agent( "gpt-5", "gpt-5", tools=tools  tools = tools))
```

Model identifier strings support automatic inference (e.g., `"gpt-5"` will be inferred as `"openai:gpt-5"`). Refer to the [reference](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model(model_provider)) to see a full list of model identifier string mappings.

For more control over the model configuration, initialize a model instance directly using the provider package. In this example, we use [`ChatOpenAI`](https://reference.langchain.com/python/integrations/langchain_openai/ChatOpenAI/). See [Chat models](/oss/python/integrations/chat) for other available chat model classes.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent from langchain_openai import ChatOpenAI from  langchain_openai import  ChatOpenAI model = ChatOpenAI(model = ChatOpenAI( model="gpt-5",  model ="gpt-5", temperature=0.1,  temperature =0.1, max_tokens=1000,  max_tokens = 1000, timeout=30  timeout = 30 # ... (other params) # ... (other params)))agent = create_agent(model, tools=tools) agent = create_agent(model, tools =tools)
```

Model instances give you complete control over configuration. Use them when you need to set specific [parameters](/oss/python/langchain/models#parameters) like `temperature`, `max_tokens`, `timeouts`, `base_url`, and other provider-specific settings. Refer to the [reference](/oss/python/integrations/providers/all_providers) to see available params and methods on your model.

#### [​](#dynamic-model) Dynamic model

Dynamic models are selected at based on the current and context. This enables sophisticated routing logic and cost optimization. To use a dynamic model, create middleware using the [`@wrap_model_call`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.wrap_model_call) decorator that modifies the model in the request:

Copy

Ask AI

```
from langchain_openai import ChatOpenAI from  langchain_openai import  ChatOpenAIfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse basic_model = ChatOpenAI(model="gpt-4o-mini") basic_model = ChatOpenAI(model ="gpt-4o-mini")advanced_model = ChatOpenAI(model="gpt-4o") advanced_model = ChatOpenAI(model ="gpt-4o") @wrap_model_call @wrap_model_calldef dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse: def  dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse: """Choose model based on conversation complexity.""" """Choose model based on conversation complexity.""" message_count = len(request.state["messages"])  message_count =  len(request.state["messages"])  if message_count > 10:  if  message_count >  10:  # Use an advanced model for longer conversations  # Use an advanced model for longer conversations model = advanced_model  model =  advanced_model else:  else: model = basic_model  model =  basic_model  request.model = model request.model =  model return handler(request)  return handler(request) agent = create_agent(agent = create_agent( model=basic_model, # Default model  model =basic_model, # Default model tools=tools,  tools =tools, middleware=[dynamic_model_selection]  middleware =[dynamic_model_selection]))
```

Pre-bound models (models with [`bind_tools`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.bind_tools) already called) are not supported when using structured output. If you need dynamic model selection with structured output, ensure the models passed to the middleware are not pre-bound.

For model configuration details, see [Models](/oss/python/langchain/models). For dynamic model selection patterns, see [Dynamic model in middleware](/oss/python/langchain/middleware#dynamic-model).

### [​](#tools) Tools

Tools give agents the ability to take actions. Agents go beyond simple model-only tool binding by facilitating:

* Multiple tool calls in sequence (triggered by a single prompt)
* Parallel tool calls when appropriate
* Dynamic tool selection based on previous results
* Tool retry logic and error handling
* State persistence across tool calls

For more information, see [Tools](/oss/python/langchain/tools).

#### [​](#defining-tools) Defining tools

Pass a list of tools to the agent.

Copy

Ask AI

```
from langchain.tools import tool from langchain.tools import  toolfrom langchain.agents import create_agent from langchain.agents import  create_agent  @tool @tooldef search(query: str) -> str: def  search(query: str) -> str: """Search for information.""" """Search for information.""" return f"Results for: {query}"  return  f"Results for: {query} " @tool @tooldef get_weather(location: str) -> str: def  get_weather(location: str) -> str: """Get weather information for a location.""" """Get weather information for a location.""" return f"Weather in {location}: Sunny, 72°F"  return  f "Weather in {location}: Sunny, 72°F" agent = create_agent(model, tools=[search, get_weather]) agent = create_agent(model, tools =[search, get_weather])
```

If an empty tool list is provided, the agent will consist of a single LLM node without tool-calling capabilities.

#### [​](#tool-error-handling) Tool error handling

To customize how tool errors are handled, use the [`@wrap_tool_call`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.wrap_tool_call) decorator to create middleware:

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import wrap_tool_call from langchain.agents.middleware import  wrap_tool_callfrom langchain_core.messages import ToolMessage from langchain_core.messages import  ToolMessage  @wrap_tool_call @wrap_tool_calldef handle_tool_errors(request, handler): def  handle_tool_errors(request, handler): """Handle tool execution errors with custom messages.""" """Handle tool execution errors with custom messages.""" try:  try: return handler(request)  return handler(request) except Exception as e:  except  Exception  as e:  # Return a custom error message to the model  # Return a custom error message to the model return ToolMessage( return ToolMessage( content=f"Tool error: Please check your input and try again. ({str(e)})",  content = f"Tool error: Please check your input and try again. ({str(e)})", tool_call_id=request.tool_call["id"]  tool_call_id =request.tool_call["id"] ) ) agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[search, get_weather],  tools =[search, get_weather], middleware=[handle_tool_errors]  middleware =[handle_tool_errors]))
```

The agent will return a [`ToolMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage) with the custom error message when a tool fails:

Copy

Ask AI

```
[[ ... ... ToolMessage( ToolMessage( content="Tool error: Please check your input and try again. (division by zero)",  content ="Tool error: Please check your input and try again. (division by zero)", tool_call_id="..."  tool_call_id ="..." ), ), ... ...]]
```

#### [​](#tool-use-in-the-react-loop) Tool use in the ReAct loop

Agents follow the ReAct (“Reasoning + Acting”) pattern, alternating between brief reasoning steps with targeted tool calls and feeding the resulting observations into subsequent decisions until they can deliver a final answer. 

Example of ReAct loop

Prompt: Identify the current most popular wireless headphones and verify availability.

Copy

Ask AI

```
================================ Human Message ================================= ================================ Human Message =================================  Find the most popular wireless headphones right now and check if they're in stock Find the most popular wireless headphones right now and check if they're in stock 
```

* **Reasoning**: “Popularity is time-sensitive, I need to use the provided search tool.”
* **Acting**: Call `search_products("wireless headphones")`

Copy

Ask AI

```
================================== Ai Message ================================== ================================== Ai Message ==================================Tool Calls:Tool Calls: search_products (call_abc123) search_products (call_abc123) Call ID: call_abc123 Call ID: call_abc123 Args: Args: query: wireless headphones query: wireless headphones 
```

Copy

Ask AI

```
================================= Tool Message ================================= ================================= Tool Message ================================= Found 5 products matching "wireless headphones". Top 5 results: WH-1000XM5, ...Found 5 products matching "wireless headphones". Top 5 results: WH-1000XM5, ... 
```

* **Reasoning**: “I need to confirm availability for the top-ranked item before answering.”
* **Acting**: Call `check_inventory("WH-1000XM5")`

Copy

Ask AI

```
================================== Ai Message ================================== ================================== Ai Message ==================================Tool Calls:Tool Calls: check_inventory (call_def456) check_inventory (call_def456) Call ID: call_def456 Call ID: call_def456 Args: Args: product_id: WH-1000XM5 product_id: WH-1000XM5 
```

Copy

Ask AI

```
================================= Tool Message ================================= ================================= Tool Message ================================= Product WH-1000XM5: 10 units in stockProduct WH-1000XM5: 10 units in stock 
```

* **Reasoning**: “I have the most popular model and its stock status. I can now answer the user’s question.”
* **Acting**: Produce final answer

Copy

Ask AI

```
================================== Ai Message ================================== ================================== Ai Message ================================== I found wireless headphones (model WH-1000XM5) with 10 units in stock...I found wireless headphones (model WH-1000XM5) with 10 units in stock... 
```

To learn more about tools, see [Tools](/oss/python/langchain/tools).

### [​](#system-prompt) System prompt

You can shape how your agent approaches tasks by providing a prompt. The [`system_prompt`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent(system_prompt)) parameter can be provided as a string:

Copy

Ask AI

```
agent = create_agent(agent = create_agent( model, model, tools, tools, system_prompt="You are a helpful assistant. Be concise and accurate."  system_prompt ="You are a helpful assistant. Be concise and accurate."))
```

When no [`system_prompt`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent(system_prompt)) is provided, the agent will infer its task from the messages directly.

#### [​](#dynamic-system-prompt) Dynamic system prompt

For more advanced use cases where you need to modify the system prompt based on runtime context or agent state, you can use [middleware](/oss/python/langchain/middleware). The [`@dynamic_prompt`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.dynamic_prompt) decorator creates middleware that generates system prompts dynamically based on the model request:

Copy

Ask AI

```
from typing import TypedDict from  typing import  TypedDict from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import dynamic_prompt, ModelRequest from langchain.agents.middleware import dynamic_prompt, ModelRequest class Context(TypedDict): class  Context(TypedDict): user_role: str user_role: str @dynamic_prompt @dynamic_promptdef user_role_prompt(request: ModelRequest) -> str: def  user_role_prompt(request: ModelRequest) -> str: """Generate system prompt based on user role.""" """Generate system prompt based on user role.""" user_role = request.runtime.context.get("user_role", "user")  user_role = request.runtime.context.get("user_role", "user") base_prompt = "You are a helpful assistant."  base_prompt = "You are a helpful assistant."  if user_role == "expert":  if  user_role ==  "expert": return f"{base_prompt} Provide detailed technical responses."  return  f "{base_prompt} Provide detailed technical responses." elif user_role == "beginner":  elif  user_role ==  "beginner": return f"{base_prompt} Explain concepts simply and avoid jargon."  return  f "{base_prompt} Explain concepts simply and avoid jargon."  return base_prompt  return  base_prompt agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[web_search],  tools =[web_search], middleware=[user_role_prompt],  middleware =[user_role_prompt], context_schema=Context  context_schema = Context)) # The system prompt will be set dynamically based on context # The system prompt will be set dynamically based on contextresult = agent.invoke(result = agent.invoke( {"messages": [{"role": "user", "content": "Explain machine learning"}]}, {"messages": [{"role": "user", "content": "Explain machine learning"}]}, context={"user_role": "expert"}  context ={"user_role": "expert"}))
```

For more details on message types and formatting, see [Messages](/oss/python/langchain/messages). For comprehensive middleware documentation, see [Middleware](/oss/python/langchain/middleware).

## [​](#invocation) Invocation

You can invoke an agent by passing an update to its [`State`](/oss/python/langgraph/graph-api#state). All agents include a [sequence of messages](/oss/python/langgraph/use-graph-api#messagesstate) in their state; to invoke the agent, pass a new message:

Copy

Ask AI

```
result = agent.invoke(result = agent.invoke( {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]} {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}))
```

For streaming steps and / or tokens from the agent, refer to the [streaming](/oss/python/langchain/streaming) guide. Otherwise, the agent follows the LangGraph [Graph API](/oss/python/langgraph/use-graph-api) and supports all associated methods.

## [​](#advanced-concepts) Advanced concepts

### [​](#structured-output) Structured output

In some situations, you may want the agent to return an output in a specific format. LangChain provides strategies for structured output via the [`response_format`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.ModelRequest(response_format)) parameter.

#### [​](#toolstrategy) ToolStrategy

`ToolStrategy` uses artificial tool calling to generate structured output. This works with any model that supports tool calling:

Copy

Ask AI

```
from pydantic import BaseModel from  pydantic import  BaseModelfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.structured_output import ToolStrategy from langchain.agents.structured_output import  ToolStrategy class ContactInfo(BaseModel): class  ContactInfo(BaseModel): name: str name: str email: str email: str phone: str phone: str agent = create_agent(agent = create_agent( model="gpt-4o-mini",  model ="gpt-4o-mini", tools=[search_tool],  tools =[search_tool], response_format=ToolStrategy(ContactInfo)  response_format =ToolStrategy(ContactInfo))) result = agent.invoke({result = agent.invoke({ "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]  "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]})}) result["structured_response"]result["structured_response"]# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

#### [​](#providerstrategy) ProviderStrategy

`ProviderStrategy` uses the model provider’s native structured output generation. This is more reliable but only works with providers that support native structured output (e.g., OpenAI):

Copy

Ask AI

```
from langchain.agents.structured_output import ProviderStrategy from langchain.agents.structured_output import  ProviderStrategy agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", response_format=ProviderStrategy(ContactInfo)  response_format =ProviderStrategy(ContactInfo)))
```

As of `langchain 1.0`, simply passing a schema (e.g., `response_format=ContactInfo`) is no longer supported. You must explicitly use `ToolStrategy` or `ProviderStrategy`.

To learn about structured output, see [Structured output](/oss/python/langchain/structured-output).

### [​](#memory) Memory

Agents maintain conversation history automatically through the message state. You can also configure the agent to use a custom state schema to remember additional information during the conversation. Information stored in the state can be thought of as the [short-term memory](/oss/python/langchain/short-term-memory) of the agent: Custom state schemas must extend [`AgentState`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.AgentState) as a `TypedDict`. There are two ways to define custom state:

1. Via [middleware](/oss/python/langchain/middleware) (preferred)
2. Via [`state_schema`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state_schema) on [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent)

Defining custom state via middleware is preferred over defining it via [`state_schema`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state_schema) on [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) because it allows you to keep state extensions conceptually scoped to the relevant middleware and tools.[`state_schema`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state_schema) is still supported for backwards compatibility on [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent).

#### [​](#defining-state-via-middleware) Defining state via middleware

Use middleware to define custom state when your custom state needs to be accessed by specific middleware hooks and tools attached to said middleware.

Copy

Ask AI

```
from langchain.agents import AgentState from langchain.agents import  AgentStatefrom langchain.agents.middleware import AgentMiddleware from langchain.agents.middleware import  AgentMiddleware from typing import Any from  typing import  Any class CustomState(AgentState): class  CustomState(AgentState): user_preferences: dict user_preferences: dict class CustomMiddleware(AgentMiddleware): class  CustomMiddleware(AgentMiddleware): state_schema = CustomState  state_schema =  CustomState tools = [tool1, tool2]  tools = [tool1, tool2]  def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:  def  before_model(self, state: CustomState, runtime) -> dict[str, Any] |  None: ... ... agent = create_agent(agent = create_agent( model, model, tools=tools,  tools =tools, middleware=[CustomMiddleware()]  middleware =[CustomMiddleware()])) # The agent can now track additional state beyond messages # The agent can now track additional state beyond messagesresult = agent.invoke({result = agent.invoke({ "messages": [{"role": "user", "content": "I prefer technical explanations"}],  "messages": [{"role": "user", "content": "I prefer technical explanations"}], "user_preferences": {"style": "technical", "verbosity": "detailed"},  "user_preferences": {"style": "technical", "verbosity": "detailed"},})})
```

#### [​](#defining-state-via-state-schema) Defining state via `state_schema`

Use the [`state_schema`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state_schema) parameter as a shortcut to define custom state that is only used in tools.

Copy

Ask AI

```
from langchain.agents import AgentState from langchain.agents import  AgentState class CustomState(AgentState): class  CustomState(AgentState): user_preferences: dict user_preferences: dict agent = create_agent(agent = create_agent( model, model, tools=[tool1, tool2],  tools =[tool1, tool2], state_schema=CustomState  state_schema = CustomState)) # The agent can now track additional state beyond messages # The agent can now track additional state beyond messagesresult = agent.invoke({result = agent.invoke({ "messages": [{"role": "user", "content": "I prefer technical explanations"}],  "messages": [{"role": "user", "content": "I prefer technical explanations"}], "user_preferences": {"style": "technical", "verbosity": "detailed"},  "user_preferences": {"style": "technical", "verbosity": "detailed"},})})
```

As of `langchain 1.0`, custom state schemas **must** be `TypedDict` types. Pydantic models and dataclasses are no longer supported. See the [v1 migration guide](/oss/python/migrate/langchain-v1#state-type-restrictions) for more details.

To learn more about memory, see [Memory](/oss/python/concepts/memory). For information on implementing long-term memory that persists across sessions, see [Long-term memory](/oss/python/langchain/long-term-memory).

### [​](#streaming) Streaming

We’ve seen how the agent can be called with `invoke` to get a final response. If the agent executes multiple steps, this may take a while. To show intermediate progress, we can stream back messages as they occur.

Copy

Ask AI

```
for chunk in agent.stream({for  chunk in agent.stream({ "messages": [{"role": "user", "content": "Search for AI news and summarize the findings"}]  "messages": [{"role": "user", "content": "Search for AI news and summarize the findings"}]}, stream_mode="values"):}, stream_mode = "values"):  # Each chunk contains the full state at that point  # Each chunk contains the full state at that point latest_message = chunk["messages"][-1]  latest_message = chunk["messages"][- 1] if latest_message.content:  if latest_message.content: print(f"Agent: {latest_message.content}")  print(f"Agent: {latest_message.content} ") elif latest_message.tool_calls:  elif latest_message.tool_calls: print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")  print(f"Calling tools: {[tc['name'] for  tc in latest_message.tool_calls]} ")
```

For more details on streaming, see [Streaming](/oss/python/langchain/streaming).

### [​](#middleware) Middleware

[Middleware](/oss/python/langchain/middleware) provides powerful extensibility for customizing agent behavior at different stages of execution. You can use middleware to:

* Process state before the model is called (e.g., message trimming, context injection)
* Modify or validate the model’s response (e.g., guardrails, content filtering)
* Handle tool execution errors with custom logic
* Implement dynamic model selection based on state or context
* Add custom logging, monitoring, or analytics

Middleware integrates seamlessly into the agent’s execution graph, allowing you to intercept and modify data flow at key points without changing the core agent logic.

For comprehensive middleware documentation including decorators like [`@before_model`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.before_model), [`@after_model`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.after_model), and [`@wrap_tool_call`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.wrap_tool_call), see [Middleware](/oss/python/langchain/middleware).

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/agents.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Philosophy](/oss/python/langchain/philosophy)[Models](/oss/python/langchain/models)