Studio - Docs by LangChain

[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/oss/python)Python

Search...

Ctrl K

OSS (v1-alpha)

LangChain and LangGraph

- [Overview](/oss/python/langchain/overview)

##### Get started

- [Install](/oss/python/langchain/install)
- [Quickstart](/oss/python/langchain/quickstart)
- [Philosophy](/oss/python/langchain/philosophy)

##### Core components

- [Agents](/oss/python/langchain/agents)
- [Models](/oss/python/langchain/models)
- [Messages](/oss/python/langchain/messages)
- [Tools](/oss/python/langchain/tools)
- [Short-term memory](/oss/python/langchain/short-term-memory)
- [Streaming](/oss/python/langchain/streaming)

##### Advanced usage

- [Long-term memory](/oss/python/langchain/long-term-memory)
- [Context engineering](/oss/python/langchain/context-engineering)
- [Structured output](/oss/python/langchain/structured-output)
- [Model Context Protocol (MCP)](/oss/python/langchain/mcp)
- [Human-in-the-loop - Coming soon](/oss/python/langchain/human-in-the-loop)
- [Multi-agent - Coming soon](/oss/python/langchain/multi-agent)
- [Retrieval](/oss/python/langchain/retrieval)
- [Runtime](/oss/python/langchain/runtime)
- [Middleware](/oss/python/langchain/middleware)

##### Use in production

- [Studio](/oss/python/langchain/studio)
- [Test](/oss/python/langchain/test)
- [Deploy](/oss/python/langchain/deploy)
- [Agent Chat UI](/oss/python/langchain/ui)
- [Observability](/oss/python/langchain/observability)

[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/oss/python)

Python

Search...

Ctrl K

