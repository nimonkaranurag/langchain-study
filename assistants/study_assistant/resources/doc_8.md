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

* [Prerequisites](#prerequisites)
* [Enable tracing](#enable-tracing)
* [Quick start](#quick-start)
* [Trace selectively](#trace-selectively)
* [Log to a project](#log-to-a-project)
* [Add metadata to traces](#add-metadata-to-traces)

[Use in production](/oss/python/langchain/studio)

# Observability

Observability is crucial for understanding how your agents behave in production. With LangChain’s [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent), you get built-in observability through [LangSmith](https://smith.langchain.com/) - a powerful platform for tracing, debugging, evaluating, and monitoring your LLM applications. Traces capture every step your agent takes, from the initial user input to the final response, including all tool calls, model interactions, and decision points. This enables you to debug your agents, evaluate performance, and monitor usage.

## [​](#prerequisites) Prerequisites

Before you begin, ensure you have the following:

* A [LangSmith account](https://smith.langchain.com/) (free to sign up)

## [​](#enable-tracing) Enable tracing

All LangChain agents automatically support LangSmith tracing. To enable it, set the following environment variables:

Copy

Ask AI

```
export LANGSMITH_TRACING=true export  LANGSMITH_TRACING = trueexport LANGSMITH_API_KEY=<your-api-key> export  LANGSMITH_API_KEY =<your-api-key>
```

You can get your API key from your [LangSmith settings](https://smith.langchain.com/settings).

## [​](#quick-start) Quick start

No extra code is needed to log a trace to LangSmith. Just run your agent code as you normally would:

Copy

Ask AI

```
from langchain.agents import create_agent from langchain.agents import  create_agent def send_email(to: str, subject: str, body: str): def  send_email(to: str, subject: str, body: str): """Send an email to a recipient.""" """Send an email to a recipient.""" # ... email sending logic # ... email sending logic return f"Email sent to {to}"  return  f "Email sent to {to} " def search_web(query: str): def  search_web(query: str): """Search the web for information.""" """Search the web for information.""" # ... web search logic # ... web search logic return f"Search results for: {query}"  return  f"Search results for: {query} " agent = create_agent(agent = create_agent( model="gpt-4o",  model ="gpt-4o", tools=[send_email, search_web],  tools =[send_email, search_web], system_prompt="You are a helpful assistant that can send emails and search the web."  system_prompt ="You are a helpful assistant that can send emails and search the web.")) # Run the agent - all steps will be traced automatically# Run the agent - all steps will be traced automaticallyresponse = agent.invoke({response = agent.invoke({ "messages": [{"role": "user", "content": "Search for the latest AI news and email a summary to john@example.com"}]  "messages": [{"role": "user", "content": "Search for the latest AI news and email a summary to john@example.com"}]})})
```

By default, the trace will be logged to the project with the name `default`. To configure a custom project name, see [Log to a project](#log-to-a-project).

## [​](#trace-selectively) Trace selectively

You may opt to trace specific invocations or parts of your application using LangSmith’s `tracing_context` context manager:

Copy

Ask AI

```
import langsmith as ls import  langsmith as  ls # This WILL be traced # This WILL be tracedwith ls.tracing_context(enabled=True): with ls.tracing_context(enabled = True): agent.invoke({"messages": [{"role": "user", "content": "Send a test email to alice@example.com"}]}) agent.invoke({"messages": [{"role": "user", "content": "Send a test email to alice@example.com"}]}) # This will NOT be traced (if LANGSMITH_TRACING is not set)# This will NOT be traced (if LANGSMITH_TRACING is not set)agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})agent.invoke({"messages": [{"role": "user", "content": "Send another email"}]})
```

## [​](#log-to-a-project) Log to a project

Statically

You can set a custom project name for your entire application by setting the `LANGSMITH_PROJECT` environment variable:

Copy

Ask AI

```
export LANGSMITH_PROJECT=my-agent-project export  LANGSMITH_PROJECT =my-agent-project
```

 

Dynamically

You can set the project name programmatically for specific operations:

Copy

Ask AI

```
import langsmith as ls import  langsmith as  ls with ls.tracing_context(project_name="email-agent-test", enabled=True): with ls.tracing_context(project_name ="email-agent-test", enabled = True): response = agent.invoke({ response = agent.invoke({ "messages": [{"role": "user", "content": "Send a welcome email"}]  "messages": [{"role": "user", "content": "Send a welcome email"}] }) })
```

## [​](#add-metadata-to-traces) Add metadata to traces

You can annotate your traces with custom metadata and tags:

Copy

Ask AI

```
response = agent.invoke(response = agent.invoke( {"messages": [{"role": "user", "content": "Send a welcome email"}]}, {"messages": [{"role": "user", "content": "Send a welcome email"}]}, config={ config ={ "tags": ["production", "email-assistant", "v1.0"],  "tags": ["production", "email-assistant", "v1.0"], "metadata": { "metadata": { "user_id": "user_123",  "user_id": "user_123", "session_id": "session_456",  "session_id": "session_456", "environment": "production"  "environment": "production" } } } }))
```

`tracing_context` also accepts tags and metadata for fine-grained control:

Copy

Ask AI

```
with ls.tracing_context(with ls.tracing_context( project_name="email-agent-test",  project_name ="email-agent-test", enabled=True,  enabled = True, tags=["production", "email-assistant", "v1.0"],  tags =["production", "email-assistant", "v1.0"], metadata={"user_id": "user_123", "session_id": "session_456", "environment": "production"}):  metadata ={"user_id": "user_123", "session_id": "session_456", "environment": "production"}): response = agent.invoke( response = agent.invoke( {"messages": [{"role": "user", "content": "Send a welcome email"}]} {"messages": [{"role": "user", "content": "Send a welcome email"}]} ) )
```

This custom metadata and tags will be attached to the trace in LangSmith.

To learn more about how to use traces to debug, evaluate, and monitor your agents, see the [LangSmith documentation](/langsmith/home).

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/observability.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Agent Chat UI](/oss/python/langchain/ui)