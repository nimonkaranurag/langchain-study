Test - Docs by LangChain

===============

[Skip to main content](https://docs.langchain.com/oss/python/langchain/test#content-area)

We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page![Image 1: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 2: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)LangChain + LangGraph

Search...

⌘K

*   [GitHub](https://github.com/langchain-ai)
*   [Try LangSmith](https://smith.langchain.com/)
*   [Try LangSmith](https://smith.langchain.com/)

Search...

Navigation

Use in production

Test

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
*   [Unit Testing](https://docs.langchain.com/oss/python/langchain/test#unit-testing)
*   [Mocking Chat Model](https://docs.langchain.com/oss/python/langchain/test#mocking-chat-model)
*   [InMemorySaver Checkpointer](https://docs.langchain.com/oss/python/langchain/test#inmemorysaver-checkpointer)
*   [Integration Testing](https://docs.langchain.com/oss/python/langchain/test#integration-testing)
*   [Installing AgentEvals](https://docs.langchain.com/oss/python/langchain/test#installing-agentevals)
*   [Trajectory Match Evaluator](https://docs.langchain.com/oss/python/langchain/test#trajectory-match-evaluator)
*   [LLM-as-Judge Evaluator](https://docs.langchain.com/oss/python/langchain/test#llm-as-judge-evaluator)
*   [Async Support](https://docs.langchain.com/oss/python/langchain/test#async-support)
*   [LangSmith Integration](https://docs.langchain.com/oss/python/langchain/test#langsmith-integration)
*   [Recording & Replaying HTTP Calls](https://docs.langchain.com/oss/python/langchain/test#recording-%26-replaying-http-calls)

[Use in production](https://docs.langchain.com/oss/python/langchain/studio)

Test
====

Copy page

Copy page

Agentic applications let an LLM decide its own next steps to solve a problem. That flexibility is powerful, but the model’s black-box nature makes it hard to predict how a tweak in one part of your agent will affect the rest. To build production-ready agents, thorough testing is essential.There are a few approaches to testing your agents:
*   [Unit tests](https://docs.langchain.com/oss/python/langchain/test#unit-testing) exercise small, deterministic pieces of your agent in isolation using in-memory fakes so you can assert exact behavior quickly and deterministically.
*   [Integration tests](https://docs.langchain.com/oss/python/langchain/test#integration-testing) test the agent using real network calls to confirm that components work together, credentials and schemas line up, and latency is acceptable.

Agentic applications tend to lean more on integration because they chain multiple components together and must deal with flakiness due to the nondeterministic nature of LLMs.
[​](https://docs.langchain.com/oss/python/langchain/test#unit-testing)

Unit Testing
------------------------------------------------------------------------------------

### [​](https://docs.langchain.com/oss/python/langchain/test#mocking-chat-model)

Mocking Chat Model

For logic not requiring API calls, you can use an in-memory stub for mocking responses.LangChain provides [`GenericFakeChatModel`](https://python.langchain.com/api_reference/core/language_models/langchain_core.language_models.fake_chat_models.GenericFakeChatModel.html) for mocking text responses. It accepts an iterator of responses (AIMessages or strings) and returns one per invocation. It supports both regular and streaming usage.

Copy

Ask AI

```
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

model = GenericFakeChatModel(messages=iter([
    AIMessage(content="", tool_calls=[ToolCall(name="foo", args={"bar": "baz"}, id="call_1")]),
    "bar"
]))

model.invoke("hello")
# AIMessage(content='', ..., tool_calls=[{'name': 'foo', 'args': {'bar': 'baz'}, 'id': 'call_1', 'type': 'tool_call'}])
```

If we invoke the model again, it will return the next item in the iterator:

Copy

Ask AI

```
model.invoke("hello, again!")
# AIMessage(content='bar', ...)
```

### [​](https://docs.langchain.com/oss/python/langchain/test#inmemorysaver-checkpointer)

InMemorySaver Checkpointer

To enable persistence during testing, you can use the [`InMemorySaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.memory.InMemorySaver) checkpointer. This allows you to simulate multiple turns to test state-dependent behavior:

Copy

Ask AI

```
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    tools=[],
    checkpointer=InMemorySaver()
)

# First invocation
agent.invoke(HumanMessage(content="I live in Sydney, Australia."))

# Second invocation: the first message is persisted (Sydney location), so the model returns GMT+10 time
agent.invoke(HumanMessage(content="What's my local time?"))
```

[​](https://docs.langchain.com/oss/python/langchain/test#integration-testing)

Integration Testing
--------------------------------------------------------------------------------------------------

Many agent behaviors only emerge when using a real LLM, such as which tool the agent decides to call, how it formats responses, or whether a prompt modification affects the entire execution trajectory. LangChain’s [`agentevals`](https://github.com/langchain-ai/agentevals) package provides evaluators specifically designed for testing agent trajectories with live models.AgentEvals lets you easily evaluate the trajectory of your agent (the exact sequence of messages, including tool calls) by performing a **trajectory match** or by using an **LLM judge**:[Trajectory match ---------------- Hard-code a reference trajectory for a given input and validate the run via a step-by-step comparison.Ideal for testing well-defined workflows where you know the expected behavior. Use when you have specific expectations about which tools should be called and in what order. This approach is deterministic, fast, and cost-effective since it doesn’t require additional LLM calls.](https://docs.langchain.com/oss/python/langchain/test#trajectory-match-evaluator)[LLM-as-judge ------------ Use a LLM to qualitatively validate your agent’s execution trajectory. The “judge” LLM reviews the agent’s decisions against a prompt rubric (which can include a reference trajectory).More flexible and can assess nuanced aspects like efficiency and appropriateness, but requires an LLM call and is less deterministic. Use when you want to evaluate the overall quality and reasonableness of the agent’s trajectory without strict tool call or ordering requirements.](https://docs.langchain.com/oss/python/langchain/test#llm-as-judge-evaluator)
### [​](https://docs.langchain.com/oss/python/langchain/test#installing-agentevals)

Installing AgentEvals

Copy

Ask AI

```
pip install agentevals
```

Or, clone the [AgentEvals repository](https://github.com/langchain-ai/agentevals) directly.
### [​](https://docs.langchain.com/oss/python/langchain/test#trajectory-match-evaluator)

Trajectory Match Evaluator

AgentEvals offers the `create_trajectory_match_evaluator` function to match your agent’s trajectory against a reference trajectory. There are four modes to choose from:

| Mode | Description | Use Case |
| --- | --- | --- |
| `strict` | Exact match of messages and tool calls in the same order | Testing specific sequences (e.g., policy lookup before authorization) |
| `unordered` | Same tool calls allowed in any order | Verifying information retrieval when order doesn’t matter |
| `subset` | Agent calls only tools from reference (no extras) | Ensuring agent doesn’t exceed expected scope |
| `superset` | Agent calls at least the reference tools (extras allowed) | Verifying minimum required actions are taken |

Strict match

The `strict` mode ensures trajectories contain identical messages in the same order with the same tool calls, though it allows for differences in message content. This is useful when you need to enforce a specific sequence of operations, such as requiring a policy lookup before authorizing an action.

Copy

Ask AI

```
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator

@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

agent = create_agent("gpt-4o", tools=[get_weather])

evaluator = create_trajectory_match_evaluator(  
    trajectory_match_mode="strict",  
)  

def test_weather_tool_called_strict():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in San Francisco?")]
    })

    reference_trajectory = [
        HumanMessage(content="What's the weather in San Francisco?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": "get_weather", "args": {"city": "San Francisco"}}
        ]),
        ToolMessage(content="It's 75 degrees and sunny in San Francisco.", tool_call_id="call_1"),
        AIMessage(content="The weather in San Francisco is 75 degrees and sunny."),
    ]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory
    )
    # {
    #     'key': 'trajectory_strict_match',
    #     'score': True,
    #     'comment': None,
    # }
    assert evaluation["score"] is True
```

Unordered match

The `unordered` mode allows the same tool calls in any order, which is helpful when you want to verify that specific information was retrieved but don’t care about the sequence. For example, an agent might need to check both weather and events for a city, but the order doesn’t matter.

Copy

Ask AI

```
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator

@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

@tool
def get_events(city: str):
    """Get events happening in a city."""
    return f"Concert at the park in {city} tonight."

agent = create_agent("gpt-4o", tools=[get_weather, get_events])

evaluator = create_trajectory_match_evaluator(  
    trajectory_match_mode="unordered",  
)  

def test_multiple_tools_any_order():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's happening in SF today?")]
    })

    # Reference shows tools called in different order than actual execution
    reference_trajectory = [
        HumanMessage(content="What's happening in SF today?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": "get_events", "args": {"city": "SF"}},
            {"id": "call_2", "name": "get_weather", "args": {"city": "SF"}},
        ]),
        ToolMessage(content="Concert at the park in SF tonight.", tool_call_id="call_1"),
        ToolMessage(content="It's 75 degrees and sunny in SF.", tool_call_id="call_2"),
        AIMessage(content="Today in SF: 75 degrees and sunny with a concert at the park tonight."),
    ]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory,
    )
    # {
    #     'key': 'trajectory_unordered_match',
    #     'score': True,
    # }
    assert evaluation["score"] is True
```

Subset and superset match

The `superset` and `subset` modes match partial trajectories. The `superset` mode verifies that the agent called at least the tools in the reference trajectory, allowing additional tool calls. The `subset` mode ensures the agent did not call any tools beyond those in the reference.

Copy

Ask AI

```
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.match import create_trajectory_match_evaluator

@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

@tool
def get_detailed_forecast(city: str):
    """Get detailed weather forecast for a city."""
    return f"Detailed forecast for {city}: sunny all week."

agent = create_agent("gpt-4o", tools=[get_weather, get_detailed_forecast])

evaluator = create_trajectory_match_evaluator(  
    trajectory_match_mode="superset",  
)  

def test_agent_calls_required_tools_plus_extra():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in Boston?")]
    })

    # Reference only requires get_weather, but agent may call additional tools
    reference_trajectory = [
        HumanMessage(content="What's the weather in Boston?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": "get_weather", "args": {"city": "Boston"}},
        ]),
        ToolMessage(content="It's 75 degrees and sunny in Boston.", tool_call_id="call_1"),
        AIMessage(content="The weather in Boston is 75 degrees and sunny."),
    ]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory,
    )
    # {
    #     'key': 'trajectory_superset_match',
    #     'score': True,
    #     'comment': None,
    # }
    assert evaluation["score"] is True
```

You can also set the `tool_args_match_mode` property and/or `tool_args_match_overrides` to customize how the evaluator considers equality between tool calls in the actual trajectory vs. the reference. By default, only tool calls with the same arguments to the same tool are considered equal. Visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#tool-args-match-modes) for more details.

### [​](https://docs.langchain.com/oss/python/langchain/test#llm-as-judge-evaluator)

LLM-as-Judge Evaluator

You can also use an LLM to evaluate the agent’s execution path with the `create_trajectory_llm_as_judge` function. Unlike the trajectory match evaluators, it doesn’t require a reference trajectory, but one can be provided if available.

Without reference trajectory

Copy

Ask AI

```
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT

@tool
def get_weather(city: str):
    """Get weather information for a city."""
    return f"It's 75 degrees and sunny in {city}."

agent = create_agent("gpt-4o", tools=[get_weather])

evaluator = create_trajectory_llm_as_judge(  
    model="openai:o3-mini",  
    prompt=TRAJECTORY_ACCURACY_PROMPT,  
)  

def test_trajectory_quality():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in Seattle?")]
    })

    evaluation = evaluator(
        outputs=result["messages"],
    )
    # {
    #     'key': 'trajectory_accuracy',
    #     'score': True,
    #     'comment': 'The provided agent trajectory is reasonable...'
    # }
    assert evaluation["score"] is True
```

With reference trajectory

If you have a reference trajectory, you can add an extra variable to your prompt and pass in the reference trajectory. Below, we use the prebuilt `TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE` prompt and configure the `reference_outputs` variable:

Copy

Ask AI

```
evaluator = create_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
)
evaluation = judge_with_reference(
    outputs=result["messages"],
    reference_outputs=reference_trajectory,
)
```

For more configurability over how the LLM evaluates the trajectory, visit the [repository](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#trajectory-llm-as-judge).

### [​](https://docs.langchain.com/oss/python/langchain/test#async-support)

Async Support

All `agentevals` evaluators support Python asyncio. For evaluators that use factory functions, async versions are available by adding `async` after `create_` in the function name.

Async judge and evaluator example

Copy

Ask AI

```
from agentevals.trajectory.llm import create_async_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
from agentevals.trajectory.match import create_async_trajectory_match_evaluator

async_judge = create_async_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

async_evaluator = create_async_trajectory_match_evaluator(
    trajectory_match_mode="strict",
)

async def test_async_evaluation():
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="What's the weather?")]
    })

    evaluation = await async_judge(outputs=result["messages"])
    assert evaluation["score"] is True
