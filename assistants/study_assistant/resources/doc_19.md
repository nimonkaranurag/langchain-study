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

* [Interrupt decision types](#interrupt-decision-types)
* [Configuring interrupts](#configuring-interrupts)
* [Responding to interrupts](#responding-to-interrupts)
* [Decision types](#decision-types)
* [Execution lifecycle](#execution-lifecycle)
* [Custom HITL logic](#custom-hitl-logic)

[Advanced usage](/oss/python/langchain/guardrails)

# Human-in-the-loop

The Human-in-the-Loop (HITL) middleware lets you add human oversight to agent tool calls. When a model proposes an action that might require review — for example, writing to a file or executing SQL — the middleware can pause execution and wait for a decision. It does this by checking each tool call against a configurable policy. If intervention is needed, the middleware issues an [interrupt](https://reference.langchain.com/python/langgraph/types/#langgraph.types.interrupt) that halts execution. The graph state is saved using LangGraph’s [persistence layer](/oss/python/langgraph/persistence), so execution can pause safely and resume later. A human decision then determines what happens next: the action can be approved as-is (`approve`), modified before running (`edit`), or rejected with feedback (`reject`).

## [​](#interrupt-decision-types) Interrupt decision types

The middleware defines three built-in ways a human can respond to an interrupt:

| Decision Type | Description | Example Use Case |
| --- | --- | --- |
| ✅ `approve` | The action is approved as-is and executed without changes. | Send an email draft exactly as written |
| ✏️ `edit` | The tool call is executed with modifications. | Change the recipient before sending an email |
| ❌ `reject` | The tool call is rejected, with an explanation added to the conversation. | Reject an email draft and explain how to rewrite it |

The available decision types for each tool depend on the policy you configure in `interrupt_on`. When multiple tool calls are paused at the same time, each action requires a separate decision. Decisions must be provided in the same order as the actions appear in the interrupt request.

When **editing** tool arguments, make changes conservatively. Significant modifications to the original arguments may cause the model to re-evaluate its approach and potentially execute the tool multiple times or take unexpected actions.

## [​](#configuring-interrupts) Configuring interrupts

To use HITL, add the middleware to the agent’s `middleware` list when creating the agent. You configure it with a mapping of tool actions to the decision types that are allowed for each action. The middleware will interrupt execution when a tool call matches an action in the mapping.

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.agents.middleware import HumanInTheLoopMiddleware from langchain.agents.middleware import  HumanInTheLoopMiddleware from langgraph.checkpoint.memory import InMemorySaver from langgraph.checkpoint.memory import  InMemorySaver  agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[write_file_tool, execute_sql_tool, read_data_tool],  tools =[write_file_tool, execute_sql_tool, read_data_tool], middleware=[ middleware =[ HumanInTheLoopMiddleware(  HumanInTheLoopMiddleware(  interrupt_on={ interrupt_on ={ "write_file": True, # All decisions (approve, edit, reject) allowed  "write_file": True, # All decisions (approve, edit, reject) allowed "execute_sql": {"allowed_decisions": ["approve", "reject"]}, # No editing allowed  "execute_sql": {"allowed_decisions": ["approve", "reject"]}, # No editing allowed # Safe operation, no approval needed # Safe operation, no approval needed "read_data": False,  "read_data": False, }, }, # Prefix for interrupt messages - combined with tool name and args to form the full message # Prefix for interrupt messages - combined with tool name and args to form the full message # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'" # e.g., "Tool execution pending approval: execute_sql with query='DELETE FROM...'"  # Individual tools can override this by specifying a "description" in their interrupt config  # Individual tools can override this by specifying a "description" in their interrupt config description_prefix="Tool execution pending approval",  description_prefix = "Tool execution pending approval", ), ), ], ], # Human-in-the-loop requires checkpointing to handle interrupts. # Human-in-the-loop requires checkpointing to handle interrupts. # In production, use a persistent checkpointer like AsyncPostgresSaver. # In production, use a persistent checkpointer like AsyncPostgresSaver. checkpointer=InMemorySaver(),  checkpointer =InMemorySaver(), ))
```

You must configure a checkpointer to persist the graph state across interrupts. In production, use a persistent checkpointer like [`AsyncPostgresSaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.postgres.aio.AsyncPostgresSaver). For testing or prototyping, use [`InMemorySaver`](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.memory.InMemorySaver).When invoking the agent, pass a `config` that includes the **thread ID** to associate execution with a conversation thread. See the [LangGraph interrupts documentation](/oss/python/langgraph/interrupts) for details.

## [​](#responding-to-interrupts) Responding to interrupts

When you invoke the agent, it runs until it either completes or an interrupt is raised. An interrupt is triggered when a tool call matches the policy you configured in `interrupt_on`. In that case, the invocation result will include an `__interrupt__` field with the actions that require review. You can then present those actions to a reviewer and resume execution once decisions are provided.

Copy

Ask AI

```
from langgraph.types import Command from langgraph.types import  Command # Human-in-the-loop leverages LangGraph's persistence layer.# Human-in-the-loop leverages LangGraph's persistence layer.# You must provide a thread ID to associate the execution with a conversation thread,# You must provide a thread ID to associate the execution with a conversation thread,# so the conversation can be paused and resumed (as is needed for human review).# so the conversation can be paused and resumed (as is needed for human review).config = {"configurable": {"thread_id": "some_id"}} config = {"configurable": {"thread_id": "some_id"}} # Run the graph until the interrupt is hit.# Run the graph until the interrupt is hit.result = agent.invoke(result = agent.invoke( { { "messages": [ "messages": [ { { "role": "user",  "role": "user", "content": "Delete old records from the database",  "content": "Delete old records from the database", } } ] ] }, }, config=config  config = config )) # The interrupt contains the full HITL request with action_requests and review_configs # The interrupt contains the full HITL request with action_requests and review_configsprint(result['__interrupt__']) print(result['__interrupt__'])# > [# > [# > Interrupt(# > Interrupt(# > value={# > value={# > 'action_requests': [# > 'action_requests': [# > {# > {# > 'name': 'execute_sql',# > 'name': 'execute_sql',# > 'arguments': {'query': 'DELETE FROM records WHERE created_at < NOW() - INTERVAL \'30 days\';'},# > 'arguments': {'query': 'DELETE FROM records WHERE created_at < NOW() - INTERVAL \'30 days\';'},# > 'description': 'Tool execution pending approval\n\nTool: execute_sql\nArgs: {...}'# > 'description': 'Tool execution pending approval\n\nTool: execute_sql\nArgs: {...}'# > }# > }# > ],# > ],# > 'review_configs': [# > 'review_configs': [# > {# > {# > 'action_name': 'execute_sql',# > 'action_name': 'execute_sql',# > 'allowed_decisions': ['approve', 'reject']# > 'allowed_decisions': ['approve', 'reject']# > }# > }# > ]# > ]# > }# > }# > )# > )# > ]# > ]  # Resume with approval decision # Resume with approval decisionagent.invoke(agent.invoke( Command(  Command(  resume={"decisions": [{"type": "approve"}]} # or "edit", "reject"  resume ={"decisions": [{"type": "approve"}]} # or "edit", "reject" ),  ),  config=config # Same thread ID to resume the paused conversation  config = config # Same thread ID to resume the paused conversation))
```

### [​](#decision-types) Decision types

* ✅ approve
* ✏️ edit
* ❌ reject

Use `approve` to approve the tool call as-is and execute it without changes.

Copy

Ask AI

```
agent.invoke(agent.invoke( Command( Command( # Decisions are provided as a list, one per action under review. # Decisions are provided as a list, one per action under review.  # The order of decisions must match the order of actions  # The order of decisions must match the order of actions # listed in the `__interrupt__` request. # listed in the `__interrupt__` request. resume={ resume ={ "decisions": [ "decisions": [ { { "type": "approve",  "type": "approve", } } ] ] } } ), ), config=config # Same thread ID to resume the paused conversation  config = config # Same thread ID to resume the paused conversation))
```

## [​](#execution-lifecycle) Execution lifecycle

The middleware defines an `after_model` hook that runs after the model generates a response but before any tool calls are executed:

1. The agent invokes the model to generate a response.
2. The middleware inspects the response for tool calls.
3. If any calls require human input, the middleware builds a `HITLRequest` with `action_requests` and `review_configs` and calls [interrupt](https://reference.langchain.com/python/langgraph/types/#langgraph.types.interrupt).
4. The agent waits for human decisions.
5. Based on the `HITLResponse` decisions, the middleware executes approved or edited calls, synthesizes [ToolMessage](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage)’s for rejected calls, and resumes execution.

## [​](#custom-hitl-logic) Custom HITL logic

For more specialized workflows, you can build custom HITL logic directly using the [interrupt](https://reference.langchain.com/python/langgraph/types/#langgraph.types.interrupt) primitive and [middleware](/oss/python/langchain/middleware) abstraction. Review the [execution lifecycle](#execution-lifecycle) above to understand how to integrate interrupts into the agent’s operation. 

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/human-in-the-loop.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Model Context Protocol (MCP)](/oss/python/langchain/mcp)[Multi-agent](/oss/python/langchain/multi-agent)