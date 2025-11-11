We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

##### LangChain v1.0

* [Release notes](/oss/python/releases/langchain-v1)
* [Migration guide](/oss/python/migrate/langchain-v1)

##### Get started

##### Core components

* [Short-term memory](/oss/python/langchain/short-term-memory)
* [Middleware](/oss/python/langchain/middleware)
* [Structured output](/oss/python/langchain/structured-output)

##### Advanced usage

* [Context engineering](/oss/python/langchain/context-engineering)
* [Model Context Protocol (MCP)](/oss/python/langchain/mcp)


* [Long-term memory](/oss/python/langchain/long-term-memory)

##### Use in production

* [Agent Chat UI](/oss/python/langchain/ui)

* [What can middleware do?](#what-can-middleware-do%3F)
* [Built-in middleware](#built-in-middleware)
* [Summarization](#summarization)
* [Human-in-the-loop](#human-in-the-loop)
* [Anthropic prompt caching](#anthropic-prompt-caching)
* [Model call limit](#model-call-limit)
* [Tool call limit](#tool-call-limit)
* [Model fallback](#model-fallback)
* [PII detection](#pii-detection)
* [To-do list](#to-do-list)
* [LLM tool selector](#llm-tool-selector)
* [Tool retry](#tool-retry)
* [LLM tool emulator](#llm-tool-emulator)
* [Context editing](#context-editing)
* [Custom middleware](#custom-middleware)
* [Decorator-based middleware](#decorator-based-middleware)
* [Available decorators](#available-decorators)
* [When to use decorators](#when-to-use-decorators)
* [Class-based middleware](#class-based-middleware)
* [Two hook styles](#two-hook-styles)
* [Node-style hooks](#node-style-hooks)
* [Wrap-style hooks](#wrap-style-hooks)
* [Custom state schema](#custom-state-schema)
* [Execution order](#execution-order)
* [Agent jumps](#agent-jumps)
* [Best practices](#best-practices)
* [Examples](#examples)
* [Dynamically selecting tools](#dynamically-selecting-tools)
* [Additional resources](#additional-resources)

[Core components](/oss/python/langchain/agents)

# Middleware

Control and customize agent execution at every step

Middleware provides a way to more tightly control what happens inside the agent. The core agent loop involves calling a model, letting it choose tools to execute, and then finishing when it calls no more tools:Middleware exposes hooks before and after each of those steps:

## What can middleware do?

## Monitor

Track agent behavior with logging, analytics, and debugging

## Modify

Transform prompts, tool selection, and output formatting

## Control

Add retries, fallbacks, and early termination logic

## Enforce

Apply rate limits, guardrails, and PII detection

Add middleware by passing it to [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent):

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[...],  tools =[...], middleware=[SummarizationMiddleware(), HumanInTheLoopMiddleware()],  middleware =[SummarizationMiddleware(), HumanInTheLoopMiddleware()],))
```

## [​](#built-in-middleware) Built-in middleware

LangChain provides prebuilt middleware for common use cases:

### [​](#summarization) Summarization

Automatically summarize conversation history when approaching token limits.

**Perfect for:**

* Long-running conversations that exceed context windows
* Multi-turn dialogues with extensive history
* Applications where preserving full conversation context matters

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import SummarizationMiddleware from langchain.agents.middleware import  SummarizationMiddleware agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[weather_tool, calculator_tool],  tools =[weather_tool, calculator_tool], middleware=[ middleware =[ SummarizationMiddleware( SummarizationMiddleware( model="gpt-4o-mini",  model ="gpt-4o-mini", max_tokens_before_summary=4000, # Trigger summarization at 4000 tokens  max_tokens_before_summary = 4000, # Trigger summarization at 4000 tokens messages_to_keep=20, # Keep last 20 messages after summary  messages_to_keep = 20, # Keep last 20 messages after summary summary_prompt="Custom prompt for summarization...", # Optional  summary_prompt ="Custom prompt for summarization...", # Optional ), ), ], ],))
```

Configuration options

[​](#param-model)

model

string

required

Model for generating summaries

[​](#param-max-tokens-before-summary)

max\_tokens\_before\_summary

number

Token threshold for triggering summarization

[​](#param-messages-to-keep)

messages\_to\_keep

number

default:"20"

Recent messages to preserve

[​](#param-token-counter)

token\_counter

function

Custom token counting function. Defaults to character-based counting.

[​](#param-summary-prompt)

summary\_prompt

string

Custom prompt template. Uses built-in template if not specified.

[​](#param-summary-prefix)

summary\_prefix

string

default:"## Previous conversation summary:"

Prefix for summary messages

### [​](#human-in-the-loop) Human-in-the-loop

Pause agent execution for human approval, editing, or rejection of tool calls before they execute.

**Perfect for:**

* High-stakes operations requiring human approval (database writes, financial transactions)
* Compliance workflows where human oversight is mandatory
* Long running conversations where human feedback is used to guide the agent

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import HumanInTheLoopMiddleware from langchain.agents.middleware import  HumanInTheLoopMiddlewarefrom langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaver agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[read_email_tool, send_email_tool],  tools =[read_email_tool, send_email_tool], checkpointer=InMemorySaver(),  checkpointer =InMemorySaver(), middleware=[ middleware =[ HumanInTheLoopMiddleware( HumanInTheLoopMiddleware( interrupt_on={ interrupt_on ={ # Require approval, editing, or rejection for sending emails # Require approval, editing, or rejection for sending emails "send_email_tool": { "send_email_tool": { "allowed_decisions": ["approve", "edit", "reject"],  "allowed_decisions": ["approve", "edit", "reject"], }, }, # Auto-approve reading emails # Auto-approve reading emails "read_email_tool": False,  "read_email_tool": False, } } ), ), ], ],))
```

Configuration options

[​](#param-interrupt-on)

interrupt\_on

dict

required

Mapping of tool names to approval configs. Values can be `True` (interrupt with default config), `False` (auto-approve), or an `InterruptOnConfig` object.

[​](#param-description-prefix)

description\_prefix

string

default:"Tool execution requires approval"

Prefix for action request descriptions

**`InterruptOnConfig` options:**

[​](#param-allowed-decisions)

allowed\_decisions

list[string]

List of allowed decisions: `"approve"`, `"edit"`, or `"reject"`

[​](#param-description)

description

string | callable

Static string or callable function for custom description

**Important:** Human-in-the-loop middleware requires a [checkpointer](/oss/python/langgraph/persistence#checkpoints) to maintain state across interruptions.See the [human-in-the-loop documentation](/oss/python/langchain/human-in-the-loop) for complete examples and integration patterns.

### [​](#anthropic-prompt-caching) Anthropic prompt caching

Reduce costs by caching repetitive prompt prefixes with Anthropic models.

**Perfect for:**

* Applications with long, repeated system prompts
* Agents that reuse the same context across invocations
* Reducing API costs for high-volume deployments

Learn more about [Anthropic Prompt Caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching#cache-limitations) strategies and limitations.

Copy

Ask AI

```
from langchain_anthropic import ChatAnthropic from  langchain_anthropic import  ChatAnthropicfrom langchain_anthropic.middleware import AnthropicPromptCachingMiddleware from langchain_anthropic.middleware import  AnthropicPromptCachingMiddlewarefrom langchain.agents import create_agent from langchain.agents import  create_agent LONG_PROMPT = """ LONG_PROMPT =  """Please be a helpful assistant.Please be a helpful assistant.  """ """ agent = create_agent(agent = create_agent( model=ChatAnthropic(model="claude-sonnet-4-5-20250929"),  model =ChatAnthropic(model ="claude-sonnet-4-5-20250929"), system_prompt=LONG_PROMPT,  system_prompt = LONG_PROMPT, middleware=[AnthropicPromptCachingMiddleware(ttl="5m")],  middleware =[AnthropicPromptCachingMiddleware(ttl = "5m")],)) # cache store # cache storeagent.invoke({"messages": [HumanMessage("Hi, my name is Bob")]})agent.invoke({"messages": [HumanMessage("Hi, my name is Bob")]}) # cache hit, system prompt is cached# cache hit, system prompt is cachedagent.invoke({"messages": [HumanMessage("What's my name?")]})agent.invoke({"messages": [HumanMessage("What's my name?")]})
```

Configuration options

[​](#param-type)

type

string

default:"ephemeral"

Cache type. Only `"ephemeral"` is currently supported.

[​](#param-ttl)

ttl

string

default:"5m"

Time to live for cached content. Valid values: `"5m"` or `"1h"`

[​](#param-min-messages-to-cache)

min\_messages\_to\_cache

number

default:"0"

Minimum number of messages before caching starts

[​](#param-unsupported-model-behavior)

unsupported\_model\_behavior

string

default:"warn"

Behavior when using non-Anthropic models. Options: `"ignore"`, `"warn"`, or `"raise"`

### [​](#model-call-limit) Model call limit

Limit the number of model calls to prevent infinite loops or excessive costs.

**Perfect for:**

* Preventing runaway agents from making too many API calls
* Enforcing cost controls on production deployments
* Testing agent behavior within specific call budgets

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import ModelCallLimitMiddleware from langchain.agents.middleware import  ModelCallLimitMiddleware agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[...],  tools =[...], middleware=[ middleware =[ ModelCallLimitMiddleware( ModelCallLimitMiddleware( thread_limit=10, # Max 10 calls per thread (across runs)  thread_limit = 10, # Max 10 calls per thread (across runs) run_limit=5, # Max 5 calls per run (single invocation)  run_limit = 5, # Max 5 calls per run (single invocation) exit_behavior="end", # Or "error" to raise exception  exit_behavior = "end", # Or "error" to raise exception ), ), ], ],))
```

Configuration options

[​](#param-thread-limit)

thread\_limit

number

Maximum model calls across all runs in a thread. Defaults to no limit.

[​](#param-run-limit)

run\_limit

number

Maximum model calls per single invocation. Defaults to no limit.

[​](#param-exit-behavior)

exit\_behavior

string

default:"end"

Behavior when limit is reached. Options: `"end"` (graceful termination) or `"error"` (raise exception)

### [​](#tool-call-limit) Tool call limit

Control agent execution by limiting the number of tool calls, either globally across all tools or for specific tools.

**Perfect for:**

* Preventing excessive calls to expensive external APIs
* Limiting web searches or database queries
* Enforcing rate limits on specific tool usage
* Protecting against runaway agent loops

To limit tool calls globally across all tools or for specific tools, set `tool_name`. For each limit, specify one or both of:

* **Thread limit** (`thread_limit`) - Max calls across all runs in a conversation. Persists across invocations. Requires a checkpointer.
* **Run limit** (`run_limit`) - Max calls per single invocation. Resets each turn.

**Exit behaviors:**

| Behavior | Effect | Best For |
| --- | --- | --- |
| **`"continue"`** (default) | Blocks exceeded calls with error messages, agent continues | Most use cases - agent handles limits gracefully |
| **`"error"`** | Raises exception immediately | Complex workflows where you want to handle the limit error manually |
| **`"end"`** | Stops with ToolMessage + AI message | Single-tool scenarios (errors if other tools pending) |

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import ToolCallLimitMiddleware from langchain.agents.middleware import  ToolCallLimitMiddleware # Global limit: max 20 calls per thread, 10 per run# Global limit: max 20 calls per thread, 10 per runglobal_limiter = ToolCallLimitMiddleware(global_limiter = ToolCallLimitMiddleware( thread_limit=20,  thread_limit = 20, run_limit=10,  run_limit = 10,)) # Tool-specific limit with default "continue" behavior# Tool-specific limit with default "continue" behaviorsearch_limiter = ToolCallLimitMiddleware(search_limiter = ToolCallLimitMiddleware( tool_name="search",  tool_name = "search", thread_limit=5,  thread_limit = 5, run_limit=3,  run_limit = 3,)) # Thread limit only (no per-run limit)# Thread limit only (no per-run limit)database_limiter = ToolCallLimitMiddleware(database_limiter = ToolCallLimitMiddleware( tool_name="query_database",  tool_name = "query_database", thread_limit=10,  thread_limit = 10,)) # Strict enforcement with "error" behavior # Strict enforcement with "error" behaviorweb_scraper_limiter = ToolCallLimitMiddleware(web_scraper_limiter = ToolCallLimitMiddleware( tool_name="scrape_webpage",  tool_name = "scrape_webpage", run_limit=2,  run_limit = 2, exit_behavior="error",  exit_behavior = "error",)) # Immediate termination with "end" behavior # Immediate termination with "end" behaviorcritical_tool_limiter = ToolCallLimitMiddleware(critical_tool_limiter = ToolCallLimitMiddleware( tool_name="delete_records",  tool_name = "delete_records", run_limit=1,  run_limit = 1, exit_behavior="end",  exit_behavior = "end",)) # Use multiple limiters together # Use multiple limiters togetheragent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[search_tool, database_tool, scraper_tool],  tools =[search_tool, database_tool, scraper_tool], middleware=[ middleware =[ global_limiter, global_limiter, search_limiter, search_limiter, database_limiter, database_limiter,  web_scraper_limiter  web_scraper_limiter ], ],))
```

Configuration options

[​](#param-tool-name)

tool\_name

string

Name of specific tool to limit. If not provided, limits apply to **all tools globally**.

[​](#param-thread-limit-1)

thread\_limit

number

Maximum tool calls across all runs in a thread (conversation). Persists across multiple invocations with the same thread ID. Requires a checkpointer to maintain state. `None` means no thread limit.

[​](#param-run-limit-1)

run\_limit

number

Maximum tool calls per single invocation (one user message → response cycle). Resets with each new user message. `None` means no run limit.**Note:** At least one of `thread_limit` or `run_limit` must be specified.

[​](#param-exit-behavior-1)

exit\_behavior

string

default:"continue"

Behavior when limit is reached:

* `"continue"` (default) - Block exceeded tool calls with error messages, let other tools and the model continue. The model decides when to end based on the error messages.
* `"error"` - Raise a `ToolCallLimitExceededError` exception, stopping execution immediately
* `"end"` - Stop execution immediately with a ToolMessage and AI message for the exceeded tool call. Only works when limiting a single tool; raises `NotImplementedError` if other tools have pending calls.

### [​](#model-fallback) Model fallback

Automatically fallback to alternative models when the primary model fails.

**Perfect for:**

* Building resilient agents that handle model outages
* Cost optimization by falling back to cheaper models
* Provider redundancy across OpenAI, Anthropic, etc.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import ModelFallbackMiddleware from langchain.agents.middleware import  ModelFallbackMiddleware agent = create_agent(agent = create_agent( model="gpt-4o", # Primary model  model ="gpt-4o", # Primary model tools=[...],  tools =[...], middleware=[ middleware =[ ModelFallbackMiddleware( ModelFallbackMiddleware( "gpt-4o-mini", # Try first on error "gpt-4o-mini", # Try first on error "claude-3-5-sonnet-20241022", # Then this "claude-3-5-sonnet-20241022", # Then this ), ), ], ],))
```

Configuration options

[​](#param-first-model)

first\_model

string | BaseChatModel

required

First fallback model to try when the primary model fails. Can be a model string (e.g., `"openai:gpt-4o-mini"`) or a `BaseChatModel` instance.

[​](#param-additional-models)

\*additional\_models

string | BaseChatModel

Additional fallback models to try in order if previous models fail

### [​](#pii-detection) PII detection

Detect and handle Personally Identifiable Information in conversations.

**Perfect for:**

* Healthcare and financial applications with compliance requirements
* Customer service agents that need to sanitize logs
* Any application handling sensitive user data

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import PIIMiddleware from langchain.agents.middleware import  PIIMiddleware agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[...],  tools =[...], middleware=[ middleware =[ # Redact emails in user input  # Redact emails in user input PIIMiddleware("email", strategy="redact", apply_to_input=True), PIIMiddleware("email", strategy = "redact", apply_to_input = True), # Mask credit cards (show last 4 digits) # Mask credit cards (show last 4 digits) PIIMiddleware("credit_card", strategy="mask", apply_to_input=True), PIIMiddleware("credit_card", strategy = "mask", apply_to_input = True),  # Custom PII type with regex  # Custom PII type with regex PIIMiddleware( PIIMiddleware( "api_key",  "api_key", detector=r"sk-[a-zA-Z0-9]{32}",  detector = r"sk-[a-zA-Z0-9]{32} ", strategy="block", # Raise error if detected  strategy = "block", # Raise error if detected ), ), ], ],))
```

Configuration options

[​](#param-pii-type)

pii\_type

string

required

Type of PII to detect. Can be a built-in type (`email`, `credit_card`, `ip`, `mac_address`, `url`) or a custom type name.

[​](#param-strategy)

strategy

string

default:"redact"

How to handle detected PII. Options:

* `"block"` - Raise exception when detected
* `"redact"` - Replace with `[REDACTED_TYPE]`
* `"mask"` - Partially mask (e.g., `****-****-****-1234`)
* `"hash"` - Replace with deterministic hash

[​](#param-detector)

detector

function | regex

Custom detector function or regex pattern. If not provided, uses built-in detector for the PII type.

[​](#param-apply-to-input)

apply\_to\_input

boolean

default:"True"

Check user messages before model call

[​](#param-apply-to-output)

apply\_to\_output

boolean

default:"False"

Check AI messages after model call

[​](#param-apply-to-tool-results)

apply\_to\_tool\_results

boolean

default:"False"

Check tool result messages after execution

### [​](#to-do-list) To-do list

Equip agents with task planning and tracking capabilities for complex multi-step tasks.

**Perfect for:**

* Complex multi-step tasks requiring coordination across multiple tools
* Long-running operations where progress visibility is important

Just as humans are more effective when they write down and track tasks, agents benefit from structured task management to break down complex problems, adapt plans as new information emerges, and provide transparency into their workflow. You may have noticed patterns like this in Claude Code, which writes out a to-do list before tackling complex, multi-part tasks.

This middleware automatically provides agents with a `write_todos` tool and system prompts to guide effective task planning.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import TodoListMiddleware from langchain.agents.middleware import  TodoListMiddlewarefrom langchain_core.messages import HumanMessage from langchain_core.messages import  HumanMessagefrom langchain_core.tools import tool from langchain_core.tools import  tool  @tool @tooldef read_file(file_path: str) -> str: def  read_file(file_path: str) -> str: """Read contents of a file.""" """Read contents of a file.""" with open(file_path) as f:  with  open(file_path) as f: return f.read()  return f.read()  @tool @tooldef write_file(file_path: str, content: str) -> str: def  write_file(file_path: str, content: str) -> str: """Write content to a file.""" """Write content to a file.""" with open(file_path, 'w') as f:  with  open(file_path, 'w') as f: f.write(content) f.write(content) return f"Wrote {len(content)} characters to {file_path}"  return  f "Wrote {len(content)}  characters to {file_path} "  @tool @tooldef run_tests(test_path: str) -> str: def  run_tests(test_path: str) -> str: """Run tests and return results.""" """Run tests and return results."""  # Simplified for example  # Simplified for example return "All tests passed!"  return "All tests passed!" agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[read_file, write_file, run_tests],  tools =[read_file, write_file, run_tests], middleware=[TodoListMiddleware()],  middleware =[TodoListMiddleware()],)) result = agent.invoke({result = agent.invoke({ "messages": [HumanMessage("Refactor the authentication module to use async/await and ensure all tests pass")]  "messages": [HumanMessage("Refactor the authentication module to use async/await and ensure all tests pass")]})}) # The agent will use write_todos to plan and track:# The agent will use write_todos to plan and track:# 1. Read current authentication module code# 1. Read current authentication module code# 2. Identify functions that need async conversion# 2. Identify functions that need async conversion# 3. Refactor functions to async/await# 3. Refactor functions to async/await# 4. Update function calls throughout codebase# 4. Update function calls throughout codebase# 5. Run tests and fix any failures# 5. Run tests and fix any failures print(result["todos"]) # Track the agent's progress through each step print(result["todos"]) # Track the agent's progress through each step
```

Configuration options

[​](#param-system-prompt)

system\_prompt

string

Custom system prompt for guiding todo usage. Uses built-in prompt if not specified.

[​](#param-tool-description)

tool\_description

string

Custom description for the `write_todos` tool. Uses built-in description if not specified.

### [​](#llm-tool-selector) LLM tool selector

Use an LLM to intelligently select relevant tools before calling the main model.

**Perfect for:**

* Agents with many tools (10+) where most aren’t relevant per query
* Reducing token usage by filtering irrelevant tools
* Improving model focus and accuracy

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import LLMToolSelectorMiddleware from langchain.agents.middleware import  LLMToolSelectorMiddleware agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[tool1, tool2, tool3, tool4, tool5, ...], # Many tools  tools =[tool1, tool2, tool3, tool4, tool5, ...], # Many tools middleware=[ middleware =[ LLMToolSelectorMiddleware( LLMToolSelectorMiddleware( model="gpt-4o-mini", # Use cheaper model for selection  model ="gpt-4o-mini", # Use cheaper model for selection max_tools=3, # Limit to 3 most relevant tools  max_tools = 3, # Limit to 3 most relevant tools always_include=["search"], # Always include certain tools  always_include =["search"], # Always include certain tools ), ), ], ],))
```

Configuration options

[​](#param-model-1)

model

string | BaseChatModel

Model for tool selection. Can be a model string or `BaseChatModel` instance. Defaults to the agent’s main model.

[​](#param-system-prompt-1)

system\_prompt

string

Instructions for the selection model. Uses built-in prompt if not specified.

[​](#param-max-tools)

max\_tools

number

Maximum number of tools to select. Defaults to no limit.

[​](#param-always-include)

always\_include

list[string]

List of tool names to always include in the selection

### [​](#tool-retry) Tool retry

Automatically retry failed tool calls with configurable exponential backoff.

**Perfect for:**

* Handling transient failures in external API calls
* Improving reliability of network-dependent tools
* Building resilient agents that gracefully handle temporary errors

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import ToolRetryMiddleware from langchain.agents.middleware import  ToolRetryMiddleware agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[search_tool, database_tool],  tools =[search_tool, database_tool], middleware=[ middleware =[ ToolRetryMiddleware( ToolRetryMiddleware( max_retries=3, # Retry up to 3 times  max_retries = 3, # Retry up to 3 times backoff_factor=2.0, # Exponential backoff multiplier  backoff_factor =2.0, # Exponential backoff multiplier initial_delay=1.0, # Start with 1 second delay  initial_delay =1.0, # Start with 1 second delay max_delay=60.0, # Cap delays at 60 seconds  max_delay =60.0, # Cap delays at 60 seconds jitter=True, # Add random jitter to avoid thundering herd  jitter = True, # Add random jitter to avoid thundering herd ), ), ], ],))
```

Configuration options

[​](#param-max-retries)

max\_retries

number

default:"2"

Maximum number of retry attempts after the initial call (3 total attempts with default)

[​](#param-tools)

tools

list[BaseTool | str]

Optional list of tools or tool names to apply retry logic to. If `None`, applies to all tools.

[​](#param-retry-on)

retry\_on

tuple[type[Exception], ...] | callable

default:"(Exception,)"

Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried.

[​](#param-on-failure)

on\_failure

string | callable

default:"return\_message"

Behavior when all retries are exhausted. Options:

* `"return_message"` - Return a ToolMessage with error details (allows LLM to handle failure)
* `"raise"` - Re-raise the exception (stops agent execution)
* Custom callable - Function that takes the exception and returns a string for the ToolMessage content

[​](#param-backoff-factor)

backoff\_factor

number

default:"2.0"

Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to 0.0 for constant delay.

[​](#param-initial-delay)

initial\_delay

number

default:"1.0"

Initial delay in seconds before first retry

[​](#param-max-delay)

max\_delay

number

default:"60.0"

Maximum delay in seconds between retries (caps exponential backoff growth)

[​](#param-jitter)

jitter

boolean

default:"true"

Whether to add random jitter (±25%) to delay to avoid thundering herd

### [​](#llm-tool-emulator) LLM tool emulator

Emulate tool execution using an LLM for testing purposes, replacing actual tool calls with AI-generated responses.

**Perfect for:**

* Testing agent behavior without executing real tools
* Developing agents when external tools are unavailable or expensive
* Prototyping agent workflows before implementing actual tools

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import LLMToolEmulator from langchain.agents.middleware import  LLMToolEmulator agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[get_weather, search_database, send_email],  tools =[get_weather, search_database, send_email], middleware=[ middleware =[ # Emulate all tools by default  # Emulate all tools by default LLMToolEmulator(), LLMToolEmulator(),  # Or emulate specific tools  # Or emulate specific tools # LLMToolEmulator(tools=["get_weather", "search_database"]), # LLMToolEmulator(tools=["get_weather", "search_database"]),  # Or use a custom model for emulation  # Or use a custom model for emulation # LLMToolEmulator(model="claude-sonnet-4-5-20250929"), # LLMToolEmulator(model="claude-sonnet-4-5-20250929"), ], ],))
```

Configuration options

[​](#param-tools-1)

tools

list[str | BaseTool]

List of tool names (str) or BaseTool instances to emulate. If `None` (default), ALL tools will be emulated. If empty list, no tools will be emulated.

[​](#param-model-2)

model

string | BaseChatModel

default:"anthropic:claude-3-5-sonnet-latest"

Model to use for generating emulated tool responses. Can be a model identifier string or BaseChatModel instance.

### [​](#context-editing) Context editing

Manage conversation context by trimming, summarizing, or clearing tool uses.

**Perfect for:**

* Long conversations that need periodic context cleanup
* Removing failed tool attempts from context
* Custom context management strategies

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit from langchain.agents.middleware import ContextEditingMiddleware, ClearToolUsesEdit agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[...],  tools =[...], middleware=[ middleware =[ ContextEditingMiddleware( ContextEditingMiddleware( edits=[ edits =[ ClearToolUsesEdit(trigger=1000), # Clear old tool uses ClearToolUsesEdit(trigger = 1000), # Clear old tool uses ], ], ), ), ], ],))
```

Configuration options

[​](#param-edits)

edits

list[ContextEdit]

default:"[ClearToolUsesEdit()]"

List of `ContextEdit` strategies to apply

[​](#param-token-count-method)

token\_count\_method

string

default:"approximate"

Token counting method. Options: `"approximate"` or `"model"`

**[`ClearToolUsesEdit`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.ClearToolUsesEdit) options:**

[​](#param-trigger)

trigger

number

default:"100000"

Token count that triggers the edit

[​](#param-clear-at-least)

clear\_at\_least

number

default:"0"

Minimum tokens to reclaim

[​](#param-keep)

keep

number

default:"3"

Number of recent tool results to preserve

[​](#param-clear-tool-inputs)

clear\_tool\_inputs

boolean

default:"False"

Whether to clear tool call parameters

[​](#param-exclude-tools)

exclude\_tools

list[string]

default:"()"

List of tool names to exclude from clearing

[​](#param-placeholder)

string

default:"[cleared]"

Placeholder text for cleared outputs

## [​](#custom-middleware) Custom middleware

Build custom middleware by implementing hooks that run at specific points in the agent execution flow. You can create middleware in two ways:

1. **Decorator-based** - Quick and simple for single-hook middleware
2. **Class-based** - More powerful for complex middleware with multiple hooks

## [​](#decorator-based-middleware) Decorator-based middleware

For simple middleware that only needs a single hook, decorators provide the quickest way to add functionality:

Copy

Ask AI

```
from langchain.agents.middleware import before_model, after_model, wrap_model_call from langchain.agents.middleware import before_model, after_model, wrap_model_callfrom langchain.agents.middleware import AgentState, ModelRequest, ModelResponse, dynamic_prompt from langchain.agents.middleware import AgentState, ModelRequest, ModelResponse, dynamic_promptfrom langchain.messages import AIMessage from langchain.messages import  AIMessagefrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langgraph.runtime import Runtime from langgraph.runtime import  Runtimefrom typing import Any, Callable from  typing import Any, Callable # Node-style: logging before model calls# Node-style: logging before model calls @before_model @before_modeldef log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None: def  log_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] |  None: print(f"About to call model with {len(state['messages'])} messages")  print(f "About to call model with {len(state['messages'])}  messages")  return None  return  None # Node-style: validation after model calls# Node-style: validation after model calls@after_model(can_jump_to=["end"]) @after_model(can_jump_to =["end"])def validate_output(state: AgentState, runtime: Runtime) -> dict[str, Any] | None: def  validate_output(state: AgentState, runtime: Runtime) -> dict[str, Any] |  None: last_message = state["messages"][-1]  last_message = state["messages"][- 1] if "BLOCKED" in last_message.content:  if  "BLOCKED"  in last_message.content: return { return { "messages": [AIMessage("I cannot respond to that request.")],  "messages": [AIMessage("I cannot respond to that request.")], "jump_to": "end"  "jump_to": "end" } }  return None  return  None # Wrap-style: retry logic# Wrap-style: retry logic @wrap_model_call @wrap_model_calldef retry_model(def  retry_model( request: ModelRequest,  request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse],  handler: Callable[[ModelRequest], ModelResponse],) -> ModelResponse:) -> ModelResponse: for attempt in range(3):  for  attempt in  range(3): try:  try: return handler(request)  return handler(request) except Exception as e:  except  Exception  as e: if attempt == 2:  if  attempt ==  2:  raise  raise print(f"Retry {attempt + 1}/3 after error: {e}")  print(f "Retry {attempt +  1}/3 after error: {e} ") # Wrap-style: dynamic prompts# Wrap-style: dynamic prompts @dynamic_prompt @dynamic_promptdef personalized_prompt(request: ModelRequest) -> str: def  personalized_prompt(request: ModelRequest) -> str: user_id = request.runtime.context.get("user_id", "guest")  user_id = request.runtime.context.get("user_id", "guest") return f"You are a helpful assistant for user {user_id}. Be concise and friendly."  return  f "You are a helpful assistant for user {user_id}. Be concise and friendly." # Use decorators in agent # Use decorators in agentagent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", middleware=[log_before_model, validate_output, retry_model, personalized_prompt],  middleware =[log_before_model, validate_output, retry_model, personalized_prompt], tools=[...],  tools =[...],))
```

### [​](#available-decorators) Available decorators

**Node-style** (run at specific execution points):

* `@before_agent` - Before agent starts (once per invocation)
* [`@before_model`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.before_model) - Before each model call
* [`@after_model`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.after_model) - After each model response
* `@after_agent` - After agent completes (once per invocation)

**Wrap-style** (intercept and control execution):

* [`@wrap_model_call`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.wrap_model_call) - Around each model call
* [`@wrap_tool_call`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.wrap_tool_call) - Around each tool call

**Convenience decorators**:

* [`@dynamic_prompt`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.dynamic_prompt) - Generates dynamic system prompts (equivalent to [`@wrap_model_call`](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.wrap_model_call) that modifies the prompt)

### [​](#when-to-use-decorators) When to use decorators

## Use decorators when

• You need a single hook  
 • No complex configuration

## Use classes when

• Multiple hooks needed  
 • Complex configuration  
 • Reuse across projects (config on init)

## [​](#class-based-middleware) Class-based middleware

### [​](#two-hook-styles) Two hook styles

## Node-style hooks

Run sequentially at specific execution points. Use for logging, validation, and state updates.

## Wrap-style hooks

Intercept execution with full control over handler calls. Use for retries, caching, and transformation.

#### [​](#node-style-hooks) Node-style hooks

Run at specific points in the execution flow:

* `before_agent` - Before agent starts (once per invocation)
* `before_model` - Before each model call
* `after_model` - After each model response
* `after_agent` - After agent completes (up to once per invocation)

**Example: Logging middleware**

Copy

Ask AI

```
from langchain.agents.middleware import AgentMiddleware, AgentState from langchain.agents.middleware import AgentMiddleware, AgentStatefrom langgraph.runtime import Runtime from langgraph.runtime import  Runtime from typing import Any from  typing import  Any class LoggingMiddleware(AgentMiddleware): class  LoggingMiddleware(AgentMiddleware): def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:  def  before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] |  None: print(f"About to call model with {len(state['messages'])} messages")  print(f "About to call model with {len(state['messages'])}  messages")  return None  return  None  def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:  def  after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] |  None: print(f"Model returned: {state['messages'][-1].content}")  print(f"Model returned: {state['messages'][- 1].content} ")  return None  return  None
```

**Example: Conversation length limit**

Copy

Ask AI

```
from langchain.agents.middleware import AgentMiddleware, AgentState from langchain.agents.middleware import AgentMiddleware, AgentStatefrom langchain.messages import AIMessage from langchain.messages import  AIMessagefrom langgraph.runtime import Runtime from langgraph.runtime import  Runtime from typing import Any from  typing import  Any class MessageLimitMiddleware(AgentMiddleware): class  MessageLimitMiddleware(AgentMiddleware): def __init__(self, max_messages: int = 50):  def  __init__(self, max_messages: int =  50): super().__init__()  super(). __init__() self.max_messages = max_messages  self.max_messages =  max_messages  def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:  def  before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] |  None: if len(state["messages"]) == self.max_messages:  if  len(state["messages"]) ==  self.max_messages: return { return { "messages": [AIMessage("Conversation limit reached.")],  "messages": [AIMessage("Conversation limit reached.")], "jump_to": "end"  "jump_to": "end" } }  return None  return  None
```

#### [​](#wrap-style-hooks) Wrap-style hooks

Intercept execution and control when the handler is called:

* `wrap_model_call` - Around each model call
* `wrap_tool_call` - Around each tool call

You decide if the handler is called zero times (short-circuit), once (normal flow), or multiple times (retry logic). **Example: Model retry middleware**

Copy

Ask AI

```
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse from typing import Callable from  typing import  Callable class RetryMiddleware(AgentMiddleware): class  RetryMiddleware(AgentMiddleware): def __init__(self, max_retries: int = 3):  def  __init__(self, max_retries: int =  3): super().__init__()  super(). __init__() self.max_retries = max_retries  self.max_retries =  max_retries  def wrap_model_call( def  wrap_model_call( self,  self, request: ModelRequest,  request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse],  handler: Callable[[ModelRequest], ModelResponse], ) -> ModelResponse: ) -> ModelResponse: for attempt in range(self.max_retries):  for  attempt in  range(self.max_retries): try:  try: return handler(request)  return handler(request) except Exception as e:  except  Exception  as e: if attempt == self.max_retries - 1:  if  attempt ==  self.max_retries -  1:  raise  raise print(f"Retry {attempt + 1}/{self.max_retries} after error: {e}")  print(f "Retry {attempt +  1}/{self.max_retries} after error: {e} ")
```

**Example: Dynamic model selection**

Copy

Ask AI

```
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponsefrom langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_model from typing import Callable from  typing import  Callable class DynamicModelMiddleware(AgentMiddleware): class  DynamicModelMiddleware(AgentMiddleware): def wrap_model_call( def  wrap_model_call( self,  self, request: ModelRequest,  request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse],  handler: Callable[[ModelRequest], ModelResponse], ) -> ModelResponse: ) -> ModelResponse:  # Use different model based on conversation length  # Use different model based on conversation length if len(request.messages) > 10:  if  len(request.messages) >  10: request.model = init_chat_model("gpt-4o") request.model = init_chat_model("gpt-4o") else:  else: request.model = init_chat_model("gpt-4o-mini") request.model = init_chat_model("gpt-4o-mini")  return handler(request)  return handler(request)
```

**Example: Tool call monitoring**

Copy

Ask AI

```
from langchain.tools.tool_node import ToolCallRequest from langchain.tools.tool_node import  ToolCallRequestfrom langchain.agents.middleware import AgentMiddleware from langchain.agents.middleware import  AgentMiddlewarefrom langchain_core.messages import ToolMessage from langchain_core.messages import  ToolMessagefrom langgraph.types import Command from langgraph.types import  Command from typing import Callable from  typing import  Callable class ToolMonitoringMiddleware(AgentMiddleware): class  ToolMonitoringMiddleware(AgentMiddleware): def wrap_tool_call( def  wrap_tool_call( self,  self, request: ToolCallRequest,  request: ToolCallRequest, handler: Callable[[ToolCallRequest], ToolMessage | Command],  handler: Callable[[ToolCallRequest], ToolMessage | Command], ) -> ToolMessage | Command: ) -> ToolMessage | Command: print(f"Executing tool: {request.tool_call['name']}")  print(f"Executing tool: {request.tool_call['name']} ") print(f"Arguments: {request.tool_call['args']}")  print(f"Arguments: {request.tool_call['args']} ")  try:  try: result = handler(request)  result = handler(request) print(f"Tool completed successfully")  print(f "Tool completed successfully")  return result  return  result except Exception as e:  except  Exception  as e: print(f"Tool failed: {e}")  print(f"Tool failed: {e} ")  raise  raise
```

### [​](#custom-state-schema) Custom state schema

Middleware can extend the agent’s state with custom properties. Define a custom state type and set it as the `state_schema`:

Copy

Ask AI

```
from langchain.agents.middleware import AgentState, AgentMiddleware from langchain.agents.middleware import AgentState, AgentMiddleware from typing_extensions import NotRequired from  typing_extensions import  NotRequired from typing import Any from  typing import  Any class CustomState(AgentState): class  CustomState(AgentState): model_call_count: NotRequired[int] model_call_count: NotRequired[int] user_id: NotRequired[str] user_id: NotRequired[str] class CallCounterMiddleware(AgentMiddleware[CustomState]): class  CallCounterMiddleware(AgentMiddleware[CustomState]): state_schema = CustomState  state_schema =  CustomState  def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:  def  before_model(self, state: CustomState, runtime) -> dict[str, Any] |  None:  # Access custom state properties  # Access custom state properties count = state.get("model_call_count", 0)  count = state.get("model_call_count", 0)  if count > 10:  if  count >  10: return {"jump_to": "end"}  return {"jump_to": "end"}  return None  return  None  def after_model(self, state: CustomState, runtime) -> dict[str, Any] | None:  def  after_model(self, state: CustomState, runtime) -> dict[str, Any] |  None:  # Update custom state  # Update custom state return {"model_call_count": state.get("model_call_count", 0) + 1}  return {"model_call_count": state.get("model_call_count", 0) +  1}
```

Copy

Ask AI

```
agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", middleware=[CallCounterMiddleware()],  middleware =[CallCounterMiddleware()], tools=[...],  tools =[...],)) # Invoke with custom state # Invoke with custom stateresult = agent.invoke({result = agent.invoke({ "messages": [HumanMessage("Hello")],  "messages": [HumanMessage("Hello")], "model_call_count": 0,  "model_call_count": 0, "user_id": "user-123",  "user_id": "user-123",})})
```

### [​](#execution-order) Execution order

When using multiple middleware, understanding execution order is important:

Copy

Ask AI

```
agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", middleware=[middleware1, middleware2, middleware3],  middleware =[middleware1, middleware2, middleware3], tools=[...],  tools =[...],))
```

Execution flow (click to expand)

**Before hooks run in order:**

1. `middleware1.before_agent()`
2. `middleware2.before_agent()`
3. `middleware3.before_agent()`

**Agent loop starts**

1. `middleware1.before_model()`
2. `middleware2.before_model()`
3. `middleware3.before_model()`

**Wrap hooks nest like function calls:**

1. `middleware1.wrap_model_call()` → `middleware2.wrap_model_call()` → `middleware3.wrap_model_call()` → model

**After hooks run in reverse order:**

1. `middleware3.after_model()`
2. `middleware2.after_model()`
3. `middleware1.after_model()`

**Agent loop ends**

1. `middleware3.after_agent()`
2. `middleware2.after_agent()`
3. `middleware1.after_agent()`

 **Key rules:**

* `before_*` hooks: First to last
* `after_*` hooks: Last to first (reverse)
* `wrap_*` hooks: Nested (first middleware wraps all others)

### [​](#agent-jumps) Agent jumps

To exit early from middleware, return a dictionary with `jump_to`:

Copy

Ask AI

```
class EarlyExitMiddleware(AgentMiddleware): class  EarlyExitMiddleware(AgentMiddleware): def before_model(self, state: AgentState, runtime) -> dict[str, Any] | None:  def  before_model(self, state: AgentState, runtime) -> dict[str, Any] |  None:  # Check some condition  # Check some condition if should_exit(state):  if should_exit(state): return { return { "messages": [AIMessage("Exiting early due to condition.")],  "messages": [AIMessage("Exiting early due to condition.")], "jump_to": "end"  "jump_to": "end" } }  return None  return  None
```

Available jump targets:

* `"end"`: Jump to the end of the agent execution
* `"tools"`: Jump to the tools node
* `"model"`: Jump to the model node (or the first `before_model` hook)

**Important:** When jumping from `before_model` or `after_model`, jumping to `"model"` will cause all `before_model` middleware to run again. To enable jumping, decorate your hook with `@hook_config(can_jump_to=[...])`:

Copy

Ask AI

```
from langchain.agents.middleware import AgentMiddleware, hook_config from langchain.agents.middleware import AgentMiddleware, hook_config from typing import Any from  typing import  Any class ConditionalMiddleware(AgentMiddleware): class  ConditionalMiddleware(AgentMiddleware): @hook_config(can_jump_to=["end", "tools"])  @hook_config(can_jump_to =["end", "tools"]) def after_model(self, state: AgentState, runtime) -> dict[str, Any] | None:  def  after_model(self, state: AgentState, runtime) -> dict[str, Any] |  None: if some_condition(state):  if some_condition(state): return {"jump_to": "end"}  return {"jump_to": "end"}  return None  return  None
```

### [​](#best-practices) Best practices

1. Keep middleware focused - each should do one thing well
2. Handle errors gracefully - don’t let middleware errors crash the agent
3. **Use appropriate hook types**:
   * Node-style for sequential logic (logging, validation)
   * Wrap-style for control flow (retry, fallback, caching)
4. Clearly document any custom state properties
5. Unit test middleware independently before integrating
6. Consider execution order - place critical middleware first in the list
7. Use built-in middleware when possible, don’t reinvent the wheel :)

## [​](#examples) Examples

### [​](#dynamically-selecting-tools) Dynamically selecting tools

Select relevant tools at runtime to improve performance and accuracy.

**Benefits:**

* **Shorter prompts** - Reduce complexity by exposing only relevant tools
* **Better accuracy** - Models choose correctly from fewer options
* **Permission control** - Dynamically filter tools based on user access

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import AgentMiddleware, ModelRequest from langchain.agents.middleware import AgentMiddleware, ModelRequest from typing import Callable from  typing import  Callable class ToolSelectorMiddleware(AgentMiddleware): class  ToolSelectorMiddleware(AgentMiddleware): def wrap_model_call( def  wrap_model_call( self,  self, request: ModelRequest,  request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse],  handler: Callable[[ModelRequest], ModelResponse], ) -> ModelResponse: ) -> ModelResponse: """Middleware to select relevant tools based on state/context.""" """Middleware to select relevant tools based on state/context.""" # Select a small, relevant subset of tools based on state/context # Select a small, relevant subset of tools based on state/context relevant_tools = select_relevant_tools(request.state, request.runtime)  relevant_tools = select_relevant_tools(request.state, request.runtime) request.tools = relevant_tools request.tools =  relevant_tools return handler(request)  return handler(request) agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=all_tools, # All available tools need to be registered upfront  tools =all_tools, # All available tools need to be registered upfront # Middleware can be used to select a smaller subset that's relevant for the given run. # Middleware can be used to select a smaller subset that's relevant for the given run. middleware=[ToolSelectorMiddleware()],  middleware =[ToolSelectorMiddleware()],))
```

ShowExtended example: GitHub vs GitLab tool selection

Copy

Ask AI

```
from dataclasses import dataclass from  dataclasses import  dataclassfrom typing import Literal, Callable from  typing import Literal, Callable from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponsefrom langchain_core.tools import tool from langchain_core.tools import  tool  @tool @tooldef github_create_issue(repo: str, title: str) -> dict: def  github_create_issue(repo: str, title: str) -> dict: """Create an issue in a GitHub repository.""" """Create an issue in a GitHub repository.""" return {"url": f"https://github.com/{repo}/issues/1", "title": title}  return {"url": f"https://github.com/{repo}/issues/1", "title": title} @tool @tooldef gitlab_create_issue(project: str, title: str) -> dict: def  gitlab_create_issue(project: str, title: str) -> dict: """Create an issue in a GitLab project.""" """Create an issue in a GitLab project.""" return {"url": f"https://gitlab.com/{project}/-/issues/1", "title": title}  return {"url": f"https://gitlab.com/{project}/-/issues/1", "title": title} all_tools = [github_create_issue, gitlab_create_issue] all_tools = [github_create_issue, gitlab_create_issue] @dataclass @dataclassclass Context: class  Context: provider: Literal["github", "gitlab"] provider: Literal["github", "gitlab"] class ToolSelectorMiddleware(AgentMiddleware): class  ToolSelectorMiddleware(AgentMiddleware): def wrap_model_call( def  wrap_model_call( self,  self, request: ModelRequest,  request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse],  handler: Callable[[ModelRequest], ModelResponse], ) -> ModelResponse: ) -> ModelResponse: """Select tools based on the VCS provider.""" """Select tools based on the VCS provider.""" provider = request.runtime.context.provider  provider = request.runtime.context.provider  if provider == "gitlab":  if  provider ==  "gitlab": selected_tools = [t for t in request.tools if t.name == "gitlab_create_issue"]  selected_tools = [t for  t in request.tools if t.name ==  "gitlab_create_issue"] else:  else: selected_tools = [t for t in request.tools if t.name == "github_create_issue"]  selected_tools = [t for  t in request.tools if t.name ==  "github_create_issue"]  request.tools = selected_tools request.tools =  selected_tools return handler(request)  return handler(request) agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=all_tools,  tools =all_tools, middleware=[ToolSelectorMiddleware()],  middleware =[ToolSelectorMiddleware()], context_schema=Context,  context_schema =Context,)) # Invoke with GitHub context # Invoke with GitHub contextagent.invoke(agent.invoke( { { "messages": [{"role": "user", "content": "Open an issue titled 'Bug: where are the cats' in the repository `its-a-cats-game`"}]  "messages": [{"role": "user", "content": "Open an issue titled 'Bug: where are the cats' in the repository `its-a-cats-game`"}] }, }, context=Context(provider="github"),  context =Context(provider = "github"),))
```

**Key points:**

* Register all tools upfront
* Middleware selects the relevant subset per request
* Use `context_schema` for configuration requirements

## [​](#additional-resources) Additional resources

* [Middleware API reference](https://reference.langchain.com/python/langchain/middleware/) - Complete guide to custom middleware
* [Human-in-the-loop](/oss/python/langchain/human-in-the-loop) - Add human review for sensitive operations
* [Testing agents](/oss/python/langchain/test) - Strategies for testing safety mechanisms

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/middleware.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Streaming](/oss/python/langchain/streaming)[Structured output](/oss/python/langchain/structured-output)