```

[​](https://docs.langchain.com/oss/python/langchain/test#langsmith-integration)

LangSmith Integration
------------------------------------------------------------------------------------------------------

For tracking experiments over time, you can log evaluator results to [LangSmith](https://smith.langchain.com/), a platform for building production-grade LLM applications that includes tracing, evaluation, and experimentation tools.First, set up LangSmith by setting the required environment variables:

Copy

Ask AI

```
export LANGSMITH_API_KEY="your_langsmith_api_key"
export LANGSMITH_TRACING="true"
```

LangSmith offers two main approaches for running evaluations: [pytest](https://docs.langchain.com/langsmith/pytest) integration and the `evaluate` function.

Using pytest integration

Copy

Ask AI

```
import pytest
from langsmith import testing as t
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT

trajectory_evaluator = create_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

@pytest.mark.langsmith
def test_trajectory_accuracy():
    result = agent.invoke({
        "messages": [HumanMessage(content="What's the weather in SF?")]
    })

    reference_trajectory = [
        HumanMessage(content="What's the weather in SF?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": "get_weather", "args": {"city": "SF"}},
        ]),
        ToolMessage(content="It's 75 degrees and sunny in SF.", tool_call_id="call_1"),
        AIMessage(content="The weather in SF is 75 degrees and sunny."),
    ]

    # Log inputs, outputs, and reference outputs to LangSmith
    t.log_inputs({})
    t.log_outputs({"messages": result["messages"]})
    t.log_reference_outputs({"messages": reference_trajectory})

    trajectory_evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory
    )
