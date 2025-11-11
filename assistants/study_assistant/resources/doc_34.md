We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

* [Overview](/oss/python/contributing/overview)

##### Contribute

* [Documentation](/oss/python/contributing/documentation)
* [Code](/oss/python/contributing/code)

##### Integrations

* + [Guide](/oss/python/contributing/integrations-langchain)
  + [Implement](/oss/python/contributing/implement-langchain)
  + [Standard tests](/oss/python/contributing/standard-tests-langchain)
  + [Publish](/oss/python/contributing/publish-langchain)
* [Co-marketing](/oss/python/contributing/comarketing)

* [Why contribute an integration to LangChain?](#why-contribute-an-integration-to-langchain%3F)
* [Components to integrate](#components-to-integrate)
* [How to contribute an integration](#how-to-contribute-an-integration)

[Integrations](/oss/python/contributing/integrations-langchain)

[LangChain](/oss/python/contributing/integrations-langchain)

# Contributing integrations

**Integrations are a core component of LangChain.** LangChain provides standard interfaces for several different components (language models, vector stores, etc) that are crucial when building LLM applications. Contributing an integration helps expand LangChain’s ecosystem and makes your service discoverable to millions of developers.

## [​](#why-contribute-an-integration-to-langchain%3F) Why contribute an integration to LangChain?

## Discoverability

LangChain is the most used framework for building LLM applications, with over 20 million monthly downloads.

## Interoperability

LangChain components expose a standard interface, allowing developers to easily swap them for each other. If you implement a LangChain integration, any developer using a different component will easily be able to swap yours in.

## Best Practices

Through their standard interface, LangChain components encourage and facilitate best practices (streaming, async, etc.) that improve developer experience and application performance.

## [​](#components-to-integrate) Components to integrate

While any component can be integrated into LangChain, there are specific types of integrations we encourage more: **Integrate these ✅**:

* [**Chat Models**](/oss/python/integrations/chat): Most actively used component type
* [**Tools/Toolkits**](/oss/python/integrations/tools): Enable agent capabilities
* [**Retrievers**](/oss/python/integrations/retrievers): Core to RAG applications
* [**Embedding Models**](/oss/python/integrations/text_embedding): Foundation for vector operations
* [**Vector Stores**](/oss/python/integrations/vectorstores): Essential for semantic search

**Not these ❌**:

* **LLMs (Text-Completion Models)**: Deprecated in favor of [Chat Models](/oss/python/integrations/chat)
* [**Document Loaders**](/oss/python/integrations/document_loaders): High maintenance burden
* [**Key-Value Stores**](/oss/python/integrations/stores): Limited usage
* **Document Transformers**: Niche use cases
* **Model Caches**: Infrastructure concerns
* **Graphs**: Complex abstractions
* **Message Histories**: Storage abstractions
* **Callbacks**: System-level components
* **Chat Loaders**: Limited demand
* **Adapters**: Edge case utilities

## [​](#how-to-contribute-an-integration) How to contribute an integration

1

Confirm eligibility

Verify that your integration is in the list of [encouraged components](#components-to-integrate) we are currently accepting.

2

Implement your package

[## How to implement a LangChain integration](/oss/python/contributing/implement-langchain)

3

Pass standard tests

If applicable, implement support for LangChain’s [standard test](/oss/python/contributing/standard-tests-langchain) suite for your integration and successfully run them.

4

Publish integration

[## How to publish an integration](/oss/python/contributing/publish-langchain)

5

Add documentation

Open a PR to add documentation for your integration to the official LangChain docs.

Integration documentation guide

An integration is only as useful as its documentation. To ensure a consistent experience for users, docs are required for all new integrations. We have a standard starting-point template for each type of integration for you to copy and modify.In a new PR to the LangChain [docs repo](https://github.com/langchain-ai/docs), create a new file in the relevant directory under `src/oss/python/integrations//integration_name.mdx` using the appropriate template file:

* [Chat models](https://github.com/langchain-ai/docs/blob/main/src/oss/python/integrations/chat/TEMPLATE.mdx)
* [Tools and toolkits](https://github.com/langchain-ai/docs/blob/main/src/oss/python/integrations/tools/TEMPLATE.mdx)
* [Retrievers](https://github.com/langchain-ai/docs/blob/main/src/oss/python/integrations/retrievers/TEMPLATE.mdx)
* Text splitters - Coming soon
* Embedding models - Coming soon
* [Vector stores](https://github.com/langchain-ai/docs/blob/main/src/oss/python/integrations/vectorstores/TEMPLATE.mdx)
* Document loaders - Coming soon
* Key-value stores - Coming soon

For reference docs, please open an issue on the repo so that a maintainer can add them.

Co-marketing

(Optional) Engage with the LangChain team for joint [co-marketing](/oss/python/contributing/comarketing).

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/contributing/integrations-langchain.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Contributing to code](/oss/python/contributing/code)[Implement a LangChain integration](/oss/python/contributing/implement-langchain)