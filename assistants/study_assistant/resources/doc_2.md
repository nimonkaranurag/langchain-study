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

* [Build a basic agent](#build-a-basic-agent)
* [Build a real-world agent](#build-a-real-world-agent)

[Get started](/oss/python/langchain/install)

# Quickstart

This quickstart takes you from a simple setup to a fully functional AI agent in just a few minutes.

## [​](#build-a-basic-agent) Build a basic agent

Start by creating a simple agent that can answer questions and call tools. The agent will use Claude Sonnet 4.5 as its language model, a basic weather function as a tool, and a simple prompt to guide its behavior.

For this example, you will need to set up a [Claude (Anthropic)](https://www.anthropic.com/) account and get an API key. Then, set the `ANTHROPIC_API_KEY` environment variable in your terminal.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent def get_weather(city: str) -> str: def  get_weather(city: str) -> str: """Get weather for a given city.""" """Get weather for a given city.""" return f"It's always sunny in {city}!"  return  f "It's always sunny in {city}!" agent = create_agent(agent = create_agent( model="claude-sonnet-4-5-20250929",  model ="claude-sonnet-4-5-20250929", tools=[get_weather],  tools =[get_weather], system_prompt="You are a helpful assistant",  system_prompt = "You are a helpful assistant",)) # Run the agent # Run the agentagent.invoke(agent.invoke( {"messages": [{"role": "user", "content": "what is the weather in sf"}]} {"messages": [{"role": "user", "content": "what is the weather in sf"}]}))
```

To learn how to trace your agent with LangSmith, see the [LangSmith documentation](/langsmith/trace-with-langchain).

## [​](#build-a-real-world-agent) Build a real-world agent

Next, build a practical weather forecasting agent that demonstrates key production concepts:

1. **Detailed system prompts** for better agent behavior
2. **Create tools** that integrate with external data
3. **Model configuration** for consistent responses
4. **Structured output** for predictable results
5. **Conversational memory** for chat-like interactions
6. **Create and run the agent** create a fully functional agent

Let’s walk through each step:

1

Define the system prompt

The system prompt defines your agent’s role and behavior. Keep it specific and actionable:

Copy

Ask AI

```
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns. SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns. You have access to two tools:You have access to two tools: - get_weather_for_location: use this to get the weather for a specific location - get_weather_for_location: use this to get the weather for a specific location - get_user_location: use this to get the user's location - get_user_location: use this to get the user's location If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""
```

2

Create tools

[Tools](/oss/python/langchain/tools) let a model interact with external systems by calling functions you define. Tools can depend on [runtime context](/oss/python/langchain/runtime) and also interact with [agent memory](/oss/python/langchain/short-term-memory).Notice below how the `get_user_location` tool uses runtime context:

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclassfrom langchain.tools import tool, ToolRuntime from langchain.tools import tool, ToolRuntime @tool @tooldef get_weather_for_location(city: str) -> str: def  get_weather_for_location(city: str) -> str: """Get weather for a given city.""" """Get weather for a given city.""" return f"It's always sunny in {city}!"  return  f "It's always sunny in {city}!" @dataclass @dataclassclass Context: class  Context: """Custom runtime context schema.""" """Custom runtime context schema.""" user_id: str user_id: str @tool @tooldef get_user_location(runtime: ToolRuntime[Context]) -> str: def  get_user_location(runtime: ToolRuntime[Context]) -> str: """Retrieve user information based on user ID.""" """Retrieve user information based on user ID.""" user_id = runtime.context.user_id  user_id = runtime.context.user_id return "Florida" if user_id == "1" else "SF"  return  "Florida"  if  user_id ==  "1"  else  "SF"
```

Tools should be well-documented: their name, description, and argument names become part of the model’s prompt. LangChain’s [`@tool` decorator](https://reference.langchain.com/python/langchain/tools/#langchain.tools.tool) adds metadata and enables runtime injection via the `ToolRuntime` parameter.

3

Configure your model

Set up your [language model](/oss/python/langchain/models) with the right [parameters](/oss/python/langchain/models#parameters) for your use case:

Copy

Ask AI

```
from langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_model model = init_chat_model(model = init_chat_model( "claude-sonnet-4-5-20250929", "claude-sonnet-4-5-20250929", temperature=0.5,  temperature =0.5, timeout=10,  timeout = 10, max_tokens=1000  max_tokens = 1000))
```

4

Define response format

Optionally, define a structured response format if you need the agent responses to match a specific schema.

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclass # We use a dataclass here, but Pydantic models are also supported.# We use a dataclass here, but Pydantic models are also supported. @dataclass @dataclassclass ResponseFormat: class  ResponseFormat: """Response schema for the agent.""" """Response schema for the agent.""" # A punny response (always required) # A punny response (always required) punny_response: str punny_response: str  # Any interesting information about the weather if available  # Any interesting information about the weather if available weather_conditions: str | None = None weather_conditions: str  |  None =  None
```

5

Add memory

Add [memory](/oss/python/langchain/short-term-memory) to your agent to maintain state across interactions. This allows the agent to remember previous conversations and context.

Copy

Ask AI

```
from langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaver checkpointer = InMemorySaver() checkpointer = InMemorySaver()
```

In production, use a persistent checkpointer that saves to a database. See [Add and manage memory](/oss/python/langgraph/add-memory#manage-short-term-memory) for more details.

6

Create and run the agent

Now assemble your agent with all the components and run it!

Copy

Ask AI

```
agent = create_agent(agent = create_agent( model=model,  model =model, system_prompt=SYSTEM_PROMPT,  system_prompt = SYSTEM_PROMPT, tools=[get_user_location, get_weather_for_location],  tools =[get_user_location, get_weather_for_location], context_schema=Context,  context_schema =Context, response_format=ResponseFormat,  response_format =ResponseFormat, checkpointer=checkpointer  checkpointer = checkpointer)) # `thread_id` is a unique identifier for a given conversation.# `thread_id` is a unique identifier for a given conversation.config = {"configurable": {"thread_id": "1"}} config = {"configurable": {"thread_id": "1"}} response = agent.invoke(response = agent.invoke( {"messages": [{"role": "user", "content": "what is the weather outside?"}]}, {"messages": [{"role": "user", "content": "what is the weather outside?"}]}, config=config,  config =config, context=Context(user_id="1")  context =Context(user_id = "1"))) print(response['structured_response']) print(response['structured_response'])# ResponseFormat(# ResponseFormat(# punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",# punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",# weather_conditions="It's always sunny in Florida!"# weather_conditions="It's always sunny in Florida!"# )# ) # Note that we can continue the conversation using the same `thread_id`.# Note that we can continue the conversation using the same `thread_id`.response = agent.invoke(response = agent.invoke( {"messages": [{"role": "user", "content": "thank you!"}]}, {"messages": [{"role": "user", "content": "thank you!"}]}, config=config,  config =config, context=Context(user_id="1")  context =Context(user_id = "1"))) print(response['structured_response']) print(response['structured_response'])# ResponseFormat(# ResponseFormat(# punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",# punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",# weather_conditions=None# weather_conditions=None# )# )
```

ShowFull example code

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclass from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_modelfrom langchain.tools import tool, ToolRuntime from langchain.tools import tool, ToolRuntimefrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaver  # Define system prompt # Define system promptSYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns. SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns. You have access to two tools:You have access to two tools: - get_weather_for_location: use this to get the weather for a specific location - get_weather_for_location: use this to get the weather for a specific location - get_user_location: use this to get the user's location - get_user_location: use this to get the user's location If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location.""" # Define context schema # Define context schema @dataclass @dataclassclass Context: class  Context: """Custom runtime context schema.""" """Custom runtime context schema.""" user_id: str user_id: str # Define tools # Define tools @tool @tooldef get_weather_for_location(city: str) -> str: def  get_weather_for_location(city: str) -> str: """Get weather for a given city.""" """Get weather for a given city.""" return f"It's always sunny in {city}!"  return  f "It's always sunny in {city}!" @tool @tooldef get_user_location(runtime: ToolRuntime[Context]) -> str: def  get_user_location(runtime: ToolRuntime[Context]) -> str: """Retrieve user information based on user ID.""" """Retrieve user information based on user ID.""" user_id = runtime.context.user_id  user_id = runtime.context.user_id return "Florida" if user_id == "1" else "SF"  return  "Florida"  if  user_id ==  "1"  else  "SF" # Configure model # Configure modelmodel = init_chat_model(model = init_chat_model( "claude-sonnet-4-5-20250929", "claude-sonnet-4-5-20250929", temperature=0  temperature = 0)) # Define response format # Define response format @dataclass @dataclassclass ResponseFormat: class  ResponseFormat: """Response schema for the agent.""" """Response schema for the agent.""" # A punny response (always required) # A punny response (always required) punny_response: str punny_response: str  # Any interesting information about the weather if available  # Any interesting information about the weather if available weather_conditions: str | None = None weather_conditions: str  |  None =  None # Set up memory # Set up memorycheckpointer = InMemorySaver() checkpointer = InMemorySaver() # Create agent # Create agentagent = create_agent(agent = create_agent( model=model,  model =model, system_prompt=SYSTEM_PROMPT,  system_prompt = SYSTEM_PROMPT, tools=[get_user_location, get_weather_for_location],  tools =[get_user_location, get_weather_for_location], context_schema=Context,  context_schema =Context, response_format=ResponseFormat,  response_format =ResponseFormat, checkpointer=checkpointer  checkpointer = checkpointer)) # Run agent # Run agent# `thread_id` is a unique identifier for a given conversation.# `thread_id` is a unique identifier for a given conversation.config = {"configurable": {"thread_id": "1"}} config = {"configurable": {"thread_id": "1"}} response = agent.invoke(response = agent.invoke( {"messages": [{"role": "user", "content": "what is the weather outside?"}]}, {"messages": [{"role": "user", "content": "what is the weather outside?"}]}, config=config,  config =config, context=Context(user_id="1")  context =Context(user_id = "1"))) print(response['structured_response']) print(response['structured_response'])# ResponseFormat(# ResponseFormat(# punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",# punny_response="Florida is still having a 'sun-derful' day! The sunshine is playing 'ray-dio' hits all day long! I'd say it's the perfect weather for some 'solar-bration'! If you were hoping for rain, I'm afraid that idea is all 'washed up' - the forecast remains 'clear-ly' brilliant!",# weather_conditions="It's always sunny in Florida!"# weather_conditions="It's always sunny in Florida!"# )# ) # Note that we can continue the conversation using the same `thread_id`.# Note that we can continue the conversation using the same `thread_id`.response = agent.invoke(response = agent.invoke( {"messages": [{"role": "user", "content": "thank you!"}]}, {"messages": [{"role": "user", "content": "thank you!"}]}, config=config,  config =config, context=Context(user_id="1")  context =Context(user_id = "1"))) print(response['structured_response']) print(response['structured_response'])# ResponseFormat(# ResponseFormat(# punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",# punny_response="You're 'thund-erfully' welcome! It's always a 'breeze' to help you stay 'current' with the weather. I'm just 'cloud'-ing around waiting to 'shower' you with more forecasts whenever you need them. Have a 'sun-sational' day in the Florida sunshine!",# weather_conditions=None# weather_conditions=None# )# )
```

To learn how to trace your agent with LangSmith, see the [LangSmith documentation](/langsmith/trace-with-langchain).

Congratulations! You now have an AI agent that can:

* **Understand context** and remember conversations
* **Use multiple tools** intelligently
* **Provide structured responses** in a consistent format
* **Handle user-specific information** through context
* **Maintain conversation state** across interactions

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/quickstart.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Install LangChain](/oss/python/langchain/install)[Philosophy](/oss/python/langchain/philosophy)