```

Run the evaluation with pytest:

Copy

Ask AI

```
pytest test_trajectory.py --langsmith-output
```

Results will be automatically logged to LangSmith.

Using the evaluate function

Alternatively, you can create a dataset in LangSmith and use the `evaluate` function:

Copy

Ask AI

```
from langsmith import Client
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT

client = Client()

trajectory_evaluator = create_trajectory_llm_as_judge(
    model="openai:o3-mini",
    prompt=TRAJECTORY_ACCURACY_PROMPT,
)

def run_agent(inputs):
    """Your agent function that returns trajectory messages."""
    return agent.invoke(inputs)["messages"]

experiment_results = client.evaluate(
    run_agent,
    data="your_dataset_name",
    evaluators=[trajectory_evaluator]
)
```

Results will be automatically logged to LangSmith.

To learn more about evaluating your agent, see the [LangSmith docs](https://docs.langchain.com/langsmith/pytest).

[​](https://docs.langchain.com/oss/python/langchain/test#recording-%26-replaying-http-calls)

Recording & Replaying HTTP Calls
------------------------------------------------------------------------------------------------------------------------------

Integration tests that call real LLM APIs can be slow and expensive, especially when run frequently in CI/CD pipelines. We recommend using a library for recording HTTP requests and responses, then replaying them in subsequent runs without making actual network calls.You can use [`vcrpy`](https://pypi.org/project/vcrpy/1.5.2/) to achieve this. If you’re using `pytest`, the [`pytest-recording` plugin](https://pypi.org/project/pytest-recording/) provides a simple way to enable this with minimal configuration. Request/responses are recorded in cassettes, which are then used to mock the real network calls in subsequent runs.Set up your `conftest.py` file to filter out sensitive information from the cassettes:

conftest.py

Copy

Ask AI

```
import pytest

