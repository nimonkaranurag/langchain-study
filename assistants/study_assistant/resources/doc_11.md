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

* [Building a knowledge base](#building-a-knowledge-base)
* [From retrieval to RAG](#from-retrieval-to-rag)
* [Retrieval Pipeline](#retrieval-pipeline)
* [Building Blocks](#building-blocks)
* [RAG Architectures](#rag-architectures)
* [2-step RAG](#2-step-rag)
* [Agentic RAG](#agentic-rag)
* [Hybrid RAG](#hybrid-rag)

[Advanced usage](/oss/python/langchain/guardrails)

# Retrieval

Large language models (LLMs) are powerful, but they have two key limitations:

* **Finite context** — they can’t ingest entire corpora at once.
* **Static knowledge** — their training data is frozen at a point in time.

Retrieval addresses these problems by fetching relevant external knowledge at query time. This is the foundation of **Retrieval-Augmented Generation (RAG)**: enhancing an LLM’s answers with context-specific information.

## [​](#building-a-knowledge-base) Building a knowledge base

A **knowledge base** is a repository of documents or structured data used during retrieval. If you need a custom knowledge base, you can use LangChain’s document loaders and vector stores to build one from your own data.

If you already have a knowledge base (e.g., a SQL database, CRM, or internal documentation system), you do **not** need to rebuild it. You can:

* Connect it as a **tool** for an agent in Agentic RAG.
* Query it and supply the retrieved content as context to the LLM [(2-Step RAG)](#2-step-rag).

See the following tutorial to build a searchable knowledge base and minimal RAG workflow: [## Tutorial: Semantic search

Learn how to create a searchable knowledge base from your own data using LangChain’s document loaders, embeddings, and vector stores. In this tutorial, you’ll build a search engine over a PDF, enabling retrieval of passages relevant to a query. You’ll also implement a minimal RAG workflow on top of this engine to see how external knowledge can be integrated into LLM reasoning.](/oss/python/langchain/knowledge-base)

### [​](#from-retrieval-to-rag) From retrieval to RAG

Retrieval allows LLMs to access relevant context at runtime. But most real-world applications go one step further: they **integrate retrieval with generation** to produce grounded, context-aware answers. This is the core idea behind **Retrieval-Augmented Generation (RAG)**. The retrieval pipeline becomes a foundation for a broader system that combines search with generation.

### [​](#retrieval-pipeline) Retrieval Pipeline

A typical retrieval workflow looks like this: Each component is modular: you can swap loaders, splitters, embeddings, or vector stores without rewriting the app’s logic.

### [​](#building-blocks) Building Blocks

[## Document loaders

Ingest data from external sources (Google Drive, Slack, Notion, etc.), returning standardized [`Document`](https://reference.langchain.com/python/langchain_core/documents/#langchain_core.documents.base.Document) objects.](/oss/python/integrations/document_loaders)[## Text splitters

Break large docs into smaller chunks that will be retrievable individually and fit within a model’s context window.](/oss/python/integrations/splitters)[## Embedding models

An embedding model turns text into a vector of numbers so that texts with similar meaning land close together in that vector space.](/oss/python/integrations/text_embedding)[## Vector stores

Specialized databases for storing and searching embeddings.](/oss/python/integrations/vectorstores)[## Retrievers

A retriever is an interface that returns documents given an unstructured query.](/oss/python/integrations/retrievers)

## [​](#rag-architectures) RAG Architectures

RAG can be implemented in multiple ways, depending on your system’s needs. We outline each type in the sections below.

| Architecture | Description | Control | Flexibility | Latency | Example Use Case |
| --- | --- | --- | --- | --- | --- |
| **2-Step RAG** | Retrieval always happens before generation. Simple and predictable | ✅ High | ❌ Low | ⚡ Fast | FAQs, documentation bots |
| **Agentic RAG** | An LLM-powered agent decides *when* and *how* to retrieve during reasoning | ❌ Low | ✅ High | ⏳ Variable | Research assistants with access to multiple tools |
| **Hybrid** | Combines characteristics of both approaches with validation steps | ⚖️ Medium | ⚖️ Medium | ⏳ Variable | Domain-specific Q&A with quality validation |

**Latency**: Latency is generally more **predictable** in **2-Step RAG**, as the maximum number of LLM calls is known and capped. This predictability assumes that LLM inference time is the dominant factor. However, real-world latency may also be affected by the performance of retrieval steps—such as API response times, network delays, or database queries—which can vary based on the tools and infrastructure in use.

### [​](#2-step-rag) 2-step RAG

In **2-Step RAG**, the retrieval step is always executed before the generation step. This architecture is straightforward and predictable, making it suitable for many applications where the retrieval of relevant documents is a clear prerequisite for generating an answer. [## Tutorial: Retrieval-Augmented Generation (RAG)

See how to build a Q&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation. This tutorial walks through two approaches:

* A **RAG agent** that runs searches with a flexible tool—great for general-purpose use.
* A **2-step RAG** chain that requires just one LLM call per query—fast and efficient for simpler tasks.](/oss/python/langchain/rag#rag-chains)

### [​](#agentic-rag) Agentic RAG

**Agentic Retrieval-Augmented Generation (RAG)** combines the strengths of Retrieval-Augmented Generation with agent-based reasoning. Instead of retrieving documents before answering, an agent (powered by an LLM) reasons step-by-step and decides **when** and **how** to retrieve information during the interaction.

The only thing an agent needs to enable RAG behavior is access to one or more **tools** that can fetch external knowledge — such as documentation loaders, web APIs, or database queries.

Copy

Ask AI

```
import requests import  requestsfrom langchain.tools import tool from langchain.tools import  toolfrom langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_modelfrom langchain.agents import create_agent from langchain.agents import  create_agent  @tool @tooldef fetch_url(url: str) -> str: def  fetch_url(url: str) -> str:  """Fetch text content from a URL"""  """Fetch text content from a URL""" response = requests.get(url, timeout=10.0)  response = requests.get(url, timeout =10.0) response.raise_for_status() response.raise_for_status() return response.text  return response.text system_prompt = """\ system_prompt =  """ \Use fetch_url when you need to fetch information from a web-page; quote relevant snippets.Use fetch_url when you need to fetch information from a web-page; quote relevant snippets. """ """ agent = create_agent(agent = create_agent( model="claude-sonnet-4-5-20250929",  model ="claude-sonnet-4-5-20250929", tools=[fetch_url], # A tool for retrieval  tools =[fetch_url], # A tool for retrieval system_prompt=system_prompt,  system_prompt =system_prompt,))
```

ShowExtended example: Agentic RAG for LangGraph's llms.txt

This example implements an **Agentic RAG system** to assist users in querying LangGraph documentation. The agent begins by loading [llms.txt](https://llmstxt.org/), which lists available documentation URLs, and can then dynamically use a `fetch_documentation` tool to retrieve and process the relevant content based on the user’s question.

Copy

Ask AI

```
import requests import  requestsfrom langchain.agents import create_agent from langchain.agents import  create_agentfrom langchain.messages import HumanMessage from langchain.messages import  HumanMessagefrom langchain.tools import tool from langchain.tools import  tool from markdownify import markdownify from  markdownify import  markdownify ALLOWED_DOMAINS = ["https://langchain-ai.github.io/"] ALLOWED_DOMAINS = ["https://langchain-ai.github.io/"]LLMS_TXT = 'https://langchain-ai.github.io/langgraph/llms.txt' LLMS_TXT = 'https://langchain-ai.github.io/langgraph/llms.txt'  @tool @tooldef fetch_documentation(url: str) -> str: def  fetch_documentation(url: str) -> str:  """Fetch and convert documentation from a URL"""  """Fetch and convert documentation from a URL""" if not any(url.startswith(domain) for domain in ALLOWED_DOMAINS):  if  not  any(url.startswith(domain) for  domain in  ALLOWED_DOMAINS): return ( return ( "Error: URL not allowed. " "Error: URL not allowed. " f"Must start with one of: {', '.join(ALLOWED_DOMAINS)}"  f"Must start with one of: {', '.join(ALLOWED_DOMAINS)} " ) ) response = requests.get(url, timeout=10.0)  response = requests.get(url, timeout =10.0) response.raise_for_status() response.raise_for_status() return markdownify(response.text)  return markdownify(response.text) # We will fetch the content of llms.txt, so this can# We will fetch the content of llms.txt, so this can# be done ahead of time without requiring an LLM request.# be done ahead of time without requiring an LLM request.llms_txt_content = requests.get(LLMS_TXT).text llms_txt_content = requests.get(LLMS_TXT).text # System prompt for the agent # System prompt for the agentsystem_prompt = f""" system_prompt =  f """You are an expert Python developer and technical assistant.You are an expert Python developer and technical assistant.Your primary role is to help users with questions about LangGraph and related tools.Your primary role is to help users with questions about LangGraph and related tools. Instructions:Instructions: 1. If a user asks a question you're unsure about — or one that likely involves API usage,1. If a user asks a question you're unsure about — or one that likely involves API usage, behavior, or configuration — you MUST use the `fetch_documentation` tool to consult the relevant docs. behavior, or configuration — you MUST use the `fetch_documentation` tool to consult the relevant docs.2. When citing documentation, summarize clearly and include relevant context from the content.2. When citing documentation, summarize clearly and include relevant context from the content.3. Do not use any URLs outside of the allowed domain.3. Do not use any URLs outside of the allowed domain.4. If a documentation fetch fails, tell the user and proceed with your best expert understanding.4. If a documentation fetch fails, tell the user and proceed with your best expert understanding. You can access official documentation from the following approved sources:You can access official documentation from the following approved sources: {llms_txt_content}{llms_txt_content} You MUST consult the documentation to get up to date documentation You MUST consult the documentation to get up to date documentationbefore answering a user's question about LangGraph.before answering a user's question about LangGraph. Your answers should be clear, concise, and technically accurate.Your answers should be clear, concise, and technically accurate. """ """ tools = [fetch_documentation] tools = [fetch_documentation] model = init_chat_model("claude-sonnet-4-0", max_tokens=32_000) model = init_chat_model("claude-sonnet-4-0", max_tokens = 32_000) agent = create_agent(agent = create_agent( model=model,  model =model, tools=tools,  tools =tools,  system_prompt=system_prompt,  system_prompt =system_prompt,  name="Agentic RAG",  name = "Agentic RAG",)) response = agent.invoke({response = agent.invoke({ 'messages': [ 'messages': [ HumanMessage(content=( HumanMessage(content =( "Write a short example of a langgraph agent using the "  "Write a short example of a langgraph agent using the " "prebuilt create react agent. the agent should be able " "prebuilt create react agent. the agent should be able " "to look up stock pricing information." "to look up stock pricing information." )) )) ] ]})}) print(response['messages'][-1].content) print(response['messages'][- 1].content)
```

 [## Tutorial: Retrieval-Augmented Generation (RAG)

See how to build a Q&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation. This tutorial walks through two approaches:

* A **RAG agent** that runs searches with a flexible tool—great for general-purpose use.
* A **2-step RAG** chain that requires just one LLM call per query—fast and efficient for simpler tasks.](/oss/python/langchain/rag)

### [​](#hybrid-rag) Hybrid RAG

Hybrid RAG combines characteristics of both 2-Step and Agentic RAG. It introduces intermediate steps such as query preprocessing, retrieval validation, and post-generation checks. These systems offer more flexibility than fixed pipelines while maintaining some control over execution. Typical components include:

* **Query enhancement**: Modify the input question to improve retrieval quality. This can involve rewriting unclear queries, generating multiple variations, or expanding queries with additional context.
* **Retrieval validation**: Evaluate whether retrieved documents are relevant and sufficient. If not, the system may refine the query and retrieve again.
* **Answer validation**: Check the generated answer for accuracy, completeness, and alignment with source content. If needed, the system can regenerate or revise the answer.

The architecture often supports multiple iterations between these steps: This architecture is suitable for:

* Applications with ambiguous or underspecified queries
* Systems that require validation or quality control steps
* Workflows involving multiple sources or iterative refinement

[## Tutorial: Agentic RAG with Self-Correction

An example of **Hybrid RAG** that combines agentic reasoning with retrieval and self-correction.](/oss/python/langgraph/agentic-rag) 

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/retrieval.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Multi-agent](/oss/python/langchain/multi-agent)[Long-term memory](/oss/python/langchain/long-term-memory)