Tools - Docs by LangChain

===============

[Skip to main content](https://docs.langchain.com/oss/python/langchain/tools#content-area)

We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page![Image 1: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 2: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)LangChain + LangGraph

Search...

⌘K

*   [GitHub](https://github.com/langchain-ai)
*   [Try LangSmith](https://smith.langchain.com/)
*   [Try LangSmith](https://smith.langchain.com/)

Search...

Navigation

Core components

Tools

[LangChain](https://docs.langchain.com/oss/python/langchain/overview)[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)[Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview)[Integrations](https://docs.langchain.com/oss/python/integrations/providers/overview)[Learn](https://docs.langchain.com/oss/python/learn)[Reference](https://docs.langchain.com/oss/python/reference/overview)[Contribute](https://docs.langchain.com/oss/python/contributing/overview)

Python

*   [Overview](https://docs.langchain.com/oss/python/langchain/overview)

##### LangChain v1.0

*   [Release notes](https://docs.langchain.com/oss/python/releases/langchain-v1)
*   [Migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1)

##### Get started

*   [Install](https://docs.langchain.com/oss/python/langchain/install)
*   [Quickstart](https://docs.langchain.com/oss/python/langchain/quickstart)
*   [Philosophy](https://docs.langchain.com/oss/python/langchain/philosophy)

##### Core components

*   [Agents](https://docs.langchain.com/oss/python/langchain/agents)
*   [Models](https://docs.langchain.com/oss/python/langchain/models)
*   [Messages](https://docs.langchain.com/oss/python/langchain/messages)
*   [Tools](https://docs.langchain.com/oss/python/langchain/tools)
*   [Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)
*   [Streaming](https://docs.langchain.com/oss/python/langchain/streaming)
*   [Middleware](https://docs.langchain.com/oss/python/langchain/middleware)
*   [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)

##### Advanced usage

*   [Guardrails](https://docs.langchain.com/oss/python/langchain/guardrails)
*   [Runtime](https://docs.langchain.com/oss/python/langchain/runtime)
*   [Context engineering](https://docs.langchain.com/oss/python/langchain/context-engineering)
*   [Model Context Protocol (MCP)](https://docs.langchain.com/oss/python/langchain/mcp)
*   [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)
*   [Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
*   [Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)
*   [Long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory)

##### Use in production

*   [Studio](https://docs.langchain.com/oss/python/langchain/studio)
*   [Test](https://docs.langchain.com/oss/python/langchain/test)
*   [Deploy](https://docs.langchain.com/oss/python/langchain/deploy)
*   [Agent Chat UI](https://docs.langchain.com/oss/python/langchain/ui)
*   [Observability](https://docs.langchain.com/oss/python/langchain/observability)

close

On this page
*   [Create tools](https://docs.langchain.com/oss/python/langchain/tools#create-tools)
*   [Basic tool definition](https://docs.langchain.com/oss/python/langchain/tools#basic-tool-definition)
*   [Customize tool properties](https://docs.langchain.com/oss/python/langchain/tools#customize-tool-properties)
*   [Custom tool name](https://docs.langchain.com/oss/python/langchain/tools#custom-tool-name)
*   [Custom tool description](https://docs.langchain.com/oss/python/langchain/tools#custom-tool-description)
*   [Advanced schema definition](https://docs.langchain.com/oss/python/langchain/tools#advanced-schema-definition)
*   [Accessing Context](https://docs.langchain.com/oss/python/langchain/tools#accessing-context)
*   [ToolRuntime](https://docs.langchain.com/oss/python/langchain/tools#toolruntime)
*   [Context](https://docs.langchain.com/oss/python/langchain/tools#context)
*   [Memory (Store)](https://docs.langchain.com/oss/python/langchain/tools#memory-store)
*   [Stream Writer](https://docs.langchain.com/oss/python/langchain/tools#stream-writer)

[Core components](https://docs.langchain.com/oss/python/langchain/agents)

Tools
=====

Copy page

Copy page

Many AI applications interact with users via natural language. However, some use cases require models to interface directly with external systems—such as APIs, databases, or file systems—using structured input.Tools are components that [agents](https://docs.langchain.com/oss/python/langchain/agents) call to perform actions. They extend model capabilities by letting them interact with the world through well-defined inputs and outputs. Tools encapsulate a callable function and its input schema. These can be passed to compatible [chat models](https://docs.langchain.com/oss/python/langchain/models), allowing the model to decide whether to invoke a tool and with what arguments. In these scenarios, tool calling enables models to generate requests that conform to a specified input schema.

**Server-side tool use**Some chat models (e.g., [OpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai), [Anthropic](https://docs.langchain.com/oss/python/integrations/chat/anthropic), and [Gemini](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai)) feature [built-in tools](https://docs.langchain.com/oss/python/langchain/models#server-side-tool-use) that are executed server-side, such as web search and code interpreters. Refer to the [provider overview](https://docs.langchain.com/oss/python/integrations/providers/overview) to learn how to access these tools with your specific chat model.

[​](https://docs.langchain.com/oss/python/langchain/tools#create-tools)

Create tools
-------------------------------------------------------------------------------------

### [​](https://docs.langchain.com/oss/python/langchain/tools#basic-tool-definition)

Basic tool definition

The simplest way to create a tool is with the [`@tool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.tool) decorator. By default, the function’s docstring becomes the tool’s description that helps the model understand when to use it:

Copy

Ask AI

```
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```

Type hints are **required** as they define the tool’s input schema. The docstring should be informative and concise to help the model understand the tool’s purpose.
### [​](https://docs.langchain.com/oss/python/langchain/tools#customize-tool-properties)

Customize tool properties

#### [​](https://docs.langchain.com/oss/python/langchain/tools#custom-tool-name)

Custom tool name

By default, the tool name comes from the function name. Override it when you need something more descriptive:

Copy

Ask AI

```
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # web_search
```

#### [​](https://docs.langchain.com/oss/python/langchain/tools#custom-tool-description)

Custom tool description

Override the auto-generated tool description for clearer model guidance:

Copy

Ask AI

```
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))
```

### [​](https://docs.langchain.com/oss/python/langchain/tools#advanced-schema-definition)

Advanced schema definition

Define complex inputs with Pydantic models or JSON schemas:

Pydantic model

JSON Schema

Copy

Ask AI

```
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

[​](https://docs.langchain.com/oss/python/langchain/tools#accessing-context)

Accessing Context
-----------------------------------------------------------------------------------------------

**Why this matters:** Tools are most powerful when they can access agent state, runtime context, and long-term memory. This enables tools to make context-aware decisions, personalize responses, and maintain information across conversations.Runtime context provides a way to inject dependencies (like database connections, user IDs, or configuration) into your tools at runtime, making them more testable and reusable.

Tools can access runtime information through the `ToolRuntime` parameter, which provides:
*   **State** - Mutable data that flows through execution (e.g., messages, counters, custom fields)
*   **Context** - Immutable configuration like user IDs, session details, or application-specific configuration
*   **Store** - Persistent long-term memory across conversations
*   **Stream Writer** - Stream custom updates as tools execute
*   **Config** - `RunnableConfig` for the execution
*   **Tool Call ID** - ID of the current tool call

### [​](https://docs.langchain.com/oss/python/langchain/tools#toolruntime)

`ToolRuntime`

Use `ToolRuntime` to access all runtime information in a single parameter. Simply add `runtime: ToolRuntime` to your tool signature, and it will be automatically injected without being exposed to the LLM.

**`ToolRuntime`**: A unified parameter that provides tools access to state, context, store, streaming, config, and tool call ID. This replaces the older pattern of using separate [`InjectedState`](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.tool_node.InjectedState), [`InjectedStore`](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.tool_node.InjectedStore), [`get_runtime`](https://reference.langchain.com/python/langgraph/runtime/#langgraph.runtime.get_runtime), and [`InjectedToolCallId`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.InjectedToolCallId) annotations.The runtime automatically provides these capabilities to your tool functions without you having to pass them explicitly or use global state.

**Accessing state:**Tools can access the current graph state using `ToolRuntime`:

Copy

Ask AI

```
from langchain.tools import tool, ToolRuntime

# Access the current conversation state
@tool
def summarize_conversation(
    runtime: ToolRuntime
) -> str:
    """Summarize the conversation so far."""
    messages = runtime.state["messages"]

    human_msgs = sum(1 for m in messages if m.__class__.__name__ == "HumanMessage")
    ai_msgs = sum(1 for m in messages if m.__class__.__name__ == "AIMessage")
    tool_msgs = sum(1 for m in messages if m.__class__.__name__ == "ToolMessage")

    return f"Conversation has {human_msgs} user messages, {ai_msgs} AI responses, and {tool_msgs} tool results"

# Access custom state fields
@tool
def get_user_preference(
    pref_name: str,
    runtime: ToolRuntime  # ToolRuntime parameter is not visible to the model
) -> str:
    """Get a user preference value."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")
```

The `tool_runtime` parameter is hidden from the model. For the example above, the model only sees `pref_name` in the tool schema - `tool_runtime` is _not_ included in the request.

**Updating state:**Use [`Command`](https://reference.langchain.com/python/langgraph/types/#langgraph.types.Command) to update the agent’s state or control the graph’s execution flow:

Copy

Ask AI

```
from langgraph.types import Command
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain.tools import tool, ToolRuntime

# Update the conversation history by removing all messages
@tool
def clear_conversation() -> Command:
    """Clear the conversation history."""

    return Command(
        update={
            "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)],
        }
    )

# Update the user_name in the agent state
@tool
def update_user_name(
    new_name: str,
    runtime: ToolRuntime
) -> Command:
    """Update the user's name."""
    return Command(update={"user_name": new_name})
```

#### [​](https://docs.langchain.com/oss/python/langchain/tools#context)

Context

Access immutable configuration and contextual data like user IDs, session details, or application-specific configuration through `runtime.context`.Tools can access runtime context through `ToolRuntime`:

Copy

Ask AI

```
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

USER_DATABASE = {
    "user123": {
        "name": "Alice Johnson",
        "account_type": "Premium",
        "balance": 5000,
        "email": "alice@example.com"
    },
    "user456": {
        "name": "Bob Smith",
        "account_type": "Standard",
        "balance": 1200,
        "email": "bob@example.com"
    }
}

@dataclass
class UserContext:
    user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's account information."""
    user_id = runtime.context.user_id

    if user_id in USER_DATABASE:
        user = USER_DATABASE[user_id]
        return f"Account holder: {user['name']}\nType: {user['account_type']}\nBalance: ${user['balance']}"
    return "User not found"

model = ChatOpenAI(model="gpt-4o")
agent = create_agent(
    model,
    tools=[get_account_info],
    context_schema=UserContext,
    system_prompt="You are a financial assistant."
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my current balance?"}]},
    context=UserContext(user_id="user123")
)
```

#### [​](https://docs.langchain.com/oss/python/langchain/tools#memory-store)

Memory (Store)

Access persistent data across conversations using the store. The store is accessed via `runtime.store` and allows you to save and retrieve user-specific or application-specific data.Tools can access and update the store through `ToolRuntime`:

Copy

Ask AI

```
from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."

store = InMemoryStore()
agent = create_agent(
    model,
    tools=[get_user_info, save_user_info],
    store=store
)

# First session: save user info
agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev"}]
})

# Second session: get user info
agent.invoke({
    "messages": [{"role": "user", "content": "Get user info for user with id 'abc123'"}]
})
# Here is the user info for user with ID "abc123":
# - Name: Foo
# - Age: 25
# - Email: foo@langchain.dev
```

See all 42 lines

#### [​](https://docs.langchain.com/oss/python/langchain/tools#stream-writer)

Stream Writer

Stream custom updates from tools as they execute using `runtime.stream_writer`. This is useful for providing real-time feedback to users about what a tool is doing.

Copy

Ask AI

```
from langchain.tools import tool, ToolRuntime

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city."""
    writer = runtime.stream_writer

    # Stream custom updates as the tool executes
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")

    return f"It's always sunny in {city}!"
```

If you use `runtime.stream_writer` inside your tool, the tool must be invoked within a LangGraph execution context. See [Streaming](https://docs.langchain.com/oss/python/langchain/streaming) for more details.

* * *

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/tools.mdx)

[Connect these docs programmatically](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

Yes No

[Messages Previous](https://docs.langchain.com/oss/python/langchain/messages)[Short-term memory Next](https://docs.langchain.com/oss/python/langchain/short-term-memory)

⌘I

[Docs by LangChain home page![Image 3: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 4: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

Resources

[Forum](https://forum.langchain.com/)[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Trust Center](https://trust.langchain.com/)

Company

[About](https://langchain.com/about)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

[Powered by Mintlify](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=langchain-5e9cc07a)