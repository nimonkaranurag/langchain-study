Models - Docs by LangChain

===============

[Skip to main content](https://docs.langchain.com/oss/python/langchain/models#content-area)

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

Models

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
*   [Basic usage](https://docs.langchain.com/oss/python/langchain/models#basic-usage)
*   [Initialize a model](https://docs.langchain.com/oss/python/langchain/models#initialize-a-model)
*   [Key methods](https://docs.langchain.com/oss/python/langchain/models#key-methods)
*   [Parameters](https://docs.langchain.com/oss/python/langchain/models#parameters)
*   [Invocation](https://docs.langchain.com/oss/python/langchain/models#invocation)
*   [Invoke](https://docs.langchain.com/oss/python/langchain/models#invoke)
*   [Stream](https://docs.langchain.com/oss/python/langchain/models#stream)
*   [Batch](https://docs.langchain.com/oss/python/langchain/models#batch)
*   [Tool calling](https://docs.langchain.com/oss/python/langchain/models#tool-calling)
*   [Structured output](https://docs.langchain.com/oss/python/langchain/models#structured-output)
*   [Supported models](https://docs.langchain.com/oss/python/langchain/models#supported-models)
*   [Advanced topics](https://docs.langchain.com/oss/python/langchain/models#advanced-topics)
*   [Multimodal](https://docs.langchain.com/oss/python/langchain/models#multimodal)
*   [Reasoning](https://docs.langchain.com/oss/python/langchain/models#reasoning)
*   [Local models](https://docs.langchain.com/oss/python/langchain/models#local-models)
*   [Prompt caching](https://docs.langchain.com/oss/python/langchain/models#prompt-caching)
*   [Server-side tool use](https://docs.langchain.com/oss/python/langchain/models#server-side-tool-use)
*   [Rate limiting](https://docs.langchain.com/oss/python/langchain/models#rate-limiting)
*   [Base URL or proxy](https://docs.langchain.com/oss/python/langchain/models#base-url-or-proxy)
*   [Log probabilities](https://docs.langchain.com/oss/python/langchain/models#log-probabilities)
*   [Token usage](https://docs.langchain.com/oss/python/langchain/models#token-usage)
*   [Invocation config](https://docs.langchain.com/oss/python/langchain/models#invocation-config)
*   [Configurable models](https://docs.langchain.com/oss/python/langchain/models#configurable-models)

[Core components](https://docs.langchain.com/oss/python/langchain/agents)

Models
======

Copy page

Copy page

[LLMs](https://en.wikipedia.org/wiki/Large_language_model) are powerful AI tools that can interpret and generate text like humans. They’re versatile enough to write content, translate languages, summarize, and answer questions without needing specialized training for each task.In addition to text generation, many models support:
*   [Tool calling](https://docs.langchain.com/oss/python/langchain/models#tool-calling) - calling external tools (like databases queries or API calls) and use results in their responses.
*   [Structured output](https://docs.langchain.com/oss/python/langchain/models#structured-output) - where the model’s response is constrained to follow a defined format.
*   [Multimodality](https://docs.langchain.com/oss/python/langchain/models#multimodal) - process and return data other than text, such as images, audio, and video.
*   [Reasoning](https://docs.langchain.com/oss/python/langchain/models#reasoning) - models perform multi-step reasoning to arrive at a conclusion.

Models are the reasoning engine of [agents](https://docs.langchain.com/oss/python/langchain/agents). They drive the agent’s decision-making process, determining which tools to call, how to interpret results, and when to provide a final answer.The quality and capabilities of the model you choose directly impact your agent’s reliability and performance. Different models excel at different tasks - some are better at following complex instructions, others at structured reasoning, and some support larger context windows for handling more information.LangChain’s standard model interfaces give you access to many different provider integrations, which makes it easy to experiment with and switch between models to find the best fit for your case.

For provider-specific integration information and capabilities, see the provider’s [chat model page](https://docs.langchain.com/oss/python/integrations/chat).

[​](https://docs.langchain.com/oss/python/langchain/models#basic-usage)

Basic usage
------------------------------------------------------------------------------------

Models can be utilized in two ways:
1.   **With agents** - Models can be dynamically specified when creating an [agent](https://docs.langchain.com/oss/python/langchain/agents#model).
2.   **Standalone** - Models can be called directly (outside of the agent loop) for tasks like text generation, classification, or extraction without the need for an agent framework.

The same model interface works in both contexts, which gives you the flexibility to start simple and scale up to more complex agent-based workflows as needed.
### [​](https://docs.langchain.com/oss/python/langchain/models#initialize-a-model)

Initialize a model

The easiest way to get started with a standalone model in LangChain is to use [`init_chat_model`](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model) to initialize one from a [chat model provider](https://docs.langchain.com/oss/python/integrations/chat) of your choice (examples below):

*   OpenAI 
*   Anthropic 
*   Azure 
*   Google Gemini 
*   AWS Bedrock 

👉 Read the [OpenAI chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/openai)

Copy

Ask AI

```
pip install -U "langchain[openai]"
```

init_chat_model

Model Class

Copy

Ask AI

```
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-4.1")
```

Copy

Ask AI

```
response = model.invoke("Why do parrots talk?")
```

See [`init_chat_model`](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model) for more detail, including information on how to pass model [parameters](https://docs.langchain.com/oss/python/langchain/models#parameters).
### [​](https://docs.langchain.com/oss/python/langchain/models#key-methods)

Key methods

[Invoke ------ The model takes messages as input and outputs messages after generating a complete response.](https://docs.langchain.com/oss/python/langchain/models#invoke)[Stream ------ Invoke the model, but stream the output as it is generated in real-time.](https://docs.langchain.com/oss/python/langchain/models#stream)[Batch ----- Send multiple requests to a model in a batch for more efficient processing.](https://docs.langchain.com/oss/python/langchain/models#batch)

In addition to chat models, LangChain provides support for other adjacent technologies, such as embedding models and vector stores. See the [integrations page](https://docs.langchain.com/oss/python/integrations/providers/overview) for details.

[​](https://docs.langchain.com/oss/python/langchain/models#parameters)

Parameters
----------------------------------------------------------------------------------

A chat model takes parameters that can be used to configure its behavior. The full set of supported parameters varies by model and provider, but standard ones include:

[​](https://docs.langchain.com/oss/python/langchain/models#param-model)

model

string

required

The name or identifier of the specific model you want to use with a provider.

[​](https://docs.langchain.com/oss/python/langchain/models#param-api-key)

api_key

string

The key required for authenticating with the model’s provider. This is usually issued when you sign up for access to the model. Often accessed by setting an environment variable.

[​](https://docs.langchain.com/oss/python/langchain/models#param-temperature)

temperature

number

Controls the randomness of the model’s output. A higher number makes responses more creative; lower ones make them more deterministic.

[​](https://docs.langchain.com/oss/python/langchain/models#param-timeout)

timeout

number

The maximum time (in seconds) to wait for a response from the model before canceling the request.

[​](https://docs.langchain.com/oss/python/langchain/models#param-max-tokens)

max_tokens

number

Limits the total number of tokens in the response, effectively controlling how long the output can be.

[​](https://docs.langchain.com/oss/python/langchain/models#param-max-retries)

max_retries

number

The maximum number of attempts the system will make to resend a request if it fails due to issues like network timeouts or rate limits.

Using [`init_chat_model`](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model), pass these parameters as inline `**kwargs`:

Initialize using model parameters

Copy

Ask AI

```
model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    # Kwargs passed to the model:
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
)
```

Each chat model integration may have additional params used to control provider-specific functionality. For example, [`ChatOpenAI`](https://reference.langchain.com/python/integrations/langchain_openai/ChatOpenAI) has `use_responses_api` to dictate whether to use the OpenAI Responses or Completions API.To find all the parameters supported by a given chat model, head to the [chat model integrations](https://docs.langchain.com/oss/python/integrations/chat) page.

* * *

[​](https://docs.langchain.com/oss/python/langchain/models#invocation)

Invocation
----------------------------------------------------------------------------------

A chat model must be invoked to generate an output. There are three primary invocation methods, each suited to different use cases.
### [​](https://docs.langchain.com/oss/python/langchain/models#invoke)

Invoke

The most straightforward way to call a model is to use [`invoke()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.invoke) with a single message or a list of messages.

Single message

Copy

Ask AI

```
response = model.invoke("Why do parrots have colorful feathers?")
print(response)
```

A list of messages can be provided to a model to represent conversation history. Each message has a role that models use to indicate who sent the message in the conversation. See the [messages](https://docs.langchain.com/oss/python/langchain/messages) guide for more detail on roles, types, and content.

Dictionary format

Copy

Ask AI

```
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate: I love programming."},
    {"role": "assistant", "content": "J'adore la programmation."},
    {"role": "user", "content": "Translate: I love building applications."}
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
```

Message objects

Copy

Ask AI

```
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    SystemMessage("You are a helpful assistant that translates English to French."),
    HumanMessage("Translate: I love programming."),
    AIMessage("J'adore la programmation."),
    HumanMessage("Translate: I love building applications.")
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
```

### [​](https://docs.langchain.com/oss/python/langchain/models#stream)

Stream

Most models can stream their output content while it is being generated. By displaying output progressively, streaming significantly improves user experience, particularly for longer responses.Calling [`stream()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.stream) returns an iterator that yields output chunks as they are produced. You can use a loop to process each chunk in real-time:

Basic text streaming

Stream tool calls, reasoning, and other content

Copy

Ask AI

```
for chunk in model.stream("Why do parrots have colorful feathers?"):
    print(chunk.text, end="|", flush=True)
```

As opposed to [`invoke()`](https://docs.langchain.com/oss/python/langchain/models#invoke), which returns a single [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) after the model has finished generating its full response, `stream()` returns multiple [`AIMessageChunk`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessageChunk) objects, each containing a portion of the output text. Importantly, each chunk in a stream is designed to be gathered into a full message via summation:

Construct an AIMessage

Copy

Ask AI

```
full = None  # None | AIMessageChunk
for chunk in model.stream("What color is the sky?"):
    full = chunk if full is None else full + chunk
    print(full.text)

# The
# The sky
# The sky is
# The sky is typically
# The sky is typically blue
# ...

print(full.content_blocks)
# [{"type": "text", "text": "The sky is typically blue..."}]
```

The resulting message can be treated the same as a message that was generated with [`invoke()`](https://docs.langchain.com/oss/python/langchain/models#invoke) - for example, it can be aggregated into a message history and passed back to the model as conversational context.

Streaming only works if all steps in the program know how to process a stream of chunks. For instance, an application that isn’t streaming-capable would be one that needs to store the entire output in memory before it can be processed.

Advanced streaming topics

"Auto-streaming" chat models

LangChain simplifies streaming from chat models by automatically enabling streaming mode in certain cases, even when you’re not explicitly calling the streaming methods. This is particularly useful when you use the non-streaming invoke method but still want to stream the entire application, including intermediate results from the chat model.In [LangGraph agents](https://docs.langchain.com/oss/python/langchain/agents), for example, you can call `model.invoke()` within nodes, but LangChain will automatically delegate to streaming if running in a streaming mode.
#### [​](https://docs.langchain.com/oss/python/langchain/models#how-it-works)

How it works

When you `invoke()` a chat model, LangChain will automatically switch to an internal streaming mode if it detects that you are trying to stream the overall application. The result of the invocation will be the same as far as the code that was using invoke is concerned; however, while the chat model is being streamed, LangChain will take care of invoking [`on_llm_new_token`](https://reference.langchain.com/python/langchain_core/callbacks/#langchain_core.callbacks.base.AsyncCallbackHandler.on_llm_new_token) events in LangChain’s callback system.Callback events allow LangGraph `stream()` and [`astream_events()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.astream_events) to surface the chat model’s output in real-time.

Streaming events

LangChain chat models can also stream semantic events using [`astream_events()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.astream_events).This simplifies filtering based on event types and other metadata, and will aggregate the full message in the background. See below for an example.

Copy

Ask AI

```
async for event in model.astream_events("Hello"):

    if event["event"] == "on_chat_model_start":
        print(f"Input: {event['data']['input']}")

    elif event["event"] == "on_chat_model_stream":
        print(f"Token: {event['data']['chunk'].text}")

    elif event["event"] == "on_chat_model_end":
        print(f"Full message: {event['data']['output'].text}")

    else:
        pass
```

Copy

Ask AI

```
Input: Hello
Token: Hi
Token:  there
Token: !
Token:  How
Token:  can
Token:  I
...
Full message: Hi there! How can I help today?
```

See the [`astream_events()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.astream_events) reference for event types and other details.

### [​](https://docs.langchain.com/oss/python/langchain/models#batch)

Batch

Batching a collection of independent requests to a model can significantly improve performance and reduce costs, as the processing can be done in parallel:

Batch

Copy

Ask AI

```
responses = model.batch([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])
for response in responses:
    print(response)
```

This section describes a chat model method [`batch()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch), which parallelizes model calls client-side.It is **distinct** from batch APIs supported by inference providers, such as [OpenAI](https://platform.openai.com/docs/guides/batch) or [Anthropic](https://docs.claude.com/en/docs/build-with-claude/batch-processing#message-batches-api).

By default, [`batch()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch) will only return the final output for the entire batch. If you want to receive the output for each individual input as it finishes generating, you can stream results with [`batch_as_completed()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch_as_completed):

Yield batch responses upon completion

Copy

Ask AI

```
for response in model.batch_as_completed([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
]):
    print(response)
```

When using [`batch_as_completed()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch_as_completed), results may arrive out of order. Each includes the input index for matching to reconstruct the original order as needed.

When processing a large number of inputs using [`batch()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch) or [`batch_as_completed()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch_as_completed), you may want to control the maximum number of parallel calls. This can be done by setting the [`max_concurrency`](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.RunnableConfig.max_concurrency) attribute in the [`RunnableConfig`](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.RunnableConfig) dictionary.

Batch with max concurrency

Copy

Ask AI

```
model.batch(
    list_of_inputs,
    config={
        'max_concurrency': 5,  # Limit to 5 parallel calls
    }
)
```

See the [`RunnableConfig`](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.RunnableConfig) reference for a full list of supported attributes.

For more details on batching, see the [reference](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch).

* * *

[​](https://docs.langchain.com/oss/python/langchain/models#tool-calling)

Tool calling
--------------------------------------------------------------------------------------

Models can request to call tools that perform tasks such as fetching data from a database, searching the web, or running code. Tools are pairings of:
1.   A schema, including the name of the tool, a description, and/or argument definitions (often a JSON schema)
2.   A function or coroutine to execute.

You may hear the term “function calling”. We use this interchangeably with “tool calling”.

Here’s the basic tool calling flow between a user and a model:To make tools that you have defined available for use by a model, you must bind them using [`bind_tools`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.bind_tools). In subsequent invocations, the model can choose to call any of the bound tools as needed.Some model providers offer built-in tools that can be enabled via model or invocation parameters (e.g. [`ChatOpenAI`](https://docs.langchain.com/oss/python/integrations/chat/openai), [`ChatAnthropic`](https://docs.langchain.com/oss/python/integrations/chat/anthropic)). Check the respective [provider reference](https://docs.langchain.com/oss/python/integrations/providers/overview) for details.

See the [tools guide](https://docs.langchain.com/oss/python/langchain/tools) for details and other options for creating tools.

Binding user tools

Copy

Ask AI

```
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

model_with_tools = model.bind_tools([get_weather])  

response = model_with_tools.invoke("What's the weather like in Boston?")
for tool_call in response.tool_calls:
    # View tool calls made by the model
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
```

When binding user-defined tools, the model’s response includes a **request** to execute a tool. When using a model separately from an [agent](https://docs.langchain.com/oss/python/langchain/agents), it is up to you to execute the requested tool and return the result back to the model for use in subsequent reasoning. When using an [agent](https://docs.langchain.com/oss/python/langchain/agents), the agent loop will handle the tool execution loop for you.Below, we show some common ways you can use tool calling.

Tool execution loop

When a model returns tool calls, you need to execute the tools and pass the results back to the model. This creates a conversation loop where the model can use tool results to generate its final response. LangChain includes [agent](https://docs.langchain.com/oss/python/langchain/agents) abstractions that handle this orchestration for you.Here’s a simple example of how to do this:

Tool execution loop

Copy

Ask AI

```
# Bind (potentially multiple) tools to the model
model_with_tools = model.bind_tools([get_weather])

# Step 1: Model generates tool calls
messages = [{"role": "user", "content": "What's the weather in Boston?"}]
ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

# Step 2: Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    # Execute the tool with the generated arguments
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)

# Step 3: Pass results back to model for final response
final_response = model_with_tools.invoke(messages)
print(final_response.text)
# "The current weather in Boston is 72°F and sunny."
```

Each [`ToolMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage) returned by the tool includes a `tool_call_id` that matches the original tool call, helping the model correlate results with requests.

Forcing tool calls

By default, the model has the freedom to choose which bound tool to use based on the user’s input. However, you might want to force choosing a tool, ensuring the model uses either a particular tool or **any** tool from a given list:

Force use of any tool

Force use of specific tools

Copy

Ask AI

```
model_with_tools = model.bind_tools([tool_1], tool_choice="any")
```

Parallel tool calls

Many models support calling multiple tools in parallel when appropriate. This allows the model to gather information from different sources simultaneously.

Parallel tool calls

Copy

Ask AI

```
model_with_tools = model.bind_tools([get_weather])

response = model_with_tools.invoke(
    "What's the weather in Boston and Tokyo?"
)

# The model may generate multiple tool calls
print(response.tool_calls)
# [
#   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
#   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
# ]

# Execute all tools (can be done in parallel with async)
results = []
for tool_call in response.tool_calls:
    if tool_call['name'] == 'get_weather':
        result = get_weather.invoke(tool_call)
    ...
    results.append(result)
```

The model intelligently determines when parallel execution is appropriate based on the independence of the requested operations.

Most models supporting tool calling enable parallel tool calls by default. Some (including [OpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai) and [Anthropic](https://docs.langchain.com/oss/python/integrations/chat/anthropic)) allow you to disable this feature. To do this, set `parallel_tool_calls=False`:

Copy

Ask AI

```
model.bind_tools([get_weather], parallel_tool_calls=False)
```

Streaming tool calls

When streaming responses, tool calls are progressively built through [`ToolCallChunk`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolCallChunk). This allows you to see tool calls as they’re being generated rather than waiting for the complete response.

Streaming tool calls

Copy

Ask AI

```
for chunk in model_with_tools.stream(
    "What's the weather in Boston and Tokyo?"
):
    # Tool call chunks arrive progressively
    for tool_chunk in chunk.tool_call_chunks:
        if name := tool_chunk.get("name"):
            print(f"Tool: {name}")
        if id_ := tool_chunk.get("id"):
            print(f"ID: {id_}")
        if args := tool_chunk.get("args"):
            print(f"Args: {args}")

# Output:
# Tool: get_weather
# ID: call_SvMlU1TVIZugrFLckFE2ceRE
# Args: {"lo
# Args: catio
# Args: n": "B
# Args: osto
# Args: n"}
# Tool: get_weather
# ID: call_QMZdy6qInx13oWKE7KhuhOLR
# Args: {"lo
# Args: catio
# Args: n": "T
# Args: okyo
# Args: "}
```

You can accumulate chunks to build complete tool calls:

Accumulate tool calls

Copy

Ask AI

```
gathered = None
for chunk in model_with_tools.stream("What's the weather in Boston?"):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)
```

* * *

[​](https://docs.langchain.com/oss/python/langchain/models#structured-output)

Structured output
------------------------------------------------------------------------------------------------

Models can be requested to provide their response in a format matching a given schema. This is useful for ensuring the output can be easily parsed and used in subsequent processing. LangChain supports multiple schema types and methods for enforcing structured output.

*   Pydantic 
*   TypedDict 
*   JSON Schema 

[Pydantic models](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) provide the richest feature set with field validation, descriptions, and nested structures.

Copy

Ask AI

```
from pydantic import BaseModel, Field

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(..., description="The title of the movie")
    year: int = Field(..., description="The year the movie was released")
    director: str = Field(..., description="The director of the movie")
    rating: float = Field(..., description="The movie's rating out of 10")

model_with_structure = model.with_structured_output(Movie)
response = model_with_structure.invoke("Provide details about the movie Inception")
print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
```

**Key considerations for structured output:**
*   **Method parameter**: Some providers support different methods (`'json_schema'`, `'function_calling'`, `'json_mode'`)
    *   `'json_schema'` typically refers to dedicated structured output features offered by a provider
    *   `'function_calling'` derives structured output by forcing a [tool call](https://docs.langchain.com/oss/python/langchain/models#tool-calling) following the given schema
    *   `'json_mode'` is a precursor to `'json_schema'` offered by some providers - it generates valid json, but the schema must be described in the prompt

*   **Include raw**: Use `include_raw=True` to get both the parsed output and the raw AI message
*   **Validation**: Pydantic models provide automatic validation, while `TypedDict` and JSON Schema require manual validation

Example: Message output alongside parsed structure

It can be useful to return the raw [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) object alongside the parsed representation to access response metadata such as [token counts](https://docs.langchain.com/oss/python/langchain/models#token-usage). To do this, set [`include_raw=True`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.with_structured_output(include_raw)) when calling [`with_structured_output`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.with_structured_output):

Copy

Ask AI

```
from pydantic import BaseModel, Field

class Movie(BaseModel):
    """A movie with details."""
    title: str = Field(..., description="The title of the movie")
    year: int = Field(..., description="The year the movie was released")
    director: str = Field(..., description="The director of the movie")
    rating: float = Field(..., description="The movie's rating out of 10")

model_with_structure = model.with_structured_output(Movie, include_raw=True)  
response = model_with_structure.invoke("Provide details about the movie Inception")
response
# {
#     "raw": AIMessage(...),
#     "parsed": Movie(title=..., year=..., ...),
#     "parsing_error": None,
# }
```

Example: Nested structures

Schemas can be nested:

Pydantic BaseModel

TypedDict

Copy

Ask AI

```
from pydantic import BaseModel, Field

class Actor(BaseModel):
    name: str
    role: str

class MovieDetails(BaseModel):
    title: str
    year: int
    cast: list[Actor]
    genres: list[str]
    budget: float | None = Field(None, description="Budget in millions USD")

model_with_structure = model.with_structured_output(MovieDetails)
```

* * *

[​](https://docs.langchain.com/oss/python/langchain/models#supported-models)

Supported models
----------------------------------------------------------------------------------------------

LangChain supports all major model providers, including OpenAI, Anthropic, Google, Azure, AWS Bedrock, and more. Each provider offers a variety of models with different capabilities. For a full list of supported models in LangChain, see the [integrations page](https://docs.langchain.com/oss/python/integrations/providers/overview).

* * *

[​](https://docs.langchain.com/oss/python/langchain/models#advanced-topics)

Advanced topics
--------------------------------------------------------------------------------------------

### [​](https://docs.langchain.com/oss/python/langchain/models#multimodal)

Multimodal

Certain models can process and return non-textual data such as images, audio, and video. You can pass non-textual data to a model by providing [content blocks](https://docs.langchain.com/oss/python/langchain/messages#message-content).

All LangChain chat models with underlying multimodal capabilities support:
1.   Data in the cross-provider standard format (see [our messages guide](https://docs.langchain.com/oss/python/langchain/messages))
2.   OpenAI [chat completions](https://platform.openai.com/docs/api-reference/chat) format
3.   Any format that is native to that specific provider (e.g., Anthropic models accept Anthropic native format)

See the [multimodal section](https://docs.langchain.com/oss/python/langchain/messages#multimodal) of the messages guide for details.Some models can return multimodal data as part of their response. If invoked to do so, the resulting [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) will have content blocks with multimodal types.

Multimodal output

Copy

Ask AI

```
response = model.invoke("Create a picture of a cat")
print(response.content_blocks)
# [
#     {"type": "text", "text": "Here's a picture of a cat"},
#     {"type": "image", "base64": "...", "mime_type": "image/jpeg"},
# ]
```

See the [integrations page](https://docs.langchain.com/oss/python/integrations/providers/overview) for details on specific providers.
### [​](https://docs.langchain.com/oss/python/langchain/models#reasoning)

Reasoning

Newer models are capable of performing multi-step reasoning to arrive at a conclusion. This involves breaking down complex problems into smaller, more manageable steps.**If supported by the underlying model,** you can surface this reasoning process to better understand how the model arrived at its final answer.

Stream reasoning output

Complete reasoning output

Copy

Ask AI

```
for chunk in model.stream("Why do parrots have colorful feathers?"):
    reasoning_steps = [r for r in chunk.content_blocks if r["type"] == "reasoning"]
    print(reasoning_steps if reasoning_steps else chunk.text)
```

Depending on the model, you can sometimes specify the level of effort it should put into reasoning. Similarly, you can request that the model turn off reasoning entirely. This may take the form of categorical “tiers” of reasoning (e.g., `'low'` or `'high'`) or integer token budgets.For details, see the [integrations page](https://docs.langchain.com/oss/python/integrations/providers/overview) or [reference](https://reference.langchain.com/python/integrations/) for your respective chat model.
### [​](https://docs.langchain.com/oss/python/langchain/models#local-models)

Local models

LangChain supports running models locally on your own hardware. This is useful for scenarios where either data privacy is critical, you want to invoke a custom model, or when you want to avoid the costs incurred when using a cloud-based model.[Ollama](https://docs.langchain.com/oss/python/integrations/chat/ollama) is one of the easiest ways to run models locally. See the full list of local integrations on the [integrations page](https://docs.langchain.com/oss/python/integrations/providers/overview).
### [​](https://docs.langchain.com/oss/python/langchain/models#prompt-caching)

Prompt caching

Many providers offer prompt caching features to reduce latency and cost on repeat processing of the same tokens. These features can be **implicit** or **explicit**:
*   **Implicit prompt caching:** providers will automatically pass on cost savings if a request hits a cache. Examples: [OpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai) and [Gemini](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai) (Gemini 2.5 and above).
*   **Explicit caching:** providers allow you to manually indicate cache points for greater control or to guarantee cost savings. Examples: [`ChatOpenAI`](https://reference.langchain.com/python/integrations/langchain_openai/ChatOpenAI) (via `prompt_cache_key`), Anthropic’s [`AnthropicPromptCachingMiddleware`](https://docs.langchain.com/oss/python/integrations/chat/anthropic#prompt-caching) and [`cache_control`](https://docs.langchain.com/oss/python/integrations/chat/anthropic#prompt-caching) options, [AWS Bedrock](https://docs.langchain.com/oss/python/integrations/chat/bedrock#prompt-caching), [Gemini](https://python.langchain.com/api_reference/google_genai/chat_models/langchain_google_genai.chat_models.ChatGoogleGenerativeAI.html).

Prompt caching is often only engaged above a minimum input token threshold. See [provider pages](https://docs.langchain.com/oss/python/integrations/chat) for details.

Cache usage will be reflected in the [usage metadata](https://docs.langchain.com/oss/python/langchain/messages#token-usage) of the model response.
### [​](https://docs.langchain.com/oss/python/langchain/models#server-side-tool-use)

Server-side tool use

Some providers support server-side [tool-calling](https://docs.langchain.com/oss/python/langchain/models#tool-calling) loops: models can interact with web search, code interpreters, and other tools and analyze the results in a single conversational turn.If a model invokes a tool server-side, the content of the response message will include content representing the invocation and result of the tool. Accessing the [content blocks](https://docs.langchain.com/oss/python/langchain/messages#standard-content-blocks) of the response will return the server-side tool calls and results in a provider-agnostic format:

Invoke with server-side tool use

Copy

Ask AI

```
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1-mini")

tool = {"type": "web_search"}
model_with_tools = model.bind_tools([tool])

response = model_with_tools.invoke("What was a positive news story from today?")
response.content_blocks
```

Result

Copy

Ask AI

```
[
    {
        "type": "server_tool_call",
        "name": "web_search",
        "args": {
            "query": "positive news stories today",
            "type": "search"
        },
        "id": "ws_abc123"
    },
    {
        "type": "server_tool_result",
        "tool_call_id": "ws_abc123",
        "status": "success"
    },
    {
        "type": "text",
        "text": "Here are some positive news stories from today...",
        "annotations": [
            {
                "end_index": 410,
                "start_index": 337,
                "title": "article title",
                "type": "citation",
                "url": "..."
            }
        ]
    }
]
```

See all 29 lines

This represents a single conversational turn; there are no associated [ToolMessage](https://docs.langchain.com/oss/python/langchain/messages#tool-message) objects that need to be passed in as in client-side [tool-calling](https://docs.langchain.com/oss/python/langchain/models#tool-calling).See the [integration page](https://docs.langchain.com/oss/python/integrations/chat) for your given provider for available tools and usage details.
### [​](https://docs.langchain.com/oss/python/langchain/models#rate-limiting)

Rate limiting

Many chat model providers impose a limit on the number of invocations that can be made in a given time period. If you hit a rate limit, you will typically receive a rate limit error response from the provider, and will need to wait before making more requests.To help manage rate limits, chat model integrations accept a `rate_limiter` parameter that can be provided during initialization to control the rate at which requests are made.

Initialize and use a rate limiter

LangChain in comes with (an optional) built-in [`InMemoryRateLimiter`](https://reference.langchain.com/python/langchain_core/rate_limiters/#langchain_core.rate_limiters.InMemoryRateLimiter). This limiter is thread safe and can be shared by multiple threads in the same process.

Define a rate limiter

Copy

Ask AI

```
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # 1 request every 10s
    check_every_n_seconds=0.1,  # Check every 100ms whether allowed to make a request
    max_bucket_size=10,  # Controls the maximum burst size.
)

model = init_chat_model(
    model="gpt-5",
    model_provider="openai",
    rate_limiter=rate_limiter  
)
```

The provided rate limiter can only limit the number of requests per unit time. It will not help if you need to also limit based on the size of the requests.

### [​](https://docs.langchain.com/oss/python/langchain/models#base-url-or-proxy)

Base URL or proxy

For many chat model integrations, you can configure the base URL for API requests, which allows you to use model providers that have OpenAI-compatible APIs or to use a proxy server.

Base URL

Many model providers offer OpenAI-compatible APIs (e.g., [Together AI](https://www.together.ai/), [vLLM](https://github.com/vllm-project/vllm)). You can use [`init_chat_model`](https://reference.langchain.com/python/langchain/models/#langchain.chat_models.init_chat_model) with these providers by specifying the appropriate `base_url` parameter:

Copy

Ask AI

```
model = init_chat_model(
    model="MODEL_NAME",
    model_provider="openai",
    base_url="BASE_URL",
    api_key="YOUR_API_KEY",
)
```

When using direct chat model class instantiation, the parameter name may vary by provider. Check the respective [reference](https://docs.langchain.com/oss/python/integrations/providers/overview) for details.

Proxy configuration

For deployments requiring HTTP proxies, some model integrations support proxy configuration:

Copy

Ask AI

```
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o",
    openai_proxy="http://proxy.example.com:8080"
)
```

Proxy support varies by integration. Check the specific model provider’s [reference](https://docs.langchain.com/oss/python/integrations/providers/overview) for proxy configuration options.

### [​](https://docs.langchain.com/oss/python/langchain/models#log-probabilities)

Log probabilities

Certain models can be configured to return token-level log probabilities representing the likelihood of a given token by setting the `logprobs` parameter when initializing the model:

Copy

Ask AI

```
model = init_chat_model(
    model="gpt-4o",
    model_provider="openai"
).bind(logprobs=True)

response = model.invoke("Why do parrots talk?")
print(response.response_metadata["logprobs"])
```

### [​](https://docs.langchain.com/oss/python/langchain/models#token-usage)

Token usage

A number of model providers return token usage information as part of the invocation response. When available, this information will be included on the [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) objects produced by the corresponding model. For more details, see the [messages](https://docs.langchain.com/oss/python/langchain/messages) guide.

Some provider APIs, notably OpenAI and Azure OpenAI chat completions, require users opt-in to receiving token usage data in streaming contexts. See the [streaming usage metadata](https://docs.langchain.com/oss/python/integrations/chat/openai#streaming-usage-metadata) section of the integration guide for details.

You can track aggregate token counts across models in an application using either a callback or context manager, as shown below:

*   Callback handler 
*   Context manager 

Copy

Ask AI

```
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import UsageMetadataCallbackHandler

model_1 = init_chat_model(model="gpt-4o-mini")
model_2 = init_chat_model(model="claude-haiku-4-5-20251001")

callback = UsageMetadataCallbackHandler()
result_1 = model_1.invoke("Hello", config={"callbacks": [callback]})
result_2 = model_2.invoke("Hello", config={"callbacks": [callback]})
callback.usage_metadata
```

Copy

Ask AI

```
{
    'gpt-4o-mini-2024-07-18': {
        'input_tokens': 8,
        'output_tokens': 10,
        'total_tokens': 18,
        'input_token_details': {'audio': 0, 'cache_read': 0},
        'output_token_details': {'audio': 0, 'reasoning': 0}
    },
    'claude-haiku-4-5-20251001': {
        'input_tokens': 8,
        'output_tokens': 21,
        'total_tokens': 29,
        'input_token_details': {'cache_read': 0, 'cache_creation': 0}
    }
}
```

### [​](https://docs.langchain.com/oss/python/langchain/models#invocation-config)

Invocation config

When invoking a model, you can pass additional configuration through the `config` parameter using a [`RunnableConfig`](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.RunnableConfig) dictionary. This provides run-time control over execution behavior, callbacks, and metadata tracking.Common configuration options include:

Invocation with config

Copy

Ask AI

```
response = model.invoke(
    "Tell me a joke",
    config={
        "run_name": "joke_generation",      # Custom name for this run
        "tags": ["humor", "demo"],          # Tags for categorization
        "metadata": {"user_id": "123"},     # Custom metadata
        "callbacks": [my_callback_handler], # Callback handlers
    }
)
```

These configuration values are particularly useful when:
*   Debugging with [LangSmith](https://docs.smith.langchain.com/) tracing
*   Implementing custom logging or monitoring
*   Controlling resource usage in production
*   Tracking invocations across complex pipelines

Key configuration attributes

[​](https://docs.langchain.com/oss/python/langchain/models#param-run-name)

run_name

string

Identifies this specific invocation in logs and traces. Not inherited by sub-calls.

[​](https://docs.langchain.com/oss/python/langchain/models#param-tags)

tags

string[]

Labels inherited by all sub-calls for filtering and organization in debugging tools.

[​](https://docs.langchain.com/oss/python/langchain/models#param-metadata)

metadata

object

Custom key-value pairs for tracking additional context, inherited by all sub-calls.

[​](https://docs.langchain.com/oss/python/langchain/models#param-max-concurrency)

max_concurrency

number

Controls the maximum number of parallel calls when using [`batch()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch) or [`batch_as_completed()`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.batch_as_completed).

[​](https://docs.langchain.com/oss/python/langchain/models#param-callbacks)

callbacks

array

Handlers for monitoring and responding to events during execution.

[​](https://docs.langchain.com/oss/python/langchain/models#param-recursion-limit)

recursion_limit

number

Maximum recursion depth for chains to prevent infinite loops in complex pipelines.

See full [`RunnableConfig`](https://reference.langchain.com/python/langchain_core/runnables/#langchain_core.runnables.RunnableConfig) reference for all supported attributes.

### [​](https://docs.langchain.com/oss/python/langchain/models#configurable-models)

Configurable models

You can also create a runtime-configurable model by specifying [`configurable_fields`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.language_models.chat_models.BaseChatModel.configurable_fields). If you don’t specify a model value, then `'model'` and `'model_provider'` will be configurable by default.

Copy

Ask AI

```
from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(temperature=0)

configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "gpt-5-nano"}},  # Run with GPT-5-Nano
)
configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "claude-sonnet-4-5-20250929"}},  # Run with Claude
)
```

Configurable model with default values

We can create a configurable model with default model values, specify which parameters are configurable, and add prefixes to configurable params:

Copy

Ask AI

```
first_model = init_chat_model(
        model="gpt-4.1-mini",
        temperature=0,
        configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
        config_prefix="first",  # Useful when you have a chain with multiple models
)

first_model.invoke("what's your name")
```

Copy

Ask AI

```
first_model.invoke(
    "what's your name",
    config={
        "configurable": {
            "first_model": "claude-sonnet-4-5-20250929",
            "first_temperature": 0.5,
            "first_max_tokens": 100,
        }
    },
)
```

Using a configurable model declaratively

We can call declarative operations like `bind_tools`, `with_structured_output`, `with_configurable`, etc. on a configurable model and chain a configurable model in the same way that we would a regularly instantiated chat model object.

Copy

Ask AI

```
from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    """Get the current weather in a given location"""

        location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

class GetPopulation(BaseModel):
    """Get the current population in a given location"""

        location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

model = init_chat_model(temperature=0)
model_with_tools = model.bind_tools([GetWeather, GetPopulation])

model_with_tools.invoke(
    "what's bigger in 2024 LA or NYC", config={"configurable": {"model": "gpt-4.1-mini"}}
).tool_calls
```

Copy

Ask AI

```
[
    {
        'name': 'GetPopulation',
        'args': {'location': 'Los Angeles, CA'},
        'id': 'call_Ga9m8FAArIyEjItHmztPYA22',
        'type': 'tool_call'
    },
    {
        'name': 'GetPopulation',
        'args': {'location': 'New York, NY'},
        'id': 'call_jh2dEvBaAHRaw5JUDthOs7rt',
        'type': 'tool_call'
    }
]
```

Copy

Ask AI

```
model_with_tools.invoke(
    "what's bigger in 2024 LA or NYC",
    config={"configurable": {"model": "claude-sonnet-4-5-20250929"}},
).tool_calls
```

Copy

Ask AI

```
[
    {
        'name': 'GetPopulation',
        'args': {'location': 'Los Angeles, CA'},
        'id': 'toolu_01JMufPf4F4t2zLj7miFeqXp',
        'type': 'tool_call'
    },
    {
        'name': 'GetPopulation',
        'args': {'location': 'New York City, NY'},
        'id': 'toolu_01RQBHcE8kEEbYTuuS8WqY1u',
        'type': 'tool_call'
    }
]
```

* * *

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/models.mdx)

[Connect these docs programmatically](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

Yes No

[Agents Previous](https://docs.langchain.com/oss/python/langchain/agents)[Messages Next](https://docs.langchain.com/oss/python/langchain/messages)

⌘I

[Docs by LangChain home page![Image 3: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 4: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

Resources

[Forum](https://forum.langchain.com/)[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Trust Center](https://trust.langchain.com/)

Company

[About](https://langchain.com/about)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

[Powered by Mintlify](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=langchain-5e9cc07a)