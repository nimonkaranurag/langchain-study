We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

* [Overview](/oss/python/langgraph/overview)

##### LangGraph v1.0

* [Release notes](/oss/python/releases/langgraph-v1)
* [Migration guide](/oss/python/migrate/langgraph-v1)

##### Get started

* [Install](/oss/python/langgraph/install)
* [Quickstart](/oss/python/langgraph/quickstart)
* [Local server](/oss/python/langgraph/local-server)
* [Thinking in LangGraph](/oss/python/langgraph/thinking-in-langgraph)
* [Workflows + agents](/oss/python/langgraph/workflows-agents)

##### Capabilities

* [Persistence](/oss/python/langgraph/persistence)
* [Durable execution](/oss/python/langgraph/durable-execution)
* [Streaming](/oss/python/langgraph/streaming)
* [Interrupts](/oss/python/langgraph/interrupts)
* [Time travel](/oss/python/langgraph/use-time-travel)
* [Memory](/oss/python/langgraph/add-memory)
* [Subgraphs](/oss/python/langgraph/use-subgraphs)

##### Production

* [Application structure](/oss/python/langgraph/application-structure)
* [Studio](/oss/python/langgraph/studio)
* [Test](/oss/python/langgraph/test)
* [Deploy](/oss/python/langgraph/deploy)
* [Agent Chat UI](/oss/python/langgraph/ui)
* [Observability](/oss/python/langgraph/observability)

##### LangGraph APIs

* [Runtime](/oss/python/langgraph/pregel)

* [Prerequisites](#prerequisites)
* [1. Install the LangGraph CLI](#1-install-the-langgraph-cli)
* [2. Create a LangGraph app 🌱](#2-create-a-langgraph-app-%F0%9F%8C%B1)
* [3. Install dependencies](#3-install-dependencies)
* [4. Create a .env file](#4-create-a-env-file)
* [5. Launch Agent server 🚀](#5-launch-agent-server-%F0%9F%9A%80)
* [6. Test your application in Studio](#6-test-your-application-in-studio)
* [7. Test the API](#7-test-the-api)
* [Next steps](#next-steps)

[Get started](/oss/python/langgraph/install)

# Run a local server

This guide shows you how to run a LangGraph application locally.

## [​](#prerequisites) Prerequisites

Before you begin, ensure you have the following:

* An API key for [LangSmith](https://smith.langchain.com/settings) - free to sign up

## [​](#1-install-the-langgraph-cli) 1. Install the LangGraph CLI

Copy

Ask AI

```
# Python >= 3.11 is required.# Python >= 3.11 is required.pip install -U "langgraph-cli[inmem]" pip  install -U "langgraph-cli[inmem]"
```

## [​](#2-create-a-langgraph-app-%F0%9F%8C%B1) 2. Create a LangGraph app 🌱

Create a new app from the [`new-langgraph-project-python` template](https://github.com/langchain-ai/new-langgraph-project). This template demonstrates a single-node application you can extend with your own logic.

Copy

Ask AI

```
langgraph new path/to/your/app --template new-langgraph-project-python langgraph  new path/to/your/app --template new-langgraph-project-python
```

**Additional templates** If you use `langgraph new` without specifying a template, you will be presented with an interactive menu that will allow you to choose from a list of available templates.

## [​](#3-install-dependencies) 3. Install dependencies

In the root of your new LangGraph app, install the dependencies in `edit` mode so your local changes are used by the server:

Copy

Ask AI

```
cd path/to/your/app cd path/to/your/apppip install -e . pip  install -e .
```

## [​](#4-create-a-env-file) 4. Create a `.env` file

You will find a `.env.example` in the root of your new LangGraph app. Create a `.env` file in the root of your new LangGraph app and copy the contents of the `.env.example` file into it, filling in the necessary API keys:

Copy

Ask AI

```
LANGSMITH_API_KEY=lsv2... LANGSMITH_API_KEY =lsv2...
```

## [​](#5-launch-agent-server-%F0%9F%9A%80) 5. Launch Agent server 🚀

Start the LangGraph API server locally:

Copy

Ask AI

```
langgraph dev langgraph  dev
```

Sample output:

Copy

Ask AI

```
> Ready!> Ready!>>> - API: [http://localhost:2024](http://localhost:2024/)> - API: [http://localhost:2024](http://localhost:2024/)>>> - Docs: http://localhost:2024/docs> - Docs: http://localhost:2024/docs>>> - LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024> - LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024 
```

The `langgraph dev` command starts Agent Server in an in-memory mode. This mode is suitable for development and testing purposes. For production use, deploy Agent Server with access to a persistent storage backend. For more information, see the [Platform setup overview](/langsmith/platform-setup).

## [​](#6-test-your-application-in-studio) 6. Test your application in Studio

[Studio](/langsmith/studio) is a specialized UI that you can connect to LangGraph API server to visualize, interact with, and debug your application locally. Test your graph in Studio by visiting the URL provided in the output of the `langgraph dev` command:

Copy

Ask AI

```
> - LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024> - LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024 
```

For an Agent Server running on a custom host/port, update the baseURL parameter. 

Safari compatibility

Use the `--tunnel` flag with your command to create a secure tunnel, as Safari has limitations when connecting to localhost servers:

Copy

Ask AI

```
langgraph dev --tunnel langgraph  dev --tunnel
```

## [​](#7-test-the-api) 7. Test the API

* Python SDK (async)
* Python SDK (sync)
* Rest API

1. Install the LangGraph Python SDK:

Copy

Ask AI

```
pip install langgraph-sdk pip  install langgraph-sdk
```

1. Send a message to the assistant (threadless run):

Copy

Ask AI

```
from langgraph_sdk import get_client from  langgraph_sdk import  get_client import asyncio import  asyncio client = get_client(url="http://localhost:2024") client = get_client(url ="http://localhost:2024") async def main(): async  def  main(): async for chunk in client.runs.stream( async  for  chunk in client.runs.stream( None, # Threadless run  None, # Threadless run "agent", # Name of assistant. Defined in langgraph.json.  "agent", # Name of assistant. Defined in langgraph.json. input={ input ={ "messages": [{ "messages": [{ "role": "human",  "role": "human", "content": "What is LangGraph?",  "content": "What is LangGraph?", }], }], }, }, ): ): print(f"Receiving new event of type: {chunk.event}...")  print(f"Receiving new event of type: {chunk.event}...") print(chunk.data)  print(chunk.data) print("\n\n")  print(" \n\n ") asyncio.run(main())asyncio.run(main())
```

## [​](#next-steps) Next steps

Now that you have a LangGraph app running locally, take your journey further by exploring deployment and advanced features:

* [Deployment quickstart](/langsmith/deployment-quickstart): Deploy your LangGraph app using LangSmith.
* [LangSmith](/langsmith/home): Learn about foundational LangSmith concepts.
* [Python SDK Reference](https://reference.langchain.com/python/platform/python_sdk/): Explore the Python SDK API Reference.

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langgraph/local-server.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Quickstart](/oss/python/langgraph/quickstart)[Thinking in LangGraph](/oss/python/langgraph/thinking-in-langgraph)