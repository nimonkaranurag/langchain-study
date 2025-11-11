We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

* [Overview](/oss/python/integrations/providers/overview)

* [All providers](/oss/python/integrations/providers/all_providers)

##### Popular Providers

* [OpenAI](/oss/python/integrations/providers/openai)
* [Anthropic (Claude)](/oss/python/integrations/providers/anthropic)
* [Google](/oss/python/integrations/providers/google)
* [AWS (Amazon)](/oss/python/integrations/providers/aws)
* [Hugging Face](/oss/python/integrations/providers/huggingface)
* [Microsoft](/oss/python/integrations/providers/microsoft)
* [Ollama](/oss/python/integrations/providers/ollama)
* [Groq](/oss/python/integrations/providers/groq)

##### Integrations by component

* [Chat models](/oss/python/integrations/chat)
* [Tools and toolkits](/oss/python/integrations/tools)
* [Retrievers](/oss/python/integrations/retrievers)
* [Text splitters](/oss/python/integrations/splitters)
* [Embedding models](/oss/python/integrations/text_embedding)
* [Vector stores](/oss/python/integrations/vectorstores)
* [Document loaders](/oss/python/integrations/document_loaders)
* [Key-value stores](/oss/python/integrations/stores)

* [Integration details](#integration-details)
* [Model features](#model-features)
* [Setup](#setup)
* [Chat models](#chat-models)
* [Instantiation](#instantiation)
* [Invocation](#invocation)
* [Multimodal usage](#multimodal-usage)
* [Image input](#image-input)
* [Audio input](#audio-input)
* [Video input](#video-input)
* [Image generation](#image-generation)
* [Tool calling](#tool-calling)
* [Structured output](#structured-output)
* [Structured output methods](#structured-output-methods)
* [Token usage tracking](#token-usage-tracking)
* [Built-in tools](#built-in-tools)
* [Native async](#native-async)
* [Safety settings](#safety-settings)
* [API reference](#api-reference)

# ChatGoogleGenerativeAI

Access Google’s Generative AI models, including the Gemini family, directly via the Gemini API or experiment rapidly using Google AI Studio. The `langchain-google-genai` package provides the LangChain integration for these models. This is often the best starting point for individual developers. For information on the latest models, their features, context windows, etc. head to the [Google AI docs](https://ai.google.dev/gemini-api/docs). All model IDs can be found in the [Gemini API docs](https://ai.google.dev/gemini-api/docs/models).

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | [JS support](https://js.langchain.com/docs/integrations/chat/google_generative_ai) | Downloads | Version |
| --- | --- | --- | --- | --- | --- | --- |
| [`ChatGoogleGenerativeAI`](https://python.langchain.com/api_reference/google_genai/chat_models/langchain_google_genai.chat_models.ChatGoogleGenerativeAI.html) | [`langchain-google-genai`](https://python.langchain.com/api_reference/google_genai/index.html) | ❌ | beta | ✅ |

### [​](#model-features) Model features

| [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | JSON mode | [Image input](/oss/python/langchain/messages#multimodal) | Audio input | Video input | [Token-level streaming](/oss/python/langchain/streaming) | Native async | [Token usage](/oss/python/langchain/models#token-usage) | [Logprobs](/oss/python/langchain/models#log-probabilities) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

### [​](#setup) Setup

To access Google AI models you’ll need to create a Google Account, get a Google AI API key, and install the `langchain-google-genai` integration package. **Installation:**

Copy

Ask AI

```
pip install -U langchain-google-genai pip install - U langchain - google - genai
```

**Credentials:** Head to <https://ai.google.dev/gemini-api/docs/api-key> (or via Google AI Studio) to generate a Google AI API key.

### [​](#chat-models) Chat models

Use the `ChatGoogleGenerativeAI` class to interact with Google’s chat models. See the [API reference](https://python.langchain.com/api_reference/google_genai/chat_models/langchain_google_genai.chat_models.ChatGoogleGenerativeAI.html) for full details.

Copy

Ask AI

```
import getpass import  getpass import os import  os if "GOOGLE_API_KEY" not in os.environ: if  "GOOGLE_API_KEY"  not  in os.environ: os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ") os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](https://docs.smith.langchain.com/) API key:

Copy

Ask AI

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")os.environ["LANGSMITH_TRACING"] = "true"os.environ["LANGSMITH_TRACING"] =  "true"
```

## [​](#instantiation) Instantiation

Now we can instantiate our model object and generate chat completions:

Copy

Ask AI

```
from langchain_google_genai import ChatGoogleGenerativeAI from  langchain_google_genai import  ChatGoogleGenerativeAI llm = ChatGoogleGenerativeAI(llm = ChatGoogleGenerativeAI( model="gemini-2.5-flash",  model ="gemini-2.5-flash", temperature=0,  temperature = 0, max_tokens=None,  max_tokens = None, timeout=None,  timeout = None, max_retries=2,  max_retries = 2, # other params... # other params...))
```

## [​](#invocation) Invocation

Copy

Ask AI

```
messages = [messages = [ ( ( "system",  "system", "You are a helpful assistant that translates English to French. Translate the user sentence.", "You are a helpful assistant that translates English to French. Translate the user sentence.", ), ), ("human", "I love programming."), ("human", "I love programming."),]]ai_msg = llm.invoke(messages) ai_msg = llm.invoke(messages) ai_msg ai_msg
```

Copy

Ask AI

```
AIMessage(content="J'adore la programmation.", additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash', 'safety_ratings': []}, id='run-3b28d4b8-8a62-4e6c-ad4e-b53e6e825749-0', usage_metadata={'input_tokens': 20, 'output_tokens': 7, 'total_tokens': 27, 'input_token_details': {'cache_read': 0}})AIMessage(content="J'adore la programmation.", additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash', 'safety_ratings': []}, id='run-3b28d4b8-8a62-4e6c-ad4e-b53e6e825749-0', usage_metadata={'input_tokens': 20, 'output_tokens': 7, 'total_tokens': 27, 'input_token_details': {'cache_read': 0}}) 
```

Copy

Ask AI

```
print(ai_msg.content) print(ai_msg.content)
```

Copy

Ask AI

```
J'adore la programmation.J'adore la programmation. 
```

## [​](#multimodal-usage) Multimodal usage

Gemini models can accept multimodal inputs (text, images, audio, video) and, for some models, generate multimodal outputs.

### [​](#image-input) Image input

Provide image inputs along with text using a [`HumanMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.HumanMessage) with a list content format. Make sure to use a model that supports image input, such as `gemini-2.5-flash`.

Copy

Ask AI

```
import base64 import  base64 from langchain.messages import HumanMessage from langchain.messages import  HumanMessage from langchain_google_genai import ChatGoogleGenerativeAI from  langchain_google_genai import  ChatGoogleGenerativeAI # Example using a public URL (remains the same)# Example using a public URL (remains the same)message_url = HumanMessage(message_url = HumanMessage( content=[ content =[ { { "type": "text",  "type": "text", "text": "Describe the image at the URL.",  "text": "Describe the image at the URL.", }, }, {"type": "image_url", "image_url": "https://picsum.photos/seed/picsum/200/300"}, {"type": "image_url", "image_url": "https://picsum.photos/seed/picsum/200/300"}, ] ]))result_url = llm.invoke([message_url]) result_url = llm.invoke([message_url])print(f"Response for URL image: {result_url.content}") print(f"Response for URL image: {result_url.content} ") # Example using a local image file encoded in base64 # Example using a local image file encoded in base64image_file_path = "/Users/philschmid/projects/google-gemini/langchain/docs/static/img/agents_vs_chains.png" image_file_path = "/Users/philschmid/projects/google-gemini/langchain/docs/static/img/agents_vs_chains.png" with open(image_file_path, "rb") as image_file: with  open(image_file_path, "rb") as image_file: encoded_image = base64.b64encode(image_file.read()).decode("utf-8")  encoded_image = base64.b64encode(image_file.read()).decode("utf-8") message_local = HumanMessage(message_local = HumanMessage( content=[ content =[ {"type": "text", "text": "Describe the local image."}, {"type": "text", "text": "Describe the local image."}, {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"}, {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image} "}, ] ]))result_local = llm.invoke([message_local]) result_local = llm.invoke([message_local])print(f"Response for local image: {result_local.content}") print(f"Response for local image: {result_local.content} ")
```

Other supported `image_url` formats:

* A Google Cloud Storage URI (`gs://...`). Ensure the service account has access.
* A PIL Image object (the library handles encoding).

### [​](#audio-input) Audio input

Provide audio file inputs along with text.

Copy

Ask AI

```
import base64 import  base64 from langchain.messages import HumanMessage from langchain.messages import  HumanMessage # Ensure you have an audio file named 'example_audio.mp3' or provide the correct path.# Ensure you have an audio file named 'example_audio.mp3' or provide the correct path.audio_file_path = "example_audio.mp3" audio_file_path = "example_audio.mp3"audio_mime_type = "audio/mpeg" audio_mime_type = "audio/mpeg" with open(audio_file_path, "rb") as audio_file: with  open(audio_file_path, "rb") as audio_file: encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")  encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8") message = HumanMessage(message = HumanMessage( content=[ content =[ {"type": "text", "text": "Transcribe the audio."}, {"type": "text", "text": "Transcribe the audio."}, { { "type": "media",  "type": "media", "data": encoded_audio, # Use base64 string directly  "data": encoded_audio, # Use base64 string directly "mime_type": audio_mime_type,  "mime_type": audio_mime_type, }, }, ] ]))response = llm.invoke([message]) # Uncomment to run response = llm.invoke([message]) # Uncomment to runprint(f"Response for audio: {response.content}") print(f"Response for audio: {response.content} ")
```

### [​](#video-input) Video input

Provide video file inputs along with text.

Copy

Ask AI

```
import base64 import  base64 from langchain.messages import HumanMessage from langchain.messages import  HumanMessage from langchain_google_genai import ChatGoogleGenerativeAI from  langchain_google_genai import  ChatGoogleGenerativeAI # Ensure you have a video file named 'example_video.mp4' or provide the correct path.# Ensure you have a video file named 'example_video.mp4' or provide the correct path.video_file_path = "example_video.mp4" video_file_path = "example_video.mp4"video_mime_type = "video/mp4" video_mime_type = "video/mp4" with open(video_file_path, "rb") as video_file: with  open(video_file_path, "rb") as video_file: encoded_video = base64.b64encode(video_file.read()).decode("utf-8")  encoded_video = base64.b64encode(video_file.read()).decode("utf-8") message = HumanMessage(message = HumanMessage( content=[ content =[ {"type": "text", "text": "Describe the first few frames of the video."}, {"type": "text", "text": "Describe the first few frames of the video."}, { { "type": "media",  "type": "media", "data": encoded_video, # Use base64 string directly  "data": encoded_video, # Use base64 string directly "mime_type": video_mime_type,  "mime_type": video_mime_type, }, }, ] ]))response = llm.invoke([message]) # Uncomment to run response = llm.invoke([message]) # Uncomment to runprint(f"Response for video: {response.content}") print(f"Response for video: {response.content} ")
```

### [​](#image-generation) Image generation

Certain models (such as `gemini-2.5-flash-image`) can generate text and images inline. You need to specify the desired `response_modalities`. See more information on the [Gemini API docs](https://ai.google.dev/gemini-api/docs/image-generation) for details.

Copy

Ask AI

```
# Running in a Jupyter notebook environment # Running in a Jupyter notebook environment import base64 import  base64 from IPython.display import Image, display from IPython.display import Image, displayfrom langchain.messages import AIMessage from langchain.messages import  AIMessagefrom langchain_google_genai import ChatGoogleGenerativeAI, Modality from  langchain_google_genai import ChatGoogleGenerativeAI, Modality llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-image") llm = ChatGoogleGenerativeAI(model ="models/gemini-2.5-flash-image") message = {message = { "role": "user",  "role": "user", "content": "Generate a photorealistic image of a cuddly cat wearing a hat.",  "content": "Generate a photorealistic image of a cuddly cat wearing a hat.",}} response = llm.invoke(response = llm.invoke( [message], [message], response_modalities=[Modality.TEXT, Modality.IMAGE],  response_modalities =[Modality. TEXT, Modality. IMAGE],)) def _get_image_base64(response: AIMessage) -> None: def  _get_image_base64(response: AIMessage) -> None: image_block = next( image_block =  next( block  block for block in response.content  for  block in response.content if isinstance(block, dict) and block.get("image_url")  if  isinstance(block, dict) and block.get("image_url") ) ) return image_block["image_url"].get("url").split(",")[-1]  return image_block["image_url"].get("url").split(",")[- 1] image_base64 = _get_image_base64(response) image_base64 = _get_image_base64(response)display(Image(data=base64.b64decode(image_base64), width=300))display(Image(data =base64.b64decode(image_base64), width = 300))
```

## [​](#tool-calling) Tool calling

You can equip the model with tools to call.

Copy

Ask AI

```
from langchain.tools import tool from langchain.tools import  tool from langchain_google_genai import ChatGoogleGenerativeAI from  langchain_google_genai import  ChatGoogleGenerativeAI  # Define the tool # Define the tool@tool(description="Get the current weather in a given location") @tool(description = "Get the current weather in a given location")def get_weather(location: str) -> str: def  get_weather(location: str) -> str: return "It's sunny."  return "It's sunny."  # Initialize the model and bind the tool # Initialize the model and bind the toolllm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite") llm = ChatGoogleGenerativeAI(model ="gemini-2.5-flash-lite")llm_with_tools = llm.bind_tools([get_weather]) llm_with_tools = llm.bind_tools([get_weather]) # Invoke the model with a query that should trigger the tool # Invoke the model with a query that should trigger the toolquery = "What's the weather in San Francisco?" query =  "What's the weather in San Francisco?"ai_msg = llm_with_tools.invoke(query) ai_msg = llm_with_tools.invoke(query) # Check the tool calls in the response # Check the tool calls in the responseprint(ai_msg.tool_calls) print(ai_msg.tool_calls) # Example tool call message would be needed here if you were actually running the tool # Example tool call message would be needed here if you were actually running the toolfrom langchain.messages import ToolMessage from langchain.messages import  ToolMessage tool_message = ToolMessage(tool_message = ToolMessage( content=get_weather(*ai_msg.tool_calls[0]["args"]),  content =get_weather(*ai_msg.tool_calls[0]["args"]), tool_call_id=ai_msg.tool_calls[0]["id"],  tool_call_id =ai_msg.tool_calls[0]["id"],))llm_with_tools.invoke([ai_msg, tool_message]) # Example of passing tool result backllm_with_tools.invoke([ai_msg, tool_message]) # Example of passing tool result back
```

Copy

Ask AI

```
[{'name': 'get_weather', 'args': {'location': 'San Francisco'}, 'id': 'a6248087-74c5-4b7c-9250-f335e642927c', 'type': 'tool_call'}][{'name': 'get_weather', 'args': {'location': 'San Francisco'}, 'id': 'a6248087-74c5-4b7c-9250-f335e642927c', 'type': 'tool_call'}] 
```

Copy

Ask AI

```
AIMessage(content="OK. It's sunny in San Francisco.", additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': []}, id='run-ac5bb52c-e244-4c72-9fbc-fb2a9cd7a72e-0', usage_metadata={'input_tokens': 29, 'output_tokens': 11, 'total_tokens': 40, 'input_token_details': {'cache_read': 0}})AIMessage(content="OK. It's sunny in San Francisco.", additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': []}, id='run-ac5bb52c-e244-4c72-9fbc-fb2a9cd7a72e-0', usage_metadata={'input_tokens': 29, 'output_tokens': 11, 'total_tokens': 40, 'input_token_details': {'cache_read': 0}}) 
```

## [​](#structured-output) Structured output

Force the model to respond with a specific structure using Pydantic models.

Copy

Ask AI

```
from langchain_core.pydantic_v1 import BaseModel, Field from langchain_core.pydantic_v1 import BaseModel, Field from langchain_google_genai import ChatGoogleGenerativeAI from  langchain_google_genai import  ChatGoogleGenerativeAI  # Define the desired structure # Define the desired structureclass Person(BaseModel): class  Person(BaseModel): """Information about a person.""" """Information about a person."""  name: str = Field(..., description="The person's name") name: str = Field(..., description = "The person's name") height_m: float = Field(..., description="The person's height in meters") height_m: float = Field(..., description = "The person's height in meters")  # Initialize the model # Initialize the modelllm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0) llm = ChatGoogleGenerativeAI(model ="gemini-2.5-flash-lite", temperature = 0) # Method 1: Default function calling approach# Method 1: Default function calling approachstructured_llm_default = llm.with_structured_output(Person) structured_llm_default = llm.with_structured_output(Person) # Method 2: Native JSON schema for better reliability (recommended)# Method 2: Native JSON schema for better reliability (recommended)structured_llm_json = llm.with_structured_output(Person, method="json_schema") structured_llm_json = llm.with_structured_output(Person, method = "json_schema") # Invoke the model with a query asking for structured information # Invoke the model with a query asking for structured informationresult = structured_llm_json.invoke(result = structured_llm_json.invoke( "Who was the 16th president of the USA, and how tall was he in meters?" "Who was the 16th president of the USA, and how tall was he in meters?"))print(result) print(result)
```

Copy

Ask AI

```
name='Abraham Lincoln' height_m=1.93name='Abraham Lincoln' height_m=1.93 
```

### [​](#structured-output-methods) Structured output methods

Two methods are supported for structured output:

* **`method="function_calling"` (default)**: Uses tool calling to extract structured data. Compatible with all Gemini models.
* **`method="json_schema"`** or **`method="json_mode"`**: Uses Gemini’s native structured output with `responseSchema`. More reliable but requires Gemini 1.5+ models. (`json_mode` is kept for backwards compatibility)

The `json_schema` method is **recommended for better reliability** as it constrains the model’s generation process directly rather than relying on post-processing tool calls.

## [​](#token-usage-tracking) Token usage tracking

Access token usage information from the response metadata.

Copy

Ask AI

```
from langchain_google_genai import ChatGoogleGenerativeAI from  langchain_google_genai import  ChatGoogleGenerativeAI llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite") llm = ChatGoogleGenerativeAI(model ="gemini-2.5-flash-lite") result = llm.invoke("Explain the concept of prompt engineering in one sentence.") result = llm.invoke("Explain the concept of prompt engineering in one sentence.") print(result.content) print(result.content)print("\nUsage Metadata:") print(" \nUsage Metadata:")print(result.usage_metadata) print(result.usage_metadata)
```

Copy

Ask AI

```
Prompt engineering is the art and science of crafting effective text prompts to elicit desired and accurate responses from large language models.Prompt engineering is the art and science of crafting effective text prompts to elicit desired and accurate responses from large language models. Usage Metadata:Usage Metadata:{'input_tokens': 10, 'output_tokens': 24, 'total_tokens': 34, 'input_token_details': {'cache_read': 0}}{'input_tokens': 10, 'output_tokens': 24, 'total_tokens': 34, 'input_token_details': {'cache_read': 0}} 
```

## [​](#built-in-tools) Built-in tools

Google Gemini supports a variety of built-in tools ([google search](https://ai.google.dev/gemini-api/docs/grounding/search-suggestions), [code execution](https://ai.google.dev/gemini-api/docs/code-execution?lang=python)), which can be bound to the model in the usual way.

Copy

Ask AI

```
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool from google.ai.generativelanguage_v1beta.types import  Tool as  GenAITool resp = llm.invoke(resp = llm.invoke( "When is the next total solar eclipse in US?",  "When is the next total solar eclipse in US?", tools=[GenAITool(google_search={})],  tools =[GenAITool(google_search ={})],)) print(resp.content) print(resp.content)
```

Copy

Ask AI

```
The next total solar eclipse visible in the United States will occur on August 23, 2044. However, the path of totality will only pass through Montana, North Dakota, and South Dakota.The next total solar eclipse visible in the United States will occur on August 23, 2044. However, the path of totality will only pass through Montana, North Dakota, and South Dakota. For a total solar eclipse that crosses a significant portion of the continental U.S., you'll have to wait until August 12, 2045. This eclipse will start in California and end in Florida.For a total solar eclipse that crosses a significant portion of the continental U.S., you'll have to wait until August 12, 2045. This eclipse will start in California and end in Florida. 
```

Copy

Ask AI

```
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool from google.ai.generativelanguage_v1beta.types import  Tool as  GenAITool resp = llm.invoke(resp = llm.invoke( "What is 2*2, use python", "What is 2*2, use python", tools=[GenAITool(code_execution={})],  tools =[GenAITool(code_execution ={})],)) for c in resp.content: for  c in resp.content: if isinstance(c, dict):  if  isinstance(c, dict): if c["type"] == "code_execution_result":  if c["type"] ==  "code_execution_result": print(f"Code execution result: {c['code_execution_result']}")  print(f"Code execution result: {c['code_execution_result']} ") elif c["type"] == "executable_code":  elif c["type"] ==  "executable_code": print(f"Executable code: {c['executable_code']}")  print(f"Executable code: {c['executable_code']} ") else:  else: print(c)  print(c)
```

Copy

Ask AI

```
Executable code: print(2*2)Executable code: print(2*2) Code execution result: 4Code execution result: 4 2*2 is 4.2*2 is 4. 
```

## [​](#native-async) Native async

Use asynchronous methods for non-blocking calls.

Copy

Ask AI

```
from langchain_google_genai import ChatGoogleGenerativeAI from  langchain_google_genai import  ChatGoogleGenerativeAI llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") llm = ChatGoogleGenerativeAI(model ="gemini-2.5-flash") async def run_async_calls(): async  def  run_async_calls():  # Async invoke  # Async invoke result_ainvoke = await llm.ainvoke("Why is the sky blue?")  result_ainvoke =  await llm.ainvoke("Why is the sky blue?") print("Async Invoke Result:", result_ainvoke.content[:50] + "...")  print("Async Invoke Result:", result_ainvoke.content[: 50] + "...")  # Async stream  # Async stream print("\nAsync Stream Result:")  print(" \nAsync Stream Result:") async for chunk in llm.astream( async  for  chunk in llm.astream( "Write a short poem about asynchronous programming." "Write a short poem about asynchronous programming." ): ): print(chunk.content, end="", flush=True)  print(chunk.content, end = "", flush = True) print("\n")  print(" \n ")  # Async batch  # Async batch results_abatch = await llm.abatch(["What is 1+1?", "What is 2+2?"])  results_abatch =  await llm.abatch(["What is 1+1?", "What is 2+2?"]) print("Async Batch Results:", [res.content for res in results_abatch])  print("Async Batch Results:", [res.content for  res in results_abatch]) await run_async_calls() await run_async_calls()
```

Copy

Ask AI

```
Async Invoke Result: The sky is blue due to a phenomenon called **Rayle...Async Invoke Result: The sky is blue due to a phenomenon called **Rayle... Async Stream Result:Async Stream Result:The thread is free, it does not wait,The thread is free, it does not wait,For answers slow, or tasks of fate.For answers slow, or tasks of fate.A promise made, a future bright,A promise made, a future bright,It moves ahead, with all its might.It moves ahead, with all its might. A callback waits, a signal sent,A callback waits, a signal sent,When data's read, or job is spent.When data's read, or job is spent.Non-blocking code, a graceful dance,Non-blocking code, a graceful dance,Responsive apps, a fleeting glance.Responsive apps, a fleeting glance. Async Batch Results: ['1 + 1 = 2', '2 + 2 = 4']Async Batch Results: ['1 + 1 = 2', '2 + 2 = 4'] 
```

## [​](#safety-settings) Safety settings

Gemini models have default safety settings that can be overridden. If you are receiving lots of “Safety Warnings” from your models, you can try tweaking the `safety_settings` attribute of the model. For example, to turn off safety blocking for dangerous content, you can construct your LLM as follows:

Copy

Ask AI

```
from langchain_google_genai import (from  langchain_google_genai import ( ChatGoogleGenerativeAI, ChatGoogleGenerativeAI, HarmBlockThreshold, HarmBlockThreshold, HarmCategory, HarmCategory,)) llm = ChatGoogleGenerativeAI(llm = ChatGoogleGenerativeAI( model="gemini-1.5-pro",  model ="gemini-1.5-pro", safety_settings={ safety_settings ={ HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory. HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold. BLOCK_NONE, }, },))
```

For an enumeration of the categories and thresholds available, see Google’s [safety setting types](https://ai.google.dev/api/python/google/generativeai/types/SafetySettingDict). 

---

## [​](#api-reference) API reference

For detailed documentation of all `ChatGoogleGenerativeAI` features and configurations head to the [API reference](https://python.langchain.com/api_reference/google_genai/chat_models/langchain_google_genai.chat_models.ChatGoogleGenerativeAI.html). 

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat/google_generative_ai.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?