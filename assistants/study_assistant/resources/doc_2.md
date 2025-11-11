We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

##### LangChain v1.0

* [Release notes](/oss/python/releases/langchain-v1)
* [Migration guide](/oss/python/migrate/langchain-v1)

##### Get started

##### Core components

* [Messages](/oss/python/langchain/messages)
* [Short-term memory](/oss/python/langchain/short-term-memory)

* [Structured output](/oss/python/langchain/structured-output)

##### Advanced usage

* [Context engineering](/oss/python/langchain/context-engineering)
* [Model Context Protocol (MCP)](/oss/python/langchain/mcp)


* [Long-term memory](/oss/python/langchain/long-term-memory)

##### Use in production

* [Agent Chat UI](/oss/python/langchain/ui)

* [Basic usage](#basic-usage)
* [Text prompts](#text-prompts)
* [Message prompts](#message-prompts)
* [Dictionary format](#dictionary-format)
* [Message types](#message-types)
* [System Message](#system-message)
* [Human Message](#human-message)
* [Text content](#text-content)
* [Message metadata](#message-metadata)
* [AI Message](#ai-message)
* [Tool calls](#tool-calls)
* [Token usage](#token-usage)
* [Streaming and chunks](#streaming-and-chunks)
* [Tool Message](#tool-message)
* [Message content](#message-content)
* [Standard content blocks](#standard-content-blocks)
* [Multimodal](#multimodal)
* [Content block reference](#content-block-reference)
* [Use with chat models](#use-with-chat-models)

[Core components](/oss/python/langchain/agents)

# Messages

Messages are the fundamental unit of context for models in LangChain. They represent the input and output of models, carrying both the content and metadata needed to represent the state of a conversation when interacting with an LLM. Messages are objects that contain:

* [**Role**](#message-types) - Identifies the message type (e.g. `system`, `user`)
* [**Content**](#message-content) - Represents the actual content of the message (like text, images, audio, documents, etc.)
* [**Metadata**](#message-metadata) - Optional fields such as response information, message IDs, and token usage

LangChain provides a standard message type that works across all model providers, ensuring consistent behavior regardless of the model being called.

## [​](#basic-usage) Basic usage

The simplest way to use messages is to create message objects and pass them to a model when [invoking](/oss/python/langchain/models#invocation).

Copy

Ask AI

```
from langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_modelfrom langchain.messages import HumanMessage, AIMessage, SystemMessage from langchain.messages import HumanMessage, AIMessage, SystemMessage model = init_chat_model("gpt-5-nano") model = init_chat_model("gpt-5-nano") system_msg = SystemMessage("You are a helpful assistant.") system_msg = SystemMessage("You are a helpful assistant.")human_msg = HumanMessage("Hello, how are you?") human_msg = HumanMessage("Hello, how are you?") # Use with chat models # Use with chat modelsmessages = [system_msg, human_msg] messages = [system_msg, human_msg]response = model.invoke(messages) # Returns AIMessage response = model.invoke(messages) # Returns AIMessage
```

### [​](#text-prompts) Text prompts

Text prompts are strings - ideal for straightforward generation tasks where you don’t need to retain conversation history.

Copy

Ask AI

```
response = model.invoke("Write a haiku about spring") response = model.invoke("Write a haiku about spring")
```

**Use text prompts when:**

* You have a single, standalone request
* You don’t need conversation history
* You want minimal code complexity

### [​](#message-prompts) Message prompts

Alternatively, you can pass in a list of messages to the model by providing a list of message objects.

Copy

Ask AI

```
from langchain.messages import SystemMessage, HumanMessage, AIMessage from langchain.messages import SystemMessage, HumanMessage, AIMessage messages = [messages = [ SystemMessage("You are a poetry expert"), SystemMessage("You are a poetry expert"), HumanMessage("Write a haiku about spring"), HumanMessage("Write a haiku about spring"), AIMessage("Cherry blossoms bloom...") AIMessage("Cherry blossoms bloom...")]]response = model.invoke(messages) response = model.invoke(messages)
```

**Use message prompts when:**

* Managing multi-turn conversations
* Working with multimodal content (images, audio, files)
* Including system instructions

### [​](#dictionary-format) Dictionary format

You can also specify messages directly in OpenAI chat completions format.

Copy

Ask AI

```
messages = [messages = [ {"role": "system", "content": "You are a poetry expert"}, {"role": "system", "content": "You are a poetry expert"}, {"role": "user", "content": "Write a haiku about spring"}, {"role": "user", "content": "Write a haiku about spring"}, {"role": "assistant", "content": "Cherry blossoms bloom..."} {"role": "assistant", "content": "Cherry blossoms bloom..."}]]response = model.invoke(messages) response = model.invoke(messages)
```

## [​](#message-types) Message types

* [System message](#system-message) - Tells the model how to behave and provide context for interactions
* [Human message](#human-message) - Represents user input and interactions with the model
* [AI message](#ai-message) - Responses generated by the model, including text content, tool calls, and metadata
* [Tool message](#tool-message) - Represents the outputs of [tool calls](/oss/python/langchain/models#tool-calling)

### [​](#system-message) System Message

A [`SystemMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.SystemMessage) represent an initial set of instructions that primes the model’s behavior. You can use a system message to set the tone, define the model’s role, and establish guidelines for responses.

Basic instructions

Copy

Ask AI

```
system_msg = SystemMessage("You are a helpful coding assistant.") system_msg = SystemMessage("You are a helpful coding assistant.") messages = [messages = [ system_msg, system_msg, HumanMessage("How do I create a REST API?") HumanMessage("How do I create a REST API?")]]response = model.invoke(messages) response = model.invoke(messages)
```

Detailed persona

Copy

Ask AI

```
from langchain.messages import SystemMessage, HumanMessage from langchain.messages import SystemMessage, HumanMessage system_msg = SystemMessage(""" system_msg = SystemMessage("""You are a senior Python developer with expertise in web frameworks.You are a senior Python developer with expertise in web frameworks.Always provide code examples and explain your reasoning.Always provide code examples and explain your reasoning.Be concise but thorough in your explanations.Be concise but thorough in your explanations.""") """) messages = [messages = [ system_msg, system_msg, HumanMessage("How do I create a REST API?") HumanMessage("How do I create a REST API?")]]response = model.invoke(messages) response = model.invoke(messages)
```

---

### [​](#human-message) Human Message

A [`HumanMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.HumanMessage) represents user input and interactions. They can contain text, images, audio, files, and any other amount of multimodal [content](#message-content).

#### [​](#text-content) Text content

Copy

Ask AI

```
response = model.invoke([response = model.invoke([ HumanMessage("What is machine learning?") HumanMessage("What is machine learning?")])])
```

#### [​](#message-metadata) Message metadata

Add metadata

Copy

Ask AI

```
human_msg = HumanMessage(human_msg = HumanMessage( content="Hello!",  content ="Hello!", name="alice", # Optional: identify different users  name = "alice", # Optional: identify different users id="msg_123", # Optional: unique identifier for tracing  id = "msg_123", # Optional: unique identifier for tracing))
```

The `name` field behavior varies by provider - some use it for user identification, others ignore it. To check, refer to the model provider’s [reference](https://reference.langchain.com/python/integrations/).

---

### [​](#ai-message) AI Message

An [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) represents the output of a model invocation. They can include multimodal data, tool calls, and provider-specific metadata that you can later access.

Copy

Ask AI

```
response = model.invoke("Explain AI") response = model.invoke("Explain AI")print(type(response)) # print(type(response)) # 
```

[`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) objects are returned by the model when calling it, which contains all of the associated metadata in the response. Providers weigh/contextualize types of messages differently, which means it is sometimes helpful to manually create a new [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) object and insert it into the message history as if it came from the model.

Copy

Ask AI

```
from langchain.messages import AIMessage, SystemMessage, HumanMessage from langchain.messages import AIMessage, SystemMessage, HumanMessage # Create an AI message manually (e.g., for conversation history)# Create an AI message manually (e.g., for conversation history)ai_msg = AIMessage("I'd be happy to help you with that question!") ai_msg = AIMessage("I'd be happy to help you with that question!") # Add to conversation history # Add to conversation historymessages = [messages = [ SystemMessage("You are a helpful assistant"), SystemMessage("You are a helpful assistant"), HumanMessage("Can you help me?"), HumanMessage("Can you help me?"), ai_msg, # Insert as if it came from the model ai_msg, # Insert as if it came from the model HumanMessage("Great! What's 2+2?") HumanMessage("Great! What's 2+2?")]] response = model.invoke(messages) response = model.invoke(messages)
```

Attributes

[​](#param-text)

text

string

The text content of the message.

[​](#param-content)

content

string | dict[]

The raw content of the message.

[​](#param-content-blocks)

content\_blocks

ContentBlock[]

The standardized [content blocks](#message-content) of the message.

[​](#param-tool-calls)

tool\_calls

dict[] | None

The tool calls made by the model. Empty if no tools are called.

[​](#param-id)

id

string

A unique identifier for the message (either automatically generated by LangChain or returned in the provider response)

[​](#param-usage-metadata)

usage\_metadata

dict | None

The usage metadata of the message, which can contain token counts when available.

[​](#param-response-metadata)

response\_metadata

ResponseMetadata | None

The response metadata of the message.

#### [​](#tool-calls) Tool calls

When models make [tool calls](/oss/python/langchain/models#tool-calling), they’re included in the [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage):

Copy

Ask AI

```
from langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_model model = init_chat_model("gpt-5-nano") model = init_chat_model("gpt-5-nano") def get_weather(location: str) -> str: def  get_weather(location: str) -> str: """Get the weather at a location.""" """Get the weather at a location.""" ... ... model_with_tools = model.bind_tools([get_weather]) model_with_tools = model.bind_tools([get_weather])response = model_with_tools.invoke("What's the weather in Paris?") response = model_with_tools.invoke("What's the weather in Paris?") for tool_call in response.tool_calls: for  tool_call in response.tool_calls: print(f"Tool: {tool_call['name']}")  print(f"Tool: {tool_call['name']} ") print(f"Args: {tool_call['args']}")  print(f"Args: {tool_call['args']} ") print(f"ID: {tool_call['id']}")  print(f"ID: {tool_call['id']} ")
```

Other structured data, such as reasoning or citations, can also appear in message [content](/oss/python/langchain/messages#message-content).

#### [​](#token-usage) Token usage

An [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) can hold token counts and other usage metadata in its [`usage_metadata`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.UsageMetadata) field:

Copy

Ask AI

```
from langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_model model = init_chat_model("gpt-5-nano") model = init_chat_model("gpt-5-nano") response = model.invoke("Hello!") response = model.invoke("Hello!")response.usage_metadataresponse.usage_metadata
```

Copy

Ask AI

```
{'input_tokens': 8,{'input_tokens': 8, 'output_tokens': 304, 'output_tokens': 304, 'total_tokens': 312, 'total_tokens': 312, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 256}} 'output_token_details': {'audio': 0, 'reasoning': 256}} 
```

See [`UsageMetadata`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.UsageMetadata) for details.

#### [​](#streaming-and-chunks) Streaming and chunks

During streaming, you’ll receive [`AIMessageChunk`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessageChunk) objects that can be combined into a full message object:

Copy

Ask AI

```
chunks = [] chunks = []full_message = None full_message =  Nonefor chunk in model.stream("Hi"): for  chunk in model.stream("Hi"): chunks.append(chunk) chunks.append(chunk) print(chunk.text)  print(chunk.text) full_message = chunk if full_message is None else full_message + chunk  full_message =  chunk if  full_message is  None  else  full_message +  chunk
```

Learn more:

* [Streaming tokens from chat models](/oss/python/langchain/models#stream)
* [Streaming tokens and/or steps from agents](/oss/python/langchain/streaming)

---

### [​](#tool-message) Tool Message

For models that support [tool calling](/oss/python/langchain/models#tool-calling), AI messages can contain tool calls. Tool messages are used to pass the results of a single tool execution back to the model. [Tools](/oss/python/langchain/tools) can generate [`ToolMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage) objects directly. Below, we show a simple example. Read more in the [tools guide](/oss/python/langchain/tools).

Copy

Ask AI

```
# After a model makes a tool call # After a model makes a tool callai_message = AIMessage(ai_message = AIMessage( content=[],  content =[], tool_calls=[{ tool_calls =[{ "name": "get_weather",  "name": "get_weather", "args": {"location": "San Francisco"},  "args": {"location": "San Francisco"}, "id": "call_123"  "id": "call_123" }] }])) # Execute tool and create result message # Execute tool and create result messageweather_result = "Sunny, 72°F" weather_result = "Sunny, 72°F"tool_message = ToolMessage(tool_message = ToolMessage( content=weather_result,  content =weather_result, tool_call_id="call_123" # Must match the call ID  tool_call_id = "call_123"  # Must match the call ID)) # Continue conversation # Continue conversationmessages = [messages = [ HumanMessage("What's the weather in San Francisco?"), HumanMessage("What's the weather in San Francisco?"), ai_message, # Model's tool call ai_message, # Model's tool call tool_message, # Tool execution result tool_message, # Tool execution result]]response = model.invoke(messages) # Model processes the result response = model.invoke(messages) # Model processes the result
```

Attributes

[​](#param-content-1)

content

string

required

The stringified output of the tool call.

[​](#param-tool-call-id)

tool\_call\_id

string

required

The ID of the tool call that this message is responding to. (this must match the ID of the tool call in the [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage))

[​](#param-name)

name

string

required

The name of the tool that was called.

[​](#param-artifact)

artifact

dict

Additional data not sent to the model but can be accessed programmatically.

The `artifact` field stores supplementary data that won’t be sent to the model but can be accessed programmatically. This is useful for storing raw results, debugging information, or data for downstream processing without cluttering the model’s context.

Example: Using artifact for retrieval metadata

For example, a [retrieval](/oss/python/langchain/retrieval) tool could retrieve a passage from a document for reference by a model. Where message `content` contains text that the model will reference, an `artifact` can contain document identifiers or other metadata that an application can use (e.g., to render a page). See example below:

Copy

Ask AI

```
from langchain.messages import ToolMessage from langchain.messages import  ToolMessage # Sent to model # Sent to modelmessage_content = "It was the best of times, it was the worst of times." message_content = "It was the best of times, it was the worst of times." # Artifact available downstream # Artifact available downstreamartifact = {"document_id": "doc_123", "page": 0} artifact = {"document_id": "doc_123", "page": 0} tool_message = ToolMessage(tool_message = ToolMessage( content=message_content,  content =message_content, tool_call_id="call_123",  tool_call_id = "call_123", name="search_books",  name = "search_books", artifact=artifact,  artifact =artifact,))
```

See the [RAG tutorial](/oss/python/langchain/rag) for an end-to-end example of building retrieval [agents](/oss/python/langchain/agents) with LangChain.

---

## [​](#message-content) Message content

You can think of a message’s content as the payload of data that gets sent to the model. Messages have a `content` attribute that is loosely-typed, supporting strings and lists of untyped objects (e.g., dictionaries). This allows support for provider-native structures directly in LangChain chat models, such as [multimodal](#multimodal) content and other data. Separately, LangChain provides dedicated content types for text, reasoning, citations, multi-modal data, server-side tool calls, and other message content. See [content blocks](#standard-content-blocks) below. LangChain chat models accept message content in the `content` attribute, and can contain:

1. A string
2. A list of content blocks in a provider-native format
3. A list of [LangChain’s standard content blocks](#standard-content-blocks)

See below for an example using [multimodal](#multimodal) inputs:

Copy

Ask AI

```
from langchain.messages import HumanMessage from langchain.messages import  HumanMessage # String content # String contenthuman_message = HumanMessage("Hello, how are you?") human_message = HumanMessage("Hello, how are you?") # Provider-native format (e.g., OpenAI)# Provider-native format (e.g., OpenAI)human_message = HumanMessage(content=[human_message = HumanMessage(content =[ {"type": "text", "text": "Hello, how are you?"}, {"type": "text", "text": "Hello, how are you?"}, {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}} {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}])]) # List of standard content blocks # List of standard content blockshuman_message = HumanMessage(content_blocks=[human_message = HumanMessage(content_blocks =[ {"type": "text", "text": "Hello, how are you?"}, {"type": "text", "text": "Hello, how are you?"}, {"type": "image", "url": "https://example.com/image.jpg"}, {"type": "image", "url": "https://example.com/image.jpg"},])])
```

Specifying `content_blocks` when initializing a message will still populate message `content`, but provides a type-safe interface for doing so.

### [​](#standard-content-blocks) Standard content blocks

LangChain provides a standard representation for message content that works across providers. Message objects implement a `content_blocks` property that will lazily parse the `content` attribute into a standard, type-safe representation. For example, messages generated from [ChatAnthropic](/oss/python/integrations/chat/anthropic) or [ChatOpenAI](/oss/python/integrations/chat/openai) will include `thinking` or `reasoning` blocks in the format of the respective provider, but can be lazily parsed into a consistent [`ReasoningContentBlock`](#content-block-reference) representation:

* Anthropic
* OpenAI

Copy

Ask AI

```
from langchain.messages import AIMessage from langchain.messages import  AIMessage message = AIMessage(message = AIMessage( content=[ content =[ {"type": "thinking", "thinking": "...", "signature": "WaUjzkyp..."}, {"type": "thinking", "thinking": "...", "signature": "WaUjzkyp..."}, {"type": "text", "text": "..."}, {"type": "text", "text": "..."}, ], ], response_metadata={"model_provider": "anthropic"}  response_metadata ={"model_provider": "anthropic"}))message.content_blocksmessage.content_blocks
```

Copy

Ask AI

```
[{'type': 'reasoning',[{'type': 'reasoning', 'reasoning': '...', 'reasoning': '...', 'extras': {'signature': 'WaUjzkyp...'}}, 'extras': {'signature': 'WaUjzkyp...'}}, {'type': 'text', 'text': '...'}] {'type': 'text', 'text': '...'}] 
```

See the [integrations guides](/oss/python/integrations/providers/overview) to get started with the inference provider of your choice.

**Serializing standard content**If an application outside of LangChain needs access to the standard content block representation, you can opt-in to storing content blocks in message content.To do this, you can set the `LC_OUTPUT_VERSION` environment variable to `v1`. Or, initialize any chat model with `output_version="v1"`:

Copy

Ask AI

```
from langchain.chat_models import init_chat_model from langchain.chat_models import  init_chat_model model = init_chat_model("gpt-5-nano", output_version="v1") model = init_chat_model("gpt-5-nano", output_version = "v1")
```

### [​](#multimodal) Multimodal

**Multimodality** refers to the ability to work with data that comes in different forms, such as text, audio, images, and video. LangChain includes standard types for these data that can be used across providers. [Chat models](/oss/python/langchain/models) can accept multimodal data as input and generate it as output. Below we show short examples of input messages featuring multimodal data.

Extra keys can be included top-level in the content block or nested in `"extras": {"key": value}`.[OpenAI](/oss/python/integrations/chat/openai#pdfs) and [AWS Bedrock Converse](/oss/python/integrations/chat/bedrock), for example, require a filename for PDFs. See the [provider page](/oss/python/integrations/providers/overview) for your chosen model for specifics.

Copy

Ask AI

```
# From URL # From URLmessage = {message = { "role": "user",  "role": "user", "content": [ "content": [ {"type": "text", "text": "Describe the content of this image."}, {"type": "text", "text": "Describe the content of this image."}, {"type": "image", "url": "https://example.com/path/to/image.jpg"}, {"type": "image", "url": "https://example.com/path/to/image.jpg"}, ] ]}} # From base64 data # From base64 datamessage = {message = { "role": "user",  "role": "user", "content": [ "content": [ {"type": "text", "text": "Describe the content of this image."}, {"type": "text", "text": "Describe the content of this image."}, { { "type": "image",  "type": "image", "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",  "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...", "mime_type": "image/jpeg",  "mime_type": "image/jpeg", }, }, ] ]}} # From provider-managed File ID# From provider-managed File IDmessage = {message = { "role": "user",  "role": "user", "content": [ "content": [ {"type": "text", "text": "Describe the content of this image."}, {"type": "text", "text": "Describe the content of this image."}, {"type": "image", "file_id": "file-abc123"}, {"type": "image", "file_id": "file-abc123"}, ] ]}}
```

Not all models support all file types. Check the model provider’s [reference](https://reference.langchain.com/python/integrations/) for supported formats and size limits.

### [​](#content-block-reference) Content block reference

Content blocks are represented (either when creating a message or accessing the `content_blocks` property) as a list of typed dictionaries. Each item in the list must adhere to one of the following block types:

Core

TextContentBlock

**Purpose:** Standard text output

[​](#param-type)

type

string

required

Always `"text"`

[​](#param-text-1)

text

string

required

The text content

[​](#param-annotations)

annotations

object[]

List of annotations for the text

[​](#param-extras)

extras

object

Additional provider-specific data

**Example:**

Copy

Ask AI

```
{{ "type": "text",  "type": "text", "text": "Hello world",  "text": "Hello world", "annotations": []  "annotations": []}}
```

ReasoningContentBlock

**Purpose:** Model reasoning steps

[​](#param-type-1)

type

string

required

Always `"reasoning"`

[​](#param-reasoning)

reasoning

string

The reasoning content

[​](#param-extras-1)

extras

object

Additional provider-specific data

**Example:**

Copy

Ask AI

```
{{ "type": "reasoning",  "type": "reasoning", "reasoning": "The user is asking about...",  "reasoning": "The user is asking about...", "extras": {"signature": "abc123"},  "extras": {"signature": "abc123"},}}
```

Multimodal

ImageContentBlock

**Purpose:** Image data

[​](#param-type-2)

type

string

required

Always `"image"`

[​](#param-url)

url

string

URL pointing to the image location.

[​](#param-base64)

base64

string

Base64-encoded image data.

[​](#param-id-1)

id

string

Reference ID to an externally stored image (e.g., in a provider’s file system or in a bucket).

[​](#param-mime-type)

mime\_type

string

Image [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#image) (e.g., `image/jpeg`, `image/png`)

AudioContentBlock

**Purpose:** Audio data

[​](#param-type-3)

type

string

required

Always `"audio"`

[​](#param-url-1)

url

string

URL pointing to the audio location.

[​](#param-base64-1)

base64

string

Base64-encoded audio data.

[​](#param-id-2)

id

string

Reference ID to an externally stored audio file (e.g., in a provider’s file system or in a bucket).

[​](#param-mime-type-1)

mime\_type

string

Audio [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#audio) (e.g., `audio/mpeg`, `audio/wav`)

VideoContentBlock

**Purpose:** Video data

[​](#param-type-4)

type

string

required

Always `"video"`

[​](#param-url-2)

url

string

URL pointing to the video location.

[​](#param-base64-2)

base64

string

Base64-encoded video data.

[​](#param-id-3)

id

string

Reference ID to an externally stored video file (e.g., in a provider’s file system or in a bucket).

[​](#param-mime-type-2)

mime\_type

string

Video [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml#video) (e.g., `video/mp4`, `video/webm`)

FileContentBlock

**Purpose:** Generic files (PDF, etc)

[​](#param-type-5)

type

string

required

Always `"file"`

[​](#param-url-3)

url

string

URL pointing to the file location.

[​](#param-base64-3)

base64

string

Base64-encoded file data.

[​](#param-id-4)

id

string

Reference ID to an externally stored file (e.g., in a provider’s file system or in a bucket).

[​](#param-mime-type-3)

mime\_type

string

File [MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml) (e.g., `application/pdf`)

PlainTextContentBlock

**Purpose:** Document text (`.txt`, `.md`)

[​](#param-type-6)

type

string

required

Always `"text-plain"`

[​](#param-text-2)

text

string

The text content

[​](#param-mime-type-4)

mime\_type

string

[MIME type](https://www.iana.org/assignments/media-types/media-types.xhtml) of the text (e.g., `text/plain`, `text/markdown`)

Tool Calling

ToolCall

**Purpose:** Function calls

[​](#param-type-7)

type

string

required

Always `"tool_call"`

[​](#param-name-1)

name

string

required

Name of the tool to call

[​](#param-args)

args

object

required

Arguments to pass to the tool

[​](#param-id-5)

id

string

required

Unique identifier for this tool call

**Example:**

Copy

Ask AI

```
{{ "type": "tool_call",  "type": "tool_call", "name": "search",  "name": "search", "args": {"query": "weather"},  "args": {"query": "weather"}, "id": "call_123"  "id": "call_123"}}
```

ToolCallChunk

**Purpose:** Streaming tool call fragments

[​](#param-type-8)

type

string

required

Always `"tool_call_chunk"`

[​](#param-name-2)

name

string

Name of the tool being called

[​](#param-args-1)

args

string

Partial tool arguments (may be incomplete JSON)

[​](#param-id-6)

id

string

Tool call identifier

[​](#param-index)

index

number | string

Position of this chunk in the stream

InvalidToolCall

**Purpose:** Malformed calls, intended to catch JSON parsing errors.

[​](#param-type-9)

type

string

required

Always `"invalid_tool_call"`

[​](#param-name-3)

name

string

Name of the tool that failed to be called

[​](#param-args-2)

args

object

Arguments to pass to the tool

[​](#param-error)

error

string

Description of what went wrong

Server-Side Tool Execution

ServerToolCall

**Purpose:** Tool call that is executed server-side.

[​](#param-type-10)

type

string

required

Always `"server_tool_call"`

[​](#param-id-7)

id

string

required

An identifier associated with the tool call.

[​](#param-name-4)

name

string

required

The name of the tool to be called.

[​](#param-args-3)

args

string

required

Partial tool arguments (may be incomplete JSON)

**Purpose:** Streaming server-side tool call fragments

[​](#param-type-11)

type

string

required

Always `"server_tool_call_chunk"`

[​](#param-id-8)

id

string

An identifier associated with the tool call.

[​](#param-name-5)

name

string

Name of the tool being called

[​](#param-args-4)

args

string

Partial tool arguments (may be incomplete JSON)

[​](#param-index-1)

index

number | string

Position of this chunk in the stream

**Purpose:** Search results

[​](#param-type-12)

type

string

required

Always `"server_tool_result"`

[​](#param-tool-call-id-1)

tool\_call\_id

string

required

Identifier of the corresponding server tool call.

[​](#param-id-9)

id

string

Identifier associated with the server tool result.

[​](#param-status)

string

required

Execution status of the server-side tool. `"success"` or `"error"`.

[​](#param-output)

Output of the executed tool.

Provider-Specific Blocks

**Purpose:** Provider-specific escape hatch

[​](#param-type-13)

type

string

required

Always `"non_standard"`

[​](#param-value)

object

required

Provider-specific data structure

**Usage:** For experimental or provider-unique features

Additional provider-specific content types may be found within the [reference documentation](/oss/python/integrations/providers/overview) of each model provider.

View the canonical type definitions in the [API reference](https://reference.langchain.com/python/langchain/messages).

Content blocks were introduced as a new property on messages in LangChain v1 to standardize content formats across providers while maintaining backward compatibility with existing code. Content blocks are not a replacement for the [`content`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.messages.BaseMessage.content) property, but rather a new property that can be used to access the content of a message in a standardized format.

## [​](#use-with-chat-models) Use with chat models

[Chat models](/oss/python/langchain/models) accept a sequence of message objects as input and return an [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) as output. Interactions are often stateless, so that a simple conversational loop involves invoking a model with a growing list of messages. Refer to the below guides to learn more:

* Built-in features for [persisting and managing conversation histories](/oss/python/langchain/short-term-memory)
* Strategies for managing context windows, including [trimming and summarizing messages](/oss/python/langchain/short-term-memory#common-patterns)

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/messages.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Models](/oss/python/langchain/models)[Tools](/oss/python/langchain/tools)