@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": [
            ("authorization", "XXXX"),
            ("x-api-key", "XXXX"),
            # ... other headers you want to mask
        ],
        "filter_query_parameters": [
            ("api_key", "XXXX"),
            ("key", "XXXX"),
        ],
    }
```

Then configure your project to recognise the `vcr` marker:

pytest.ini

pyproject.toml

Copy

Ask AI

```
[pytest]
markers =
    vcr: record/replay HTTP via VCR
addopts = --record-mode=once
```

The `--record-mode=once` option records HTTP interactions on the first run and replays them on subsequent runs.

Now, simply decorate your tests with the `vcr` marker:

Copy

Ask AI

```
@pytest.mark.vcr()
def test_agent_trajectory():
    # ...
```

The first time you run this test, your agent will make real network calls and pytest will generate a cassette file `test_agent_trajectory.yaml` in the `tests/cassettes` directory. Subsequent runs will use that cassette to mock the real network calls, granted the agent’s requests don’t change from the previous run. If they do, the test will fail and you’ll need to delete the cassette and rerun the test to record fresh interactions.

When you modify prompts, add new tools, or change expected trajectories, your saved cassettes will become outdated and your existing tests **will fail**. You should delete the corresponding cassette files and rerun the tests to record fresh interactions.

* * *

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/test.mdx)

[Connect these docs programmatically](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

Yes No

[Studio Previous](https://docs.langchain.com/oss/python/langchain/studio)[Deploy Next](https://docs.langchain.com/oss/python/langchain/deploy)

⌘I

[Docs by LangChain home page![Image 3: light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![Image 4: dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

Resources

[Forum](https://forum.langchain.com/)[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Trust Center](https://trust.langchain.com/)

Company

[About](https://langchain.com/about)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

[Powered by Mintlify](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=langchain-5e9cc07a)