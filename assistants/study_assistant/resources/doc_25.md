What's new in v1 - Docs by LangChain

===============

[Skip to main content](https://docs.langchain.com/oss/python/releases/langchain-v1#content-area)

We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page![Image 1: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 2: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)LangChain + LangGraph

Search...

⌘K

*   [GitHub](https://github.com/langchain-ai)
*   [Try LangSmith](https://smith.langchain.com/)
*   [Try LangSmith](https://smith.langchain.com/)

Search...

Navigation

LangChain v1.0

What's new in v1

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

![Image 3: US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

close

On this page
*   [create_agent](https://docs.langchain.com/oss/python/releases/langchain-v1#create-agent)
*   [Middleware](https://docs.langchain.com/oss/python/releases/langchain-v1#middleware)
*   [Prebuilt middleware](https://docs.langchain.com/oss/python/releases/langchain-v1#prebuilt-middleware)
*   [Custom middleware](https://docs.langchain.com/oss/python/releases/langchain-v1#custom-middleware)
*   [Built on LangGraph](https://docs.langchain.com/oss/python/releases/langchain-v1#built-on-langgraph)
*   [Structured output](https://docs.langchain.com/oss/python/releases/langchain-v1#structured-output)
*   [Standard content blocks](https://docs.langchain.com/oss/python/releases/langchain-v1#standard-content-blocks)
*   [Benefits](https://docs.langchain.com/oss/python/releases/langchain-v1#benefits)
*   [Simplified package](https://docs.langchain.com/oss/python/releases/langchain-v1#simplified-package)
*   [Namespace](https://docs.langchain.com/oss/python/releases/langchain-v1#namespace)
*   [langchain-classic](https://docs.langchain.com/oss/python/releases/langchain-v1#langchain-classic)
*   [Migration guide](https://docs.langchain.com/oss/python/releases/langchain-v1#migration-guide)
*   [Reporting issues](https://docs.langchain.com/oss/python/releases/langchain-v1#reporting-issues)
*   [Additional resources](https://docs.langchain.com/oss/python/releases/langchain-v1#additional-resources)
*   [See also](https://docs.langchain.com/oss/python/releases/langchain-v1#see-also)

[LangChain v1.0](https://docs.langchain.com/oss/python/releases/langchain-v1)

What's new in v1
================

Copy page

Copy page

**LangChain v1 is a focused, production-ready foundation for building agents.** We’ve streamlined the framework around three core improvements:

[create_agent ------------ The new standard for building agents in LangChain, replacing `langgraph.prebuilt.create_react_agent`.](https://docs.langchain.com/oss/python/releases/langchain-v1#create-agent)[Standard content blocks ----------------------- A new `content_blocks` property that provides unified access to modern LLM features across providers.](https://docs.langchain.com/oss/python/releases/langchain-v1#standard-content-blocks)[Simplified namespace -------------------- The `langchain` namespace has been streamlined to focus on essential building blocks for agents, with legacy functionality moved to `langchain-classic`.](https://docs.langchain.com/oss/python/releases/langchain-v1#simplified-package)

To upgrade,

pip

uv

Copy

Ask AI

```
pip install -U langchain
```

For a complete list of changes, see the [migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1).
[​](https://docs.langchain.com/oss/python/releases/langchain-v1#create-agent)

`create_agent`
---------------------------------------------------------------------------------------------

[`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) is the standard way to build agents in LangChain 1.0. It provides a simpler interface than [`langgraph.prebuilt.create_react_agent`](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.chat_agent_executor.create_react_agent) while offering greater customization potential by using [middleware](https://docs.langchain.com/oss/python/releases/langchain-v1#middleware).

Copy

Ask AI

```
from langchain.agents import create_agent

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[search_web, analyze_data, send_email],
    system_prompt="You are a helpful research assistant."
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "Research AI safety trends"}
    ]
})
```

Under the hood, [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) is built on the basic agent loop — calling a model, letting it choose tools to execute, and then finishing when it calls no more tools:

![Image 4: Core agent loop diagram](https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=ac72e48317a9ced68fd1be64e89ec063)

For more information, see [Agents](https://docs.langchain.com/oss/python/langchain/agents).
### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#middleware)

Middleware

Middleware is the defining feature of [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent). It offers a highly customizable entry-point, raising the ceiling for what you can build.Great agents require [context engineering](https://docs.langchain.com/oss/python/langchain/context-engineering): getting the right information to the model at the right time. Middleware helps you control dynamic prompts, conversation summarization, selective tool access, state management, and guardrails through a composable abstraction.
#### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#prebuilt-middleware)

Prebuilt middleware

LangChain provides a few [prebuilt middlewares](https://docs.langchain.com/oss/python/langchain/middleware#built-in-middleware) for common patterns, including:
*   [`PIIMiddleware`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.PIIMiddleware): Redact sensitive information before sending to the model
*   [`SummarizationMiddleware`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.SummarizationMiddleware): Condense conversation history when it gets too long
*   [`HumanInTheLoopMiddleware`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.HumanInTheLoopMiddleware): Require approval for sensitive tool calls

Copy

Ask AI

```
from langchain.agents import create_agent
from langchain.agents.middleware import (
    PIIMiddleware,
    SummarizationMiddleware,
    HumanInTheLoopMiddleware
)

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[read_email, send_email],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware(
            "phone_number",
            detector=(
                r"(?:\+?\d{1,3}[\s.-]?)?"
                r"(?:\(?\d{2,4}\)?[\s.-]?)?"
                r"\d{3,4}[\s.-]?\d{4}"
			),
			strategy="block"
        ),
        SummarizationMiddleware(
            model="claude-sonnet-4-5-20250929",
            max_tokens_before_summary=500
        ),
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions": ["approve", "edit", "reject"]
                }
            }
        ),
    ]
)
```

#### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#custom-middleware)

Custom middleware

You can also build custom middleware to fit your needs. Middleware exposes hooks at each step in an agent’s execution:

![Image 5: Middleware flow diagram](https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=eb4404b137edec6f6f0c8ccb8323eaf1)

Build custom middleware by implementing any of these hooks on a subclass of the [`AgentMiddleware`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware) class:

| Hook | When it runs | Use cases |
| --- | --- | --- |
| `before_agent` | Before calling the agent | Load memory, validate input |
| `before_model` | Before each LLM call | Update prompts, trim messages |
| `wrap_model_call` | Around each LLM call | Intercept and modify requests/responses |
| `wrap_tool_call` | Around each tool call | Intercept and modify tool execution |
| `after_model` | After each LLM response | Validate output, apply guardrails |
| `after_agent` | After agent completes | Save results, cleanup |

Example custom middleware:

Copy

Ask AI

```
from dataclasses import dataclass
from typing import Callable

from langchain_openai import ChatOpenAI

from langchain.agents.middleware import (
    AgentMiddleware,
    ModelRequest
)
from langchain.agents.middleware.types import ModelResponse

@dataclass
class Context:
    user_expertise: str = "beginner"

class ExpertiseBasedToolMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        user_level = request.runtime.context.user_expertise

        if user_level == "expert":
            # More powerful model
            model = ChatOpenAI(model="gpt-5")
            tools = [advanced_search, data_analysis]
        else:
            # Less powerful model
            model = ChatOpenAI(model="gpt-5-nano")
            tools = [simple_search, basic_calculator]

        request.model = model
        request.tools = tools
        return handler(request)

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[
        simple_search,
        advanced_search,
        basic_calculator,
        data_analysis
    ],
    middleware=[ExpertiseBasedToolMiddleware()],
    context_schema=Context
)
```

See all 47 lines

For more information, see [the complete middleware guide](https://docs.langchain.com/oss/python/langchain/middleware).
### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#built-on-langgraph)

Built on LangGraph

Because [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) is built on [LangGraph](https://docs.langchain.com/oss/python/langgraph), you automatically get built in support for long running and reliable agents via:

Persistence
-----------

Conversations automatically persist across sessions with built-in checkpointing

Streaming
---------

Stream tokens, tool calls, and reasoning traces in real-time

Human-in-the-loop
-----------------

Pause agent execution for human approval before sensitive actions

Time travel
-----------

Rewind conversations to any point and explore alternate paths and prompts

You don’t need to learn LangGraph to use these features—they work out of the box.
### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#structured-output)

Structured output

[`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) has improved structured output generation:
*   **Main loop integration**: Structured output is now generated in the main loop instead of requiring an additional LLM call
*   **Structured output strategy**: Models can choose between calling tools or using provider-side structured output generation
*   **Cost reduction**: Eliminates extra expense from additional LLM calls

Copy

Ask AI

```
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel

class Weather(BaseModel):
    temperature: float
    condition: str

def weather_tool(city: str) -> str:
    """Get the weather for a city."""
    return f"it's sunny and 70 degrees in {city}"

agent = create_agent(
    "gpt-4o-mini",
    tools=[weather_tool],
    response_format=ToolStrategy(Weather)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in SF?"}]
})

print(repr(result["structured_response"]))
# results in `Weather(temperature=70.0, condition='sunny')`
```

**Error handling**: Control error handling via the `handle_errors` parameter to `ToolStrategy`:
*   **Parsing errors**: Model generates data that doesn’t match desired structure
*   **Multiple tool calls**: Model generates 2+ tool calls for structured output schemas

* * *

[​](https://docs.langchain.com/oss/python/releases/langchain-v1#standard-content-blocks)

Standard content blocks
-----------------------------------------------------------------------------------------------------------------

Content block support is currently only available for the following integrations:
*   [`langchain-anthropic`](https://pypi.org/project/langchain-anthropic/)
*   [`langchain-aws`](https://pypi.org/project/langchain-aws/)
*   [`langchain-openai`](https://pypi.org/project/langchain-openai/)
*   [`langchain-google-genai`](https://pypi.org/project/langchain-google-genai/)
*   [`langchain-ollama`](https://pypi.org/project/langchain-ollama/)

Broader support for content blocks will be rolled out gradually across more providers.

The new [`content_blocks`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.messages.BaseMessage.content_blocks) property introduces a standard representation for message content that works across providers:

Copy

Ask AI

```
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-5-20250929")
response = model.invoke("What's the capital of France?")

# Unified access to content blocks
for block in response.content_blocks:
    if block["type"] == "reasoning":
        print(f"Model reasoning: {block['reasoning']}")
    elif block["type"] == "text":
        print(f"Response: {block['text']}")
    elif block["type"] == "tool_call":
        print(f"Tool call: {block['name']}({block['args']})")
```

### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#benefits)

Benefits

*   **Provider agnostic**: Access reasoning traces, citations, built-in tools (web search, code interpreters, etc.), and other features using the same API regardless of provider
*   **Type safe**: Full type hints for all content block types
*   **Backward compatible**: Standard content can be [loaded lazily](https://docs.langchain.com/oss/python/langchain/messages#standard-content-blocks), so there are no associated breaking changes

For more information, see our guide on [content blocks](https://docs.langchain.com/oss/python/langchain/messages#standard-content-blocks).

* * *

[​](https://docs.langchain.com/oss/python/releases/langchain-v1#simplified-package)

Simplified package
-------------------------------------------------------------------------------------------------------

LangChain v1 streamlines the [`langchain`](https://pypi.org/project/langchain/) package namespace to focus on essential building blocks for agents. The refined namespace exposes the most useful and relevant functionality:
### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#namespace)

Namespace

| Module | What’s available | Notes |
| --- | --- | --- |
| [`langchain.agents`](https://reference.langchain.com/python/langchain/agents) | [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent), [`AgentState`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.AgentState) | Core agent creation functionality |
| [`langchain.messages`](https://reference.langchain.com/python/langchain/messages) | Message types, [content blocks](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ContentBlock), [`trim_messages`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.trim_messages) | Re-exported from @[`langchain-core`] |
| [`langchain.tools`](https://reference.langchain.com/python/langchain/tools) | [`@tool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.tool), [`BaseTool`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.BaseTool), injection helpers | Re-exported from @[`langchain-core`] |
| [`langchain.chat_models`](https://reference.langchain.com/python/langchain/models) | [`init_chat_model`](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model), [`BaseChatModel`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel) | Unified model initialization |
| [`langchain.embeddings`](https://reference.langchain.com/python/langchain/embeddings) | [`Embeddings`](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings), [`init_embeddings`](https://reference.langchain.com/python/langchain_core/embeddings/#langchain_core.embeddings.embeddings.Embeddings) | Embedding models |

Most of these are re-exported from `langchain-core` for convenience, which gives you a focused API surface for building agents.

Copy

Ask AI

```
# Agent building
from langchain.agents import create_agent

# Messages and content
from langchain.messages import AIMessage, HumanMessage

# Tools
from langchain.tools import tool

# Model initialization
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings
```

### [​](https://docs.langchain.com/oss/python/releases/langchain-v1#langchain-classic)

`langchain-classic`

Legacy functionality has moved to [`langchain-classic`](https://pypi.org/project/langchain-classic) to keep the core packages lean and focused.**What’s in `langchain-classic`:**
*   Legacy chains and chain implementations
*   Retrievers (e.g. `MultiQueryRetriever` or anything from the previous `langchain.retrievers` module)
*   The indexing API
*   The hub module (for managing prompts programmatically)
*   [`langchain-community`](https://pypi.org/project/langchain-community) exports
*   Other deprecated functionality

If you use any of this functionality, install [`langchain-classic`](https://pypi.org/project/langchain-classic):

pip

uv

Copy

Ask AI

```
pip install langchain-classic
```

Then update your imports:

Copy

Ask AI

```
from langchain import ...
from langchain_classic import ...

from langchain.chains import ...
from langchain_classic.chains import ...

from langchain.retrievers import ...
from langchain_classic.retrievers import ...

from langchain import hub  
from langchain_classic import hub
```

[​](https://docs.langchain.com/oss/python/releases/langchain-v1#migration-guide)

Migration guide
-------------------------------------------------------------------------------------------------

See our [migration guide](https://docs.langchain.com/oss/python/migrate/langchain-v1) for help updating your code to LangChain v1.
[​](https://docs.langchain.com/oss/python/releases/langchain-v1#reporting-issues)

Reporting issues
---------------------------------------------------------------------------------------------------

Please report any issues discovered with 1.0 on [GitHub](https://github.com/langchain-ai/langchain/issues) using the `'v1'`[label](https://github.com/langchain-ai/langchain/issues?q=state%3Aopen%20label%3Av1).
[​](https://docs.langchain.com/oss/python/releases/langchain-v1#additional-resources)

Additional resources
-----------------------------------------------------------------------------------------------------------

[LangChain 1.0 ------------- Read the announcement](https://blog.langchain.com/langchain-langchain-1-0-alpha-releases/)[Middleware Guide ---------------- Deep dive into middleware](https://blog.langchain.com/agent-middleware/)[Agents Documentation -------------------- Full agent documentation](https://docs.langchain.com/oss/python/langchain/agents)[Message Content --------------- New content blocks API](https://docs.langchain.com/oss/python/langchain/messages#message-content)[Migration guide --------------- How to migrate to LangChain v1](https://docs.langchain.com/oss/python/migrate/langchain-v1)[GitHub ------ Report issues or contribute](https://github.com/langchain-ai/langchain)

[​](https://docs.langchain.com/oss/python/releases/langchain-v1#see-also)

See also
-----------------------------------------------------------------------------------

*   [Versioning](https://docs.langchain.com/oss/python/versioning) - Understanding version numbers
*   [Release policy](https://docs.langchain.com/oss/python/release-policy) - Detailed release policies

* * *

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/python/releases/langchain-v1.mdx)

[Connect these docs programmatically](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

Yes No

[LangChain overview Previous](https://docs.langchain.com/oss/python/langchain/overview)[LangChain v1 migration guide Next](https://docs.langchain.com/oss/python/migrate/langchain-v1)

⌘I

[Docs by LangChain home page![Image 6: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 7: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

Resources

[Forum](https://forum.langchain.com/)[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Trust Center](https://trust.langchain.com/)

Company

[About](https://langchain.com/about)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

[Powered by Mintlify](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=langchain-5e9cc07a)