- [GitHub](https://github.com/langchain-ai)
- [Forum](https://forum.langchain.com/)
- [Forum](https://forum.langchain.com/)

Search...

Navigation

Use in production

Studio

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Integrations](/oss/python/integrations/providers)[Learn](/oss/python/learn)[Reference](/oss/python/versioning)[Contributing](/oss/python/contributing)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Integrations](/oss/python/integrations/providers)[Learn](/oss/python/learn)[Reference](/oss/python/versioning)[Contributing](/oss/python/contributing)

- [GitHub](https://github.com/langchain-ai)
- [Forum](https://forum.langchain.com/)

On this page

- [Prerequisites](#prerequisites)
- [Setup local LangGraph server](#setup-local-langgraph-server)
- [1. Install the LangGraph CLI](#1-install-the-langgraph-cli)
- [2. Prepare your agent](#2-prepare-your-agent)
- [3. Environment variables](#3-environment-variables)
- [4. Make your app LangGraph-compatible](#4-make-your-app-langgraph-compatible)
- [5. Install dependencies](#5-install-dependencies)
- [6. View your agent in Studio](#6-view-your-agent-in-studio)

[Use in production](/oss/python/langchain/studio)

# Studio

Copy page

Copy page

**Alpha Notice:** These docs cover the **v1-alpha** release. Content is incomplete and subject to change.For the latest stable version, see the v0 [LangChain Python](https://python.langchain.com/docs/introduction/) or [LangChain JavaScript](https://js.langchain.com/docs/introduction/) docs.

This guide will walk you through how to use **LangGraph Studio** to visualize, interact, and debug your agent locally.
LangGraph Studio is our free-to-use, powerful agent IDE that integrates with [LangSmith](/langsmith/home) to enable tracing, evaluation, and prompt engineering. See exactly how your agent thinks, trace every decision, and ship smarter, more reliable agents.

## [​](#prerequisites) Prerequisites

Before you begin, ensure you have the following:

- An API key for [LangSmith](https://smith.langchain.com/settings) (free to sign up)

## [​](#setup-local-langgraph-server) Setup local LangGraph server

### [​](#1-install-the-langgraph-cli) 1. Install the LangGraph CLI

Copy

Ask AI

```
# Python >= 3.11 is required.
pip install --upgrade "langgraph-cli[inmem]"

```

### [​](#2-prepare-your-agent) 2. Prepare your agent

We’ll use the following simple agent as an example:

agent.py

Copy

Ask AI

```
from langchain.agents import create_agent

model = ChatOpenAI(model="gpt-4o")

def send_email(to: str, subject: str, body: str):
    """Send an email"""
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... email sending logic

    return f"Email sent to {to}"

agent = create_agent(
    "openai:gpt-4o",
    tools=[send_email],
    prompt="You are an email assistant. Always use the send_email tool.",
)

```

### [​](#3-environment-variables) 3. Environment variables

Create a `.env` file in the root of your project and fill in the necessary API keys. We’ll need to set the `LANGSMITH_API_KEY` environment variable to the API key you get from [LangSmith](https://smith.langchain.com/settings).

Be sure not to commit your `.env` to version control systems such as Git!

.env

Copy

Ask AI

```
LANGSMITH_API_KEY=lsv2...

```

### [​](#4-make-your-app-langgraph-compatible) 4. Make your app LangGraph-compatible

Inside your app’s directory, create a configuration file `langgraph.json`:

langgraph.json

Copy

Ask AI

```
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent.py:agent"
  },
  "env": ".env"
}

```

`create_agent()` automatically returns a compiled LangGraph graph that we can pass to the `graphs` key in our configuration file.

See the [LangGraph configuration file reference](/langgraph-platform/cli#configuration-file) for detailed explanations of each key in the JSON object of the configuration file.

So far, our project structure looks like this:

Copy

Ask AI

```
my-app/
├── src
│   └── agent.py
├── .env
└── langgraph.json

```

### [​](#5-install-dependencies) 5. Install dependencies

In the root of your new LangGraph app, install the dependencies:

pip

uv

Copy

Ask AI

```
pip install -e .

```

### [​](#6-view-your-agent-in-studio) 6. View your agent in Studio

Start your LangGraph server:

Copy

Ask AI

```
langgraph dev

```

Safari blocks `localhost` connections to Studio. To work around this, run the above command with `--tunnel` to access Studio via a secure tunnel.

Your agent will be accessible via API (`http://127.0.0.1:2024`) and the Studio UI `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`:

![Agent view in LangGraph studio UI](https://mintcdn.com/langchain-5e9cc07a/TCDks4pdsHdxWmuJ/oss/images/studio_create-agent.png?fit=max&auto=format&n=TCDks4pdsHdxWmuJ&q=85&s=ebd259e9fa24af7d011dfcc568f74be2)

Studio makes each step of your agent easily observable. Replay any input and inspect the exact prompt, tool arguments, return values, and token/latency metrics. If a tool throws an exception, Studio records it with surrounding state so you can spend less time debugging.
Keep your dev server running, edit prompts or tool signatures, and watch Studio hot-reload. Re-run the conversation thread from any step to verify behavior changes. See [Manage threads](/langgraph-platform/threads-studio#edit-thread-history) for more details.
As your agent grows, the same view scales from a single-tool demo to multi-node graphs, keeping decisions legible and reproducible.

For an in-depth look at LangGraph Studio, check out our comprehensive [LangGraph Studio overview](/langgraph-platform/langgraph-studio).

Was this page helpful?

YesNo

[Middleware](/oss/python/langchain/middleware)[Test](/oss/python/langchain/test)

Assistant

Responses are generated using AI and may contain mistakes.

[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-teal.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=16111530672bf976cb54ef2143478342)![dark logo](https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/brand/langchain-docs-lilac.svg?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=b70fb1a2208670492ef94aef14b680be)](https://docs.langchain.com/oss/python)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

Resources

[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Trust Center](https://trust.langchain.com/)

Company

[About](https://langchain.com/about)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChainAI)[linkedin](https://www.linkedin.com/company/langchain/)[youtube](https://www.youtube.com/@LangChain)

[Powered by Mintlify](https://mintlify.com/preview-request?utm_campaign=poweredBy&utm_medium=referral&utm_source=langchain-5e9cc07a)